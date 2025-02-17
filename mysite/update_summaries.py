import os
import django
import time
import google.api_core.exceptions
import google.generativeai as genai
import concurrent.futures  # ✅ 멀티스레딩 추가
from django.db import transaction  # ✅ 트랜잭션 추가
import threading

# ✅ Django 환경 설정 (설정 파일이 있는 프로젝트 경로 입력)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # "config"는 프로젝트명
django.setup()

from youtube_api.models import YouTubeVideo  # ✅ 이제 Django 환경이 로드된 상태에서 가져오기 가능!

# ✅ API 키 설정
import json
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    GEMINI_API_KEY = config["GEMINI_API_KEY"]

# ✅ Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(video):
    """Gemini를 이용해 자막 또는 설명을 요약"""
    model = genai.GenerativeModel("gemini-pro")
    captions = video.captions if video.captions else ""
    description = video.description if video.description else ""

    print(f"📡 [요약 시작] {video.video_id} (자막 길이: {len(captions)}, 설명 길이: {len(description)})")

    prompt_text = f"""다음은 한 영상의 자막과 설명입니다.
    - 자막: {captions[:2000]}
    - 설명: {description}
    위 내용을 바탕으로 2~3문장으로 요약해주세요."""

    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            print(f"📡 [API 요청] {video.video_id} (시도 {attempt + 1}/{retry_attempts})")

            # ✅ API 요청을 별도 스레드에서 실행하여 타임아웃 적용
            result = [None]
            def api_call():
                try:
                    response = model.generate_content(prompt_text)
                    result[0] = response
                except Exception as e:
                    result[0] = e

            thread = threading.Thread(target=api_call)
            thread.start()
            thread.join(timeout=60)  # ✅ 60초 대기 (타임아웃 설정)

            if isinstance(result[0], Exception):
                raise result[0]  # 오류 발생 시 예외 던지기

            response = result[0]

            if not response or not response.candidates:
                print(f"⚠️ Gemini API 응답 없음: {response}")
                return "요약 실패 (응답 없음)"

            candidate = response.candidates[0]
            if candidate.finish_reason == "SAFETY":
                print(f"⚠️ Gemini가 콘텐츠를 요약할 수 없음 (안전 문제 감지): {candidate.safety_ratings}")
                return "요약 실패 (안전 문제 감지)"

            print(f"✅ [요약 완료] {video.video_id}")
            return candidate.content.parts[0].text.strip() if candidate.content.parts else "요약 불가능"

        except google.api_core.exceptions.DeadlineExceeded:
            print(f"⚠️ 요청 시간이 초과됨 (Timeout)! {attempt + 1}/{retry_attempts}회 재시도 중...")
            time.sleep(5)

        except google.api_core.exceptions.ResourceExhausted:
            print(f"⚠️ Gemini API 할당량 초과! {attempt + 1}/{retry_attempts}회 재시도 중...")
            time.sleep(10)

        except Exception as e:
            print(f"⚠️ Gemini API 호출 오류: {e}")
            return "요약 실패"

    return "요약 실패 (할당량 초과)"

def process_video(video):
    """한 개의 영상을 처리하는 함수"""
    if video.summary:  # ✅ 이미 요약된 영상이면 건너뛰기
        print(f"✅ {video.video_id} 이미 요약됨, 건너뜀.")
        return

    # ✅ 중복 실행 방지 (최신 데이터 가져오기)
    video.refresh_from_db()
    if video.summary:
        print(f"🔄 {video.video_id} 다른 프로세스에서 이미 요약됨, 건너뜀.")
        return

    summary = generate_summary(video)

    # ✅ 트랜잭션 적용 (동시 수정 방지)
    with transaction.atomic():
        video.refresh_from_db()  # ✅ 최신 데이터 다시 가져오기 (동시 수정 방지)
        if not video.summary:  # ✅ 다른 스레드에서 먼저 업데이트한 경우 방지
            video.summary = summary
            video.save()
            print(f"✅ {video.video_id} 요약 완료")

def update_summaries():
    """DB에서 '요약 실패' 데이터를 포함하여 다시 요약 실행"""
    total_videos = YouTubeVideo.objects.filter(summary__in=[None, "요약 실패"]).count()
    print(f"🎯 총 요약해야 할 영상 개수: {total_videos}")

    while True:
        videos = YouTubeVideo.objects.filter(summary__in=[None, "요약 실패"])[:100]  # ✅ '요약 실패' 포함
        if not videos:
            print("✅ 모든 영상이 정상적으로 요약 완료됨!")
            break  # ✅ 더 이상 요약할 영상이 없으면 종료

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(process_video, videos)

        print(f"⏳ 다음 100개 요약 시작... (남은 영상: {YouTubeVideo.objects.filter(summary__in=[None, '요약 실패']).count()})")
        time.sleep(5)  # ✅ 요청 간 짧은 대기 (API 부담 완화)

if __name__ == "__main__":
    update_summaries()

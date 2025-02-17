import os
import django
import time
import google.api_core.exceptions
import google.generativeai as genai


# ✅ Django 환경 설정을 명확히 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # settings.py가 있는 Django 앱명 입력
django.setup()

from youtube_api.models import YouTubeVideo  # ✅ 이제 Django 환경이 로드된 상태에서 가져오기 가능!


# ✅ API 키 설정 (config.json에서 로드)
import json
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    GEMINI_API_KEY = config["GEMINI_API_KEY"]

# ✅ Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(captions, description):
    """Gemini를 이용해 자막 또는 설명을 요약"""
    model = genai.GenerativeModel("gemini-pro")

    if captions and len(captions) > 1000:
        prompt_text = f"""다음은 한 영상의 자막과 설명입니다.
        - 자막: {captions[:2000]}
        - 설명: {description}
        위 내용을 바탕으로 2~3문장으로 요약해주세요."""
    elif captions:
        prompt_text = f"이 영상의 자막을 2~3문장으로 요약해줘: {captions}"
    else:
        prompt_text = f"이 영상의 설명을 2~3문장으로 요약해줘: {description}"

    retry_attempts = 3  # 최대 3번 재시도
    for attempt in range(retry_attempts):
        try:
            response = model.generate_content(prompt_text)
            time.sleep(2)  # ✅ 각 요청 사이에 2초 대기 (할당량 초과 방지)

            # ✅ 응답이 없거나 안전성 문제로 차단된 경우 예외 처리
            if not response.candidates:
                print(f"⚠️ Gemini API 응답 없음: {response}")
                return "요약 실패 (응답 없음)"

            candidate = response.candidates[0]
            if candidate.finish_reason == "SAFETY":
                print(f"⚠️ Gemini가 콘텐츠를 요약할 수 없음 (안전 문제 감지): {candidate.safety_ratings}")
                return "요약 실패 (안전 문제 감지)"

            return candidate.content.parts[0].text.strip() if candidate.content.parts else "요약 불가능"
        
        except google.api_core.exceptions.ResourceExhausted:
            print(f"⚠️ Gemini API 할당량 초과! {attempt + 1}/{retry_attempts}회 재시도 중...")
            time.sleep(5)  # ✅ 5초 대기 후 다시 시도
        except Exception as e:
            print(f"⚠️ Gemini API 호출 오류: {e}")
            return "요약 실패"

    return "요약 실패 (할당량 초과)"  # 3번 재시도 후에도 실패하면 오류 메시지 반환

def update_summaries():
    """DB에 저장된 모든 영상의 요약을 생성"""
    videos = YouTubeVideo.objects.all()

    for video in videos:
        if video.summary:  # ✅ 이미 요약이 있으면 건너뛰기
            print(f"✅ {video.video_id} 이미 요약됨, 건너뜀.")
            continue

        captions = video.captions if video.captions else ""
        summary = generate_summary(captions, video.description)

        # ✅ DB 업데이트
        video.summary = summary
        video.save()
        print(f"✅ {video.video_id} 요약 완료")

if __name__ == "__main__":
    update_summaries()

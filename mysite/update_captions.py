import os
import django
import time
from youtube_transcript_api import YouTubeTranscriptApi  # ✅ 자막 가져오는 라이브러리 추가

# ✅ Django 환경 설정을 명확히 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # settings.py가 있는 Django 앱명 입력
django.setup()

from youtube_api.models import YouTubeVideo  # ✅ Django 모델 가져오기

def get_captions(video_id):
    """YouTubeTranscriptApi를 이용해 해당 영상의 한국어 자막 가져오기"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko"])
        captions = "\n".join([f"{entry['start']} --> {entry['start'] + entry['duration']}\n{entry['text']}" for entry in transcript])
        return captions
    except Exception:
        return None  # 자막이 없으면 None 반환

def update_captions():
    """DB에 저장된 영상 중 captions(자막)이 없는 것만 업데이트"""
    videos = YouTubeVideo.objects.filter(captions__isnull=True) | YouTubeVideo.objects.filter(captions="")  # ✅ 자막이 없는 영상만 선택
    total_videos = videos.count()  # ✅ 전체 업데이트할 동영상 개수
    updated_videos = []
    
    print(f"\n🚀 총 {total_videos}개의 동영상에서 자막이 없으며, 업데이트를 진행합니다...\n")

    for index, video in enumerate(videos, start=1):
        start_time = time.time()  # ✅ 개별 영상 처리 시작 시간
        captions = get_captions(video.video_id)

        if captions:  # ✅ 새로운 자막이 있으면 업데이트 대기
            video.captions = captions
            updated_videos.append(video)
            status = "✅ 업데이트 완료"
        else:
            status = "❌ 자막 없음"

        elapsed_time = time.time() - start_time  # ✅ 처리 시간 계산
        progress = (index / total_videos) * 100  # ✅ 진행률 계산

        print(f"[{index}/{total_videos}] {progress:.2f}% | {video.video_id} | {status} ({elapsed_time:.2f}s)")

    if updated_videos:
        YouTubeVideo.objects.bulk_update(updated_videos, ["captions"])  # ✅ 일괄 업데이트로 속도 향상
        print(f"\n🎉 총 {len(updated_videos)}개의 영상 자막이 업데이트되었습니다.")
    else:
        print("\n✅ 업데이트할 자막이 없습니다.")

if __name__ == "__main__":
    update_captions()

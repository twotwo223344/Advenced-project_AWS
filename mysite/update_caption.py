import os
import django
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
    """DB에 저장된 모든 영상의 captions(자막)만 업데이트"""
    videos = YouTubeVideo.objects.all()
    updated_count = 0

    for video in videos:
        captions = get_captions(video.video_id)

        if captions:  # ✅ 새로운 자막이 있으면 업데이트
            video.captions = captions
            video.save()
            updated_count += 1
            print(f"✅ {video.video_id} 캡션 업데이트 완료")
        else:
            print(f"❌ {video.video_id} 자막 없음 (변경 없음)")

    print(f"\n🎉 총 {updated_count}개의 영상에 대한 자막이 업데이트되었습니다.")

if __name__ == "__main__":
    update_captions()

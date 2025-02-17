import os
import django

# ✅ Django 환경 설정을 명확히 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # settings.py가 있는 Django 앱명 입력
django.setup()

from youtube_api.models import YouTubeVideo  # ✅ Django 모델 가져오기

def delete_videos_without_captions():
    """자막이 없는 동영상 삭제 (사용자 확인 후 진행)"""
    videos_to_delete = YouTubeVideo.objects.filter(captions__isnull=True) | YouTubeVideo.objects.filter(captions="")  # ✅ 자막 없는 영상 필터링
    total_to_delete = videos_to_delete.count()  # ✅ 삭제 대상 개수

    if total_to_delete == 0:
        print("\n✅ 모든 영상에 자막이 있습니다. 삭제할 항목이 없습니다.")
        return

    print(f"\n🗑️ 총 {total_to_delete}개의 동영상이 자막이 없습니다.")
    print("삭제 대상 리스트:")
    for idx, video in enumerate(videos_to_delete, start=1):
        print(f"{idx}. {video.title} ({video.video_id})")

    # ✅ 사용자 확인 메시지
    confirm = input("\n정말 위의 동영상들을 삭제하시겠습니까? (y/N): ").strip().lower()

    if confirm == "y":
        videos_to_delete.delete()
        print(f"\n✅ 총 {total_to_delete}개의 동영상이 삭제되었습니다.")
    else:
        print("\n❌ 삭제가 취소되었습니다.")

if __name__ == "__main__":
    delete_videos_without_captions()

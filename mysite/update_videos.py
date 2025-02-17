import os
import django

# ✅ Django 환경 설정을 명확히 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # settings.py가 있는 Django 앱명 입력
django.setup()

from youtube_api.utils import update_videos_with_summary

if __name__ == "__main__":
    update_videos_with_summary()

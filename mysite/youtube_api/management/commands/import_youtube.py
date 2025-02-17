import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from youtube_api.models import YouTubeVideo  # ✅ 모델 가져오기

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # ✅ Django 환경 설정

class Command(BaseCommand):
    help = "youtube_api 폴더의 CSV 데이터를 데이터베이스에 삽입합니다."

    def handle(self, *args, **options):
        file_path = os.path.join(settings.BASE_DIR, "youtube_api", "youtube_videos.csv")

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"❌ CSV 파일을 찾을 수 없습니다: {file_path}"))
            return
        
        try:
            df = pd.read_csv(file_path)

            inserted_count = 0
            updated_count = 0

            for _, row in df.iterrows():
                print(f"📌 저장할 데이터: video_id={row['video_id']}, views={row['views']}, captions={row['captions']}, summary={row['summary']}")  # ✅ 데이터 확인용 출력

                obj, created = YouTubeVideo.objects.update_or_create(
                    video_id=row["video_id"],  # ✅ 기존 데이터가 있으면 업데이트
                    defaults={
                        "title": row["title"],
                        "description": row["description"],
                        "captions": row["captions"] if not pd.isna(row["captions"]) else "",
                        "views": int(row["views"]) if str(row["views"]).isdigit() else 0,
                        "summary": row["summary"] if not pd.isna(row["summary"]) else "",
                        "tags": row["tags"] if not pd.isna(row["tags"]) else "",  # ✅ tags 추가
                    }
                )

                if created:
                    inserted_count += 1
                else:
                    updated_count += 1

            self.stdout.write(self.style.SUCCESS(f"✅ {inserted_count}개 삽입, {updated_count}개 업데이트 완료!"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ 오류 발생: {e}"))

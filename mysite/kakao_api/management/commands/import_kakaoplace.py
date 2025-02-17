from django.core.management.base import BaseCommand
from django.conf import settings
import os
import pandas as pd
from kakao_api.models import kakaoplace  # ✅ 모델 가져오기

class Command(BaseCommand):
    help = "kakao_api 폴더의 CSV 데이터를 데이터베이스에 삽입 또는 업데이트합니다."

    def handle(self, *args, **options):
        # CSV 파일 경로 자동 설정
        file_path = os.path.join(settings.BASE_DIR, "kakao_api", "kakao_api_kakaoplace_summary.csv")

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"❌ CSV 파일을 찾을 수 없습니다: {file_path}"))
            return
        
        try:
            # ✅ CSV 파일 로드 (UTF-8 인코딩 사용)
            df = pd.read_csv(file_path, encoding="utf-8")

            # ✅ 유효한 카테고리 필터링
            valid_categories = {"restaurant", "cafe", "tour"}
            df = df[df["category"].isin(valid_categories)]

            # ✅ 데이터 삽입 또는 업데이트
            for _, row in df.iterrows():
                place, created = kakaoplace.objects.update_or_create(
                    name=row["name"],
                    defaults={
                        "category": row["category"],
                        "rating": row["rating"] if not pd.isna(row["rating"]) else None,
                        "rating_count": row["rating_count"],
                        "review_count": row["review_count"],
                        "review_text": row["review_text"] if not pd.isna(row["review_text"]) else "",
                        "review_summary": row["review_summary"] if "review_summary" in df.columns and not pd.isna(row["review_summary"]) else "",
                        "created_at": row["created_at"]
                    }
                )
                action = "추가됨" if created else "업데이트됨"
                self.stdout.write(self.style.SUCCESS(f"✅ {row['name']} ({row['category']}) {action}"))

            self.stdout.write(self.style.SUCCESS(f"🎉 CSV 데이터 처리 완료!"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ 오류 발생: {e}"))

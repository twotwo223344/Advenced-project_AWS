from django.db import models
from django.utils.timezone import now

class kakaoplace(models.Model):
    CATEGORY_CHOICES = [
        ('restaurant', '맛집'),
        ('cafe', '카페'),
        ('tour', '관광지'),
    ]

    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    rating = models.FloatField(null=True, blank=True)
    rating_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    review_text = models.TextField(null=True, blank=True)  # ✅ 새 필드 추가
    review_summary = models.TextField(null=True, blank=True)  # ✅ 요약된 리뷰 저장
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

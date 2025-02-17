from django.contrib import admin
from .models import kakaoplace  # ✅ 모델명 변경

@admin.register(kakaoplace)  # ✅ 소문자 모델명 적용
class kakaoplaceAdmin(admin.ModelAdmin):  
    list_display = ('name', 'category', 'rating', 'review_count', 'created_at')  # ✅ Admin 목록에서 보일 필드
    search_fields = ('name', 'category')  # ✅ 검색 가능 필드
    list_filter = ('category',)  # ✅ 필터 추가 (맛집, 카페, 관광지)

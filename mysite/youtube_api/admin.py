from django.contrib import admin
from .models import YouTubeVideo

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "video_id", "views", "published_date")  # ✅ 관리자 목록에서 보이는 필드
    list_filter = ("published_date", "views")  # ✅ 필터 기능 추가
    search_fields = ("title", "video_id", "description")  # ✅ 검색 기능 추가
    ordering = ("-views",)  # ✅ 조회수 순 정렬
    readonly_fields = ("video_id", "views", "published_date")  # ✅ 수정 불가능한 필드 (video_id는 고유값)
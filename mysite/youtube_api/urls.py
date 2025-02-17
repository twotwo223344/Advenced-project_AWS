from django.urls import path
from . import views
from youtube_api.views import video_list, search_videos, video_detail, search_top_videos

urlpatterns = [
    path('', views.video_list, name='video_list'),  # 기본 URL에 연결
    path('search/', search_videos, name='search_videos'),  # ✅ 검색 결과 페이지 추가
    path('dashboard/', views.dashboard, name='dashboard'),  # 대시보드 추가
    path('<str:video_id>/', video_detail, name='video_detail'),
    path("search/top/", search_top_videos, name="search_top_videos"),  # 썸네일 전용 API
]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from youtube_api.views import opendoor  # opendoor 뷰 함수 추가


urlpatterns = [
    path('admin/', admin.site.urls),
    path('youtube/', include('youtube_api.urls')),
    path('kakao/', include('kakao_api.urls')),
    path("opendoor/", opendoor, name="opendoor"),  # ✅ opendoor 추가
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])  # ✅ STATIC_URL 추가
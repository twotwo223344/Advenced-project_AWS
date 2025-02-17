import os
import django
import requests
# ✅ Django 환경 설정을 명확히 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # settings.py가 있는 Django 앱명 입력
django.setup()

from youtube_api.models import YouTubeVideo  # ✅ 이제 Django 환경이 로드된 상태에서 가져오기 가능!

# ✅ API 키 설정 (config.json에서 로드)
import json
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    YOUTUBE_API_KEY = config["YOUTUBE_API_KEY"]

def get_videos_data(video_ids):
    """YouTube API를 이용해 여러 영상의 조회수, 태그, 설명을 가져옴"""
    ids_string = ",".join(video_ids)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={ids_string}&key={YOUTUBE_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    
    return None  # API 응답 실패 시 None 반환

def update_videos_metadata():
    """DB에 저장된 모든 영상의 조회수, 태그, 설명을 업데이트"""
    videos = YouTubeVideo.objects.all()
    video_ids = [video.video_id for video in videos]

    for i in range(0, len(video_ids), 50):  # YouTube API는 50개씩 요청 가능
        batch_ids = video_ids[i:i+50]
        data = get_videos_data(batch_ids)

        if data and "items" in data:
            for item in data["items"]:
                video_id = item["id"]
                views = int(item["statistics"]["viewCount"])
                tags = item["snippet"].get("tags", [])
                description = item["snippet"]["description"]

                # ✅ DB 업데이트
                YouTubeVideo.objects.filter(video_id=video_id).update(
                    views=views,
                    tags=", ".join(tags) if tags else None,
                    description=description
                )
                print(f"✅ {video_id} 업데이트 완료 (조회수: {views})")

if __name__ == "__main__":
    update_videos_metadata()

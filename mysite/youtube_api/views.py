from django.shortcuts import render, get_object_or_404
from youtube_api.models import YouTubeVideo
from django.db.models import Q
import re
from youtube_api.utils import format_timestamp 
from django.core.paginator import Paginator 
from django.http import JsonResponse


def video_list(request):
    """
    저장된 모든 동영상 리스트를 불러와 HTML로 렌더링 (타임스탬프 변환 추가).
    """
    videos = YouTubeVideo.objects.filter(captions__isnull=False).order_by('-views')  # ✅ 자막 있는 동영상만 가져오기
    
    video_data = []  # ✅ 가공된 데이터 저장할 리스트

    for video in videos:
        matched_captions = []
        captions = video.captions.split("\n")  # 자막을 줄 단위로 분할

        for i in range(len(captions)):
            line = captions[i]

            if "-->" in line:  # ✅ 타임스탬프 줄이면 처리
                timestamp = line.split("-->")[0].strip()  # 시작 시간 추출
                try:
                    seconds = float(timestamp)
                    formatted_time = format_timestamp(int(seconds))  # 🔹 hh:mm:ss 변환
                except ValueError:
                    seconds = 0
                    formatted_time = "00:00:00"
                continue  # ✅ 실제 텍스트가 있는 줄로 이동

            if line.strip():  # ✅ 빈 줄이 아닌 경우만 저장
                matched_captions.append({
                    "time": formatted_time,  # ✅ 변환된 hh:mm:ss 포맷
                    "seconds": int(seconds),  # 초 단위
                    "text": line.strip()  # ✅ 실제 자막 텍스트
                })

        video_data.append({
            "video_id": video.video_id,
            "title": video.title,
            "captions": matched_captions  # ✅ 변환된 자막 포함
        })

    # ✅ 페이지네이션 적용
    paginator = Paginator(video_data, 5)  
    page_number = request.GET.get("page")  
    page_obj = paginator.get_page(page_number)  

    return JsonResponse({
    "videos": list(page_obj),  # 페이지 데이터 JSON 변환
    "has_next": page_obj.has_next(),
    "has_previous": page_obj.has_previous(),
    "current_page": page_obj.number,
    "total_pages": paginator.num_pages,
}, safe=False)



def search_videos(request):
    """
    검색 기능: 
    - 제목 검색 → 해당 영상의 모든 자막과 타임스탬프 포함
    - 자막 검색 → 해당 자막이 있는 영상만 결과에 표시되며, 검색된 자막 부분만 포함
    """
    query = request.GET.get('q', '').strip()  # 검색어 가져오기 (공백 제거)
    search_type = request.GET.get("search_type", "captions")  # 기본값: 자막 검색

    videos = YouTubeVideo.objects.all()
    search_results = []

    if query:
        for video in videos:
            matched_captions = []
            matched_title = False
            captions = video.captions.split("\n") if video.captions else []

            # ✅ 자막 검색
            if search_type == "captions":
                for i in range(len(captions)):
                    line = captions[i]
                    if query in line:
                        timestamp = "0"
                        if i > 0 and "-->" in captions[i - 1]:
                            timestamp = captions[i - 1].split("-->")[0].strip()
                        try:
                            seconds = float(timestamp)
                            formatted_time = format_timestamp(int(seconds))
                        except ValueError:
                            seconds = 0
                            formatted_time = "00:00:00"

                        matched_captions.append({
                            "time": formatted_time,
                            "seconds": int(seconds),
                            "text": line.strip()
                        })

            # ✅ 제목 검색
            if search_type == "title" and query.lower() in video.title.lower():
                matched_title = True
                # 🔹 제목 검색 시 해당 영상의 **모든 자막 포함**
                for i in range(len(captions)):
                    line = captions[i]
                    if "-->" in line:  # 타임스탬프 줄이면 처리
                        timestamp = line.split("-->")[0].strip()
                        try:
                            seconds = float(timestamp)
                            formatted_time = format_timestamp(int(seconds))
                        except ValueError:
                            seconds = 0
                            formatted_time = "00:00:00"
                        continue
                    if line.strip():
                        matched_captions.append({
                            "time": formatted_time,
                            "seconds": int(seconds),
                            "text": line.strip()
                        })

            # ✅ 검색 결과 추가 (타이틀이 맞거나 자막에서 검색어가 발견된 경우)
            if matched_captions or matched_title:
                search_results.append({
                    "video_id": video.video_id,
                    "title": video.title,
                    "matches": matched_captions,
                    "matched_title": matched_title
                })

    # ✅ 페이지네이션 설정 (페이지 URL에 검색 조건 유지)
    paginator = Paginator(search_results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return JsonResponse({
        "results": list(page_obj),
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "total_pages": paginator.num_pages,
    }, safe=False)


def dashboard(request):
    """
    간단한 대시보드 데이터 표시
    """
    data = {
        "top_videos": [
            {"title": "부산 BEST 2", "views": 12345, "likes": 678},
            {"title": "부산 여행 BEST 23", "views": 9876, "likes": 543},
        ]
    }
    return render(request, 'dashboard.html', data)


def video_detail(request, video_id):
    """
    개별 동영상 상세 정보를 반환
    """
    video = get_object_or_404(YouTubeVideo, video_id=video_id)

    # 자막 데이터 가공
    matched_captions = []
    captions = video.captions.split("\n") if video.captions else []
    
    for i in range(len(captions)):
        line = captions[i]
        if "-->" in line:
            timestamp = line.split("-->")[0].strip()
            try:
                seconds = float(timestamp)
                formatted_time = format_timestamp(int(seconds))
            except ValueError:
                seconds = 0
                formatted_time = "00:00:00"
            continue
        if line.strip():
            matched_captions.append({
                "time": formatted_time,
                "seconds": int(seconds),
                "text": line.strip()
            })

    return JsonResponse({
        "video_id": video.video_id,
        "title": video.title,
        "tags": video.tags,
        "summary": video.summary,
        "captions": matched_captions
    })

def opendoor(request):
    return render(request, "opendoor.html")  # opendoor.html 템플릿 연결

def search_top_videos(request):
    query = request.GET.get("q", "")
    search_type = request.GET.get("search_type", "captions")
    limit = request.GET.get("limit", 5)

    if not query:
        return JsonResponse({"results": []})

    # 검색어를 기반으로 검색
    if search_type == "captions":
        videos = YouTubeVideo.objects.filter(captions__icontains=query)
    else:
        videos = YouTubeVideo.objects.filter(title__icontains=query)

    # 조회수 높은 순으로 5개만 선택
    videos = videos.order_by("-views")[:int(limit)]

    # JSON 응답 생성
    results = [
        {
            "video_id": video.video_id,
            "title": video.title,
            "views": video.views,
        }
        for video in videos
    ]
    
    return JsonResponse({"results": results})

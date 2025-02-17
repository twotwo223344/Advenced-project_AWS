from django.shortcuts import render
from django.conf import settings
import os
import matplotlib
from django.http import JsonResponse


matplotlib.use('Agg')  # ✅ GUI 백엔드 사용 방지
import matplotlib.pyplot as plt
from matplotlib import font_manager
from .models import kakaoplace

# Windows 한글 폰트 적용 (Malgun Gothic)
font_path = "C:/Windows/Fonts/malgun.ttf"
if os.path.exists(font_path):
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())

def dashboard(request):
    """ 대시보드: 맛집, 카페, 관광지 데이터를 개별적으로 정렬하여 JSON 반환 """
    categories = [
        ("Restaurant", "restaurant"),
        ("Cafe", "cafe"),
        ("Place", "tour"),
    ]

    sort_label_dict = {
        "rating": "평점순",
        "rating_count": "건수순",
        "review_count": "리뷰수순"
    }

    category_data = []
    for title, category in categories:
        # 개별 필터 적용 (각각 다른 GET 파라미터 사용)
        sort_param = f"sort_{category}"
        sort_by = request.GET.get(sort_param, "rating_count")
        sort_label = sort_label_dict.get(sort_by, "건수순")

        places = list(kakaoplace.objects.filter(category=category).values(
            "name", "rating", "rating_count", "review_count", "review_summary"
        ))  # ✅ `review_summary` 포함

        # 개별 정렬 적용
        if sort_by == "rating":
            places.sort(key=lambda x: x["rating"] or 0, reverse=True)
        elif sort_by == "review_count":
            places.sort(key=lambda x: x["review_count"] or 0, reverse=True)
        else:  # 기본: 건수순
            places.sort(key=lambda x: x["rating_count"] or 0, reverse=True)

        top_places = places[:10] if places else []
        graph_url = generate_chart(top_places, title, sort_by, category) if top_places else ""

        category_data.append({
            "title": title,
            "places": top_places,
            "graph_url": graph_url,
            "filter_label": sort_label,
            "sort_param": sort_param,  # 개별 정렬을 위한 파라미터 전달
            "selected_sort": sort_by  # 현재 선택된 정렬 기준
        })

    # ✅ JSON 응답 추가 (React에서 사용 가능)
    return JsonResponse({"category_data": category_data}, json_dumps_params={'ensure_ascii': False})

def generate_chart(places, title, sort_by, category):
    """ 개별 정렬 기준에 따른 그래프 생성 """
    if not places:
        return ""

    names = []
    values = []

    for place in places:
        names.append(place["name"])
        if sort_by == "rating":
            values.append(place["rating"])
        elif sort_by == "review_count":
            values.append(place["review_count"])
        else:  # 기본: 건수순
            values.append(place["rating_count"])

    plt.figure(figsize=(10, 6))
    plt.barh(names, values, color='skyblue')
    plt.xlabel(sort_by, fontsize=14)
    plt.ylabel('이름', fontsize=14)
    plt.title(f'{title} TOP 10 {sort_by} 비교', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().invert_yaxis()

    graph_path = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(graph_path, exist_ok=True)
    image_path = os.path.join(graph_path, f'{category}_{sort_by}_chart.png')

    plt.savefig(image_path, format='png', bbox_inches='tight', dpi=150)
    plt.close()  # ✅ GUI 백엔드 사용 방지

    return settings.MEDIA_URL + f'charts/{category}_{sort_by}_chart.png'

def place_list(request):
    """ 모든 맛집, 카페, 관광지 목록을 반환하는 함수 (JSON 포맷) """
    places = list(kakaoplace.objects.all().values("name", "category", "rating", "rating_count", "review_summary"))  # ✅ `review_summary` 추가
    return JsonResponse({"places": places}, json_dumps_params={'ensure_ascii': False})
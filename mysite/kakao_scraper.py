import time
import os
import django
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.db import transaction

# Django 프로젝트 설정 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from kakao_api.models import kakaoplace

def extract_reviews(driver, max_reviews=30):
    """✅ 후기 페이지에서 최대 max_reviews개 리뷰 가져오는 함수"""
    reviews_list = []
    prev_review_count = 0

    try:
        while len(reviews_list) < max_reviews:
            review_elements = driver.find_elements(By.CSS_SELECTOR, "p.txt_comment > span")
            for review in review_elements[len(reviews_list):]:
                review_text = review.text.strip()
                if review_text and review_text not in reviews_list:
                    reviews_list.append(review_text)

            # ✅ "후기 더보기" 버튼 클릭 (있을 경우)
            try:
                more_button = driver.find_element(By.CSS_SELECTOR, "a.link_more span.txt_more")
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(2)

                if len(reviews_list) == prev_review_count:
                    break
                prev_review_count = len(reviews_list)
            except:
                break

    except Exception as e:
        print(f"⚠️ 리뷰 크롤링 실패: {e}")

    return " | ".join(reviews_list)

def save_place_to_db(place_name, rating, rating_count, review_count, review_text, category):
    """✅ 장소 데이터를 데이터베이스에 저장"""
    with transaction.atomic():
        kakaoplace.objects.update_or_create(
            name=place_name,
            defaults={
                "rating": float(rating) if rating else "비공개",
                "rating_count": rating_count,  
                "review_count": review_count,
                "review_text": review_text,
                "category": category
            }
        )
        print(f"✅ 저장 완료: {place_name} - ⭐ {rating} | 🏆 {rating_count}건 | 💬 {review_count}개 | 📝 리뷰 저장됨")

def get_places_details(place_name, category, max_results=30):
    """✅ 장소 크롤링 (장소 더보기 이후 페이지네이션 기능 추가)"""

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    search_url = f"https://map.kakao.com/?q={place_name}"
    driver.get(search_url)
    time.sleep(3)

    results = set()

    # ✅ "장소 더보기" 버튼 클릭
    try:
        more_button = driver.find_element(By.CSS_SELECTOR, "a#info\\.search\\.place\\.more")
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(3)
    except:
        print("🚫 '장소 더보기' 버튼 없음. 기본 목록만 크롤링 진행.")

    while len(results) < max_results:
        print(f"📄 현재 장소 크롤링 중: {place_name}")

        # ✅ 페이지 번호 리스트 가져오기
        try:
            page_numbers = driver.find_elements(By.CSS_SELECTOR, 'div#info\\.search\\.page a')

            for page in page_numbers:
                page_num = page.text.strip()
                if not page_num.isdigit():  # 숫자가 아닌 요소 필터링
                    continue  

                print(f"🔄 페이지 {page_num} 크롤링 중...")
                driver.execute_script("arguments[0].click();", page)
                time.sleep(3)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'li.PlaceItem'))
                )

                places = driver.find_elements(By.CSS_SELECTOR, 'li.PlaceItem')

                for place in places:
                    if len(results) >= max_results:
                        return results  

                    try:
                        place_name = place.find_element(By.CSS_SELECTOR, 'a.link_name').text
                        rating = place.find_element(By.CSS_SELECTOR, 'em.num').text

                        try:
                            review_count = place.find_element(By.CSS_SELECTOR, 'a.review em').text
                            review_count = int(review_count.replace(',', '')) if isinstance(review_count, str) else review_count
                        except:
                            review_count = 0

                        try:
                            rating_count_element = place.find_element(By.CSS_SELECTOR, 'a.numberofscore')
                            rating_count = rating_count_element.text.strip()
                            rating_count = int(rating_count.replace('건', '').replace(',', '')) if isinstance(rating_count, str) else rating_count
                        except:
                            rating_count = 0

                        reviews_text = ""
                        try:
                            review_link = place.find_element(By.CSS_SELECTOR, 'a.review').get_attribute("href")
                            driver.execute_script(f"window.open('{review_link}', '_blank');")
                            time.sleep(3)
                            driver.switch_to.window(driver.window_handles[1])
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'span'))
                            )
                            reviews_text = extract_reviews(driver)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            pass

                        if place_name not in results:
                            results.add(place_name)
                            save_place_to_db(place_name, rating, rating_count, review_count, reviews_text, category)

                    except Exception as e:
                        print(f"⚠️ 장소 정보 크롤링 실패: {e}")

        except:
            print("🚫 페이지 번호를 찾을 수 없음")

        # ✅ "다음" 버튼 클릭 (모든 페이지 번호를 순차적으로 누른 후)
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button#info\\.search\\.page\\.next')
            if "disabled" in next_button.get_attribute("class"):
                print("🚫 다음 페이지 없음. 크롤링 종료.")
                break

            print("⏭️ 다음 페이지로 이동")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)

        except:
            print("🚫 '다음' 버튼이 비활성화됨. 크롤링 종료.")
            break

    driver.quit()
    return results

# 🔹 **검색어별 크롤링 실행**
if __name__ == "__main__":
    categories = {
        "부산 맛집": "restaurant",
        "부산 카페": "cafe",
        "부산 관광지": "tour",
    }

    for search_term, category in categories.items():
        print(f"\n🔍 **'{search_term}' 크롤링 시작...**")
        results = get_places_details(search_term, category, max_results=30)

        if results:
            print(f"\n✅ **'{search_term}' 크롤링 완료 ({len(results)}개 저장됨)**")
        else:
            print(f"\n⚠️ '{search_term}'에서 크롤링된 데이터가 없습니다.")

    print("\n🎉 모든 크롤링이 완료되었습니다! 🚀")

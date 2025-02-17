import json

def save_to_json(data, filename="places.json"):
    """크롤링한 데이터를 JSON 파일로 저장"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ {filename} 저장 완료!")

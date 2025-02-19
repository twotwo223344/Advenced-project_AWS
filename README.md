

# Travel Video Search AI
AI 기반으로 부산지역 여행 영상을 검색하는 프로젝트입니다.

## 주요 기능
- 키워드 검색을 통한 여행 영상 탐색
- YouTube API를 활용한 영상 리스트 제공
- 특정 장소(예: 해운대) 관련 영상 검색
- 대시보드를 통한 리뷰 데이터 분석 (맛집 등 

## 개발 기간  
**2025.01.25 ~ 2025.02.20**  
- 프로젝트 기획  
- 데이터 수집 및 전처리 
- 백엔드 구축 (Django & PostgreSQL)    
- 검색 기능 및 대시보드 추가
- 프론트엔드 개발 (React & MUI) 
- 배포 및 최적화 (AWS)

## 프로젝트 데이터 흐름도
- Django 백엔드가 YouTube API를 활용해 영상 데이터를 가져옴
- Kakao Map 크롤링을 통해 장소 리뷰 수집
- Gemini API를 활용해 영상 & 리뷰 요약 생성
- PostgreSQL Database에 저장
- React 프론트엔드가 Django API에서 데이터를 가져와 UI에 표시

<img src="데이터흐름도.png" alt="데이터 흐름도" width="600">

## 프로젝트 폴더 구조
```plaintext
root/
│── mysite/  # Django 백엔드
│   │── config/  # 환경설정 및 URL 설정
│   │── kakao_api/  # Kakao API 관련 크롤링 코드
│   │── youtube_api/  # YouTube API 연동 코드
│   └── database/  # PostgreSQL 관련 설정
│
│── my-frontend/  # React 프론트엔드
│   │── public/  # 정적 파일 (이미지, HTML)
│   │── src/  # 소스 코드
│   │── package.json  # 프론트엔드 패키지 정보
│   │── README.md  # 프론트엔드 문서화 파일
│
└── README.md  # 프로젝트 설명 파일


## 기술 스택
- **Frontend:** React, TailwindCSS, MUI
- **Backend:** Django, PostgreSQL
- **AI Model:** OpenAI Whisper (자막 기반 검색), Gemini API
- **Deployment:** AWS (EC2)

## 설치 및 실행 방법
```
git clone https://github.com/사용자명/레포지토리명.git
cd 레포지토리명

-Backend 실행
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

-Frontend 실행
cd frontend
npm install
npm start
```

## 팀 소개
-팀명 : 휴먼원정대
-팀원 : 이준혁(팀장), 배휘호, 이기성, 김민석
<img src="team.png" alt="팀원 소개" width="600">


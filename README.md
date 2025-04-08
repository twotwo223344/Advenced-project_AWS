

# Travel Video Search AI Service Project

AI 기반으로 부산지역 여행 영상을 검색하는 프로젝트입니다.

## 주요 기능
- 키워드 검색을 통한 여행 영상 탐색
- YouTube API를 활용한 영상 리스트 제공
- 특정 장소(예: 해운대) 관련 영상 검색
- 대시보드를 통한 리뷰 데이터 분석

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

<img src="pic/흐름도.png" alt="데이터 흐름도" width="600">

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
    │── public/  # 정적 파일 (이미지, HTML)
    │── src/  # 소스 코드
    │── package.json  # 프론트엔드 패키지 정보
    
```

## 기술 스택
<table>
  <tr>
    <td>
      <ul>
        <li><strong>Frontend:</strong> React, TailwindCSS, MUI</li>
        <li><strong>Backend:</strong> Django, PostgreSQL</li>
        <li><strong>AI Model:</strong> OpenAI Whisper (자막 기반 검색), Gemini API</li>
        <li><strong>Deployment:</strong> AWS (EC2)</li>
      </ul>
    </td>
    <td>
      <img src="pic/기술스택.png" alt="기술스택" width="300">
    </td>
  </tr>
</table>

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

## 실행 화면
<table>
  <tr>
    <td><img src="pic/시작화면.png" alt="시작화면" width="400"></td>
    <td><img src="pic/대시보드.png" alt="대시보드" width="400"></td>
  </tr>
  <tr>
    <td><img src="pic/검색창.png" alt="검색" width="400"></td>
    <td><img src="pic/상세.png" alt="상세" width="400"></td>
  </tr>
</table>

## 기능 시연 영상

각 기능별 동작 시연을 `.gif`로 확인하실 수 있습니다.  
GitHub에서 바로 재생되며, 별도 클릭 없이 자동으로 동작 모습을 보여줍니다.

<table>
  <tr>
    <td><strong>1. 메인페이지</strong></td>
    <td><strong>2. 타임스탬프</strong></td>
  </tr>
  <tr>
    <td><img src="pic/메인페이지.gif" alt="메인페이지 시연" width="400"></td>
    <td><img src="pic/타임스탬프.gif" alt="타임스탬프 시연" width="400"></td>
  </tr>
  <tr>
    <td><strong>3. 검색 Top5</strong></td>
    <td><strong>4. 상세페이지</strong></td>
  </tr>
  <tr>
    <td><img src="pic/검색_top5.gif" alt="검색 Top5 시연" width="400"></td>
    <td><img src="pic/상세페이지.gif" alt="상세페이지 시연" width="400"></td>
  </tr>
  <tr>
    <td><strong>5. 대시보드</strong></td>
    <td></td>
  </tr>
  <tr>
    <td><img src="pic/대시보드.gif" alt="대시보드 시연" width="400"></td>
    <td></td>
  </tr>
</table>


## 팀 소개
-팀명 : 휴먼원정대
-팀원 : 이준혁(팀장), 배휘호, 이기성, 김민석


<img src="pic/team.png" alt="팀 소개" width="600">

import React, { useEffect, useState, useRef, useCallback } from "react";
import { useParams } from "react-router-dom";
import "./VideoDetail.css"; // ✅ CSS 적용
import { useNavigate } from "react-router-dom";  // ✅ 추가

function VideoDetail() {
  const { videoId } = useParams();
  console.log("🔹 videoId 확인:", videoId);

  const [video, setVideo] = useState(null);
  const [loading, setLoading] = useState(true);
  const playerRef = useRef(null);
  const isYouTubeReady = useRef(false);
  const navigate = useNavigate();  // ✅ navigate 정의

  // ✅ YouTube Iframe API 로드
  useEffect(() => {
    const loadYouTubeAPI = () => {
      return new Promise((resolve) => {
        if (window.YT && window.YT.Player) {
          console.log("✅ YouTube API 이미 로드됨");
          resolve();
        } else {
          console.log("📌 YouTube API 새로 로드 중...");
          const script = document.createElement("script");
          script.src = "https://www.youtube.com/iframe_api";
          script.async = true;
          document.body.appendChild(script);

          script.onload = () => {
            console.log("✅ YouTube API 로드 완료");
            resolve();
          };
        }
      });
    };

    loadYouTubeAPI().then(() => {
      isYouTubeReady.current = true;
      console.log("🔄 YouTube API 재설정 완료");

      if (playerRef.current) {
        console.log(`🔄 기존 플레이어 삭제: ${videoId}`);
        playerRef.current.destroy();
        playerRef.current = null;
      }

      setTimeout(() => {
        console.log(`🎬 새 플레이어 생성: ${videoId}`);
        createPlayer(videoId);
      }, 500);
    });
  }, [videoId]); // ✅ videoId 변경될 때마다 실행

  // ✅ 영상 데이터 가져오기
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/youtube/${videoId}/`)
      .then((res) => res.json())
      .then((data) => {
        console.log("📌 상세 페이지 데이터:", data);
        setVideo(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("상세 페이지 로딩 오류:", error);
        setLoading(false);
      });
  }, [videoId]);

  // ✅ 유튜브 플레이어 생성
  const createPlayer = useCallback((videoId) => {
    if (!isYouTubeReady.current || playerRef.current) return;
    console.log(`🎬 Creating YouTube Player for: ${videoId}`);

    playerRef.current = new window.YT.Player("youtube-player", {
      events: {
        onReady: () => console.log(`✅ Player Ready: ${videoId}`),
      },
    });
  }, []);

  // ✅ 타임스탬프 클릭 시 이동
  const seekToTime = useCallback((seconds) => {
    const player = playerRef.current;
    if (player && typeof player.seekTo === "function") {
      console.log(`⏩ Seeking to ${seconds} seconds`);
      player.seekTo(seconds, true);
    } else {
      console.warn(`⚠️ Player not ready, retrying...`);
      setTimeout(() => seekToTime(seconds), 1000);
    }
  }, []);

  if (loading) return <p>Loading...</p>;
  if (!video) return <p>해당 영상 정보를 찾을 수 없습니다.</p>;

  return (
    <div className="video-detail-container">
      {/* <h1 className="video-title">{video.title}</h1> */}
      <div className="video-caption-wrapper">
        <div className="video-content">
          <iframe
            id="youtube-player"
            width="750"
            height="420"
            src={`https://www.youtube.com/embed/${video.video_id}?enablejsapi=1`}
            title={video.title}
            frameBorder="0"
            allowFullScreen
          ></iframe>
        </div>
        <div className="captions-container">
          <h2>자막</h2>
          <ul className="captions-list">
            {video.captions.map((caption, index) => (
              <li key={index} className="caption-item">
                <button className="timestamp" onClick={() => seekToTime(caption.seconds)}>
                  [{caption.time}]
                </button>{" "}
                {caption.text}
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="hashtags">
        <h2>해시태그</h2>
        <div className="tags">
          {video.tags.split(",").map((tag, index) => (
            <span key={index} className="tag">#{tag.trim()}</span>
          ))}
        </div>
      </div>
      <div className="summary">
        <h2>요약</h2>
        <p>{video.summary}</p>
      </div>
      {/* ✅ 목록 보기 버튼 추가 */}
      <div className="back-to-list">
      <button className="back-button" onClick={() => navigate(-1)}>목록 보기</button>
      </div>
    </div>
  );
}

export default VideoDetail;

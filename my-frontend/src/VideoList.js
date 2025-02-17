import React, { useEffect, useState, useRef, useCallback } from "react";
import { Link } from "react-router-dom";
import "./VideoList.css";

function VideoList() {
  const [videos, setVideos] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [totalPages, setTotalPages] = useState(1);
  const playerRefs = useRef({});
  const isYouTubeReady = useRef(false);
  const captionRefs = useRef({});
  const videoHeightRefs = useRef({});
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768); // ✅ 모바일 감지


  // ✅ 화면 크기 감지하여 `isMobile` 상태 업데이트
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  
  // ✅ 유튜브 영상 높이에 맞춰 자막 컨테이너 조정
  const adjustCaptionHeight = () => {
    Object.keys(captionRefs.current).forEach((videoId) => {
      const player = playerRefs.current[videoId];
      const captionContainer = captionRefs.current[videoId];

      if (player && captionContainer) {
        const videoHeight = player.getIframe().clientHeight;
        const padding = 10; // ✅ CSS 패딩 고려
        captionContainer.style.height = `${videoHeight - padding * 2}px`;
      }
    });
  };

  // ✅ YouTube Iframe API 로드
  useEffect(() => {
    const loadYouTubeAPI = () => {
      return new Promise((resolve) => {
        if (window.YT && window.YT.Player) {
          resolve();
        } else {
          const script = document.createElement("script");
          script.src = "https://www.youtube.com/iframe_api";
          script.async = true;
          document.body.appendChild(script);

          script.onload = () => {
            resolve();
          };
        }
      });
    };

    loadYouTubeAPI().then(() => {
      isYouTubeReady.current = true;
    });
  }, []);

  // ✅ 영상 리스트 데이터 가져오기
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/youtube/?page=${page}&page_size=5`)
      .then((response) => response.json())
      .then((data) => {
        if (data.videos && Array.isArray(data.videos)) {
          setVideos(data.videos);
          setHasNext(data.has_next || false);
          setHasPrevious(data.has_previous || false);
          setTotalPages(data.total_pages || 1);
        } else {
          console.error("⚠️ API 응답 오류:", data);
          setVideos([]);
        }
      })
      .catch((error) => {
        console.error("데이터 불러오기 오류:", error);
        setVideos([]);
      });
  }, [page]);

  // ✅ 유튜브 플레이어 생성
  const createPlayer = useCallback((videoId) => {
    if (!isYouTubeReady.current || playerRefs.current[videoId]) return;

    playerRefs.current[videoId] = new window.YT.Player(`player-${videoId}`, {
      events: {
        onReady: (event) => {
          console.log(`✅ Player Ready: ${videoId}`);
          videoHeightRefs.current[videoId] = event.target.getIframe().clientHeight;
          adjustCaptionHeight();
        },
      },
    });

    setTimeout(() => {
      adjustCaptionHeight();
    }, 1000);
  }, []);

  // ✅ 기존 플레이어 삭제 후 재생성
  useEffect(() => {
    if (isYouTubeReady.current && videos.length > 0) {
      videos.forEach((video) => {
        const container = document.getElementById(`player-${video.video_id}`);
        if (playerRefs.current[video.video_id]) {
          playerRefs.current[video.video_id].destroy();
          delete playerRefs.current[video.video_id];
        }

        if (container) {
          container.innerHTML = "";
        }

        setTimeout(() => {
          createPlayer(video.video_id);
        }, 500);
      });
    }
  }, [videos]);

  // ✅ 창 크기 변경 시 자막 높이 조정
  useEffect(() => {
    window.addEventListener("resize", adjustCaptionHeight);
    return () => window.removeEventListener("resize", adjustCaptionHeight);
  }, []);

  // ✅ 데이터 로드 후 자막 높이 조정
  useEffect(() => {
    if (videos.length > 0) {
      setTimeout(adjustCaptionHeight, 1000);
    }
  }, [videos]);

  // ✅ **seekToTime 함수 추가 (타임스탬프 클릭 시 이동)**
  const seekToTime = useCallback((videoId, seconds) => {
    const player = playerRefs.current[videoId];
    if (player && typeof player.seekTo === "function") {
      player.seekTo(seconds, true);
    } else {
      console.warn(`⚠️ Player for video ${videoId} not ready, retrying...`);
      setTimeout(() => seekToTime(videoId, seconds), 1000);
    }
  }, []);

  // ✅ **자막 리스트 렌더링**
  const renderCaptions = (video) =>
    video.captions.map((caption, index) => (
      <li key={index} className="list-caption-item">
        <button
          onClick={(e) => {
            e.preventDefault();
            seekToTime(video.video_id, caption.seconds);
          }}
          className="list-timestamp"
        >
          <strong>[{caption.time}]</strong> {caption.text}
        </button>
      </li>
    ));

  return (
    <div className="list-container">
      <h3 className="list-title">busan youtube list</h3>
      {videos.length > 0 ? (
        videos.map((video) => (
          <div key={video.video_id} className="video-card">
            <br></br>
            <h2 className="list-video-title">
              <Link to={`/detail/${video.video_id}`}>{video.title}</Link>
            </h2>
            <div className="list-video-caption-wrapper">
              <div className="list-video-content">
                <iframe
                  id={`player-${video.video_id}`}
                  className="list-video-iframe"
                  src={`https://www.youtube.com/embed/${video.video_id}?enablejsapi=1`}
                  title={video.title}
                  frameBorder="0"
                  allowFullScreen
                ></iframe>
              </div>

              <div ref={(el) => (captionRefs.current[video.video_id] = el)} className="list-captions-container">
                <ul className="list-captions-list">{renderCaptions(video)}</ul>
              </div>
            </div>
          </div>
        ))
      ) : (
        <p className="text-center text-gray-500">Loading...</p>
      )}

      {/* ✅ 페이지네이션 추가 */}
      <div className="pagination">
        {hasPrevious && (
          <>
            <button onClick={() => setPage(1)}>« First</button>
            <button onClick={() => setPage(page - 1)}>‹ Prev</button>
          </>
        )}
        <span>
          Page {page} of {totalPages}
        </span>
        {hasNext && (
          <>
            <button onClick={() => setPage(page + 1)}>Next ›</button>
            <button onClick={() => setPage(totalPages)}>Last »</button>
          </>
        )}
      </div>
    </div>
  );
}

export default VideoList;

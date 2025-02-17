import React, { useState, useEffect, useRef, useCallback } from "react";
import { useLocation, Link } from "react-router-dom";
import "./SearchResults.css"; // ✅ 스타일 적용

function SearchResults() {
  const [results, setResults] = useState([]); // ✅ 검색 결과 상태
  const [loading, setLoading] = useState(false);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const playerRefs = useRef({});
  const isYouTubeReady = useRef(false);
  const captionRefs = useRef({});
  const videoHeightRefs = useRef({});
  const location = useLocation();

  // ✅ URL에서 검색어 및 검색 유형 가져오기
  const params = new URLSearchParams(location.search);
  const query = params.get("q") || "";
  const searchType = params.get("search_type") || "captions";

  // ✅ 검색 실행
  useEffect(() => {
    if (!query) return;

    setLoading(true);
    setResults([]); // ✅ 기존 검색 결과 초기화 (새 검색 시 깔끔하게 갱신)

    fetch(`http://127.0.0.1:8000/youtube/search/?q=${encodeURIComponent(query)}&search_type=${searchType}&page=${currentPage}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.results && Array.isArray(data.results)) {
          setResults(data.results);
          setTotalPages(data.total_pages || 1);
        } else {
          setResults([]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("검색 요청 오류:", err);
        setResults([]);
        setLoading(false);
      });
  }, [location.search, currentPage]); // ✅ URL 변경될 때마다 검색 실행

  // ✅ 유튜브 자막 높이 자동 조절
  const adjustCaptionHeight = () => {
    Object.keys(captionRefs.current).forEach((videoId) => {
      const player = playerRefs.current[videoId];
      const captionContainer = captionRefs.current[videoId];

      if (player && captionContainer) {
        const videoHeight = player.getIframe().clientHeight;
        const padding = 10;
        captionContainer.style.height = `${videoHeight - padding * 2}px`;
      }
    });
  };

  // ✅ YouTube API 로드
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

  // ✅ 유튜브 플레이어 생성
  const createPlayer = useCallback((videoId) => {
    if (!isYouTubeReady.current || playerRefs.current[videoId]) return;

    playerRefs.current[videoId] = new window.YT.Player(`player-${videoId}`, {
      events: {
        onReady: (event) => {
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
    if (isYouTubeReady.current && results.length > 0) {
      results.forEach((video) => {
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
  }, [results]);

  // ✅ 창 크기 변경 시 자막 높이 조정
  useEffect(() => {
    window.addEventListener("resize", adjustCaptionHeight);
    return () => window.removeEventListener("resize", adjustCaptionHeight);
  }, []);

  // ✅ 데이터 로드 후 자막 높이 조정
  useEffect(() => {
    if (results.length > 0) {
      setTimeout(adjustCaptionHeight, 1000);
    }
  }, [results]);

  // ✅ 타임스탬프 클릭 시 이동
  const seekToTime = (videoId, seconds) => {
    const player = playerRefs.current[videoId];
    if (player && typeof player.seekTo === "function") {
      player.seekTo(seconds, true);
    } else {
      setTimeout(() => {
        if (!playerRefs.current[videoId]) {
          createPlayer(videoId);
        }
        seekToTime(videoId, seconds);
      }, 1000);
    }
  };

  return (
    <div className="search-container">
      
      <h2 className="search-subtitle">
        "{query}" 검색 결과 ({searchType === "captions" ? "자막" : "제목"} 기준)
      </h2>

      {loading && <p className="search-loading">검색 중...</p>}

      {results.length > 0 ? (
        <>
          {results.map((video) => (
            <div key={video.video_id} className="search-video-card">
              <h2 className="search-video-title">
                <Link to={`/detail/${video.video_id}`}>{video.title}</Link>
              </h2>

              <div className="search-video-caption-wrapper">
                <div className="search-video-content">
                  <iframe
                    id={`player-${video.video_id}`}
                    className="search-video-iframe"
                    src={`https://www.youtube.com/embed/${video.video_id}?enablejsapi=1`}
                    title={video.title}
                    frameBorder="0"
                    allowFullScreen
                  ></iframe>
                </div>

                <div
                  ref={(el) => (captionRefs.current[video.video_id] = el)}
                  className="search-captions-container"
                >
                  <ul className="search-captions-list">
                    {video.matches.map((caption, index) => (
                      <li key={index} className="search-caption-item">
                        <button className="search-timestamp" onClick={() => seekToTime(video.video_id, caption.seconds)}>
                          [{caption.time}]
                        </button>{" "}
                        {caption.text}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}

          {/* ✅ 페이지네이션 UI 적용 */}
<div className="search-pagination">
  {currentPage > 1 && (
    <>
      <button onClick={() => setCurrentPage(1)} className="search-page-btn">
        « First
      </button>
      <button onClick={() => setCurrentPage(currentPage - 1)} className="search-page-btn">
        ‹ Prev
      </button>
    </>
  )}
  <span className="search-page-number">
    Page {currentPage} of {totalPages}
  </span>
  {currentPage < totalPages && (
    <>
      <button onClick={() => setCurrentPage(currentPage + 1)} className="search-page-btn">
        Next ›
      </button>
      <button onClick={() => setCurrentPage(totalPages)} className="search-page-btn">
        Last »
      </button>
    </>
  )}
</div>

        </>
      ) : (
        <p className="search-no-results">검색 결과가 없습니다.</p>
      )}
    </div>
  );
}

export default SearchResults;

import React, { useEffect, useState } from "react";
import "./OpenDoor.css";
import VideoList from "./VideoList";
import Dashboard from "./Dashboard";

function OpenDoor() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="opendoor-container">
      {/* ✅ opendoor 전용 비디오 배경 */}
      <div className="opendoor-section">
        <video autoPlay loop muted className={`background-video ${isMobile ? "mobile-video" : ""}`}>
          <source src="http://127.0.0.1:8000/static/videos/background.mp4" type="video/mp4" />
          당신의 브라우저는 비디오 태그를 지원하지 않습니다.
        </video>
        <div className="content">
          <h1>Welcome to Busan</h1>
          <p>Discover the beauty of Busan with our interactive guides and videos.</p>
          <button
            className="explore-btn"
            onClick={() => document.getElementById("video-list").scrollIntoView({ behavior: "smooth" })}
          >
            Explore Videos
          </button>
        </div>
      </div>

      {/* ✅ 영상 리스트 섹션 */}
      <div id="video-list" className="section-container">
        <div className="video-background">
          <video autoPlay loop muted className={`section-video ${isMobile ? "mobile-section-video" : ""}`}>
            <source src="http://127.0.0.1:8000/static/videos/background5.mp4" type="video/mp4" />
            당신의 브라우저는 비디오 태그를 지원하지 않습니다.
          </video>
        </div>
        <VideoList />
      </div>

      {/* ✅ 대시보드 섹션 */}
      <div id="dashboard-section" className="section-container">
        <div className="video-background">
          <video autoPlay loop muted className={`section-video ${isMobile ? "mobile-section-video" : ""}`}>
            <source src="http://127.0.0.1:8000/static/videos/background5 copy.mp4" type="video/mp4" />
            당신의 브라우저는 비디오 태그를 지원하지 않습니다.
          </video>
        </div>
        <Dashboard />
      </div>
    </div>
  );
}

export default OpenDoor;

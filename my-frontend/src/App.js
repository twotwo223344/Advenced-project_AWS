import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";  // ✅ 공통 네비게이션 추가
import Footer from "./Footer";  // ✅ 푸터 추가

import SearchPage from "./SearchPage";
import SearchResults from "./SearchResults";
import VideoDetail from "./VideoDetail";
import Dashboard from "./Dashboard";
import OpenDoor from "./OpenDoor";
import ScrollToTop from "./ScrollToTop"; // ✅ 스크롤 복구 기능 추가

function App() {
  return (
    <Router>
      <ScrollToTop /> {/* ✅ 여기에 추가해서 사용하도록 설정! */}
      <Navbar /> {/* ✅ 모든 페이지에서 네비게이션 바 사용 */}
      
      {/* ✅ 페이지 콘텐츠를 감싸는 div 추가 */}
      <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
        <Routes>
          <Route path="/" element={<OpenDoor />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/results" element={<SearchResults />} />
          <Route path="/detail/:videoId" element={<VideoDetail />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/opendoor" element={<OpenDoor />} />
        </Routes>
        
        <Footer /> {/* ✅ 푸터 추가 */}
      </div>
    </Router>
  );
}

export default App;

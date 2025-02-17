import React, { useEffect, useState, useRef } from "react";
import { AppBar, Toolbar, IconButton, Typography, Box } from "@mui/material";
import { FaVideo, FaChartBar, FaSearch } from "react-icons/fa";
import { useNavigate, useLocation } from "react-router-dom"; // ✅ useLocation 추가
import SearchForm from "./SearchForm"; // ✅ 검색창 컴포넌트 추가

function Navbar() {
  const [bgColor, setBgColor] = useState("rgba(0, 70, 150, 0.5)"); // ✅ 기본 네비게이션 바 색상
  const [iconColor, setIconColor] = useState("white"); // ✅ 아이콘 색상 (기본: 흰색)
  const [showSearch, setShowSearch] = useState(false);
  const searchRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation(); // ✅ 현재 페이지 확인

  // ✅ 스크롤 이벤트 감지하여 네비게이션 바 스타일 변경
  useEffect(() => {
    const handleScroll = () => {
      const videoSection = document.getElementById("video-list");
      const dashboardSection = document.getElementById("dashboard-section");

      if (
        (videoSection && window.scrollY >= videoSection.offsetTop - 50) ||
        (dashboardSection && window.scrollY >= dashboardSection.offsetTop - 50)
      ) {
        setBgColor("rgba(128, 128, 128, 0.7)"); // ✅ 더 진한 회색 반투명
        setIconColor("white");
      } else {
        setBgColor("rgba(128, 128, 128, 0.5)"); // ✅ 기본 회색 반투명
        setIconColor("white");
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // ✅ 특정 섹션으로 부드럽게 스크롤 이동
  const scrollToSection = (sectionId) => {
    if (sectionId === "opendoor") {
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: "smooth" });
    }
  };

  // ✅ 검색 아이콘 클릭 시 /search 페이지로 이동하는 함수
  const handleSearchClick = () => {
    navigate("/search");
  };

  // ✅ "Human Traveler" 버튼 클릭 시 이동 로직
  const handleHumTravelerClick = () => {
    // 🔹 검색 페이지 또는 비디오 상세 페이지에서는 /opendoor로 이동
    if (location.pathname === "/search" || location.pathname.startsWith("/detail/")) {
      navigate("/opendoor");
    } else {
      scrollToSection("opendoor"); // 🔹 기존 기능 유지 (최상단으로 스크롤 이동)
    }
  };

  // ✅ 검색 페이지 및 비디오 상세 페이지 여부 확인
  const isSearchOrVideoPage = location.pathname === "/search" || location.pathname.startsWith("/video/");

  return (
    <AppBar
      position="fixed"
      sx={{
        background: bgColor, // ✅ 반투명 회색
        transition: "background 0.3s ease-in-out",
        boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.2)", // ✅ 그림자 추가
        WebkitBackdropFilter: "blur(10px)", // ✅ 크로스 브라우저 지원
      }}
    >
      <Toolbar sx={{ display: "flex", justifyContent: "space-between", padding: "10px" }}>
        {/* ✅ Human Traveler 버튼 */}
        <Typography
          variant="h6"
          component="div"
          sx={{ cursor: "pointer", fontWeight: "bold", color: iconColor }}
          onClick={handleHumTravelerClick} // 🔹 동적 이동 기능 추가
        >
          Human Traveler
        </Typography>

    {/* ✅ 네비게이션 아이콘 (검색 페이지 & 비디오 상세 페이지에서는 동영상 & 대시보드 버튼 숨김) */}
    <Box>
          {location.pathname !== "/search" && !location.pathname.startsWith("/detail/") && (
            <>
              <IconButton sx={{ color: iconColor }} onClick={() => scrollToSection("video-list")}>
                <FaVideo size={24} />
              </IconButton>
              <IconButton sx={{ color: iconColor }} onClick={() => scrollToSection("dashboard-section")}>
                <FaChartBar size={24} />
              </IconButton>
            </>
          )}
          {/* ✅ 검색 아이콘은 항상 유지 */}
          <IconButton sx={{ color: iconColor }} onClick={handleSearchClick}>
            <FaSearch size={24} />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;

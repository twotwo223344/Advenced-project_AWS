import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import PropTypes from "prop-types";
import "./SearchForm.css";

function SearchBar({ query, onChange, searchType, setSearchType, suggestions, onSelectSuggestion }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <div className="search-bar-container" style={{ height: "250px", width: "100%", maxWidth: "900px", margin: "0 auto" }}> {/* ✅ 검색창 크기 고정 */}
      <div className="search-bar" style={{ display: "flex", alignItems: "center", gap: "10px", width: "100%" }}>
        <input
          type="text"
          className="search-input"
          placeholder="검색어 입력..."
          value={query}
          onChange={onChange}
          
        />
        <div className="dropdown" style={{ position: "relative" }}>
          <button 
            type="button" 
            className="dropdown-button" 
            onClick={() => setDropdownOpen(!dropdownOpen)}
            style={{ height: "40px" }}
          >
            {searchType === "captions" ? "자막 ▼" : "제목 ▼"}
          </button>
          {dropdownOpen && (
            <div className="dropdown-menu" style={{ position: "absolute", top: "100%", left: "0", zIndex: 10, background: "white", borderRadius: "5px", boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)", overflow: "hidden" }}>
              <button type="button" onClick={() => { setSearchType("captions"); setDropdownOpen(false); }}>
                자막 검색
              </button>
              <button type="button" onClick={() => { setSearchType("title"); setDropdownOpen(false); }}>
                제목 검색
              </button>
            </div>
          )}
        </div>
        <button type="submit" className="search-button" style={{ height: "40px" }}>🔍</button>
      </div>
      <div style={{ height: "110px", background: "#f9f9f9", padding: "10px", borderRadius: "8px", width: "100%" }}> 
        {suggestions.length > 0 ? (
          <>
            <p style={{ fontSize: "14px", fontWeight: "bold", marginBottom: "5px" }}>조회수 TOP 5</p>
            <div className="suggestions-container" style={{ display: "flex", gap: "10px", overflowX: "hidden", justifyContent: "center", width: "100%" }}>
              {suggestions.map((video) => {
                const thumbnailUrl = `https://img.youtube.com/vi/${video.video_id}/0.jpg`;
                return (
                  <div 
                    key={video.video_id} 
                    className="suggestion-item" 
                    style={{ transition: "transform 0.3s ease-in-out", cursor: "pointer" }}
                    onMouseEnter={(e) => e.currentTarget.style.transform = "scale(1.1)"}
                    onMouseLeave={(e) => e.currentTarget.style.transform = "scale(1)"}
                  >
                    <a href={`/detail/${video.video_id}`} style={{ textDecoration: "none" }}>
                      <img 
                        src={thumbnailUrl} 
                        alt="Video Thumbnail" 
                        className="suggestion-thumbnail" 
                        style={{ width: "180px", height: "100px", objectFit: "cover", borderRadius: "5px" }}
                      />
                    </a>
                  </div>
                );
              })}
            </div>
          </>
        ) : (
          <div style={{ height: "100px" }}></div> 
        )}
      </div>
    </div>
  );
}

SearchBar.propTypes = {
  query: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  searchType: PropTypes.string.isRequired,
  setSearchType: PropTypes.func.isRequired,
  suggestions: PropTypes.array.isRequired,
  onSelectSuggestion: PropTypes.func.isRequired,
};

function SearchForm() {
  const navigate = useNavigate();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const [query, setQuery] = useState(params.get("q") || "");
  const [searchType, setSearchType] = useState(params.get("search_type") || "captions");
  const [suggestions, setSuggestions] = useState([]);
  let timeoutId = null;

  useEffect(() => {
    if (query.trim() === "") {
      setSuggestions([]);
      return;
    }

    setSuggestions([]);
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      fetch(`http://127.0.0.1:8000/youtube/search/top/?q=${encodeURIComponent(query)}&search_type=${searchType}&limit=5`)
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          console.log("검색어:", query, "조회수 TOP 5 비디오:", data.results);
          setSuggestions(data.results || []);
        })
        .catch((error) => console.error("Error fetching top videos:", error));
    }, 300);
  }, [query, searchType]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() === "") return;

    navigate(`/search?q=${encodeURIComponent(query)}&search_type=${searchType}`);

    // ✅ 검색 완료 후 스크롤 자동 이동 기능 추가
    setTimeout(() => {
      const searchResultsSection = document.getElementById("search-results-section");
      if (searchResultsSection) {
        searchResultsSection.scrollIntoView({ behavior: "smooth" });
      }
    }, 300);
  };

  return (
    <div className="search-page">
      <h1 className="search-logo">Travler</h1>
      <div className="search-container">
        <form onSubmit={handleSubmit} className="search-form">
          <SearchBar 
            query={query} 
            onChange={(e) => setQuery(e.target.value)} 
            searchType={searchType} 
            setSearchType={setSearchType} 
            suggestions={suggestions}
            onSelectSuggestion={(selected) => setQuery(selected)}
          />
        </form>
      </div>
    </div>
  );
}

export default SearchForm;
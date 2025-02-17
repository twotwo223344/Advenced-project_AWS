import React from "react";
import "./SearchPage.css"; // ✅ 새로운 스타일 파일 추가
import SearchForm from "./SearchForm";
import SearchResults from "./SearchResults";

function SearchPage() {
  return (
    <div className="search-page-container">
      {/* ✅ 검색 폼 섹션 */}
      <div className="search-section">
        <SearchForm />
      </div>

      {/* ✅ 검색 결과 섹션 */}
      <div id="search-results-section" className="search-results-container">
        <SearchResults />
      </div>
    </div>
  );
}

export default SearchPage;

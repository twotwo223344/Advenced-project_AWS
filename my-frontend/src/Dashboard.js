import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";
import "./Dashboard.css"; // ✅ 스타일 적용

function Dashboard() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  // ✅ 정렬 기준을 관리하는 상태 (각 카테고리에 대한 정렬 방식 저장)
  const [sortCriteria, setSortCriteria] = useState({
    restaurant: "rating_count", // ✅ 기본값: 건수순
    cafe: "rating_count",
    tour: "rating_count",
  });

  // ✅ Django API에서 대시보드 데이터 가져오기
  useEffect(() => {
    const url = new URL("http://127.0.0.1:8000/kakao/dashboard/");

    Object.keys(sortCriteria).forEach(category => {
      url.searchParams.append(`sort_${category}`, sortCriteria[category]);
    });

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        console.log("📌 대시보드 데이터:", data);

        // ✅ 블로그 순 (review_count) 정렬 문제 해결 (내림차순 적용)
        const sortedData = data.category_data.map(category => ({
          ...category,
          places: [...category.places].sort((a, b) => {
            if (sortCriteria[category.sort_param.replace("sort_", "")] === "review_count") {
              return (b.review_count || 0) - (a.review_count || 0); // ✅ 내림차순 정렬
            }
            return (b.rating_count || 0) - (a.rating_count || 0); // ✅ 기본 정렬
          })
        }));

        console.log("📌 정렬된 데이터:", sortedData);
        setCategories(sortedData || []);
        setLoading(false);
      })
      .catch((error) => {
        console.error("❌ 데이터를 불러오는 중 오류 발생!", error);
        setLoading(false);
      });
  }, [sortCriteria]); // ✅ 정렬 기준이 바뀔 때마다 API 호출

  // ✅ 정렬 버튼 클릭 시 새로운 정렬 기준 적용
  const updateSortCriteria = (category, newSort) => {
    setSortCriteria((prev) => ({ ...prev, [category]: newSort }));
  };

  if (loading) return <p className="text-center">🔄 로딩 중...</p>;

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Dashboard</h1>
      <br></br><br></br>

      {/* ✅ 가로 정렬을 위한 Flex 컨테이너 */}
      <div className="dashboard-flex">
        {categories.map((category, index) => (
          <div key={index} className="category-section">
            <h2 className="category-title">{category.title}</h2>

            {/* ✅ 정렬 버튼 */}
            <div className="sort-buttons">
              <button onClick={() => updateSortCriteria(category.sort_param.replace("sort_", ""), "rating_count")}>
                별점, 리뷰순
              </button>
              <button onClick={() => updateSortCriteria(category.sort_param.replace("sort_", ""), "review_count")}>
                블로그순
              </button>
            </div>

            {/* ✅ 차트 표시 (차트에서 review_count 값 제대로 표시) */}
            {category.places.length > 0 ? (
              <div className="chart-wrapper">
                <Bar
                  data={{
                    labels: category.places.map((place) => place.name),
                    datasets: [
                      {
                        label: `${category.title} (${category.filter_label})`,
                        data: category.places.map((place) => 
                          sortCriteria[category.sort_param.replace("sort_", "")] === "review_count"
                            ? place.review_count || 0 // ✅ 블로그 순일 경우 review_count 사용
                            : place.rating_count || 0 // ✅ 기본값 rating_count 사용
                        ),
                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: { display: false },
                    },
                  }}
                />
              </div>
            ) : (
              <p>📉 차트 데이터 없음</p>
            )}

            {/* ✅ 장소 리스트 → 정렬 기준에 따라 표시될 값 변경 */}
<ul className="place-list">
  {category.places.map((place, i) => (
    <li key={i}>
      <strong>{place.name}</strong> - ⭐ {place.rating.toFixed(1)}점 (
      {category.selected_sort === "review_count"
        ? `${place.review_count}건`  
        : `${place.rating_count}건`}  
      )
      <br />
      📝 리뷰 요약: {place.review_summary || "없음"}
    </li>
  ))}
</ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;

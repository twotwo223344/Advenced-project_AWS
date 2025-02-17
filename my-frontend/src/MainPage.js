import React from "react";
import OpenDoor from "./OpenDoor";
import VideoList from "./VideoList";

function MainPage() {
  return (
    <div>
      <OpenDoor />  {/* ✅ 배경 비디오와 Welcome 버튼 */}
      <VideoList />  {/* ✅ 리스트 페이지 */}
    </div>
  );
}

export default MainPage;
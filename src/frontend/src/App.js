import React from "react";
import ChatBox from "./components/chat/ChatBox";

function App() {
  return (
    <>
      <div className="container">
        <div className="home-title">
          <div className="d-flex flex-column align-items-center">
            <h1>GhemBOT</h1>
            <h2>Deadline Reminder Assistant Chatbot</h2>
          </div>
        </div>

        <div className="d-flex flex-column align-items-center justify-content-center">
          <ChatBox />
        </div>
      </div>
    </>
  );
}

export default App;

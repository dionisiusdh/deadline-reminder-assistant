import React from "react";
import ChatBox from "./components/chat/ChatBox";
import "./App.css";

function App() {
  return (
    <>
      <div className="container d-flex flex-column align-items-center justify-content-center">
        <div className="home-title">
          <div className="d-flex flex-column align-items-center">
            <h1>GhemBOT</h1>
            <h2>Deadline Reminder Assistant Chatbot</h2>
          </div>
        </div>

        <ChatBox />
      </div>
      <style>
        {`
          .home-title {
            background-color: #181717;
            color: #FFF;
            width: 60%;
            padding: 10px 0;
          }
        `}
      </style>
    </>
  );
}

export default App;

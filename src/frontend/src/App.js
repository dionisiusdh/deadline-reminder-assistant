import React from "react";
import ChatBox from "./components/chat/ChatBox";
import "./App.css";

function App() {
  return (
    <>
      <div className="container d-flex flex-column align-items-center justify-content-center">
        <div className="home-title">
          <div className="home-title-content d-flex flex-column align-items-start">
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
            padding: .5rem 2rem;
          }

          .home-title-content h1 {
            font-size: 2rem;
            margin-left: -2px;
          }

          .home-title-content h2 {
            font-size: 1rem;
            font-weight: 200;
          }
        `}
      </style>
    </>
  );
}

export default App;

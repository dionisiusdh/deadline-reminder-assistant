import React from "react";
import ChatBox from "./components/chat/ChatBox";
import "./App.css";

function App() {
  const [gender, setGender] = React.useState(0);
  return (
    <>
      <div className="container d-flex flex-column align-items-center justify-content-center">
        <div className="home-title">
          <div className="d-flex flex-row justify-content-between">
            <div className="home-title-content d-flex flex-column align-items-start">
              <h1>GhemBOT</h1>
              <h2>Deadline Reminder Assistant Chatbot</h2>
            </div>
            <div className="d-flex flex-row align-items-center">
              {gender === 0 ? (
                <>
                  <img
                    src="https://previews.123rf.com/images/victor85/victor851711/victor85171100224/90388679-male-sex-symbol-circle-icon-black-round-minimalist-icon-isolated-on-white-background-gender-symbol-s.jpg"
                    alt="pic"
                    onClick={() => setGender(0)}
                    className="img-selected"
                  />
                  <img
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7FKv6jQfsogh9NRdn-wfRdYhIVxz5amLlmw&usqp=CAU"
                    alt="pic"
                    onClick={() => setGender(1)}
                    className="img-unselected"
                  />
                </>
              ) : (
                <>
                  <img
                    src="https://previews.123rf.com/images/victor85/victor851711/victor85171100224/90388679-male-sex-symbol-circle-icon-black-round-minimalist-icon-isolated-on-white-background-gender-symbol-s.jpg"
                    alt="pic"
                    onClick={() => setGender(0)}
                    className="img-unselected"
                  />
                  <img
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7FKv6jQfsogh9NRdn-wfRdYhIVxz5amLlmw&usqp=CAU"
                    alt="pic"
                    onClick={() => setGender(1)}
                    className="img-selected"
                  />
                </>
              )}
            </div>
          </div>
        </div>

        <ChatBox gender={gender} />
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

          .img-selected:hover {
            cursor: pointer;
          }

          .img-unselected {
            opacity: 0.5;
          }

          .img-unselected:hover {
            cursor: pointer;
          }

          @media screen and (max-width: 800px) {
            .home-title {
              width: 100%; 
            }
          }
        `}
      </style>
    </>
  );
}

export default App;

import React from "react";
import MessageBox from "./MessageBox";

const ChatWindow = (props) => {
  const { messages, messageEndRef, gender } = props;

  return (
    <>
      <div className="chat-window">
        {messages.map((message) => {
          return (
            <div className="">
              <MessageBox message={message} gender={gender}/>
            </div>
          );
        })}
        <div ref={messageEndRef} />
      </div>
      <style>
        {`
            .chat-window {
                overflow-y: auto;
                width: 100%;
                padding: 15px;
            }

            ::-webkit-scrollbar {
              width: .3rem;
            }
            
            ::-webkit-scrollbar-track {
              background: #1e1e24;
            }
            
            ::-webkit-scrollbar-thumb {
              background: #6649b8;
              border-radius: 2px;
            }
            
        `}
      </style>
    </>
  );
};

export default ChatWindow;

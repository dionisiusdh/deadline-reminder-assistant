import React from "react";
import MessageBox from "./MessageBox";

const ChatWindow = (props) => {
  const { messages, messageEndRef } = props;

  return (
    <>
      <div className="chat-window">
        {messages.map((message) => {
          return (
            <div className="">
              <MessageBox message={message} />
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
                
            }

            ::-webkit-scrollbar {
                width: .5rem;
              }
              ::-webkit-scrollbar-thumb {
                background-color: #777777;
                border-radius: 2px;
              }
            
        `}
      </style>
    </>
  );
};

export default ChatWindow;

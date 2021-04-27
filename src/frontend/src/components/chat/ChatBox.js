import React, { useRef, useState } from "react";
import ChatInput from "./ChatInput";
import ChatWindow from "./ChatWindow";

const ChatBox = () => {
  const messageEndRef = useRef(null);

  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const messagesTest = [
    {
      sender: "bot",
      content: "Welcome to GhemBOT",
    },
  ];

  const [messages, setMessages] = useState(messagesTest);

  const addMessages = (newMessages) => {
    setMessages([...messages, ...newMessages]);
  };
  return (
    <>
      <div className="chat-box d-flex flex-column justify-content-between align-items-center">
        <ChatWindow messages={messages} messageEndRef={messageEndRef} />

        <ChatInput scrollToBottom={scrollToBottom} addMessages={addMessages} />
      </div>
      <style>
        {`
            .chat-box {
                background-color: rgb(40, 37, 53);
                width: 60%;
                height: 80vh;
                max-height: 80vh;
            }
          `}
      </style>
    </>
  );
};

export default ChatBox;

import React, { useRef, useState } from "react";
import ChatInput from "./ChatInput";
import ChatWindow from "./ChatWindow";

const ChatBox = (props) => {
  const { gender } = props
  const messageEndRef = useRef(null);

  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const messagesTest = [
    {
      sender: "bot",
      content: "Halo! Namaku GhemBOT, personal assistant kamu!",
    },
  ];

  const [messages, setMessages] = useState(messagesTest);

  const addMessages = (newMessages) => {
    setMessages([...messages, ...newMessages]);
  };
  return (
    <>
      <div className="chat-box d-flex flex-column justify-content-between align-items-center">
        <ChatWindow messages={messages} messageEndRef={messageEndRef} gender={gender}/>

        <ChatInput scrollToBottom={scrollToBottom} addMessages={addMessages} />
      </div>
      <style>
        {`
            .chat-box {
                background-color: rgb(40, 37, 53);
                width: 60%;
                height: 86.5vh;
                max-height: 86.5vh;
            }
          `}
      </style>
    </>
  );
};

export default ChatBox;

import axios from "axios";
import React, { useEffect, useState } from "react";

const ChatInput = (props) => {
  const { scrollToBottom, addMessages } = props;
  const [inputContent, setInputContent] = useState("");

  const handleSendMessage = async () => {
    if (inputContent.trim()) {
      console.log(inputContent);

      var newMessages = [
        {
          sender: "user",
          content: inputContent,
        },
      ];

      setInputContent("");

      const requestBody = {
        msg: inputContent,
      };

      axios
        .post("http://localhost:5000/bot", requestBody)
        .then((res) => {
          console.log(res.data.reply);
          const reply = {
            sender: "bot",
            content: res.data.reply,
          };

          newMessages = [...newMessages, reply];
        })
        .catch(() => {
          console.log("errr");
          const reply = {
            sender: "bot",
            content: "Error occured!",
          };

          newMessages = [...newMessages, reply];
        })
        .finally(() => {
          addMessages(newMessages);
          scrollToBottom();
        });
    }
  };

  return (
    <>
      <div className="chat-input-box w-100 d-flex align-items-center">
        <div className="chat-input-container w-100 ml-2 mt-2 mb-2">
          <input
            className="chat-input w-100"
            value={inputContent}
            onChange={(e) => setInputContent(e.target.value)}
            onKeyDown={(e) => (e.key === "Enter" ? handleSendMessage() : null)}
          />
        </div>
        <div className="m-2">
          <button className="chat-input-btn" onClick={handleSendMessage}>
            {">"}
          </button>
        </div>
      </div>

      <style>
        {`
            .chat-input {
                border: none;
                background: #d9d9d9;
                padding: .5rem 1rem;
                border-radius: 7px;
            }

            .chat-input:focus {
                outline: none;
            }

            .chat-input-box {
                background: #bbbbbb;
                
            }

            .chat-input-btn {
                background: #3F88C5;
                padding: .5rem 1rem;
                color: white;
                border: none;
                border-radius: 7px;
            }
          `}
      </style>
    </>
  );
};

export default ChatInput;

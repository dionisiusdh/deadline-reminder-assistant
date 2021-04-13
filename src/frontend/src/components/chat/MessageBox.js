import React from "react";

const MessageBox = (props) => {
  const { message } = props;

  const getMessageClassName = () => {
    if (message.sender == "user") {
      return "justify-content-end text-right";
    } else {
      return "";
    }
  };

  const getMessageBoxClassName = () => {
    if (message.sender == "user") {
      return "msg-content-box-user";
    } else {
      return "msg-content-box-bot";
    }
  };
  return (
    <>
      <div className={`msg d-flex ${getMessageClassName()}`}>
        <div className={`msg-content-box m-1 ${getMessageBoxClassName()}`}>
          <p className="msg-content">{message.content}</p>
        </div>
      </div>
      <style>
        {`
            .msg {
                width: 100%;
            }
            .msg-content-box {
                max-width: 90%;
                border-radius: 5px;
                word-break:break-word;
            }

            .msg-content-box-user {
                background: #B5BD89;
            }

            .msg-content-box-bot {
                background: #d9d9d9;
            }

            .msg-content {
                padding: 0;
                margin: .5rem 1.5rem;
            }


          `}
      </style>
    </>
  );
};

export default MessageBox;

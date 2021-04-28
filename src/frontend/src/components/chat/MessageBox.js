import React from "react";

const MessageBox = (props) => {
  const { message, gender } = props;

  const getMessageClassName = () => {
    if (message.sender === "user") {
      return "justify-content-end text-right";
    } else {
      return "";
    }
  };

  const getMessageBoxClassName = () => {
    if (message.sender === "user") {
      if (gender === 0) {
        return "msg-content-box-user";
      } else {
        return "msg-content-box-user-female";
      }
    } else {
      return "msg-content-box-bot";
    }
  };

  const getParsedString = (message) => {
    const seperattedNewLineString = message.split("\n");

    return (
      <>
        {seperattedNewLineString.map((words, index) => {
          if (index === 0) {
            return words;
          } else {
            return (
              <>
                <br />
                {words}
              </>
            );
          }
        })}
      </>
    );
  };
  return (
    <>
      <div className={`msg d-flex align-items-center ${getMessageClassName()}`}>
        {message.sender === "user" ? (
          gender === 0 ? (
            <>
              <div
                className={`msg-content-box m-1 ${getMessageBoxClassName()}`}
              >
                <p className="msg-content">
                  {getParsedString(message.content)}
                </p>
              </div>
              <img
                src="https://i.pinimg.com/originals/51/f6/fb/51f6fb256629fc755b8870c801092942.png"
                alt="pic"
              />
            </>
          ) : (
            <>
              <div
                className={`msg-content-box m-1 ${getMessageBoxClassName()}`}
              >
                <p className="msg-content">
                  {getParsedString(message.content)}
                </p>
              </div>
              <img src="https://i.ibb.co/BwpS5mB/perempuan.png" alt="pic" />
            </>
          )
        ) : (
          <>
            <img
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSsiNvOHxUiSPKEUAS3h2lIfU-RRDugpDidA&usqp=CAU"
              alt="pic"
            />
            <div className={`msg-content-box m-1 ${getMessageBoxClassName()}`}>
              <p className="msg-content">{getParsedString(message.content)}</p>
            </div>
          </>
        )}
      </div>
      <style>
        {`
            .msg {
                width: 100%;
                margin-bottom: 10px;
            }
            .msg-content-box {
                max-width: 80%;
                line-height: 20px;
                border-radius: 20px;
                word-break:break-word;
            }

            .msg-content-box-user {
                color: #FFF;
                background: #0b93f6;
            }

            .msg-content-box-user-female {
                color: #FFF;
                background: #fc46aa;
            }

            .msg-content-box-bot {
                background: #d9d9d9;
            }

            .msg-content {
                padding: 0;
                margin: .7rem 1.3rem;
            }

            img {
              width: 40px;
              height: 40px;
              border-radius: 50%;
              margin: 2px 5px;
            }
          `}
      </style>
    </>
  );
};

export default MessageBox;

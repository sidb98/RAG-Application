import React from 'react';
import '../Chat.css';

const ChatMessage = ({ message }) => {
  return (
    <div className={`message-container ${message.sender}`}>
      <div className={`message-bubble ${message.sender}`}>
        {message.text}
      </div>
    </div>
  );
};

export default ChatMessage;

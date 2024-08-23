import React, { useState } from 'react';
import '../Chat.css';
import ChatMessage from '../ChatMessage';
import ChatInput from '../ChatInput';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { text: 'Hello human, How can I help you?', sender: 'bot' },
  ]);

  const handleSendMessage = (message, sender) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, sender: sender },
    ]);
  };

  return (
    <div className="chat-container">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))}
      </div>   
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatInterface;

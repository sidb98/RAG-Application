import React, { useState } from 'react';
import '../Chat.css';
import axios from 'axios';

const baseURL = process.env.REACT_APP_API_BASE_URL;

export default function ChatInput({ onSendMessage }) {
  const [inputValue, setInputValue] = useState('');

  const formatSources = (sources) => {
    sources = [...new Set(sources)];
    let data_source = sources.map((src) => {
      let lastColonIndex = src.lastIndexOf(':');
      return src.substring(0, lastColonIndex);
    });
    let data_source_string = "Sources: " + data_source.join(', ');
    return data_source_string;
  }


  const handleSendMessage = () => {
    if (inputValue.trim() !== '') {
      onSendMessage(inputValue, 'user');
      axios.post(`${baseURL}/query`, { query_string: inputValue })
      .then((res) => {
        console.log(res.data);
        onSendMessage(res.data.response_text, 'bot');
        onSendMessage(formatSources(res.data.sources), 'source');

      })
      .catch((err) => console.error(err));
      setInputValue('');
    }
  };


  return (
    <div className="input-container">
      <input
        className="input-field"
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
        placeholder="Type your message here..."
      />
      <button className="send-button" onClick={handleSendMessage}>
        Send
      </button>
    </div>
  );
}





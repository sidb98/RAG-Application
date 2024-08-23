import React from 'react';
import ChatInterface from './ChatInterface';
import SideBar from './SideBar';
import './App.css';

const App = () => {
  return (
    <div className="app-container">
      <SideBar />
      <ChatInterface />
    </div>
  );
};

export default App;

import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import { v4 as uuidv4 } from 'uuid';

function App() {
  // Generate session ID on first load or retrieve from local storage
  const [sessionId] = useState(() => {
    const stored = localStorage.getItem('tesco_session_id');
    if (stored) return stored;
    const newId = uuidv4();
    localStorage.setItem('tesco_session_id', newId);
    return newId;
  });

  return (
    <div className="app-container">
      <ChatInterface sessionId={sessionId} />
    </div>
  );
}

export default App;

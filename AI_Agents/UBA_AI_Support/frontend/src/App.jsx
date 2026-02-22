import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { Send, User, Bot, Loader2 } from 'lucide-react';

const App = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I am UBA AI Support. How can I assist you with your banking needs today?",
      id: 'welcome'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(localStorage.getItem('uba_session_id') || null);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input, id: Date.now() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          session_id: sessionId
        })
      });

      if (!response.ok) throw new Error('Failed to connect to server');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMsgId = Date.now() + 1;
      let assistantContent = '__TYPING__';

      setMessages(prev => [...prev, { role: 'assistant', content: assistantContent, id: assistantMsgId }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '').trim();

            if (dataStr === '[DONE]') {
              setIsLoading(false);
              continue;
            }

            try {
              const data = JSON.parse(dataStr);

              if (data.session_id && !sessionId) {
                setSessionId(data.session_id);
                localStorage.setItem('uba_session_id', data.session_id);
              }

              if (data.content) {
                if (assistantContent === '__TYPING__') {
                  assistantContent = data.content;
                } else {
                  assistantContent += data.content;
                }
                setMessages(prev => prev.map(msg =>
                  msg.id === assistantMsgId ? { ...msg, content: assistantContent } : msg
                ));
              }
            } catch (e) {
              console.error('Error parsing SSE data', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "I'm sorry, I'm experiencing some technical difficulties. Please try again later.",
        id: Date.now() + 2
      }]);
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="header-logo">
          <img src="/assets/logo.png" alt="UBA Logo" />
          <span className="header-title">UBA AI Support</span>
        </div>
      </header>

      <div className="chat-window" ref={scrollRef}>
        {messages.map((msg, index) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-sender">
              {msg.role === 'user' ? 'You' : 'UBA Support'}
            </div>
            <div className={`message-bubble ${msg.role === 'assistant' && isLoading && index === messages.length - 1 ? 'streaming' : ''}`}>
              <div className="message-content">
                {msg.content === '__TYPING__' ? (
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                ) : (
                  <>
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeRaw]}
                    >
                      {msg.content}
                    </ReactMarkdown>
                    {msg.role === 'assistant' && isLoading && index === messages.length - 1 && (
                      <div className="typing-indicator mini">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <form className="input-area" onSubmit={handleSubmit}>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about UBA services, accounts, or support..."
            disabled={isLoading}
          />
        </div>
        <button type="submit" className="send-btn" disabled={isLoading || !input.trim()}>
          {isLoading ? <Loader2 className="animate-spin" /> : <Send size={20} />}
        </button>
      </form>
    </div>
  );
};

export default App;

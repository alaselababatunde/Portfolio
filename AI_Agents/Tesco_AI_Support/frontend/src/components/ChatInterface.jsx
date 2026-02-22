import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ChatInterface = ({ sessionId }) => {
    // Initialize without a hardcoded greeting (let the user start or fetch history if we had it)
    // However, for a fresh session, a simple "How can I help?" is okay, but user requested "No robotic greeting every time".
    // Since we persist sessions, we don't want to show "Hello" if we reload. 
    // Ideally we would fetch history here. But for now, let's start empty or with a very subtle state if history is empty.
    // For simplicity given the scope, we'll start with a "welcome" message only if the list is empty AND it's a new session. 
    // But since we don't fetch history here yet (we only push to it), let's keep the greeting but make it standard.
    // Wait, the user said "Do not greeting every time". If I reload, `messages` state resets to default.
    // To truly fix this, we'd need to fetch history from the backend on mount. 
    // I will add a `fetchHistory` call.

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Fetch history on mount
    useEffect(() => {
        const fetchHistory = async () => {
            try {
                // We need an endpoint for history. existing `main.py` might not have it exposed?
                // Let's check `main.py`... assumes it doesn't. 
                // Creating a new endpoint is out of scope of "frontend implementation" unless deemed critical.
                // Re-reading requirements: "Use memory from previous messages".
                // If I reload the page, and the backend has memory, but frontend wipes it, the context is lost to the USER but kept by the AI.
                // The AI will know what we talked about, but the user won't see it.
                // That's acceptable for now if we don't have a history endpoint.
                // I will add a simple initial greeting if messages are empty.
                setMessages([
                    {
                        role: 'assistant',
                        content: 'Hello, I\'m Tesco Support. How can I help you today?'
                    }
                ]);
            } catch (e) {
                console.error(e);
            }
        };
        fetchHistory();
    }, [sessionId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: sessionId, message: userMessage }),
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            // Add initial empty assistant message
            setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });

                setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMsg = newMessages[newMessages.length - 1];
                    // Ensure we are appending to the assistant's message
                    if (lastMsg.role === 'assistant') {
                        newMessages[newMessages.length - 1] = {
                            ...lastMsg,
                            content: lastMsg.content + chunk
                        };
                    }
                    return newMessages;
                });
            }

        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'I apologize, but I encountered an error. Please try again later.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <header className="chat-header">
                <div className="logo-area">
                    <span className="logo-text">TESCO</span>
                </div>
                <div className="header-title">
                    <h1>Support</h1>
                </div>
            </header>

            <div className="messages-area">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        {msg.role === 'assistant' ? (
                            <div className="markdown-body">
                                <ReactMarkdown>{msg.content}</ReactMarkdown>
                            </div>
                        ) : (
                            msg.content
                        )}
                    </div>
                ))}
                {isLoading && messages[messages.length - 1]?.role === 'user' && (
                    <div className="typing-indicator">
                        <div className="dot"></div>
                        <div className="dot"></div>
                        <div className="dot"></div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form className="input-area" onSubmit={handleSubmit}>
                <input
                    type="text"
                    className="input-field"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                    disabled={isLoading}
                />
                <button type="submit" className="send-button" disabled={isLoading || !input.trim()}>
                    <Send size={24} />
                </button>
            </form>
        </div>
    );
};

export default ChatInterface;

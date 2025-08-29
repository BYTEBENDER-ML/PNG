import React, { useState, useRef, useEffect } from 'react';

// Main App component for the entire chatbot application
const App = () => {
  const [messages, setMessages] = useState([
    {
      sender: 'InnovateBot',
      text: "Hello! I'm InnovateBot, your AI colleague. I'm here to help you brainstorm solutions, streamline processes, or tackle any modern-day problem you're facing. What's on your mind today?",
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scrolls to the bottom of the chat window on new messages
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Handles the user sending a message
  const handleSendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage = { sender: 'You', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const chatHistory = [...messages, userMessage];
      const prompt = `
        You are InnovateBot, a professional, encouraging, and collaborative AI designed to help employees solve modern-day company problems. Your purpose is to engage with employees, understand their challenges, and offer actionable advice, tools, or innovative solutions.

        Your responses should be:
        1. Professional and encouraging.
        2. Focused on problem-solving, project management, career growth, or creative challenges.
        3. Clear and concise.
        4. Structured, using bullet points or numbered lists when appropriate.
        5. You can ask clarifying questions to better understand the user's needs.

        Here is the conversation history:
        ${chatHistory.map(m => `${m.sender}: ${m.text}`).join('\n')}

        InnovateBot:`;

      const payload = {
        contents: [{ role: "user", parts: [{ text: prompt }] }]
      };

      const apiKey = "";
      const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

      const response = await fetchWithExponentialBackoff(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      let botResponseText = "Sorry, I couldn't get a response. Please try again.";

      if (result.candidates && result.candidates.length > 0) {
        botResponseText = result.candidates[0].content.parts[0].text;
      }

      setMessages((prevMessages) => [...prevMessages, { sender: 'InnovateBot', text: botResponseText }]);
    } catch (error) {
      console.error('Error fetching from API:', error);
      setMessages((prevMessages) => [...prevMessages, { sender: 'InnovateBot', text: 'Apologies, but an error occurred. Please try again later.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Utility function for exponential backoff during API calls
  const fetchWithExponentialBackoff = async (url, options, retries = 5, delay = 1000) => {
    for (let i = 0; i < retries; i++) {
      try {
        const response = await fetch(url, options);
        if (response.status !== 429) { // 429 is Too Many Requests
          return response;
        }
      } catch (error) {
        // Continue with retries on network errors
      }
      await new Promise(res => setTimeout(res, delay * Math.pow(2, i)));
    }
    throw new Error('API request failed after multiple retries.');
  };

  // Handles 'Enter' key press in the textarea
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 antialiased">
      <div className="flex flex-col flex-1 max-w-4xl w-full mx-auto p-4 md:p-6 overflow-hidden">
        
        {/* Chat Header */}
        <div className="bg-white rounded-t-xl shadow-lg p-4 mb-4 flex items-center justify-between">
          <div className="flex items-center">
            <div className="relative">
              <span className="absolute top-0 right-0 h-2 w-2 rounded-full bg-green-500 ring-2 ring-white"></span>
              <div className="flex items-center justify-center h-10 w-10 bg-blue-500 rounded-full text-white font-bold text-lg">
                AI
              </div>
            </div>
            <div className="ml-4">
              <h1 className="text-xl font-bold text-gray-800">InnovateBot</h1>
              <p className="text-sm text-gray-500">Your AI Colleague</p>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto bg-white rounded-b-xl shadow-lg p-4 md:p-6 mb-4 space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.sender === 'You' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs md:max-w-md p-4 rounded-3xl shadow-sm ${
                  msg.sender === 'You'
                    ? 'bg-blue-500 text-white rounded-br-none'
                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.text}</p>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-xs md:max-w-md p-4 rounded-3xl shadow-sm bg-gray-200 text-gray-800 rounded-bl-none">
                <span className="animate-pulse">InnovateBot is thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white rounded-xl shadow-lg p-4">
          <div className="flex items-end space-x-2">
            <textarea
              className="flex-1 p-3 border border-gray-300 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              placeholder="Type your message here..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              rows={1}
              style={{ maxHeight: '150px' }}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || input.trim() === ''}
              className="px-6 py-3 bg-blue-500 text-white rounded-xl shadow-md hover:bg-blue-600 transition-colors duration-200 disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;

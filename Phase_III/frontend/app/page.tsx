'use client';

import { useState, useRef, useEffect } from 'react';

export default function ChatInterface() {
  const [messages, setMessages] = useState<{id: number, text: string, sender: 'user' | 'bot'}[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [userId, setUserId] = useState<string>('');
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Initialize session and user ID
  useEffect(() => {
    // Check for authentication token
    const authToken = localStorage.getItem('authToken');
    if (authToken) {
      setIsLoggedIn(true);

      // Get user info from token or local storage
      const storedUserId = localStorage.getItem('user_id');
      if (storedUserId) {
        setUserId(storedUserId);
      } else {
        // If logged in but no user ID stored, we might need to get it from the backend
        const newUserID = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        localStorage.setItem('user_id', newUserID);
        setUserId(newUserID);
      }
    } else {
      // Generate or retrieve session ID
      const storedSessionId = localStorage.getItem('chat_session_id');
      if (storedSessionId) {
        setSessionId(storedSessionId);
      } else {
        const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        localStorage.setItem('chat_session_id', newSessionId);
        setSessionId(newSessionId);
      }

      // Generate or retrieve user ID
      const storedUserId = localStorage.getItem('user_id');
      if (storedUserId) {
        setUserId(storedUserId);
      } else {
        const newUserID = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        localStorage.setItem('user_id', newUserID);
        setUserId(newUserID);
      }
    }

    // Add welcome message
    setMessages([
      {
        id: 1,
        text: "Hello! I'm your AI assistant for managing tasks. You can ask me to create, update, or delete tasks. How can I help you today?",
        sender: 'bot'
      }
    ]);
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user' as const
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare headers with authentication token if available
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      const authToken = localStorage.getItem('authToken');
      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }

      // Call the backend API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers,
        body: JSON.stringify({
          user_id: userId,
          session_id: sessionId,
          message: inputValue
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot' as const
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I encountered an error processing your request. Please try again.",
        sender: 'bot' as const
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className="text-xl font-bold text-gray-900">Advanced Task Manager</h1>
              </div>
              <div className="flex items-center space-x-4">
                {isLoggedIn ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    <span className="text-sm text-gray-600">Connected</span>
                    <button
                      onClick={() => {
                        localStorage.removeItem('authToken');
                        localStorage.removeItem('user_id');
                        setIsLoggedIn(false);
                      }}
                      className="text-sm bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
                    >
                      Logout
                    </button>
                  </div>
                ) : (
                  <div className="flex space-x-2">
                    <a href="/login" className="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                      Login
                    </a>
                    <a href="/signup" className="text-sm bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500">
                      Sign Up
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        <main className="mt-8">
          <div className="max-w-4xl mx-auto px-4 py-8">
            <header className="mb-8 text-center">
              <h1 className="text-3xl font-bold text-gray-900">Todo AI Assistant</h1>
              <p className="text-gray-600 mt-2">Chat with your AI task manager</p>
            </header>

            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              {/* Chat Messages */}
              <div className="h-[60vh] overflow-y-auto p-4 bg-gray-50">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`mb-4 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-2 ${
                        message.sender === 'user'
                          ? 'bg-blue-500 text-white rounded-br-none'
                          : 'bg-gray-200 text-gray-800 rounded-bl-none'
                      }`}
                    >
                      {message.text}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="mb-4 flex justify-start">
                    <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 rounded-bl-none max-w-[80%]">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                        <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="border-t border-gray-200 p-4 bg-white">
                <form onSubmit={handleSubmit} className="flex space-x-2">
                  <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Type your message here..."
                    className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={isLoading}
                  />
                  <button
                    type="submit"
                    disabled={!inputValue.trim() || isLoading}
                    className="bg-blue-500 text-white rounded-lg px-6 py-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Send
                  </button>
                </form>

                <div className="mt-3 text-sm text-gray-500">
                  <p>Examples: "Create a task to buy groceries", "Mark task #1 as complete", "List my tasks"</p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
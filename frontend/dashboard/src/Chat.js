import React, { useState, useEffect, useRef } from 'react';
import { getAgentsList, chatWithAgent } from './api';

function Chat({ token, onLogout }) {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState('accounts');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    getAgentsList(token)
      .then((data) => setAgents(data.agents))
      .catch(() => setError('Could not load agents list'));
  }, [token]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const data = await chatWithAgent(token, input, selectedAgent, sessionId);
      setSessionId(data.session_id);
      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }]);
    } catch (err) {
      const detail = err.response?.data?.detail || 'Something went wrong';
      setError(typeof detail === 'string' ? detail : 'Request failed');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">AI Business Platform</h1>
        <button
          onClick={onLogout}
          className="text-sm text-red-600 hover:text-red-800"
        >
          Logout
        </button>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar: agent selector */}
        <div className="w-64 bg-white border-r p-4">
          <h2 className="text-sm font-semibold text-gray-500 mb-3">SELECT AGENT</h2>
          <div className="space-y-2">
            {agents.map((agent) => (
              <button
                key={agent.name}
                onClick={() => {
                  setSelectedAgent(agent.name);
                  setMessages([]);
                  setSessionId(null);
                }}
                className={`w-full text-left px-3 py-2 rounded ${
                  selectedAgent === agent.name
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <div className="font-medium capitalize">{agent.name}</div>
                <div className="text-xs opacity-75">{agent.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Chat area */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-gray-400 text-center mt-10">
                Start a conversation with the {selectedAgent} agent
              </div>
            )}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-lg px-4 py-2 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-white border text-gray-800'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white border px-4 py-2 rounded-lg text-gray-400">
                  Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className="bg-red-100 text-red-700 px-4 py-2 text-sm">{error}</div>
          )}

          <form onSubmit={handleSend} className="p-4 bg-white border-t flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={`Message the ${selectedAgent} agent...`}
              className="flex-1 border rounded px-4 py-2"
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Chat;
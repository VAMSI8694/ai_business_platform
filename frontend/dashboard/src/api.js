import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('grant_type', 'password');
  formData.append('username', username);
  formData.append('password', password);

  const response = await axios.post(`${API_BASE_URL}/auth/token`, formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });

  return response.data; // { access_token, token_type }
};

export const register = async (username, email, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/register`, {
    username, email, password
  });
  return response.data;
};
export const getAgentsList = async (token) => {
  const response = await axios.get(`${API_BASE_URL}/agents/list`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const chatWithAgent = async (token, message, agentName, sessionId) => {
  const response = await axios.post(
    `${API_BASE_URL}/agents/chat`,
    {
      message,
      agent_name: agentName,
      session_id: sessionId || null,
      context: null
    },
    {
      headers: { Authorization: `Bearer ${token}` }
    }
  );
  return response.data;
};
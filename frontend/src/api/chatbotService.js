import axios from 'axios';
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://120.76.249.191:8000';

export const chatbotService = {
  async ask(message) {
    const response = await axios.post(`${API_BASE_URL}/chatbot/ask`, { message });
    return response.data;
  }
}; 
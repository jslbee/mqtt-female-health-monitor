import axios from 'axios';

// 从环境变量获取API地址，如果没有则使用默认值
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const menstrualService = {
    async predictNextPeriod(clientId, lastPeriodDate) {
        try {
            const response = await axios.post(`${API_BASE_URL}/predict`, {
                client_id: clientId,
                last_period_date: lastPeriodDate
            });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || '预测服务出错');
        }
    }
}; 
import axios from 'axios';

// 从环境变量获取API地址，如果没有则使用默认值
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://120.76.249.191:8000';

export const menstrualService = {
    async predictNextPeriod(lastPeriodDate) {
        try {
            const response = await axios.post(`${API_BASE_URL}/predict`, {
                last_period_date: lastPeriodDate
            });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || '预测服务出错');
        }
    },
    async getClientIds() {
        const response = await axios.get(`${API_BASE_URL}/client_ids`);
        return response.data;
    }
}; 
import api from './config';

// 健康数据相关 API
export const healthApi = {
  // 获取心率数据
  getHeartRate: () => api.get('/heart-rate'),
  
  // 获取体温数据
  getTemperature: () => api.get('/temperature'),
  
  // 获取经期数据
  getMenstrual: () => api.get('/menstrual'),
  
  // 获取预测数据
  async getPrediction() {
    // 模拟 API 返回数据
    return {
      heartRate: '75',
      temperature: '36.5',
      nextCycle: '2023-11-01'
    };
  },
  
  // 保存心情数据
  saveMood: (moodData) => api.post('/mood', moodData),
  
  // 获取健康指标摘要
  getHealthSummary: () => api.get('/health-summary')
};

// 用户相关 API
export const userApi = {
  // 用户登录
  login: (credentials) => api.post('/auth/login', credentials),
  
  // 用户注册
  register: (userData) => api.post('/auth/register', userData),
  
  // 获取用户信息
  getUserInfo: () => api.get('/user/info'),
  
  // 更新用户信息
  updateUserInfo: (userData) => api.put('/user/info', userData)
};

// 消息相关 API
export const messageApi = {
  // 获取消息列表
  getMessages: () => api.get('/messages'),
  
  // 发送消息
  sendMessage: (messageData) => api.post('/messages', messageData),
  
  // 标记消息为已读
  markAsRead: (messageId) => api.put(`/messages/${messageId}/read`)
}; 
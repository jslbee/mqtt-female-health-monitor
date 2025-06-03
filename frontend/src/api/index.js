import axios from 'axios';

const API_BASE_URL = 'http://120.76.249.191:8000'; // 云服务器后端地址

// 注册API
export const registerApi = (username, password) => {
  return axios.post(`${API_BASE_URL}/register`,
    new URLSearchParams({ username, password }),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
};

// 获取token时用
export const loginApi = (username, password) => {
  return axios.post(`${API_BASE_URL}/token`, 
    new URLSearchParams({ username, password }), // 按后端要求用表单格式
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  );
};

// 通用的带token请求
function authGet(url, token) {
  return axios.get(`${API_BASE_URL}${url}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
}

// 具体API
export const healthApi = {
  // 获取心率数据
  getHeartRate: (token) => authGet('/heartrate', token),

  // 获取体温数据
  getTemperature: (token) => authGet('/temperature', token),

  // 获取月经周期数据
  getMenstrual: (token) => authGet('/menstrual', token)
};
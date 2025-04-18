// scripts.js

// 页面跳转
function goToRecords() {
    window.location.href = "records.html";
  }
  
// MQTT客户端配置
const mqttConfig = {
    host: '120.76.249.191',  // 你的MQTT服务器地址
    port: 9001,              // WebSocket端口（通常是9001或8083）
    path: '/mqtt',           // WebSocket路径，根据你的服务器配置可能不需要
    clientId: 'web-client-' + Math.random().toString(16).substr(2, 8)
};

// 创建MQTT客户端
const client = new Paho.MQTT.Client(
  mqttConfig.host, 
  mqttConfig.port, 
  mqttConfig.path,
  mqttConfig.clientId
);

// 连接选项
const options = {
  timeout: 3,
  onSuccess: onConnect,
  onFailure: function(e) {
    console.log("连接失败: " + e.errorMessage);
    setTimeout(connect, 5000); // 5秒后重试
  }
};

// 连接函数
function connect() {
  console.log("尝试连接到MQTT服务器...");
  client.connect(options);
}

// 初始连接
connect();

// 连接成功回调
function onConnect() {
    console.log('MQTT连接成功');
    
    // 根据当前页面URL决定订阅哪些主题
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage.includes('heart_rate')) {
        client.subscribe("health/wearable/heart_rate");
        console.log('已订阅心率数据主题');
    } 
    else if (currentPage.includes('temperature')) {
        client.subscribe("health/wearable/temperature");
        console.log('已订阅体温数据主题');
    }
    else if (currentPage.includes('menstrual')) {
        client.subscribe("health/userinput/menstrual_cycle");
        console.log('已订阅月经周期数据主题');
    }
    else {
        // metrics页面或首页订阅所有主题
        client.subscribe("health/wearable/heart_rate");
        client.subscribe("health/wearable/temperature");
        client.subscribe("health/userinput/menstrual_cycle");
        console.log('已订阅所有健康数据主题');
    }
}

// 消息接收处理
client.onMessageArrived = function(message) {
    console.log('收到消息:', message.payloadString);
    // 处理接收到的数据
    handleMQTTData(message.payloadString);
};

// 处理MQTT数据
function handleMQTTData(data) {
    try {
        const parsedData = JSON.parse(data);
        
        // 判断数据类型并更新相应的UI
        if (parsedData.heart_rate) {
            // 更新心率显示
            updateHeartRateUI(parsedData);
        } else if (parsedData.value || parsedData.temp) { // 体温数据
            // 更新体温显示
            updateTemperatureUI(parsedData);
        } else if (parsedData.duration) { // 月经周期数据
            // 更新月经周期显示
            updateMenstrualUI(parsedData);
        }
    } catch (error) {
        console.error('数据处理错误:', error);
    }
}

// 更新心率UI的函数
function updateHeartRateUI(data) {
    console.log('更新心率UI:', data);
    
    // 获取心率显示元素
    const heartRateElement = document.getElementById('heart-rate-value');
    if (heartRateElement) {
        heartRateElement.textContent = data.heart_rate.toFixed(1);
    }
    
    // 更新状态显示
    const statusElement = document.getElementById('heart-rate-status');
    if (statusElement && data.health_status) {
        statusElement.textContent = data.health_status;
    }
    
    // 更新图表（如果存在）
    if (typeof updateHeartRateChart === 'function') {
        updateHeartRateChart(data);
    }
}

// 更新体温UI的函数
function updateTemperatureUI(data) {
    console.log('更新体温UI:', data);
    
    // 获取体温值（处理不同的数据格式）
    const temperature = data.value || data.temp;
    
    // 获取体温显示元素
    const tempElement = document.getElementById('temperature-value');
    if (tempElement) {
        tempElement.textContent = temperature.toFixed(1);
    }
    
    // 更新体温状态
    const tempStatusElement = document.getElementById('temperature-status');
    if (tempStatusElement) {
        let status = '正常';
        
        if (temperature < 36.0) {
            status = '偏低';
        } else if (temperature > 37.2) {
            status = '偏高';
        }
        
        tempStatusElement.textContent = status;
    }
    
    // 更新图表（如果存在）
    if (typeof updateTemperatureChart === 'function') {
        updateTemperatureChart(data);
    }
}

// 更新月经周期UI的函数
function updateMenstrualUI(data) {
    console.log('更新月经周期UI:', data);
    
    // 获取月经周期显示元素
    const durationElement = document.getElementById('menstrual-duration');
    if (durationElement) {
        durationElement.textContent = data.duration;
    }
    
    // 更新状态信息
    const conditionElement = document.getElementById('menstrual-condition');
    if (conditionElement && data.condition) {
        conditionElement.textContent = data.condition;
    }
    
    // 更新图表（如果存在）
    if (typeof updateMenstrualChart === 'function') {
        updateMenstrualChart(data);
    }
}

// 连接MQTT服务器
client.connect(options);

// 发送数据到MQTT服务器
function sendDataToMQTT(topic, data) {
    const message = new Paho.MQTT.Message(JSON.stringify(data));
    message.destinationName = topic;
    client.send(message);
}

// 全局变量存储图表实例
let heartRateChart;
let temperatureChart;
let menstrualChart;

// 页面加载完成后初始化图表
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
});

// 初始化所有图表
function initCharts() {
    // 根据当前页面初始化相应的图表
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage.includes('heart_rate') || currentPage === 'metrics.html') {
        initHeartRateChart();
    }
    
    if (currentPage.includes('temperature') || currentPage === 'metrics.html') {
        initTemperatureChart();
    }
    
    if (currentPage.includes('menstrual') || currentPage === 'metrics.html') {
        initMenstrualChart();
    }
}

// 初始化心率图表
function initHeartRateChart() {
    const heartRateCanvas = document.getElementById('heart-rate-chart');
    if (!heartRateCanvas) return;
    
    heartRateChart = new Chart(heartRateCanvas, {
        type: 'line',
        data: {
            labels: [], // 时间标签
            datasets: [{
                label: '心率 (BPM)',
                data: [], // 心率数据
                borderColor: '#E57C9F',
                backgroundColor: 'rgba(229, 124, 159, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 500
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 40,
                    max: 140,
                    title: {
                        display: true,
                        text: '心率 (BPM)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: '时间'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '实时心率监测'
                }
            }
        }
    });
}

// 初始化体温图表
function initTemperatureChart() {
    const temperatureCanvas = document.getElementById('temperature-chart');
    if (!temperatureCanvas) return;
    
    temperatureChart = new Chart(temperatureCanvas, {
        type: 'line',
        data: {
            labels: [], // 时间标签
            datasets: [{
                label: '体温 (°C)',
                data: [], // 体温数据
                borderColor: '#4A2C40',
                backgroundColor: 'rgba(74, 44, 64, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 500
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 35,
                    max: 40,
                    title: {
                        display: true,
                        text: '体温 (°C)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: '时间'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '实时体温监测'
                }
            }
        }
    });
}

// 初始化月经周期图表
function initMenstrualChart() {
    const menstrualCanvas = document.getElementById('menstrual-chart');
    if (!menstrualCanvas) return;
    
    menstrualChart = new Chart(menstrualCanvas, {
        type: 'bar',
        data: {
            labels: [], // 日期标签
            datasets: [{
                label: '月经持续天数',
                data: [], // 月经周期数据
                backgroundColor: '#E57C9F',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '天数'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: '记录日期'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '月经周期记录'
                }
            }
        }
    });
}

// 更新心率图表
function updateHeartRateChart(data) {
    if (!heartRateChart) return;
    
    const timestamp = data.timestamp ? 
        new Date(data.timestamp).toLocaleTimeString() : 
        new Date().toLocaleTimeString();
    
    // 添加新数据点
    heartRateChart.data.labels.push(timestamp);
    heartRateChart.data.datasets[0].data.push(data.heart_rate);
    
    // 保持最新的10个数据点
    if (heartRateChart.data.labels.length > 10) {
        heartRateChart.data.labels.shift();
        heartRateChart.data.datasets[0].data.shift();
    }
    
    // 更新图表
    heartRateChart.update();
}

// 更新体温图表
function updateTemperatureChart(data) {
    if (!temperatureChart) return;
    
    const timestamp = data.timestamp ? 
        new Date(data.timestamp).toLocaleTimeString() : 
        new Date().toLocaleTimeString();
    
    // 获取体温值（处理不同的数据格式）
    const temperature = data.value || data.temp;
    
    // 添加新数据点
    temperatureChart.data.labels.push(timestamp);
    temperatureChart.data.datasets[0].data.push(temperature);
    
    // 保持最新的10个数据点
    if (temperatureChart.data.labels.length > 10) {
        temperatureChart.data.labels.shift();
        temperatureChart.data.datasets[0].data.shift();
    }
    
    // 更新图表
    temperatureChart.update();
}

// 更新月经周期图表
function updateMenstrualChart(data) {
    if (!menstrualChart) return;
    
    const timestamp = data.timestamp ? 
        new Date(data.timestamp).toLocaleDateString() : 
        new Date().toLocaleDateString();
    
    // 检查日期是否已存在
    const existingIndex = menstrualChart.data.labels.indexOf(timestamp);
    
    if (existingIndex !== -1) {
        // 如果日期已存在，更新数据
        menstrualChart.data.datasets[0].data[existingIndex] = data.duration;
    } else {
        // 添加新数据点
        menstrualChart.data.labels.push(timestamp);
        menstrualChart.data.datasets[0].data.push(data.duration);
        
        // 保持最新的6个数据点
        if (menstrualChart.data.labels.length > 6) {
            menstrualChart.data.labels.shift();
            menstrualChart.data.datasets[0].data.shift();
        }
    }
    
    // 更新图表
    menstrualChart.update();
}

// 表单提交处理函数
document.addEventListener('DOMContentLoaded', function() {
    // 月经周期数据表单
    const menstrualForm = document.getElementById('menstrual-form');
    if (menstrualForm) {
        menstrualForm.addEventListener('submit', submitMenstrualData);
    }
});

// 提交月经周期数据
function submitMenstrualData(event) {
    event.preventDefault();
    
    // 获取表单数据
    const duration = document.getElementById('menstrual-duration-input').value;
    
    // 验证输入
    if (!duration || isNaN(duration)) {
        alert('请输入有效的天数');
        return;
    }
    
    // 确定健康状态
    let condition = '';
    if (duration < 5) {
        condition = "注意！您最近可能压力过大！";
    } else if (duration <= 7) {
        condition = "很好！保持健康！";
    } else {
        condition = "注意！您的身体可能需要帮助！";
    }
    
    // 准备数据
    const data = {
        duration: parseFloat(duration),
        condition: condition
    };
    
    // 发送到MQTT服务器
    sendDataToMQTT('health/userinput/menstrual_cycle', data);
    
    // 更新本地UI显示
    const durationDisplay = document.getElementById('menstrual-duration');
    if (durationDisplay) {
        durationDisplay.textContent = duration;
    }
    
    const conditionDisplay = document.getElementById('menstrual-condition');
    if (conditionDisplay) {
        conditionDisplay.textContent = condition;
    }
    
    // 更新图表（如果存在）
    if (typeof updateMenstrualChart === 'function') {
        updateMenstrualChart(data);
    }
    
    // 清空表单
    event.target.reset();
    
    // 提示用户
    alert('月经周期数据已提交');
}

const API_BASE_URL = 'http://your-server-ip:3000/api';

// 加载历史心率数据
async function loadHeartRateHistory() {
  try {
    const response = await fetch(`${API_BASE_URL}/heart_rate`);
    const data = await response.json();
    
    if (data.length > 0 && heartRateChart) {
      // 提取最近10条数据
      const recentData = data.slice(-10);
      
      // 更新图表数据
      heartRateChart.data.labels = recentData.map(item => {
        const date = new Date(item.timestamp);
        return date.toLocaleTimeString();
      });
      
      heartRateChart.data.datasets[0].data = recentData.map(item => item.heart_rate);
      heartRateChart.update();
    }
  } catch (error) {
    console.error('加载心率历史数据失败:', error);
  }
}

// 同样方式添加体温和月经周期数据加载函数
async function loadTemperatureHistory() {
  // 类似实现...
}

async function loadMenstrualHistory() {
  // 类似实现...
}

// 在页面加载完成时调用这些函数
document.addEventListener('DOMContentLoaded', function() {
  initCharts();
  
  // 根据当前页面加载相应的历史数据
  const currentPage = window.location.pathname.split('/').pop();
  
  if (currentPage.includes('heart_rate')) {
    loadHeartRateHistory();
  } else if (currentPage.includes('temperature')) {
    loadTemperatureHistory();
  } else if (currentPage.includes('menstrual')) {
    loadMenstrualHistory();
  } else if (currentPage === 'metrics.html') {
    // 加载所有数据
    loadHeartRateHistory();
    loadTemperatureHistory();
    loadMenstrualHistory();
  }
});
  
USE health_data;

-- 查看最近的经期数据
SELECT * FROM menstrual_cycle ORDER BY time_received DESC LIMIT 5;

-- 查看最近的心率数据
SELECT * FROM heart_rate_data ORDER BY time_received DESC LIMIT 5;

-- 查看最近的温度数据
SELECT * FROM temperature_data ORDER BY time_received DESC LIMIT 5; 
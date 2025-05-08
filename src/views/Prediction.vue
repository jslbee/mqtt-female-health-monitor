<template>
  <div class="predicted">
    <h1>Prediction</h1>
    <div class="prediction-section">
      <h2>Heart Rate Prediction</h2>
      <p>Predicted heart rate: {{ predictions.heartRate }} bpm</p>
    </div>
    <div class="prediction-section">
      <h2>Temperature Prediction</h2>
      <p>Predicted temperature: {{ predictions.temperature }}°C</p>
    </div>
    <div class="prediction-section">
      <h2>Menstrual Cycle Prediction</h2>
      <p>Predicted next cycle: {{ predictions.nextCycle }}</p>
    </div>
  </div>
</template>

<script>
import { healthApi } from '../api/services';

export default {
  name: 'Prediction',
  data() {
    return {
      predictions: {
        heartRate: '--',
        temperature: '--',
        nextCycle: '--'
      }
    };
  },
  async created() {
    try {
      const data = await healthApi.getPrediction();
      this.predictions = data;
    } catch (error) {
      console.error('获取预测数据失败:', error);
    }
  }
};
</script>

<style scoped>
.predicted {
  padding: 20px;
}
.prediction-section {
  margin-bottom: 20px;
  padding: 15px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(156,91,128,0.08);
}
</style> 
<template>
  <div class="heart-rate-chart">
    <div class="card">
      <h2>心率记录</h2>
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
      <div class="form-group">
        <label for="heartRate">记录心率</label>
        <input 
          type="number" 
          id="heartRate" 
          v-model="newHeartRate" 
          placeholder="输入心率值"
        >
      </div>
      <button class="btn" @click="addHeartRate">添加记录</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'HeartRateChart',
  setup() {
    const chartCanvas = ref(null)
    const chart = ref(null)
    const newHeartRate = ref('')
    const heartRates = ref([])

    const initChart = () => {
      const ctx = chartCanvas.value.getContext('2d')
      chart.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: '心率',
            data: [],
            borderColor: '#E57C9F',
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: false,
              suggestedMin: 40,
              suggestedMax: 120
            }
          }
        }
      })
    }

    const addHeartRate = () => {
      if (!newHeartRate.value) return
      
      const now = new Date()
      const timeStr = now.toLocaleTimeString()
      heartRates.value.push({
        time: timeStr,
        value: Number(newHeartRate.value)
      })
      
      updateChart()
      newHeartRate.value = ''
    }

    const updateChart = () => {
      if (!chart.value) return
      
      chart.value.data.labels = heartRates.value.map(item => item.time)
      chart.value.data.datasets[0].data = heartRates.value.map(item => item.value)
      chart.value.update()
    }

    onMounted(() => {
      initChart()
    })

    return {
      chartCanvas,
      newHeartRate,
      addHeartRate
    }
  }
}
</script>

<style scoped>
.heart-rate-chart {
  padding: 20px;
}

.chart-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
}
</style> 
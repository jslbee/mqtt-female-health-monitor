<template>
  <div class="temperature-chart">
    <div class="card">
      <h2>体温记录</h2>
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
      <div class="form-group">
        <label for="temperature">记录体温</label>
        <input 
          type="number" 
          id="temperature" 
          v-model="newTemperature" 
          placeholder="输入体温值"
          step="0.1"
        >
      </div>
      <button class="btn" @click="addTemperature">添加记录</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'TemperatureChart',
  setup() {
    const chartCanvas = ref(null)
    const chart = ref(null)
    const newTemperature = ref('')
    const temperatures = ref([])

    const initChart = () => {
      const ctx = chartCanvas.value.getContext('2d')
      chart.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: '体温',
            data: [],
            borderColor: '#E57C9F',
            tension: 0.4,
            fill: true,
            backgroundColor: 'rgba(229, 124, 159, 0.1)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: false,
              suggestedMin: 35.5,
              suggestedMax: 37.5,
              ticks: {
                callback: value => value.toFixed(1) + '°C'
              }
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: context => context.raw.toFixed(1) + '°C'
              }
            }
          }
        }
      })
    }

    const addTemperature = () => {
      if (!newTemperature.value) return
      
      const now = new Date()
      const timeStr = now.toLocaleTimeString()
      temperatures.value.push({
        time: timeStr,
        value: Number(newTemperature.value)
      })
      
      updateChart()
      newTemperature.value = ''
    }

    const updateChart = () => {
      if (!chart.value) return
      
      chart.value.data.labels = temperatures.value.map(item => item.time)
      chart.value.data.datasets[0].data = temperatures.value.map(item => item.value)
      chart.value.update()
    }

    onMounted(() => {
      initChart()
    })

    return {
      chartCanvas,
      newTemperature,
      addTemperature
    }
  }
}
</script>

<style scoped>
.temperature-chart {
  padding: 20px;
}

.chart-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
}
</style> 
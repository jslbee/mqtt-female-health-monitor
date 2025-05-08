<template>
  <div>
    <NavBar />
    <div class="container">
      <div class="header">
        <h1>Heart Rate Data</h1>
      </div>
      <div class="chart-container">
        <div class="chart-title">
          <i class="ri-heart-pulse-line"></i>
          <h2>Heart Rate Trend</h2>
        </div>
        <canvas ref="chartCanvas"></canvas>
        <div class="stats-container">
          <div class="stat-card">
            <div class="stat-value">78</div>
            <div class="stat-label">Average Heart Rate (bpm)</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">65</div>
            <div class="stat-label">Minimum Heart Rate (bpm)</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">95</div>
            <div class="stat-label">Maximum Heart Rate (bpm)</div>
          </div>
        </div>
        <div class="data-card">
          <h3>Heart Rate Health Tips</h3>
          <p>Normal resting heart rate for adults ranges from 60-100 beats per minute, and may be lower for athletes. Consistently high resting heart rate may indicate increased stress or other health issues. Monitoring heart rate helps understand physical condition and health trends.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import Chart from 'chart.js/auto'

export default {
  name: 'HeartRate',
  components: { NavBar },
  setup() {
    const chartCanvas = ref(null)
    onMounted(() => {
      const ctx = chartCanvas.value.getContext('2d')
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan 1', 'Jan 2', 'Jan 3', 'Jan 4', 'Jan 5', 'Jan 6', 'Jan 7'],
          datasets: [{
            label: 'Heart Rate (bpm)',
            data: [75, 80, 78, 85, 82, 72, 76],
            borderColor: '#E57C9F',
            backgroundColor: 'rgba(229, 124, 159, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointBackgroundColor: '#E57C9F',
            pointBorderColor: '#FFF',
            pointRadius: 5,
            pointHoverRadius: 7
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top', labels: { color: '#4A2C40', font: { size: 14 } } },
            tooltip: { backgroundColor: 'rgba(74, 44, 64, 0.8)' }
          },
          scales: {
            y: {
              beginAtZero: false,
              min: 60,
              max: 100,
              grid: { color: 'rgba(74, 44, 64, 0.1)' },
              ticks: { color: '#4A2C40', font: { size: 12 }, callback: v => v + ' bpm' },
              title: { display: true, text: 'Heart Rate (bpm)', color: '#4A2C40', font: { size: 14 } }
            },
            x: {
              grid: { color: 'rgba(74, 44, 64, 0.05)' },
              ticks: { color: '#4A2C40', font: { size: 12 } }
            }
          }
        }
      })
    })
    return { chartCanvas }
  }
}
</script>

<style scoped>
.container { max-width: 1000px; margin: 0 auto; padding: 30px; }
.header { text-align: center; padding: 30px 20px 40px; }
.chart-container { background: white; border-radius: 8px; padding: 20px; margin: 20px 0; }
.chart-title { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 25px; }
.stats-container { display: flex; gap: 20px; margin-top: 30px; }
.stat-card { background: #fff; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 4px 12px rgba(156,91,128,0.08); }
.stat-value { font-size: 32px; font-weight: bold; color: #E57C9F; margin-bottom: 5px; }
.stat-label { font-size: 14px; color: #4A2C40; }
.data-card { background: rgba(229,124,159,0.05); border-radius: 15px; padding: 20px; margin-top: 30px; border-left: 4px solid #E57C9F; }
.data-card h3 { color: #4A2C40; margin-top: 0; margin-bottom: 15px; font-size: 18px; }
.data-card p { color: #666; margin: 0; line-height: 1.6; }
</style> 
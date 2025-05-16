<template>
  <div>
    <NavBar />
    <div class="container">
      <div class="header">
        <h2 class="header-title"><i class="ri-calendar-event-line"></i>Menstrual Data</h2>
        <p class="header-subtitle">Track your menstrual cycle to understand your physiological condition and health status.</p>
      </div>
      <!-- 经期历史数据展示 -->
      <div class="menstrual-list">
        <h3>Recent Menstrual Records</h3>
        <ul>
          <li v-for="item in menstrualList" :key="item.id">
            Date: {{ formatDate(item.timestamp) }} | Duration: {{ item.duration }} days | Condition: {{ item.condition }}
          </li>
        </ul>
      </div>
      <!-- Menstrual Summary -->
      <div class="cycle-summary">
        <div class="cycle-stat">
          <div class="stat-number">28</div>
          <div class="stat-title">Average Cycle Length (days)</div>
        </div>
        <div class="cycle-stat">
          <div class="stat-number">5</div>
          <div class="stat-title">Average Period Days</div>
        </div>
        <div class="cycle-stat">
          <div class="stat-number">14</div>
          <div class="stat-title">Average Ovulation Day (cycle day)</div>
        </div>
        <div class="cycle-stat">
          <div class="stat-number">5</div>
          <div class="stat-title">Days Until Next Period</div>
        </div>
      </div>
      <!-- Menstrual Chart -->
      <div class="chart-container">
        <canvas ref="menstrualChart"></canvas>
      </div>
      <!-- Calendar View -->
      <div class="calendar-section">
        <h3 class="section-title"><i class="ri-calendar-line"></i>Cycle Calendar</h3>
        <div class="calendar-header">
          <div class="calendar-month">October 2023</div>
          <div class="calendar-controls">
            <button class="calendar-button"><i class="ri-arrow-left-s-line"></i></button>
            <button class="calendar-button"><i class="ri-arrow-right-s-line"></i></button>
          </div>
        </div>
        <div class="calendar-grid">
          <div class="calendar-day-header">Sun</div>
          <div class="calendar-day-header">Mon</div>
          <div class="calendar-day-header">Tue</div>
          <div class="calendar-day-header">Wed</div>
          <div class="calendar-day-header">Thu</div>
          <div class="calendar-day-header">Fri</div>
          <div class="calendar-day-header">Sat</div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day">1</div>
          <div class="calendar-day">2</div>
          <div class="calendar-day">3</div>
          <div class="calendar-day">4</div>
          <div class="calendar-day period">5</div>
          <div class="calendar-day period">6</div>
          <div class="calendar-day period">7</div>
          <div class="calendar-day period">8</div>
          <div class="calendar-day period">9</div>
          <div class="calendar-day">10</div>
          <div class="calendar-day">11</div>
          <div class="calendar-day">12</div>
          <div class="calendar-day">13</div>
          <div class="calendar-day fertile">14</div>
          <div class="calendar-day fertile">15</div>
          <div class="calendar-day fertile">16</div>
          <div class="calendar-day fertile">17</div>
          <div class="calendar-day ovulation">18</div>
          <div class="calendar-day fertile">19</div>
          <div class="calendar-day fertile">20</div>
          <div class="calendar-day today">21</div>
          <div class="calendar-day">22</div>
          <div class="calendar-day">23</div>
          <div class="calendar-day">24</div>
          <div class="calendar-day">25</div>
          <div class="calendar-day">26</div>
          <div class="calendar-day">27</div>
          <div class="calendar-day">28</div>
          <div class="calendar-day">29</div>
          <div class="calendar-day">30</div>
          <div class="calendar-day">31</div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
          <div class="calendar-day empty"></div>
        </div>
      </div>
      <!-- Health Tips -->
      <div class="tips-section">
        <h3 class="section-title"><i class="ri-heart-3-line"></i>Menstrual Health Tips</h3>
        <div class="tips-grid">
          <div class="tip-card">
            <div class="tip-icon"><i class="ri-water-flash-line"></i></div>
            <div class="tip-title">Stay Hydrated</div>
            <div class="tip-content">Maintain adequate water intake during your period to help reduce bloating and water retention.</div>
          </div>
          <div class="tip-card">
            <div class="tip-icon"><i class="ri-rest-time-line"></i></div>
            <div class="tip-title">Get Enough Rest</div>
            <div class="tip-content">Ensure sufficient sleep to help your body recover and alleviate menstrual fatigue.</div>
          </div>
          <div class="tip-card">
            <div class="tip-icon"><i class="ri-leaf-line"></i></div>
            <div class="tip-title">Balanced Diet</div>
            <div class="tip-content">Increase intake of iron-rich foods such as dark leafy vegetables, red meat, and legumes.</div>
          </div>
          <div class="tip-card">
            <div class="tip-icon"><i class="ri-mental-health-line"></i></div>
            <div class="tip-title">Relax Your Mind</div>
            <div class="tip-content">Try meditation or gentle yoga to help alleviate mood swings associated with premenstrual syndrome.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

export default {
  name: 'Menstrual',
  components: { NavBar },
  setup() {
    const menstrualChart = ref(null)
    const menstrualList = ref([])
    let chartInstance = null

    // 日期格式化函数
    function formatDate(dateStr) {
      if (!dateStr) return ''
      const d = new Date(dateStr)
      return d.toLocaleDateString()
    }

    // 获取经期数据并动态生成图表
    onMounted(async () => {
      try {
        const res = await axios.get('http://120.76.249.191:8080/menstrual')
        menstrualList.value = res.data

        // 生成 labels 和 period days
        const labels = res.data.map((item, idx) => `Cycle ${res.data.length - idx}`)
        const periodDays = res.data.map(item => item.duration)

        // 销毁旧图表（如果有）
        if (chartInstance) {
          chartInstance.destroy()
        }
        // 初始化新图表
        const ctx = menstrualChart.value.getContext('2d')
        chartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labels.reverse(), // 最新的在右侧
            datasets: [
              {
                label: 'Period Days',
                data: periodDays.reverse(),
                backgroundColor: '#E57C9F',
                borderColor: '#E57C9F',
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'top', labels: { color: '#4A2C40' } }
            },
            scales: {
              y: {
                beginAtZero: true,
                grid: { color: 'rgba(74, 44, 64, 0.1)' },
                ticks: { color: '#4A2C40' }
              },
              x: {
                grid: { color: 'rgba(74, 44, 64, 0.1)' },
                ticks: { color: '#4A2C40' }
              }
            }
          }
        })
      } catch (e) {
        console.error('Failed to fetch menstrual data:', e)
      }
    })

    return { menstrualChart, menstrualList, formatDate }
  }
}
</script>

<style scoped>
/* 只迁移主要结构样式，细节可后续补充 */
.container { max-width: 1200px; margin: 0 auto; padding: 30px; }
.header { text-align: center; margin-bottom: 30px; }
.header-title { color: #4A2C40; font-size: 32px; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; gap: 10px; }
.header-title i { color: #E57C9F; }
.header-subtitle { color: #666; font-size: 16px; max-width: 700px; margin: 0 auto; }
.menstrual-list { margin: 30px 0; }
.menstrual-list ul { list-style: none; padding: 0; }
.menstrual-list li { background: #fff5f7; margin-bottom: 8px; padding: 10px 16px; border-radius: 8px; color: #4A2C40; }
.cycle-summary { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 15px; margin-bottom: 25px; }
.cycle-stat { background-color: rgba(229, 124, 159, 0.05); border-radius: 15px; padding: 15px; text-align: center; transition: all 0.3s ease; }
.cycle-stat:hover { background-color: rgba(229, 124, 159, 0.1); transform: translateY(-3px); }
.stat-number { font-size: 28px; font-weight: bold; color: #E57C9F; margin-bottom: 5px; }
.stat-title { font-size: 14px; color: #4A2C40; }
.chart-container { background-color: white; border-radius: 20px; padding: 30px; margin: 20px auto; box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12); }
.calendar-section { margin-top: 30px; background-color: white; border-radius: 20px; padding: 30px; box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12); }
.section-title { color: #4A2C40; font-size: 22px; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
.section-title i { color: #E57C9F; }
.calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.calendar-month { font-size: 18px; font-weight: bold; color: #4A2C40; }
.calendar-controls { display: flex; gap: 10px; }
.calendar-button { background-color: rgba(229, 124, 159, 0.1); color: #4A2C40; border: none; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.3s ease; }
.calendar-button:hover { background-color: #E57C9F; color: white; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
.calendar-day-header { text-align: center; font-weight: bold; padding: 5px; color: #4A2C40; }
.calendar-day { aspect-ratio: 1; background-color: white; border-radius: 10px; display: flex; align-items: center; justify-content: center; border-radius: 10px; font-size: 14px; background-color: rgba(229, 124, 159, 0.05); color: #4A2C40; position: relative; transition: all 0.3s ease; }
.calendar-day:hover { background-color: rgba(229, 124, 159, 0.1); transform: scale(1.05); }
.calendar-day.period { background-color: rgba(229, 124, 159, 0.3); color: #4A2C40; font-weight: bold; }
.calendar-day.fertile { background-color: rgba(126, 184, 162, 0.2); color: #4A2C40; }
.calendar-day.ovulation { background-color: rgba(126, 184, 162, 0.4); color: #4A2C40; font-weight: bold; }
.calendar-day.today { border: 2px solid #E57C9F; }
.calendar-day.empty { background-color: transparent; }
.tips-section { margin-top: 30px; background-color: white; border-radius: 20px; padding: 30px; box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12); }
.tips-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
.tip-card { background-color: rgba(229, 124, 159, 0.05); border-radius: 15px; padding: 15px; transition: all 0.3s ease; }
.tip-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(229, 124, 159, 0.1); }
.tip-icon { font-size: 24px; color: #E57C9F; margin-bottom: 10px; }
.tip-title { font-size: 16px; font-weight: bold; color: #4A2C40; margin-bottom: 10px; }
.tip-content { font-size: 14px; color: #666; line-height: 1.5; }
</style> 
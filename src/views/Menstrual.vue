<template>
  <div>
    <button class="back-btn" @click="goBack">返回首页</button>
    <div class="container">
      <div class="header">
        <h2 class="header-title"><i class="ri-calendar-event-line"></i>Menstrual Data</h2>
        <p class="header-subtitle">Track your menstrual cycle to understand your physiological condition and health status.</p>
      </div>

      <!-- Menstrual Chart -->
      <div class="chart-container">
        <canvas ref="menstrualChart"></canvas>
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

      <!-- 经期历史数据展示 - 列表 -->
      <div class="menstrual-list">
        <h3>Recent Menstrual Records (List)</h3>
        <ul>
          <li v-for="item in menstrualList" :key="item.id">
            Date: {{ formatDate(item.timestamp) }} | Duration: {{ item.duration }} days | Condition: {{ item.condition }}
          </li>
        </ul>
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
import { useRouter } from 'vue-router'

export default {
  name: 'Menstrual',
  components: { NavBar },
  setup() {
    const menstrualChart = ref(null)
    const menstrualList = ref([])
    let chartInstance = null
    const router = useRouter()

    // 日期格式化函数
    function formatDate(dateStr) {
      if (!dateStr) return ''
      const d = new Date(dateStr)
      return d.toLocaleDateString()
    }

    // 获取经期数据并动态生成图表
    onMounted(async () => {
      try {
        const res = await axios.get('http://120.76.249.191:8000/menstrual')
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

    // 返回首页方法
    const goBack = () => {
      router.push('/metrics')
    }

    return {
      menstrualChart,
      menstrualList,
      formatDate,
      goBack,
    }
  },
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
.menstrual-list h3 { color: #4A2C40; margin-bottom: 15px; }
.menstrual-list ul { list-style: none; padding: 0; }
.menstrual-list li { background: #fff5f7; margin-bottom: 8px; padding: 10px 16px; border-radius: 8px; color: #4A2C40; }

.cycle-summary { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 15px; margin-bottom: 25px; }
.cycle-stat { background-color: rgba(229, 124, 159, 0.05); border-radius: 15px; padding: 15px; text-align: center; transition: all 0.3s ease; }
.cycle-stat:hover { background-color: rgba(229, 124, 159, 0.1); transform: translateY(-3px); }
.stat-number { font-size: 28px; font-weight: bold; color: #E57C9F; margin-bottom: 5px; }
.stat-title { font-size: 14px; color: #4A2C40; }

.chart-container { background-color: white; border-radius: 20px; padding: 30px; margin: 20px auto; box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12); text-align: center; /* 确保内容居中 */ }
canvas { display: inline-block; /* 让 canvas 元素可以被 text-align 居中 */ max-width: 100%; height: auto; }

.tips-section { margin-top: 30px; background-color: white; border-radius: 20px; padding: 30px; box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12); }
.tips-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
.tip-card { background-color: rgba(229, 124, 159, 0.05); border-radius: 15px; padding: 15px; transition: all 0.3s ease; }
.tip-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(229, 124, 159, 0.1); }
.tip-icon { font-size: 24px; color: #E57C9F; margin-bottom: 10px; }
.tip-title { font-size: 16px; font-weight: bold; color: #4A2C40; margin-bottom: 10px; }
.tip-content { font-size: 14px; color: #666; line-height: 1.5; }

.back-btn {
  margin: 20px 0 0 20px;
  padding: 6px 18px;
  background: #E57C9F;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
}
.back-btn:hover {
  background: #d66a8d;
}
</style> 
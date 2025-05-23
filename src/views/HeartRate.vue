<template>
  <div>
    <button class="back-btn" @click="goBack">Back to Home</button>
  <div class="heart-rate-page femel-bg">
    <FemalCard title="Heart Rate Monitoring">
      <div class="chart-section">
        <div class="status-tip">
          <i class="ri-heart-pulse-fill status-icon" :class="statusColor"></i>
          <span class="status-text" :class="statusColor">{{ healthStatusTip }}</span>
        </div>
        <div ref="chartRef" style="width: 100%; height: 340px;"></div>
      </div>
    </FemalCard>
    <div class="stats-row">
      <FemalCard variant="soft" class="stat-card">
        <div class="stat-icon stat-icon-main"><i class="ri-heart-pulse-line"></i></div>
        <div class="stat-label">Average Heart Rate</div>
        <div class="stat-value">{{ stats.average }} <span>BPM</span></div>
      </FemalCard>
      <FemalCard variant="soft" class="stat-card">
        <div class="stat-icon stat-icon-low"><i class="ri-arrow-down-line"></i></div>
        <div class="stat-label">Minimum Heart Rate</div>
        <div class="stat-value">{{ stats.min }} <span>BPM</span></div>
      </FemalCard>
      <FemalCard variant="soft" class="stat-card">
        <div class="stat-icon stat-icon-high"><i class="ri-arrow-up-line"></i></div>
        <div class="stat-label">Maximum Heart Rate</div>
        <div class="stat-value">{{ stats.max }} <span>BPM</span></div>
      </FemalCard>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { healthApi } from '@/api';
import FemalCard from '@/components/FemalUI/FemalCard.vue';
import '@/components/FemalUI/styles.css';

export default {
  name: 'HeartRate',
  components: { FemalCard },
  setup() {
    const chartRef = ref(null);
    let chart = null;
    let timer = null;
    const stats = ref({ average: 0, min: 0, max: 0 });
    const latest = ref({ value: 0, status: 'Normal' });

    // Health status determination
    const getHealthStatus = (hr) => {
      if (hr < 60) return 'Low';
      if (hr > 100) return 'High';
      return 'Normal';
    };
    const statusColor = computed(() => {
      if (latest.value.status === 'Normal') return 'status-normal';
      if (latest.value.status === 'High') return 'status-high';
      if (latest.value.status === 'Low') return 'status-low';
      return '';
    });
    const healthStatusTip = computed(() => {
      if (latest.value.status === 'Normal') return 'Heart rate is normal, keep it up!';
      if (latest.value.status === 'High') return 'Heart rate is high, take some rest and relax.';
      if (latest.value.status === 'Low') return 'Heart rate is low, pay attention to nutrition and exercise.';
      return '';
    });

    const initChart = () => {
      if (chartRef.value) {
        chart = echarts.init(chartRef.value);
        const option = {
          tooltip: {
            trigger: 'axis',
            formatter: function(params) {
              const data = params[0];
              return `${data.name}<br/>Heart Rate: ${data.value} BPM`;
            }
          },
          xAxis: {
            type: 'time',
            axisLabel: { formatter: '{HH}:{mm}' }
          },
          yAxis: {
            type: 'value',
            name: 'Heart Rate (BPM)',
            min: 40,
            max: 120
          },
          series: [{
            name: 'Heart Rate',
            type: 'line',
            smooth: true,
            data: [],
            itemStyle: { color: '#E57C9F' },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(229, 124, 159, 0.3)' },
                { offset: 1, color: 'rgba(229, 124, 159, 0.1)' }
              ])
            }
          }]
        };
        chart.setOption(option);
      }
    };

    const updateData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await healthApi.getHeartRate();
        const data = response.data;
        const chartData = data.map(item => [item.timestamp, item.heart_rate]);
        if (data && data.length > 0) {
          const last = data[data.length - 1];
          latest.value.value = last.heart_rate;
          latest.value.status = getHealthStatus(last.heart_rate);

          // 统计心率
          const heartRates = data.map(item => item.heart_rate);
          const sum = heartRates.reduce((a, b) => a + b, 0);
          const avg = (sum / heartRates.length).toFixed(2);
          const min = Math.min(...heartRates).toFixed(2);
          const max = Math.max(...heartRates).toFixed(2);
          stats.value = {
            average: avg,
            min: min,
            max: max
          };
        } else {
          stats.value = { average: 0, min: 0, max: 0 };
        }
        chart.setOption({ series: [{ data: chartData }] });
      } catch (error) {
        console.error('Failed to get heart rate data:', error);
      }
    };

    const goBack = () => {
      window.location.hash = '';
      window.location.pathname = '/metrics';
    };

    onMounted(() => {
      initChart();
      updateData();
      timer = setInterval(updateData, 30000);
    });
    onUnmounted(() => {
      if (chart) chart.dispose();
      if (timer) clearInterval(timer);
    });
    return { chartRef, stats, latest, healthStatusTip, statusColor, goBack };
  }
};
</script>

<style scoped>
.heart-rate-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 0 24px 0;
}
.chart-section {
  padding-bottom: 0;
}
.status-tip {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  margin-bottom: 10px;
  font-weight: 500;
  letter-spacing: 1px;
}
.status-icon {
  font-size: 1.5rem;
  margin-right: 8px;
}
.status-normal {
  color: #7EB8A2;
}
.status-high {
  color: #E86B6B;
}
.status-low {
  color: #1890ff;
}
.status-text {
  font-weight: 600;
}
.stats-row {
  display: flex;
  gap: 18px;
  margin-top: 8px;
}
.stat-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 0;
  min-height: 140px;
  box-shadow: none;
  background: linear-gradient(135deg, #fff 70%, #FFF5F7 100%);
}
.stat-icon {
  font-size: 2.2rem;
  margin-bottom: 8px;
}
.stat-icon-main {
  color: #E57C9F;
}
.stat-icon-low {
  color: #1890ff;
}
.stat-icon-high {
  color: #E86B6B;
}
.stat-label {
  color: #4A2C40;
  font-size: 1rem;
  margin-bottom: 4px;
}
.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #E57C9F;
  letter-spacing: 1px;
}
.stat-value span {
  font-size: 1rem;
  color: #AE5F87;
  font-weight: 400;
}
@media (max-width: 700px) {
  .stats-row {
    flex-direction: column;
    gap: 10px;
  }
  .stat-card {
    min-height: 100px;
  }
}
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
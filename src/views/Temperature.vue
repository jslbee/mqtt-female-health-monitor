<template>
  <div>
    <button class="back-btn" @click="goBack">Back to Home</button>
  <div class="temperature-page femel-bg">
    <FemalCard title="Temperature Monitoring">
      <div class="chart-section">
        <div class="status-tip">
          <i class="ri-thermometer-line status-icon" :class="statusColor"></i>
          <span class="status-text" :class="statusColor">{{ healthStatusTip }}</span>
        </div>
        <div ref="chartRef" style="width: 100%; height: 340px;"></div>
      </div>
    </FemalCard>
    <div class="stats-row">
      <FemalCard variant="soft" class="stat-card">
        <div class="stat-icon stat-icon-main"><i class="ri-thermometer-line"></i></div>
          <div class="stat-label">Average Temperature</div>
          <div class="stat-value">{{ stats.average }} <span>°C</span></div>
        </FemalCard>
        <FemalCard variant="soft" class="stat-card">
          <div class="stat-icon stat-icon-low"><i class="ri-arrow-down-line"></i></div>
          <div class="stat-label">Minimum Temperature</div>
          <div class="stat-value">{{ stats.min }} <span>°C</span></div>
      </FemalCard>
      <FemalCard variant="soft" class="stat-card">
          <div class="stat-icon stat-icon-high"><i class="ri-arrow-up-line"></i></div>
          <div class="stat-label">Maximum Temperature</div>
          <div class="stat-value">{{ stats.max }} <span>°C</span></div>
      </FemalCard>
    </div>
    <FemalCard v-if="latestWarning" variant="soft">
      <div class="warning-container">
        <div class="warning-icon">⚠️</div>
        <div class="warning-message">{{ latestWarning }}</div>
      </div>
    </FemalCard>
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
  name: 'Temperature',
  components: { FemalCard },
  setup() {
    const chartRef = ref(null);
    let chart = null;
    let timer = null;
    const latestWarning = ref('');
    const latest = ref({ value: 0, status: 'Normal' });
    const stats = ref({ average: 0, min: 0, max: 0 });

    // Health status determination
    const getHealthStatus = (temp) => {
      if (temp < 35.5) return 'Hypothermia';
      if (temp >= 38.0) return 'High Fever';
      if (temp >= 37.5) return 'Low Fever';
      if (temp < 36.0) return 'Low';
      if (temp > 37.2) return 'High';
      return 'Normal';
    };
    const statusColor = computed(() => {
      if (latest.value.status === 'Normal') return 'status-normal';
      if (latest.value.status === 'High Fever' || latest.value.status === 'Low Fever' || latest.value.status === 'High') return 'status-high';
      if (latest.value.status === 'Hypothermia' || latest.value.status === 'Low') return 'status-low';
      return '';
    });
    const healthStatusTip = computed(() => {
      if (latest.value.status === 'Normal') return 'Temperature is normal, keep it up!';
      if (latest.value.status === 'High Fever') return 'High fever warning, please seek medical attention.';
      if (latest.value.status === 'Low Fever') return 'Low fever, please rest and drink more water.';
      if (latest.value.status === 'Hypothermia') return 'Temperature is too low, please keep warm.';
      if (latest.value.status === 'High') return 'Temperature is slightly high, please monitor.';
      if (latest.value.status === 'Low') return 'Temperature is slightly low, please keep warm.';
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
              return `${data.name}<br/>Temperature: ${data.value}°C`;
            }
          },
          xAxis: {
            type: 'time',
            axisLabel: { formatter: '{HH}:{mm}' }
          },
          yAxis: {
            type: 'value',
            name: 'Temperature (°C)',
            min: 35,
            max: 42,
            splitLine: { lineStyle: { type: 'dashed' } }
          },
          series: [{
            name: 'Temperature',
            type: 'line',
            smooth: true,
            data: [],
            itemStyle: { color: '#7EB8A2' },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(126, 184, 162, 0.3)' },
                { offset: 1, color: 'rgba(126, 184, 162, 0.1)' }
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
        const response = await healthApi.getTemperature();
        const data = response.data;
        const chartData = data.map(item => [item.timestamp, item.temperature]);
        if (data && data.length > 0) {
          const last = data[data.length - 1];
          latest.value.value = last.temperature;
          latest.value.status = getHealthStatus(last.temperature);
          if (last.warning) latestWarning.value = last.warning;

          // 统计体温
          const temps = data.map(item => item.temperature);
          const sum = temps.reduce((a, b) => a + b, 0);
          const avg = (sum / temps.length).toFixed(2);
          const min = Math.min(...temps).toFixed(2);
          const max = Math.max(...temps).toFixed(2);
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
        console.error('Failed to get temperature data:', error);
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
    return { chartRef, latestWarning, latest, healthStatusTip, statusColor, goBack, stats };
  }
};
</script>

<style scoped>
.temperature-page {
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
  background: linear-gradient(135deg, #fff 70%, #F5FAF7 100%);
}
.stat-icon {
  font-size: 2.2rem;
  margin-bottom: 8px;
}
.stat-icon-main {
  color: #7EB8A2;
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
.warning-container {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
}
.warning-icon {
  font-size: 20px;
}
.warning-message {
  color: #E57C9F;
  font-size: 1rem;
  font-weight: 500;
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
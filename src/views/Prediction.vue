<template>
  <div>
    <NavBar />
    <div class="prediction-container">
      <h2>月经周期预测</h2>
      
      <div class="input-section">
        <el-form :model="predictionForm" label-width="120px">
          <el-form-item label="上次月经日期">
            <el-date-picker
              v-model="predictionForm.lastPeriodDate"
              type="date"
              placeholder="选择日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="getPrediction" :loading="loading">
              预测下一次月经
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="predictionResult" class="result-section">
        <el-card class="prediction-card">
          <template #header>
            <div class="card-header">
              <span>预测结果</span>
            </div>
          </template>
          <div class="prediction-content">
            <p>预测日期: {{ predictionDate }}</p>
            <p>平均周期: {{ averageCycle }} 天</p>
          </div>
        </el-card>
      </div>

      <div v-if="error" class="error-message">
        <el-alert
          :title="error"
          type="error"
          show-icon>
        </el-alert>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { menstrualService } from '@/api/menstrualService'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'Prediction',
  components: {
    NavBar
  },
  setup() {
    const predictionForm = reactive({
      lastPeriodDate: ''
    })
    const predictionResult = ref(null)
    const loading = ref(false)
    const error = ref('')
    const predictionDate = ref('')
    const averageCycle = ref('')

    const getPrediction = async () => {
      if (!predictionForm.lastPeriodDate) {
        error.value = '请选择上次月经日期'
        return
      }
      loading.value = true
      error.value = ''
      try {
        const result = await menstrualService.predictNextPeriod(
          predictionForm.lastPeriodDate
        )
        let resultStr = result
        if (typeof result === 'object' && result.result) {
          resultStr = result.result
        }
        // 用正则提取日期和天数
        const dateMatch = resultStr.match(/(\d{4}-\d{2}-\d{2})/)
        const daysMatch = resultStr.match(/average cycle of approximately (\d+) days/)
        predictionDate.value = dateMatch ? dateMatch[1] : ''
        averageCycle.value = daysMatch ? daysMatch[1] : ''
        predictionResult.value = resultStr
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    return {
      predictionForm,
      predictionResult,
      loading,
      error,
      predictionDate,
      averageCycle,
      getPrediction
    }
  }
}
</script>

<style scoped>
.prediction-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  min-height: calc(100vh - 64px);
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

h2 {
  color: #4A2C40;
  font-size: clamp(32px, 5vw, 40px);
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 700;
  letter-spacing: 1px;
  background: linear-gradient(to right, #4A2C40, #E57C9F);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
  padding-bottom: 5px;
}

.input-section {
  background: #fff;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 24px rgba(156, 91, 128, 0.12);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.input-section:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(156, 91, 128, 0.16);
}

:deep(.el-form-item__label) {
  color: #E57C9F;
  font-weight: 600;
  font-size: 1.1rem;
}

:deep(.el-input__inner) {
  border-radius: 8px;
  border: 1px solid rgba(156, 91, 128, 0.2);
  transition: all 0.3s ease;
  font-size: 1.1rem;
}

:deep(.el-input__inner:focus) {
  border-color: #E57C9F;
  box-shadow: 0 0 0 2px rgba(229, 124, 159, 0.1);
}

:deep(.el-button--primary) {
  background: #E57C9F;
  border-color: #E57C9F;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  font-weight: 600;
}

:deep(.el-button--primary:hover) {
  background: #C45D7D;
  border-color: #C45D7D;
  transform: translateY(-2px);
}

.result-section {
  margin-top: 2rem;
}

:deep(.el-card) {
  border-radius: 20px;
  border: none;
  box-shadow: 0 8px 24px rgba(156, 91, 128, 0.12);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #fff;
}

:deep(.el-card__header) {
  background: #E57C9F !important;
  color: #fff !important;
  border-radius: 20px 20px 0 0;
  padding: 1.2rem 1.5rem;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.2rem;
  font-weight: 600;
}

.prediction-content {
  padding: 2rem 1.5rem;
  font-size: 1.25rem;
  line-height: 2;
  color: #4A2C40;
  text-align: center;
}

.prediction-content p {
  margin-bottom: 1.2rem;
  font-size: 1.2rem;
}

.prediction-content p:first-child {
  color: #E57C9F;
  font-size: 1.4rem;
  font-weight: bold;
}

.prediction-content p:last-child {
  margin-bottom: 0;
  color: #4A2C40;
  font-weight: 600;
  font-size: 1.2rem;
}

.error-message {
  margin-top: 1.5rem;
}

:deep(.el-alert) {
  border-radius: 8px;
  padding: 1rem 1.5rem;
}

:deep(.el-alert--error) {
  background-color: #fff2f0;
  border: 1px solid #ffccc7;
}

:deep(.el-alert__title) {
  color: #ff4d4f;
  font-size: 1rem;
}

:deep(.el-date-editor.el-input) {
  width: 100%;
}

:deep(.el-date-editor .el-input__inner) {
  padding-left: 40px;
}

:deep(.el-date-editor .el-input__prefix) {
  color: #E57C9F;
}
</style> 
<template>
  <div>
    <NavBar />
    <div class="prediction-container">
      <h2>Menstrual Cycle Prediction</h2>
      
      <div class="input-section">
        <el-form :model="predictionForm" label-width="120px">
          <el-form-item label="Last Period Date">
            <el-date-picker
              v-model="predictionForm.lastPeriodDate"
              type="date"
              placeholder="Select date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="getPrediction" :loading="loading">
              Predict Next Period
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="predictionResult" class="result-section">
        <el-card class="prediction-card">
          <template #header>
            <div class="card-header">
              <span>Prediction Result</span>
            </div>
          </template>
          <div class="prediction-content">
            <p>Predicted Date: {{ predictionDate }}</p>
            <p>Average Cycle: {{ averageCycle }} days</p>
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

      <!-- Placeholder image section for aesthetics -->
      <div class="aesthetic-image-container">
        <img src="@/assets/images/menstrual cycle illustration.jpg" alt="Decorative image related to cycle tracking" loading="lazy" class="aesthetic-image">
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
        error.value = 'Please select the last period date'
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
  font-family: 'Playfair Display', serif;
  background: linear-gradient(45deg, #E57C9F 30%, #B19CD9 70%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
  padding-bottom: 5px;
  position: relative;
  animation: gradientFlow 8s ease infinite;
  background-size: 200% 200%;
  text-shadow: 0 2px 4px rgba(177, 156, 217, 0.2);
}

@keyframes gradientFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.input-section {
  background: #fff;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 24px rgba(177, 156, 217, 0.12);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(177, 156, 217, 0.1);
}

.input-section:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(177, 156, 217, 0.16);
}

:deep(.el-form-item__label) {
  color: #B19CD9;
  font-weight: 600;
  font-size: 1.1rem;
  font-family: 'Playfair Display', serif;
}

:deep(.el-input__inner) {
  border-radius: 12px;
  border: 1px solid rgba(177, 156, 217, 0.2);
  transition: all 0.3s ease;
  font-size: 1.1rem;
  background-color: #F8F9FF;
}

:deep(.el-input__inner:focus) {
  border-color: #B19CD9;
  box-shadow: 0 0 0 2px rgba(177, 156, 217, 0.1);
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #E57C9F 0%, #B19CD9 100%);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #B19CD9 0%, #E57C9F 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(177, 156, 217, 0.2);
}

.result-section {
  margin-top: 2rem;
}

:deep(.el-card) {
  border-radius: 20px;
  border: 1px solid rgba(177, 156, 217, 0.1);
  box-shadow: 0 8px 24px rgba(177, 156, 217, 0.12);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #fff;
}

:deep(.el-card__header) {
  background: linear-gradient(135deg, #B19CD9 0%, #E57C9F 100%) !important;
  color: #fff !important;
  border-radius: 20px 20px 0 0;
  padding: 1.2rem 1.5rem;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 1px;
  font-family: 'Playfair Display', serif;
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
  font-family: 'Playfair Display', serif;
}

.prediction-content p {
  margin-bottom: 1.2rem;
  font-size: 1.2rem;
}

.prediction-content p:first-child {
  color: #B19CD9;
  font-size: 1.4rem;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(177, 156, 217, 0.2);
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
  border-radius: 12px;
  padding: 1rem 1.5rem;
  border: 1px solid rgba(177, 156, 217, 0.1);
}

:deep(.el-alert--error) {
  background-color: #fff2f0;
  border: 1px solid #ffccc7;
}

:deep(.el-alert__title) {
  color: #ff4d4f;
  font-size: 1rem;
  font-family: 'Playfair Display', serif;
}

:deep(.el-date-editor.el-input) {
  width: 100%;
}

:deep(.el-date-editor .el-input__inner) {
  padding-left: 40px;
  background-color: #F8F9FF;
}

:deep(.el-date-editor .el-input__prefix) {
  color: #B19CD9;
}

:deep(.el-date-picker) {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(177, 156, 217, 0.15);
}

:deep(.el-date-picker__header) {
  color: #B19CD9;
  font-family: 'Playfair Display', serif;
}

:deep(.el-date-table th) {
  color: #4A2C40;
  font-weight: 600;
}

:deep(.el-date-table td.available:hover) {
  color: #B19CD9;
}

:deep(.el-date-table td.current:not(.disabled) span) {
  background-color: #B19CD9;
  color: #fff;
}

/* Aesthetic Image Styles */
.aesthetic-image-container {
  margin-top: 40px;
  text-align: center; /* Center the image */
}

.aesthetic-image {
  max-width: 100%; /* Make it full width within its container */
  height: auto;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(177, 156, 217, 0.12);
  opacity: 0.7; /* Reduce opacity */
}
</style> 
<template>
  <div class="prediction-container">
    <h2>月经周期预测</h2>
    
    <div class="input-section">
      <el-form :model="predictionForm" label-width="120px">
        <el-form-item label="用户ID">
          <el-input v-model="predictionForm.clientId" placeholder="请输入用户ID (例如: nfp8122)"></el-input>
        </el-form-item>
        
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
          <p>{{ predictionResult.message }}</p>
          <p>平均周期: {{ predictionResult.average_cycle }} 天</p>
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
</template>

<script>
import { ref, reactive } from 'vue'
import { menstrualService } from '@/api/menstrualService'

export default {
  name: 'Prediction',
  setup() {
    const predictionForm = reactive({
      clientId: '',
      lastPeriodDate: ''
    })
    const predictionResult = ref(null)
    const loading = ref(false)
    const error = ref('')

    const getPrediction = async () => {
      if (!predictionForm.clientId || !predictionForm.lastPeriodDate) {
        error.value = '请填写所有必填字段'
        return
      }

      loading.value = true
      error.value = ''
      
      try {
        const result = await menstrualService.predictNextPeriod(
          predictionForm.clientId,
          predictionForm.lastPeriodDate
        )
        predictionResult.value = result
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
  color: #9C5B80;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
}

.input-section {
  background: #ffffff;
  border-radius: 16px;
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
  color: #9C5B80;
  font-weight: 500;
}

:deep(.el-input__inner) {
  border-radius: 8px;
  border: 1px solid rgba(156, 91, 128, 0.2);
  transition: all 0.3s ease;
}

:deep(.el-input__inner:focus) {
  border-color: #9C5B80;
  box-shadow: 0 0 0 2px rgba(156, 91, 128, 0.1);
}

:deep(.el-button--primary) {
  background: #9C5B80;
  border-color: #9C5B80;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  background: #E57C9F;
  border-color: #E57C9F;
  transform: translateY(-2px);
}

:deep(.el-button--primary.is-loading) {
  background: #9C5B80;
  border-color: #9C5B80;
}

.result-section {
  margin-top: 2rem;
}

:deep(.el-card) {
  border-radius: 16px;
  border: none;
  box-shadow: 0 8px 24px rgba(156, 91, 128, 0.12);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

:deep(.el-card:hover) {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(156, 91, 128, 0.16);
}

:deep(.el-card__header) {
  background: #9C5B80;
  color: #ffffff;
  border-radius: 16px 16px 0 0;
  padding: 1rem 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.2rem;
  font-weight: 600;
}

.prediction-content {
  padding: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #666;
}

.prediction-content p {
  margin-bottom: 1rem;
}

.prediction-content p:last-child {
  margin-bottom: 0;
  color: #9C5B80;
  font-weight: 500;
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
  color: #9C5B80;
}
</style> 
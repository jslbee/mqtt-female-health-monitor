<template>
  <div class="female-example" :style="{ backgroundColor: FemaleColors.background, padding: '40px' }">
    <h1 :style="{ color: FemaleColors.text, marginBottom: '40px', textAlign: 'center' }">女性健康系统UI组件</h1>
    
    <!-- 按钮展示 -->
    <female-card title="按钮设计">
      <div style="display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 24px;">
        <female-button type="primary">主要按钮</female-button>
        <female-button type="secondary">次要按钮</female-button>
        <female-button type="outline">轮廓按钮</female-button>
        <female-button type="text">文本按钮</female-button>
        <female-button type="primary" :disabled="true">禁用按钮</female-button>
      </div>
      
      <div style="display: flex; flex-wrap: wrap; gap: 16px;">
        <female-button type="primary" size="small">小按钮</female-button>
        <female-button type="primary" size="medium">中按钮</female-button>
        <female-button type="primary" size="large">大按钮</female-button>
      </div>
    </female-card>
    
    <!-- 输入框展示 -->
    <female-card title="输入框设计">
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <female-input 
          v-model="inputValue" 
          placeholder="请输入姓名" 
        />
        
        <female-input 
          placeholder="请输入邮箱" 
          type="email"
          icon="✉️"
        />
        
        <female-input 
          placeholder="请输入密码" 
          type="password"
          error="密码长度至少为8位"
        />
        
        <female-input 
          placeholder="禁用状态" 
          :disabled="true"
        />
      </div>
    </female-card>
    
    <!-- 健康记录卡片示例 -->
    <female-card title="健康记录统计" variant="soft">
      <div style="padding: 16px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 24px;">
          <div>
            <h4 :style="{ color: FemaleColors.text, marginBottom: '8px' }">本月健康评分</h4>
            <div style="display: flex; align-items: center;">
              <span style="font-size: 32px; font-weight: bold; color: #E57C9F;">86</span>
              <span style="margin-left: 8px; color: #7EB8A2;">↑4%</span>
            </div>
          </div>
          
          <div>
            <h4 :style="{ color: FemaleColors.text, marginBottom: '8px' }">完成度</h4>
            <div style="font-size: 32px; font-weight: bold; color: #AE5F87;">75%</div>
          </div>
          
          <div>
            <h4 :style="{ color: FemaleColors.text, marginBottom: '8px' }">目标达成</h4>
            <div style="font-size: 32px; font-weight: bold; color: #7EB8A2;">12/15</div>
          </div>
        </div>
        
        <div style="margin-top: 24px; display: flex; justify-content: center;">
          <female-button type="primary" @click="viewDetails">查看详情</female-button>
        </div>
      </div>
    </female-card>
  </div>
</template>

<script>
import { FemaleButton, FemaleInput, FemaleCard, FemaleColors } from '../components/FemelUI';

export default {
  name: 'FemaleExample',
  components: {
    FemaleButton,
    FemaleInput,
    FemaleCard
  },
  data() {
    return {
      inputValue: '',
      FemaleColors
    };
  },
  methods: {
    viewDetails() {
      alert('查看健康详情');
    }
  }
};
</script>

<style>
/* 可以添加页面特定的样式 */
.female-example {
  font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
}
</style> 
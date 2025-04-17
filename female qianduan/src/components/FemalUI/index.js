import FemaleButton from './FemaleButton.vue';
import FemaleInput from './FemaleInput.vue';
import FemaleCard from './FemaleCard.vue';

// 颜色主题
export const FemaleColors = {
  primary: '#E57C9F', // 粉红色调 - 主色
  secondary: '#F4AFBB', // 浅粉色 - 次要色
  accent: '#AE5F87', // 深粉紫色 - 强调色
  background: '#FFF5F7', // 浅粉背景
  text: '#4A2C40', // 深紫文字
  success: '#7EB8A2', // 柔和绿色
  warning: '#F9C096', // 柔和橙色
  error: '#E86B6B', // 柔和红色
  neutral: '#F0E4EB', // 中性色
  white: '#FFFFFF', // 白色
  shadow: 'rgba(156, 91, 128, 0.12)', // 阴影颜色
};

// 创建插件以便全局注册
const FemaleUI = {
  install(app) {
    app.component('FemaleButton', FemaleButton);
    app.component('FemaleInput', FemaleInput);
    app.component('FemaleCard', FemaleCard);
  }
};

// 导出单个组件
export {
  FemaleButton,
  FemaleInput,
  FemaleCard
};

// 导出插件
export default FemaleUI; 
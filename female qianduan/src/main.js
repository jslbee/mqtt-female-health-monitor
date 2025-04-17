import { createApp } from 'vue';
import App from './App.vue';
import FemelUI from './components/FemelUI';

// 创建Vue应用
const app = createApp(App);

// 全局注册Femel UI组件
app.use(FemelUI);

// 挂载应用
app.mount('#app'); 
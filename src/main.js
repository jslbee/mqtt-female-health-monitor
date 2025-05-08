import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/styles/main.css';

// 创建Vue应用
const app = createApp(App);

// 挂载应用
app.use(router);

app.mount('#app'); 
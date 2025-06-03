import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './assets/styles/main.css';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 创建Vue应用
const app = createApp(App);

// 挂载应用
app.use(router);
app.use(ElementPlus)

app.mount('#app'); 
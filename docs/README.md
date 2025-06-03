# Artemis - 女性健康管理系统

## 项目简介
Artemis 是一个基于 Vue 3 开发的女性健康管理系统，提供健康指标监测、预测分析、消息中心等功能。系统采用前后端分离架构，使用现代化的技术栈构建。

## 功能特点
- 健康指标监测（心率、体温、经期）
- 智能预测分析
- 实时数据展示
- 响应式设计，支持移动端和桌面端
- 用户认证与授权

## 技术栈
- Vue 3
- Vue Router
- Axios
- Chart.js
- Vite
- Remix Icon

## 项目结构
```
artemis/
├── src/
│   ├── api/              # API 相关配置和服务
│   │   ├── config.js     # Axios 配置
│   │   └── services.js   # API 服务
│   ├── views/            # 页面组件
│   │   └── Prediction.vue
│   ├── App.vue           # 根组件
│   └── main.js           # 应用入口
├── index.html            # HTML 入口
├── package.json          # 项目配置
├── vite.config.js        # Vite 配置
└── README.md            # 项目说明
```

## 开发环境设置
1. 安装依赖：
```bash
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

3. 构建生产版本：
```bash
npm run build
```

4. 预览生产版本：
```bash
npm run preview
```

## 环境要求
- Node.js >= 18.0.0
- npm >= 8.0.0

## 注意事项
- 开发时请确保后端 API 服务已启动
- 默认开发服务器端口为 3000
- 生产环境部署前请确保已正确配置环境变量

## 联系方式
如有问题，请联系系统管理员。

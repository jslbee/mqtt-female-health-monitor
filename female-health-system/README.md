# Femel UI - 女性健康系统UI组件库

这是一套专为女性健康系统设计的Vue UI组件库，以柔和的色调、简约的设计为特点。

## 主要特点

- 柔和粉色系为主色调，打造温暖亲切的界面体验
- 圆角设计贯穿各组件，提供友好的视觉感受
- 简约且功能完备的组件设计
- 完全基于Vue 3开发，支持按需引入

## 包含组件

- 按钮 (FemelButton)
- 输入框 (FemelInput)
- 卡片 (FemelCard)
- 更多组件持续开发中...

## 安装与使用

### 安装

```bash
# 假设通过npm包安装
npm install femel-ui
```

### 全局引入

```js
import { createApp } from 'vue';
import App from './App.vue';
import FemelUI from 'femel-ui';

const app = createApp(App);
app.use(FemelUI);
app.mount('#app');
```

### 按需引入

```js
import { FemelButton, FemelInput } from 'femel-ui';

export default {
  components: {
    FemelButton,
    FemelInput
  }
}
```

## 组件示例

### 按钮

```vue
<template>
  <femel-button type="primary">主要按钮</femel-button>
  <femel-button type="secondary">次要按钮</femel-button>
  <femel-button type="outline">轮廓按钮</femel-button>
  <femel-button type="text">文本按钮</femel-button>
  <femel-button type="primary" :disabled="true">禁用按钮</femel-button>
</template>
```

### 输入框

```vue
<template>
  <femel-input v-model="inputValue" placeholder="请输入内容" />
  <femel-input 
    placeholder="带图标的输入框" 
    icon="✉️" 
  />
  <femel-input 
    placeholder="错误状态" 
    error="输入内容有误" 
  />
</template>

<script>
export default {
  data() {
    return {
      inputValue: ''
    }
  }
}
</script>
```

### 卡片

```vue
<template>
  <femel-card title="基础卡片">
    这是卡片内容
  </femel-card>
  
  <femel-card title="柔和风格卡片" variant="soft">
    这是柔和风格的卡片内容
  </femel-card>
</template>
```

## 色彩系统

组件库提供了一套统一的色彩系统：

```js
import { FemelColors } from 'femel-ui';

// 使用颜色
const primaryColor = FemelColors.primary; // '#E57C9F'
```

主要颜色：
- primary: '#E57C9F' - 粉红色调(主色)
- secondary: '#F4AFBB' - 浅粉色(次要色)
- accent: '#AE5F87' - 深粉紫色(强调色)
- background: '#FFF5F7' - 浅粉背景
- text: '#4A2C40' - 深紫文字

## 许可证

MIT 

# 女性健康监测系统

这是一个基于 Vue.js 的女性健康监测系统，提供心率、体温、经期等健康数据的监测和展示功能。

## 系统要求

- 现代浏览器（Chrome、Firefox、Safari、Edge 等）
- 网络连接（用于加载 Vue.js）

## 安装步骤

1. 解压文件
   - 将 `female-health-system.zip` 解压到任意目录
   - 解压后得到 `female-health-system` 文件夹

2. 运行方式（选择以下任一方式）：

   a. 直接打开（简单方式）：
   - 进入 `female-health-system/pages` 目录
   - 双击 `index.html` 在浏览器中打开

   b. 使用本地服务器（推荐方式）：
   - 使用 Visual Studio Code + Live Server 插件
   - 或使用 Python：`python -m http.server`
   - 或使用 Node.js：`npx http-server`

## 项目结构

```
female-health-system/
├── assets/              # 资源文件
│   ├── css/            # 样式文件
│   └── js/             # JavaScript 文件
├── pages/              # 页面文件
│   ├── index.html      # 首页
│   ├── login.html      # 登录页
│   ├── register.html   # 注册页
│   ├── metrics.html    # 健康指标页
│   ├── heart_rate_chart.html  # 心率图表
│   ├── temperature.html      # 体温图表
│   └── menstrual.html        # 经期图表
└── README.md           # 说明文档
```

## 功能特点

- 心率监测和图表展示
- 体温记录和趋势分析
- 经期周期追踪
- 健康指标统计
- 用户友好的界面设计

## 开发说明

如果您想要修改或开发新功能：

1. 在原始项目文件夹中进行开发
2. 修改完成后重新打包
3. 测试打包后的项目是否正常运行

## 注意事项

- 确保有网络连接以加载 Vue.js
- 建议使用现代浏览器以获得最佳体验
- 首次使用需要注册账号

## 技术支持

如有问题或建议，请联系技术支持。

## 许可证

MIT 
// female-ui-simple.js
const FemaleColors = {
  primary: '#E57C9F',
  secondary: '#F4AFBB',
  accent: '#AE5F87',
  background: '#FFF5F7',
  text: '#4A2C40',
  success: '#7EB8A2',
  warning: '#F9C096',
  error: '#E86B6B',
  neutral: '#F0E4EB',
  white: '#FFFFFF',
  border: '#F0E4EB'
};

// 控制台输出调试信息
console.log('Female UI 组件正在加载...');

// 定义组件
const FemaleButton = {
  props: {
    text: {
      type: String,
      default: '点击我'
    },
    type: {
      type: String,
      default: 'primary'
    }
  },
  template: `
    <button class="female-button" :class="type" @click="$emit('click')">
      {{ text }}
    </button>
  `
};

const FemaleInput = {
  props: {
    placeholder: {
      type: String,
      default: ''
    },
    value: {
      type: String,
      default: ''
    }
  },
  template: `
    <input
      class="female-input"
      :placeholder="placeholder"
      :value="value"
      @input="$emit('input', $event.target.value)"
    />
  `
};

const FemaleCard = {
  props: {
    title: {
      type: String,
      required: true
    }
  },
  template: `
    <div class="female-card">
      <div class="female-card-header">
        <h3 class="female-card-title">{{ title }}</h3>
      </div>
      <div class="female-card-content">
        <slot></slot>
      </div>
    </div>
  `
};

// 导航组件
const FemaleNav = {
  template: `
    <nav class="female-nav">
      <a href="metrics.html" class="nav-link">健康指标</a>
      <a href="consultation.html" class="nav-link">健康咨询</a>
      <a href="messages.html" class="nav-link">消息中心</a>
      <a href="records.html" class="nav-link">健康记录</a>
    </nav>
  `,
  methods: {
    goToRecords() {
      window.location.href = "records.html";
    }
  }
};

// 注册组件
Vue.component('female-nav', FemaleNav);
Vue.component('female-button', FemaleButton);
Vue.component('female-input', FemaleInput);
Vue.component('female-card', FemaleCard);

// 输出调试信息
console.log('Female UI 组件已加载完成');
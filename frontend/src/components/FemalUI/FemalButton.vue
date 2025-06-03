<template>
  <button 
    :class="[
      'female-button', 
      `female-button-${type}`, 
      `female-button-${size}`, 
      { 'female-button-disabled': disabled }
    ]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'FemaleButton',
  props: {
    type: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'outline', 'text'].includes(value)
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.female-button {
  border: none;
  outline: none;
  border-radius: 999px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(156, 91, 128, 0.12);
}

.female-button-primary {
  background-color: #E57C9F;
  color: #FFFFFF;
}

.female-button-primary:hover {
  background-color: #d66a8d;
}

.female-button-secondary {
  background-color: #F4AFBB;
  color: #4A2C40;
}

.female-button-secondary:hover {
  background-color: #e9a0ac;
}

.female-button-outline {
  background-color: transparent;
  color: #E57C9F;
  border: 1.5px solid #E57C9F;
  box-shadow: none;
}

.female-button-outline:hover {
  background-color: rgba(229, 124, 159, 0.1);
}

.female-button-text {
  background-color: transparent;
  color: #E57C9F;
  box-shadow: none;
}

.female-button-text:hover {
  background-color: rgba(229, 124, 159, 0.1);
}

.female-button-small {
  padding: 6px 16px;
  font-size: 12px;
}

.female-button-medium {
  padding: 10px 24px;
  font-size: 14px;
}

.female-button-large {
  padding: 14px 30px;
  font-size: 16px;
}

.female-button-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> 
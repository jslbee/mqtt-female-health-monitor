<template>
  <div :class="['female-card', `female-card-${variant}`]">
    <div v-if="title || $slots.icon" class="female-card-header">
      <div v-if="$slots.icon" class="female-card-icon">
        <slot name="icon"></slot>
      </div>
      <h3 v-if="title" class="female-card-title">{{ title }}</h3>
    </div>
    <div class="female-card-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FemaleCard',
  props: {
    title: {
      type: String,
      default: ''
    },
    variant: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'soft'].includes(value)
    }
  }
}
</script>

<style scoped>
.female-card {
  background-color: #FFFFFF;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
  overflow: hidden;
  margin-bottom: 24px;
}

.female-card-header {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(240, 228, 235, 0.5);
}

.female-card-icon {
  margin-right: 8px;
  color: #E57C9F;
}

.female-card-title {
  margin: 0;
  font-size: 18px;
  color: #4A2C40;
  font-weight: 500;
}

.female-card-content {
  padding: 24px;
}

.female-card-soft {
  background-color: #FFF5F7;
  box-shadow: none;
  border: 1.5px solid rgba(229, 124, 159, 0.1);
}
</style> 
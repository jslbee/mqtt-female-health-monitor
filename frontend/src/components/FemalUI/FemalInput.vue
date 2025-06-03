<template>
  <div :class="['female-input-container', { 'female-input-error': error }]">
    <div v-if="icon" class="female-input-icon">
      <slot name="icon">{{ icon }}</slot>
    </div>
    <input
      :type="type"
      class="female-input"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :disabled="disabled"
    />
    <div v-if="error" class="female-input-error-message">{{ error }}</div>
  </div>
</template>

<script>
export default {
  name: 'FemaleInput',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    icon: {
      type: String,
      default: ''
    },
    error: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.female-input-container {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 16px;
}

.female-input {
  width: 100%;
  padding: 12px 16px;
  border: 1.5px solid #F0E4EB;
  border-radius: 12px;
  background-color: #FFFFFF;
  color: #4A2C40;
  font-size: 14px;
  transition: all 0.3s ease;
}

.female-input:focus {
  border-color: #E57C9F;
  outline: none;
  box-shadow: 0 0 0 3px rgba(229, 124, 159, 0.2);
}

.female-input::placeholder {
  color: #b5a3af;
}

.female-input-icon {
  position: absolute;
  left: 12px;
  color: #b5a3af;
}

.female-input-icon + .female-input {
  padding-left: 40px;
}

.female-input-error .female-input {
  border-color: #E86B6B;
}

.female-input-error .female-input:focus {
  box-shadow: 0 0 0 3px rgba(232, 107, 107, 0.2);
}

.female-input-error-message {
  color: #E86B6B;
  font-size: 12px;
  margin-top: 4px;
}
</style> 
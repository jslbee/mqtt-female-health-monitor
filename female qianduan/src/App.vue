<template>
  <div class="app">
    <FemelExample />
  </div>
</template>

<script>
import FemelExample from './examples/FemelExample.vue';

export default {
  name: 'App',
  components: {
    FemelExample
  }
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
}

.app {
  min-height: 100vh;
}
</style> 
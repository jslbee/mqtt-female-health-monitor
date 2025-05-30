<template>
  <nav class="navbar">
    <router-link to="/metrics" class="nav-item home-link">
      <i class="ri-home-line"></i> 返回首页
    </router-link>
    <router-link to="/metrics" class="nav-item">Health Metrics</router-link>
    <router-link to="/prediction" class="nav-item">Prediction</router-link>
    <router-link to="/messages" class="nav-item">Messages</router-link>
    <router-link to="/records" class="nav-item">Team Members</router-link>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #e57c9f;
  padding: 0 40px;
  height: 60px;
  width: 100%;
}
.nav-item {
  color: #fff;
  margin-right: 40px;
  text-decoration: none;
  font-size: 20px;
  font-weight: 500;
}
.nav-item.router-link-exact-active {
  border-bottom: 2px solid #fff;
}
.home-link {
  display: flex;
  align-items: center;
  gap: 5px;
}
</style> 
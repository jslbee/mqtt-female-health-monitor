<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2 class="login-title">欢迎回来</h2>
        <p class="login-subtitle">登录你的健康监测账号</p>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码" required />
        </div>
        <div class="remember-forgot">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>
        <div class="button-container">
          <button class="female-button" type="submit">登录</button>
        </div>
        <div class="register-link">
          没有账号？<a href="#">立即注册</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false
    }
  },
  methods: {
    handleLogin() {
      // 简单模拟登录逻辑
      if (this.username && this.password) {
        localStorage.setItem('isLoggedIn', 'true')
        this.$router.push('/metrics')
      } else {
        alert('请输入用户名和密码')
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #FFF5F7;
  padding: 20px;
}
.login-card {
  background-color: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
}
.login-header {
  text-align: center;
  margin-bottom: 30px;
}
.login-title {
  color: #4A2C40;
  font-size: 24px;
  margin-bottom: 10px;
}
.login-subtitle {
  color: #666;
  font-size: 16px;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  color: #4A2C40;
  margin-bottom: 8px;
  font-size: 14px;
}
.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #E57C9F;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s;
}
.form-group input:focus {
  outline: none;
  border-color: #4A2C40;
  box-shadow: 0 0 0 2px rgba(229, 124, 159, 0.2);
}
.remember-forgot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}
.forgot-password {
  color: #E57C9F;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}
.forgot-password:hover {
  color: #4A2C40;
}
.button-container {
  margin-top: 20px;
  text-align: center;
}
.female-button {
  width: 100%;
  max-width: 200px;
  margin: 0 auto;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 16px;
  background-color: #E57C9F;
  color: white;
  border: none;
  transition: all 0.3s ease;
  cursor: pointer;
}
.female-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(229, 124, 159, 0.3);
  background-color: #d66a8d;
}
.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}
.register-link a {
  color: #E57C9F;
  text-decoration: none;
  transition: color 0.3s;
}
.register-link a:hover {
  color: #4A2C40;
}
@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
}
</style>

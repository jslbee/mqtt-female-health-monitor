<template>
  <div>
    <NavBar />
    <div class="register-container">
      <div class="register-card">
        <h2 class="register-title">注册新账号</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="username">用户名</label>
            <input type="text" id="username" v-model="username" required />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <div class="button-container">
            <button class="female-button" type="submit">注册</button>
          </div>
          <div class="login-link">
            已有账号？<a @click.prevent="goToLogin" href="#">去登录</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import { registerApi } from '@/api'

export default {
  name: 'Register',
  components: { NavBar },
  data() {
    return {
      username: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      alert('点击了注册');
      if (!this.username || !this.password) {
        alert('请输入用户名和密码');
        return;
      }
      this.loading = true;
      try {
        await registerApi(this.username, this.password);
        alert('注册成功，请登录');
        this.$router.push('/login');
      } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
          alert('注册失败：' + err.response.data.detail);
        } else {
          alert('注册失败，请重试');
        }
      } finally {
        this.loading = false;
      }
    },
    goToLogin() {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #FFF5F7;
  padding: 20px;
}
.register-card {
  background-color: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
}
.register-title {
  color: #4A2C40;
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
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
.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}
.login-link a {
  color: #E57C9F;
  text-decoration: none;
  transition: color 0.3s;
}
.login-link a:hover {
  color: #4A2C40;
}
</style> 
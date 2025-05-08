<template>
  <div>
    <NavBar />
    <div class="container">
      <div class="header">
        <h1>Messages</h1>
        <p class="subtitle">View your latest notifications and messages.</p>
      </div>
      <div class="messages-section">
        <div v-for="(message, index) in messages" :key="index" class="message-item" :class="{ 'unread': !message.read }" @click="toggleMessage(index)">
          <div class="message-header">
            <span class="sender">{{ message.sender }}</span>
            <span class="date">{{ message.date }}</span>
          </div>
          <div class="message-content" :class="{ 'expanded': message.expanded }">
            {{ message.content }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
export default {
  name: 'Messages',
  components: { NavBar },
  data() {
    return {
      messages: [
        { sender: 'Dr. Smith', date: '2023-10-01', content: 'Your test results are ready.', read: false, expanded: false },
        { sender: 'Nurse Johnson', date: '2023-09-30', content: 'Please schedule your next appointment.', read: true, expanded: false }
      ]
    };
  },
  methods: {
    toggleMessage(index) {
      this.messages[index].expanded = !this.messages[index].expanded;
      this.messages[index].read = true;
    }
  }
}
</script>

<style scoped>
.container { max-width: 900px; margin: 0 auto; padding: 30px; }
.header { text-align: center; margin-bottom: 30px; }
.subtitle { color: #666; font-size: 16px; margin-top: 10px; }
.messages-section { background: #fff; border-radius: 15px; padding: 25px; box-shadow: 0 4px 12px rgba(156,91,128,0.08); }
.message-item { border-bottom: 1px solid #f0e0e7; padding: 18px 0; cursor: pointer; }
.message-item:last-child { border-bottom: none; }
.message-header {
  display: flex;
  justify-content: space-between;
}
.sender { font-weight: bold; color: #E57C9F; margin-bottom: 6px; }
.date { color: #aaa; font-size: 13px; }
.message-content {
  display: none;
}
.message-content.expanded {
  display: block;
}
.unread .sender { color: #C45D7D; }
</style> 
<template>
  <div class="bg-gradient">
    <NavBar />
    <div class="container">
      <div class="header">
        <h1>AI 聊天助手</h1>
        <p class="subtitle">和AI健康助手对话，获取健康建议或解答。</p>
      </div>
      <div class="chat-section" ref="chatSection">
        <div
          v-for="(msg, idx) in chatHistory"
          :key="idx"
          :class="['chat-row', msg.role]"
        >
          <div :class="['chat-bubble', msg.role]">
            <span class="role">{{ msg.role === 'user' ? '我' : 'AI' }}</span>
            <span class="content">{{ msg.content }}</span>
          </div>
        </div>
      </div>
      <div class="input-section">
        <el-input
          v-model="userInput"
          placeholder="请输入您的问题…"
          :autosize="{ minRows: 2, maxRows: 4 }"
          type="textarea"
          class="chat-input"
          @keyup.enter.native="sendMessage"
          :disabled="loading"
        />
        <el-button type="primary" @click="sendMessage" :loading="loading" class="send-btn">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import { ref, nextTick } from 'vue'
import { chatbotService } from '@/api/chatbotService'

export default {
  name: 'Messages',
  components: { NavBar },
  setup() {
    const chatHistory = ref([
      { role: 'ai', content: '您好，我是AI健康助手，有什么可以帮您？' }
    ])
    const userInput = ref('')
    const loading = ref(false)
    const chatSection = ref(null)

    const scrollToBottom = () => {
      nextTick(() => {
        if (chatSection.value) {
          chatSection.value.scrollTop = chatSection.value.scrollHeight
        }
      })
    }

    const sendMessage = async () => {
      if (!userInput.value.trim()) return
      const message = userInput.value
      chatHistory.value.push({ role: 'user', content: message })
      userInput.value = ''
      loading.value = true
      scrollToBottom()
      try {
        const reply = await chatbotService.ask(message)
        // 兼容AI返回json字符串的情况
        let aiContent = reply
        if (typeof reply === 'object' && reply.response) {
          aiContent = reply.response
        } else if (typeof reply === 'string' && reply.startsWith('{')) {
          try {
            const obj = JSON.parse(reply)
            aiContent = obj.response || reply
          } catch {
            aiContent = reply
          }
        }
        chatHistory.value.push({ role: 'ai', content: aiContent })
      } catch (e) {
        chatHistory.value.push({ role: 'ai', content: 'AI服务暂时不可用，请稍后再试。' })
      } finally {
        loading.value = false
        scrollToBottom()
      }
    }

    return { chatHistory, userInput, loading, sendMessage, chatSection }
  }
}
</script>

<style scoped>
.bg-gradient {
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(120deg, #f8e1f0 0%, #f6f7fb 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.container {
  max-width: 900px;
  width: 100%;
  margin: 40px auto 0 auto;
  padding: 30px 0;
  display: flex;
  flex-direction: column;
  height: 85vh;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(156,91,128,0.10);
}
.header {
  text-align: center;
  margin-bottom: 20px;
}
.subtitle {
  color: #666;
  font-size: 16px;
  margin-top: 10px;
}
.chat-section {
  background: #fff;
  border-radius: 20px;
  padding: 30px 20px 30px 20px;
  min-height: 300px;
  flex: 1 1 auto;
  box-shadow: 0 4px 12px rgba(156,91,128,0.08);
  margin-bottom: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.chat-row {
  display: flex;
  margin-bottom: 16px;
}
.chat-row.user {
  justify-content: flex-end;
}
.chat-row.ai {
  justify-content: flex-start;
}
.chat-bubble {
  max-width: 70%;
  padding: 14px 18px;
  border-radius: 18px;
  font-size: 16px;
  line-height: 1.7;
  box-shadow: 0 2px 8px rgba(156,91,128,0.08);
  word-break: break-all;
  position: relative;
  display: flex;
  flex-direction: column;
}
.chat-bubble.user {
  background: linear-gradient(135deg, #e57c9f 0%, #f8b6d6 100%);
  color: #fff;
  align-items: flex-end;
  border-bottom-right-radius: 4px;
}
.chat-bubble.ai {
  background: #f5f5f5;
  color: #4A2C40;
  align-items: flex-start;
  border-bottom-left-radius: 4px;
}
.role {
  font-size: 13px;
  font-weight: bold;
  margin-bottom: 4px;
  opacity: 0.7;
}
.input-section {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  margin-top: 10px;
  padding-bottom: 10px;
}
.chat-input {
  flex: 1 1 auto;
  min-height: 48px;
  font-size: 16px;
}
.send-btn {
  height: 48px;
  font-size: 16px;
  padding: 0 24px;
}
.chat-bubble .content {
  display: block;
  text-align: left;
}
</style> 
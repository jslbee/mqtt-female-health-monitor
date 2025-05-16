<template>
  <div>
    <NavBar />
    <div class="health-records">
      <h1>Health Records</h1>
      <div class="profile-card">
        <img src="https://cdn.jsdelivr.net/gh/edent/SuperTinyIcons/images/svg/user.svg" alt="Avatar" class="avatar" />
        <div class="profile-info">
          <h2>Jane Doe</h2>
          <p>Age: 28</p>
          <p>Gender: Female</p>
          <button class="edit-btn">Edit Profile</button>
        </div>
      </div>
      <div class="history-section">
        <h2>Health History</h2>
        <div v-for="(record, index) in healthHistory" :key="index" class="history-item" @click="toggleHistory(index)">
          <div class="history-header">
            <span class="date">{{ record.date }}</span>
            <span class="condition">{{ record.condition }}</span>
          </div>
          <div class="history-details" :class="{ 'expanded': record.expanded }">
            {{ record.details }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'HealthRecords',
  components: { NavBar },
  data() {
    return {
      healthHistory: [
        { date: '2023-10-01', condition: 'Fever', details: 'Temperature: 38.5°C, Treated with rest and medication.', expanded: false },
        { date: '2023-09-30', condition: 'Headache', details: 'Mild headache, resolved with over-the-counter pain relievers.', expanded: false }
      ]
    };
  },
  methods: {
    toggleHistory(index) {
      this.healthHistory[index].expanded = !this.healthHistory[index].expanded;
    }
  }
};
</script>

<style scoped>
.health-records {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 64px);
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

h1 {
  color: #9C5B80;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
}

.profile-card {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  padding: 2rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(156, 91, 128, 0.12);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(156, 91, 128, 0.16);
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 2rem;
  border: 4px solid #9C5B80;
  padding: 4px;
  background: #fff;
}

.profile-info {
  flex: 1;
}

.profile-info h2 {
  color: #9C5B80;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.profile-info p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.edit-btn {
  background: #9C5B80;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.edit-btn:hover {
  background: #E57C9F;
  transform: translateY(-2px);
}

.history-section {
  background: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(156, 91, 128, 0.12);
}

.history-section h2 {
  color: #9C5B80;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

.history-item {
  margin-bottom: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(156, 91, 128, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.history-item:hover {
  border-color: #9C5B80;
  box-shadow: 0 4px 12px rgba(156, 91, 128, 0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-header .date {
  color: #9C5B80;
  font-weight: 600;
  font-size: 1.1rem;
}

.history-header .condition {
  color: #666;
  font-size: 1.1rem;
}

.history-details {
  display: none;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(156, 91, 128, 0.1);
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

.history-details.expanded {
  display: block;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 
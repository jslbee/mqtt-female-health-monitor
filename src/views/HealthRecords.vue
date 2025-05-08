<template>
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
</template>

<script>
export default {
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
  padding: 20px;
}
.profile-card {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(156,91,128,0.08);
}
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 20px;
}
.profile-info {
  flex: 1;
}
.edit-btn {
  background: #E57C9F;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}
.history-item {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
}
.history-header {
  display: flex;
  justify-content: space-between;
}
.history-details {
  display: none;
}
.history-details.expanded {
  display: block;
}
</style> 
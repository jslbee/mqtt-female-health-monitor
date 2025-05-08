<template>
  <div>
    <NavBar />
    <div class="header">
      <h1 class="animated-title"><i class="ri-heart-pulse-line" style="color: #E57C9F; font-size: 0.9em; margin-right: 15px;"></i>Artemis</h1>
      <h2>FEMALE HEALTH MONITORING SYSTEM</h2>
    </div>
    <div class="health-summary">
      <h3 class="summary-title">Health Data Summary</h3>
      <div class="summary-stats">
        <div class="stat-item">
          <div class="stat-value">78</div>
          <div class="stat-label">Average Heart Rate (bpm)</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">36.5°</div>
          <div class="stat-label">Average Temperature</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">28</div>
          <div class="stat-label">Current Cycle (days)</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">5</div>
          <div class="stat-label">Days Until Next Period</div>
        </div>
      </div>
    </div>
    <!-- Featured image section -->
    <div class="featured-image">
      <div class="image-container">
        <img src="https://images.pexels.com/photos/7991361/pexels-photo-7991361.jpeg?auto=compress&cs=tinysrgb&w=1200" alt="Women's Health Care" loading="lazy">
        <div class="image-overlay">
          <h3>Care for Women's Health, Every Day</h3>
          <p>Regularly monitor your physical condition, track health data, and help every woman better understand her body and maintain a healthy, beautiful life.</p>
        </div>
      </div>
    </div>
    <!-- Health metrics display -->
    <div class="dashboard">
      <router-link to="/heart-rate" class="female-card">
        <div class="card-icon"><i class="ri-heart-pulse-line"></i></div>
        <h3>Heart Rate</h3>
        <p>View your heart rate data</p>
      </router-link>
      <router-link to="/temperature" class="female-card">
        <div class="card-icon"><i class="ri-temp-hot-line"></i></div>
        <h3>Temperature</h3>
        <p>View your temperature data</p>
      </router-link>
      <router-link to="/menstrual" class="female-card">
        <div class="card-icon"><i class="ri-calendar-event-line"></i></div>
        <h3>Menstrual</h3>
        <p>View your menstrual data</p>
      </router-link>
    </div>
    <!-- Mood record section -->
    <div class="health-overview">
      <h3 class="overview-title"><i class="ri-emotion-happy-line"></i>Record Mood</h3>
      <div class="image-container">
        <img src="https://images.pexels.com/photos/3807770/pexels-photo-3807770.jpeg?auto=compress&cs=tinysrgb&w=1200" alt="Record Daily Mood" loading="lazy">
        <div class="image-overlay">
          <h4>Record Today's Mood</h4>
          <p>Track your emotional changes to understand your physical and mental health status.</p>
        </div>
      </div>
      <div class="mood-container">
        <h3 class="section-title">Today's Mood</h3>
        <p class="section-subtitle">Record your current emotional state</p>
        <div class="mood-grid">
          <div v-for="mood in moods" :key="mood.id" class="mood-item" :class="{ selected: selectedMood === mood.id }" @click="selectMood(mood.id)" :data-mood="mood.id">
            <div class="mood-icon" :class="mood.color">
              <i :class="mood.icon"></i>
            </div>
            <div class="mood-label">{{ mood.label }}</div>
          </div>
        </div>
        <div class="mood-submit">
          <button class="female-button" @click="saveMood">Save Mood</button>
        </div>
      </div>
    </div>
    <!-- Health tips -->
    <div class="health-tips">
      <h3 class="tips-title">Health Tips</h3>
      <div class="tip-card">
        <h4>Menstrual Health</h4>
        <p>During menstruation, keep warm, avoid strenuous exercise and cold stimulation, and appropriately supplement iron-rich foods such as lean meat and spinach.</p>
      </div>
      <div class="tip-card">
        <h4>Emotional Regulation</h4>
        <p>Relieve stress and anxiety through mindfulness meditation, deep breathing, or gentle yoga to maintain mental health.</p>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'
export default {
  name: 'Dashboard',
  components: { NavBar },
  data() {
    return {
      selectedMood: null,
      moods: [
        { id: 'happy', label: 'Happy', icon: 'ri-emotion-happy-line', color: 'mood-happy' },
        { id: 'sad', label: 'Sad', icon: 'ri-emotion-sad-line', color: 'mood-sad' },
        { id: 'excited', label: 'Excited', icon: 'ri-emotion-laugh-line', color: 'mood-excited' },
        { id: 'calm', label: 'Calm', icon: 'ri-emotion-normal-line', color: 'mood-calm' },
        { id: 'frustrated', label: 'Frustrated', icon: 'ri-emotion-unhappy-line', color: 'mood-frustrated' },
        { id: 'tired', label: 'Tired', icon: 'ri-emotion-line', color: 'mood-tired' },
        { id: 'badmood', label: 'Low', icon: 'ri-emotion-2-line', color: 'mood-badmood' },
        { id: 'relax', label: 'Relaxed', icon: 'ri-emotion-line', color: 'mood-relax' },
        { id: 'fun', label: 'Fun', icon: 'ri-emotion-laugh-line', color: 'mood-fun' }
      ]
    }
  },
  methods: {
    selectMood(moodId) {
      this.selectedMood = moodId;
    },
    saveMood() {
      if (!this.selectedMood) {
        alert('Please select a mood first');
        return;
      }
      const today = new Date().toISOString().split('T')[0];
      const moodData = {
        date: today,
        mood: this.selectedMood
      };
      let moodHistory = JSON.parse(localStorage.getItem('moodHistory') || '[]');
      moodHistory.push(moodData);
      localStorage.setItem('moodHistory', JSON.stringify(moodHistory));
      alert('Mood recorded successfully');
      this.selectedMood = null;
    }
  }
}
</script>

<style scoped>
.header {
  text-align: center;
  padding: 40px 20px 50px;
  position: relative;
}
.header::after {
  content: '';
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background-color: #E57C9F;
  border-radius: 3px;
}
h1 {
  color: #4A2C40;
  font-size: clamp(36px, 5vw, 48px);
  margin-bottom: 15px;
  letter-spacing: 1px;
  font-weight: 700;
}
h2 {
  color: #4A2C40;
  font-size: clamp(18px, 2.5vw, 24px);
  font-weight: normal;
  margin: 0;
  opacity: 0.8;
  letter-spacing: 2px;
  text-transform: uppercase;
  background: linear-gradient(to right, #4A2C40, #E57C9F);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
  padding-bottom: 5px;
}
.animated-title {
  display: inline-block;
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
}
.animated-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #E57C9F;
  transform: scaleX(0);
  transform-origin: bottom right;
  transition: transform 0.5s ease;
}
.animated-title:hover {
  transform: translateY(-5px);
  text-shadow: 0 5px 15px rgba(229, 124, 159, 0.3);
}
.animated-title:hover::after {
  transform: scaleX(1);
  transform-origin: bottom left;
}
.animated-title i {
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
.health-summary {
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 50px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
}
.summary-title {
  color: #4A2C40;
  font-size: clamp(18px, 2.5vw, 22px);
  margin-bottom: 15px;
  text-align: center;
}
.summary-stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 15px;
}
.stat-item {
  text-align: center;
  flex: 1;
  min-width: 120px;
  padding: 15px 10px;
  border-radius: 15px;
  background-color: rgba(229, 124, 159, 0.05);
  transition: all 0.3s ease;
}
.stat-item:hover {
  background-color: rgba(229, 124, 159, 0.1);
  transform: translateY(-3px);
}
.stat-value {
  font-size: clamp(24px, 3vw, 32px);
  font-weight: bold;
  color: #E57C9F;
  margin-bottom: 5px;
}
.stat-label {
  font-size: clamp(12px, 1.5vw, 14px);
  color: #4A2C40;
}
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: clamp(20px, 3vw, 40px);
  max-width: 1200px;
  margin: 0 auto 60px;
}
.female-card {
  height: 100%;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: clamp(16px, 3vw, 24px);
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
  text-decoration: none;
  color: #4A2C40;
  transition: all 0.3s ease;
}
.female-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(156, 91, 128, 0.15);
  color: #E57C9F;
}
.card-icon {
  font-size: 48px;
  color: #E57C9F;
  margin-bottom: 20px;
  text-align: center;
}
.health-overview {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  max-width: 1200px;
  margin: 40px auto 40px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
}
.overview-title {
  color: #4A2C40;
  font-size: clamp(18px, 2.5vw, 22px);
  margin-bottom: 25px;
  text-align: center;
}
.image-container {
  position: relative;
  margin-bottom: 20px;
}
.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: none;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
}
.image-overlay h4 {
  color: #fff;
  font-size: clamp(16px, 2vw, 18px);
  margin-bottom: 10px;
}
.image-overlay p {
  color: #fff;
  font-size: clamp(14px, 1.5vw, 16px);
}
.mood-container {
  text-align: center;
}
.section-title {
  color: #4A2C40;
  font-size: clamp(18px, 2.5vw, 22px);
  margin-bottom: 10px;
}
.section-subtitle {
  color: #666;
  font-size: clamp(14px, 1.5vw, 16px);
}
.mood-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}
.mood-item {
  cursor: pointer;
  padding: 10px;
  border-radius: 10px;
  background-color: rgba(229, 124, 159, 0.05);
  transition: all 0.3s ease;
}
.mood-item:hover {
  background-color: rgba(229, 124, 159, 0.1);
}
.mood-item.selected {
  background-color: rgba(229, 124, 159, 0.1);
}
.mood-icon {
  font-size: 24px;
  color: #E57C9F;
  margin-bottom: 5px;
}
.mood-label {
  font-size: clamp(12px, 1.5vw, 14px);
  color: #4A2C40;
}
.mood-submit {
  margin-top: 20px;
}
.female-button {
  padding: 10px 20px;
  background-color: #E57C9F;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.female-button:hover {
  background-color: #C45D7D;
}
.health-tips {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  max-width: 1200px;
  margin: 40px auto 40px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
}
.tips-title {
  color: #4A2C40;
  font-size: clamp(18px, 2.5vw, 22px);
  margin-bottom: 25px;
  text-align: center;
}
.tip-card {
  background-color: rgba(229, 124, 159, 0.05);
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  border-left: 4px solid #E57C9F;
}
.tip-card h4 {
  color: #4A2C40;
  margin-top: 0;
  margin-bottom: 10px;
  font-size: clamp(16px, 2vw, 18px);
}
.tip-card p {
  color: #666;
  margin: 0;
  font-size: clamp(14px, 1.5vw, 16px);
}
</style> 
<template>
  <div>
    <NavBar />
    <div class="header">
      <h1 class="animated-title"><i class="ri-heart-pulse-line" style="color: #E57C9F; font-size: 0.9em; margin-right: 15px;"></i>Artemis</h1>
      <h2>FEMALE HEALTH MONITORING SYSTEM</h2>
    </div>
    <div class="health-summary fade-in">
      <h3 class="summary-title">Health Data Summary</h3>
      <div class="summary-stats">
        <div class="stat-item">
          <div class="stat-value">{{ healthStats.averageHeartRate }}</div>
          <div class="stat-label">Average Heart Rate (bpm)</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ healthStats.averageTemperature }}°</div>
          <div class="stat-label">Average Temperature</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ healthStats.currentCycle }}</div>
          <div class="stat-label">Current Cycle (days)</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ healthStats.daysUntilNextPeriod }}</div>
          <div class="stat-label">Days Until Next Period</div>
        </div>
      </div>
    </div>
    <!-- Featured image section -->
    <div class="featured-image fade-in">
      <div class="image-container">
        <img src="https://images.pexels.com/photos/7991361/pexels-photo-7991361.jpeg?auto=compress&cs=tinysrgb&w=1200" alt="Women's Health Care" loading="lazy">
        <div class="image-overlay">
          <h3>Care for Women's Health, Every Day</h3>
          <p>Regularly monitor your physical condition,<br>track health data, and help every woman better understand her body.</p>
        </div>
      </div>
    </div>
    <!-- Health metrics display -->
    <div class="dashboard fade-in">
      <router-link to="/heart-rate" class="female-card heart-rate-card">
        <div class="card-icon"><i class="ri-heart-pulse-line"></i></div>
        <h3>Heart Rate</h3>
        <p>View your heart rate data</p>
      </router-link>
      <router-link to="/temperature" class="female-card temperature-card">
        <div class="card-icon"><i class="ri-temp-hot-line"></i></div>
        <h3>Temperature</h3>
        <p>View your temperature data</p>
      </router-link>
      <router-link to="/menstrual" class="female-card menstrual-card">
        <div class="card-icon"><i class="ri-calendar-event-line"></i></div>
        <h3>Menstrual</h3>
        <p>View your menstrual data</p>
      </router-link>
    </div>
    <!-- Mood record section -->
    <div class="health-overview fade-in">
      <h3 class="overview-title"><i class="ri-emotion-happy-line"></i>Record Mood</h3>
      <div class="image-container fade-in">
        <img src="https://images.pexels.com/photos/3807770/pexels-photo-3807770.jpeg?auto=compress&cs=tinysrgb&w=1200" alt="Record Daily Mood" loading="lazy">
        <div class="image-overlay">
          <h4>Record Today's Mood</h4>
          <p>Track your emotional changes to understand your physical and mental health status.</p>
        </div>
      </div>
      <div class="mood-container" ref="moodSelection">
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
          <button class="female-button clear-button" @click="clearSelectedDate" v-if="selectedDateForMood">Clear Selection</button>
        </div>
      </div>
    </div>

    <!-- Mood History Calendar Section -->
    <div class="mood-calendar-section health-overview fade-in">
      <h3 class="overview-title"><i class="ri-history-line"></i>Mood History Calendar</h3>
      <div class="calendar-header-custom">
         <button @click="moveCalendar('prevYear')">&lt;&lt;</button>
         <button @click="moveCalendar('prevMonth')">&lt;</button>
         <span>{{ currentMonthYear }}</span>
         <button @click="moveCalendar('nextMonth')">&gt;</button>
         <button @click="moveCalendar('nextYear')">&gt;&gt;</button>
      </div>
      <div class="calendar-container">
        <CalendarView
          :show-date="currentCalendarDate"
          :items="calendarEvents"
          class="theme-default holiday-us-traditional holiday-us-official"
          @click-date="handleClickDate"
          @click-item="handleClickItem"
        >
          <template #dayContent="{ day }">
            <div class="day-content" :class="{ 'selected-date': isDateSelected(day.date) }">
              <div class="day-number">{{ day.label }}</div>
              <div class="mood-icons">
                <i v-for="mood in getMoodsForDate(day.date)" :key="mood.id" :class="[mood.icon, mood.color]" :title="mood.label"></i>
              </div>
            </div>
          </template>
        </CalendarView>
      </div>
    </div>

    <!-- User Guide Section -->
    <div class="user-guide health-overview fade-in">
      <h3 class="overview-title"><i class="ri-book-open-line"></i>User Guide</h3>
      <div class="guide-content">
        <div class="guide-section">
          <h4><i class="ri-heart-pulse-line"></i>Health Data</h4>
          <ul>
            <li>Heart Rate: Monitor your heart rate changes in real-time to understand your physical condition</li>
            <li>Temperature: Record daily temperature to track physiological cycle changes</li>
            <li>Menstrual Tracking: Record menstrual periods and predict next cycle</li>
          </ul>
        </div>
        <div class="guide-section">
          <h4><i class="ri-emotion-happy-line"></i>Mood Recording</h4>
          <ul>
            <li>Daily Mood: Select an icon that matches your current mood</li>
            <li>Mood Calendar: View historical mood records to understand emotional changes</li>
            <li>Mood Analysis: Analyze emotional patterns through long-term records</li>
          </ul>
        </div>
        <div class="guide-section">
          <h4><i class="ri-calendar-event-line"></i>Calendar Features</h4>
          <ul>
            <li>Click Date: Select specific dates to record mood</li>
            <li>View History: Check past mood records through calendar</li>
            <li>Data Sync: All data is automatically saved and accessible anytime</li>
          </ul>
        </div>
        <div class="guide-section">
          <h4><i class="ri-message-2-line"></i>AI Chat Assistant</h4>
          <ul>
            <li>Health Consultation: Consult AI assistant about health-related questions</li>
            <li>Smart Suggestions: Get personalized health recommendations</li>
            <li>Real-time Chat: 24/7 online support for your questions</li>
          </ul>
        </div>
        <div class="guide-section">
          <h4><i class="ri-line-chart-line"></i>Data Prediction</h4>
          <ul>
            <li>Period Prediction: Predict next period based on historical data</li>
            <li>Health Trends: Analyze health data trends</li>
            <li>Smart Reminders: Important dates and health notifications</li>
          </ul>
        </div>
        <div class="guide-section">
          <h4><i class="ri-shield-check-line"></i>Privacy & Security</h4>
          <ul>
            <li>Data Encryption: All data is encrypted and stored</li>
            <li>Privacy Protection: Strict privacy protection policies</li>
            <li>Security Authentication: Multiple authentication protection</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Health tips -->
    <div class="health-tips fade-in">
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
import { CalendarView } from 'vue-simple-calendar'

import 'vue-simple-calendar/dist/vue-simple-calendar.css'
import 'vue-simple-calendar/dist/css/default.css'
import 'vue-simple-calendar/dist/css/holidays-us.css'

export default {
  name: 'Dashboard',
  components: { NavBar, CalendarView },
  data() {
    return {
      selectedMood: null,
      moodHistory: [],
      moods: [
        { id: 'happy', label: 'Happy', icon: 'ri-emotion-happy-line', color: 'mood-happy' },
        { id: 'sad', label: 'Sad', icon: 'ri-cloudy-line', color: 'mood-sad' },
        { id: 'excited', label: 'Excited', icon: 'ri-fire-line', color: 'mood-excited' },
        { id: 'calm', label: 'Calm', icon: 'ri-leaf-line', color: 'mood-calm' },
        { id: 'frustrated', label: 'Frustrated', icon: 'ri-emotion-unhappy-line', color: 'mood-frustrated' },
        { id: 'tired', label: 'Tired', icon: 'ri-moon-clear-line', color: 'mood-tired' },
        { id: 'badmood', label: 'Low', icon: 'ri-rainy-line', color: 'mood-badmood' },
        { id: 'relax', label: 'Relaxed', icon: 'ri-bubble-chart-line', color: 'mood-relax' },
        { id: 'fun', label: 'Fun', icon: 'ri-magic-line', color: 'mood-fun' }
      ],
      healthStats: {
        averageHeartRate: 78,
        averageTemperature: 36.5,
        currentCycle: 28,
        daysUntilNextPeriod: 5
      },
      currentCalendarDate: new Date(),
      selectedDateForMood: null,
    }
  },
  computed: {
    calendarEvents() {
      return this.moodHistory.map(record => {
        const mood = this.moods.find(m => m.id === record.mood);
        return {
          id: record.date + '_' + record.mood,
          startDate: new Date(record.date),
          endDate: new Date(record.date),
          title: mood ? mood.label : record.mood,
          classes: ['mood-event', `mood-${record.mood}`],
          moodId: record.mood
        };
      });
    },
    currentMonthYear() {
      const options = { year: 'numeric', month: 'long' };
      return this.currentCalendarDate.toLocaleDateString(undefined, options);
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
      const dateToSave = this.selectedDateForMood ? this.selectedDateForMood : new Date().toISOString().split('T')[0];

      const moodData = {
        date: dateToSave,
        mood: this.selectedMood
      };
      let moodHistory = JSON.parse(localStorage.getItem('moodHistory') || '[]');

      moodHistory = moodHistory.filter(record => record.date !== dateToSave);

      moodHistory.push(moodData);
      localStorage.setItem('moodHistory', JSON.stringify(moodHistory));
      alert('Mood recorded successfully');
      this.selectedMood = null;
      this.selectedDateForMood = null;
      this.loadMoodHistory();
      console.log('Mood saved and loadMoodHistory called. Current moodHistory:', this.moodHistory);
    },
    loadMoodHistory() {
      this.moodHistory = JSON.parse(localStorage.getItem('moodHistory') || '[]');
      this.moodHistory.sort((a, b) => new Date(b.date) - new Date(a.date));
      console.log('Mood history loaded:', this.moodHistory);
    },
    getMoodLabel(moodId) {
      const mood = this.moods.find(m => m.id === moodId);
      return mood ? mood.label : moodId;
    },
    setCurrentCalendarDate(date) {
      this.currentCalendarDate = date;
    },
    getMoodsForDate(date) {
      const dateString = date.toISOString().split('T')[0];
      const records = this.moodHistory.filter(record => record.date === dateString);
      console.log(`Getting moods for date: ${dateString}, found records: `, records);
      return records.map(record => this.moods.find(mood => mood.id === record.mood)).filter(mood => mood !== undefined);
    },
    handleClickDate(date) {
      // 使用本地时间而不是UTC时间
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const clickedDateString = `${year}-${month}-${day}`;

      if (this.selectedDateForMood === clickedDateString) {
        this.selectedDateForMood = null;
      } else {
        this.selectedDateForMood = clickedDateString;
      }
      console.log('Clicked date string:', this.selectedDateForMood);

      this.$nextTick(() => {
        const moodSection = this.$refs.moodSelection;
        if (moodSection) {
          moodSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    },
    handleClickItem(item) {
      console.log('Clicked item:', item);
      const date = new Date(item.startDate);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      this.selectedDateForMood = `${year}-${month}-${day}`;

      if (item.moodId) {
        this.selectedMood = item.moodId;
      }

      this.$nextTick(() => {
        const moodSection = this.$refs.moodSelection;
        if (moodSection) {
          moodSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    },
    isDateSelected(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const dateString = `${year}-${month}-${day}`;
      return this.selectedDateForMood === dateString;
    },
    clearSelectedDate() {
      if (this.selectedDateForMood) {
        // 从localStorage中删除选中日期的记录
        let moodHistory = JSON.parse(localStorage.getItem('moodHistory') || '[]');
        moodHistory = moodHistory.filter(record => record.date !== this.selectedDateForMood);
        localStorage.setItem('moodHistory', JSON.stringify(moodHistory));
        
        // 重新加载心情历史
        this.loadMoodHistory();
      }
      
      this.selectedDateForMood = null;
      this.selectedMood = null;
      console.log('Selected date and mood cleared.');
    },
    moveCalendar(period) {
      const newDate = new Date(this.currentCalendarDate);
      switch (period) {
        case 'prevYear':
          newDate.setFullYear(newDate.getFullYear() - 1);
          break;
        case 'prevMonth':
          newDate.setMonth(newDate.getMonth() - 1);
          break;
        case 'nextMonth':
          newDate.setMonth(newDate.getMonth() + 1);
          break;
        case 'nextYear':
          newDate.setFullYear(newDate.getFullYear() + 1);
          break;
      }
      this.currentCalendarDate = newDate;
    },
  },
  mounted() {
    this.loadMoodHistory();
    // Smooth scrolling when navigating
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
        });
      });
    });

    // Intersection Observer for fade-in animation
    // Delay setting up observer to ensure DOM is ready
    setTimeout(() => {
      const fadeInElements = this.$el.querySelectorAll('.fade-in');

      const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target); // Stop observing once visible
          }
        });
      }, {
        threshold: 0.1 // Trigger when 10% of the element is visible
      });

      fadeInElements.forEach(element => {
        // Check if element is already visible on load
        if (element.getBoundingClientRect().top < window.innerHeight && element.getBoundingClientRect().bottom > 0) {
          element.classList.add('is-visible');
        } else {
          observer.observe(element);
        }
      });
    }, 100); // Add a small delay (e.g., 100ms)
  },
  beforeDestroy() {
    // Optional: Disconnect observer when component is destroyed
    const fadeInElements = this.$el.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        observer.unobserve(entry.target);
      });
    });
    fadeInElements.forEach(element => {
      observer.observe(element);
    });
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
  background-color: #D83F87;
  border-radius: 3px;
}
h1 {
  color: #2A1B3D;
  font-size: clamp(36px, 5vw, 48px);
  margin-bottom: 15px;
  letter-spacing: 1px;
  font-weight: 700;
}
h2 {
  color: #2A1B3D;
  font-size: clamp(18px, 2.5vw, 24px);
  font-weight: normal;
  margin: 0;
  opacity: 0.8;
  letter-spacing: 2px;
  text-transform: uppercase;
  background: linear-gradient(to right, #2A1B3D, #D83F87);
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
  background: linear-gradient(135deg, #fff 0%, #FFF5F7 100%);
  border-radius: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 50px;
  box-shadow: 0 4px 20px rgba(42, 27, 61, 0.12);
  border: 1px solid rgba(216, 63, 135, 0.1);
}
.summary-title {
  color: #2A1B3D;
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
  background: linear-gradient(135deg, rgba(216, 63, 135, 0.05) 0%, rgba(68, 49, 141, 0.05) 100%);
  transition: all 0.3s ease;
  border: 1px solid rgba(216, 63, 135, 0.1);
}
.stat-item:hover {
  background: linear-gradient(135deg, rgba(216, 63, 135, 0.1) 0%, rgba(68, 49, 141, 0.1) 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(216, 63, 135, 0.15);
}
.stat-value {
  font-size: clamp(24px, 3vw, 32px);
  font-weight: bold;
  color: #D83F87;
  margin-bottom: 5px;
}
.stat-label {
  font-size: clamp(12px, 1.5vw, 14px);
  color: #2A1B3D;
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
  border: 1px solid rgba(216, 63, 135, 0.1);
  border-radius: 20px;
  text-decoration: none;
  color: #4A2C40;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
.female-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  z-index: 1;
}
.female-card > * {
  z-index: 2;
  position: relative;
}
.female-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(216, 63, 135, 0.15);
}
.card-icon {
  font-size: 48px;
  color: #D83F87;
  margin-bottom: 20px;
  text-align: center;
}
.health-overview {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  max-width: 1200px;
  margin: 40px auto 40px;
  box-shadow: 0 4px 20px rgba(42, 27, 61, 0.12);
}
.overview-title {
  color: #2A1B3D;
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
  text-align: center;
}
.image-overlay h3 {
  color: #fff;
  font-size: clamp(24px, 3vw, 36px);
  margin-bottom: 12px;
  font-weight: 700;
  -webkit-text-stroke: 1px rgba(0, 0, 0, 0.5);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  max-width: 85%;
  line-height: 1.3;
}
.image-overlay p {
  color: #fff;
  font-size: clamp(16px, 1.8vw, 22px);
  line-height: 1.5;
  -webkit-text-stroke: 0.5px rgba(0, 0, 0, 0.5);
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
  max-width: 85%;
  font-weight: 500;
}
.image-overlay h4 {
  color: #fff;
  font-size: clamp(22px, 2.5vw, 32px);
  margin-bottom: 12px;
  font-weight: 600;
  -webkit-text-stroke: 0.8px rgba(0, 0, 0, 0.5);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  max-width: 90%;
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
  background-color: rgba(216, 63, 135, 0.05);
  transition: all 0.3s ease;
}
.mood-item:hover {
  background-color: rgba(216, 63, 135, 0.1);
}
.mood-item.selected {
  background-color: rgba(216, 63, 135, 0.1);
}
.mood-icon {
  font-size: 24px;
  color: #D83F87;
  margin-bottom: 5px;
}
.mood-label {
  font-size: clamp(12px, 1.5vw, 14px);
  color: #2A1B3D;
}
.mood-submit {
  margin-top: 20px;
}
.female-button {
  padding: 10px 20px;
  background-color: #D83F87;
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
  background: linear-gradient(135deg, #fff 0%, #F5FAF7 100%);
  border: 1px solid rgba(68, 49, 141, 0.1);
  border-radius: 20px;
  padding: 30px;
  max-width: 1200px;
  margin: 40px auto 40px;
  box-shadow: 0 4px 20px rgba(42, 27, 61, 0.12);
}
.tips-title {
  color: #2A1B3D;
  font-size: clamp(18px, 2.5vw, 22px);
  margin-bottom: 25px;
  text-align: center;
}
.tip-card {
  background: linear-gradient(135deg, rgba(216, 63, 135, 0.05) 0%, rgba(68, 49, 141, 0.05) 100%);
  border: 1px solid rgba(216, 63, 135, 0.1);
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}
.tip-card:hover {
  background: linear-gradient(135deg, rgba(216, 63, 135, 0.1) 0%, rgba(68, 49, 141, 0.1) 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(216, 63, 135, 0.15);
}
.tip-card h4 {
  color: #2A1B3D;
  margin-top: 0;
  margin-bottom: 10px;
  font-size: clamp(16px, 2vw, 18px);
}
.tip-card p {
  color: #666;
  margin: 0;
  font-size: clamp(14px, 1.5vw, 16px);
}

/* Styles for Mood History Calendar Section */
.mood-calendar-section {
  margin-top: 40px;
}

/* Fade-in Animation Styles */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

.fade-in.is-visible {
  opacity: 1 !important;
  transform: translateY(0) !important;
}

.calendar-container {
  position: relative;
  height: 500px;
}

/* Custom styles for mood events in calendar */
.cv-item.mood-event {
  border-radius: 4px;
  padding: 2px 5px;
  font-size: 0.8rem;
  color: white;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Example: Styling based on mood */
.cv-item.mood-happy {
  background-color: #FFD700;
}

.cv-item.mood-sad {
  background-color: #87CEEB;
}

.cv-item.mood-excited {
  background-color: #FF6B6B;
}

.cv-item.mood-calm {
  background-color: #98FB98;
}

.cv-item.mood-frustrated {
  background-color: #FF4500;
}

.cv-item.mood-tired {
  background-color: #9370DB;
}

.cv-item.mood-badmood {
  background-color: #4682B4;
}

.cv-item.mood-relax {
  background-color: #20B2AA;
}

.cv-item.mood-fun {
  background-color: #FF69B4;
}

/* Styles for day content to show mood icons */
.cv-day .day-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
}

.cv-day .day-number {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 5px;
}

.cv-day .mood-icons {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  justify-content: center;
}

.cv-day .mood-icons i {
  font-size: 0.9em;
}

.cv-day .mood-icons i.mood-happy { color: #FFD700; }
.cv-day .mood-icons i.mood-sad { color: #87CEEB; }
.cv-day .mood-icons i.mood-excited { color: #FF6B6B; }
.cv-day .mood-icons i.mood-calm { color: #98FB98; }
.cv-day .mood-icons i.mood-frustrated { color: #FF4500; }
.cv-day .mood-icons i.mood-tired { color: #9370DB; }
.cv-day .mood-icons i.mood-badmood { color: #4682B4; }
.cv-day .mood-icons i.mood-relax { color: #20B2AA; }
.cv-day .mood-icons i.mood-fun { color: #FF69B4; }

/* Hide the default event rendering in the calendar cells */
.cv-day .cv-item {
  display: none;
}

/* Style for selected date */
.cv-day .day-content.selected-date {
  background-color: rgba(216, 63, 135, 0.2);
  border: 2px solid #D83F87;
  border-radius: 8px;
}

/* Style for clear button */
.mood-submit .clear-button {
  background-color: #A4B3B6;
  margin-left: 10px;
}

.mood-submit .clear-button:hover {
  background-color: #93a2a4;
}

/* Custom calendar header styles */
.calendar-header-custom {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  font-size: 1.2rem;
  color: #4A2C40;
}

.calendar-header-custom button {
  background: none;
  border: 1px solid #ccc;
  padding: 5px 10px;
  margin: 0 5px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.calendar-header-custom button:hover {
  background-color: #f0f0f0;
}

.calendar-header-custom span {
  font-weight: bold;
  margin: 0 10px;
}

/* Define background images for each card */
.heart-rate-card {
  background-image: url('@/assets/images/heart rate.jpg'); /* Replace with your image path */
}

.temperature-card {
  background-image: url('@/assets/images/temperature.jpg'); /* Replace with your image path */
}

.menstrual-card {
  background-image: url('@/assets/images/menstrual.jpg'); /* Replace with your image path */
}

.female-card:hover::before {
  background-color: rgba(255, 255, 255, 0.4); /* Less opaque overlay on hover */
}

/* 使用指南样式 */
.user-guide {
  margin-top: 40px;
  background: linear-gradient(135deg, #fff 0%, #FFF5F7 100%);
}

.guide-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px;
}

.guide-section {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(42, 27, 61, 0.08);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.guide-section:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(216, 63, 135, 0.15);
  background: rgba(255, 255, 255, 0.95);
}

.guide-section h4 {
  color: #2A1B3D;
  font-size: 1.2rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(216, 63, 135, 0.1);
}

.guide-section h4 i {
  color: #D83F87;
  font-size: 1.4rem;
}

.guide-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}

.guide-section ul li {
  color: #666;
  margin-bottom: 12px;
  padding-left: 24px;
  position: relative;
  line-height: 1.6;
  font-size: 0.95rem;
}

.guide-section ul li:before {
  content: "•";
  color: #D83F87;
  position: absolute;
  left: 0;
  font-size: 1.2em;
}

.guide-section ul li:last-child {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .guide-content {
    grid-template-columns: 1fr;
  }
  
  .guide-section {
    margin-bottom: 15px;
  }
}
</style> 
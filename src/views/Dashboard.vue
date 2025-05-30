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
    <div class="health-overview">
      <h3 class="overview-title"><i class="ri-emotion-happy-line"></i>Record Mood</h3>
      <div class="image-container">
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
    <div class="mood-calendar-section health-overview">
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
        { id: 'sad', label: 'Sad', icon: 'ri-emotion-sad-line', color: 'mood-sad' },
        { id: 'excited', label: 'Excited', icon: 'ri-emotion-laugh-line', color: 'mood-excited' },
        { id: 'calm', label: 'Calm', icon: 'ri-emotion-normal-line', color: 'mood-calm' },
        { id: 'frustrated', label: 'Frustrated', icon: 'ri-emotion-unhappy-line', color: 'mood-frustrated' },
        { id: 'tired', label: 'Tired', icon: 'ri-emotion-line', color: 'mood-tired' },
        { id: 'badmood', label: 'Low', icon: 'ri-emotion-2-line', color: 'mood-badmood' },
        { id: 'relax', label: 'Relaxed', icon: 'ri-emotion-line', color: 'mood-relax' },
        { id: 'fun', label: 'Fun', icon: 'ri-emotion-laugh-line', color: 'mood-fun' }
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
  },
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
  background: linear-gradient(135deg, #fff 0%, #FFF5F7 100%);
  border-radius: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 50px;
  box-shadow: 0 4px 20px rgba(156, 91, 128, 0.12);
  border: 1px solid rgba(229, 124, 159, 0.1);
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
  background: linear-gradient(135deg, rgba(229, 124, 159, 0.05) 0%, rgba(126, 184, 162, 0.05) 100%);
  transition: all 0.3s ease;
  border: 1px solid rgba(229, 124, 159, 0.1);
}
.stat-item:hover {
  background: linear-gradient(135deg, rgba(229, 124, 159, 0.1) 0%, rgba(126, 184, 162, 0.1) 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(229, 124, 159, 0.15);
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
  border: 1px solid rgba(229, 124, 159, 0.1);
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
  box-shadow: 0 8px 30px rgba(229, 124, 159, 0.15);
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
  background: linear-gradient(135deg, #fff 0%, #F5FAF7 100%);
  border: 1px solid rgba(126, 184, 162, 0.1);
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
  background: linear-gradient(135deg, rgba(229, 124, 159, 0.05) 0%, rgba(126, 184, 162, 0.05) 100%);
  border: 1px solid rgba(229, 124, 159, 0.1);
  border-radius: 15px;
  padding: 20px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}
.tip-card:hover {
  background: linear-gradient(135deg, rgba(229, 124, 159, 0.1) 0%, rgba(126, 184, 162, 0.1) 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(229, 124, 159, 0.15);
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

/* Styles for Mood History Calendar Section */
.mood-calendar-section {
  margin-top: 40px;
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
  background-color: #a8e6cf;
}

.cv-item.mood-sad {
  background-color: #ffaaa5;
}

.cv-item.mood-excited {
  background-color: #ffd3b6;
}

.cv-item.mood-calm {
  background-color: #a2b9bc;
}

.cv-item.mood-frustrated {
  background-color: #ff8b94;
}

.cv-item.mood-tired {
  background-color: #bae1ff;
}

.cv-item.mood-badmood {
  background-color: #c23b22;
}

.cv-item.mood-relax {
  background-color: #77dd77;
}

.cv-item.mood-fun {
  background-color: #fdfd96;
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

.cv-day .mood-icons i.mood-happy { color: #a8e6cf; }
.cv-day .mood-icons i.mood-sad { color: #ffaaa5; }
.cv-day .mood-icons i.mood-excited { color: #ffd3b6; }
.cv-day .mood-icons i.mood-calm { color: #a2b9bc; }
.cv-day .mood-icons i.mood-frustrated { color: #ff8b94; }
.cv-day .mood-icons i.mood-tired { color: #bae1ff; }
.cv-day .mood-icons i.mood-badmood { color: #c23b22; }
.cv-day .mood-icons i.mood-relax { color: #77dd77; }
.cv-day .mood-icons i.mood-fun { color: #fdfd96; }

/* Hide the default event rendering in the calendar cells */
.cv-day .cv-item {
  display: none;
}

/* Style for selected date */
.cv-day .day-content.selected-date {
  background-color: rgba(156, 91, 128, 0.2); /* Highlight with a light background color */
  border: 2px solid #9C5B80; /* Add a border */
  border-radius: 8px;
}

/* Style for clear button */
.mood-submit .clear-button {
  background-color: #a2b9bc; /* Grey color */
  margin-left: 10px;
}

.mood-submit .clear-button:hover {
  background-color: #8d9a9c; /* Darker grey on hover */
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
</style> 
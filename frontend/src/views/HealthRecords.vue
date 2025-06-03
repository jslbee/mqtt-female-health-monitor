<template>
  <div>
    <NavBar />
    <div class="health-records">
      <h1>Team Members</h1>
      
      <!-- 团队成员部分 -->
      <div class="team-section">
        <div class="team-grid">
          <div v-for="(member, index) in teamMembers" :key="index" class="member-card">
            <img :src="member.avatar" :alt="member.name" class="member-avatar" />
            <div class="member-info">
              <h3>{{ member.name }}</h3>
              <p>{{ member.role }}</p>
              <p>Student ID: {{ member.studentId }}</p>
              <p v-if="member.email" class="email">{{ member.email }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  name: 'TeamMembers',
  components: { NavBar },
  data() {
    return {
      teamMembers: [
        {
          name: 'Jieying Shen',
          role: 'Group Leader – Back-End Development & Server Connection',
          studentId: '2202329013036N',
          email: 'shenj36@coventry.ac.uk',
          avatar: new URL('../assets/team/Jieying Shen.jpg', import.meta.url).href
        },
        {
          name: 'Xinyu Wu',
          role: 'Team Member – Front-End Development & Front-Back End Integration',
          studentId: '202329013083N',
          email: 'wux78@coventry.ac.uk',
          avatar: new URL('../assets/team/Xinyu Wu.jpg', import.meta.url).href
        },
        {
          name: 'Xingyu Luo',
          role: 'Team Member – Back-End Database Setup & Data Generation',
          studentId: '202329013038N',
          email: 'luox18@coventry.ac.uk',
          avatar: new URL('../assets/team/Xingyu Luo1.jpg', import.meta.url).href
        },
        {
          name: 'Xinyue Li',
          role: 'Team Member– Back-End Database setup&  MQTT Database Connectivity',
          studentId: '202329013005N',
          email: 'lix211@coventry.ac.uk',
          avatar: new URL('../assets/team/Xinyue Li.jpg', import.meta.url).href
        },
        {
          name: 'He Ji',
          role: 'Team member – MQTT heart rate part & Prediction model',
          studentId: '202329013002N',
          email: 'jih3@coventry.ac.uk',
          avatar: new URL('../assets/team/He Ji.jpg', import.meta.url).href
        }
      ],
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
  text-transform: uppercase;
  letter-spacing: 2px;
}

.team-section {
  margin-bottom: 2rem;
  background: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 24px rgba(156, 91, 128, 0.12);
}

.team-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
}

@media (max-width: 768px) {
}

.member-card {
  flex: 0 1 300px;
  max-width: calc(33.33% - 1.5rem);
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(156, 91, 128, 0.1);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  will-change: transform;
}

@media (max-width: 1024px) {
  .member-card {
    max-width: calc(50% - 1.5rem);
  }
}

@media (max-width: 768px) {
  .member-card {
    max-width: 100%;
  }
}

.member-card:hover {
  transform: translateY(-5px);
}

.member-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 1rem;
  border: 4px solid #9C5B80;
  padding: 4px;
  background: #fff;
  object-fit: cover;
}

.member-info h3 {
  color: #9C5B80;
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.member-info p {
  color: #666;
  font-size: 1rem;
  margin-bottom: 0.3rem;
  line-height: 1.4;
}

.member-info .email {
  color: #9C5B80;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  word-break: break-all;
}
</style> 
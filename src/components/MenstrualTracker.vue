<template>
  <div class="menstrual-tracker">
    <div class="card">
      <h2>经期记录</h2>
      <div class="calendar-container">
        <div class="calendar-header">
          <button class="btn" @click="previousMonth">上个月</button>
          <h3>{{ currentMonthYear }}</h3>
          <button class="btn" @click="nextMonth">下个月</button>
        </div>
        <div class="calendar-grid">
          <div v-for="day in weekDays" :key="day" class="calendar-day-header">{{ day }}</div>
          <div 
            v-for="day in calendarDays" 
            :key="day.date"
            :class="['calendar-day', {
              'other-month': !day.currentMonth,
              'menstrual': day.isMenstrual,
              'fertile': day.isFertile,
              'ovulation': day.isOvulation
            }]"
            @click="toggleDayStatus(day)"
          >
            {{ day.dayOfMonth }}
            <div class="day-indicator" v-if="day.isMenstrual || day.isFertile || day.isOvulation"></div>
          </div>
        </div>
      </div>
      <div class="legend">
        <div class="legend-item">
          <span class="legend-color menstrual"></span>
          <span>经期</span>
        </div>
        <div class="legend-item">
          <span class="legend-color fertile"></span>
          <span>易受孕期</span>
        </div>
        <div class="legend-item">
          <span class="legend-color ovulation"></span>
          <span>排卵日</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'MenstrualTracker',
  setup() {
    const currentDate = ref(new Date())
    const weekDays = ['日', '一', '二', '三', '四', '五', '六']
    
    const currentMonthYear = computed(() => {
      return currentDate.value.toLocaleDateString('zh-CN', { 
        year: 'numeric', 
        month: 'long' 
      })
    })

    const calendarDays = computed(() => {
      const year = currentDate.value.getFullYear()
      const month = currentDate.value.getMonth()
      
      const firstDay = new Date(year, month, 1)
      const lastDay = new Date(year, month + 1, 0)
      
      const days = []
      
      // 添加上个月的天数
      const firstDayWeekday = firstDay.getDay()
      for (let i = firstDayWeekday - 1; i >= 0; i--) {
        const date = new Date(year, month, -i)
        days.push({
          date: date.toISOString(),
          dayOfMonth: date.getDate(),
          currentMonth: false,
          isMenstrual: false,
          isFertile: false,
          isOvulation: false
        })
      }
      
      // 添加当前月的天数
      for (let i = 1; i <= lastDay.getDate(); i++) {
        const date = new Date(year, month, i)
        days.push({
          date: date.toISOString(),
          dayOfMonth: i,
          currentMonth: true,
          isMenstrual: false,
          isFertile: false,
          isOvulation: false
        })
      }
      
      // 添加下个月的天数
      const remainingDays = 42 - days.length
      for (let i = 1; i <= remainingDays; i++) {
        const date = new Date(year, month + 1, i)
        days.push({
          date: date.toISOString(),
          dayOfMonth: date.getDate(),
          currentMonth: false,
          isMenstrual: false,
          isFertile: false,
          isOvulation: false
        })
      }
      
      return days
    })

    const previousMonth = () => {
      currentDate.value = new Date(
        currentDate.value.getFullYear(),
        currentDate.value.getMonth() - 1,
        1
      )
    }

    const nextMonth = () => {
      currentDate.value = new Date(
        currentDate.value.getFullYear(),
        currentDate.value.getMonth() + 1,
        1
      )
    }

    const toggleDayStatus = (day) => {
      if (!day.currentMonth) return
      
      // 这里可以添加状态切换逻辑
      day.isMenstrual = !day.isMenstrual
      // 可以在这里添加其他状态的计算逻辑
    }

    return {
      currentMonthYear,
      weekDays,
      calendarDays,
      previousMonth,
      nextMonth,
      toggleDayStatus
    }
  }
}
</script>

<style scoped>
.menstrual-tracker {
  padding: 20px;
}

.calendar-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.calendar-day-header {
  text-align: center;
  font-weight: bold;
  padding: 10px;
}

.calendar-day {
  position: relative;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
  transition: var(--transition);
}

.calendar-day:hover {
  background-color: var(--secondary-color);
}

.other-month {
  opacity: 0.5;
}

.menstrual {
  background-color: rgba(229, 124, 159, 0.2);
}

.fertile {
  background-color: rgba(248, 187, 208, 0.2);
}

.ovulation {
  background-color: rgba(255, 192, 203, 0.2);
}

.legend {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 4px;
}

.legend-color.menstrual {
  background-color: rgba(229, 124, 159, 0.2);
}

.legend-color.fertile {
  background-color: rgba(248, 187, 208, 0.2);
}

.legend-color.ovulation {
  background-color: rgba(255, 192, 203, 0.2);
}
</style> 
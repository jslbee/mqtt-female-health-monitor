
# Artemis – Female Health Monitoring System

**Artemis** is a lightweight, modular, and privacy-conscious health monitoring platform tailored for female users. It integrates real-time physiological data collection, menstrual cycle tracking and prediction, and intuitive data visualization into one unified system.

> 🖥️ **Live Demo**: [http://120.76.249.191/](http://120.76.249.191/)

---

## 🌟 Features

- 🔄 **MQTT-based data transmission** for real-time, lightweight sensor communication  
- 📊 **Menstrual cycle prediction engine** based on personal data and time series logic  
- 📈 **Visual health dashboard** built with Vue 3 and ECharts  
- 🔐 **Privacy-first architecture**, ensuring data is processed and visualized securely  
- 🧩 Modular and extensible system design  

---

## 🛠️ Tech Stack

- **Frontend**: Vue 3, Vite, ECharts  
- **Backend**: FastAPI (Python)  
- **Database**: MySQL  
- **Protocol**: MQTT  
- **Deployment**: Nginx on Ubuntu VPS  

---

## 📂 Project Structure

```

Artemis/
├── frontend/              # Vue3 + Vite frontend
├── backend/               # FastAPI backend with RESTful APIs
├── mqtt/                  # MQTT client and data simulation scripts
├── database/              # MySQL schema and sample data
└── docs/                  # Documentation and reports

````

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js and npm
- MySQL 8+
- MQTT broker (e.g. Mosquitto)

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
````

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. MQTT Data Simulation (Optional)

```bash
cd mqtt
python simulate_sensor.py
```

---

## 💡 Purpose & Impact

**Artemis** was born from the need to provide accessible and respectful health monitoring tools for women—especially students and individuals who lack access to traditional healthcare support.

By combining open-source technologies with thoughtful UX design, Artemis empowers users to better understand and anticipate their physical and emotional states. Our goal is to reduce anxiety, improve awareness, and build tools that center care and equity.

This project is submitted as part of a national innovation competition.

---

## 👨‍💻 Team

We are a group of undergraduate students passionate about AI, healthcare technology, and human-centered design.
Feedback and contributions are welcome!

---

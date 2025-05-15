from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from datetime import datetime, timedelta

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zaq13910975598',  # 请修改为您的MySQL密码
    'database': 'health_data'
}

@app.get("/api/heart-rate")
async def get_heart_rate():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 获取最近24小时的数据
        time_threshold = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            SELECT time_received, heart_rate, health_status 
            FROM heart_rate_data 
            WHERE time_received > %s 
            ORDER BY time_received ASC
        ''', (time_threshold,))
        data = cursor.fetchall()
        
        # 计算统计数据
        if data:
            heart_rates = [item['heart_rate'] for item in data]
            stats = {
                'average': round(sum(heart_rates) / len(heart_rates), 1),
                'min': min(heart_rates),
                'max': max(heart_rates)
            }
        else:
            stats = {'average': 0, 'min': 0, 'max': 0}
        
        return {
            "data": data,
            "stats": stats
        }
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

@app.get("/api/temperature")
async def get_temperature():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 获取最近24小时的数据
        time_threshold = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            SELECT time_received, value, warning, trend 
            FROM temperature_data 
            WHERE time_received > %s 
            ORDER BY time_received ASC
        ''', (time_threshold,))
        data = cursor.fetchall()
        
        return {"data": data}
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
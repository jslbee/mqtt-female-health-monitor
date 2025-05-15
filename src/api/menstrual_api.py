from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime, timedelta
from pydantic import BaseModel

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class PredictionRequest(BaseModel):
    client_id: str
    last_period_date: str

# 加载数据
try:
    df = pd.read_excel("WashedFedCycleData.xlsx")
    df_clean = df.dropna(subset=["LengthofCycle"])
    df_clean["LengthofCycle"] = df_clean["LengthofCycle"].astype(int)
    avg_cycle_df = df_clean.groupby("ClientID")["LengthofCycle"].mean().reset_index()
    avg_cycle_df.rename(columns={"LengthofCycle": "AvgCycleLength"}, inplace=True)
except Exception as e:
    print(f"Error loading data: {e}")

@app.post("/api/predict")
async def predict_next_period(request: PredictionRequest):
    try:
        match = avg_cycle_df[avg_cycle_df["ClientID"] == request.client_id]
        if match.empty:
            raise HTTPException(status_code=404, detail=f"User {request.client_id} not found")

        avg_cycle = match["AvgCycleLength"].values[0]
        last_period_date = datetime.strptime(request.last_period_date, "%Y-%m-%d")
        next_period_date = last_period_date + timedelta(days=round(avg_cycle))

        return {
            "client_id": request.client_id,
            "predicted_date": next_period_date.date().isoformat(),
            "average_cycle": round(avg_cycle),
            "message": f"预测的下一次月经开始日期是 {next_period_date.date()}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
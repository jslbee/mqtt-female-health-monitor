import pandas as pd
from datetime import datetime, timedelta
import os

# Load data
BASE_DIR = os.path.dirname(__file__)  # 当前文件所在目录：app/
file_path = os.path.join(BASE_DIR, "data", "WashedFedCycleData.xlsx")

df = pd.read_excel(file_path)

# Data cleaning: Remove records of non periodic data
df_clean = df.dropna(subset=["LengthofCycle"])
df_clean["LengthofCycle"] = df_clean["LengthofCycle"].astype(int)

# Calculate the average cycle of each user
avg_cycle_df = df_clean.groupby("ClientID")["LengthofCycle"].mean().reset_index()
avg_cycle_df.rename(columns={"LengthofCycle": "AvgCycleLength"}, inplace=True)

# Main prediction function
def predict_next_period(client_id, last_period_date_str):
    """
    input：
        client_id(such as 'nfp8122')
        last_period_date_str: (format 'YYYY-MM-DD')
    output：
        predict result of the prediction in string
    """
    match = avg_cycle_df[avg_cycle_df["ClientID"] == client_id]
    if match.empty:
        return f"Not Found The Data of client {client_id}!"

    avg_cycle = match["AvgCycleLength"].values[0]
    last_period_date = datetime.strptime(last_period_date_str, "%Y-%m-%d")
    next_period_date = last_period_date + timedelta(days=round(avg_cycle))

    return f"The predicted start date of the next menstrual cycle for you is {next_period_date.date()}(with an average cycle of approximately {round(avg_cycle)} days)_"

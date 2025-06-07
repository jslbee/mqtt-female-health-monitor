import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random
import time

# 初始化数据
x_data = []
y_data = []

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot_date([], [], linestyle='solid', marker=None)

# 设置图表样式
ax.set_title("Real-time Heart-rate Visualization")
ax.set_xlabel("Time (last 60 seconds)")
ax.set_ylabel("Heart-rate (bpm)")
ax.set_ylim(50, 100)  # 固定 Y 轴范围
ax.grid(True)

# 设置时间格式与刻度控制
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax.xaxis.set_major_locator(mdates.SecondLocator(bysecond=[0, 30]))  # 每 30 秒一个刻度

for _ in range(200):  # 控制采样次数
    now = datetime.now()
    pulse = random.randint(60, 100)

    x_data.append(now)
    y_data.append(pulse)

    # 设置 X 轴范围为最近 60 秒
    time_window_start = now - timedelta(seconds=60)
    ax.set_xlim(time_window_start, now)

    # 过滤出 60 秒内的数据进行绘制
    x_display = [x for x in x_data if x >= time_window_start]
    y_display = y_data[-len(x_display):]

    line.set_data(x_display, y_display)

    fig.autofmt_xdate()
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(3)  # 每 3 秒更新一次

plt.ioff()
plt.show()

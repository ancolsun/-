import tkinter as tk
from tkinter import ttk
import datetime
import math

# 中国主要城市及其经度（可扩展）
cities = {
    "北京": 116.4,
    "上海": 121.5,
    "广州": 113.3,
    "重庆": 106.5,
    "武汉": 114.1,
    "天津": 117.2,
    "西安": 108.9,
    "成都": 104.1,
}

def update_time():
    # 获取当前选中的城市
    city = city_var.get()
    longitude = cities.get(city, 116.4)  # 默认北京

    # 获取当前时间
    now = datetime.datetime.now()

    # 计算北京时间
    beijing_time = now.strftime("%H:%M:%S")

    # 计算平太阳时
    time_diff = (longitude - 120) * 4 / 60  # 每度经度差4分钟，转换为小时
    mean_solar_time = now + datetime.timedelta(hours=time_diff)
    mean_solar_time_str = mean_solar_time.strftime("%H:%M:%S")

    # 计算真太阳时（简化版时差方程）
    day_of_year = now.timetuple().tm_yday
    eot = 9.87 * math.sin(2 * math.pi * day_of_year / 365) - 7.53 * math.cos(math.pi * day_of_year / 365) - 1.5 * math.sin(math.pi * day_of_year / 365)
    true_solar_time = mean_solar_time + datetime.timedelta(minutes=eot)
    true_solar_time_str = true_solar_time.strftime("%H:%M:%S")

    # 更新显示
    true_solar_label.config(text=true_solar_time_str)
    mean_solar_label.config(text=f"平太阳时: {mean_solar_time_str}")
    beijing_label.config(text=f"北京时间: {beijing_time}")

    # 每秒更新
    root.after(1000, update_time)

# 创建主窗口
root = tk.Tk()
root.title("真太阳时展示")
root.geometry("500x300")

# 创建真太阳时显示区域
true_solar_frame = tk.Frame(root, bg="#007aff")  # 蓝色背景
true_solar_frame.pack(pady=20)
true_solar_label = tk.Label(true_solar_frame, text="00:00:00", font=("Helvetica", 36), fg="white", bg="#007aff")
true_solar_label.pack(padx=20, pady=10)

# 创建平太阳时和北京时间显示区域
other_time_frame = tk.Frame(root)
other_time_frame.pack(pady=10)
mean_solar_label = tk.Label(other_time_frame, text="平太阳时: 00:00:00", font=("Helvetica", 18))
mean_solar_label.pack(side="left", padx=20)
beijing_label = tk.Label(other_time_frame, text="北京时间: 00:00:00", font=("Helvetica", 18))
beijing_label.pack(side="right", padx=20)

# 创建城市选择下拉菜单
city_var = tk.StringVar()
city_combobox = ttk.Combobox(root, textvariable=city_var, values=list(cities.keys()))
city_combobox.set("北京")  # 默认选择北京
city_combobox.pack(pady=20)

# 启动时间更新
update_time()

# 运行主循环
root.mainloop()
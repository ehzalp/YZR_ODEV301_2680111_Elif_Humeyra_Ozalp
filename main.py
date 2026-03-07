import numpy as np
import matplotlib.pyplot as plt
from robot import MobileRobot
from controller import PIDController
from utils import calculate_metrics

# Parametreler
DT = 0.01
T_FINAL = 40.0
t_axis = np.arange(0, T_FINAL, DT)

def run_simulation(kp, ki, kd, scenario="normal"):
    robot = MobileRobot()
    pid = PIDController(kp, ki, kd, DT)
    
    v_history = []
    ref_history = []
    v_ref = 1.0
    
    for t in t_axis:
        # Senaryo: Referans Değişimi
        if scenario == "ref_change" and t >= 20.0:
            v_ref = 2.0
            
        # Senaryo: Bozucu Etki (t=15'te 10 Newtonluk rüzgar)
        dist = 10.0 if (scenario == "disturbance" and 15.0 <= t <= 15.5) else 0.0
        
        u = pid.compute(v_ref, robot.v)
        v = robot.step(u, DT, disturbance=dist)
        
        v_history.append(v)
        ref_history.append(v_ref)
        
    return np.array(v_history), np.array(ref_history)

# --- 1. Adım: PID Karşılaştırma ---
v_p, _ = run_simulation(10.0, 0.0, 0.0)
v_pi, _ = run_simulation(10.0, 5.0, 0.0)
v_pid, v_ref_ax = run_simulation(15.0, 10.0, 2.0)

plt.figure(figsize=(10,5))
plt.plot(t_axis, v_p, label='Sadece P')
plt.plot(t_axis, v_pi, label='PI')
plt.plot(t_axis, v_pid, label='PID')
plt.plot(t_axis, v_ref_ax, 'k--', label='Referans')
plt.title("Kontrolör Karşılaştırmaları")
plt.legend(); plt.grid(); plt.show()

# --- 2. Adım: Bozucu Analizi ---
v_dist, v_ref_dist = run_simulation(15.0, 10.0, 2.0, scenario="disturbance")
plt.figure(figsize=(10,5))
plt.plot(t_axis, v_dist, color='orange', label='PID (Bozucu Altında)')
plt.axvspan(15, 15.5, color='red', alpha=0.1, label='Bozucu Aralığı')
plt.title("Bozucu Etki ve Toparlanma")
plt.legend(); plt.grid(); plt.show()

metrics = calculate_metrics(t_axis, v_pid, 1.0)
print("PID Performans Metrikleri:", metrics)
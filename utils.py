import numpy as np

def calculate_metrics(t, v, v_ref, start_idx=0):
    # Dilimleme ve sadece ilgili bölümü kullanma
    t_slice = t[start_idx:]
    v_slice = v[start_idx:]
    
    # 1. Kalıcı Durum Hatası
    ess = abs(v_ref - v_slice[-1])
    
    # 2. Maksimum Aşım (Overshoot)
    max_v = max(v_slice)
    overshoot = ((max_v - v_ref) / v_ref) * 100 if max_v > v_ref else 0
    
    # 3. Yerleşme Süresi (%5 tolerans)
    tolerance = 0.05 * v_ref
    within_tolerance = np.abs(v_slice - v_ref) <= tolerance
    indices = np.where(~within_tolerance)[0]
    ts = t_slice[indices[-1]] - t_slice[0] if len(indices) > 0 else 0
    
    return {"Ess": ess, "Overshoot (%)": overshoot, "Settling Time (s)": ts}
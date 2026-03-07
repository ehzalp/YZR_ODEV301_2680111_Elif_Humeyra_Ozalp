class MobileRobot:
    def __init__(self, m=5.0, b=0.8):
        self.m = m  # Kütle (kg)
        self.b = b  # Sürtünme katsayısı (Ns/m)
        self.v = 0.0  # Başlangıç hızı (m/s)

    def step(self, u, dt, disturbance=0.0):
        # Diferansiyel Denklem: dv/dt = (u - b*v) / m
        # Euler Entegrasyonu: v_yeni = v_eski + (dv/dt * dt)
        dvdt = (u + disturbance - self.b * self.v) / self.m
        self.v += dvdt * dt
        return self.v
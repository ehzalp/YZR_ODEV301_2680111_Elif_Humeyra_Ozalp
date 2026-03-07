class PIDController:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, setpoint, measurement):
        error = setpoint - measurement
        
        # P terimi
        p_out = self.kp * error
        
        # I terimi
        self.integral += error * self.dt
        i_out = self.ki * self.integral
        
        # D terimi
        derivative = (error - self.prev_error) / self.dt
        d_out = self.kd * derivative
        
        self.prev_error = error
        return p_out + i_out + d_out
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz

# Time parameters
t = np.linspace(0, 10, 1000)
dt = t[1] - t[0]

# Parameters
alpha = 1.2
beta = 0.7
I_max = 1.0
theta = 1.5

# Simulated information flow I(t) (e.g., oscillating + noise)
I_t = 0.5 + 0.3 * np.sin(2 * np.pi * 0.8 * t) + 0.05 * np.random.randn(len(t))

# Metastability function M(t)
dI_dt = np.gradient(I_t, dt)
M_t = np.abs(dI_dt) * (1 - I_t / I_max)

# Coordination dynamics C(t) via numerical integration
C_t = np.zeros_like(t)
for i in range(1, len(t)):
    dC = alpha * I_t[i] * M_t[i] - beta * C_t[i-1]
    C_t[i] = C_t[i-1] + dC * dt

# Qualia function Q(t): smoothed integral of C(t) over time
Q_t = cumtrapz(C_t, t, initial=0)

# Qualia activation (1 if Q ≥ θ, else 0)
qualia_active = Q_t >= theta

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(4, 1, 1)
plt.plot(t, I_t, label='Information I(t)')
plt.ylabel('I(t)')
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(t, M_t, label='Metastability M(t)', color='orange')
plt.ylabel('M(t)')
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(t, C_t, label='Coordination Dynamics C(t)', color='green')
plt.ylabel('C(t)')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(t, Q_t, label='Qualia Potential Q(t)', color='red')
plt.axhline(theta, color='gray', linestyle='--', label='Qualia Threshold θ')
plt.fill_between(t, 0, Q_t, where=qualia_active, color='red', alpha=0.3, label='Qualia Active')
plt.xlabel('Time (t)')
plt.ylabel('Q(t)')
plt.legend()

plt.tight_layout()
plt.show()

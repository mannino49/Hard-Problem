# qualia_dynamics_visualization.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.ndimage import gaussian_filter1d
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# 1. Generate synthetic data
t = np.linspace(0, 10, 1000)
dt = t[1] - t[0]
alpha = 1.2
beta = 0.7
I_max = 1.0
theta = 1.5

# Simulate I(t) with noise + sinusoid
np.random.seed(0)
I_t = 0.5 + 0.3 * np.sin(2 * np.pi * 0.8 * t) + 0.05 * np.random.randn(len(t))
dI_dt = np.gradient(I_t, dt)
M_t = np.abs(dI_dt) * (1 - I_t / I_max)

# Compute C(t)
C_t = np.zeros_like(t)
for i in range(1, len(t)):
    dC = alpha * I_t[i] * M_t[i] - beta * C_t[i-1]
    C_t[i] = C_t[i-1] + dC * dt

# Compute Q(t)
Q_t = integrate.cumulative_trapezoid(C_t, t, initial=0)
qualia_active = Q_t >= theta

# Smooth values
I_smooth = gaussian_filter1d(I_t, sigma=5)
M_smooth = gaussian_filter1d(M_t, sigma=5)
C_smooth = gaussian_filter1d(C_t, sigma=5)

# 2. Plot Phase Space Projection
plt.figure(figsize=(8, 6))
plt.plot(I_smooth, C_smooth, lw=2, color='darkgreen')
plt.xlabel("Information I(t)")
plt.ylabel("Coordination C(t)")
plt.title("Phase Space: C(t) vs I(t)")
plt.grid(True)
plt.tight_layout()
plt.savefig("phase_space_projection.png")
plt.show()

# 3. Smoothed 3D Attractor
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(I_smooth, M_smooth, C_smooth, color='blue', lw=1.5)
ax.set_xlabel('Information I(t)')
ax.set_ylabel('Metastability M(t)')
ax.set_zlabel('Coordination C(t)')
ax.set_title('Smoothed 3D Attractor')
plt.tight_layout()
plt.savefig("3d_attractor.png")
plt.show()

# 4. Animate the Trajectory
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

line, = ax.plot([], [], [], color='blue', lw=2)
ax.set_xlim(np.min(I_smooth), np.max(I_smooth))
ax.set_ylim(np.min(M_smooth), np.max(M_smooth))
ax.set_zlim(np.min(C_smooth), np.max(C_smooth))
ax.set_xlabel('Information I(t)')
ax.set_ylabel('Metastability M(t)')
ax.set_zlabel('Coordination C(t)')
ax.set_title('Animated Metastable Trajectory')

def update(num):
    line.set_data(I_smooth[:num], M_smooth[:num])
    line.set_3d_properties(C_smooth[:num])
    return line,

ani = animation.FuncAnimation(fig, update, frames=500, interval=20, blit=True)

# Save the animation as GIF instead of MP4
ani.save("metastable_trajectory_animation.gif", writer='pillow', fps=15)

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize

# Set random seed for reproducibility
np.random.seed(42)

# Time parameters
t = np.linspace(0, 20, 2000)  # Extended time range for better dynamics exploration
dt = t[1] - t[0]

# Parameters
alpha = 0.6  # Coupling strength between information and metastability
beta = 0.3   # Decay rate of coordination dynamics
I_max = 0.8  # Maximum information capacity
theta = 0.8  # Qualia threshold

# Simulated information flow I(t) with multiple frequency components for richer dynamics
I_t = 0.5 + 0.3 * np.sin(2 * np.pi * 0.5 * t) + 0.15 * np.sin(2 * np.pi * 1.2 * t) + 0.05 * np.random.randn(len(t))

# Metastability function M(t)
dI_dt = np.gradient(I_t, dt)
M_t = np.abs(dI_dt) * (1 - I_t / I_max)

# Coordination dynamics C(t) via numerical integration
C_t = np.zeros_like(t)
for i in range(1, len(t)):
    dC = alpha * I_t[i] * M_t[i] - beta * C_t[i-1]
    C_t[i] = C_t[i-1] + dC * dt

# Qualia function Q(t): smoothed integral of C(t) over time
Q_t = integrate.cumulative_trapezoid(C_t, t, initial=0)

# Qualia activation (1 if Q ≥ θ, else 0)
qualia_active = Q_t >= theta

# Create a figure with multiple subplots for comprehensive analysis
fig = plt.figure(figsize=(15, 12))

# Time series plots
plt.subplot(3, 2, 1)
plt.plot(t, I_t, label='Information I(t)')
plt.ylabel('I(t)')
plt.title('Information Flow')
plt.legend()

plt.subplot(3, 2, 2)
plt.plot(t, M_t, label='Metastability M(t)', color='orange')
plt.ylabel('M(t)')
plt.title('Metastability')
plt.legend()

plt.subplot(3, 2, 3)
plt.plot(t, C_t, label='Coordination Dynamics C(t)', color='green')
plt.ylabel('C(t)')
plt.title('Coordination Dynamics')
plt.legend()

plt.subplot(3, 2, 4)
plt.plot(t, Q_t, label='Qualia Potential Q(t)', color='red')
plt.axhline(theta, color='gray', linestyle='--', label='Qualia Threshold θ')
plt.fill_between(t, 0, Q_t, where=qualia_active, color='red', alpha=0.3, label='Qualia Active')
plt.ylabel('Q(t)')
plt.title('Qualia Potential')
plt.legend()

# Phase space plot: I(t) vs M(t) vs C(t)
ax1 = fig.add_subplot(3, 2, 5, projection='3d')
scatter = ax1.scatter(I_t[:-1], M_t[:-1], C_t[:-1], c=t[:-1], cmap='viridis', s=1, alpha=0.7)
ax1.set_xlabel('Information I(t)')
ax1.set_ylabel('Metastability M(t)')
ax1.set_zlabel('Coordination C(t)')
ax1.set_title('Phase Space: I-M-C Dynamics')
fig.colorbar(scatter, ax=ax1, label='Time')

# 2D Phase portrait: C(t) vs I(t) with color indicating Q(t)
ax2 = fig.add_subplot(3, 2, 6)
scatter2 = ax2.scatter(I_t, C_t, c=Q_t, cmap='plasma', s=2, alpha=0.7)
ax2.set_xlabel('Information I(t)')
ax2.set_ylabel('Coordination C(t)')
ax2.set_title('Phase Portrait: I-C with Qualia Coloring')
cbar = fig.colorbar(scatter2, ax=ax2, label='Qualia Potential Q(t)')

# Add a horizontal line at the qualia threshold in the colorbar
cbar.ax.axhline(y=theta, color='black', linestyle='--', linewidth=1)
cbar.ax.text(0.5, theta, 'θ', color='black', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Additional analysis: Plot the phase space trajectory in 2D with time progression
plt.figure(figsize=(12, 10))

# I(t) vs dI/dt phase space (information flow dynamics)
plt.subplot(2, 2, 1)
plt.scatter(I_t[:-1], dI_dt[:-1], c=t[:-1], cmap='viridis', s=2)
plt.colorbar(label='Time')
plt.xlabel('Information I(t)')
plt.ylabel('dI/dt')
plt.title('Information Flow Dynamics')

# M(t) vs C(t) phase space (metastability-coordination relationship)
plt.subplot(2, 2, 2)
plt.scatter(M_t[:-1], C_t[:-1], c=Q_t[:-1], cmap='plasma', s=2)
cbar = plt.colorbar(label='Qualia Potential Q(t)')
cbar.ax.axhline(y=theta, color='black', linestyle='--', linewidth=1)
plt.xlabel('Metastability M(t)')
plt.ylabel('Coordination C(t)')
plt.title('Metastability-Coordination Relationship')

# I(t) vs Q(t) phase space (information-qualia relationship)
plt.subplot(2, 2, 3)
plt.scatter(I_t[:-1], Q_t[:-1], c=M_t[:-1], cmap='viridis', s=2)
plt.colorbar(label='Metastability M(t)')
plt.axhline(y=theta, color='black', linestyle='--', linewidth=1)
plt.xlabel('Information I(t)')
plt.ylabel('Qualia Potential Q(t)')
plt.title('Information-Qualia Relationship')

# C(t) vs dC/dt phase space (coordination dynamics)
dC_dt = np.gradient(C_t, dt)
plt.subplot(2, 2, 4)
plt.scatter(C_t[:-1], dC_dt[:-1], c=qualia_active[:-1], cmap='coolwarm', s=2)
plt.colorbar(label='Qualia Active')
plt.xlabel('Coordination C(t)')
plt.ylabel('dC/dt')
plt.title('Coordination Dynamics')

plt.tight_layout()
plt.show()

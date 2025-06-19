import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 파라미터 설정
c = 343
rho0 = 1.21
Q = 1e-4
f = 1000  # Hz
omega = 2 * np.pi * f
k = omega / c

# 공간 설정
x = np.arange(-2, 2.01, 0.01)
y = np.arange(-2, 2.01, 0.01)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)
r[r == 0] = 1e-10

# 시간 설정
t_values = np.arange(0, 0.00205, 0.00005)  # 0 ~ 2 ms

# 연속 시간으로 시뮬레이션
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(np.zeros_like(r), extent=[-2, 2, -2, 2], origin='lower',
               cmap='seismic', vmin=-0.3, vmax=0.3)
plt.colorbar(im, ax=ax, label='Pressure [Pa]')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')

def update(frame):
    t = t_values[frame]
    p = 1j * omega * rho0 * Q / (4 * np.pi * r) * np.exp(1j * (omega * t - k * r))
    im.set_array(np.real(p))
    ax.set_title(f't = {t*1e3:.2f} ms')
    return [im]

continuous = animation.FuncAnimation(fig, update, frames=len(t_values), blit=True)

# 동영상 저장
continuous.save("pressure_field_1khz.mp4", fps=20, dpi=150)

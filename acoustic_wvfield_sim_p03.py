import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 공통 파라미터
c = 343
rho0 = 1.21
f = 1000
omega = 2 * np.pi * f
k = omega / c

# 음원 정보: (x, y, Q)
sources = [(-0.05, 0.0, 1e-4),
           ( 0.05, 0.0, 1e-4),
           ( 0.00, 0.0, 2e-4)]

# 공간 설정
x = np.arange(-2, 2.01, 0.01)
y = np.arange(-2, 2.01, 0.01)
X, Y = np.meshgrid(x, y)

# 시간 설정
t_values = np.arange(0, 0.00205, 0.00005)

# 동영상 초기화
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(np.zeros_like(X), extent=[-2, 2, -2, 2], origin='lower',
               cmap='seismic', vmin=-0.3, vmax=0.3)
plt.colorbar(im, ax=ax, label='Pressure [Pa]')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')

def update(frame):
    t = t_values[frame]
    p_total = np.zeros_like(X, dtype=complex)
    for sx, sy, Q in sources:
        r = np.sqrt((X - sx)**2 + (Y - sy)**2)
        r[r == 0] = 1e-10
        p = 1j * omega * rho0 * Q / (4 * np.pi * r) * np.exp(1j * (omega * t - k * r))
        p_total += p
    im.set_array(np.real(p_total))
    ax.set_title(f't = {t*1e3:.2f} ms')
    return [im]

continuous = animation.FuncAnimation(fig, update, frames=len(t_values), blit=True)

# 동영상 저장
continuous.save("pressure_field_3_sources.mp4", fps=20, dpi=150)

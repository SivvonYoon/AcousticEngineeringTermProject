import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 파라미터
c = 343
rho0 = 1.21
f = 1000
omega = 2 * np.pi * f
k = omega / c
R = 0.8

# 실제 음원 + 3개 1차 반사 소스
sources = [
    (0.0, 0.5, 1.0),           # 실제 음원
    (0.0, -0.5, R),            # 바닥 반사
    (-3.0, 0.5, R),            # 좌측 벽 반사 (x = -1.5 기준)
    (3.0, 0.5, R)              # 우측 벽 반사 (x = 1.5 기준)
]

# 격자 생성
x = np.arange(-1.5, 1.51, 0.01)
y = np.arange(0.0, 2.01, 0.01)
X, Y = np.meshgrid(x, y)

# 시간 설정
t_values = np.arange(0, 0.00205, 0.00005)

# 동영상으로
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(np.zeros_like(X), extent=[-1.5, 1.5, 0, 2], origin='lower',
               cmap='seismic', vmin=-0.3, vmax=0.3)
plt.colorbar(im, ax=ax, label='Pressure [Pa]')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')

def update(frame):
    t = t_values[frame]
    p_total = np.zeros_like(X, dtype=complex)
    for sx, sy, gain in sources:
        r = np.sqrt((X - sx)**2 + (Y - sy)**2)
        r[r == 0] = 1e-10
        Q = 1e-4 * gain
        p = 1j * omega * rho0 * Q / (4 * np.pi * r) * np.exp(1j * (omega * t - k * r))
        p_total += p
    im.set_array(np.real(p_total))
    ax.set_title(f't = {t*1e3:.2f} ms')
    return [im]

continuous = animation.FuncAnimation(fig, update, frames=len(t_values), blit=True)

# 저장
continuous.save("pressure_field_with_reflection.mp4", fps=20, dpi=150)

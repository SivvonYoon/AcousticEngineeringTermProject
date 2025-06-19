import numpy as np
import matplotlib.pyplot as plt

# 파라미터 설정
c = 343                # 음속 [m/s]
rho0 = 1.21            # 공기 밀도 [kg/m^3]
Q = 1e-4               # 부피속도 [m^3/s]
frequencies = [1000, 3000]  # Hz
t = 0

# 공간 설정
x = np.arange(-2, 2.01, 0.01)
y = np.arange(-2, 2.01, 0.01)
X, Y = np.meshgrid(x, y)                                                                                                                       
r = np.sqrt(X**2 + Y**2)
r[r == 0] = 1e-10  # 0으로 나눠지는 거 방지용

# 주파수별 음장 시각화
for f in frequencies:
    omega = 2 * np.pi * f
    k = omega / c
    p = 1j * omega * rho0 * Q / (4 * np.pi * r) * np.exp(-1j * k * r)
    p_real = np.real(p)

    plt.figure(figsize=(6, 5))
    im = plt.imshow(p_real, extent=[-2, 2, -2, 2], origin='lower', cmap='seismic')
    plt.title(f'Pressure Field at t=0 s (f = {f} Hz)')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.colorbar(im, label='Pressure [Pa]')
    plt.clim(-0.3, 0.3)
    plt.tight_layout()
    plt.savefig(f'pressure_field_{f}Hz.png', dpi=300)
    plt.show()

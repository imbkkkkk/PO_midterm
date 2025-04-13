import netCDF4 as nc 
import numpy as np
import matplotlib.pyplot as plt
import gsw

dataset = nc.Dataset("C:/Users/ASUS/Desktop/coding/PO/HW1/mercatorglorys12v1_gl12_mean_1993_2016_01.nc" ,'r')

latitude = dataset.variables['latitude'][:]
longitude = dataset.variables['longitude'][:]
depth = dataset.variables['depth'][:]

uo = dataset.variables['uo'][0,0,:,:] 
vo = dataset.variables['vo'][0,0,:,:]
zos = dataset.variables['zos'][0,:,:]

new_lon = (longitude + 360) % 360
sort_idx = np.argsort(new_lon)
sorted_lon = new_lon[sort_idx]

sorted_uo = uo[:, sort_idx]
sorted_vo = vo[:, sort_idx]
sorted_zos = zos[:, sort_idx]

latitude_np = latitude[1020:1560]
longitude_np = sorted_lon[1440:3120]
uo_np = sorted_uo[1020:1560, 1440:3120]
vo_np = sorted_vo[1020:1560, 1440:3120]
zos_np = sorted_zos[1020:1560, 1440:3120]

# 基本參數
g = 9.81  # m/s^2
omega = 7.2921e-5  # 地球自轉角速度 rad/s
deg2rad = np.pi / 180

# 經緯度網格
lat = latitude_np
lon = longitude_np
Lon, Lat = np.meshgrid(lon, lat)

# Coriolis parameter f (2Ωsin(φ))
f = 2 * omega * np.sin(Lat * deg2rad)
f = np.where(f == 0, np.nan, f)  # 避免除以0

# 地球半徑 & spacing
Re = 6371000  # m
dy = (lat[1] - lat[0]) * deg2rad * Re
dx = (lon[1] - lon[0]) * deg2rad * Re * np.cos(Lat * deg2rad)  # 注意cos(lat)

# 計算 SSH 梯度
deta_dy, deta_dx = np.gradient(zos_np, dy, axis=0), np.gradient(zos_np, axis=1)
deta_dx = deta_dx / dx  # 每格的 dx 是 2D，因此要除以 dx 網格

# 計算地轉速度
u_g = -g * deta_dy / f
v_g = g * deta_dx / f

step = 40

plt.figure(figsize=(10,6))
plt.contour(lon, lat, zos_np, levels=100, colors='k', linewidths = 0.2)
plt.contourf(lon, lat, zos_np, cmap='viridis', levels=100)
plt.colorbar(label='SSH (m)')
plt.quiver(lon[::step], lat[::step], u_g[::step,::step], v_g[::step,::step], color='k', width = 0.002)
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
plt.title('Geostrophic Velocity over SSH')
plt.savefig('mid_10.png')
plt.show()

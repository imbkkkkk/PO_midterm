import netCDF4 as nc 
import numpy as np
import matplotlib.pyplot as plt
import gsw

dataset = nc.Dataset("C:/Users/ASUS/Desktop/coding/PO/HW1/mercatorglorys12v1_gl12_mean_1993_2016_01.nc" ,'r')

latitude = dataset.variables['latitude'][:]
longitude = dataset.variables['longitude'][:]
depth = dataset.variables['depth'][:]

uo_s = dataset.variables['uo'][0,0,:,:] 
vo_s = dataset.variables['vo'][0,0,:,:]
uo_d = dataset.variables['uo'][0,23,:,:] 
vo_d = dataset.variables['vo'][0,23,:,:]
zos = dataset.variables['zos'][0,:,:]

new_lon = (longitude + 360) % 360
sort_idx = np.argsort(new_lon)
sorted_lon = new_lon[sort_idx]

sorted_uos = uo_s[:, sort_idx]
sorted_vos = vo_s[:, sort_idx]
sorted_uod = uo_d[:, sort_idx]
sorted_vod = vo_d[:, sort_idx]
sorted_zos = zos[:, sort_idx]

latitude_np = latitude[1020:1560]
longitude_np = sorted_lon[1440:3120]
uos_np = sorted_uos[1020:1560, 1440:3120]
vos_np = sorted_vos[1020:1560, 1440:3120]
uod_np = sorted_uod[1020:1560, 1440:3120]
vod_np = sorted_vod[1020:1560, 1440:3120]
zos_np = sorted_zos[1020:1560, 1440:3120]

g = 9.81
omega = 7.2921e-5
deg2rad = np.pi / 180

lat = latitude_np
lon = longitude_np
Lon, Lat = np.meshgrid(lon, lat)

f = 2 * omega * np.sin(Lat * deg2rad)
f = np.where(f == 0, np.nan, f)

Re = 6371000  # m
dy = (lat[1] - lat[0]) * deg2rad * Re
dx = (lon[1] - lon[0]) * deg2rad * Re * np.cos(Lat * deg2rad)

deta_dy, deta_dx = np.gradient(zos_np, dy, axis=0), np.gradient(zos_np, axis=1)
deta_dx = deta_dx / dx 

u_g = -g * deta_dy / f
v_g = g * deta_dx / f

from numpy import cos, sin, arccos, deg2rad

us1 = uos_np / np.sqrt(uos_np**2 + vos_np**2)
vs1 = vos_np / np.sqrt(uos_np**2 + vos_np**2)
ud1 = uod_np / np.sqrt(uod_np**2 + vod_np**2)
vd1 = vod_np / np.sqrt(uod_np**2 + vod_np**2)
u2 = u_g / np.sqrt(u_g**2 + v_g**2)
v2 = v_g / np.sqrt(u_g**2 + v_g**2)

# cos_angle_s = us1 * u2 + vs1 * v2
# angle_diff_s = np.arccos(np.clip(cos_angle_s, -1, 1)) * 180 / np.pi  # in degrees
# cos_angle_d = ud1 * u2 + vd1 * v2
# angle_diff_d = np.arccos(np.clip(cos_angle_d, -1, 1)) * 180 / np.pi  # in degrees

# bins = np.arange(0, 190, 5) 
# hist_s, bin_edges_s = np.histogram(angle_diff_s.flatten(), bins=bins)
# hist_d, bin_edges_d = np.histogram(angle_diff_d.flatten(), bins=bins)

# bin_centers_s = (bin_edges_s[:-1] + bin_edges_s[1:]) / 2
# bin_centers_d = (bin_edges_d[:-1] + bin_edges_d[1:]) / 2

# plt.figure(figsize=(10,6))
# plt.plot(bin_centers_s, hist_s, color='b', linewidth = 3, label='depth=0')
# plt.plot(bin_centers_d, hist_d, color='r', linewidth = 3, label='depth=23')
# plt.xlabel('difference of direction (°)')
# plt.ylabel('frequency')
# plt.title('Difference of Direction between Geostophic Currents and Velocity Field')
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.savefig('mid_11.png')
# plt.show()

# plt.figure(figsize=(10,6))
# plt.hist(angle_diff_d.flatten(), bins=50, color='pink')
# plt.hist(angle_diff_s.flatten(), bins=50, color='skyblue')
# plt.plot(angle_diff_s.flatten(), color='skyblue')
# plt.plot(angle_diff_d.flatten(), color='pink')
# plt.xlabel('difference of direction (°)')
# plt.ylabel('frequency')
# plt.title('Difference of Direction between Geostophic Current and Velocity Field at depth=0')
# plt.show()

speed_s = np.sqrt(uos_np**2 + vos_np**2)
speed_d = np.sqrt(uod_np**2 + vod_np**2)
speed_g = np.sqrt(u_g**2 + v_g**2)
diff_s = speed_s - speed_g
diff_d = speed_d - speed_g

bins = np.arange(-2, 2.05, 0.05)
hist_s, bin_edges_s = np.histogram(diff_s.flatten(), bins=bins)
hist_d, bin_edges_d = np.histogram(diff_d.flatten(), bins=bins)

bin_centers_s = (bin_edges_s[:-1] + bin_edges_s[1:]) / 2
bin_centers_d = (bin_edges_d[:-1] + bin_edges_d[1:]) / 2

# plt.figure(figsize=(10, 6))
# plt.hist(diff_s.flatten(), bins=50, color='b')
# plt.xlabel('observed - geostophic [m/s]')
# plt.ylabel('frequency')
# plt.title('Difference of Magnitude of Velocity between Geostophic Currents and Velocity Field')
# plt.show()
plt.figure(figsize=(10,6))
plt.plot(bin_centers_s, hist_s, color='b', linewidth = 3, label='depth=0')
plt.plot(bin_centers_d, hist_d, color='r', linewidth = 3, label='depth=23')
plt.xlabel('observed - geostophic [m/s]')
plt.ylabel('frequency')
plt.title('Difference of Magnitude of Velocity between Geostophic Currents and Velocity Field')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('mid_12.png')
plt.show()

max_abs = np.max(np.abs([diff_s, diff_d]))

plt.figure(figsize=(10, 6))
cf1 = plt.contourf(longitude_np, latitude_np, diff_s, cmap='RdBu_r', vmin=-max_abs, vmax=max_abs, levels=20)
plt.colorbar(cf1, label='diff [m/s]')
plt.title('Difference of Magnitude of Velocity between Geostophic Currents and Velocity Field at depth=0')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('mid_13.png')
plt.show()

plt.figure(figsize=(10, 6))
cf2 = plt.contourf(longitude_np, latitude_np, diff_d, cmap='RdBu_r', vmin=-max_abs, vmax=max_abs, levels=20)
plt.colorbar(cf2, label='diff [m/s]')
plt.title('Difference of Magnitude of Velocity between Geostophic Currents and Velocity Field at depth=23')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('mid_14.png')
plt.show()
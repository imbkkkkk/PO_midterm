import netCDF4 as nc 
import numpy as np
import matplotlib.pyplot as plt
import gsw

dataset = nc.Dataset("C:/Users/ASUS/Desktop/coding/PO/HW1/mercatorglorys12v1_gl12_mean_1993_2016_01.nc" ,'r')

latitude = dataset.variables['latitude'][:]
longitude = dataset.variables['longitude'][:]
depth = dataset.variables['depth'][:]

new_lon = (longitude + 360) % 360
sort_idx = np.argsort(new_lon)
sorted_lon = new_lon[sort_idx]

#(50,2041,4320)

# 1380 for 35N #A
# 480 for 40S #B

# 1800 for -30
# thetao =  dataset.variables['thetao'][0,0,:,:]
# so = dataset.variables['so'][0,0,:,:]
# uo = dataset.variables['uo'][0,0,:,:]
# vo = dataset.variables['vo'][0,0,:,:]
zos = dataset.variables['zos'][0,:,:]

sorted_zos = zos[:, sort_idx]

plt.figure(figsize=(10,6))
plt.contour(sorted_lon, latitude, sorted_zos, colors = 'k', levels = 25, linewidths = 0.5)
plt.contourf(sorted_lon, latitude, sorted_zos, levels = 25)
plt.colorbar()
plt.title("ssh (Jan)")

plt.savefig(f"mid_1.png")
plt.show()
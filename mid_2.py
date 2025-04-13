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
 
# for i in range(2,13):
#     dataset1 = nc.Dataset(f'C:/Users/ASUS/Desktop/coding/PO/HW1/mercatorglorys12v1_gl12_mean_1993_2016_{i:02d}.nc', 'r')
#     uo1 =  dataset1.variables['uo'][0,0,:,:]
#     vo1 = dataset1.variables['vo'][0,0,:,:]
#     zos1 = dataset1.variables['zos'][0,:,:]
#     uo += uo1
#     vo += vo1
#     zos += zos1

# uo = uo / 12
# vo = vo / 12
# zos = zos / 12
 
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

#kurosio(lat_np,lon_np) = (25N240:35N360,125E60:140E240)     
speed = np.sqrt(uo_np**2 + vo_np**2)

# v_ku = max_speed = np.sqrt(uo_np**2 + vo_np**2).max()
# print(uo_np[240,60])
# print(v_ku, 'm/s')

# plt.plot(latitude_np, uo_np[:,0:240],label='Eastthward Velocity')
# plt.xlabel('latitude [°N]')
# plt.ylabel('velocity [m/s]')
# plt.title('Eastward Velocity Distribution over Latitude between 120°E and 140°N')
# plt.savefig(f"mid_4.png")
# plt.show()     

# plt.plot(latitude_np, vo_np[:,0:240],label='Northward Velocity')
# plt.xlabel('latitude [°N]')
# plt.ylabel('velocity [m/s]')
# plt.title('Northward Velocity Distribution over Latitude between 120°E and 140°N')
# plt.savefig(f"mid_5.png")
# plt.show()        

# plt.plot(latitude_np, speed[:,0:240],label='Velocity')
# plt.xlabel('latitude [°N]')
# plt.ylabel('velocity [m/s]')
# plt.title('Velocity Distribution over Latitude between 120°E and 140°N')
# plt.savefig(f"mid_6.png")
# plt.show()

# plt.plot(longitude_np[0:240], vo_np[:,0:240].T,label='Velocity')
# plt.xlabel('latitude [°N]')
# plt.ylabel('velocity [m/s]')
# plt.title('Northward Velocity Distribution over Longitude between 120°E and 140°N')
# plt.savefig(f"mid_7.png")
# plt.show()

#
plt.contourf(longitude_np[0:240], latitude_np, speed[:,0:240], levels = 20)
plt.colorbar()
plt.title("Velocity Field between 120°E and 140°N")
plt.savefig(f"mid_9.png")
plt.show()
exit()          
#%%
step = 40

plt.figure(figsize=(10,6))
plt.contour(longitude_np, latitude_np, zos_np, colors = 'k', levels = 20, linewidths = 0.5)
plt.contourf(longitude_np, latitude_np, zos_np, levels = 20)
plt.colorbar()
max_speed = np.sqrt(uo_np**2 + vo_np**2).max()
scale = max_speed / 0.5  
q = plt.quiver(longitude_np[::step], latitude_np[::step], uo_np[::step,::step], vo_np[::step,::step], width = 0.002, scale = scale, color = 'k')


plt.title("ssh & surface velocity field(Annual)")
plt.quiverkey(q, X=0.95, Y=0.95, 
              U=0.1, 
              label='0.1 m/s', 
              labelpos='E',
              color='black',
              fontproperties={'weight': 'bold'})
# plt.savefig(f"mid_3.png")
plt.show()
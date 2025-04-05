import serial
import time
# from ahrs.filters import Madgwick
import numpy as np

from panda3d.core import loadPrcFileData
loadPrcFileData('', 'window-title IMU 3D Viewer')

# from direct.showbase.ShowBase import ShowBase
# from panda3d.core import NodePath
# from scipy.spatial.transform import Rotation as R

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM9'

# madgwick = Madgwick()
# q = madgwick.updateIMU(q, gyr=[gx, gy, gz], acc=[ax, ay, az])

ser.open()
data = ser.readline().decode('utf-8').strip()
ser.close()
print(data)

ser.open()
data = ser.readline().decode('utf-8').strip()
ser.close()
print(data)



def read_imu_data():
    ser.open()

    data = ser.readline().decode().strip()
    ser.close()
    print(data)
    try:
        if not data.startswith("#"):
            return None, None, None, False
        else:
            data = data[1:]  # remove #
            parts = data.split(',')
            print(parts)

            if len(parts) == 9:
                a = True
                ax, ay, az = map(float, parts[0:3])
                gx, gy, gz = map(float, parts[3:6])
                mx, my, mz = map(float, parts[6:9])
                return (ax, ay, az), (gx, gy, gz), (mx, my, mz), a
    except:
        pass
    return None, None, None, False


accel, gyro, mag, cond = read_imu_data()
if (cond == True):
    print(accel)
    print(gyro)
    print(mag)
else:
    print('bad')

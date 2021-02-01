import time
from rplidar import RPLidar
lidar = RPLidar('COM8')

# info = lidar.get_info()
# print(info)

health = lidar.get_health()
print(health)

i = 0

time.sleep(5)


def stopLidar():
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

def iterable_measurements():
    for i, measurement in enumerate(lidar.iter_measurments()):
        
        if measurement[2] > 0 and measurement[2] < 90:
            # if measurement[0] == True:
            print(measurement)
        # if i > 10:
        #     stopLidar()

def raw_measurements():
    for measurement in (lidar.iter_measurments()):
        if measurement[2] == 120:
            print(measurement)
        
def iterable_scans():
    for i, scan in enumerate(lidar.iter_scans()):
        # print('%d: Got %d measurments' % (i, len(scan)))
        print(i)
        print(scan[0][0])
        if i > 0:
            stopLidar()

# lidar.reset()

# iterable_scans()
# raw_measurements()
iterable_measurements()
# stopLidar()
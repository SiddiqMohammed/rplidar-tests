import sys
import time
from rplidar import RPLidar
import math


PORT_NAME = 'COM8'  # COM port used by the lidar

stop = False
templist = []

# in mm
tp_dist = 600 
tp_dist_tolerance = 50
tp_angle = 90 
tp_angle_tolerance = 10


def scan(lidar):
    global stop
    while True:
        counter = 0
        print('Recording measurements... Press Crl+C to stop.')

        for measurment in lidar.iter_measurments():
            if stop == True:
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                break

            # t
            if (measurment[2] > tp_angle - tp_angle_tolerance and measurment[2] < tp_angle + tp_angle_tolerance) :  # in angular range
                templist.append(measurment[3])
                
            else:
                if len(templist) != 0:
                    avg_val = average(templist)

                    if avg_val < tp_dist + tp_dist_tolerance and avg_val > tp_dist - tp_dist_tolerance:
                        print(avg_val)
                        # print(measurment[3])
                    templist.clear()

def average(lst):
    return sum(lst) / len(lst) 


def run():
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    lidar.start_motor()
    time.sleep(1)
    info = lidar.get_info()
    print(info)
    try:
        scan(lidar)
    except KeyboardInterrupt:
        stop = True
        print('Stopping.')
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()


if __name__ == '__main__':
    run()

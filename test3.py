import sys
import time
from rplidar import RPLidar
import math


PORT_NAME = 'COM8'  # COM port used by the lidar

stop = False
templist = []

touchpoint = 200
tp_tolerance = 20

def scan(lidar):
    global stop
    while True:
        counter = 0
        print('Recording measurements... Press Crl+C to stop.')
        data = 0
        range_sum = 0
        for measurment in lidar.iter_measurments():
            if stop == True:
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                break

            if (measurment[2] > 89 and measurment[2] < 100) :  # in angular range
                templist.append(measurment[3])
            else:
                if len(templist) != 0:
                    avg_val = average(templist)

                    if avg_val < touchpoint + tp_tolerance and avg_val > touchpoint - tp_tolerance:
                        print(avg_val)
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

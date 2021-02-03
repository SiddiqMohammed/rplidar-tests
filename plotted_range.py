import serial
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
from rplidar import RPLidar
import math





PORT_NAME = 'COM8'  # COM port used by the lidar

stop = False
templist = []

# in mm
tp_dist = 240 
tp_dist_tolerance = 30
tp_angle = 90 
tp_angle_tolerance = 1

# tp_dist_array = [240, 340]
# tp_angle_array = [90, 70]

json_data = [[340, 70], [240, 90]]
# json_data = [ [360, 70]]

def scan(lidar):
    global stop
    i = 0
    plt.ion()
    fig=plt.figure()

    i=0
    x=list()
    y=list()
    filtered_val = 0

    while True:


        print('Recording measurements... Press Crl+C to stop.')

        for measurment in lidar.iter_measurments():
            if stop == True:
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                break

          
            
        
            if (measurment[2] > tp_angle - tp_angle_tolerance and measurment[2] < tp_angle + tp_angle_tolerance) :  # in angular range
                templist.append(measurment[3])
                
            else:
                if len(templist) != 0:
                    avg_val = average(templist)

                    if avg_val < tp_dist + tp_dist_tolerance and avg_val > tp_dist - tp_dist_tolerance:
                        print(f"avg val: {avg_val}")
                        filtered_val = (0.8 * filtered_val) + (0.2 * avg_val)
                        print(f"filtered val: {filtered_val}")

                        x.append(i)
                        y.append(avg_val)

                        plt.plot(i, float(filtered_val), "bo")
                        plt.plot(i, float(avg_val), "ro")
                        i += 1
                        plt.show()
                        plt.pause(0.0001)  # Note this correction
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

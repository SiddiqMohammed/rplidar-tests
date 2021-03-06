import sys
import time
from rplidar import RPLidar
import math


PORT_NAME = 'COM8'  # COM port used by the lidar

stop = False
templist = []

# in mm
# tp_dist = 240 
tp_dist_tolerance = 30
# tp_angle = 90 
tp_angle_tolerance = 1

# tp_dist_array = [240, 340]
# tp_angle_array = [90, 70]

json_data = [[340, 70], [240, 90]]
# json_data = [ [360, 70]]

def scan(lidar):
    global stop
    filtered_val = 0

    while True:
        print('Recording measurements... Press Crl+C to stop.')

        for measurment in lidar.iter_measurments():
            if stop == True:
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                break

            for tp in range(0, len(json_data)):
                # print(tp)
                # print(json_data[tp][0])

                tp_dist = json_data[tp][0]
                tp_angle = json_data[tp][1]
                
            
                if (measurment[2] > tp_angle - tp_angle_tolerance and measurment[2] < tp_angle + tp_angle_tolerance) :  # in angular range
                    templist.append(measurment[3])
                    
                else:
                    if len(templist) != 0:
                        avg_val = average(templist)
                        filtered_val = (0.8 * filtered_val) + (0.2 * avg_val)

                        if filtered_val < tp_dist + tp_dist_tolerance and filtered_val > tp_dist - tp_dist_tolerance:
                            # print(avg_val)
                            print(f"Clicked {tp}")
                            print(json_data[tp][0], json_data[tp][1])
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

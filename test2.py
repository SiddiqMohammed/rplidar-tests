import sys
import time
from rplidar import RPLidar
import math


PORT_NAME = 'COM8'  # COM port used by the lidar

stop = False
angles_list_0 = []
angles_list_1 = []

# in mm
tp_dist = [360, 240]
tp_dist_tolerance = 20
dist_precision = 1  # number of times the value has to be repeated to be registered as precise

tp_angle = [260, 300]
tp_angle_tolerance = 5

# tp_dist_array = [240, 340]
# tp_angle_array = [90, 70]

json_data = [[340, 70], [240, 90]]
# json_data = [ [360, 70]]

def scan(lidar):
    global stop
    filtered_val = [0, 0]

    while True:
        print('Recording measurements... Press Crl+C to stop.')

        for measurment in lidar.iter_measurments():
            if stop == True:
                lidar.stop()
                lidar.stop_motor()
                lidar.disconnect()
                break

                
            # Check if the angle is 70
            if (measurment[2] > tp_angle[0] - tp_angle_tolerance and measurment[2] < tp_angle[0] + tp_angle_tolerance) :  # in angular range
                angles_list_0.append(measurment[3])

                if len(angles_list_0) >dist_precision:
                    avg_val = average(angles_list_0)
                    filtered_val[0] = (0.8 * filtered_val[0]) + (0.2 * avg_val)

                    if filtered_val[0] < tp_dist[0] + tp_dist_tolerance and filtered_val[0] > tp_dist[0] - tp_dist_tolerance:
                        # print(avg_val)
                        print(f"Clicked 0 at {filtered_val[0]}mm at 270deg")
                    angles_list_0.clear()


            # check if the angle is 90
            if (measurment[2] > tp_angle[1] - tp_angle_tolerance and measurment[2] < tp_angle[1] + tp_angle_tolerance) :  # in angular range
                angles_list_1.append(measurment[3])

                if len(angles_list_1) > dist_precision:
                    avg_val = average(angles_list_1)
                    filtered_val[1] = (0.8 * filtered_val[1]) + (0.2 * avg_val)

                    if filtered_val[1] < tp_dist[1] + tp_dist_tolerance and filtered_val[1] > tp_dist[1] - tp_dist_tolerance:
                        # print(avg_val)
                        print(f"Clicked 1 at {filtered_val[1]}mm at 90deg")
                    angles_list_1.clear()

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

#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

import sys
import time
import math

PORT_NAME = 'COM8'
DMAX = 4000
IMIN = 0
IMAX = 50
lidar = RPLidar(PORT_NAME)

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    for measurment in lidar.iter_measurments():
        if (measurment[2] > 80 and measurment[2] < 100):  # in angular range
            print(measurment[3])
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                        cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)

    iterator = lidar.iter_scans()
    


    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()



# angle_offset = 50  # this compensates for the Lidar being placed in a rotated position
# gain = 2.0  # this is the steering gain
# speed = 70  # crusing speed
# # this compensates for any steering bias the car has. Positive numbers steer to the right
# steering_correction = -10
# start = time.time()
# stop = False





# def scan(lidar):
#     global stop
#     time1 = time.time()
#     while True:
#         counter = 0
#         print('Recording measurements... Press Crl+C to stop.')
#         data = 0
#         range_sum = 0
#         lasttime = time.time()
#         for measurment in lidar.iter_measurments():
#             if stop == True:
#                 lidar.stop()
#                 lidar.stop_motor()
#                 # c.send("motors",0,0,0)  # turn off wheel motors
#                 lidar.disconnect()
#                 break
#             if (measurment[2] > 260 and measurment[2] < 280):  # in angular range
#                 print(measurment[3])
#                 # if (measurment[3] < 1000 and measurment[3] > 100):  # in distance range
#                     # angle weighted by distance; basically we're coming up with an obstacle centroid
#                     # data = data + measurment[2]
#                     # range_sum = range_sum + measurment[3] # sum all the distances so we can normalize later
#                     # counter = counter + 1  # increment counter
#             # if time.time() > (lasttime + 0.1):
#             #     # print("this should happen ten times a second")
#             #     if counter > 0:  # this means we see something
#             #         # average of detected angles
#             #         average_angle = (data/counter) - angle_offset
#             #         # convert to a vector component
#             #         obstacle_direction = int(
#             #             100*math.atan(math.radians(average_angle)))
#             #         # steer in the opposite direction as obstacle (I'll replace this with a PID)
#             #         drive_direction = -1 * obstacle_direction
#             #         # print("Drive direction: ", drive_direction)

#             #         counter = 0  # reset counter
#             #         data = 0  # reset data
#             #         range_sum = 0
#             #     else:
#             #         drive_direction = 0
#             #     # steer(drive_direction)  # Send data to motors
#             #     lasttime = time.time()  # reset 10Hz timer


# def run():
#     '''Main function'''
#     lidar = RPLidar(PORT_NAME)
#     lidar.start_motor()
#     time.sleep(1)
#     info = lidar.get_info()
#     print(info)
#     try:
#         scan(lidar)
#     except KeyboardInterrupt:
#         stop = True
#         print('Stopping.')
#         lidar.stop()
#         lidar.stop_motor()
#         lidar.disconnect()


# if __name__ == '__main__':
#     run()

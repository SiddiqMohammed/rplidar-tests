# Quick stop rplidar using script

from rplidar import RPLidar
lidar = RPLidar('COM8')

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
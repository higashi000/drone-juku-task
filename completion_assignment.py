import time
from dronekit import connect, VehicleMode
from pymavlink import mavutil

vehicle = connect('127.0.0.1:14551', wait_ready=True, timeout=60)

def pos_msg(x = 0, y = 0, z = 0):
    return vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        0,0,0,
        x, y, z,
        0,0,0,
        0,0)

while not vehicle.is_armable:
    print("Initialize")
    time.sleep(1)

print("arm")
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

while not vehicle.armed:
    print("waiting arm")
    time.sleep(1)

targetAltude = 50

print("takeoff")
vehicle.simple_takeoff(targetAltude)

while True:
    print("altitude:",vehicle.location.global_relative_frame.alt)

    if vehicle.location.global_relative_frame.alt >= targetAltude * 0.95:
        print("Target altitude has been reached")
        break

    time.sleep(1)

for x in range(0, 100):
    vehicle.send_mavlink(pos_msg(2, 0, 0))
    time.sleep(0.1)


for x in range(0, 100):
    vehicle.send_mavlink(pos_msg(0, -2, 0))
    time.sleep(0.1)


for x in range(0, 100):
    vehicle.send_mavlink(pos_msg(-2, 0, 0))
    time.sleep(0.1)

for x in range(0, 100):
    vehicle.send_mavlink(pos_msg(0, 2, 0))
    time.sleep(0.1)

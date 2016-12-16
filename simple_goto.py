#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)
Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.
Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)

def get_distance_meters(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

# Provided target coordinate from IMechE
rawTarget = LocationGlobalRelative(20.8069099, 106.6084313, 20)

# Check mode is AUTO; Altitude is safe enough
safe_altitude = 10
while not (vehicle.mode == VehicleMode("AUTO") and vehicle.location.global_relative_frame.alt>=safe_altitude):
 print "Not safe altitude or not AUTO" 
 time.sleep(1)
 
# Only proceed when we are close to the rawTarget
while vehicle.mode == VehicleMode("AUTO"):
 remainingDistance = get_distance_meters(vehicle.location.global_frame,rawTarget)
 if remainingDistance < 170:
  print "Close to target, location corrected by images"
  break;
 print "remaining distance ", remainingDistance
 time.sleep(2)
 
# Switch to guided mode
print "Switch to Guided mode"
vehicle.mode = VehicleMode("GUIDED")
time.sleep(1)

# Go to correct TARGET (result from image processing)
# TBD: Calculate correctedTarget from captured images
correctedTarget = LocationGlobalRelative(20.8065690, 106.6098690, 20)
vehicle.simple_goto(correctedTarget)

# Only return to mode auto when reaching the TARGET
while vehicle.mode == VehicleMode("GUIDED"): 
 remainingDistance = get_distance_meters(vehicle.location.global_frame,correctedTarget) 
 if remainingDistance < 5: 
  print "Reach real Target, switch back to AUTO" 
  break; 
 time.sleep(2)
vehicle.mode = VehicleMode("AUTO")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

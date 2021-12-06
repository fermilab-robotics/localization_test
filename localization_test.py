#Noah Curfman
#11/18/2021


""" 
Printout and log to .csv Spot vision frame, Spot odom frame, and
frames of all fiducials in range.
"""

from __future__ import print_function
import argparse
import csv
import sys
import time
import datetime
import os

import bosdyn
import bosdyn.client
import bosdyn.client.util
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.world_object import WorldObjectClient
from bosdyn.api import world_object_pb2
from bosdyn.client.math_helpers import SE3Pose, quat_to_eulerZYX
from bosdyn.client.frame_helpers import *


containerDebuginVS = False

def is_docker():
    path = '/proc/self/cgroup'
    return (os.path.exists('/.dockerenv') or
            os.path.isfile(path) and any('docker' in line for line in open(path)))


def create_csv_filename():
    if is_docker() and containerDebuginVS:
        return f'/pos_out/localization_test_output_{time.strftime("%Y%m%d-%H%M%S")}.csv'
    return f'localization_test_output_{time.strftime("%Y%m%d-%H%M%S")}.csv'


def main(argv):


    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_common_arguments(parser)

    #If running in a container env in VSCode use -vs to be able to run this script from the VScode terminal with
    #python3 localization_test.py -vs --username $USERNAME --password $PASSWORD $ROBOT_IP
    parser.add_argument('-vs', dest='containerDebuginVS', action='store_true')
    options = parser.parse_args(argv)

 

    # Create robot object with a world object client.
    sdk = bosdyn.client.create_standard_sdk('localization_test_client ')
    robot = sdk.create_robot(options.hostname)
    robot.authenticate(options.username, options.password)
    # Time sync is necessary so that time-based filter requests can be converted.
    robot.time_sync.wait_for_sync()

    #Create robot state world object clients
    robot_state_client = robot.ensure_client(RobotStateClient.default_service_name)
    world_object_client = robot.ensure_client(WorldObjectClient.default_service_name)

    # Creat an empty list to hold data
    data_list = []
    curr_fname = ''

    try:
        while True:
            input("Press Enter to log robot and fiducial positions...")


            # Get info for vision and odom frames 
            odom_T_body = get_a_tform_b(robot_state_client.get_robot_state().kinematic_state.transforms_snapshot,"odom","body")
            vision_T_body = get_a_tform_b(robot_state_client.get_robot_state().kinematic_state.transforms_snapshot,"vision","body") 
            robotPositionTime = datetime.datetime.now()


            # Get all fiducial objects (an object of a specific type).
            request_fiducials = [world_object_pb2.WORLD_OBJECT_APRILTAG]
            fiducial_objects = world_object_client.list_world_objects(object_type=request_fiducials).world_objects
            fiducialTime = datetime.datetime.now()


            #Convert Quaternions to Euler Angles
            odomBodyEuler = quat_to_eulerZYX(odom_T_body.rot)
            visionBodyEuler = quat_to_eulerZYX(vision_T_body.rot)
           
            # Robot position data printout
            print()
            print("-"*10 + "Robot Position" + "-"*10)
            print("time: " + str(robotPositionTime))
            print()

            print("Odom:")
            print("    x: " + str(odom_T_body.x))
            print("    y: " + str(odom_T_body.y))
            print("    z: " + str(odom_T_body.z))
            print(f'    yaw:{odomBodyEuler[0]}')
            print(f'    pitch:{odomBodyEuler[1]}')
            print(f'    roll:{odomBodyEuler[2]}')
            print("")


            print("Vision:")
            print("    x: " + str(vision_T_body.x))
            print("    y: " + str(vision_T_body.y))
            print("    z: " + str(vision_T_body.z))
            print(f'    yaw:{visionBodyEuler[0]}')
            print(f'    pitch:{visionBodyEuler[1]}')
            print(f'    roll:{visionBodyEuler[2]}')

            
            # Log robot position data
            data_entry = {
               'bot_odom_x': odom_T_body.x,
               'bot_odom_y': odom_T_body.y,
               'bot_odom_z': odom_T_body.z,
               'bot_odom_yaw': odomBodyEuler[0],
               'bot_odom_pitch': odomBodyEuler[1],
               'bot_odom_roll': odomBodyEuler[2],
               'bot_vis_x': vision_T_body.x,
               'bot_vis_y': vision_T_body.y,
               'bot_vis_z': vision_T_body.z,
               'bot_vis_yaw': visionBodyEuler[0],
               'bot_vis_pitch': visionBodyEuler[1],
               'bot_vis_roll': visionBodyEuler[2],
               'bot_time' : robotPositionTime
            }

            data_list.append(data_entry)
           
            
            # Fiducial position data header printout            
            print("")
            print("-"*10 + "Fiducial Positions" + "-"*10)
            print("time: " + str(fiducialTime))
            print()


            for fiducial in fiducial_objects:
                vision_T_fiducial = get_a_tform_b(fiducial.transforms_snapshot, VISION_FRAME_NAME, fiducial.apriltag_properties.frame_name_fiducial)
                odom_T_fiducial = get_a_tform_b(fiducial.transforms_snapshot, ODOM_FRAME_NAME, fiducial.apriltag_properties.frame_name_fiducial)

                odomTagEuler = quat_to_eulerZYX(odom_T_fiducial.rot)
                visionTagEuler = quat_to_eulerZYX(vision_T_fiducial.rot)

                # Fidcucial position data printout
                print("Odom " + fiducial.name + ":")
                print("    x: "+ str(odom_T_fiducial.x))
                print("    y: "+ str(odom_T_fiducial.y))
                print("    z: "+ str(odom_T_fiducial.z))
                print(f'    yaw:{odomTagEuler[0]}')
                print(f'    pitch:{odomTagEuler[1]}')
                print(f'    roll:{odomTagEuler[2]}')
                print("")


                print("Vision " + fiducial.name +  ":")
                print("    x: "+ str(vision_T_fiducial.x))
                print("    y: "+ str(vision_T_fiducial.y))
                print("    z: "+ str(vision_T_fiducial.z))
                print(f'    yaw:{odomVisionEuler[0]}')
                print(f'    pitch:{odomVisionEuler[1]}')
                print(f'    roll:{odomVisionEuler[2]}')
                print('') 


                #Log fiducial position data
                data_entry.update({
                  fiducial.name + '_odom_x': odom_T_body.x,
                  fiducial.name + '_odom_y': odom_T_body.y,
                  fiducial.name + '_odom_z': odom_T_body.z,
                  fiducial.name + '_odom_yaw': odomTagEuler[0],
                  fiducial.name + '_odom_pitch': odomTagEuler[1],
                  fiducial.name + '_odom_roll': odomTagEuler[2],
                  fiducial.name + '_vis_x': vision_T_body.x,
                  fiducial.name + '_vis_y': vision_T_body.y,
                  fiducial.name + '_vis_z': odom_T_body.z,
                  fiducial.name + '_vis_yaw': odomVisionEuler[0],
                  fiducial.name + '_vis_pitch': odomVisionEuler[1],
                  fiducial.name + '_vis_roll': odomVisionEuler[2],
                })
         

            data_entry.update({'tag_time' : fiducialTime})
            data_list.append(data_entry)
                               
       

            # Create csv with header then write latest row
            keys = data_list[0].keys()
            if curr_fname == '':
                curr_fname = create_csv_filename()
                with open(curr_fname, 'w') as output_file:
                    header_writer = csv.DictWriter(output_file, keys)
                    header_writer.writeheader()
            with open(curr_fname, 'a') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writerow(data_list[-1])


    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, exiting")
        return True
 


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)

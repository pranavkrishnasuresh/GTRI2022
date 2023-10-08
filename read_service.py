#!/usr/bin/env python

import json
from os.path import exists
import geometry_msgs
import rospy
from tf.transformations import quaternion_from_euler
from point_loader.srv import poseRequest
import math

def handle_read(req):
    print("Returning poseStamped " + req.name)
    return take_from_json(req.name)

# initializes the service and calls the handle_read function to retreive the data
def poseRequest_server():                                    
    rospy.init_node("poseRequest_server")
    s = rospy.Service("poseRequest_read", poseRequest, handle_read)
    print("Ready to read")
    rospy.spin()

path_name = "amalli7"

# opens the json file and returns the requested poseStamped name 
def take_from_json(pose_name):
    with open('/home/{}/pose_file.json'.format(path_name), 'r') as json_file:
        data = json.load(json_file)
        if pose_name in data:
            return make_pose(data[pose_name]) 
        else:
            print("Failed to read pose from file: {}".format(pose_name))
            return -1

# creates a poseStamped object with the relevant information 
def make_pose(pose_data):
    header, x, y, z, roll, pitch, yaw = pose_data
    pose1 = geometry_msgs.msg.PoseStamped()
    pose1.header.stamp = rospy.Time.now()
    pose1.header.frame_id = "/" + header
    pose1.pose.position.x = x
    pose1.pose.position.y = y
    pose1.pose.position.z = z
    quat = quaternion_from_euler(roll, pitch, yaw)
    pose1.pose.orientation.x = math.radians(quat[0])
    pose1.pose.orientation.y = math.radians(quat[1])
    pose1.pose.orientation.z = math.radians(quat[2])
    pose1.pose.orientation.w = math.radians(quat[3])
    return pose1


if __name__ == '__main__':
    poseRequest_server()
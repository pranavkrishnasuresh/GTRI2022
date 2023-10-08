#!/usr/bin/env python

import json
from os.path import exists
import rospy
from point_loader.srv import poseSend
from tf.transformations import euler_from_quaternion
import math

def handle_write(req):
    print("Adding poseStamped " + req.name)
    return send_to_json(req.name, pose_to_list(req.Pose))


def poseSend_server():                                    
    rospy.init_node("poseSend_server")
    s = rospy.Service("poseSend_write", poseSend, handle_write)
    print("Ready to write")
    rospy.spin()

path_name = "wbyrnes3"

def send_to_json(name, pose_data):
    if not exists('/home/{}/pose_file.json'.format(path_name)):
        with open('/home/{}/pose_file.json'.format(path_name), 'w') as json_file:
            json.dump({}, json_file)
            print("here!")
    with open('/home/{}/pose_file.json'.format(path_name), 'r') as json_file:
        json_dict_old = json.load(json_file)
        json_dict_old[name] = pose_data
    with open('/home/{}/pose_file.json'.format(path_name), 'w') as json_file:
        json.dump(json_dict_old, json_file)
        return 1

def pose_to_list(p):
    euler = euler_from_quaternion((p.pose.orientation.x,p.pose.orientation.y,p.pose.orientation.z, p.pose.orientation.w))
    return [p.header.frame_id, p.pose.position.x, p.pose.position.y, p.pose.position.z, math.degrees(euler[0]), math.degrees(euler[1]), math.degrees(euler[2])]

if __name__ == '__main__':
    poseSend_server()

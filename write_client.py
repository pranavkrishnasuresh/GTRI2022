#!/usr/bin/env python

import sys
import rospy
from point_loader.srv import poseSend 

# pose Send client with error handling 
def poseSend_client(name_arg, pose_data):
    rospy.wait_for_service('poseSend_write')
    try:
        poseSend_write = rospy.ServiceProxy('poseSend_write', poseSend)
        return poseSend_write(name_arg,pose_data)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

# usage which retreives first argument from the cmd line
def usage():
    return "%s [name] [pose]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        name = sys.argv[1]
        pose = sys.argv[2]
    else:
        print(usage())
        sys.exit(1)
    print("Sending %s and %s"%(name, pose))
    print(poseSend_client(name, pose))
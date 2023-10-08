#!/usr/bin/env python

import sys
import rospy
from point_loader.srv import poseRequest

# pose request client with error handling 
def poseRequest_client(name_arg):
    rospy.wait_for_service('poseRequest_read')
    try:
        postRequest_read = rospy.ServiceProxy('poseRequest_read', poseRequest)
        return postRequest_read(name_arg)
    except rospy.ServiceException as e:
        print("Service read call failed: %s"%e)

# usage which retreives first argument from the cmd line
def usage():
    return "%s [pose name]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        name = sys.argv[1]
    else:
        print(usage())
        sys.exit(1)
    print("Requesting %s"%(name))
    print(poseRequest_client(name))

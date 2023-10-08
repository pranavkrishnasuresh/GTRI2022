#!/usr/bin/env python

import rospy
from wellplate_grab.srv import gripperCommand
from os import path
import rospy
import serial

def handle_gripper(req):
    print("Sending command [1=close, 0=open]: {} ".format(req.open_close))
    serial_device = "/dev/ttyACM1"
    sd = SerialDriver(serial_device, "gripperCommand_server", debug=True)
    if req.open_close == 0:
        gripper_command = "close" # need to implement logic to find what command to send
    elif req.open_close == 1:
        gripper_command = "open" 
    sd._send_command(gripper_command, serial_device)
    return sd._get_feedback(serial_device)

# initializes the service and calls the handle_read function to retreive the data
def gripperCommand_server():                                    
    rospy.init_node("gripperCommand_server")
    s = rospy.Service("gripperCommand_send", gripperCommand, handle_gripper)
    print("Ready to send command")
    rospy.spin()


class SerialDriver:

    def __init__(self, serial_device_info, node_name="serial_driver", debug=False):

        # Initialize ros node
        rospy.init_node(node_name)
        self.debug = debug
        self.conn = None

        # Import rosparam values
        self.serial_device_info = rospy.get_param("~serial_device", default=serial_device_info)
        self.timeout = rospy.get_param("~command_timeout", default=1.0)
        self.baudrate = rospy.get_param("~baudrate", default=None)
        conn_timeout = rospy.get_param("~conn_timeout", default=5)
        confirm_conn = rospy.get_param("~confirm_connect", default=True)

        # connect to serial device
        connected = False
        stime = rospy.get_rostime().to_sec()
        while not connected and rospy.get_rostime().to_sec() < stime + 5:
            try:
                self.connect_to_device()
                connected = True
            except (serial.serialutil.SerialException, FileNotFoundError):
                if confirm_conn == True:
                    rospy.logwarn(
                        "Unable to connect to device %s, retrying...",
                        self.serial_device_info)
                    rospy.sleep(rospy.Duration(0.5))
                else:
                    rospy.loginfo("Serial driver unable to connect to hardware, using sim HW.")
                    connected = True  # Spoof connection
        
        if not connected:
            rospy.logerr("Could not connect to serial device %s after %d seconds, aborting setup.",self.serial_device_info, conn_timeout)
            return

        # roslog connection info
        if self.debug:
            rospy.loginfo("Device " + self.serial_device_info + " connected. Params:\n"+ "Command File: " + command_file + "\n"+ "Command Length: " + str(self.cmd_len) + "\n")

        rospy.loginfo("Serial_driver initialized successfully.")
        rospy.spin()

    def connect_to_device(self):
        """ Open a serial connection to the specified device. """

        if isinstance(self.serial_device_info, str):
            # Open named port
            self.conn = serial.Serial()
            self.conn.port = self.serial_device_info
            self.conn.timeout = self.timeout
            if self.baudrate is not None:
                self.conn.baudrate = int(self.baudrate)
            self.conn.open()

        elif isinstance(self.serial_device_info, dict):
            # Open unnamed port
            self.conn = serial.Serial()
            raise NotImplementedError  # TODO: Parse out dictionary params
            # self.conn.open()

        else:
            rospy.logerr("Device specification must be of type string or dictionary, not " + str(type(self.serial_device_info)))
            raise TypeError

        if not self.conn.is_open:
            rospy.logerr("Unable to open connection to " + str(self.serial_device_info))
            raise ConnectionError

    def _send_command(command, conn):
        """ Send the provided serial command to the attached device. """

        rospy.loginfo("Sending command " + str(command))
        cmd_bytes = command.encode('utf8')
        conn.write(cmd_bytes)

    def _get_feedback(conn):
        """Return feedback from device as a String."""

        # Flush commands and read all feedback
        conn.flush()
        res = conn.readlines()

        if len(res) == 0:
            res = "No feedback received."
        else:
            res = "\n".join([r.decode("utf8") for r in res])  # Join all lines into single string

        return res

if __name__ == '__main__':
    gripperCommand_server()
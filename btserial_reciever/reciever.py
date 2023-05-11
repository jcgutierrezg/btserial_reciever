#!/usr/bin/env python3 

from warnings import catch_warnings
import rclpy
import time
import serial
import json
from geometry_msgs.msg import Vector3
from rclpy.node import Node


class btreciever(Node):

    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/pts/1', 9600, timeout=1)
            self.ser.reset_input_buffer()   
            print("Conexion Serial exitosa")     
        except Exception:
            pass
        super().__init__('BTReciever')
        self.RPYinfo = self.create_publisher(Vector3,'RPYinfo',10)
        while rclpy.ok():
            self.ser = serial.Serial('/dev/pts/1', 9600, timeout=1)
            #if self.ser.in_waiting > 0:
            if 1:
                #print("R")
                #line = serial.Serial('/dev/pts/1', 9600, timeout=1).read_until('\n').decode('utf-8').rstrip()
                line = "10;20;30"
                print(line)
                #print("P")

                splitString = line.split(";")
                if len(splitString) == 3:

                    roll = splitString[0]
                    pitch = splitString[1]
                    yaw = splitString[2]
                    msg = Vector3()
                    msg.x = float(roll) 
                    msg.y = float(pitch) 
                    msg.z = float(yaw)
                
                    self.RPYinfo.publish(msg)
                    print("sent")


    
def main(args=None):
    rclpy.init(args=args)
    BTReciever=btreciever()
    rclpy.spin(BTReciever)
    BTReciever.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

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
            self.ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
            self.ser.reset_input_buffer()   
            print("Conexion Serial exitosa")     
        except Exception:
            pass
        super().__init__('BTReciever')
        self.RPYinfo = self.create_publisher(Vector3,'RPYinfo',10)
        while rclpy.ok():
            self.ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
            if self.ser.in_waiting > 0:
                print("R")
                line = serial.Serial('/dev/rfcomm0', 9600, timeout=1).readline().decode('utf-8').rstrip()
                print(line)
                print("P")
                splitString = line.split(";")
                roll = splitString[1]
                pitch = splitString[2]
                yaw = splitString[3]
                msg = Vector3()
                msg.x = roll 
                msg.y = pitch
                msg.z = yaw
                
                self.RPYinfo.publish(msg)


    
def main(args=None):
    rclpy.init(args=args)
    BTReciever=btreciever()
    rclpy.spin(BTReciever)
    BTREciever.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

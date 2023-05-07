#!/usr/bin/env python3 

from warnings import catch_warnings
import rclpy
import time
import serial
import json
from std_msgs.msg import String
from rclpy.node import Node

# Este codigo sirve para la comunicacion serial entre una ESP y una Raspberry. Es un nodo de ros2 que publica el mensaje entregado 
# por la ESP en el tópico "respuestaESP". Los mensajes son tipo String. 

# Este codigo es para ROS2.

class btreciever(Node):

    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
            self.ser.reset_input_buffer()   
            print("Conexion Serial exitosa")     
        except Exception:
            pass
        super().__init__('BTReciever')
        self.RPYinfo = self.create_publisher(String,'RPYinfo',10)
        while rclpy.ok():
            self.ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
            if self.ser.in_waiting > 0:
                print("R")
                line = serial.Serial('/dev/rfcomm0', 9600, timeout=1).readline().decode('utf-8').rstrip()
                msg = String()
                msg.data=line
                print(line)
                print("P")
                self.RPYinfo.publish(msg)


    
def main(args=None):
    rclpy.init(args=args)
    BTReciever=btreciever()
    rclpy.spin(BTReciever)
    BTREciever.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

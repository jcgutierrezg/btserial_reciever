from statemachine import StateMachine, State
import time

from warnings import catch_warnings
import rclpy
import serial
import json
from geometry_msgs.msg import Pose
from rclpy.node import Node


posX = 0
posY = 0
posZ = 0
oriX = 0
oriY = 0
oriZ = 0

angle1 = 0.0 
angle2 = 0.0
angle3 = 0.0
angle4 = 0.0
angle5 = 0.0
angle6 = 0.0

roll = 0
pitch = 0
yaw = 0
JoyX = 0
JoyY = 0
button = 0

switchFlag1 = 0
switchFlag2 = 0
switchFlag3 = 0
switchFlag4 = 0
switchFlag5 = 0
switchFlag6 = 0

posXhome = 0
posYhome = -0.2
posZhome = 0.5

NullFlag = 0
 

class MasterGlove(StateMachine):
 
    # creating states
    Start = State("Start", initial = True)
    Null = State("Null")
    #ButtonIn = State("ButtonIn")
    InverseKin = State("InverseKin")
    RPY = State("RPY")
    Home = State("Home")
    DirectKin = State("DirectKin")
    Disable = State("Disable")
      
    # transitions of the state
    initiate = Start.to(Null)

    InverseKin_Null = InverseKin.to(Null)
    RPY_Null = RPY.to(Null)
    Home_Null = Home.to(Null)
    DirectKin_Null = DirectKin.to(Null)
    Disable_Null = Disable.to(Null)

    IKMode = Null.to(InverseKin)
    RPYMode = Null.to(RPY)
    HomeMode = Null.to(Home)
    DKMode = Null.to(DirectKin)
    DisableMode = Null.to(Disable)

    def __init__(self):
        self.IK_Axis = 0
        self.DK_Pair = 0
        super(MasterGlove, self).__init__()


    def NullState(self):

        global NullFlag, button

        if(NullFlag == 1):
            time.sleep(0.5)
            button = 0
            NullFlag = 0

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper() 

        elif(button == 3):

            HomeMode()

        elif(button == 4):

            RPYMode()

        elif(button == 5):

            IKMode()

        elif(button == 6):

            DKMode()

        else:
            pass

    def InverseKinState(self):

        global NullFlag, button, switchFlag5, switchFlag5time, posX, JoyX, posY, JoyY, posZ

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 3):
                NullFlag = 1
                InverseKin_Null()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                moveItExec()
            else:
                moveItPlan()

        elif(button == 5):

            if(time.time()-switchFlag5time >= 0.5):
                switchFlag5 = 0
            
            if(self.IK_Axis == 0 and switchFlag5 == 0):

                self.IK_Axis = 1
                switchFlag5 = 1
                switchFlag5time = time.time()
            
            elif(self.IK_Axis == 1 and switchFlag5 == 0):

                self.IK_Axis = 0
                switchFlag5 = 1
                switchFlag5time = time.time()

        else:

            if(self.IK_Axis == 0):

                if(JoyX>100 and JoyX<156):

                    posX = posX

                elif(JoyX>=156):

                    posX = posX + (JoyX/128-1)

                elif(JoyX<=100):

                    posX = posX - ((255-JoyX)/128-1)



                if(JoyY>100 and JoyY<156):

                    posY = posY

                elif(JoyY>=156):

                    posY = posY + (JoyY/128-1)

                elif(JoyY<=100):

                    posY = posY - ((255-JoyY)/128-1)

            else:

                if(JoyX>100 and JoyX<156):

                    posZ = posZ

                elif(JoyX>=156):

                    posZ = posZ + (JoyX/128-1)

                elif(JoyX<=100):

                    posZ = posZ - ((255-JoyX)/128-1)



                if(JoyY>100 and JoyY<156):

                    posY = posY

                elif(JoyY>=156):

                    posY = posY + (JoyY/128-1)

                elif(JoyY<=100):

                    posY = posY - ((255-JoyY)/128-1)


    def RPYState(self):

        global NullFlag, button, oriX, oriY, oriZ, roll, pitch, yaw

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 3):

                NullFlag = 1
                RPY_Null()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                moveItExec()
            else:
                moveItPlan()

        else:

            oriX = roll
            #etc

    def HomeState(self):

        global NullFlag, button, posX, posY, posZ, posXhome, posYhome, posZhome

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 3):
                NullFlag = 1
                Home_Null()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                moveItExec()
            else:
                moveItPlan()

        else:

            posX = posXhome

            posY = posYhome

            posZ = posZhome
            #etc

    def DirectKinState(self):

        global NullFlag, button, angle1, angle2, angle3, angle4, angle5, angle6, switchFlag5time, switchFlag5, JoyX, JoyY

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 3):
                NullFlag = 1
                DirectKin_Null()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove()

            if(totalTime >= 2.0):
                btreciever.writeATTinys(3.0)

            else:
                pass

        elif(button == 5):

            if(time.time()-switchFlag5time >= 0.5):
                switchFlag5 = 0
            
            if(self.DK_Pair == 0 and switchFlag5 == 0):

                self.DK_Pair = 1
                switchFlag5 = 1
                switchFlag5time = time.time()
            
            elif(self.DK_Pair == 1 and switchFlag5 == 0):

                self.DK_Pair = 2
                switchFlag5 = 1
                switchFlag5time = time.time()

            elif(self.DK_Pair == 2 and switchFlag5 == 0):

                self.DK_Pair = 0
                switchFlag5 = 1
                switchFlag5time = time.time()

        else:

            if(self.DK_Pair == 0):

                if(JoyX>100 and JoyX<156):

                    angle1 = angle1

                elif(JoyX>=156):

                    angle1 = angle1 + (JoyX/128-1)

                elif(JoyX<=100):

                    angle1 = angle1 - ((255-JoyX)/128-1)



                if(JoyY>100 and JoyY<156):

                    angle2 = angle2

                elif(JoyY>=156):

                    angle2 = angle2 + (JoyY/128-1)

                elif(JoyY<=100):

                    angle2 = angle2 - ((255-JoyY)/128-1)

            elif(self.DK_Pair == 1):

                if(JoyX>100 and JoyX<156):

                    angle3 = angle3

                elif(JoyX>=156):

                    angle3 = angle3 + (JoyX/128-1)

                elif(JoyX<=100):

                    angle3 = angle3 - ((255-JoyX)/128-1)



                if(JoyY>100 and JoyY<156):

                    angle4 = angle4

                elif(JoyY>=156):

                    angle4 = angle4 + (JoyY/128-1)

                elif(JoyY<=100):

                    angle4 = angle4 - ((255-JoyY)/128-1)

            else:

                if(JoyX>100 and JoyX<156):

                    angle5 = angle5

                elif(JoyX>=156):

                    angle5 = angle5 + (JoyX/128-1)

                elif(JoyX<=100):

                    angle5 = angle5 - ((255-JoyX)/128-1)



                if(JoyY>100 and JoyY<156):

                    angle6 = angle6

                elif(JoyY>=156):

                    angle6 = angle6 + (JoyY/128-1)

                elif(JoyY<=100):

                    angle6 = angle6 - ((255-JoyY)/128-1)


class btreciever(Node):

    def __init__(self):
        global glove
        try:
            self.ser = serial.Serial('/dev/pts/1', 9600, timeout=1)
            self.ser.reset_input_buffer()   
            print("Conexion Serial exitosa")     
        except Exception:
            pass
        super().__init__('BTReciever')
        self.RPYinfo = self.create_publisher(Pose,'RPYinfo',10)
        self.ATTinyinfo = self.create_publisher(Pose,'ATTinyInfo',10)
        while(rclpy.ok()):
            masterCycle(self, glove)

    def readGlove(self):

        global roll, pitch, yaw, JoyX, JoyY, button

        #self.ser = serial.Serial('/dev/pts/1', 9600, timeout=1)
        #if self.ser.in_waiting > 0:
        if 1:
            #print("R")
            #line = serial.Serial('/dev/pts/1', 9600, timeout=1).read_until('\n').decode('utf-8').rstrip()
            line = "10;20;30;128;128;0"
            print(line)
            #print("P")

            splitString = line.split(";")
            if len(splitString) == 6:

                roll = splitString[0]
                pitch = splitString[1]
                yaw = splitString[2]
                JoyX = splitString[3]
                JoyY = splitString[4]
                button = splitString[5]

    def publishPose(self):

        global posX, posY, posZ, roll, pitch, yaw

        msg = Pose()

        msg.position.x = float(posX)
        msg.position.y = float(posY)
        msg.position.z = float(posZ)

        msg.orientation.w = float(0.0)
        msg.orientation.x = float(roll)
        msg.orientation.y = float(pitch)
        msg.orientation.z = float(yaw)

        self.RPYinfo.publish(msg)
        print("Sent Pose")

    def publishATTiny(self, Mode):

        global angle1, angle2, angle3, angle4, angle5, angle6

        msg = Pose()

        msg.position.x = float(angle1)
        msg.position.y = float(angle2)
        msg.position.z = float(angle3)

        msg.orientation.w = float(Mode)
        msg.orientation.x = float(angle4)
        msg.orientation.y = float(angle5)
        msg.orientation.z = float(angle6)

        self.ATTinyinfo.publish(msg)
        print("Sent Pose")

        angle1 = 0.0
        angle2 = 0.0
        angle3 = 0.0
        angle4 = 0.0
        angle5 = 0.0
        angle6 = 0.0




def masterCycle(btrecieverN, gloveS):

    while(gloveS.Null.is_active):
        btrecieverN.readGlove()
        gloveS.NullState()
        #btrecieverN.publishPose()

    while(gloveS.InverseKin.is_active):
        btrecieverN.readGlove()
        gloveS.InverseKinState()
        btrecieverN.publishPose()

    while(gloveS.RPY.is_active):
        btrecieverN.readGlove()
        gloveS.RPYState()
        btrecieverN.publishPose()

    while(gloveS.Home.is_active):
        btrecieverN.readGlove()
        gloveS.HomeState()
        btrecieverN.publishPose()

    while(gloveS.DirectKin.is_active):
        btrecieverN.readGlove()
        gloveS.DirectKinState()

def switchLaser():
    global angle1, angle2, angle3, angle4, angle5, angle6

    angle1 = 0.0
    angle2 = 0.0
    angle3 = 0.0
    angle4 = 0.0
    angle5 = 0.0
    angle6 = 0.0

    btreciever.publishATTiny(btreciever, 1.0)

def switchGripper():

    global angle1, angle2, angle3, angle4, angle5, angle6

    angle1 = 0.0
    angle2 = 0.0
    angle3 = 0.0
    angle4 = 0.0
    angle5 = 0.0
    angle6 = 0.0

    btreciever.publishATTiny(btreciever, 2.0)

def moveItPlan():
    test = 1

def moveItExec():
    test = 1


def main(args=None):
    global glove 
    glove = MasterGlove()
    glove.initiate()
    rclpy.init(args=args)
    BTReciever=btreciever()
    rclpy.spin(BTReciever)
    BTReciever.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


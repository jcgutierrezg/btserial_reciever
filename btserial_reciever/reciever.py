from statemachine import StateMachine, State
import time
import requests

from warnings import catch_warnings
import rclpy
import serial
import json
from geometry_msgs.msg import Pose
from rclpy.node import Node

url = "http://192.168.75.70/pose"

posX = 0
posY = 0
posZ = 0
OriX = 0
OriY = 0
OriZ = 0

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
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper() 

        else:
            pass

    def InverseKinState(self):

        global NullFlag, button, posX, JoyX, posY, JoyY, posZ, currentSubstate

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                moveItExec()
            else:
                moveItPlan()


        else:

            if(currentSubstate == 1):

                if(JoyX>500 and JoyX<540):

                    posX = posX

                elif(JoyX>=540):

                    posX = posX - (JoyX/512-1)/1000

                elif(JoyX<=500):

                    posX = posX + ((1023-JoyX)/512-1)/1000



                if(JoyY>500 and JoyY<540):

                    posY = posY

                elif(JoyY>=540):

                    posY = posY - (JoyY/512-1)/1000

                elif(JoyY<=500):

                    posY = posY + ((1023-JoyY)/512-1)/1000

            else:

                if(JoyX>500 and JoyX<540):

                    posZ = posZ

                elif(JoyX>=540):

                    posZ = posZ - (JoyX/512-1)/1000

                elif(JoyX<=500):

                    posZ = posZ + ((1023-JoyX)/512-1)/1000



                if(JoyY>500 and JoyY<540):

                    posY = posY

                elif(JoyY>=540):

                    posY = posY - (JoyY/512-1)/1000

                elif(JoyY<=500):

                    posY = posY + ((1023-JoyY)/512-1)/1000


    def RPYState(self):

        global NullFlag, button, roll, pitch, yaw, OriX, OriY, OriZ

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                moveItExec()
            else:
                moveItPlan()
        else:

            OriX = roll
            OriY = pitch
            OriZ = yaw
            

    def HomeState(self):

        global NullFlag, button, posX, posY, posZ, posXhome, posYhome, posZhome, OriX, OriY, OriZ

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                moveItExec()
            else:
                moveItPlan()

        else:

            posX = posXhome

            posY = posYhome

            posZ = posZhome

            OriX = 0.0

            OriY = 0.0

            OriZ = 0.0


            #etc

    def DirectKinState(self):

        global NullFlag, button, angle1, angle2, angle3, angle4, angle5, angle6, currentSubstate, JoyX, JoyY

        if(button == 2):
            startTime = time.time()

            while(button == 2):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                switchLaser()
            else:
                switchGripper()

        elif(button == 1):
            startTime = time.time()

            while(button == 1):
                currentTime = time.time()

                totalTime = currentTime-startTime
                btreciever.readGlove(self)

            if(totalTime >= 2.0):
                btreciever.writeATTinys(self, 3.0)

            else:
                pass

        else:

            if(currentSubstate == 1):

                if(JoyX>500 and JoyX<540):

                    angle1 = angle1

                elif(JoyX>=540):

                    angle1 = angle1 + (JoyX/512-1)

                elif(JoyX<=500):

                    angle1 = angle1 - ((1023-JoyX)/512-1)



                if(JoyY>500 and JoyY<540):

                    angle2 = angle2

                elif(JoyY>=540):

                    angle2 = angle2 + (JoyY/512-1)

                elif(JoyY<=500):

                    angle2 = angle2 - ((1023-JoyY)/512-1)

            elif(currentSubstate == 2):

                if(JoyX>500 and JoyX<540):

                    angle3 = angle3

                elif(JoyX>=540):

                    angle3 = angle3 + (JoyX/512-1)

                elif(JoyX<=500):

                    angle3 = angle3 - ((1023-JoyX)/512-1)



                if(JoyY>500 and JoyY<540):

                    angle4 = angle4

                elif(JoyY>=540):

                    angle4 = angle4 + (JoyY/512-1)

                elif(JoyY<=500):

                    angle4 = angle4 - ((1023-JoyY)/512-1)

            else:

                if(JoyX>500 and JoyX<540):

                    angle5 = angle5

                elif(JoyX>=540):

                    angle5 = angle5 + (JoyX/512-1)

                elif(JoyX<=500):

                    angle5 = angle5 - ((1023-JoyX)/512-1)



                if(JoyY>500 and JoyY<540):

                    angle6 = angle6

                elif(JoyY>=540):

                    angle6 = angle6 + (JoyY/512-1)

                elif(JoyY<=500):

                    angle6 = angle6 - ((1023-JoyY)/512-1)


class btreciever(Node):

    def __init__(self):
        global glove
        super().__init__('BTReciever')
        self.RPYinfo = self.create_publisher(Pose,'RPYinfo',10)
        self.ATTinyinfo = self.create_publisher(Pose,'ATTinyinfo',10)
        while(rclpy.ok()):
            masterCycle(self, glove)

    def readGlove(self):

        global roll, pitch, yaw, JoyX, JoyY, button, currentState, currentSubstate

        response = requests.get(url)

        if(response.status_code == 200):
            line = response.text

        #print(line)
        #line = "10;20;30;128;128;0"
        #print(line)
        #print("P")
        splitString = line.split(";")
        if len(splitString) == 8:

            roll = float(splitString[0])
            pitch = float(splitString[1])
            yaw = float(splitString[2])
            JoyX = int(splitString[3])
            JoyY = int(splitString[4])
            button = int(splitString[5])
            currentState = int(splitString[6])
            currentSubstate = int(splitString[7])

    def publishPose(self):

        global posX, posY, posZ, OriX, OriY, OriZ

        msg = Pose()

        msg.position.x = float(posX)
        msg.position.y = float(posY)
        msg.position.z = float(posZ)

        msg.orientation.w = float(0.0)
        msg.orientation.x = float(OriX)
        msg.orientation.y = float(OriY)
        msg.orientation.z = float(OriZ)

        print(posX)
        print(posY)
        print(posZ)
        print(OriX)
        print(OriY)
        print(OriZ)

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

    global currentState

    while(gloveS.Null.is_active):
        btrecieverN.readGlove()
        gloveS.NullState()
        #print(currentState)
        print("Null")

        if(currentState == 2):

            gloveS.IKMode()

        elif(currentState == 3):

            gloveS.RPYMode()

        elif(currentState == 4):

            gloveS.HomeMode()

        elif(currentState == 5):

            gloveS.DKMode()
        #btrecieverN.publishPose()

    while(gloveS.InverseKin.is_active):
        btrecieverN.readGlove()
        gloveS.InverseKinState()
        btrecieverN.publishPose()
        print("IK")
        if(currentState != 2):

            gloveS.InverseKin_Null()

    while(gloveS.RPY.is_active):
        btrecieverN.readGlove()
        gloveS.RPYState()
        btrecieverN.publishPose()
        print("RPY")
        if(currentState != 3):

            gloveS.RPY_Null()

    while(gloveS.Home.is_active):
        btrecieverN.readGlove()
        gloveS.HomeState()
        btrecieverN.publishPose()
        print("Home")
        if(currentState != 4):

            gloveS.Home_Null()

    while(gloveS.DirectKin.is_active):
        btrecieverN.readGlove()
        gloveS.DirectKinState()
        print("DK")
        if(currentState != 5):

            gloveS.DirectKin_Null()

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


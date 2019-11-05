import socket
import time
import webbrowser
import pygame
import smtplib
from email.mime.text import MIMEText

# please connect to ARA's Wi-Fi before running program - PASSWORD: 12345678
class ARA:
    def __init__(self):
        # used to open the socket and send commands (packets) to ARA (Raspberry Pi 3) through its Wi-Fi
        # double check these are correct by using Wireshark to packet sniff when connected to ARA's Wi-Fi
        self.ip = "192.168.1.1"
        self.port = 2001
        self.stop = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])
        self.forward = bytearray([0xFF, 0x00, 0x04, 0x00, 0xFF])
        self.backward = bytearray([0xFF, 0x00, 0x03, 0x00, 0xFF])
        self.left = bytearray([0xFF, 0x00, 0x01, 0x00, 0xFF])
        self.right = bytearray([0xFF, 0x00, 0x02, 0x00, 0xFF])
        self.clawOpen = bytearray([0xFF, 0x01, 0x04, 0x56, 0xFF])
        self.clawClose = bytearray([0xFF, 0x01, 0x04, 0xab, 0xFF])
        self.clawHorizontal = bytearray([0xFF, 0x01, 0x03, 0x56, 0xFF])
        self.clawVertical = bytearray([0xFF, 0x01, 0x03, 0xab, 0xFF])

    def getIP(self):
        return self.ip

    def setIP(self, ip):
        self.ip = ip

    def getPort(self):
        return self.port

    def setPort(self, port):
        self.port = port

    def sendCommand(self, command):
        '''

        :param: command as a byte array sent over Wi-Fi to ARA
        :return: N/A

        Sends a command to ARA through Wi-Fi. The command must be a byte array.
        '''

        ara = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ara.connect((self.getIP(), self.getPort()))
        ara.send(command)

    def stopMovement(self):
        '''

        :param: N/A
        :return: N/A

        Sends stop command to ARA using stop attribute defined in the constructor.
        '''

        print("Sending stop command.")
        self.sendCommand(self.stop)

    def moveForward(self):
        '''

        :param: N/A
        :return: N/A

        Sends move forward command to ARA using forward attribute defined in the constructor.
        '''

        print("Sending forward command.")
        self.sendCommand(self.forward)

    def moveBackward(self):
        '''

        :param: N/A
        :return: N/A

        Sends move backward command to ARA using backward attribute defined in the constructor.
        '''

        print("Sending backward command.")
        self.sendCommand(self.backward)

    def turnLeft(self):
        '''

        :param: N/A
        :return: N/A

        Sends turn left command to ARA using left attribute defined in the constructor.
        '''

        print("Sending turn left command.")
        self.sendCommand(self.left)

    def turnRight(self):
        '''

        :param: N/A
        :return: N/A

        Sends turn right command to ARA using right attribute defined in the constructor.
        '''

        print("Sending turn right command.")
        self.sendCommand(self.right)

    def clawControl(self, pos):
        '''

        :param pos: enter 0 to close claw or 1 to open claw
        :return: N/A

        Sends claw open or close command to ARA using the claw open and close attributes
        defined in the constructor.
        '''

        if pos == 1:
            print("Sending claw open command.")
            self.sendCommand(self.clawOpen)
        else:
            print("Sending claw close command.")
            self.sendCommand(self.clawClose)

    def clawRotate(self, pos):
        '''

        :param pos: enter 0 to rotate the claw to its vertical position or
        1 to rotate it to its horizontal position
        :return: N/A

        Sends claw rotate command to ARA using the claw horizontal and vertical attributes
        defined in the constructor.
        '''

        if pos == 1:
            print("Sending claw rotate horizontal command.")
            self.sendCommand(self.clawHorizontal)
        else:
            print("Sending claw rotate vertical command.")
            self.sendCommand(self.clawVertical)


# variables used to open socket and send commands
# MAKE SURE TO CHANGE THE IP ADDRESS TO THE IP OF THE RASPBERRY PI ON ARA
IP = "192.168.1.1"
PORT = 2001

def stopMovement():
    '''

    :param N/A
    :return: N/A

    Sends stop command to ARA while movement keys
    aren't being pressed in main loop.
    '''

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    c.send(stopData)
    print("Stop command sent.")

def forward(dist):
    '''

    :param dist: distance in 6 inches to move ARA forward
    :return: N/A
    '''

    # speed for motors (left set to 70, right set to 68)
    forwardleftSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])
    forwardrightSpeed = bytearray([0xFF, 0x02, 0x02, 0x44, 0xFF])

    # used to send the forward command
    forwardData = bytearray([0xFF, 0x00, 0x04, 0x00, 0xFF])

    # used to send the turn right command
    turnRightData = bytearray([0xFF, 0x00, 0x02, 0x00, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print ("Opening socket...")
    c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print ("Socket opened.")
    print ("Sending left speed for forward command...")
    c.send(forwardleftSpeed)
    print ("Command sent.")
    print ("Sending right speed for forward command...")
    c.send(forwardrightSpeed)
    print ("Command sent.")

    for i in range(dist):

        print("Sending forward command...")
        c.send(forwardData)
        print("Command sent.")
        print("Pausing for a second...")
        time.sleep(1)
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")
        print("Adjusting position based on error.")
        print("Sending turn right command...")
        c.send(turnRightData)
        print("Command sent.")
        print("Pausing for about 2/10 of a second...")
        time.sleep(0.150)
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def backward(dist):
    '''

    :param dist: distance in 6 inches to move ARA backward
    :return: N/A
    '''

    # speed for motors (left set to 68, right set to 70)
    backwardleftSpeed = bytearray([0xFF, 0x02, 0x01, 0x44, 0xFF])
    backwardrightSpeed = bytearray([0xFF, 0x02, 0x02, 0x46, 0xFF])

    # used to send the forward command
    backwardData = bytearray([0xFF, 0x00, 0x03, 0x00, 0xFF])

    # used to send the turn left command
    turnLeftData = bytearray([0xFF, 0x00, 0x01, 0x00, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")
    print("Sending left speed for backward command...")
    c.send(backwardleftSpeed)
    print("Command sent.")
    print("Sending right speed for backward command...")
    c.send(backwardrightSpeed)
    print("Command sent.")

    for i in range(dist):
        print("Sending backward command...")
        c.send(backwardData)
        print("Command sent.")
        print("Pausing for a second...")
        time.sleep(1)
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")
        print("Adjusting position based on error.")
        print("Sending turn left command...")
        c.send(turnLeftData)
        print("Command sent.")
        print("Pausing for about 1/10 of a second...")
        time.sleep(0.050)
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def turnLeft(deg):
    '''

    :param deg: degrees by an interval of 90 to turn ARA left
    :param dist: distance in 6 inches to move ARA forward
    :return: N/A
    '''

    # speed for motors (left set to 70, right set to 70)
    turningLeftLeftSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])
    turningLeftRightSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])

    # used to send the turn left command
    turnLeftData = bytearray([0xFF, 0x00, 0x01, 0x00, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")
    print("Sending left speed for turn left command...")
    c.send(turningLeftLeftSpeed)
    print("Command sent.")
    print("Sending right speed for turn left command...")
    c.send(turningLeftRightSpeed)
    print("Command sent.")

    for i in range(deg):
        print("Sending turn left command...")
        c.send(turnLeftData)
        print("Command sent.")
        print("Pausing for 3/4 of a second...")
        time.sleep(0.75)
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def turnRight(deg):
    '''

    :param deg: degrees by an interval of 90 to turn ARA right
    :param dist: distance in 6 inches to move ARA forward
    :return: N/A
    '''

    # speed for motors (left set to 70, right set to 70)
    turningRightLeftSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])
    turningRightRightSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])

    # used to send the turn left command
    turnRightData = bytearray([0xFF, 0x00, 0x02, 0x00, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")
    print("Sending left speed for turn right command...")
    c.send(turningRightLeftSpeed)
    print("Command sent.")
    print("Sending right speed for turn right command...")
    c.send(turningRightRightSpeed)
    print("Command sent.")

    for i in range(deg):
        print("Sending turn right command...")
        c.send(turnRightData)
        print("Command sent.")
        print("Pausing for about a second...")
        time.sleep(0.85)
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def clawClench(pos):
    '''

    :param pos: enter 0 to clench claw or 1 to open
    :return: N/A
    '''

    # used to send the claw clench command
    clawClenchDataOpen = bytearray([0xFF, 0x01, 0x04, 0x56, 0xFF])
    clawClenchDataClose = bytearray([0xFF, 0x01, 0x04, 0xab, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")

    if pos == 1:
        print("Sending claw open command...")
        c.send(clawClenchDataOpen)
        print("Claw open command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    else:
        print("Sending claw close command...")
        c.send(clawClenchDataClose)
        print("Claw close command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def clawRotate(pos):
    '''

    :param pos: enter 0 to rotate claw vertical or 1 to rotate it horizontally
    :return: N/A
    '''

    # used to send the claw rotate command
    clawRotateDataPosHor = bytearray([0xFF, 0x01, 0x03, 0x56, 0xFF])
    clawRotateDataPosVert = bytearray([0xFF, 0x01, 0x03, 0xab, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")

    if pos == 1:
        print("Sending claw rotate horizontal command...")
        c.send(clawRotateDataPosHor)
        print("Claw rotate horizontal command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")


    else:
        print("Sending claw rotate vertical command...")
        c.send(clawRotateDataPosVert)
        print("Claw rotate vertical command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def armMidMove(pos):
    '''

    :param pos: enter 0 to move arm mid to lowest position, 1 to move to mid position, 2 to move to highest position
    :return: N/A
    '''

    # used to send the arm mid move command
    armMidDataLow = bytearray([0xFF, 0x01, 0x02, 0x00, 0xFF])
    armMidDataMid = bytearray([0xFF, 0x01, 0x02, 0x56, 0xFF])
    armMidDataHigh = bytearray([0xFF, 0x01, 0x02, 0xab, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")

    if pos == 1:
        print("Sending arm mid move mid command...")
        c.send(armMidDataMid)
        print("Arm mid move mid command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    elif pos == 2:
        print("Sending arm mid move high command...")
        c.send(armMidDataHigh)
        print("Arm mid move high command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    else:
        print("Sending arm mid move low command...")
        c.send(armMidDataLow)
        print("Arm mid move low command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def armBaseMove(pos):
    '''

    :param pos: enter 0 to move arm base to lowest position, 1 to move to mid position, 2 to move to highest position
    :return: N/A
    '''

    # used to send the arm base move command
    armBaseDataLow = bytearray([0xFF, 0x01, 0x01, 0x00, 0xFF])
    armBaseDataMid = bytearray([0xFF, 0x01, 0x01, 0x56, 0xFF])
    armBaseDataHigh = bytearray([0xFF, 0x01, 0x01, 0xab, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")

    if pos == 1:
        print("Sending arm base move mid command...")
        c.send(armBaseDataMid)
        print("Arm base move mid command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    elif pos == 2:
        print("Sending arm base move high command...")
        c.send(armBaseDataHigh)
        print("Arm base move high command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    else:
        print("Sending arm base move low command...")
        c.send(armBaseDataLow)
        print("Arm base move low command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def cameraPan(pos):
    '''

    :param pos: enter 0 to pan camera right, 1 to pan camera to mid, 2 to pan camera left
    :return: N/A
    '''

    # used to send the camera pan command
    cameraPanDataRight = bytearray([0xFF, 0x01, 0x07, 0x2b, 0xFF])
    cameraPanDataMid = bytearray([0xFF, 0x01, 0x07, 0x56, 0xFF])
    cameraPanDataLeft = bytearray([0xFF, 0x01, 0x07, 0xab, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")

    if pos == 1:
        print("Sending camera pan mid command...")
        c.send(cameraPanDataMid)
        print("Camera pan mid command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    elif pos == 2:
        print("Sending camera pan left command...")
        c.send(cameraPanDataLeft)
        print("Camera pan left command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    else:
        print("Sending camera pan right command...")
        c.send(cameraPanDataRight)
        print("Camera pan right command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def cameraTilt(pos):
    '''

    :param pos: enter 0 to tilt camera down, 1 to pan camera to mid, 2 to tilt camera up
    :return: N/A
    '''

    # used to send the camera tilt command
    cameraTiltDataDown = bytearray([0xFF, 0x01, 0x08, 0x00, 0xFF])
    cameraTiltDataMid = bytearray([0xFF, 0x01, 0x08, 0x32, 0xFF])
    cameraTiltDataUp = bytearray([0xFF, 0x01, 0x08, 0xab, 0xFF])

    # used to send the stop command
    stopData = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])

    print("Opening socket...")
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    print("Socket opened.")

    if pos == 1:
        print("Sending camera tilt mid command...")
        c.send(cameraTiltDataMid)
        print("Camera tilt mid command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    elif pos == 2:
        print("Sending camera tilt up command...")
        c.send(cameraTiltDataUp)
        print("Camera tilt up command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

    else:
        print("Sending camera tilt down command...")
        c.send(cameraTiltDataDown)
        print("Camera tilt down command sent.")
        print("Sending stop command...")
        c.send(stopData)
        print("Command sent.")

def cameraStream():

    # opening camera stream (http://192.168.1.1:8080/?action=stream)
    webbrowser.open("http://192.168.1.1:8080/?action=stream", new=0, autoraise=True)

def sms():

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # Use sms gateway provided by mobile carrier:
    # at&t:     number@mms.att.net
    # t-mobile: number@tmomail.net
    # verizon:  number@vtext.com
    # sprint:   number@page.nextel.com / pm.sprint.com

    server.starttls()

    server.login('affordablerobotassistant@gmail.com', 'aragetup320')

    # send message to Curt
    msg = MIMEText('Activity detected via ARA. Please check on Kofi.')
    msg["Subject"] = "ARA"
    msg["From"] = "affordablerobotassistant@gmail.com"
    msg["To"] = "2674756129@tmomail.net"
    server.send_message(msg)

    # send message to Kire
    msg = MIMEText('Activity detected via ARA. Please check on Kofi.')
    msg["Subject"] = "ARA"
    msg["From"] = "affordablerobotassistant@gmail.com"
    msg["To"] = "3024806121@pm.sprint.com"
    server.send_message(msg)

    # send message to Shamar
    msg = MIMEText('Activity detected via ARA. Please check on Kofi.')
    msg["Subject"] = "ARA"
    msg["From"] = "affordablerobotassistant@gmail.com"
    msg["To"] = "4435700079@tmomail.net"
    server.send_message(msg)

    # send message to me
    msg = MIMEText('Activity detected via ARA. Text messages sent to emergency contacts.')
    msg["Subject"] = "ARA"
    msg["From"] = "affordablerobotassistant@gmail.com"
    msg["To"] = "5163126540@pm.sprint.com"
    server.send_message(msg)

def controls():

    print("KEYBOARD CONTROLS: ")
    print("________________________")
    print("w: moves ARA forward 12 inches at a time")
    print("s: moves ARA backward 12 inches at a time")
    print("a: turns ARA left 90 degrees and moves her forward 6 inches")
    print("d: turns ARA right 90 degrees and moves her forward 6 inches")
    print("q: open ARA's claw")
    print("e: close ARA's claw")
    print("z: rotate ARA's claw to a vertical position")
    print("x: rotate ARA's claw to a horizontal position")
    print("i: move arm mid to highest position")
    print("k: move arm mid to middle position")
    print(",: move arm mid to lowest position")
    print("u: move arm base to highest position")
    print("j: move arm base to middle position")
    print("m: move arm base to lowest position")
    print("l: pan camera left")
    print(";: pan camera mid")
    print("': pan camera right")
    print("o: tilt camera down")
    print("p: tilt camera mid")
    print("[: tilt camera up")
    print("spacebar: starts ARA's camera stream")
    print("esc: sends text message to user")
    print("c: prints these controls")
    print("")
    print("")
    print("")
    print("PS4 CONTROLLER CONTROLS: ")
    print("________________________")
    print("R2: moves ARA forward 12 inches at a time")
    print("L2: moves ARA backward 12 inches at a time")
    print("L1: turns ARA left 90 degrees and moves her forward 6 inches")
    print("R1: turns ARA right 90 degrees and moves her forward 6 inches")
    print("circle: open ARA's claw")
    print("cross: close ARA's claw")
    print("square: rotate ARA's claw to a vertical position")
    print("triangle: rotate ARA's claw to a horizontal position")
    print("LS Up: move arm mid to highest position")
    print("L3: move arm mid to middle position")
    print("LS Down: move arm mid to lowest position")
    print("RS Up: move arm base to highest position")
    print("R3: move arm base to middle position")
    print("RS Down: move arm base to lowest position")
    print("Tilt Left: pan camera left")
    print("Tilt Up: pan camera mid")
    print("Tilt Right: pan camera right")
    print("Tilt Down: tilt camera mid")
    print("Down: tilt camera down")
    print("Up: tilt camera up")
    print("PS Button: starts ARA's camera stream")
    print("Share button: sends text message to user")
    print("options: prints these controls")

def testARA():
    '''
    tests the functionality of ARA's components
    :return: N/A
    '''
    print(" ----------------------------------------- TESTING -----------------------------------------")

    # testing the motors
    forward(1)
    time.sleep(1)
    backward(1)
    time.sleep(1)
    turnLeft(1)
    time.sleep(1)
    turnRight(1)
    time.sleep(1)

    # testing the claw
    clawClench(0)
    time.sleep(1)
    clawClench(1)
    time.sleep(1)
    clawRotate(0)
    time.sleep(1)
    clawRotate(1)
    time.sleep(1)

    # testing the arm
    armMidMove(0)
    time.sleep(1)
    armMidMove(2)
    time.sleep(1)
    armMidMove(1)
    time.sleep(1)
    armBaseMove(0)
    time.sleep(1)
    armBaseMove(1)
    time.sleep(1)
    armBaseMove(2)
    time.sleep(1)

    # testing the camera servo
    cameraPan(0)
    time.sleep(1)
    cameraPan(2)
    time.sleep(1)
    cameraPan(1)
    time.sleep(1)
    cameraTilt(0)
    time.sleep(1)
    cameraTilt(2)
    time.sleep(1)
    cameraTilt(1)

    # turning the camera stream on
    cameraStream()

    print(" -------------------------------------- TEST FINISHED --------------------------------------")

def commandARA():
    '''
    controls ARA while using a 2-D environment
    :return: N/A
    '''

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 40
    HEIGHT = 40

    # This sets the margin between each cell
    MARGIN = 10

    # creates a 2 dimensional array
    grid = []
    for row in range(7):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(7):
            grid[row].append(0)  # Append a cell

    # sets the initial position of ARA and the object
    araRow = 6
    araCol = 3
    grid[araRow][araCol] = 1

    objRow = 0
    objCol = 3
    grid[objRow][objCol] = 2

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [400, 400]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("ARA 2-D Environment")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    print("Initalizing Command ARA...")
    controls()

    # -------- Main Loop -----------

    while not done:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:
                # If user clicked close
                print("Fin.")
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:

                # move ARA forward
                if event.key == pygame.K_w:
                    forward(1)

                    grid[araRow][araCol] = 0
                    araRow -= 1
                    grid[araRow][araCol] = 1

                    print("ARA Grid coordinates: ", araRow, araCol)

                # move ARA backward
                elif event.key == pygame.K_s:
                    backward(1)

                    grid[araRow][araCol] = 0
                    araRow += 1
                    grid[araRow][araCol] = 1

                    print("ARA Grid coordinates: ", araRow, araCol)

                # move ARA left
                elif event.key == pygame.K_a:
                    turnLeft(1)
                    forward(1)
                    turnRight(1)

                    grid[araRow][araCol] = 0
                    araCol -= 1
                    grid[araRow][araCol] = 1

                    print("ARA Grid coordinates: ", araRow, araCol)

                # move ARA right
                elif event.key == pygame.K_d:
                    turnRight(1)
                    forward(1)
                    turnLeft(1)

                    grid[araRow][araCol] = 0
                    araCol += 1
                    grid[araRow][araCol] = 1

                    print("ARA Grid coordinates: ", araRow, araCol)

                # start ARA's camera stream
                elif event.key == pygame.K_SPACE:
                    cameraStream()

                # print ARA's controls
                elif event.key == pygame.K_c:
                    controls()

                # open ARA's claw
                elif event.key == pygame.K_q:
                    clawClench(1)

                # close ARA's claw
                elif event.key == pygame.K_e:
                    clawClench(0)

                # rotate ARA's claw to a vertical position
                elif event.key == pygame.K_z:
                    clawRotate(0)

                # rotate ARA's claw to a horizontal position
                elif event.key == pygame.K_x:
                    clawRotate(1)

                # move arm mid to highest position
                elif event.key == pygame.K_i:
                    armMidMove(2)

                # move arm mid to middle position
                elif event.key == pygame.K_k:
                    armMidMove(1)

                # move arm mid to lowest position
                elif event.key == pygame.K_COMMA:
                    armMidMove(0)

                # move arm base to highest position
                elif event.key == pygame.K_u:
                    armBaseMove(2)

                # move arm base to middle position
                elif event.key == pygame.K_j:
                    armBaseMove(1)

                # move arm base to lowest position
                elif event.key == pygame.K_m:
                    armBaseMove(0)

                # pan camera left
                elif event.key == pygame.K_l:
                    cameraPan(2)

                # pan camera mid
                elif event.key == pygame.K_SEMICOLON:
                    cameraPan(1)

                # pan camera right
                elif event.key == pygame.K_QUOTE:
                    cameraPan(0)

                # tilt camera upwards
                elif event.key == pygame.K_LEFTBRACKET:
                    cameraTilt(2)

                # tilt camera mid
                elif event.key == pygame.K_p:
                    cameraTilt(1)

                # tilt camera downwards
                elif event.key == pygame.K_o:
                    cameraTilt(0)

                # send text message to user
                elif event.key == pygame.K_ESCAPE:
                    sms()

                else:
                    print("Command not recognized. Press the 'c' key to see controls.")

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(7):
            for column in range(7):
                color = WHITE
                if grid[row][column] == 1:
                    color = GREEN
                elif grid[row][column] == 2:
                    color = BLUE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.pp
    pygame.quit()

def constForward():
    '''

    :param N/A
    :return: N/A

    Sends forward command to ARA while the
    'w' key is being pressed.
    '''

    # speed for motors (left set to 70, right set to 68)
    forwardleftSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])
    forwardrightSpeed = bytearray([0xFF, 0x02, 0x02, 0x44, 0xFF])

    # used to send the forward command
    forwardData = bytearray([0xFF, 0x00, 0x04, 0x00, 0xFF])

    # opens socket and sends speed to motors for forward command
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    c.send(forwardleftSpeed)
    c.send(forwardrightSpeed)
    c.send(forwardData)
    print("Forward command sent.")

def constBackward():
    '''

    :param N/A
    :return: N/A

    Sends backward command to ARA while the
    's' key is being pressed.
    '''

    # speed for motors on ARA (left set to 68, right set to 70)
    backwardleftSpeed = bytearray([0xFF, 0x02, 0x01, 0x44, 0xFF])
    backwardrightSpeed = bytearray([0xFF, 0x02, 0x02, 0x46, 0xFF])

    # used to send the backward command
    backwardData = bytearray([0xFF, 0x00, 0x03, 0x00, 0xFF])

    # opens socket and sends speed to motors for backwards command
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    c.send(backwardleftSpeed)
    c.send(backwardrightSpeed)
    c.send(backwardData)
    print("Backward command sent.")

def constTurnLeft():
    '''

    :param: N/A
    :return: N/A

    Sends turn left command to ARA while the
    'a' key is being pressed.
    '''

    # speed for motors (left set to 70, right set to 70)
    turningLeftLeftSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])
    turningLeftRightSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])

    # used to send the turn left command
    turnLeftData = bytearray([0xFF, 0x00, 0x01, 0x00, 0xFF])

    # opens socket and sends speed to motors for turning ARA left
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    c.send(turningLeftLeftSpeed)
    c.send(turningLeftRightSpeed)
    c.send(turnLeftData)
    print("Turn left command sent.")

def constTurnRight():
    '''

    :param: N/A
    :return: N/A

    Sends the turn right command to ARA while the
    'd' key is being pressed.
    '''

    # speed for motors (left set to 70, right set to 70)
    turningRightLeftSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])
    turningRightRightSpeed = bytearray([0xFF, 0x02, 0x01, 0x46, 0xFF])

    # used to send the turn left command
    turnRightData = bytearray([0xFF, 0x00, 0x02, 0x00, 0xFF])

    # opens
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((IP, PORT))
    c.send(turningRightLeftSpeed)
    c.send(turningRightRightSpeed)
    c.send(turnRightData)
    print("Turn right command sent.")

def constControl():
    '''

    :param: N/A
    :return: N/A

    Initializes and controls ARA based on keyboard input.
    '''

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 40
    HEIGHT = 40

    # This sets the margin between each cell
    MARGIN = 10

    # creates a 2 dimensional array
    grid = []
    for row in range(7):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(7):
            grid[row].append(0)  # Append a cell

    # sets the initial position of ARA and the object
    araRow = 6
    araCol = 3
    grid[araRow][araCol] = 1

    objRow = 0
    objCol = 3
    grid[objRow][objCol] = 2

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [400, 400]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("ARA 2-D Environment")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    print("Initializing ARA...")
    araObj = ARA()
    controls()
    
    # -------- Main Loop -----------
    while not done:
        # checking pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            print("Exiting the program.")
            done = True
        # while w is pressed, move ARA forward
        elif keys[pygame.K_w]:
            araObj.moveForward()
        # while s is pressed, move ARA backward
        elif keys[pygame.K_s]:
            araObj.moveBackward()
        # while a is pressed, turn ARA left
        elif keys[pygame.K_a]:
            araObj.turnLeft()
        # while d is pressed, turn ARA right
        elif keys[pygame.K_d]:
            araObj.turnRight()
        # while q is pressed, open ARA's claw
        elif keys[pygame.K_q]:
            araObj.clawControl(1)
        # while e is pressed, close ARA's claw
        elif keys[pygame.K_e]:
            araObj.clawControl(0)
        # while z is pressed, rotate ARA's claw vertically
        elif keys[pygame.K_z]:
            araObj.clawRotate(0)
        # while x is pressed, rotate ARA's claw horizontally
        elif keys[pygame.K_x]:
            araObj.clawRotate(1)
        # if no keys are being pressed, stop ARA from moving
        else:
            araObj.stopMovement()

        # check if the user did something other than holding a key down
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If user clicked close
                print("Exiting the program.")
                done = True

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(7):
            for column in range(7):
                color = WHITE
                if grid[row][column] == 1:
                    color = GREEN
                elif grid[row][column] == 2:
                    color = BLUE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.pp
    pygame.quit()

constControl()


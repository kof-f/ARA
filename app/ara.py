""" Affordable Robot Assistant (ARA) - Developed by Kofi Forson

This file contains the ARA class that implements the main functionality of ARA.
There are getter/setter methods used to control every aspect of the robot from
its camera to its claw. For more information on ARA, visit the website:
akizzlebrand.com/ara.

"""

import socket
import time
import webbrowser
import pygame
import smtplib
from email.mime.text import MIMEText


# please connect to ARA's Wi-Fi before running program - DEFAULT PASSWORD: 12345678
class ARA:
    def __init__(self, left_speed=80, right_speed=80, ip="192.168.1.1", port=2001):
        # used to open the socket and send commands (packets) to ARA (Raspberry Pi 3) through its Wi-Fi
        # double check these are correct by using Wireshark to packet sniff when connected to ARA's Wi-Fi
        self.ip = ip
        self.port = port

        # used to open ARA's camera stream
        self.camera_stream_url = "http://" + self.ip + ":8080/?action=stream"

        # the speed is passed as a decimal and converted to hexadecimal in the bytearray
        self.left_motor_speed = bytearray([0xFF, 0x02, 0x01, int(hex(left_speed), 16), 0xFF])
        self.right_motor_speed = bytearray([0xFF, 0x02, 0x02, int(hex(right_speed), 16), 0xFF])

        # used to control the movement of ARA
        self.stop = bytearray([0xFF, 0x00, 0x00, 0x00, 0xFF])
        self.forward = bytearray([0xFF, 0x00, 0x04, 0x00, 0xFF])
        self.backward = bytearray([0xFF, 0x00, 0x03, 0x00, 0xFF])
        self.left = bytearray([0xFF, 0x00, 0x01, 0x00, 0xFF])
        self.right = bytearray([0xFF, 0x00, 0x02, 0x00, 0xFF])

        # used to control ARA's claw
        self.claw_clench_pos = bytearray([0xFF, 0x01, 0x04, 0x56, 0xFF])
        self.claw_rotate_pos = bytearray([0xFF, 0x01, 0x03, 0x56, 0xFF])

        # used to control ARA's arm
        self.arm_mid_pos = bytearray([0xFF, 0x01, 0x02, 0x56, 0xFF])
        self.arm_base_pos = bytearray([0xFF, 0x01, 0x01, 0x56, 0xFF])

        # used to control the camera pan and tilt
        self.camera_pan_pos = bytearray([0xFF, 0x01, 0x07, 0x56, 0xFF])
        self.camera_tilt_pos = bytearray([0xFF, 0x01, 0x08, 0x32, 0xFF])
        # cameraTiltDataMid = bytearray([0xFF, 0x01, 0x08, 0x32, 0xFF])
        # cameraTiltDataUp = bytearray([0xFF, 0x01, 0x08, 0xab, 0xFF])
        # cameraPanDataMid = bytearray([0xFF, 0x01, 0x07, 0x56, 0xFF])
        # cameraPanDataLeft = bytearray([0xFF, 0x01, 0x07, 0xab, 0xFF])

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_left_speed(self):
        return self.left_motor_speed

    def set_left_speed(self, left_motor_speed):
        # setting boundaries for the left motor speed
        # min = 20 and max = 100
        if left_motor_speed > 100:
            left_motor_speed = 100
        elif left_motor_speed < 20:
            left_motor_speed = 20
        self.left_motor_speed = bytearray([0xFF, 0x02, 0x01, int(hex(left_motor_speed), 16), 0xFF])

    def get_right_speed(self):
        return self.right_motor_speed

    def set_right_speed(self, right_motor_speed):
        # setting boundaries for the right motor speed
        # min = 20 and max = 100
        if right_motor_speed > 100:
            right_motor_speed = 100
        elif right_motor_speed < 20:
            right_motor_speed = 20
        self.right_motor_speed = bytearray([0xFF, 0x02, 0x02, int(hex(right_motor_speed), 16), 0xFF])

    def get_claw_clench_pos(self):
        return self.claw_clench_pos

    def set_claw_clench_pos(self, claw_clench_pos):
        # setting boundaries for the claw clench position
        # the claw is fully open at 86 and fully closed at 171
        # so there's no need to accept input outside of those boundaries
        if claw_clench_pos < 86:
            claw_clench_pos = 86
        elif claw_clench_pos > 171:
            claw_clench_pos = 171
        self.claw_clench_pos = bytearray([0xFF, 0x01, 0x04, int(hex(claw_clench_pos), 16), 0xFF])

    def get_claw_rotate_pos(self):
        return self.claw_rotate_pos

    def set_claw_rotate_pos(self, claw_rotate_pos):
        # setting boundaries for the claw rotate position
        # the claw is horizontal at 86 and vertical at 171
        # so there's no need to accept input outside of those boundaries
        if claw_rotate_pos < 86:
            claw_rotate_pos = 86
        elif claw_rotate_pos > 171:
            claw_rotate_pos = 171
        self.claw_rotate_pos = bytearray([0xFF, 0x01, 0x03, int(hex(claw_rotate_pos), 16), 0xFF])

    def get_arm_mid_pos(self):
        return self.arm_mid_pos

    def set_arm_mid_pos(self, arm_mid_pos):
        # setting boundaries for the arm mid position
        # at 0 it's at its lowest and at 171 it's at its highest
        # so there's no need to accept input outside of those boundaries
        if arm_mid_pos < 0:
            arm_mid_pos = 0
        elif arm_mid_pos > 171:
            arm_mid_pos = 171
        self.arm_mid_pos = bytearray([0xFF, 0x01, 0x02, int(hex(arm_mid_pos), 16), 0xFF])

    def get_arm_base_pos(self):
        return self.arm_base_pos

    def set_arm_base_pos(self, arm_base_pos):
        # setting boundaries for the arm base position
        # at 0 it's at its lowest and at 171 it's at its highest
        # so there's no need to accept input outside of those boundaries
        if arm_base_pos < 0:
            arm_base_pos = 0
        elif arm_base_pos > 171:
            arm_base_pos = 171
        self.arm_base_pos = bytearray([0xFF, 0x01, 0x01, int(hex(arm_base_pos), 16), 0xFF])

    def get_camera_pan_pos(self):
        return self.camera_pan_pos

    def set_camera_pan_pos(self, camera_pan_pos):
        # setting boundaries for the camera pan position
        # at 171 it's fully looking left and at 43 it's fully looking right
        # so there's no need to accept input outside of those boundaries
        if camera_pan_pos < 43:
            camera_pan_pos = 43
        elif camera_pan_pos > 171:
            camera_pan_pos = 171
        self.camera_pan_pos = bytearray([0xFF, 0x01, 0x07, int(hex(camera_pan_pos), 16), 0xFF])

    def get_camera_tilt_pos(self):
        return self.camera_tilt_pos

    def set_camera_tilt_pos(self, camera_tilt_pos):
        # setting boundaries for the camera pan position
        # at 0 it's fully tilted down and at 171 it's fully tilted up
        # so there's no need to accept input outside of those boundaries
        if camera_tilt_pos < 0:
            camera_tilt_pos = 0
        elif camera_tilt_pos > 171:
            camera_tilt_pos = 171
        self.camera_tilt_pos = bytearray([0xFF, 0x01, 0x08, int(hex(camera_tilt_pos), 16), 0xFF])

    def send_command_to_ARA(self, command):
        '''

        :param: command as a byte array sent over Wi-Fi to ARA
        :return: N/A

        Sends a command to ARA through Wi-Fi. The command must be a byte array.
        '''

        ara = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ara.connect((self.get_ip(), self.get_port()))
        ara.send(command)

    def initialize_speed(self):
        '''

        :param: N/A
        :return: N/A

        Initializes the speed of ARA by using the left and right speed attributes defined in the constructor.
        '''

        print("Sending left speed command.")
        self.send_command_to_ARA(self.left_motor_speed)
        print("Sending right speed command.")
        self.send_command_to_ARA(self.right_motor_speed)

    def stop_movement(self):
        '''

        :param: N/A
        :return: N/A

        Sends stop command to ARA using stop attribute defined in the constructor.
        '''

        self.send_command_to_ARA(self.stop)

    def move_forward(self):
        '''

        :param: N/A
        :return: N/A

        Sends move forward command to ARA using forward attribute defined in the constructor.
        '''

        print("Sending forward command.")
        self.send_command_to_ARA(self.forward)

    def move_backward(self):
        '''

        :param: N/A
        :return: N/A

        Sends move backward command to ARA using backward attribute defined in the constructor.
        '''

        print("Sending backward command.")
        self.send_command_to_ARA(self.backward)

    def turn_left(self):
        '''

        :param: N/A
        :return: N/A

        Sends turn left command to ARA using left attribute defined in the constructor.
        '''

        print("Sending turn left command.")
        self.send_command_to_ARA(self.left)

    def turn_right(self):
        '''

        :param: N/A
        :return: N/A

        Sends turn right command to ARA using right attribute defined in the constructor.
        '''

        print("Sending turn right command.")
        self.send_command_to_ARA(self.right)

    def claw_clench(self):
        '''

        :param: N/A
        :return: N/A

        Sends claw clench or release command to ARA using the claw position attribute
        defined in the constructor.
        '''

        print("Sending claw clench command.")
        self.send_command_to_ARA(self.claw_clench_pos)

    def claw_rotate(self):
        '''

        :param: N/A
        :return: N/A

        Sends claw rotate command to ARA using the claw rotate attributes defined in
        the constructor.
        '''

        print("Sending claw rotate command.")
        self.send_command_to_ARA(self.claw_rotate_pos)

    def arm_mid_move(self):
        '''

        :param: N/A
        :return: N/A

        Sends arm mid move command to ARA using the arm mid attributes defined in
        the constructor.
        '''

        print("Sending arm mid move command.")
        self.send_command_to_ARA(self.arm_mid_pos)

    def arm_base_move(self):
        '''

        :param: N/A
        :return: N/A

        Sends arm base move command to ARA using the arm base attributes defined in
        the constructor.
        '''

        print("Sending arm base move command.")
        self.send_command_to_ARA(self.arm_base_pos)

    def camera_pan(self):
        '''

        :param: N/A
        :return: N/A

        Sends camera pan command to ARA using the camera pan attributes defined in
        the constructor.
        '''

        print("Sending camera pan command.")
        self.send_command_to_ARA(self.camera_pan_pos)

    def camera_tilt(self):
        '''

        :param: N/A
        :return: N/A

        Sends camera tilt command to ARA using the camera pan attributes defined in
        the constructor.
        '''

        print("Sending camera tilt command.")
        self.send_command_to_ARA(self.camera_tilt_pos)

    def open_camera_stream(self):
        '''

        :param N/A
        :return: N/A

        Opens ARA's camera stream with a web browser.
        '''

        print("Opening ARA's camera stream.")
        webbrowser.open(self.camera_stream_url, new=0, autoraise=True)


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
    print("m: sends text message to user")
    print("c: prints these controls")
    print("ESC: closes the control program")
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

    # initializes ARA and sets its speed
    print("Initializing ARA...")
    command_ARA = ARA(80, 80)
    command_ARA.initialize_speed()
    controls()

    # variables to track the current position of the arm and claw
    claw_clench_current_pos = 86
    claw_rotate_current_pos = 86
    arm_mid_current_pos = 86
    arm_base_current_pos = 171

    # variables to track the current position of the camera
    camera_pan_pos = 86
    camera_tilt_pos = 50

    # -------- Main Loop -----------
    while not done:
        # checking pressed keys
        keys = pygame.key.get_pressed()
        # while w is pressed, move ARA forward
        if keys[pygame.K_w]:
            command_ARA.move_forward()
        # while s is pressed, move ARA backward
        elif keys[pygame.K_s]:
            command_ARA.move_backward()
        # while a is pressed, turn ARA left
        elif keys[pygame.K_a]:
            command_ARA.turn_left()
        # while d is pressed, turn ARA right
        elif keys[pygame.K_d]:
            command_ARA.turn_right()
        # while q is pressed, open ARA's claw
        elif keys[pygame.K_q]:
            claw_clench_current_pos -= 2
            command_ARA.set_claw_clench_pos(claw_clench_current_pos)
            command_ARA.claw_clench()
        # while e is pressed, close ARA's claw
        elif keys[pygame.K_e]:
            claw_clench_current_pos += 2
            command_ARA.set_claw_clench_pos(claw_clench_current_pos)
            command_ARA.claw_clench()
        # while z is pressed, rotate ARA's claw counterclockwise
        elif keys[pygame.K_z]:
            claw_rotate_current_pos += 2
            command_ARA.set_claw_rotate_pos(claw_rotate_current_pos)
            command_ARA.claw_rotate()
        # while x is pressed, rotate ARA's claw clockwise
        elif keys[pygame.K_x]:
            claw_rotate_current_pos -= 2
            command_ARA.set_claw_rotate_pos(claw_rotate_current_pos)
            command_ARA.claw_rotate()
        # while i is pressed, move ARA's middle arm higher
        elif keys[pygame.K_i]:
            arm_mid_current_pos += 2
            command_ARA.set_arm_mid_pos(arm_mid_current_pos)
            command_ARA.arm_mid_move()
        # while , is pressed, move ARA's middle arm lower
        elif keys[pygame.K_COMMA]:
            arm_mid_current_pos -= 2
            command_ARA.set_arm_mid_pos(arm_mid_current_pos)
            command_ARA.arm_mid_move()
        # while u is pressed, move ARA's base arm higher
        elif keys[pygame.K_u]:
            arm_base_current_pos += 2
            command_ARA.set_arm_base_pos(arm_base_current_pos)
            command_ARA.arm_base_move()
        # while m is pressed, move ARA's base arm lower
        elif keys[pygame.K_m]:
            arm_base_current_pos -= 2
            command_ARA.set_arm_base_pos(arm_base_current_pos)
            command_ARA.arm_base_move()
        # while l is pressed, pan ARA's camera left
        elif keys[pygame.K_l]:
            camera_pan_pos += 2
            command_ARA.set_camera_pan_pos(camera_pan_pos)
            command_ARA.camera_pan()
        # while ' is pressed, pan ARA's camera right
        elif keys[pygame.K_QUOTE]:
            camera_pan_pos -= 2
            command_ARA.set_camera_pan_pos(camera_pan_pos)
            command_ARA.camera_pan()
        # while [ is pressed, pan ARA's camera right
        elif keys[pygame.K_LEFTBRACKET]:
            camera_tilt_pos += 2
            command_ARA.set_camera_tilt_pos(camera_tilt_pos)
            command_ARA.camera_tilt()
        # while o is pressed, pan ARA's camera right
        elif keys[pygame.K_o]:
            camera_tilt_pos -= 2
            command_ARA.set_camera_tilt_pos(camera_tilt_pos)
            command_ARA.camera_tilt()
        # if no keys are being pressed, stop ARA from moving
        else:
            command_ARA.stop_movement()

        # check if the user did something other than holding a key down
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If user clicked close
                print("Exiting the program.")
                done = True
            elif event.type == pygame.KEYDOWN:
                # if the ESC key is pressed, close the program
                if event.key == pygame.K_SPACE:
                    print("Exiting the program.")
                # if the spacebar is pressed, open ARA's camera stream
                if event.key == pygame.K_SPACE:
                    command_ARA.open_camera_stream()

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



if __name__ == "__main__":
    constControl()

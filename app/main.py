""" Affordable Robot Assistant (ARA) - Developed by Kofi Forson

This file contains the main ARA file that enables a user to control ARA.
It makes a call to the ARA class. For more information on ARA, visit the
website: akizzlebrand.com/ara.

"""

import pygame

import ara as ara

def main():
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
    ara_row = 6
    ara_col = 3
    grid[ara_row][ara_col] = 1

    obj_row = 0
    obj_col = 3
    grid[obj_row][obj_col] = 2

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
    command_ARA = ara.ARA()
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

    print("""
 ___ _  ____ ___ _
/ _ `/ / __// _ `/
\_,_/ /_/   \_,_/ 
Developed by Kofi Forson
Prototype Version: 1.0
""")

    main()
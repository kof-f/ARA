[<img src = https://uploads-ssl.webflow.com/5d3ca6f373102c5f1ec0740c/5dba2b904bc6349f3398b283_ara-logo.png>](https://www.akizzlebrand.com/ara)

ARA is an an **A**ffordable **R**obot **A**ssistant which will assist disadvantaged individuals 
with the everyday struggles they face in the confines of their home. View the 
[abstract](https://www.dropbox.com/s/7nufchlxttsa6s7/Affordable%20Robot%20Assistant%20Abstract.pdf?dl=0) 
to discover more about why ARA was developed.

## Software Features
 * Object-oriented design
    - ARA class controls the functions of the robot.
 * Emergency texts
    - ARA can act as an alert system and send texts to emergency contacts.
 * Simple code
    - Clearly defined functions and supplemental comments
 * Simple operation
    - Download the git repo, change a few variables (if necessary) and run the file.
    
## Hardware Features
 * DualShock 4 (DS4) Controller/Keyboard Operated
    - Control ARA with a controller, keyboard or both!
 * Raspberry Pi 3
    - All motors are connected/operated by a Raspberry Pi 3 that lives on ARA
 * HD Camera
    - Streams video for easy navigation in any environment
    - Could be used as an alarm when movement is detected in your environment 
    (future-work)
 * Arm and Claw
    - Move ARA's arm and claw to grab items in your environment
 * Stainless Steel
    - ARA's body is built of steel for durability
 * Continuous track
    - Makes it easy for ARA to traverse through any environment regardless of
    its obstacles.
    
## Requirements
### Applications
* Install [Wireshark](https://www.wireshark.org/download.html) for packet sniffing
* Install [DS4Windows](https://github.com/Jays2Kings/DS4Windows/releases) for controlling ARA with a DS4 controller
 (Windows users only)
    - For connecting a DS4 controller to Mac, follow this
    [guide](https://www.macworld.co.uk/how-to/mac/use-ps4-xbox-controller-mac-3626259/).
### Python Modules
* Install pygame which is used by the script to map keyboard input to an ARA command. Try the following code in your
terminal:
`pip3 install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org pygame`. This
command should work on both Windows and Mac.
    - If you're having problems installing pygame on Mac, try following this
     [guide](https://nostarch.com/download/Teach_Your_Kids_to_Code_InstallingPygame_MacLinux.pdf).
 
 ## Controls
 ### Keyboard Controls
  * **w:** moves ARA forward 12 inches at a time
  * **s:** moves ARA backward 12 inches at a time
  * **a:** turns ARA left 90 degrees and moves her forward 6 inches
  * **d:** turns ARA right 90 degrees and moves her forward 6 inches
  * **q:** open ARA's claw
  * **e:** close ARA's claw
  * **z:** rotate ARA's claw to a vertical position
  * **x:** rotate ARA's claw to a horizontal position
  * **i:** move arm mid to highest position
  * **k:** move arm mid to middle position
  * **,:** move arm mid to lowest position
  * **u:** move arm base to highest position
  * **j:** move arm base to middle position
  * **m:** move arm base to lowest position
  * **l:** pan camera left
  * **;:** pan camera mid
  * **':** pan camera right
  * **o:** tilt camera down
  * **p:** tilt camera mid
  * **[:** tilt camera up
  * **spacebar:** starts ARA's camera stream
  * **1:** sends text message to user
  * **c:** prints these controls
  * **esc:** exits the program
   
 ### DualShock 4 Controller: 
* **R2:** moves ARA forward 12 inches at a time
* **L2:** moves ARA backward 12 inches at a time
* **L1:** turns ARA left 90 degrees and moves her forward 6 inches
* **R1:** turns ARA right 90 degrees and moves her forward 6 inches
* **circle:** open ARA's claw
* **cross:** close ARA's claw
* **square:** rotate ARA's claw to a vertical position
* **triangle:** rotate ARA's claw to a horizontal position
* **LS Up:** move arm mid to highest position
* **L3:** move arm mid to middle position
* **LS Down:** move arm mid to lowest position
* **RS Up:** move arm base to highest position
* **R3:** move arm base to middle position
* **RS Down:** move arm base to lowest position
* **Tilt Left:** pan camera left
* **Tilt Up:** pan camera mid
* **Tilt Right:** pan camera right
* **Tilt Down:** tilt camera mid
* **Down:** tilt camera down
* **Up:** tilt camera up
* **PS Button:** starts ARA's camera stream
* **Share button:** sends text message to user
* **options:** prints these controls

## Funder Acknowledgment
The research and development required to launch ARA was supported by the 
[Department of Computer and Information Sciences](https://cast.desu.edu/departments/computer-information-sciences)
at [Delaware State University](https://www.desu.edu/).
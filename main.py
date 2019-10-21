# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:35:01 2019

@author: sergey
"""

import serial.tools.list_ports
import serial
import pygame

ser = serial.Serial('/dev/ttyUSB0', timeout=1, baudrate=9600, parity='N', stopbits=1, bytesize=8)

def send_and_receive(sendstr):
    global ser, busy
    if not ser or not ser.isOpen():
        return
    try:
        s=sendstr.strip('\n\r')+'\n\r'
        ser.write(s)
    except:
    #    busy = False
        raise
    finally:
        busy = False

send_and_receive('VR=4')


import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def _print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    
pressed=0
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            ser.close()
            done=True # Flag that we are done so we exit this loop
            
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")


    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint._print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    buttons = joystick.get_numbuttons()
    if joystick.get_button(4)==1 and joystick.get_button(1)==1 and event.type == pygame.JOYBUTTONDOWN:
        send_and_receive('MCN')
        print 1
        pressed=1
    if joystick.get_button(4)==1 and joystick.get_button(3)==1 and event.type == pygame.JOYBUTTONDOWN:
        send_and_receive('MCP')
        print 2                                
        pressed=1

    if joystick.get_button(4)==1 and joystick.get_button(7)==1 and event.type == pygame.JOYBUTTONDOWN:
        send_and_receive('ALMCLR')
        print 4                                
 

    if pressed==1 and event.type == pygame.JOYBUTTONUP and (joystick.get_button(4)==0 or joystick.get_button(1)==0 or joystick.get_button(2)==0):
        send_and_receive('SSTOP')
        print 3
        pressed=0

            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.


    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:35:01 2019

@author: sergey
"""

import serial.tools.list_ports
import serial
import pygame
import time

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
    
pressed=0
pygame.init()

done = False
v_st=0.1
pygame.joystick.init()
send_and_receive("VR="+str(v_st))
time.sleep(0.1)
send_and_receive("DIS=1000")

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            ser.close()
            done=True # Flag that we are done so we exit this loop
            
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    joystick_count = pygame.joystick.get_count()
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    buttons = joystick.get_numbuttons()
    value=joystick.get_axis(1)
    
    if value>0.0:
        v=round(abs(value)*v_st*20, 3)
        send_and_receive("cv "+str(v))
    elif value == 0.0:
        send_and_receive("cv "+str(v_st))

    if joystick.get_button(4)==1 and joystick.get_button(1)==1 and event.type == pygame.JOYBUTTONDOWN:
        if pressed==0:
            send_and_receive("DIS=-1000")
            time.sleep(0.05)
            send_and_receive("VR=1")
            time.sleep(0.05)
            send_and_receive('MI')
            
            print 1
            pressed=1
    if joystick.get_button(4)==1 and joystick.get_button(3)==1 and event.type == pygame.JOYBUTTONDOWN:
        if pressed==0:
            send_and_receive("DIS=1000")
            time.sleep(0.05)
            send_and_receive("VR=1")
            time.sleep(0.05)
            send_and_receive('MI')
            print 2                                
            pressed=1

    if joystick.get_button(4)==1 and joystick.get_button(7)==1 and event.type == pygame.JOYBUTTONDOWN:
        send_and_receive('ALMCLR')
        print 4                                
 

    if joystick.get_button(4)==0:
        send_and_receive('HSTOP')
        print 3
        pressed=0
    time.sleep(0.05)
            
pygame.quit ()

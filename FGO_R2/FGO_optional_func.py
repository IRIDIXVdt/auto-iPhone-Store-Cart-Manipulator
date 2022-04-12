# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 20:17:33 2020

@author: McLaren
"""

import sys
sys.path.append(r'D:\FGO_R2')
import Serial
import Base_func
import time

#无限池抽取函数
def InfinatePool():
    Serial.port_open('com3')
    Serial.mouse_set_zero()
    Serial.mouse_move((320,360))
    for i in range(100):
        Serial.mouse_click()

#友情池抽取函数
def FriendPointSummon():
    Serial.port_open('com3')
    time.sleep(0.5)
    
    Serial.mouse_set_zero()

    Serial.touch(540,472)
        
    while True:
        Serial.touch(707,480,2)
        time.sleep(1)
        Serial.touch(647,570,8)

#搓丸子        
def MakeCraftEssenceEXCard():
    Serial.port_open('com3')
    Serial.mouse_set_zero()
    
    while True:
        Serial.touch(720,280)
        time.sleep(0.5)
        Serial.mouse_swipe((150,250),(600,600),0.5)
        Serial.touch(990,570,3)
        time.sleep(0.5)
        Serial.touch(720,507,10)

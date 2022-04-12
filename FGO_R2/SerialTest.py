# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:37:11 2019

@author: McLaren
"""

import serial
import time
import numpy as np
import random

ser = serial.Serial()


def port_open(port_no):
    ser.port = port_no  # 设置端口号
    ser.baudrate = 9600  # 设置波特率
    ser.bytesize = 8  # 设置数据位
    ser.stopbits = 1  # 设置停止位
    ser.parity = "N"  # 设置校验位

    if (ser.isOpen()):
        print("串口已经打开")
    else:
        ser.open()  # 打开串口,要找到对的串口号才会成功
        if (ser.isOpen()):
            print("串口打开成功")
        else:
            print("串口打开失败")


def port_close():
    ser.close()
    if (ser.isOpen()):
        print("串口关闭失败")
    else:
        print("串口关闭成功")


# bytes.fromhex(hex(99)[2:])
xy_old = (0, 0)  # 投屏界面的像素位置(1080,607)


def mouse_click():
    ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 1, 0, 0, 0]))
    ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 0, 0, 0, 0]))
    time.sleep(0.3)


def mouse_hold():
    ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 1, 0, 0, 0]))
    time.sleep(0.3)


def mouse_release():
    ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 0, 0, 0, 0]))
    time.sleep(0.3)


def mouse_set_zero():
    global xy_old
    for i in range(10):
        ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 0, 128, 128, 0]))
    xy_old = (0, 0)


#    ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 0, 0, 127, 0]))
#    ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, 0, 0, 68, 0]))

def mouse_swipe(From, To, delay=0.1):
    mouse_move(From, key=0)
    time.sleep(delay)
    mouse_hold()
    time.sleep(delay)
    mouse_move(To, key=1)
    time.sleep(delay)
    mouse_release()


def mouse_move(xy_new, key=0):
    global xy_old
    dx = round((xy_new[0] - xy_old[0]) / 1280 * 1.18 * 122 / 12.7 * 127)
    dy = round((xy_new[1] - xy_old[1]) / 720 * 1.18 * 69 / 7.2 * 127)
    X = list()
    Y = list()
    if dx > 0:
        # 向着X正方向移动
        max = 127
        cyc_x = dx // max
        mod_x = dx % max
        for i in range(0, cyc_x):
            X.append(max)
        if mod_x != 0:
            X.append(mod_x)
    else:
        # 向着X负方向移动
        dx = -dx
        max = 127
        cyc_x = dx // max
        mod_x = dx % max
        for i in range(0, cyc_x):
            X.append(256 - max)
        if mod_x != 0:
            X.append(256 - mod_x)
    if dy > 0:
        # 向着Y正方向移动
        max = 127
        cyc_y = dy // max
        mod_y = dy % max
        for i in range(0, cyc_y):
            Y.append(max)
        if mod_y != 0:
            Y.append(mod_y)
    else:
        # 向着Y负方向移动
        dy = -dy
        max = 127
        cyc_y = dy // max
        mod_y = dy % max
        for i in range(0, cyc_y):
            Y.append(256 - max)
        if mod_y != 0:
            Y.append(256 - mod_y)

    if len(X) > len(Y):
        for i in range(len(X) - len(Y)):
            Y.append(0)
    elif len(Y) > len(X):
        for i in range(len(Y) - len(X)):
            X.append(0)

    for i in range(len(X)):
        ser.write(serial.to_bytes([0x08, 0x00, 0xA1, 0x02, key, X[i], Y[i], 0]))
    time.sleep(0.3)
    xy_old = xy_new


def touch(X_Position, Y_Position, times=1):
    if (ser.isOpen()):
        for i in range(times):
            mouse_move((X_Position, Y_Position))
            mouse_click()
    else:
        print("发送失败，串口未打开")


def card(TreasureDevice_no=1):
    # Current_state.WaitForBattleStart()
    mouse_set_zero()
    touch(965 - np.random.randint(0, 44), 526 - np.random.randint(0, 44))  # 点击攻击
    time.sleep(2)
    touch(386 - np.random.randint(0, 88) + (TreasureDevice_no - 1) * 193,
          219 - np.random.randint(0, 87))  # 打手宝具,参数可选1-3号宝具位
    Card_index = random.sample(range(0, 4), 2)  # 随机两张牌
    touch(149 - np.random.randint(0, 88) + (Card_index[0]) * 213, 465 - np.random.randint(0, 88))
    touch(149 - np.random.randint(0, 88) + (Card_index[1]) * 213, 465 - np.random.randint(0, 88))
    print(' Card has pressed')


def character_skill(character_no, skill_no, para=None):  # 角色编号，技能编号，选人（可选）
    Position = (
        416 - np.random.randint(0, 22) + (character_no - 2) * 263 + (skill_no - 2) * 80, 500 - np.random.randint(0, 30))
    touch(Position[0], Position[1])
    if para != None:
        Position = (605 - np.random.randint(0, 131) + (para - 1) * 263, 430 - np.random.randint(0, 120))  # 技能选人
        touch(Position[0], Position[1])
    time.sleep(0.5)  # 等待技能动画时间
    # Current_state.WaitForBattleStart()
    print(' Character{}\'s skill{} has pressed'.format(character_no, skill_no))


port_open("com3")  # 串口调试
# time.sleep(2)
mouse_set_zero()
# mouse_click()
time.sleep(1)
# touch(760, 266)
print("Now moving")
# mouse_swipe((200 + np.random.randint(0, 400), 500), (200 + np.random.randint(0, 400), 250))
# mouse_move((1055, 220))
# time.sleep(1)
# mouse_move((1055, 264))
# time.sleep(1)
# mouse_move((1055, 308))
# time.sleep(1)
# mouse_move((1055, 352))
# time.sleep(1)
# mouse_move((1055, 396))
# for i in range(0, 5):
#     touch(1055, 185 + i * 35)
#     time.sleep(0.5)
# touch(702 - np.random.randint(0, 351), 307 - np.random.randint(0, 44))  # 点击金苹果
# touch(175 - np.random.randint(0, 87), 175 - np.random.randint(0, 87))  # 点击关卡
# touch(763 - np.random.randint(0, 123), 482 - np.random.randint(0, 26))  # 点击确定
# touch(149 - np.random.randint(0, 88), 465 - np.random.randint(0, 88))  # 点击攻击
# card(2)
# touch(412 - np.random.randint(0, 26), 491 - np.random.randint(0, 26))  # 点击技能
# touch(605 - np.random.randint(0, 131), 430 - np.random.randint(0, 141))  # 点击人物
character_skill(1, 1, np.random.randint(1, 3))
character_skill(1, 2, np.random.randint(1, 3))
character_skill(1, 3, np.random.randint(1, 3))
character_skill(2, 1, np.random.randint(1, 3))
character_skill(2, 2, np.random.randint(1, 3))
character_skill(2, 3, np.random.randint(1, 3))
character_skill(3, 1, np.random.randint(1, 3))
character_skill(3, 2, np.random.randint(1, 3))
character_skill(3, 3, np.random.randint(1, 3))
port_close()

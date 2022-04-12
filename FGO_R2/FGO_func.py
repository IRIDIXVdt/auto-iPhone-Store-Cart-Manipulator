# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""
import time
import sys
from tqdm import tqdm
import random

sys.path.append(r'D:/FGO_R2')
import Serial
import Base_func
import numpy as np


# from Notice import sent_message


class state:
    def HasBackToMenu(self):
        Flag, Position = Base_func.match_template('Menu_button')
        while bool(1 - Flag):
            time.sleep(1)
            Flag, Position = Base_func.match_template('Menu_button')

    def WaitForBattleStart(self):
        Flag, Position = Base_func.match_template('Attack_button')
        while bool(1 - Flag):
            time.sleep(3)
            Flag, Position = Base_func.match_template('Attack_button')

    def WaitForBattleEnd(self):
        while True:
            time.sleep(1)
            Flag, Position = Base_func.match_template('Battlefinish_sign2')
            time.sleep(1)
            if Flag:
                break
            Serial.touch(877 - np.random.randint(0, 614), 88 - np.random.randint(0, 79))  # 跳过无用内容

    def WaitForFriendShowReady(self):
        Flag, Position = Base_func.match_template('friend_sign2')
        while bool(1 - Flag):
            time.sleep(1)
            Flag, Position = Base_func.match_template('friend_sign2')
            if Flag:
                break
            Flag, Position = Base_func.match_template('no_friend')
            if Flag:
                break


Current_state = state()


def enter_battle():
    Current_state.HasBackToMenu()
    # 确认已经返回菜单界面
    Flag, Position = Base_func.match_template('LastOrder_sign')
    time.sleep(1)
    if Flag:
        Serial.touch(Position[0] + 230, Position[1] + 50)
        print(' ')
        print(' Enter battle success')
    else:
        print(' Enter battle fail')


def apple_feed():
    time.sleep(1.5)
    Flag, Position = Base_func.match_template('AP_recover')
    if Flag:
        Flag, Position = Base_func.match_template('Silver_apple', True, 0.99)
        if Flag:
            Serial.touch(702 - np.random.randint(0, 351), 412 - np.random.randint(0, 44))  # 点击银苹果
            time.sleep(1.5)
            Flag, Position = Base_func.match_template('Feedapple_decide')
            Serial.touch(763 - np.random.randint(0, 123), 482 - np.random.randint(0, 26))  # 点击确定
            print(' Feed silver apple success')
        else:
            Flag, Position = Base_func.match_template('Gold_apple')
            if Flag:
                Serial.touch(702 - np.random.randint(0, 351), 307 - np.random.randint(0, 44))  # 点击金苹果
                time.sleep(1.5)
                Flag, Position = Base_func.match_template('Feedapple_decide')

                Serial.touch(763 - np.random.randint(0, 123), 482 - np.random.randint(0, 26))  # 点击确定
                print(' Feed gold apple success')
                time.sleep(2)
            else:
                print(' No apple remain')
                Serial.touch(0, 0)
                sys.exit(0)
    else:
        print(' No need to feed apple')


def find_friend(servant):
    time_limit_flag = 1
    Current_state.WaitForFriendShowReady()
    Flag, Position = Base_func.match_template(servant + '_skill_level', False, 0.95)
    while bool(1 - Flag):  # 第一次找人失败（悲
        print(' Didn\'t find {}, retry. Attempt{}'.format(servant, time_limit_flag))
        # Flag, Position = Base_func.match_template('Refresh_friend')
        Serial.touch(702, 105, 2)  # 点刷新键
        # Flag, Position = Base_func.match_template('Refresh_decide')
        Serial.touch(737 - np.random.randint(0, 70), 482 - np.random.randint(0, 26))  # 点确定
        Current_state.WaitForFriendShowReady()
        # time.sleep(1.5)
        Flag, Position = Base_func.match_template(servant + '_skill_level')
        if Flag:  # 找到了（可喜可贺
            break
        time_limit_flag += 1
        if time_limit_flag > 5:
            print(" Error: cannot find target servant")
            sys.exit()
        time.sleep(15)

    print(' Successful in finding ', servant)
    # Serial.touch(Position[0], Position[1] - 60)
    Serial.touch(658 - np.random.randint(0, 439), Position[1] - 100)
    print(' Position one value for target servant is: ' + str(Position[1]))
    time.sleep(1.5)
    Serial.touch(1005, 570)
    print(' Start-battle button pressed')


def find_friend_2(servant):  # 此功能用于活动外free本
    Current_state.WaitForFriendShowReady()

    Flag, Position = Base_func.match_template(servant + '_skill_level')
    if bool(1 - Flag):
        for i in range(0, 5):
            Serial.touch(1055, 255 + i * 35)
            time.sleep(0.5)
            Flag, Position = Base_func.match_template(servant + '_skill_level')
            time.sleep(1)
            if Flag:
                break
        print("encounter issue while searching target servant")

    print(' Success find ', servant)
    Serial.touch(Position[0] - 450 - np.random.randint(0, 100), Position[1] - 100)
    time.sleep(1.5)
    Serial.touch(1005, 570)
    print(' Start battle button pressed')


def quit_battle():
    print("Starting quit battle in 4s")
    time.sleep(4)
    # Serial.touch(877 - np.random.randint(0, 614), 88 - np.random.randint(0, 79), 5)  # 点击左上角五次来跳过无用内容
    # while True:
    #     time.sleep(1)
    #     Flag, Position = Base_func.match_template('Battlefinish_sign2')
    #     time.sleep(1)
    #     if Flag:
    #         break
    #     Serial.touch(877 - np.random.randint(0, 614), 88 - np.random.randint(0, 79))  # 跳过无用内容
    Current_state.WaitForBattleEnd()
    # Flag, Position = Base_func.match_template('Master_face')
    # if Flag:
    #     break
    # Flag, Position = Base_func.match_template('Master_face')
    # if Flag:
    #     print(' 翻车，需要人工处理')  # 翻车检测
    #     Serial.mouse_set_zero()
    #     # sent_message(text='【FGO】: Encounter a battle error.')
    #     sys.exit(0)
    print(' Battle finished')
    time.sleep(1)
    # Flag, Position = Base_func.match_template('Rainbow_box')  # 检测是否掉礼装，若掉落则短信提醒
    # if Flag:
    #     sent_message()
    # for i in range(0, 4):
    #     Serial.touch(1005 - np.random.randint(0, 100), 570 - np.random.randint(0, 100))
    # Serial.touch(986, 565, 6)
    # # -------------------------------------------
    # Serial.touch(285, 500, 2)  # 拒绝好友申请
    Serial.touch(986, 565, 2)
    Serial.touch(290, 495, 3)  # 拒绝好友申请
    # Current_state.WaitForResultCheck()  # 此条只限FGO 咕哒咕哒终章
    # Serial.touch(570 - np.random.randint(0, 88), 456 - np.random.randint(0, 26), 3)  # 此条只限FGO 咕哒咕哒终章

    Serial.mouse_set_zero()  # 鼠标复位,防止误差累积
    print(' Quit success')
    time.sleep(5)


def Master_skill(skill_no, para=None, suit='Trans'):  # para 只有在极地服那里才有用
    Current_state.WaitForBattleStart()
    Serial.touch(1018 - np.random.randint(0, 27), 272 - np.random.randint(0, 18))  # 御主技能按键
    Serial.touch(842 - np.random.randint(0, 17) + (skill_no - 2) * 79, 272 - np.random.randint(0, 26))  # 技能1-3
    if suit == 'Trans':
        # if skill_no == 1:
        #     Serial.touch(763 - np.random.randint(0, 17), 272 - np.random.randint(0, 26))  # 技能1
        # elif skill_no == 2:
        #     Serial.touch(842 - np.random.randint(0, 17), 272 - np.random.randint(0, 26))  # 技能2
        # el
        if skill_no == 3:  # 换人: 默认场上的右一 与 后备的左一 对换
            # Serial.touch(921 - np.random.randint(0, 17), 272 - np.random.randint(0, 26))  # 技能3
            Serial.touch(500 - np.random.randint(0, 88), 307 - np.random.randint(0, 44))  # 场上的右一
            Serial.touch(658 - np.random.randint(0, 88), 307 - np.random.randint(0, 44))  # 后备的左一
            Serial.touch(605 - np.random.randint(0, 104), 526 - np.random.randint(0, 17))  # 确认
    elif suit == 'Jedi':
        Position = (605 - np.random.randint(0, 131) + (para - 2) * 263, 430 - np.random.randint(0, 120))  # 技能选人
        Serial.touch(Position[0], Position[1])
    else:
        print("Functions not implemented yet")
    time.sleep(1)
    print(' Master skill{} has been pressed'.format(skill_no))
    time.sleep(1)


def character_skill(character_no, skill_no, para=None):  # 角色编号，技能编号，选人（可选）
    Current_state.WaitForBattleStart()
    Position = (
        416 - np.random.randint(0, 22) + (character_no - 2) * 263 + (skill_no - 2) * 80, 500 - np.random.randint(0, 30))
    Serial.touch(Position[0], Position[1])
    if para != None:
        Position = (605 - np.random.randint(0, 131) + (para - 2) * 263, 430 - np.random.randint(0, 120))  # 技能选人
        Serial.touch(Position[0], Position[1])
    time.sleep(3)  # 等待技能动画时间

    print(' Character{}\'s skill{} has pressed'.format(character_no, skill_no))


def card(TreasureDevice_no=1):
    Current_state.WaitForBattleStart()
    Serial.touch(965 - np.random.randint(0, 44), 526 - np.random.randint(0, 44))  # 点击攻击
    time.sleep(2)
    Serial.touch(386 - np.random.randint(0, 88) + (TreasureDevice_no - 1) * 193,
                 219 - np.random.randint(0, 87))  # 打手宝具,参数可选1-3号宝具位
    Card_index = random.sample(range(0, 5), 2)  # 随机两张牌
    Serial.touch(149 - np.random.randint(0, 88) + (Card_index[0]) * 213, 465 - np.random.randint(0, 88))
    Serial.touch(149 - np.random.randint(0, 88) + (Card_index[1]) * 213, 465 - np.random.randint(0, 88))
    Serial.mouse_set_zero()
    print(' Card has pressed')


def card_null():
    Current_state.WaitForBattleStart()
    Serial.mouse_set_zero()
    Serial.touch(965 - np.random.randint(0, 44), 526 - np.random.randint(0, 44))  # 点击攻击
    time.sleep(1)
    Card_index = random.sample(range(0, 5), 3)  # 随机三张牌
    for i in Card_index:
        Serial.touch(149 - np.random.randint(0, 88) + i * 213, 465 - np.random.randint(0, 88))
    print(' Card has pressed')


def battle():
    event_20200506_01()

def event_20200920_01():
    Serial.mouse_set_zero()
    time.sleep(15)
    print("Battle Start ;) ")
    # Turn one
    Current_state.WaitForBattleStart()  # 判断是否进入战斗界面
    character_skill(2, 3, 1)
    character_skill(1, 3)
    card(1)
    time.sleep(25)
    # Turn two
    Current_state.WaitForBattleStart()
    character_skill(3, 1)
    character_skill(3, 2, 2)
    character_skill(3, 3, 2)
    Master_skill(3)
    character_skill(3, 3)
    character_skill(3, 2)

    character_skill(3, 1, 2)
    character_skill(1, 3)

    card(1)
    time.sleep(25)
    # Turn three
    Current_state.WaitForBattleStart()
    character_skill(1, 1, 2)
    #character_skill(3, 1, 1)
    Master_skill(1)
    card(2)
    time.sleep(15)

def event_20200506_01():
    Serial.mouse_set_zero()
    time.sleep(15)
    print("Battle Start ;) ")
    # Turn one
    Current_state.WaitForBattleStart()  # 判断是否进入战斗界面
    character_skill(2, 2)
    character_skill(2, 1)
    character_skill(3, 3, 2)

    card(2)
    time.sleep(15)
    # Turn two
    Current_state.WaitForBattleStart()
    character_skill(3, 1)
    character_skill(3, 2, 1)
    Master_skill(3)
    character_skill(3, 2)
    character_skill(3, 3)
    character_skill(3, 1, 2)
    card(2)
    time.sleep(15)
    # Turn three
    Current_state.WaitForBattleStart()
    character_skill(1, 1)
    character_skill(1, 3)
    Master_skill(1)
    card(1)
    time.sleep(15)


def FGO_process(times=1, servant='CBA'):
    for i in tqdm(range(times)):
        times -= 1
        enter_battle()
        apple_feed()
        find_friend(servant)
        battle()
        quit_battle()
        print(' ')
        print(' {} times of battles remain'.format(times))


def main(port_no, times=1, servant='Caber'):
    Serial.port_open(port_no)  # 写入通讯的串口号
    Serial.mouse_set_zero()
    FGO_process(times, servant)
    Serial.port_close()
    print(' All done!')

def check(img):
    Flag, Position = Base_func.match_template(img)
    if Flag:
        Serial.touch(Position[0] * 0.8, Position[1] * 0.8)


def main2():
    Serial.port_open('com5')  # 写入通讯的串口号

    while (True):
        Serial.mouse_set_zero()
        check('roll')
        check('reset')
        check('end')
        check('new')
        Flag, Position = Base_func.match_template('sukasaha')
        if Flag:
            Serial.touch(317, 337)
        Flag, Position = Base_func.match_template('sukasahaBody')
        if Flag:
            Serial.touch(320, 340)
    Serial.port_close()
    print(' All done!')

if __name__ == '__main__':
    # main('com5', 8)
    main2()
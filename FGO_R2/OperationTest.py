
import Serial
import Base_func
import time
import sys
# from tqdm import tqdm
import random
import numpy as np

sys.path.append(r'FGO_R2')


def checkState():
    list = ['NoAvailable', 'CheckOutReady', 'CheckTime', 'CheckTimeNot',
            'Password', 'PayNow', 'CheckOut', 'ReloadPay', 'TouchPay', 'ConfirmAndPay']
    # Flag, Position = Base_func.match_template('CartButton')
    for listItem in list:
        Flag, Position = Base_func.match_template(listItem, True, 0.9)
        if Flag:
            # print('Current state is:', listItem)
            return listItem
        # print('current', listItem, Flag)
    return None


def touchCart():
    Serial.mouse_set_zero()
    Flag, Position = Base_func.match_template('CartButton')
    # Serial.mouse_move(50, 50)
    time.sleep(1)
    if Flag:
        print('exist at', Position)
        Serial.touch(780, 580)


def checkOut():
    # Serial.mouse_set_zero()
    Flag, Position = Base_func.match_template('CartCheckOut')
    time.sleep(1)
    if Flag:
        print('exist at', Position)
        Serial.touch(850, 550)


def pay():
    time.sleep(1)
    Serial.touch(850, 590)


def main(port_no, times=1, ):
    # Serial.port_open(port_no)
    # time.sleep(5)

    for i in range(100):
        time.sleep(3)
        cState = checkState()
        print('currently it is', cState)

    # Serial.port_close()
    print(' All done!')


if __name__ == '__main__':
    # main('com5', 8)
    main('com3')

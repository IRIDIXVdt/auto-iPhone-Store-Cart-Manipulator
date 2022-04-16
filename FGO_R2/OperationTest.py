
import Serial
import Base_func
import time
import sys
# from tqdm import tqdm
import random
import numpy as np
import datetime

sys.path.append(r'FGO_R2')


def checkState():
    Serial.mouse_set_zero()
    list = ['CartNotReady', 'AllTimeAreFull',  'NoAvailable', 'CheckOutReady', 'CheckTime', 'CheckTimeNot',
            'PassNow', 'PayNow', 'CheckOut', 'ReloadPay', 'TouchPay','AutoSelectTime', 'ConfirmAndPay',  'NoTimeAtAll', 'AwkwardSelectAll', ]
    # Flag, Position = Base_func.match_template('CartButton')
    for listItem in list:
        Flag, Position = Base_func.match_template(listItem, False, 0.90)
        if Flag:
            # print('Current state is:', listItem)
            return listItem
        # print('current', listItem, Flag)
    return None


def handleState(cState):
    # print('Current State is', cState)
    # time.sleep(1)
    if cState == 'CartNotReady' or cState == 'NoAvailable':
        # we want to refresh
        touchCart()
    elif cState == 'AllTimeAreFull':
        touchGoBack()
    elif cState == 'CheckOutReady' or cState == 'AwkwardSelectAll':
        # we want to select them all
        hitSelectAll()
        time.sleep(1)
    elif cState == 'CheckTime':
        # select first slot in time
        selectTime()
    elif cState == 'CheckTimeNot' or cState == 'AutoSelectTime' or cState == 'NoTimeAtAll':
        # refresh this thing
        restartPayNow()
    # elif cState == 'NoTimeAtAll':
    #     # refresh this thing
    #     restartPayNow()
    elif cState == 'PassNow':
        # insert info
        zfPass()
    elif cState == 'PayNow':
        # pay zfb
        zfPayNow()
    elif cState == 'CheckOut':
        # go to check out
        ddCheckOut()
    elif cState == 'ReloadPay':
        # click reload
        ddReload()
    elif cState == 'TouchPay':
        # disable it
        zfNoTouchPay()
    elif cState == 'ConfirmAndPay':
        # touch pay now
        ddPayNow()


def touchCart():
    Serial.mouse_move((600, 1200))
    Serial.touch(420, 1200)
    # Serial.touch(400, 1040)


def hitSelectAll():
    Serial.mouse_move((50, 1200))
    Serial.touch(50, 1100)


def ddCheckOut():
    Serial.touch(500, 950)


def ddPayNow():
    Serial.mouse_move((600, 1200))
    Serial.touch(550, 1150)


def restartPayNow():
    Serial.touch(50, 50)
    time.sleep(0.5)
    Serial.touch(50, 50)
    time.sleep(0.5)
    touchCart()
    # Serial.mouse_move((600, 1200))
    # Serial.touch(550, 1150)


def selectTime():
    Serial.touch(500, 550)


def ddReload():
    Serial.touch(300, 650)


def zfPayNow():
    Serial.touch(300, 1000)


def newMove():
    Serial.mouse_move(1500, 1500)
    Serial.mouse_move(900, 800)
    Serial.mouse_set_zero()


def zfPass():
    Serial.mouse_set_zero()
    time.sleep(0.2)
    Serial.touch(300, 880)
    time.sleep(0.2)
    Serial.touch(300, 800)
    time.sleep(0.2)
    Serial.touch(100, 960)
    time.sleep(0.2)
    Serial.touch(500, 880)
    time.sleep(0.2)
    Serial.touch(100, 800)
    time.sleep(0.2)
    Serial.touch(300, 960)


def zfNoTouchPay():
    Serial.touch(400, 650)


def touchGoBack():
    Serial.touch(300, 600)


def wait():
    t = datetime.datetime.today()
    print(t)
    future = datetime.datetime(t.year, t.month, 14, 6, 0)

    print("now we will sleep", (future-t))
    time.sleep((future-t).total_seconds())


def main(port_no, times=1, ):

    Serial.port_open(port_no)
    Serial.mouse_set_zero()
    time.sleep(1)
    # time.sleep(5)

    while 1:
        time.sleep(0.1)
        cState = checkState()
        print('currently it is', cState)
        handleState(cState)
        if cState == 'TouchPay':
            break

    # ddCheckOut()
    # zfNoTouchPay()

    Serial.port_close()
    print(' All done!')


if __name__ == '__main__':
    # main('com5', 8)
    main('com3')

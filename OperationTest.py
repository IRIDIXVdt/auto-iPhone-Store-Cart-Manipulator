import time
import sys
# from tqdm import tqdm
import random
import numpy as np

sys.path.append(r'FGO_R2')
import Serial
import Base_func

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
    Serial.port_open(port_no)  # 写入通讯的串口号
    time.sleep(1)
    touchCart()
    checkOut()
    pay()
    Serial.port_close()
    print(' All done!')


if __name__ == '__main__':
    # main('com5', 8)
    main('com3')

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 19:50:04 2019

@author: McLaren
"""

import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con, win32api
import sys

sys.path.append(r'D:/FGO_R2')


# from Notice import sent_message


class Fuse:
    def __init__(self):
        self.value = 0
        self.tolerant_time = 500  # 截取50张图片后仍未发现对应目标则报错
        # 防止程序死在死循环里

    def increase(self):
        self.value += 1

    def reset(self):
        self.value = 0

    def alarm(self):
        if self.value == self.tolerant_time:
            # sent_message(text='【FGO】: Encounter a fuse error.')
            print('【FGO】: Encounter a fuse error.')
            sys.exit()

fuse = Fuse()

def match_template(filename, show_switch=False, err=0.9):
    fuse.increase()
    temppath = 'outPut\\' + filename + '.jpg'
    # temppath = 'FGO_R2\\Template2\\' + filename + '.jpg'
    img = window_capture()
    player_template = cv.imread(temppath)
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)

    # print(max_val)  # 测试用 打出max val： 如果小于0.9 说明是多余的帧数

    if max_val > err:  # 当图片中有与模板匹配度超过90%的部分时：
        print(max_val)
        corner_loc = (max_loc[0] + player_template.shape[1], max_loc[1] + player_template.shape[0])
        player_spot = (max_loc[0] + int(player_template.shape[1] / 2), max_loc[1] + int(player_template.shape[0] / 2))
        if show_switch:  # 重写了函数 修改了内容 使文字可以显示
            cv.rectangle(img, max_loc, corner_loc, (0, 0, 255), 2)
            cv.putText(img, filename, (max_loc[0], max_loc[1] - 10), 1, 1.5, (20, 20, 255), 1, cv.LINE_4)
            cv.imshow("MatchResult", img)
            k = cv.waitKey(1000)
            if k == -1:
                cv.destroyAllWindows()

        fuse.reset()
        return True, player_spot
    else:
        fuse.alarm()
        return False, 0


def window_capture():
    hwnd = win32gui.FindWindow("CHWindow", None)  # 窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, filename)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

    # img = cv.imread(filename)
    # 截取出ios屏幕区域
    cropped = img[37:height - 1, 1:width - 1]  # 裁剪坐标为[y0:y1, x0:x1]
    # cv.imwrite('D:/FGO_R2/Template/1.jpg', cropped)  # 测试用 保存文件
    win32gui.DeleteObject(saveBitMap.GetHandle())  # 释放内存
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    return cropped

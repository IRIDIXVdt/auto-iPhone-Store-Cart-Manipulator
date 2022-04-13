import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con, win32api

def window_capture():
    hwnd = win32gui.FindWindow("CHWindow", None)
    hwndDC = win32gui.GetWindowDC(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, filename)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

    # img = cv.imread(filename)
    cropped = img[37:height - 1, 1:width - 1] 

    cvresult = cv.imwrite(name, cropped) 
    print(cvresult)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return cropped

name = "outPut\\Test.jpg"
print()
window_capture()


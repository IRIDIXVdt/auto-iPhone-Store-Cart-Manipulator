import cv2 as cv
import numpy as np

tar = 'FGO_R2/Template/Search.jpg'  # "CvTt/search_pic_main.jpg"

def match_template(filename, show_switch=False, err=0.8):
    temppath = 'FGO_R2\\Template2\\' + filename + '.jpg'
    img = cv.imread(tar)
    player_template = cv.imread(temppath)
    player = cv.matchTemplate(img, player_template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(player)
    print(max_val)
    # 当图片中有与模板匹配度超过90%的部分时：
    if max_val > err:
        # 框选出目标，并标出中心点
        corner_loc = (max_loc[0] + player_template.shape[1], max_loc[1] + player_template.shape[0])
        player_spot = (max_loc[0] + int(player_template.shape[1] / 2), max_loc[1] + int(player_template.shape[0] / 2))

        if show_switch:
            cv.rectangle(img, max_loc, corner_loc, (0, 0, 255), 2)
            cv.putText(img, filename, (max_loc[0], max_loc[1] - 10), 1, 1.5, (20, 20, 255), 1, cv.LINE_4)
            cv.imshow("FGO_MatchResult", img)
            k = cv.waitKey(2000)
            if k == -1:
                cv.destroyAllWindows()

        return True, player_spot
    else:
        return False, 0


def template_demo():
    tpl = cv.imread(tp)
    target = cv.imread(tar)
    # cv.imshow("template image", tpl)
    # cv.imshow("target image", target)

    th, tw = tpl.shape[:2]  # 获取模板图像的高宽

    # methods = [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED,
    #            cv.TM_CCOEFF_NORMED]  # [cv.TM_SQDIFF_NORMED, cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED]  # 各种匹配算法
    # for md in methods:
    md = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(target, tpl, md)
    # result是我们各种算法下匹配后的图像
    # cv.imshow("%s" % md, result)
    # 获取的是每种公式中计算出来的值，每个像素点都对应一个值
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # if md == cv.TM_SQDIFF_NORMED:
    #     tl = min_loc  # tl是左上角点
    # else:
    tl = max_loc
    # if min_val > 0.8:
    print(max_val)
    br = (tl[0] + tw, tl[1] + th)  # 右下点
    cv.rectangle(target, tl, br, (15, 15, 238), 2)  # 画矩形

    cv.imshow("match-%s" % md, target)


match_template("Attack_button", True)

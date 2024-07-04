import cv2
import os
import aircv as ac
import random

from PIL import Image
from .win import Win
from .keymouse import KM

# 获取程序的当前工作目录
root = os.getcwd()


class Utils:
    def getRandomCenter(lt, w, h):
        wr = int(w/2)
        hr = int(h/2)
        fw = int(wr*0.8)
        fh = int(hr*0.8)
        rw = random.randint(-fw, fw)
        rh = random.randint(-fh, fh)
        print(wr, fw, rw)
        cx = lt[0] + wr + rw
        cy = lt[1] + hr + rh
        return (cx, cy)

    def compareImg(source, target, threshold=0.5, bgremove=False, isShow=False):
        result = ac.find_template(
            source, target, threshold=threshold, bgremove=bgremove)
        if result:
            lt = result['rectangle'][0]
            rb = result['rectangle'][3]
            if isShow:
                cv2.rectangle(source, lt, rb, (0, 0, 255), 2)
                cv2.imshow('Matched Image', source)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            w = rb[0] - lt[0]
            h = rb[1] - lt[1]
            result['random_center'] = Utils.getRandomCenter(lt, w, h)
        print(result)
        return result

    def clickByImg(hwnd, target, isCap=True):
        source = None
        if isCap:
            source = Win.capture(hwnd, isSave=False)
        res = Utils.compareImg(source, target, isShow=True)
        rc = res['random_center']
        confidence = res['confidence']
        if confidence > 0.9:
            KM.click(hwnd, rc[0], rc[1])
            return True
        else:
            print('未匹配成功，请检测图片模板是否正确！')
            return False


class SetInfo:
    def __init__(self, hwnd, saveName):
        self.saveName = saveName
        self.hwnd = hwnd

    def setting(self):
        img = Win.capture(self.hwnd, isSave=False)
        rois = cv2.selectROIs('select img tpl', img, False, False)
        if len(rois) > 0:
            for i, roi in enumerate(rois):
                x, y, w, h = roi
                select = img[int(y):int(y+h), int(x):int(x+w)]
                cv2.imwrite(
                    root + f'/selectImgTpl/{self.saveName}_{i}.png', select)
                Utils.compareImg(img, select, isShow=True)

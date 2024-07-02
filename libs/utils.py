import cv2
import os

from PIL import Image
from .win import Win
from .keymouse import KM

# 获取程序的当前工作目录
root = os.getcwd()


class Utils:
    def hist_similar(lh, rh):
        assert len(lh) == len(rh)
        return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)

    def split_image(img, part_size=(64, 64)):
        w, h = img.size
        pw, ph = part_size
        assert w % pw == h % ph == 0
        return [img.crop((i, j, i + pw, j + ph)).copy() for i in range(0, w, pw)
                for j in range(0, h, ph)]

    def make_regalur_image(img, size=(256, 256)):
        """我们有必要把所有的图片都统一到特别的规格，在这里我选择是的256x256的分辨率。"""
        return img.resize(size).convert('RGB')

    def calc_similar(li, ri):
        li = Utils.make_regalur_image(Image.fromarray(
            cv2.cvtColor(li, cv2.COLOR_BGR2RGB)))
        ri = Utils.make_regalur_image(Image.fromarray(
            cv2.cvtColor(ri, cv2.COLOR_BGR2RGB)))
        return sum(Utils.hist_similar(l.histogram(), r.histogram()) for l, r in zip(Utils.split_image(li), Utils.split_image(ri))) / 16.0

    def compareImg(target, source):
        img = source
        # 系数匹配法，越接近1表示匹配度越高
        temp = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = temp.shape[:2]  # 获取需要检测的模板大小
        res5 = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF)
        # cv2.normalize(res5, res5, 0, 1, cv2.NORM_MINMAX)  # 归一化TM_CCOEFF算法处理结果，便于显示
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(
            res5)  # 获取归一化相关性匹配中的匹配度最高的位置
        r = img.copy()
        # 匹配度最高的位置画白色矩形框
        cv2.rectangle(r, maxLoc, (maxLoc[0] + w, maxLoc[1] + h), 255, 5)
        return r, (Utils.calc_similar(temp, img[maxLoc[1]:maxLoc[1] + h, maxLoc[0]:maxLoc[0] + w])), maxLoc


class SetInfo:
    def __init__(self, slogan, saveName, hwnd):
        self.slogan = slogan
        self.saveName = saveName
        self.hwnd = hwnd

    def setting(self):
        print(self.slogan)
        img = Win.capture(self.hwnd, isSave=False)
        roi = cv2.selectROI(img)
        print(roi)
        select = img[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
        cv2.imwrite(root + self.saveName, select)
        a, ra, _ = Utils.compareImg(select, img)
        cv2.imshow('yb', a)
        print("相似度", ra)
        KM.click(int((roi[0] + roi[0] + roi[2]) / 2),
                 int((roi[1] + roi[1] + roi[3]) / 2), self.hwnd)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

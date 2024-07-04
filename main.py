import cv2
import os
import time
from libs.win import Win
from libs.utils import SetInfo, Utils
from libs.keymouse import KM

# 获取程序的当前工作目录
root = os.getcwd()
if __name__ == "__main__":
    wins = Win.get_win_by_title('Chrome')
    hwnd = wins[0]['hwnd']
    # Win.capture(hwnd)
    # SetInfo(hwnd, "imgTpl").setting()
    # time.sleep(1)
    temp = cv2.imread(f"{root}/selectImgTpl/imgTpl_0.png")
    Utils.clickByImg(hwnd, temp)
    time.sleep(1)
    KM.send_str(hwnd, '2223333我说a')

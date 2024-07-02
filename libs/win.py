
import win32gui
import win32ui
import win32api
import win32con
import cv2
import numpy as np
from ctypes import windll
import os

# 获取程序的当前工作目录
root = os.getcwd()


class Win:
    def capture(hwnd, isSave=True):
        try:
            if hwnd is None:
                print('请传入窗口句柄！')
                return False
            # 获取后台窗口的句柄，注意后台窗口不能最小化
            win32api.PostMessage(hwnd, win32con.WM_SETFOCUS, 0, 0)
            # 如果窗口最小化了需要激活窗口再截图
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            # 排除缩放干扰
            # windll.user32.SetProcessDPIAware()
            # 获取窗口的大小
            left, top, right, bottom = win32gui.GetClientRect(hwnd)
            w = right - left
            h = bottom - top
            print(f'截图窗口大小：{w}*{h}')

            # 开始截图
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
            res = False
            if not result:
                print(f"截图失败！: {result}")
                return res
            else:
                # saveBitMap.SaveBitmapFile(
                #     saveDC, root+'\capture\capture.png')
                signedIntsArray = saveBitMap.GetBitmapBits(True)
                im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
                im_opencv.shape = (h, w, 4)
                cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
                if isSave:
                    cv2.imwrite(root+'\capture\capture.png', im_opencv)
                res = im_opencv
                # cv2.imshow('Cap Image', im_opencv)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
            # 释放资源
            if 'saveBitMap' in locals():
                win32gui.DeleteObject(saveBitMap.GetHandle())
            if 'saveDC' in locals():
                saveDC.DeleteDC()
            if 'mfcDC' in locals():
                mfcDC.DeleteDC()
            if 'hwndDC' in locals():
                win32gui.ReleaseDC(hwnd, hwndDC)
            return res
        except Exception as e:
            print(f"发生错误：{e}")
            # 释放资源
            if 'saveBitMap' in locals():
                win32gui.DeleteObject(saveBitMap.GetHandle())
            if 'saveDC' in locals():
                saveDC.DeleteDC()
            if 'mfcDC' in locals():
                mfcDC.DeleteDC()
            if 'hwndDC' in locals():
                win32gui.ReleaseDC(hwnd, hwndDC)
            # 记录日志或抛出异常
            return False

    def get_win_by_title(title_keyword: str):
        hwnds = []

        def eWCallback(hwnd, data):
            title = win32gui.GetWindowText(hwnd)
            if title_keyword in title:
                data.append({
                    'title': title,
                    'hwnd': hwnd
                })
            return True
        win32gui.EnumWindows(eWCallback, hwnds)
        print(f'找到{len(hwnds)}个窗口', hwnds)
        return hwnds

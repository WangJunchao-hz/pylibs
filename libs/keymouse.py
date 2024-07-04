import win32gui
import win32api
import win32con
import time
import random


class KM:
    def click(hwnd, cx, cy, type='L'):
        win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        lp = win32api.MAKELONG(cx, cy)
        mk = win32con.MK_LBUTTON
        wmDown = win32con.WM_LBUTTONDOWN
        wmUp = win32con.WM_LBUTTONUP
        if type == 'R':
            mk = win32con.MK_RBUTTON
            wmDown = win32con.WM_RBUTTONDOWN
            wmUp = win32con.WM_RBUTTONUP
        win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, mk, lp)
        win32api.PostMessage(hwnd, wmDown, mk, lp)
        time.sleep(0.01)
        win32api.PostMessage(hwnd, wmUp, mk, lp)

    def send_str(hwnd, text):
        astrToint = [ord(c) for c in text]
        for item in astrToint:
            win32api.PostMessage(hwnd, win32con.WM_CHAR, item, 0)
            t = random.uniform(0.1, 0.5)
            time.sleep(float("{:.2f}".format(t)))

    def send_key(id, hwnd):
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, id, 0)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, id, 0)

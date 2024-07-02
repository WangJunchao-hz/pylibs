import win32gui
import win32api
import win32con
import time


class KM:
    def click(cx, cy, hwnd, type='L'):
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
        time.sleep(0.005)
        win32api.PostMessage(hwnd, wmUp, mk, lp)

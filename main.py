from libs.win import Win
from libs.utils import SetInfo
if __name__ == "__main__":
    wins = Win.get_win_by_title('Chrome')
    hwnd = wins[0]['hwnd']
    # Win.capture(hwnd)
    SetInfo("圈出铲子", "\capture\chanzi.png", hwnd).setting()

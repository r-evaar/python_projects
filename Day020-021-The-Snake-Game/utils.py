import pyautogui


def getScreenFit(ratio):
    assert 0 < ratio <= 1, "Please select a positive ratio between 0 and 1"
    res = pyautogui.size()
    res = [round(elem*ratio) for elem in res]
    print(res)
    return res

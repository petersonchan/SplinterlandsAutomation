from ppadb.client import Client
import keyboard
import cv2 as cv
import numpy as np
import time
import os

button_list = ['battle_button.png', 'create_team_button.png', 'ready_to_rumble_yes.png',\
               'rumble_button.png', 'skip_1.png', 'skip_2.png', 'done_button.png']

def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    else:
        print("Device Connected")
    return devices[0]

def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)

def clickSrceen(x_position, y_position):
    adb_command = "adb shell input tap " + str(x_position) + " " + str(y_position)
    os.system(adb_command)

if __name__ == "__main__":
    device_phone = connect_device()
    while True:
        take_screenshot(device_phone)
        img = cv.imread('screen.png', 0)
        for i in range(len(button_list)):
            template = cv.imread(button_list[i], 0)
            w, h = template.shape[::-1]
            res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                if (np.any(res >= threshold)) == True:
                    x_position = int(pt[0] + w / 2)
                    y_position = int(pt[1] + h / 2)
                    print(button_list[i], " ", x_position, " ", y_position)
                    clickSrceen(x_position, y_position)
                    time.sleep(2)
                    break


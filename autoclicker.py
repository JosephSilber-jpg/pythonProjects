import pynput
import keyboard
import time

mouse = pynput.mouse.Controller()
running = True
active = False

while running:
    if keyboard.is_pressed('o') or active:
        mouse.click(pynput.mouse.Button.left, 1)
        time.sleep(0.01)

    if keyboard.is_pressed('\\') and not active:
        active = True
    if keyboard.is_pressed('\\') and active:
        active = False

    if keyboard.is_pressed('p'):
        running = False
        break
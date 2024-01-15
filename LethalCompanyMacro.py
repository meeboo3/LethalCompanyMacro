import os
import time
import win32api
import win32con
import keyboard
import pyperclip

version = '1.2.0'

if os.path.exists('LCM.txt'):
    with open('LCM.txt', encoding='utf-8', mode='rt') as f:
        switch_key, transmit_key = [i.replace('_', ' ').split('+') for i in f.read().split(' ')]
else:
    switch_key = ['page down']
    transmit_key = ['down']

curr_copy = ''
run = False


def check(keys: list[str]):
    def fn(event: keyboard.KeyboardEvent):
        if not event.name == keys[-1]:
            return False
        for key in keys[:-1]:
            if not keyboard.is_pressed(key):
                return False
        else:
            return True

    return fn


switch_check = check(switch_key)
transmit_check = check(transmit_key)


def log(text):
    print(f'[{time.strftime("%X")}] {text}')


def copy(text):
    global curr_copy

    if curr_copy != text:
        pyperclip.copy(text)
        curr_copy = text


def paste():
    # ctrl
    win32api.keybd_event(17, 0, 0, 0)
    # v
    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


def switch():
    copy('switch')
    paste()
    # enter
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    log('enter switch')


def transmit():
    copy('transmit ')
    paste()
    log('enter transmit')


text_key = {
    'up': '↑',
    'right': '→',
    'down': '↓',
    'left': '←'
}


def fmt(text: list[str]):
    return ' + '.join(text_key.get(i, i) for i in text)


def process(event):
    if switch_check(event):
        switch()
    elif transmit_check(event):
        transmit()


print(f'press `{fmt(switch_key)}` to quickly enter `switch + enter`\n'
      f'press `{fmt(transmit_key)}` to quickly enter `transmit `\n'
      f'https://github.com/meeboo3/LethalCompanyMacro v{version}')

keyboard.on_press(process)
keyboard.wait()

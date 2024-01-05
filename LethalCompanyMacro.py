import os
import time
import win32api
import win32con
import keyboard
import pyperclip

if os.path.exists('LCM.txt'):
    with open('LCM.txt', encoding='utf-8', mode='rt') as f:
        switch_key, transmit_key = f.read().split(' ')
else:
    switch_key = 'up'
    transmit_key = 'down'

curr_copy = ''
run = False


def run_wrapper(fn):
    def _(args):
        global run
        if run:
            return
        run = True
        fn(args)
        run = False

    return _


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


@run_wrapper
def switch(evt):
    copy('switch')
    paste()
    # enter
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    log('enter switch')


@run_wrapper
def transmit(evt):
    copy('transmit ')
    paste()
    log('enter transmit')


print('press `↑` to quickly enter `switch + enter`\n'
      'press `↓` to quickly enter `transmit `\n'
      'https://github.com/meeboo3/LethalCompanyMacro')
keyboard.on_press_key(switch_key, switch)
keyboard.on_press_key(transmit_key, transmit)
keyboard.wait()

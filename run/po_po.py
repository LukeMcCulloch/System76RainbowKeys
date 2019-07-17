from subprocess import Popen, PIPE
import sys
import traceback
import re
import time

from keyboard_backlight_control import *

def set_state_off(color_ctrl):
    color_ctrl.set_list([Color('000000'), Color('202020'), Color('000000')])

def set_state_a(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('202000'), Color('000000')])

def set_state_b(color_ctrl):
    color_ctrl.set_list([Color('000000'), Color('002020'), Color('FF0000')])

def set_state_both(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('002020'), Color('FF0000')])


def run():
    factory = Factory()
    color_ctrl = factory.color_ctrl()
    set_state_both(color_ctrl)
#    while True:
#        for f in [set_state_a, set_state_b]:
#            for i in range(3):
#                f(color_ctrl)
#                time.sleep(0.05)
#                set_state_off(color_ctrl)
#                time.sleep(0.01)
#            f(color_ctrl)
#            time.sleep(0.15)
            

if __name__ == '__main__':
    run()
#    try:
#        run()
#    except KbError as e:
#        print(str(e), file=sys.stderr)
#        exit(1)
#    except Exception as e:
#        traceback.print_exc(file=sys.stderr)
#        exit(1)

from subprocess import Popen, PIPE
import sys
import traceback
import re
import time

from keyboard_backlight_control import *
#from ColorConstants import colors
"""

colors{'purple':'FF00FF',
        'blue':'0000FF',
        'red':'FF0000',
        'green':'0FF00D',
        yellow:'',
        orange:''}
"""

colors = {'purple':'FF00FF',
            'blue':'0000FF',
             'red':'FF0000',
           'green':'0FF00D',
            'teal':'0FF0FF',
         'magenta':'F00FFF',
          'burntorange':'FF0F0F',
          'yellow':'FFFF00',
          'orange':'FF8C00',
          'orangered':'FF4500',
          'whiteDim':'202020',
          'whiteBright' :'FFFFFF',
          'off':'000000'}

def set_state_off(color_ctrl):
    color_ctrl.set_list([Color('000000'), Color('202020'), Color('000000')])

def set_state_a(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('202000'), Color('000000')])

def set_state_b(color_ctrl):
    color_ctrl.set_list([Color('000000'), Color('002020'), Color('FF0000')])

# blue left, red right
def set_state_blueLeft_redRight(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('002020'), Color('FF0000')])

# blue left, greem middle, green right
def set_state_BlueGreenGreen(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('6DD000'), Color('0FF000')])


def set_state_BlueGreenRed(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('0FF000'), Color('FF0000')])


def set_state_BlueRedGreen(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('FF0000'), Color('0FF000')])


def set_state_BlueGreenPurple(color_ctrl):
    color_ctrl.set_list([Color('0000FF'), Color('0FF00D'), Color('FF00FF')])

def set_state_PurpleBlueGreen(color_ctrl):
    color_ctrl.set_list([Color('FF00FF'), Color('0000FF'), Color('0FF00D')])


def set_state_RedBlueGreen(color_ctrl):
    color_ctrl.set_list([Color('FF0000'), Color('0000FF'), Color('0FF00D')])


def set_state_RedGreenBlue(color_ctrl):
    color_ctrl.set_list([Color('FF0000'), Color('0FF00D'), Color('0000FF')])


# blue left, greem middle, purple right
def set_state_TEST(color_ctrl):
    color_ctrl.set_list([Color(colors['blue']), 
                        Color(colors['green']), 
                        Color(colors['yellow'])])


def run():
    factory = Factory()
    color_ctrl = factory.color_ctrl()
    
    #call to set the color scheme:
    set_state_TEST(color_ctrl)

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

import os
import types
import sys

debug = False

def set_debug(d):
    global debug
    debug = d

class KbError(Exception):
    pass

class Path:
    def __init__(self, path, readonly=False):
        self.path = path
        self.readonly = readonly
        self.cache = None
        if not os.path.isfile(path):
            raise AssertionError('file ' + path + ' does not exist')

    def invalidate(self):
        self.cache = None

    def get(self):
        if not os.access(self.path, os.R_OK):
            raise KbError('permission error reading ' + self.path + ' (try running with sudo)')
        if self.cache == None:
            f = open(self.path, "r")
            self.cache = f.read().strip()
            f.close()
            if debug:
                print('read \'' + self.cache + '\' from ' + self.path)
        return self.cache

    def set(self, value):
        if self.readonly:
            raise AssertionError('tried to write to readonly file ' + self.path)
        if not os.access(self.path, os.W_OK):
            raise KbError('permission error writing ' + self.path + ' (try running with sudo)')
        self.get() # load the current value into the cache if needed, so we don't write unnecessarily
        if self.cache == None or self.cache != value.strip():
            f = open(self.path,"w+")
            f.write(value)
            f.close()
            self.cache = value.strip()
            if debug:
                print('wrote \'' + self.cache + '\' to ' + self.path)

class BrightnessCtrl:
    def __init__(self, base_path):
        self.brightness = Path(base_path + 'brightness')
        self.max_brightness = Path(base_path + 'max_brightness', readonly=True)

    def set(self, value):
        assert isinstance(value, float) or isinstance(value, int), 'set_brightness() sent bad type'
        assert value >= 0, 'set_brightness() sent value less than 0'
        assert value <= 1, 'set_brightness() sent value greater than 1'
        out_str = '0'
        if value > 0:
            max = int(self.max_brightness.get())
            assert max > 0, 'max brightness is zero, wtf?'
            out_str = str(int(value * max))
        self.brightness.set(out_str)

    def get(self):
        max = int(self.max_brightness.get())
        assert max > 0, 'max brightness is zero, wtf?'
        return float(int(self.brightness.get())) / max

def str_to_int(s, b):
	return sum((ord(d)%32+(ord(d)>>6)*25-16)*b**e for e,d in enumerate(s[::-1]))

def int_to_str(i, b, n):
    return ''.join(chr(i//b**e%b+i//b**e%b//10*7+48) for e in range(n)[::-1])

def assert_is_hex(s):
    for c in s:
        assert (c >= '0' and c <= '9') or (c >= 'a' and c <= 'f') or (c >= 'A' and c <= 'F'), (
            '\'' + str(c) + '\' is not a number or letter from A to F')

class Color:
    def __init__(self, c):
        if isinstance(c, str):
            assert len(c) == 6, str(c) + ' is not 6 digits long'
            assert_is_hex(c)
            self.r = str_to_int(c[0:2], 16)
            self.g = str_to_int(c[2:4], 16)
            self.b = str_to_int(c[4:6], 16)
        else:
            assert len(c) == 3, 'color has wrong number of components'
            l = []
            for i in c:
                if isinstance(i, str):
                    assert_is_hex(i)
                    l.append(str_to_int(i, 16))
                elif isinstance(i, int) or isinstance(i, float):
                    assert i >= 0 and i < 256, str(i) + 'is not in the range 0-255'
                    l.append(int(i))
                else:
                    raise AssertionError('color component is bad type')
            self.r = l[0]
            self.g = l[1]
            self.b = l[2]

    def get_hex(self):
        return int_to_str(self.r, 16, 2) + int_to_str(self.g, 16, 2) + int_to_str(self.b, 16, 2)

class ColorCtrl:
    def __init__(self, base_path):
        options = [
            ['color_left', 'color_center', 'color_right'],
            ['color_left', 'color_right'],
            ['color']]
        for option in options:
            works = True
            for i in option:
                if not os.path.isfile(base_path + i):
                    works = False
            if works:
                self.colors = [Path(base_path + i) for i in option]
                return
        raise AssertionError('\n\ncontents of ' + base_path + ':\n' + ' '.join(os.listdir(base_path)) + '\n\n' +
                             'could not detect keyboard backlight color, your system may not yet be supported')
    def get_num(self):
        return len(self.colors)

    def get_list(self):
        return [Color(c.get()) for c in self.colors]

    def set_list(self, colors):
        assert isinstance(colors, list), 'not sent a list'
        assert len(colors) == len(self.colors), 'given ' + str(len(colors)) + ' colors but keyboard has ' + str(len(self.colors))
        for c in colors:
            assert isinstance(c, Color), 'non color in list'
        for i in range(len(self.colors)):
            out_str = colors[i].get_hex()
            self.colors[i].set(out_str)

    def set_single(self, color):
        assert isinstance(color, Color), 'sent a non color'
        out_str = color.get_hex()
        for c in self.colors:
            c.set(out_str)

class Factory:
    def __init__(self):
        leds_path = '/sys/class/leds/'
        kbd_dirs = []
        for i in os.listdir(leds_path):
            if i.endswith('::kbd_backlight'):
                kbd_dirs.append(i)
        if len(kbd_dirs) == 0:
            raise KbError('no ' + leds_path + '*::kbd_backlight/ directories found\n' +
                              '    you may not have a keyboard backlight')
        #if len(kbd_dirs) > 1:
        #    print('WARNING: multiple keyboard backlights found: ' + str(kbd_dirs) + ', choosing ' + kbd_dirs[0], file=sys.stderr)
        self.base_path = leds_path + kbd_dirs[0] + '/'
        assert os.path.isdir(self.base_path), 'base path ' + self.base_path + ' is not directory'
        self.brightness = None
        self.color = None

    def brightness_ctrl(self):
        if self.brightness == None:
            self.brightness = BrightnessCtrl(self.base_path)
        return self.brightness

    def color_ctrl(self):
        if self.color == None:
            self.color = ColorCtrl(self.base_path)
        return self.color

if __name__ == '__main__':
    #print('This file should be imported, not run directly. You may be looking for kb-backlight', file=sys.stderr)
    #exit(1)
    pass

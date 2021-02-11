#!/usr/bin/python
# encoding: utf-8

import plistlib
import sys
#import tkFont
#import Tkinter as tk

from AppKit import (
    NSFont,
    NSFontAttributeName,
    NSMakeSize,
    NSMaxX,
    NSMutableDictionary,
    NSString
    )

plist = "/preferences/appearance/prefs.plist"
theme = "theme.plist"
DEFAULT_FONT = "<System>"
DEFAULT_SIZE = 18


class FontWidthCalcTk(object):
    """Calculate the display width of strings using the TKinter.
    
    This is the original method but crashes on macOS 11.2 Big Sur.
    """
    def __init__(self, font, size):
        t = tk.Tk()
        self.font = tkFont.Font(family=font, size=size)
    
    def measure(self, str):
        return self.font.measure(str)


class FontWidthCalcDumb(object):
    def __init__(self, font, size):
        pass
    
    def measure(self, _str):
        return len(_str)


class FontWidthCalcObjC(object):
    """Calculate the display width of strings using the PyObjC bridge."""
    
    def __init__(self, font, size):
        self._max_size = NSMakeSize(sys.float_info.max, sys.float_info.max)
        self._options = 1 << 3 # NSStringDrawingOptions.NSStringDrawingUsesDeiceMetrics
            # https://developer.apple.com/documentation/uikit/nsstringdrawingoptions?language=objc
        self._attributes = NSMutableDictionary.dictionary()
        self._attributes.setObject_forKey_(NSFontAttributeName, font)
        if font == "<System>":
            self.font = NSFont.systemFontOfSize_(size)
        else:
            self.font = NSFont.fontWithName_size_(font, size)
        
        self._terminator = '1'
        self._terminator_width = self._measure(self._terminator)
        
    def _measure(self, _str):
        s = NSString.alloc().initWithString_(_str)
        box = s.boundingRectWithSize_options_attributes_context_(self._max_size, self._options, self._attributes, None)
        return NSMaxX(box)
        
    def measure(self, _str):
        return self._measure(_str + self._terminator) - self._terminator_width


class Format(object):
    def __init__(self, key, path):
        self.font = self._load_font(key, path)
        
    def _load_font(self, key, path):
        try:
            font, size = self._load_plist(key, path + plist)
        except:
            try:
                font, size = self._load_plist(key, theme)
            except:
                font, size = DEFAULT_FONT, DEFAULT_SIZE
        #return FontWidthCalcTk(font, size)
        return FontWidthCalcObjC(font, size)
    
    def _load_plist(self, key, path):
        pref = plistlib.readPlist(path)
        font = pref['themes'][key]['resultTextFont']
        size = pref['themes'][key]['resultTextFontSize'] * 4 + 8
        return font, size

    def format(self, weeks, title):
        pos = [self.font.measure(title[:title.find(day)]) for day in title.split()]
        space_width = self.font.measure(u' ')
        str_list = []
        for week in weeks:
            str = ""
            for i, day in enumerate(week):
                number_of_spaces = (pos[i] - self.font.measure(str)) / space_width
                str += u' ' * int(round(number_of_spaces))
                str += day
            str_list.append(str)
        return str_list


if __name__ == "__main__":
    
    from util import DEFAULT_SETTINGS
    
    key = "alfred.theme.custom.A1911D25-FB72-4E1C-9180-7A8A71DB327F"
    path = "~/Library/Application Support/Alfred 2/Alfred.alfredpreferences"
    f = Format(key, path)
    from cal import Cal
    c = Cal(DEFAULT_SETTINGS, key, path)
    arr = f.format(c.get_cal(c.get_weeks(2015, 1, 6)), c.week_text(6))
    print c.week_text(6)
    for str in arr:
        print(str)

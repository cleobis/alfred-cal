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
        if font == "<System>":
            nsfont = NSFont.systemFontOfSize_(size)
        else:
            nsfont = NSFont.fontWithName_size_(font, size)
        self._attributes = NSMutableDictionary.dictionary()
        self._attributes.setObject_forKey_(nsfont, NSFontAttributeName)
        
        self._terminator = '1'
        self._terminator_width = self._measure(self._terminator)
        
    def _measure(self, _str):
        s = NSString.alloc().initWithString_(_str)
        box = s.boundingRectWithSize_options_attributes_context_(self._max_size, self._options, self._attributes, None)
        return NSMaxX(box)
        
    def measure(self, _str):
        return self._measure(_str + self._terminator) - self._terminator_width


class Format(object):
    def __init__(self, theme_uid, preference_path, log=None):
        self.log = log
        self.font = self._load_font(theme_uid, preference_path)
        
    def _load_font(self, theme_uid, preference_path):
        try:
            theme_path = self.theme_path_from_id(theme_uid, preference_path)
        except Exception as err:
            self.log and self.log.error("Unable to find theme file for {}, preference path \"{}\"".format(theme_uid, preference_path))
            theme_path = None
        
        try:
            font, size = self.read_theme_font_name_size(theme_path)
        except Exception as err:
            font = None
            self.log and self.log.error("Unable to parse theme file \"{}\". Error:\n{}".format(theme_path, err))
            
        if theme_path is None or font is None:
            font, size = DEFAULT_FONT, DEFAULT_SIZE
        
        self.log and self.log.info("Font: {} {}pt".format(font, size))
        
        return FontWidthCalcObjC(font, size)
    
    def theme_path_from_id(self, theme_uid, preference_path):
        """Return the path to the them file for a theme uid.
    
        A theme uid is of the form "theme.bundled.*" or "theme.custom.*". The 
        returned file path is a json file that can be parsed.
    
        Args:
            theme_uid (str): The theme uid
            preference_path (str): The path to the user's preference file. Used for custom themes.
    
        Returns
            str: The filesystem path to the theme json file. None if the theme is not found.
        """
    
        import os
    
        if theme_uid.startswith("theme.custom."):
            id = theme_uid.split('.')
            if len(id) < 3:
                return None
            id = id[2]
            path = os.path.join(preference_path, "themes", "theme.custom." + id, "theme.json")
        
        elif theme_uid.startswith("theme.bundled."):
            # Get the path to the application
            from AppKit import NSWorkspace
            ws = NSWorkspace.sharedWorkspace()
            url = ws.URLForApplicationWithBundleIdentifier_("com.runningwithcrayons.Alfred")
            if not url:
                return None
            app_path = str(url.path())
        
            # Get the theme file name. I can't find an automatic conversion to the theme file.
            theme_map = {
                "theme.bundled.default":       "Alfred.alfredappearance",
                "theme.bundled.dark":          "Alfred Dark.alfredappearance",
                "theme.bundled.modern":        "Alfred Modern.alfredappearance",
                "theme.bundled.moderndark":    "Alfred Modern Dark.alfredappearance",
                "theme.bundled.classic":       "Alfred Classic.alfredappearance",
                "theme.bundled.osx":           "Alfred macOS.alfredappearance",
                "theme.bundled.osxdark":       "Alfred macOS Dark.alfredappearance",
                "theme.bundled.frostyteal":    "Frosty Teal.alfredappearance",
                "theme.bundled.modernavenir":  "Large Avenir.alfredappearance",
                "theme.bundled.highcontrast":  "High Contrast.alfredappearance",
                }
            if theme_uid not in theme_map:
                return None
            path = os.path.join(app_path, "Contents", "Frameworks", "Alfred Framework.framework",
                "Resources", theme_map[theme_uid])
        
        else:
            return None
    
        if not os.path.isfile(path):
            return None
    
        return path

    def read_theme_font_name_size(self, theme_path):
        """Get the font name and size from a theme json file.
    
        Args:
            theme_path (str): The path to the theme json file.
    
        Returns:
            str: The font name. ??? for the default system font.
            float: The font size
        """
        import json
    
        f = open(theme_path, "r")
        theme_data = json.load(f)
        text = theme_data["alfredtheme"]["result"]["text"]
        font = text["font"]
        size = text["size"]
    
        if font == "System":
            font = "<System>"
    
        return font, size

    def format(self, weeks, title):
        pos = [self.font.measure(title[:title.find(day)+len(day)]) for day in title.split()]
        space = u'\u200a' # hair space
        space_width = self.font.measure(space)
        str_list = []
        for week in weeks:
            str = ""
            for i, day in enumerate(week):
                number_of_spaces = (pos[i] - self.font.measure(str) - self.font.measure(day)) / space_width
                str += space * int(round(number_of_spaces))
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

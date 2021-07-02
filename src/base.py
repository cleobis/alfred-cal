#!/usr/bin/python
# encoding: utf-8

from util import DEFAULT_SETTINGS
from workflow import Workflow, ICON_INFO
import sys


class Base(object):
    def __init__(self):
        wf = Workflow(default_settings=DEFAULT_SETTINGS,
            update_settings={
                'github_slug': 'cleobis/alfred-cal',
            }
            )
        self.wf = wf
        self.log = wf.logger
        
        self.args = wf.args
        if "-set" in self.args:
            # option to config.py.
            self.args.remove("-set")
        if len(self.args) > 1:
            self.log.error("Expected only one argument. If testing from command line, wrap arguments in double quotes.")
        self.args = self.args[0] if len(wf.args) > 0 else ""
        
    def execute(self):
        if self.wf.update_available:
            self.wf.add_item('New version available',
                        'Action this item to install the update',
                        autocomplete='workflow:update',
                        icon=ICON_INFO)
        
        sys.exit(self.wf.run(self.main))

    def main(self, wf):
        pass

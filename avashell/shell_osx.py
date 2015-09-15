# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals

import os
import logging
import AppKit

from Foundation import (NSDate, NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSSearchPathForDirectoriesInDomains,
                        NSMakeRect, NSLog, NSObject)

from AppKit import *

from avashell.utils import resource_path
from avashell.shell_base import ShellBase, STR_EXIT, STR_OPEN_HELP

logger = logging.getLogger(__name__)


def applicationSupportFolder(self):
    paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,NSUserDomainMask,True)
    basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
    fullPath = basePath.stringByAppendingPathComponent_("Ava")
    if not os.path.exists(fullPath):
        os.mkdir(fullPath)
    return fullPath


class AppDelegate(NSObject):
    def init(self):
        # self = super(AppDelegate, self).init()
        if self is None:
            return None

        return self

    def applicationDidFinishLaunching_(self, sender):
        logger.debug("Application did finish launching.")

        logger.debug("Icon file: %s", resource_path('ava/res/eavatar.png'))
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.icon = NSImage.alloc().initByReferencingFile_(resource_path('res/icon.png'))
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)
    	self.statusitem.setHighlightMode_(True)
        self.statusitem.setEnabled_(True)

        #make the menu
        self.menubarMenu = NSMenu.alloc().init()

        self.openItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(STR_OPEN_HELP, 'openHelp:', '')
        self.menubarMenu.addItem_(self.openItem)

        self.menuItem = NSMenuItem.separatorItem()
        self.menubarMenu.addItem_(self.menuItem)

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(STR_EXIT, 'quitApp:', '')
        self.menubarMenu.addItem_(self.quit)

        #add menu to statusitem
        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_(u'AvaShell - running')

    def applicationWillTerminate_(self, sender):
        logger.debug("Application will terminate.")

    def openHelp_(self, notification):

        self.shell.open_help()

    def quitApp_(self, notification):
        nsapplication = NSApplication.sharedApplication()
        logger.debug('closing application')
        nsapplication.terminate_(notification)


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()

        self.app = None
        self.delegate = None
        self.mainframe = None

    def run(self):

        self.app = NSApplication.sharedApplication()
        self.app.activateIgnoringOtherApps_(True)
        self.delegate = AppDelegate.alloc().init()
        self.delegate.shell = self
        self.delegate.app = self.app
        self.app.setDelegate_(self.delegate)

        self.app.run()

if __name__ == '__main__':
    shell = Shell()
    shell.run()

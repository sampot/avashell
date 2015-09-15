# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from abc import abstractmethod

import webbrowser

STR_OPEN_HELP = u'Help...'
STR_EXIT = u'Quit AvaShell'
STR_STATUS = u'AvaShell - running'

class ShellBase(object):

    def __init__(self):
        pass

    def open_help(self):
        webbrowser.open('https://samkuo.me')  # changed to wherever your doc is

    @abstractmethod
    def run(self):
        """ Starts up the shell.
        """
        pass

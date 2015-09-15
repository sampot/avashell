# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from abc import abstractmethod
from threading import Thread

import webbrowser

STR_OPEN_HELP = u'Help...'
STR_EXIT = u'Quit AvaShell'
STR_STATUS = u'AvaShell - running'

import avashell.exports

_logger = logging.getLogger(__name__)

try:
    from avaconfig import *
except ImportError:
    pass

class ShellBase(object):

    def __init__(self):
        pass

    def open_help(self):
        webbrowser.open('https://samkuo.me')  # changed to wherever your doc is

    def run_script(self):

        try:
            import avastartup
        except:
            _logger.exception("Error in running avastartup script.")

    def run(self):
        t = Thread(target=self.run_script)
        t.setDaemon(True)
        t.start()

        self._run()

    @abstractmethod
    def _run(self):
        """ Starts up the shell.
        """
        pass

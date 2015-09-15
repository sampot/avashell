# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

from avashell.utils import resource_path
from avashell.shell_base import ShellBase, STR_EXIT, STR_OPEN_HELP


class StatusIcon(object):
    def __init__(self, shell):
        self.shell = shell
        self.ind = appindicator.Indicator.new("AvaShell-indicator",
                                           resource_path("res/icon.png"),
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_icon_theme_path(resource_path('res/'))

        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon("icon.png")

        self.menu_setup()
        self.ind.set_menu(self.menu)

    def menu_setup(self):
        self.menu = Gtk.Menu()

        self.open_item = Gtk.MenuItem.new_with_label(STR_OPEN_HELP)
        self.open_item.connect("activate", self.on_open_help)
        self.open_item.show()

        self.quit_item = Gtk.MenuItem.new_with_label(STR_EXIT)
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()

        self.menu.append(self.open_item)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(self.quit_item)

    def on_open_help(self, sender):
        self.shell.open_help()

    def quit(self, widget):
        self.ind.set_status(appindicator.IndicatorStatus.PASSIVE)
        Gtk.main_quit()


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()
        self.statusIcon = StatusIcon(self)

    def run(self):
        Gtk.main()


if __name__ == '__main__':
    shell = Shell()
    shell.run()


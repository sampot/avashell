# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import os

import win32api
import win32con
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

import itertools
import glob

from avashell.utils import resource_path
from avashell.shell_base import ShellBase, STR_OPEN_HELP, STR_EXIT, STR_STATUS


class MainFrame(object):
    def __init__(self, message_map):
        self.window_class_name = "AvaShellWnd"
        self.hinst = None
        self.class_atom = self.register_wnd_class(message_map)
        self.hwnd = self.create_window()

    def register_wnd_class(self, message_map):
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        self.hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # could also specify a wndproc.
        return win32gui.RegisterClass(window_class)

    def create_window(self):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = win32gui.CreateWindow(self.class_atom,
                                     self.window_class_name,
                                     style,
                                     0,
                                     0,
                                     310,
                                     250,
                                     0,
                                     0,
                                     self.hinst,
                                     None)
        win32gui.UpdateWindow(hwnd)
        return hwnd

    def show(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)

    def close(self):
        win32gui.PostQuitMessage(0)


_QUIT = 'QUIT'

_FIRST_ID = 1023
_ID_OPEN_HELP = 1024
_ID_QUIT = 1100


class StatusIcon(object):
    def __init__(self, s):
        self.shell = s

        self.icons = itertools.cycle(glob.glob(resource_path('res/*.ico')))
        self.hover_text = STR_STATUS

        self.menu_options = ((STR_OPEN_HELP, None, None, _ID_OPEN_HELP),
                             ("-", None, None, 1025),
                             (STR_EXIT, None, None, _ID_QUIT),)

        self.icon = self.icons.next()

        self.default_menu_index = 0

        self.notify_id = None
        self.hicon = None
        self.refresh_icon()

    def refresh_icon(self):
        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            self.hicon = win32gui.LoadImage(hinst,
                                            self.icon,
                                            win32con.IMAGE_ICON,
                                            0,
                                            0,
                                            icon_flags)
        else:
            print("Can't find icon file - using default.")
            self.hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        self.notify_id = (self.shell.main_frame.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20,
                          self.hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)

        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.shell.main_frame.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.shell.main_frame.hwnd,
                                None)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[
                                                                  ::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_text == "-":
                win32gui.InsertMenu(menu, 0, win32con.MF_BYPOSITION,
                                    win32con.MF_SEPARATOR, None)
            else:
                item, extras = win32gui_struct.PackMENUITEMINFO(
                    text=option_text,
                    hbmpItem=option_icon,
                    wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y,
                                   win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0,
                            win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def switch_icon(self):
        self.icon = self.icons.next()
        self.refresh_icon()


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()

        msg_taskbar_restart = win32gui.RegisterWindowMessage("TaskbarCreated")
        self.message_map = {msg_taskbar_restart: self.OnRestart,
                            win32con.WM_DESTROY: self.OnDestroy,
                            win32con.WM_COMMAND: self.OnCommand,
                            win32con.WM_USER + 20: self.OnTaskbarNotify, }

        self.main_frame = MainFrame(self.message_map)
        self.status_icon = StatusIcon(self)

    def run(self):
        # while not win32gui.PumpWaitingMessages():
        #    time.sleep(0.1)
        win32gui.PumpMessages()

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self.status_icon.refresh_icon()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.main_frame.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(_FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP:
            self.status_icon.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:
            pass

        return True

    def execute_menu_option(self, id):
        if id == _ID_QUIT:
            win32gui.DestroyWindow(self.main_frame.hwnd)
        elif id == _ID_OPEN_HELP:
            self.open_help()



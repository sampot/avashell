# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

def create_shell():
    """
    Creates the shell based on a specified platform.

    :param platform: The platform identifier.
    :return:
    """
    plat = sys.platform
    if plat.startswith("win32"):
        from avashell.shell_win32 import Shell
    elif plat.startswith("darwin"):
        from avashell.shell_osx import Shell
    elif plat.startswith("linux"):
        from avashell.shell_gtk import Shell
    else:
        print("Unsupported platform.", file=sys.stderr)
        sys.exit(-1)

    return Shell()


def main():
    shell = create_shell()
    shell.run()

if __name__ == '__main__':
    main()

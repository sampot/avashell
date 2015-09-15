# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


# import packages/modules that you want the startup script can access

import os
import sys
import logging
import logging.config
import sqlite3
import _sqlite3

# workaround for missing codec in Tiny core linux
from encodings import hex_codec, ascii, utf_8, utf_32
from click import group, command

from avashell import utils
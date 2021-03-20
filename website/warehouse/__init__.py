from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
server_directory = os.path.abspath(os.path.join(BASE_DIR, 'server'))
warehouse_directory = Path(__file__).resolve().parent
sys.path.append(server_directory)
sys.path.append(warehouse_directory)

import asyncio
import time
from .server_setup import *

asyncio.run(m.main())
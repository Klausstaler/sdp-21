from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

import sys
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
server_directory = os.path.abspath(os.path.join(BASE_DIR.parent, 'server'))
warehouse_directory = Path(__file__).resolve().parent
design_directory = os.path.abspath(os.path.join(BASE_DIR, 'design'))

sys.path.append(server_directory)
sys.path.append(warehouse_directory)
sys.path.append(design_directory)
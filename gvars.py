# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from os import environ
from os.path import expanduser, dirname, abspath
from sys import platform as sysplatform

home = expanduser("~")
PLATFORM_LOCATIONS = {"linux": ".config",
                      "darwin": ".config"}
VERSION = "0.0.2"
FILE_DIRECTORY = dirname(abspath(__file__))

if sysplatform.startswith("win"):
    OS = "Windows"
    DATA_PATH = environ["APPDATA"] + "\\AlreadyClaimedNotifier"
else:
    if sysplatform.startswith("linux"):
        OS = "Linux"
    elif sysplatform == "darwin":
        OS = "Mac"
    else:
        OS = sysplatform.title()
    DATA_PATH = home + "/" + PLATFORM_LOCATIONS[sysplatform] + "/AlreadyClaimedNotifier"

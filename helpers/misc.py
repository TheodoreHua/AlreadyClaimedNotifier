# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from tkinter import Tk
from tkinter.messagebox import showerror as _showerror, askyesno as _askyesno

def showerror(*args, **kwargs):
    Tk().withdraw()
    _showerror(*args, **kwargs)

def askyesno(*args, **kwargs):
    Tk().withdraw()
    return _askyesno(*args, **kwargs)

def notify(notifier, title:str, text:str):
    notifier.title = title
    notifier.text = text
    notifier.send(block=False)

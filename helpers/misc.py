# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from tkinter import Tk
from tkinter.ttk import Label, Button

def showerror(title="", message=""):
    m = Tk()
    m.title(title)
    m.wm_attributes("-topmost", 1)
    m.resizable(0, 0)
    Label(m, text=message).grid(row=0, column=0)
    Button(m, command=m.destroy, text="Ok").grid(row=1, column=0, sticky="WE")
    m.mainloop()

def askyesno(title="", message=""):
    status = False
    def callback():
        nonlocal status
        status = True
        m.destroy()
    m = Tk()
    m.title(title)
    m.wm_attributes("-topmost", 1)
    m.resizable(0, 0)
    Label(m, text=message).grid(row=0, column=0, columnspan=2)
    Button(m, command=callback, text="Yes").grid(row=1, column=0, sticky="WE")
    Button(m, command=m.destroy, text="No").grid(row=1, column=1, sticky="WE")
    m.mainloop()
    return status

def notify(notifier, title:str, text:str):
    notifier.title = title
    notifier.text = text
    notifier.send(block=False)

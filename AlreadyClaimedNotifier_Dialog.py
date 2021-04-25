# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import os
from time import sleep
from tkinter import Tk
from tkinter.messagebox import showerror as _showerror, askyesno as _askyesno
from webbrowser import open as wbopen

import praw
import pystray
from PIL import Image
from praw.exceptions import MissingRequiredAttributeException

from file_handler import get_praw, get_config, get_checked, get_reply, assert_data, file_checked
from gvars import VERSION, FILE_DIRECTORY


def askyesno(*args, **kwargs):
    Tk().withdraw()
    return _askyesno(*args, **kwargs)


def callback():
    while True:
        for comment in reddit.inbox.comment_replies():
            if comment.id not in checked_entries:
                if comment.body in get_reply() and comment.author.name == "transcribersofreddit":
                    submission = comment.submission
                    open_link = askyesno(title="POST IS ALREADY CLAIMED",
                                         description="WARNING: Post with title {} has already been claimed! Click 'Yes' to open"
                                                     " the page".format(submission.title))
                    if open_link:
                        wbopen(submission.permalink)
                checked_entries.append(comment.id)
        sleep(config["delay"])


def terminate_loop():
    file_checked(checked_entries)
    os._exit(0)


def showerror(*args, **kwargs):
    Tk().withdraw()
    _showerror(*args, **kwargs)


assert_data()
config = get_config()
checked_entries = get_checked()
claimed_reply = get_reply()

if config["os"] in [None, ""] or config["user"] in [None, ""]:
    showerror(title="Error", message="Missing config values, exiting...")
    exit()
else:
    try:
        reddit = praw.Reddit(user_agent=config["os"] + ":alreadyclaimednotifier:v" + VERSION + "(by u/--B_L_A_N_K--)",
                             **get_praw())
    except MissingRequiredAttributeException:
        showerror(title="Credentials Error", message="Missing one or more required credentials")
        exit()

image = Image.open(FILE_DIRECTORY + "/icon.png")
icon = pystray.Icon("ACN Ver " + VERSION, image, menu=pystray.Menu(pystray.MenuItem("Exit Program", terminate_loop)))
icon.visible = True
icon.run(setup=lambda icon: callback())

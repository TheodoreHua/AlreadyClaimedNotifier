# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import os
from time import sleep, time
from tkinter import Tk
from tkinter.messagebox import showerror as _showerror, askyesno as _askyesno
from webbrowser import open as wbopen

import praw
import pystray
import requests
from PIL import Image
from packaging import version
from praw.exceptions import MissingRequiredAttributeException
from win10toast_click import ToastNotifier

from file_handler import get_praw, get_config, get_checked, get_reply, assert_data, file_checked
from gvars import VERSION, FILE_DIRECTORY, OS


def callback():
    toast = ToastNotifier()
    while True:
        for comment in reddit.inbox.comment_replies():
            if comment.id not in checked_entries:
                if comment.author.name == "transcribersofreddit" and time() - comment.created_utc < 86400:
                    for r in claimed_reply:
                        if comment.body in r:
                            submission = comment.submission
                            toast.show_toast("POST IS ALREADY CLAIMED",
                                             "WARNING: Post with title {} has already been claimed! Click this notification to open"
                                             " the page".format(submission.title),
                                             duration=config["notification_duration"],
                                             icon_path=FILE_DIRECTORY + "/icon.ico", callback_on_click=
                                             lambda link=submission.permalink: wbopen("www.reddit.com" + link))
                            break
                checked_entries.append(comment.id)
        sleep(config["delay"])


def terminate_loop():
    file_checked(checked_entries)
    # noinspection PyProtectedMember
    os._exit(0)


def showerror(*args, **kwargs):
    Tk().withdraw()
    _showerror(*args, **kwargs)


def askyesno(*args, **kwargs):
    Tk().withdraw()
    return _askyesno(*args, **kwargs)


assert_data()
config = get_config()
checked_entries = get_checked()
claimed_reply = get_reply()

if config["user"] in [None, ""]:
    showerror(title="Error", message="Missing config values, exiting...")
    exit()
elif OS != "Windows":
    showerror(title="Error, Not Supported", description="ACN Notification is only supported on Windows, for support"
                                                        " in other operating systems, use ACN Dialog.")
    exit()
else:
    try:
        reddit = praw.Reddit(user_agent=OS + ":alreadyclaimednotifier:v" + VERSION + "(by u/--B_L_A_N_K--)",
                             **get_praw())
    except MissingRequiredAttributeException:
        showerror(title="Credentials Error", message="Missing one or more required credentials")
        exit()

# Check for updates
if config["update_check"]:
    # Check GitHub API endpoint
    resp = requests.get("https://api.github.com/repos/TheodoreHua/AlreadyClaimedNotifier/releases/latest")
    # Check whether response is a success
    if resp.status_code == 200:
        resp_js = resp.json()
        # Check whether the version number of remote is greater than version number of local (to avoid dev conflict)
        if version.parse(resp_js["tag_name"][1:]) > version.parse(VERSION):
            # Ask user whether or not they want to open the releases page
            yn_resp = askyesno("New Version",
                               "A new version ({}) is available.\n\nPress yes to open page and no to ignore.\nUpdate "
                               "checking can be disabled in config.".format(resp_js["tag_name"]))
            if yn_resp:
                wbopen("https://github.com/TheodoreHua/AlreadyClaimedNotifier/releases/latest")
    else:
        showerror(title="Error",
                  message="Received status code {} while trying to check for updates.".format(resp.status_code))

image = Image.open(FILE_DIRECTORY + "/icon.png")
icon = pystray.Icon("ACN Ver " + VERSION, image, menu=pystray.Menu(pystray.MenuItem("ACN Ver " + VERSION, lambda: None,
                                                                                    enabled=False),
                                                                   pystray.MenuItem("Exit Program", terminate_loop)))
icon.visible = True
icon.run(setup=lambda icon: callback())

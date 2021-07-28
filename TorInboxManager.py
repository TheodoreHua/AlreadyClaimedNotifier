# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from argparse import ArgumentParser
from time import sleep, time
from webbrowser import open as wbopen

import praw
import requests
from notifypy import Notify
from packaging import version
from praw.exceptions import MissingRequiredAttributeException
from alive_progress import alive_bar

from gvars import OS, VERSION
from helpers import *


def main():
    # Generate notifier object
    notifier = Notify(default_notification_application_name="ToR Inbox Manager", default_notification_icon="icon.png")

    # Perform data checks
    assert_data()
    config = get_config()
    checked_entries = get_checked()
    if config["checks"]["already_claimed"]:
        claimed_replies = get_replies()

    if config["user"] in [None, ""]:
        showerror(title="Error", message="Missing config value user")
        exit()
    else:
        # Create Reddit Instance
        try:
            reddit = praw.Reddit(user_agent=OS + ":torinboxmanager:v" + VERSION + "(by /u/--B_L_A_N_K--)", **get_praw())
        except MissingRequiredAttributeException:
            showerror(title="Credentials Error", message="Missing one or more required PRAW credentials")
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

    # Mainloop
    try:
        while True:
            print("Starting check with a limit of {}".format(config["limit"]))
            with alive_bar(config["limit"]) as bar:
                # noinspection PyUnboundLocalVariable
                for comment in reddit.inbox.comment_replies(limit=config["limit"]):
                    if comment.id not in checked_entries and type(comment.author) is not type(None) and \
                            comment.author.name == "transcribersofreddit" and time() - comment.created_utc < 86400:
                        if config["checks"]["already_claimed"]:
                            # noinspection PyUnboundLocalVariable
                            for r in claimed_replies:
                                if comment.body in r:
                                    submission = comment.submission
                                    if config["dialog"]:
                                        if askyesno("Already Claimed", "{} is already claimed, press Yes to open it"
                                                .format(submission.title)):
                                            wbopen("www.reddit.com" + submission.permalink)
                                    else:
                                        notify(notifier, "Already Claimed", "{} is already claimed, check the CLI for the link"
                                               .format(submission.title))
                                    print("Already claimed post found ({}): https://www.reddit.com/{}"
                                          .format(submission.title, submission.permalink))
                    checked_entries.append(comment.id)
                    bar()
            print("Checking completed, waiting {} seconds before next check".format(config["delay"]))
            file_checked(checked_entries)
            sleep(config["delay"])
    except KeyboardInterrupt:
        file_checked(checked_entries)


if __name__ == "__main__":
    parser = ArgumentParser(description="Manage your inbox easier while transcribing")
    args = parser.parse_args()

    if len(vars(args)) < 1:
        print("Terminate the program using Ctrl + C")
        main()


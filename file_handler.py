# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import configparser
import json
from os import mkdir
from os.path import isfile, isdir

from gvars import DATA_PATH


def get_praw():
    config = configparser.ConfigParser()
    config.read(DATA_PATH + "/praw.ini")
    return dict(config["credentials"])


def get_config():
    config = configparser.ConfigParser()
    config.read(DATA_PATH + "/config.ini")
    cfg = dict(config["CONFIG"])
    for name, value in cfg.items():
        if name in ["delay", "notification_duration"]:
            cfg[name] = int(value)
        elif name in ["update_check"]:
            cfg[name] = bool(int(value))
    return cfg


def get_checked():
    with open(DATA_PATH + "/data/checked.json", "r") as f:
        return json.load(f)


def get_reply():
    with open(DATA_PATH + "/data/reply.txt", "r") as f:
        return f.read()


def file_checked(new_entries: list):
    with open(DATA_PATH + "/data/checked.json", "w") as f:
        json.dump(new_entries, f)


def assert_data():
    """Method to check if the data files exists, if it doesn't exist, create it"""
    if not isdir(DATA_PATH):
        mkdir(DATA_PATH)
    if not isdir(DATA_PATH + "/data"):
        mkdir(DATA_PATH + "/data")
    if not isfile(DATA_PATH + "/config.ini"):
        config = configparser.ConfigParser(allow_no_value=True, comment_prefixes=("#", "l"))
        config["CONFIG"] = {"delay": "10",
                            "user": "Username",
                            "notification_duration": "15",
                            "update_check": "1"}
        config["notes"] = {}
        config.set("notes", "; Fill in the above values according to the README")
        with open(DATA_PATH + "/config.ini", "w") as f:
            config.write(f)
    if not isfile(DATA_PATH + "/praw.ini"):
        config = configparser.ConfigParser(allow_no_value=True, comment_prefixes=("#", ";"))
        config["credentials"] = {"client_id": "",
                                 "client_secret": "",
                                 "username": "usernamehere",
                                 "password": "passwordhere"}
        config["notes"] = {}
        config.set("notes", "; Replace usernamehere and passwordhere with your username and password. If 2FA is "
                            "enabled on your account then follow the instructions in the README")
        with open(DATA_PATH + "/praw.ini", "w") as f:
            config.write(f)
    if not isfile(DATA_PATH + "/data/checked.json"):
        with open(DATA_PATH + "/data/checked.json", "w") as f:
            json.dump([], f)
    if not isfile(DATA_PATH + "/data/reply.txt"):
        with open(DATA_PATH + "/data/reply.txt", "w") as f:
            f.write(
                """I'm sorry, but it looks like someone else has already claimed this post! You can check in with them to see if they need any help, but otherwise I suggest sticking around to see if another post pops up here in a little bit.
                
                
                ---
                
                v0.6.0 | This message was posted by a bot. | [FAQ](https://www.reddit.com/r/TranscribersOfReddit/wiki/index) | [Source](https://github.com/GrafeasGroup/tor) | Questions? [Message the mods!](https://www.reddit.com/message/compose?to=%2Fr%2FTranscribersOfReddit&subject=Bot%20Question&message=)""")

# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

"""
DO NOT USE AUTO-REFORMAT CODE IN THIS FILE, IT WILL BREAK THE DEFAULT REPLIES.
"""

import configparser
import json
from os import mkdir, listdir
from os.path import isfile, isdir, join

from gvars import DATA_PATH

CONFIG_VALUES = {"delay": "10",
                 "user": "Username",
                 "notification_duration": "15",
                 "update_check": "1"}

DEFAULT_REPLIES = [
"""I'm sorry, but it looks like someone else has already claimed this post! You can check in with them to see if they need any help, but otherwise I suggest sticking around to see if another post pops up here in a little bit.


---

v0.6.0 | This message was posted by a bot. | [FAQ](https://www.reddit.com/r/TranscribersOfReddit/wiki/index) | [Source](https://github.com/GrafeasGroup/tor) | Questions? [Message the mods!](https://www.reddit.com/message/compose?to=%2Fr%2FTranscribersOfReddit&subject=Bot%20Question&message=)""",
"""This post has already been completed! Perhaps you can find a new one on the front page?


---

v0.6.0 | This message was posted by a bot. | [FAQ](https://www.reddit.com/r/TranscribersOfReddit/wiki/index) | [Source](https://github.com/GrafeasGroup/tor) | Questions? [Message the mods!](https://www.reddit.com/message/compose?to=%2Fr%2FTranscribersOfReddit&subject=Bot%20Question&message=)"""
]


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
    reply_list = []
    for i in [j for j in listdir(DATA_PATH + "/data/replies") if isfile(join(DATA_PATH + "/data/replies", j))]:
        with open(DATA_PATH + "/data/replies/" + i, "r") as k:
            reply_list.append(k.read())
    return reply_list


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
        config["CONFIG"] = CONFIG_VALUES
        config["notes"] = {}
        config.set("notes", "; Fill in the above values according to the README")
        with open(DATA_PATH + "/config.ini", "w") as f:
            config.write(f)
    else:
        oldconfig = get_config()
        missing_keys = []
        for needed_key in CONFIG_VALUES.keys():
            if needed_key not in oldconfig.keys():
                missing_keys.append(needed_key)
        if len(missing_keys) > 0:
            with open(DATA_PATH + "/config.ini", "w") as f:
                new_data = {i:str(j) if i not in ["update_check"] else "1" if j else "0" for i, j in oldconfig.items()}
                for missing_key in missing_keys:
                    # noinspection PyTypeChecker
                    new_data[missing_key] = CONFIG_VALUES[missing_key]
                config = configparser.ConfigParser(allow_no_value=True, comment_prefixes=("#", "l"))
                # noinspection PyTypeChecker
                config["CONFIG"] = new_data
                config["notes"] = {}
                config.set("notes", "; Fill in the above values according to the README")
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
    if not isdir(DATA_PATH + "/data/replies"):
        mkdir(DATA_PATH + "/data/replies")
        for i, reply in enumerate(DEFAULT_REPLIES):
            with open(DATA_PATH + "/data/replies/reply{}.txt".format(i + 1), "w") as f:
                f.write(reply)

#!/usr/bin/env python
import random
import socket
import sys
from configparser import ConfigParser
from webbrowser import open as wbopen

import praw

from gvars import DATA_PATH


def receive_connection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 9575))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send("HTTP/1.1 200 OK\r\n\r\n{}".format(message).encode("utf-8"))
    client.close()


def main():
    """Provide the program's entry point when directly executed."""
    config = ConfigParser()
    config.read(DATA_PATH + "/praw.ini")
    client_id = config["credentials"]["client_id"]
    client_secret = config["credentials"]["client_secret"]
    scopes = ["privatemessages"]

    reddit = praw.Reddit(
        client_id=client_id.strip(),
        client_secret=client_secret.strip(),
        redirect_uri="http://localhost:9575",
        user_agent="praw_refresh_token_example",
    )
    state = str(random.randint(0, 65000))
    url = reddit.auth.url(scopes, state, "permanent")
    print("If it didn't automatically open, click the following link: " + url)
    wbopen(url)
    sys.stdout.flush()

    client = receive_connection()
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value
        for (key, value) in [token.split("=") for token in param_tokens]
    }

    if state != params["state"]:
        send_message(
            client,
            "State mismatch. Expected: {} Received: {}".format(
                state, params["state"]
            ),
        )
        return 1
    elif "error" in params:
        send_message(client, params["error"])
        return 1

    refresh_token = reddit.auth.authorize(params["code"])
    try:
        del config
        config = ConfigParser()
        config["credentials"] = {"client_id": client_id,
                                 "client_secret": client_secret,
                                 "refresh_token": refresh_token}
        with open(DATA_PATH + "/praw.ini", "w") as f:
            config.write(f)
    except:
        send_message(client, "WARNING: VALUE HAS NOT BEEN AUTOMATICALLY ENTERED!\nCopy paste the following 3 lines into"
                             " the praw.ini file and delete everything that was there originally:\n[credentials]\n"
                             "client_id = {}\nclient_secret = {}\nrefresh_token = {}\n".format(client_id,
                                                                                               client_secret,
                                                                                               refresh_token))
    else:
        send_message(client, "Value has successfully been automatically entered, you can close this window now.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

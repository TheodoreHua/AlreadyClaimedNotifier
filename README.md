# Already Claimed Notifier

[![Inactively Maintained](https://img.shields.io/badge/Maintenance%20Level-Inactively%20Maintained-yellow.svg)](https://github.com/TheodoreHua/MaintenanceLevels#inactively-maintained)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/theodorehuadev@gmail.com)  
[![GitHub issues](https://img.shields.io/github/issues/TheodoreHua/AlreadyClaimedNotifier)](https://github.com/TheodoreHua/AlreadyClaimedNotifier/issues)
![GitHub pull requests](https://img.shields.io/github/issues-pr/TheodoreHua/AlreadyClaimedNotifier)
[![GitHub license](https://img.shields.io/github/license/TheodoreHua/AlreadyClaimedNotifier)](https://github.com/TheodoreHua/AlreadyClaimedNotifier/blob/master/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/TheodoreHua/AlreadyClaimedNotifier)](https://github.com/TheodoreHua/AlreadyClaimedNotifier/releases/latest)
![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/TheodoreHua/AlreadyClaimedNotifier/latest)
![GitHub repo size](https://img.shields.io/github/repo-size/TheodoreHua/AlreadyClaimedNotifier)

**This is an unofficial program and is not officially endorsed by the Transcribers of Reddit; they are in no way
involved with this program and are not liable for any matters relating to it.**

*This program serves to assist you by sending you notifications when the post you claimed was already claimed. You
should not solely rely on this program and continue to be cautious when claiming and finishing posts. I take no liablity
for any issues that happen as a result of using this program*

Also known as ACN, this program sends a notification to the user when it detects a comment reply stating that the post
their doing has already been claimed. It is designed with r/TranscribersOfReddit transcribers in mind; specifically
those who don't want to summon an angry mod...

## Versions
### ACN Notification
`AlreadyClaimedNotifier_Notification.pyw`

- **Is only supported on Windows**
- Utilizes Window's notification system to show warnings

### ACN Dialog
`AlreadyClaimedNotifier_Dialog.pyw`

- Is supported on all operating systems
- Uses a popup warning dialog to show warnings

## Installation and Use

1. Download the latest stable release from the releases page and extract it to a folder of your choice.
2. Run `pip install -r requirements.txt` in the folder where you extracted the files (you might need to do so as
   root/admin).
3. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to
   `https://www.reddit.com/prefs/apps/` and creating a new app. Give it a name ("AlreadyClaimedNotifier" or "ACN" are
   easy to remember). Choose "script". Give it a description (which can really be anything you want). Set the redirect
   url to `http://localhost:9575` as this may be important later on. You can set the about url as whatever you want (I
   set it to the ACN repo link).
4. Run the program once then close it, don't worry if it says that there are missing config values.
5. Now open up file explorer and go to `C:\Users\Username\AppData\Roaming\AlreadyClaimedNotifier` or, press the Windows 
   Key + R and enter `%APPDATA%\AlreadyClaimedNotifier`.
6. Open up the file named `config.ini` and input the values as specified by the name.
7. Open `praw.ini` and fill in the client ID and client secret obtained in step 3 (Client ID is located under the text 
   `personal use script` and Client Secret is under the `secret` section). Now fill in your username and password. 
   Note that if you have 2FA enabled on your account you MUST use a refresh token, to see how to do this go to the 
   [Obtaining a Refresh Token](#obtaining-a-refresh-token) section.
8. Done

Once you're done, just navigate to the folder where `AlreadyClaimedNotifier_Notification.pyw` or 
`AlreadyClaimedNotifier_Dialog.pyw` is and run the file. You might run with an IDE you have installed, or simply run 
itself, or you can run it from the command line. On Windows, you do it like this: 
`python AlreadyClaimedNotifier_Notification.pyw` or `python AlreadyClaimedNotifier_Dialog.pyw`. The application doesn't 
have a window and instead runs in the background, you can see if it's running by looking at the tray and looking for the
[icon](#icon). You can close the program by right-clicking the icon and clicking Exit Program. If this 
doesn't work, terminate it in Task Manager.

## Other Instructions

### Config Values
- ***Delay***: The amount of time between each checking cycle in seconds. The lower the number is, the more resources 
  the program will use. This is generally fine for high-end computers (so long as you don't set it under around 0.025)
  but for lower-end ones, I'd recommend a higher number.
  - Default: `10`
- ***User***: Your username
  - Default: `Username`
- ***Notification Duration***: The amount of time the notification shows on your screen in seconds. Note that the 
  program will NOT be checking for new claimed posts while the notification shows.
  - Default: `15`
  - Is not used on Dialog version however is still required to be filled to avoid parsing errors.

### Obtaining a Refresh Token
Run `get_refreshtoken.py` (remember to do this only AFTER you've filled in the `client_id` and `client_secret`, it's 
fine if you leave `username`, `password`, and `refresh_token` blank.), it should open up a page in your browser 
automatically, if not, you'll have to manually click the link. Follow the flow on Reddit and once it's done, it should 
automatically fill in the values for you behind the scene. If you get an error saying `invalid redirect_uri parameter`,
make sure you have `http://localhost:9575` set as the redirect uri in the reddit app (exactly that). If you get an 
output saying that it was not succesfully entered automatically, you'll have to copy & paste all the lines in the 
output (except the notice) and paste it into the `praw.ini` file, deleting everything that was there originally.

## Icon

**Credits to [@chakeson](https://github.com/chakeson) for making the icon**

![Program Icon](icon.png)

## FAQ

#### Can I add more variants of replies to check for?
Yes, you can go to the subfolder `data/replies` 
([how to get to the data folder](#where-are-the-config-and-data-files-located)) and create a new file (named anything 
you want, without spaces) and paste the exact raw markdown reply you want to check for in it. By default, it already 
has 2 replies (post is already claimed, post is already completed). You can find a list of some bot replies 
[here](https://github.com/GrafeasGroup/tor/blob/main/tor/strings/en_US.yml) (You have to copy the reply text 
then add the footer in with 2 new lines seperating the last line of the response and the `---`. an alternative is to 
find a comment and open it up in old reddit, pressing the `source` button and copy-pasting the entirety of it into 
the file).

#### Can I use this to get a reply for the bot can't find my transcription?
Yes, you can add the can't find a transcript reply following the 
[instructions](#can-i-add-more-variants-of-replies-to-check-for). Note that the notification will still warn you about the 
post being already claimed instead of saying that it didn't detect your transcription, but it still works in that it 
sends you a notification. I may add a separate feature that checks for that itself and gives a more appropriate warning,
however that's a low priority feature as it still works using this method.

#### I messed up something in the configuration settings, and now it won't start/is crashing, what should I do?

Try to look at the error and correct it by editing `config.json` or `praw.ini` by yourself (See below FAQ on where the
files are located). If the error cannot be resolved by yourself, delete the `config.json` and/or `praw.ini` files, then
run ACN. The program will re-create the files, and you'll be good to go. You **WILL** have to re-setup the config and 
PRAW files.

#### Where are the config and data files located?

##### Windows:

`C:\Users\your_username\AppData\Roaming\AlreadyClaimedNotifier`

##### Linux:

`/home/your_username/.config/AlreadyClaimedNotifier`

##### MacOS:

Should be `/home/your_username/.config/AlreadyClaimedNotifier` although I'm not certain

#### Where can I contact the developer?

If you want to report an issue with ACN you can
[open a bug report](https://github.com/TheodoreHua/AlreadyClaimedNotifier/issues/new), otherwise you can email me
at `theodorehuadev@gmail.com`.

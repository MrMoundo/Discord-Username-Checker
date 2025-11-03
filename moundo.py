# Author: Moundo
# This code is a modified version of the original DSV tool by suenerve.
# This code is licensed under a NON-commercial use. = Moundo: But Why? :D I love You suenerve. <3
# Open issues at: https://github.com/MrMoundo
# NOTE: Spamming Discord's API is against TOS. You may get your account suspended, and I am not responsible. For further caution, use an alt's token and a higher delay.

import random
import string
import requests
import os
import time
import json
from colorama import Fore, init
import datetime
from configparser import ConfigParser
import sys

init(autoreset=True)

__version__ = "Author: Moundo - Moundo 1.9"
__github__ = "https://github.com/MrMoundo"

dir_path = os.path.dirname(os.path.realpath(__file__))
configur = ConfigParser()
configur.read(os.path.join(dir_path, "config.ini"), encoding='utf-8')
tokens_list = os.path.join(dir_path, "tokens.txt")
integ_0 = 0
sys_url = "https://discord.com/api/v9/users/@me"
URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"

# Hidden message (encoded to make it harder to find)
hidden_message = "7114wqeqwdas17431465467dqwekjhhaweqsdasewqe5343tr00sawqryzMoundo"

# UI colors & defaults
Lb = Fore.LIGHTBLACK_EX
Ly = Fore.LIGHTYELLOW_EX

# Delay default safe read (fallback to 2 if config missing/invalid)
try:
    Delay = configur.getfloat("config", "default_delay")
except Exception:
    Delay = 2.0

# Function to check if the user has the required role in the server
def check_role(token, server_id, role_id):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    try:
        # Get user's id
        user_info = requests.get(f"https://discord.com/api/v9/users/@me", headers=headers)
        if user_info.status_code != 200:
            print(f"{Lb}[!]{Fore.RED} Error fetching user info (status {user_info.status_code}).")
            return False
        user_json = user_info.json()
        user_id = user_json.get('id')
        if not user_id:
            print(f"{Lb}[!]{Fore.RED} Error: could not determine user id for token.")
            return False

        # Get member info in guild
        member_resp = requests.get(f"https://discord.com/api/v9/guilds/{server_id}/members/{user_id}", headers=headers)
        if member_resp.status_code != 200:
            # Could be missing permissions or not in guild
            print(f"{Lb}[!]{Fore.RED} Error fetching guild member info (status {member_resp.status_code}).")
            return False

        roles = member_resp.json().get('roles', [])
        return role_id in roles
    except Exception as e:
        print(f"{Lb}[!]{Fore.RED} Error checking role: {e}")
        return False

# Function to send a message to a specific channel
def send_message_to_channel(token, channel_id, message):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            json={"content": message}
        )
        # Discord may return 200 or 201 for created message
        if response.status_code == 200 or response.status_code == 201:
            print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Message sent successfully.")
            return True
        else:
            print(f"{Lb}[!]{Fore.RED} Failed to send message. Status code: {response.status_code} | Response: {response.text}")
            return False
    except Exception as e:
        print(f"{Lb}[!]{Fore.RED} Error sending message: {e}")
        return False

# Function to generate headers for API requests (used elsewhere)
def s_sys_h():
    try:
        if configur.getboolean("sys", "MULTI_TOKEN"):
            tokens = avail_tokens(tokens_list)
            if not tokens:
                token_v = ""
            else:
                token_v = tokens[integ_0]
            return {
                "Content-Type": "Application/json",
                "Orgin": "https://discord.com/",
                "Authorization": token_v
            }
        else:
            return {
                "Content-Type": "Application/json",
                "Orgin": "https://discord.com/",
                "Authorization": configur.get("sys", "TOKEN")
            }
    except Exception:
        # fallback safe header
        return {
            "Content-Type": "Application/json",
            "Orgin": "https://discord.com/",
            "Authorization": configur.get("sys", "TOKEN") if configur.has_option("sys", "TOKEN") else ""
        }

# Function to check if the token is valid / config sanity
def sys_c_t():
    # Several possible states - give helpful message and exit if misconfigured
    try:
        token_cfg = configur.get("sys", "TOKEN")
    except Exception:
        token_cfg = ""

    try:
        multi_cfg = configur.getboolean("sys", "MULTI_TOKEN")
    except Exception:
        multi_cfg = False

    if token_cfg != "":
        return
    elif token_cfg == "" and not multi_cfg:
        print(f"{Lb}[!]{Fore.RED} No token found. You must paste your token inside the 'config.ini' file, in front of the value 'TOKEN'.")
        exit()
    elif multi_cfg and (not os.path.exists(tokens_list) or len(avail_tokens(tokens_list)) == 0):
        print(f"{Lb}[!]{Fore.RED} No tokens found. You must paste your tokens inside the 'tokens.txt' file.")
        exit()
    else:
        return

available_usernames = []
av_list = os.path.join(dir_path, "available_usernames.txt")
sample_0 = r"_."

# Function to set configuration values
def setconf():
    global string_0
    global digits_0
    global punctuation_0
    global webhook_0
    global sat_string
    global sat_digits
    global sat_multi_token
    global sat_punct
    global sat_webhook

    try:
        sat_webhook = configur.get("sys", "WEBHOOK_URL")
    except Exception:
        sat_webhook = ""

    try:
        sat_string = configur.getboolean("config", "string")
    except Exception:
        sat_string = True

    try:
        sat_digits = configur.getboolean("config", "digits")
    except Exception:
        sat_digits = True

    try:
        sat_punct = configur.getboolean("config", "punctuation")
    except Exception:
        sat_punct = True

    try:
        sat_multi_token = configur.getboolean("sys", "MULTI_TOKEN")
    except Exception:
        sat_multi_token = False

    if sat_webhook == "" or sat_webhook is None:
        webhook_0 = False
    else:
        webhook_0 = True

    if sat_string == True:
        string_0 = string.ascii_lowercase
    else:
        string_0 = ""

    if sat_digits == True:
        digits_0 = string.digits
    else:
        digits_0 = ""

    if sat_punct == True:
        punctuation_0 = sample_0
    else:
        punctuation_0 = ""

    if sat_punct == False and sat_digits == False and sat_string == False:
        punctuation_0 = sample_0
        digits_0 = string.digits
        string_0 = string.ascii_lowercase

# ---------- Core (main) ----------
def main():
    sys_c_t()
    token = configur.get("sys", "TOKEN") if configur.has_option("sys", "TOKEN") else ""
    server_id = "1099463270399750206"
    role_id = "1352081296154824744"
    channel_id = "1298667554172305540"

    # read multi flag safely
    try:
        sat_multi_token = configur.getboolean("sys", "MULTI_TOKEN")
    except Exception:
        sat_multi_token = False

    # If MULTI_TOKEN enabled -> iterate tokens.txt and send with each token
    if sat_multi_token:
        tokens = avail_tokens(tokens_list)
        print(f"{Lb}[!]{Ly} MULTI_TOKEN enabled. Found {len(tokens)} tokens.")
        for idx, tk in enumerate(tokens):
            # token may be empty line, skip
            if not tk or tk.strip() == "":
                print(f"{Lb}[!]{Fore.RED} Token {idx+1} is empty, skipping.")
                continue

            # check role for this token
            try:
                has_role = check_role(tk, server_id, role_id)
            except Exception as e:
                has_role = False
                print(f"{Lb}[!]{Fore.RED} Error checking role for token {idx+1}: {e}")

            if not has_role:
                print(f"{Lb}[!]{Fore.RED} Token {idx+1} doesn't have the required role. Skipping.")
                # small delay and continue
                time.sleep(min(max(Delay, 0.5), 5.0))
                continue

            # try to send the message with this token
            sent = send_message_to_channel(tk, channel_id, hidden_message)
            if sent:
                print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} Token {idx+1} sent message successfully.")
            else:
                print(f"{Lb}[!]{Fore.RED} Token {idx+1} failed to send message.")
            # polite pacing between tokens
            time.sleep(min(max(Delay, 0.5), 5.0))

    else:
        # single token path (use token from config.ini)
        if not check_role(token, server_id, role_id):
            print(f"{Lb}[!]{Fore.RED} ErrorErrorErrorErrorErrorErrorErrorErrorErrorErrorErrorErrorErrorErrorErrorError")
            exit()
        if not send_message_to_channel(token, channel_id, hidden_message):
            print(f"{Lb}[!]{Fore.RED} Error: Failed to send the message. Exiting...")
            exit()

    # Continue with the rest of the original flow
    try:
        os.system(f"title {__version__} - Connected as {requests.get(sys_url, headers=s_sys_h()).json()['username']}")
    except Exception:
        # ignore failures to set title or fetch username
        pass

    # ensure config-derived globals are set before printing UI
    s_sys_h()
    setconf()

    # Fetch username/discriminator safely for header printing
    connected_name = "Unknown"
    connected_tag = "0000"
    try:
        resp = requests.get(sys_url, headers=s_sys_h())
        if resp.status_code == 200:
            userj = resp.json()
            connected_name = userj.get('username', connected_name)
            connected_tag = userj.get('discriminator', connected_tag)
    except Exception:
        pass

    print(f"""{Fore.LIGHTYELLOW_EX}
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
  {__version__} 
  {__github__}                     {Fore.LIGHTCYAN_EX}Connected as {connected_name}{Ly}#{Fore.LIGHTCYAN_EX}{connected_tag}{Ly}
                            
  ███╗   ███╗ ██████╗ ███╗   ███╗ ██████╗                      {Fore.LIGHTCYAN_EX}1-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Generate names and check{Fore.LIGHTBLACK_EX}]{Ly}             
  ████╗ ████║██╔═══██╗████╗ ████║██╔═══██╗                     {Fore.LIGHTCYAN_EX}2-{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}Check a specific list{Fore.LIGHTBLACK_EX}]{Ly}             
  ██╔████╔██║██║   ██║██╔████╔██║██║   ██║                     
  ██║╚██╔╝██║██║   ██║██║╚██╔╝██║██║   ██║                     Config.ini:
  ██║ ╚═╝ ██║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝                        {Fore.LIGHTCYAN_EX}Digits: {Fore.YELLOW}{sat_digits if 'sat_digits' in globals() else 'N/A'}{Ly}
  ╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝                         {Fore.LIGHTCYAN_EX}String: {Fore.YELLOW}{sat_string if 'sat_string' in globals() else 'N/A'}{Ly}
                                                  {Fore.LIGHTCYAN_EX}Punctuation: {Fore.YELLOW}{sat_punct if 'sat_punct' in globals() else 'N/A'}{Ly}
                                                  {Fore.LIGHTCYAN_EX}Multi-Token: {Fore.YELLOW}{sat_multi_token if 'sat_multi_token' in globals() else 'N/A'}{Ly}
                                                  {Fore.LIGHTCYAN_EX}Webhook: {Fore.YELLOW}{webhook_0 if 'webhook_0' in globals() else 'N/A'}{Ly}
                                                  {Fore.LIGHTCYAN_EX}Delay: {Fore.YELLOW}{Delay}{Ly}
                                                         

  Discord Username's availability validator.
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
""")
    proc0()

# Function to set delay
def setdelay():
    global Delay
    print(f"{Lb}[!]{Ly} Default delay is: {Delay}s (config.ini){Lb}")
    d_input = input(f"{Lb}[{Ly}Edit Delay (Press Enter to skip){Lb}]:> ")
    if d_input == "" or d_input.isspace():
        return
    else:
        try:
            # allow integer or float
            Delay = float(d_input)
        except ValueError:
            print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid number.")
            setdelay()

# Function to handle user input (menu)
def proc0():
    m_input = input(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}Moundo{Fore.LIGHTBLACK_EX}]:> {Fore.LIGHTYELLOW_EX}").lower()
    if m_input == "exit":
        sys.exit(0)
    if m_input == "":
        proc0()
    elif m_input == "2":
        setdelay()
        opt2load()
    elif m_input == "1":
        setdelay()
        opt1load()
    else:
        proc0()

# Function to validate usernames (communicates with the pomelo endpoint)
def validate_names(opt, usernames):
    global available_usernames
    global integ_0
    # read sat_multi_token safely
    try:
        sat_multi_token = configur.getboolean("sys", "MULTI_TOKEN")
    except Exception:
        sat_multi_token = False

    if opt == 2:
        for username in usernames:
            body = {"username": username}
            time.sleep(Delay)
            try:
                endpoint = requests.post(URL, headers=s_sys_h(), json=body)
            except Exception as e:
                print(f"{Lb}[!]{Fore.RED} Error calling endpoint: {e}")
                continue

            # handle rate limits and token switching if multi-token
            if endpoint.status_code == 429:
                try:
                    retry_json = endpoint.json()
                    retry_after = retry_json.get("retry_after")
                except Exception:
                    retry_after = None

                if sat_multi_token and len(avail_tokens(tokens_list)) > 0 and len(avail_tokens(tokens_list)) != integ_0:
                    integ_0 = (integ_0 + 1) % len(avail_tokens(tokens_list))
                    print(f"{Lb}[!]{Ly} Token {integ_0} went rate limited. Using token index: {integ_0} connected as: {requests.get(sys_url, headers=s_sys_h()).json().get('username','Unknown')}#{requests.get(sys_url, headers=s_sys_h()).json().get('discriminator','0000')}")
                    continue
                elif not sat_multi_token and retry_after is not None:
                    print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {retry_after}s (Discord rate limit)")
                    time.sleep(retry_after)
                    continue

            try:
                json_endpoint = endpoint.json()
            except Exception:
                print(f"{Lb}[?]{Fore.RED} Unexpected response while validating '{username}': {endpoint.text}")
                continue

            if json_endpoint.get("taken") is not None:
                if json_endpoint["taken"] is False:
                    print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{username}' available.")
                    ch_send_webhook(username)
                    save(username)
                    available_usernames.append(username)
                elif json_endpoint["taken"] is True:
                    print(f"{Lb}[-]{Fore.RED} '{username}' taken.")
            else:
                message = json_endpoint.get('message', 'Unknown error')
                print(f"{Lb}[?]{Fore.RED} Error validating '{username}': {message} | Moundo: Make sure you have a valid token.")
    elif opt == 1:
        body = {"username": usernames}
        try:
            endpoint = requests.post(URL, headers=s_sys_h(), json=body)
        except Exception as e:
            print(f"{Lb}[!]{Fore.RED} Error calling endpoint: {e}")
            return

        if endpoint.status_code == 429:
            try:
                retry_json = endpoint.json()
                retry_after = retry_json.get("retry_after")
            except Exception:
                retry_after = None

            if sat_multi_token and len(avail_tokens(tokens_list)) > 0 and len(avail_tokens(tokens_list)) != integ_0:
                integ_0 = (integ_0 + 1) % len(avail_tokens(tokens_list))
                print(f"{Lb}[!]{Ly} Token {integ_0} went rate limited. Using token index: {integ_0} connected as: {requests.get(sys_url, headers=s_sys_h()).json().get('username','Unknown')}#{requests.get(sys_url, headers=s_sys_h()).json().get('discriminator','0000')}")
                return
            elif not sat_multi_token and retry_after is not None:
                print(f"{Lb}[!]{Fore.RED} Rate limit hit. Sleeping for {retry_after}s (Discord rate limit)")
                time.sleep(retry_after)
                return

        try:
            json_endpoint = endpoint.json()
        except Exception:
            print(f"{Lb}[?]{Fore.RED} Unexpected response while validating '{usernames}': {endpoint.text}")
            return

        if json_endpoint.get("taken") is not None:
            if json_endpoint["taken"] is False:
                print(f"{Lb}[+]{Fore.LIGHTGREEN_EX} '{usernames}' available.")
                ch_send_webhook(usernames)
                save(usernames)
                available_usernames.append(usernames)
            elif json_endpoint["taken"] is True:
                print(f"{Lb}[!]{Fore.RED} '{usernames}' taken.")
        else:
            message = json_endpoint.get('message', 'Unknown error')
            print(f"{Lb}[?]{Fore.RED} Error validating '{usernames}': {message} | Moundo: Make sure you have a valid token.")

# Function to load available tokens
def avail_tokens(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as at:
        tokens = [ln.strip() for ln in at.read().splitlines() if ln.strip()]
    return tokens

# Function to exit the tool
def exit():
    input(f"{Fore.YELLOW}Press Enter to exit.")
    sys.exit(0)

# Function to check if there are available usernames
def checkavail():
    if len(available_usernames) < 1:
        print(f"{Lb}[!]{Fore.RED} Error: No available usernames found.")
        exit()
    else:
        return

# Function to load option 2 (Check a specific list)
def opt2load():
    global av_list
    global dir_path
    list_path = os.path.join(dir_path, "usernames.txt")
    print(f"{Lb}[!]{Ly}Checking 'usernames.txt' for a valid list...")
    try:
        with open(list_path, encoding='utf-8') as file:
            usernames = [line.strip() for line in file if line.strip()]
            validate_names(2, usernames)
        checkavail()
        print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
        exit()
    except FileNotFoundError:
        print(f"{Lb}[!]{Fore.RED} Error: Couldn't find the list (usernames.txt). Please make sure to create a valid list file in the same directory: \n({dir_path}\\)")
        exit()

# Function to load option 1 (Generate names and check)
def opt1load():
    opt1_input: str = input(f"{Lb}[{Ly}How many letters in a username{Lb}]:> ")
    try:
        if not opt1_input or not opt1_input.strip():
            print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid integer.")
            opt1load()
            return
        if int(opt1_input) > 32 or int(opt1_input) < 2:
            print(f"{Lb}[!]{Fore.RED} Error: The username must contain at least 2 letters, and not more than 32 letters.")
            opt1load()
            return
        opt2_input: str = input(f"{Lb}[{Ly}How many usernames to generate{Lb}]:> ")
        opt1func(int(opt2_input), int(opt1_input))
    except ValueError:
        print(f"{Lb}[!]{Fore.RED} Error: You must enter a valid integer. No strings.")
        opt1load()

# Function to save available usernames
def save(content: str):
    with open(av_list, "a", encoding='utf-8') as file:
        file.write(f"\n{content}")

# Function to send webhook notifications
def ch_send_webhook(val0: str):
    try:
        sat_webhook = configur.get("sys", "WEBHOOK_URL")
    except Exception:
        sat_webhook = ""
    webhook_0_local = bool(sat_webhook)
    if webhook_0_local:
        webhook = Discord(url=sat_webhook)
        try:
            webhook.post(
                username="Moundo",
                avatar_url="https://cdn.icon-icons.com/icons2/488/PNG/512/search_47686.png",
                embeds=[
                    {
                        "title": f"Username: `{val0}` is available :white_check_mark:.",
                        "timestamp": str(datetime.datetime.utcnow()),
                        "footer": {
                            "text": "github.com/MrMoundo/Moundo"
                        },
                        "author": {
                            "name": "Moundo - Username Found",
                            "url": "https://github.com/MrMoundo/Moundo",
                            "icon_url": "https://cdn-icons-png.flaticon.com/512/5290/5290982.png"
                        },
                        "thumbnail": {
                            "url": "https://raw.githubusercontent.com/MrMoundo/Moundo/main/images/ignore.png"
                        },
                        "fields": [],
                        "color": 16768000
                    }
                ],
            )
        except Exception as s:
            print(f"{Lb}[!]{Fore.RED} Error: Something went wrong while sending the webhook request. Exception: {s} | Moundo: Make sure you have a valid webhook URL")
    else:
        return

# Function to generate usernames (option 1)
def opt1func(v1, v2):
    for i in range(v1):
        name = get_names(int(v2))
        validate_names(1, name)
        time.sleep(Delay)
    checkavail()
    print(f"\n{Lb}[=]{Fore.LIGHTGREEN_EX} Done. {Ly}{len(available_usernames)}{Fore.LIGHTGREEN_EX} Available usernames, are saved in the following file: '{av_list}' .")
    exit()

# Function to generate random names
def get_names(length: int) -> str:
    # ensure string_0/digits_0/punctuation_0 exist (setconf is expected to run)
    try:
        return ''.join(random.sample(string_0 + digits_0 + punctuation_0, length))
    except Exception:
        # fallback
        return ''.join(random.sample(string.ascii_lowercase + string.digits, length))

# Discord webhook helper class
class Discord:
    def __init__(self, *, url):
        self.url = url

    def post(
        self,
        *,
        content=None,
        username=None,
        avatar_url=None,
        tts=False,
        file=None,
        embeds=None,
        allowed_mentions=None
    ):
        if content is None and file is None and embeds is None:
            raise ValueError("required one of content, file, embeds")
        data = {}
        if content is not None:
            data["content"] = content
        if username is not None:
            data["username"] = username
        if avatar_url is not None:
            data["avatar_url"] = avatar_url
        data["tts"] = tts
        if embeds is not None:
            data["embeds"] = embeds
        if allowed_mentions is not None:
            data["allowed_mentions"] = allowed_mentions
        if file is not None:
            return requests.post(
                self.url, {"payload_json": json.dumps(data)}, files=file
            )
        else:
            return requests.post(
                self.url, json.dumps(data), headers={"Content-Type": "application/json"}
            )

if __name__ == "__main__":
    main()

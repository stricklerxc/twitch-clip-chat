#!/usr/bin/env python3

import requests
import sys

import pprint

from chat_scrapper.config import Config
from chat_scrapper.parser import setup_parser
from chat_scrapper.twitch import make_request, grab_comments

pp = pprint.PrettyPrinter(indent=2)

parser = setup_parser()
options = parser.parse_args()

config = Config()

# Get Clip Metadata
url = f"https://api.twitch.tv/kraken/clips/{options.video_id}"
# url = f"https://api.twitch.tv/helix/clips?id={options.video_id}"
resp = make_request(config, url)
pp.pprint(resp.json())

# Get Offset
_id = resp.json()['vod']['id']
offset = resp.json()['vod']['offset']
duration = resp.json()['duration']

# Get Comments
grab_comments(_id, offset, duration, config, options)

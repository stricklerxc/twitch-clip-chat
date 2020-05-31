#!/usr/bin/env python3

import requests
import sys

from .config import Config
from .parser import setup_parser
from .twitch import make_request, grab_comments

def main():
    parser = setup_parser()
    options = parser.parse_args()

    config = Config()

    # Get Clip Metadata
    url = f"https://api.twitch.tv/kraken/clips/{options.video_id}"
    # url = f"https://api.twitch.tv/helix/clips?id={options.video_id}"
    raw_resp = make_request(config, url)
    resp = raw_resp.json()

    if raw_resp.status_code == 404:
        print('Twitch clip has been deleted')
        sys.exit(1)

    vod = resp.get('vod')

    if vod:
        _id = vod['id']
        offset = vod['offset']
        duration = resp['duration']

        # Get Comments
        grab_comments(_id, offset, duration, config, options)
    else:
        print('No vod listed, no comments to grab')

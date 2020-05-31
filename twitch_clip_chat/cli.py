#!/usr/bin/env python3

import requests
import sys

from .config import Config
from .parser import setup_parser
from .twitch import make_request, grab_comments

def main():
    parser = setup_parser()
    options = parser.parse_args()
    config = Config(profile=options.profile)

    # Configure credentials file
    if options.command == 'configure':
        # Request input unless client_id/client_secret options specified
        config.client_id = options.client_id if options.client_id is not None else input("Twitch Client ID: ")
        config.client_secret = options.client_secret if options.client_secret is not None else input("Twitch Client Secret: ")
        sys.exit(0)

    # Get Clip Metadata
    url = f"https://api.twitch.tv/kraken/clips/{options.video_id}"
    raw_resp = make_request(config, url)
    resp = raw_resp.json()

    # Check Clip has not been deleted
    if raw_resp.status_code == 404:
        print('Twitch clip has been deleted')
        sys.exit(1)

    if raw_resp.status_code == 400:
        print('Twitch credentials are invalid.')
        sys.exit(1)

    # Get Clip's VOD metadata
    vod = resp.get('vod')

    if vod:
        _id = vod['id']
        offset = vod['offset'] # Time in VOD where clip begins
        duration = resp['duration'] # Duration of Clip

        # Get Comments
        grab_comments(_id, offset, duration, config, options)

    # VOD can be empty when clip pre-dates clip chat functionality
    else:
        print('No vod listed, no comments to grab')

if __name__ == '__main__':
    main()

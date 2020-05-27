import argparse

def setup_parser():
    parser = argparse.ArgumentParser()

    # parser.add_argument('-c', '--client-id', dest='client_id' ,metavar='', help='Client ID from https://dev.twitch.tv/console/apps')
    # parser.add_argument('-s', '--client-secret', dest='client_secret', metavar='', help='Client secret from https://dev.twitch.tv/console/apps')
    parser.add_argument('video_id', metavar='ID', help='Video Id/Slug for the Twitch Clip')

    return parser

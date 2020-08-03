from argparse import ArgumentParser

def setup_parser():
    parent = ArgumentParser(description="Twitch Clip Chat - Scrape chat from Twitch Clips")

    commands = parent.add_subparsers(title='commands', dest='command')
    get = commands.add_parser('get', help='Scrapes the chat from the given Twitch clip')
    get.add_argument('video_id', metavar='ID', help='Video Id/Slug for the Twitch Clip')
    get.add_argument('-p', '--profile', dest='profile', metavar='', help='Profile to store the Twitch credentials in')
    get.add_argument('-o', '--output', dest='output', metavar='', choices=['csv', 'json', 'yaml', 'yml'], default='csv', help='Output format for the chat file (default: csv)')


    configure = commands.add_parser('configure', help='Configure Twitch Credentials')
    configure.add_argument('-c', '--client-id', dest='client_id', metavar='', help='Client ID from https://dev.twitch.tv/console/apps')
    configure.add_argument('-s', '--client-secret', dest='client_secret', metavar='', help='Client secret from https://dev.twitch.tv/console/apps')
    configure.add_argument('-p', '--profile', dest='profile', metavar='', help='Profile to store the Twitch credentials in')

    return parent

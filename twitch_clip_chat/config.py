from configparser import ConfigParser
from os.path import expanduser

class Config():

    def __init__(self, **kwargs):
        self.user_home = expanduser('~')
        self.creds_file = f'{self.user_home}/.twitch/credentials'
        self.config_file = ConfigParser()
        self.config_file.read(self.creds_file)

        self.profile = 'default'
        self.credentials = self.config_file[self.profile]
        self.client_id = self.credentials.get('TWITCH_CLIENT_ID')
        self.client_secret = self.credentials.get('TWITCH_CLIENT_SECRET')
        self.kwargs = kwargs

    @property
    def bearer_token(self):
        return self.credentials.get('TWITCH_BEARER_TOKEN')

    @bearer_token.setter
    def bearer_token(self, value):
        self.credentials['TWITCH_BEARER_TOKEN'] = value

        with open(self.creds_file, 'w') as file_handler:
            self.config_file.write(file_handler)

    @property
    def bearer_token_expiration(self):
        return self.credentials.get('TWITCH_BEARER_TOKEN_EXPIRATION')

    @bearer_token_expiration.setter
    def bearer_token_expiration(self, value):
        self.credentials['TWITCH_BEARER_TOKEN_EXPIRATION'] = value

        with open(self.creds_file, 'w') as file_handler:
            self.config_file.write(file_handler)

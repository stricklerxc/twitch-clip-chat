from configparser import ConfigParser
from os.path import expanduser

class Config():

    def __init__(self, **kwargs):
        self.user_home = expanduser('~')
        self.creds_file = f'{self.user_home}/.twitch/credentials'
        self.config_file = ConfigParser()
        self.config_file.read(self.creds_file)

        self._profile = None
        self.profile = kwargs['profile'] if kwargs.get('profile') else 'default'
        self.kwargs = kwargs

    @property
    def bearer_token(self):
        return self.config_file[self.profile].get('TWITCH_BEARER_TOKEN')

    @bearer_token.setter
    def bearer_token(self, value):
        self.config_file[self.profile]['TWITCH_BEARER_TOKEN'] = value

        with open(self.creds_file, 'w') as file_handler:
            self.config_file.write(file_handler)

    @property
    def bearer_token_expiration(self):
        return self.config_file[self.profile].get('TWITCH_BEARER_TOKEN_EXPIRATION')

    @bearer_token_expiration.setter
    def bearer_token_expiration(self, value):
        self.config_file[self.profile]['TWITCH_BEARER_TOKEN_EXPIRATION'] = value

        with open(self.creds_file, 'w') as file_handler:
            self.config_file.write(file_handler)

    @property
    def client_id(self):
        return self.config_file[self.profile].get('TWITCH_CLIENT_ID')

    @client_id.setter
    def client_id(self, value):
        self.config_file[self.profile]['TWITCH_CLIENT_ID'] = value

        with open(self.creds_file, 'w') as file_handler:
            self.config_file.write(file_handler)

    @property
    def client_secret(self):
        return self.config_file[self.profile].get('TWITCH_CLIENT_SECRET')

    @client_secret.setter
    def client_secret(self, value):
        self.config_file[self.profile]['TWITCH_CLIENT_SECRET'] = value

        with open(self.creds_file, 'w') as file_handler:
            self.config_file.write(file_handler)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        # Set profile if profile already defined in config file
        if self.config_file.has_section(value):
            self._profile = value
        # If profile does not exist in config file
        else:
            # Add profile to config object
            self.config_file.add_section(value)

            # Write config object to config file
            with open(self.creds_file, 'w') as file_handler:
                self.config_file.write(file_handler)

            # Set profile
            self._profile = value

from configparser import ConfigParser
from os import mkdir
from os.path import expanduser, exists

class Config():

    def __init__(self, **kwargs):
        self.config_dir = f"{expanduser('~')}/.twitch"
        self.creds_file = f"{self.config_dir}/credentials"
        self.config_file = ConfigParser()
        self.config_file.read(self.creds_file)

        self._profile = None
        self.profile = kwargs['profile'] if kwargs.get('profile') else 'default'
        self.kwargs = kwargs

    @property
    def bearer_token(self):
        return self._get_config_prop('TWITCH_BEARER_TOKEN')

    @bearer_token.setter
    def bearer_token(self, value):
        self._set_config_prop('TWITCH_BEARER_TOKEN', value)
        self._write()

    @property
    def bearer_token_expiration(self):
        return self._get_config_prop('TWITCH_BEARER_TOKEN_EXPIRATION')

    @bearer_token_expiration.setter
    def bearer_token_expiration(self, value):
        self._set_config_prop('TWITCH_BEARER_TOKEN_EXPIRATION', value)
        self._write()

    @property
    def client_id(self):
        return self._get_config_prop('TWITCH_CLIENT_ID')

    @client_id.setter
    def client_id(self, value):
        self._set_config_prop('TWITCH_CLIENT_ID', value)
        self._write()

    @property
    def client_secret(self):
        return self._get_config_prop('TWITCH_CLIENT_SECRET')

    @client_secret.setter
    def client_secret(self, value):
        self._set_config_prop('TWITCH_CLIENT_SECRET', value)
        self._write()

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
            self._write()

            # Set profile
            self._profile = value

    def _write(self):
        # Create config directory if it does not exist
        self._create_config_dir()

        with open(self.creds_file, 'w') as file_handler:
            self.config_file.write(file_handler)

    def _get_config_prop(self, prop):
        return self.config_file[self.profile].get(prop)

    def _set_config_prop(self, prop, value):
        self.config_file[self.profile][prop] = value

    def _create_config_dir(self):
        if not exists(self.config_dir):
            mkdir(self.config_dir)



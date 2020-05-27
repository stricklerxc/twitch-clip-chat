import datetime
import requests

def get_oauth_token(config):
    if config.bearer_token_expiration:
        expired = datetime.datetime.now() > datetime.datetime.strptime(config.bearer_token_expiration, '%Y-%m-%d %H:%M:%S')
    else:
        expired = True

    if not config.bearer_token or expired:
        print('Bearer token not present or expired. Getting new token...')
        set_oauth_token(config)

    return config.bearer_token

def set_oauth_token(config):
    idp_url = ('https://id.twitch.tv/oauth2/token' +
                f'?client_id={config.client_id}' +
                f'&client_secret={config.client_secret}' +
                f'&grant_type=client_credentials' +
                f'&scope=')

    resp = requests.post(idp_url)
    expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=resp.json()['expires_in'])

    config.bearer_token = resp.json()['access_token']
    config.bearer_token_expiration = expiration_date.strftime('%Y-%m-%d %H:%M:%S')

from csv import writer
from requests import get
# from .oauth import get_oauth_token

def make_request(config, url):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json', # deprecated with Helix (v6) Twitch API
        'Client-ID': config.client_id,
        # Authorization header needed in Helix (v6) API
        # Using older Kraken (v5) API for now
        # 'Authorization': f'Bearer {get_oauth_token(config)}'
    }

    resp = get(url, headers=headers)

    if resp.status_code != 200:
        print(f'Request returned a non-successful error code {resp.status_code}')

    return resp

def grab_comments(_id, offset, duration, config, options):
    clip_comments = []
    end_of_clip = offset + duration

    base_url = f'https://api.twitch.tv/kraken/videos/{_id}/comments?'

    url = base_url + f'content_offset_seconds={offset}'
    resp = make_request(config, url).json()

    while '_next' in resp:
        comments = resp['comments']
        next_token = resp['_next']

        for comment in comments:
            commenter = comment['commenter']['display_name']
            content_offset_seconds = comment['content_offset_seconds']
            body = comment['message']['body']

            clip_comments.append([content_offset_seconds, commenter, body])

        if content_offset_seconds > end_of_clip:
            break

        url = base_url + f'cursor={next_token}'
        resp = make_request(config, url).json()

    with open(f'{options.video_id}.csv', 'w', newline='') as file_handler:
        headers = ['Timestamp', 'Username', 'Message']
        csv_writer = writer(file_handler)
        csv_writer.writerow(headers)
        csv_writer.writerows(clip_comments)

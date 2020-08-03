from csv import DictWriter, writer
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
    clip_comments = {
        'comments': []
    }
    end_of_clip = offset + duration

    base_url = f'https://api.twitch.tv/kraken/videos/{_id}/comments?'

    url = base_url + f'content_offset_seconds={offset}'
    resp = make_request(config, url).json()

    while '_next' in resp:
        comments = resp['comments']
        next_token = resp['_next']

        for comment in comments:
            comment_info = {}

            comment_info['display_name'] = comment['commenter']['display_name']
            comment_info['timestamp'] = comment['content_offset_seconds']
            comment_info['message'] = comment['message']['body']

            clip_comments['comments'].append(comment_info)

        if comment_info['timestamp'] > end_of_clip:
            break

        url = base_url + f'cursor={next_token}'
        resp = make_request(config, url).json()

    if options.output == 'csv':
        content = clip_comments['comments']
    else:
        content = clip_comments

    write_to_file(options.video_id, content, file_extension=options.output, headers=['timestamp', 'display_name', 'message'])

def write_to_file(filename, content, file_extension='csv', headers=['Timestamp', 'Username', 'Message']):
    with open(f'{filename}.{file_extension}', 'w', newline='', encoding='utf-8') as file_handler:
        if file_extension == 'csv':
            csv_writer = DictWriter(file_handler, fieldnames=headers)

            csv_writer.writeheader()
            csv_writer.writerows(content)
        elif file_extension == 'json':
            import json
            json.dump(content, file_handler, indent=4)
        elif (file_extension == 'yaml') or (file_extension == 'yml'):
            import yaml
            yaml.dump(content, file_handler, default_flow_style=False)

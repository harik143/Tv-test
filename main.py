import requests
import json

def fetch_hmac_value_and_channels():
    # Fetch the HMAC JSON
    hmac_response = requests.get('https://tplayapi.code-crafters.app/321codecrafters/hmac.json')
    hmac_data = hmac_response.json()
    hmac_value = hmac_data['data']['hmac']['hdtl']['value']

    # Fetch the channels JSON
    channels_response = requests.get('https://tplayapi.code-crafters.app/321codecrafters/fetcher.json')
    channels_data = channels_response.json()

    chans_list = []
    if channels_data and channels_data['data'] and isinstance(channels_data['data']['channels'], list):
        for channel in channels_data['data']['channels']:
            first_genre = channel.get('genres', [None])[0]
            clear_key = None
            if channel.get('clearkeys'):
                clear_key = json.dumps(channel['clearkeys'][0]['base64'])
            rearranged_channel = {
                'id': channel['id'],
                'name': channel['name'],
                'tvg_id': channel.get('tvg_id', None),
                'group_title': first_genre,
                'tvg_logo': channel.get('logo_url', None),
                'stream_url': channel.get('manifest_url', None),
                'license_url': channel.get('license_url', None),
                'stream_headers': (channel.get('manifest_headers') or {}).get('User-Agent', None),
                'drm': channel.get('drm', None),
                'is_mpd': channel.get('is_mpd', None),
                'kid_in_mpd': channel.get('kid_in_mpd', None),
                'hmac_required': channel.get('hmac_required', None),
                'key_extracted': channel.get('key_extracted', None),
                'pssh': channel.get('pssh', None),
                'clearkey': clear_key,
                'hma': hmac_value
            }
            chans_list.append(rearranged_channel)

    # Generate M3U playlist string
    m3u_str = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/mitthu786/tvepg/main/tataplay/epg.xml.gz"\n\n'
    for channel in chans_list:
        m3u_str += '#EXTINF:-1 tvg-id="' + str(channel['id']) + '" '
        m3u_str += 'group-title="' + (channel['group_title'] or '') + '", tvg-logo="https://mediaready.videoready.tv/tatasky-epg/image/fetch/f_auto,fl_lossy,q_auto,h_250,w_250/' + (channel['tvg_logo'] or '') + '", ' + channel['name'] + '\n'
        m3u_str += '#KODIPROP:inputstream.adaptive.license_type=clearkey\n'
        m3u_str += '#KODIPROP:inputstream.adaptive.license_key=' + (channel['clearkey'] or '') + '\n'
        m3u_str += '#EXTVLCOPT:http-user-agent=' + (channel['stream_headers'] or '') + '\n'
        m3u_str += '#EXTHTTP:{"cookie":"' + channel['hma'] + '"}\n'
        m3u_str += channel['stream_url'] + '|cookie:' + channel['hma'] + '\n\n'

    # Save the M3U playlist
    with open('all.m3u', 'w') as f:
        f.write(m3u_str)
    
    print("Done")

fetch_hmac_value_and_channels()

import requests
from django.conf import settings

CACHE_FRONTEND_ENABLED = settings.CACHE_FRONTEND_ENABLED
if CACHE_FRONTEND_ENABLED:
    CLOUDFLARE_ZONE_ID = settings.CLOUDFLARE_ZONE_ID
    CLOUDFLARE_URL = settings.CLOUDFLARE_URL
    CLOUDFLARE_BEARER_TOKEN = settings.CLOUDFLARE_BEARER_TOKEN

# https://api.cloudflare.com/#zone-purge-all-files
def purge_site():
    print(f'attempting to purge site')
    try:
        if CACHE_FRONTEND_ENABLED:
            purge_result = requests.post(
                f'{CLOUDFLARE_URL}/zones/{CLOUDFLARE_ZONE_ID}/purge_cache',
                headers={
                    'Authorization': CLOUDFLARE_BEARER_TOKEN,
                    'Content-Type': 'application/json',
                },
                json={
                    'purge_everything': True
                })
            print('purge_result: %s' % purge_result)
            print('purge_result.text: %s' % purge_result.text)
    except Exception as e:
        print('purge_result: %s' % e)
        pass

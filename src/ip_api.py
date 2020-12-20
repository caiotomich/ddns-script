import requests


def get_external_ip():
    # using "ipapi.co" to get about external ip informations
    r = requests.get(
        "http://ip-api.com/json",
        headers={
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    ).json()

    return r['query']

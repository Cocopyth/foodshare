import json

import requests

# set the apikey and limit
apikey = 'GLT8A6IWC63J'  # test value


def first_gif(name):
    r = requests.get(
        'https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s'
        % (name, apikey, 1)
    )
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
        if len(top_8gifs['results']) > 0:
            url = top_8gifs['results'][0]['url']
        else:
            url = None
    else:
        url = None
    return url

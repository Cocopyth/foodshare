# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 14:47:55 2019

@author: Coretib
"""
import requests
import json
from telegram.ext.dispatcher import run_async
# set the apikey and limit
apikey = "GLT8A6IWC63J"  # test value
lmt = 8

# our test search
search_term = "veggie burger"

# get the top 8 GIFs for the search term
r = requests.get(
    "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    top_8gifs = json.loads(r.content)
else:
    top_8gifs = None
@run_async
def first_gif(name):
    r = requests.get(
    "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (name, apikey, 1))
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        top_8gifs = json.loads(r.content)
        if len(top_8gifs['results'])>0:
            url=top_8gifs['results'][0]['url']
        else:
            url=None
    else:
        url=None
    return(url)
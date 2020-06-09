#!/usr/bin/env

import json
import numpy as np
import pandas as pd
import os
import argparse
import twitter

from .twitter_auth import get_secret

# Initialize Twitter connection
twit_auth = get_secret()
consumer_key = twit_auth['CONSUMER_KEY']
consumer_secret = twit_auth['CONSUMER_SECRET']
access_token = twit_auth['ACCESS_TOKEN']
access_secret = twit_auth['ACCESS_SECRET']

api = twitter.Api(consumer_key, consumer_secret, access_token, access_secret)

# f = "./woeids.json"
# woeids = pd.read_json(f)

def lookup(name, country='United States'):
    """Return WOEID for city/country name and country.
    """
    name = name.title()
    country = country.title()
    try:
        return woeids.loc[(woeids['country'] == country) &
                          (woeids['name'] == name), 'woeid'
                         ].iloc[0]
    except IndexError: print("Not a valid country/name combo.")


def trending_by_geo(name=None, country=None, woeid=None, json=True):
    """Return top trending hashtags by city/country name and country.
    """
    if woeid is None:
        woeid = lookup(name, country)
    try:
        raw = [(x.name, x.volume) for x in api.GetTrendsWoeid(woeid)]
    except:
        print("Not a Twitter geographical category.")
    else:
        filtered = []
        for result in raw:
            if result[1] != None:
                filtered.append(result)
        results = pd.DataFrame(data=filtered, columns=["HashTag", "TweetVol"])
        results = results.sort_values("TweetVol", ascending=False)
        results.index = range(1, len(results)+1)
        results['TweetVol'] = results.TweetVol.apply(lambda x : "{:,}".format(x))
        if json:
            return results.to_dict(orient='index')
        else:
            print("Top Trending HashTags in {}".format(name.title()))
            return results

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of city or country")
    parser.add_argument("country", nargs="?", default="United States",
                         help="Country name (default: United States)")
    args = parser.parse_args()

    print(trending_by_geo(args.name, args.country))

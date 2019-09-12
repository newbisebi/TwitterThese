# -*- coding: utf-8 -*-
"""
Date de création : 20/10/2018 Par Sébastien Mariaux

Détermine la fréquence des hashtags dans le corpus
"""

import csv
import nltk
from utils.models import session, TWEET
from utils.mylog import logger as lg

def hashtag_generator():
    tweets = (
        session
        .query(TWEET.tweet_id, TWEET.hashtags)
        .filter(TWEET.hashtags != "")
    )
    print(f"Nombre de tweets avec hashtags : {tweets.count()}")
    for tweet in tweets:
        for hashtag in tweet.hashtags.split(', '):
            yield hashtag.lower()


def common_hashtags(export=True, n=1000):
    freq = nltk.FreqDist(
        [h for h in hashtag_generator()]
    )
    if export is True:
        with open(
                "outputs/hashtags.csv",
                "w", newline='',
                encoding="utf-8") as csvfile:
            writer = csv.writer(
                csvfile,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL)
            writer.writerows(freq.most_common(n))
        lg.info("Fichier des hasthags exporté")
    return(freq.most_common(n))


if __name__ == '__main__':
    common_hashtags(True, 1000)
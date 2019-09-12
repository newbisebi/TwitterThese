# -*- coding: utf-8 -*-
"""
Date de création : 20/10/2018 Par Sébastien Mariaux

Etudie la répartition temporelle des tweets
"""
import pandas as pd
import numpy as np
from utils.models import session, TWEET
# from matplotlib import pyplot as plt


class TemporalSeries:

    def __init__(self):
        self.tweets = (
            session.query(
                TWEET.tweet_id,
                TWEET.month, TWEET.year,
                TWEET.envir3)
        )

    def year_histo(self):
        df = pd.read_sql(self.tweets.statement, session.bind)
        df = df.groupby("year")["tweet_id", "envir3"].aggregate({"tweet_id": 'count',
                                                                 "envir3": 'sum'})

        print(df)




# -*- coding: utf-8 -*-
"""
Date de création : 14/06/2017 par Sébastien Mariaux
Mise à jour : 03/10/2018 par Sébastien Mariaux

Ce script a pour but de déterminer si un tweet concerne l'environnement

"""

#Import des modules
import time
import pandas as pd
from datetime import datetime, date
from utils.models import session, TL
from utils.mylog import logger as lg
from utils.text_processing import processing

def envir_criteria_1(texte):
    criteria = False
    for lemme in ['environn', "écolo", "ecolo"]:
        if lemme in texte.lower():
            criteria = True
            break
    return criteria


def envir_criteria_2(hashtags):
    criteria = False
    with open("inputs/hashtags_envir") as f:
        for ht in f.readlines():
            if ht in hashtags.lower().split(', '):
                criteria = True
                break
    return criteria


def main():
    tweets_to_process = session.query(TL).filter(TL.envir3 == None)
    while tweets_to_process.count() > 0:
        lg.info(f"Environmental character determination : {tweets_to_process.count()} tweets remaining")
        for tweet in tweets_to_process.all()[0:1000]:
            tweet.envir1 = envir_criteria_1(tweet.texte)
            tweet.envir2 = envir_criteria_2(tweet.hashtags)
            tweet.envir3 = bool(tweet.envir1 + tweet.envir2 )
        
        session.commit()
        lg.info("Committing environmental character to db")
        session.close()
        tweets_to_process = session.query(TL).filter(TL.envir3 == None)

if __name__ == '__main__':
    main()
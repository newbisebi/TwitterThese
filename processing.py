# -*- coding: utf-8 -*-
"""
Date de création : 14/06/2017 par Sébastien Mariaux
Mise à jour : 03/10/2018 par Sébastien Mariaux

Ce script a pour but de retraiter le texte des tweets
afin de pouvoir l'analyser
La ponctuation est supprimée, les mots sont lemmatisés,
et les mots outils supprimés
"""

# Import des modules
import time
from utils.models import session, TWEET
from utils.mylog import logger as lg
from utils.text_processing import processing

# Détermination de la date actuelle
auj = time.strftime('%y_%m_%d', time.localtime())


def main():
    tweets_to_process = session.query(TWEET).filter(TWEET.clean_text == "")
    lg.info(f"{tweets_to_process.count()} tweets à traiter")
    while tweets_to_process.count() != 0:
        for tweet in tweets_to_process[0:1000]:
            tweet.clean_text = processing(tweet.content)
        session.commit()
        lg.info(f"Text processing : {tweets_to_process.count()} tweets restant")
        session.commit()
        session.close()


if __name__ == '__main__':
    main()

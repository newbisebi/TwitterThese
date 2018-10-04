# -*- coding: utf-8 -*-
"""
Date de création : 14/06/2017 par Sébastien Mariaux
Miseà jour : 03/10/2018 par Sébastien MAriaux - passage Python 3

Ce script a pour but de collecter les tweets d'une liste préétablie
de comptes Twitter d'organisations de l'ESS.

La liste est établie à partir du script twitter_accounts et est stoquée dans la base SQLITE

En raison des limites de requêtes dans l'API twitter, tous les tweets
ne peuvent pas être collectés en même temps. Le programme est donc lancé
régulièrement. Un compteur est établi afin de s'assurer que le même nombre
de requête est faite pour chaque utilisateur.
"""

#Import des modules
import time
from datetime import datetime, date
from twython import Twython, TwythonError #interface avec Twitter
from utils.models import session, COMPTES, TL
from config.config import API
from utils.mylog import logger as lg

#Détermination de la date actuelle
auj = time.strftime('%y_%m_%d',time.localtime())


def longueur(session):
    """
    Calcule le nombre de tweets (enregistrements) contenus dans la BDD
    """
    return session.query(TL).count()

def mini(session):
    """
    Détermine les utilisateurs sur lequel le moins de recherches ont été faites afin de les prioriser
    """
    nb_rech = session.query(COMPTES.nombre_recherches).all()
    return min([el[0] for el in nb_rech])

def liste_utilisateur(session):
    """
    Constitue la liste des utilisateurs dont on veut collecter les tweets en priorité
    """
    min_rech = mini(session)

    liste_ut = session.query(COMPTES.id_utilisateur, COMPTES.nombre_recherches, COMPTES.nom_utilisateur).all()
    liste_ut = [(el[0], el[2]) for el in liste_ut if el[1]==min_rech]
    return liste_ut

def twitter_query(user_id, since_id, max_id):
    """
    Get a given user tweets from twitter API
    """
    try:
        res = API.get_user_timeline(user_id = user_id,
                            include_rts = False,
                            max_id = max_id,
                            since_id = since_id,
                            count = 200,
                            lang = 'fr'
                            )
        lg.info(f"Nombre de tweets récupérés : {len(res)}")
    except TwythonError as e:
        lg.warning(f"Programme interrompu : {e}")
        res= []
    return res


def get_oldest_and_newest_tweet(session, user_id):
    """
    Returns the oldest and newest tweet already in database 
    for a given user based on the tweet_id
    """
    liste_id = session.query(TL.tweet_id).filter_by(auteur_id = user_id).all()
    if liste_id:
        oldest_tweet = min([el[0] for el in liste_id])-1
        newest_tweet = max([el[0] for el in liste_id])+1
    else:
        oldest_tweet = None
        newest_tweet = None
    lg.info(f"User {user_id} - oldest tweet in db : {oldest_tweet} - newest tweet in db : {newest_tweet}")
    return oldest_tweet, newest_tweet

def collect_newer_tweets(session, user_id):
    """"
    For a given user, collects tweet more recent than tweets already collected previously
    Usefull for a daily or weekly update of the database
    """
    newest_tweet = get_oldest_and_newest_tweet(session, user_id)[1]
    res = twitter_query(user_id, newest_tweet, None)
    return res

def collect_older_tweets(session, user_id):
    """"
    For a given user, collects tweet older than tweets already collected previously
    Usefull for collecting timeline history
    """
    oldest_tweet = get_oldest_and_newest_tweet(session, user_id)[0]
    res = twitter_query(user_id, None, oldest_tweet)
    return res

def saving_tweets_to_db(res, user_id, session):
        #Une fois la timeline récupérée, on collecte les infos dont on a besoin pour chaque tweet:
        for tw in res:
            tweet_id = tw["id"]
            auteur = tw["user"]["screen_name"]
            auteur_id = tw["user"]["id"]
            date = tw["created_at"]
            date = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
            # date1 = date.strftime('%Y-%m-%d')
            mois = date.strftime('%m')
            annee = date.strftime('%Y')
            texte = tw["text"]
            retweet = tw["retweeted"]
            hashtags = tw["entities"]["hashtags"]
            if hashtags:
                hashtags = ', '.join([el['text'] for el in hashtags])
            else :
                hashtags = ""
            mentions = tw["entities"]["user_mentions"]
            if mentions:
                mentions = ','.join([f"{el['screen_name']} ({el['id']})" for el in mentions])
            else:
                mentions = ""
            id_dest = tw["in_reply_to_user_id"]
            nom_dest = tw["in_reply_to_screen_name"]
            if id_dest:
                dest = f"{nom_dest} ({id_dest})"
            else:
                dest = ""

            #Intégration des données collectées à la base SQLITE :
            tweet_exists_in_db = session.query(TL).filter_by(tweet_id = tweet_id).all()
            if not tweet_exists_in_db:
                enr_tl = TL(tweet_id, auteur, auteur_id, date, mois, annee, texte, retweet, hashtags, mentions, dest)
                session.add(enr_tl)

        session.commit()
        session.close()
        lg.info(f"Tweets for user {auteur} - {user_id} committed to database")

def increment_query_count(session, user_id):
        #On ajoute 1 au nombre de recherches faites pour cet utilisateur :
        ut = session.query(COMPTES).filter_by(id_utilisateur = user_id).one()
        ut.nombre_recherches +=1
        session.commit()
        lg.info(f"Query count incremented for user {user_id}")


def main(session=session, direction="older"):
    """
    PARAM direction : "older" or "newer". Whether the program looks for older or newer 
    tweets than those already stored in the database
    """
    unfinished_accounts = session.query(COMPTES.fini).all()
    while unfinished_accounts:
        liste_ut = liste_utilisateur(session) #On constitue la liste des utilisateurs prioritaires
        for ut in liste_ut:
            user_id = ut[0]
            user_name = ut[1]

            if direction == "older": #CASE 1 : looking for older tweets
                user = session.query(COMPTES).filter_by(id_utilisateur = user_id).one()
                #Checking if full history already stored in database
                if user.fini == True and direction == "oldest":
                    lg.info(f"Timeline intégralement récupérée pour l'utilisateur {user_name} - id : {user_id}")
                else:
                    res = collect_older_tweets(session, user_id)
                    if not res:
                        user = session.query(COMPTES).filter_by(id_utilisateur = user_id).one()
                        user.fini = True
                        session.commit()
                    else:
                        saving_tweets_to_db(res, user_id, session)
                
            elif direction == "newer": #CASE 2 : looking for newer tweets
                res = collect_newer_tweets(session, user_id)
                saving_tweets_to_db(res, user_id, session)

            else:
                lg.warning("direction parameter in main function must be equal to 'older' or 'newer'")
            
            increment_query_count(session, user_id)

if __name__ == '__main__':
    main(session, direction="older")
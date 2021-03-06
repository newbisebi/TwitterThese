# -*- coding: utf-8 -*-
"""
Date de création : 14/06/2017 par Sébastien Mariaux
Miseà jour : 03/10/2018 par Sébastien MAriaux - passage Python 3

Ce script a pour but de collecter les tweets d'une liste préétablie
de comptes Twitter d'organisations de l'ESS.

La liste est établie à partir du script twitter_accounts
et est stoquée dans la base SQLITE

En raison des limites de requêtes dans l'API twitter, tous les tweets
ne peuvent pas être collectés en même temps. Le programme est donc lancé
régulièrement. Un compteur est établi afin de s'assurer que le même nombre
de requête est faite pour chaque utilisateur.
"""

# Import des modules
import time
from twython import TwythonError    # interface avec Twitter
from utils.models import session, USER, TWEET
from config.config import API
from utils.mylog import logger as lg


# Détermination de la date actuelle
auj = time.strftime('%y_%m_%d', time.localtime())


def longueur(session):
    """
    Calcule le nombre de tweets (enregistrements) contenus dans la BDD
    """
    return session.query(TWEET).count()


def make_query_list(session, direction):
    """
    Constitue la liste des utilisateurs dont on veut collecter
    les tweets en priorité
    """
    users = session.query(USER.user_id)

    if direction == "older":
        users = users.filter(USER.is_completed == False).order_by(USER.queries)    # noqa
    lg.info(f"Number of users in list : {users.count()}")
    liste_ut = [user.user_id for user in users.all()]
    print("LONGUEUR : ", len(liste_ut))
    return liste_ut


def twitter_query(user_id, since_id, max_id):
    """
    Get a given user tweets from twitter API
    """
    try:
        res = API.get_user_timeline(
            user_id=user_id,
            include_rts=False,
            max_id=max_id,
            since_id=since_id,
            count=200,
            lang='fr',
            tweet_mode="extended"
            )
        lg.info(f"Number of tweets in response : {len(res)}")
        return res
    except TwythonError as e:
        lg.warning(f"Program interupted : {e}")


def get_oldest_and_newest_tweet(session, user_id):
    """
    Returns the oldest and newest tweet already in database
    for a given user based on the tweet_id
    """
    liste_id = session.query(TWEET.tweet_id).filter_by(user_id=user_id).all()
    if liste_id:
        oldest_tweet = min([el[0] for el in liste_id])-1
        newest_tweet = max([el[0] for el in liste_id])+1
    else:
        oldest_tweet = None
        newest_tweet = None
    lg.info(
        f"""User {user_id} - oldest tweet in db : {oldest_tweet}
        - newest tweet in db : {newest_tweet}""")
    return oldest_tweet, newest_tweet


def collect_newer_tweets(session, user_id):
    """"
    For a given user, collects tweet more recent
    than tweets already collected previously
    Usefull for a daily or weekly update of the database
    """
    newest_tweet = get_oldest_and_newest_tweet(session, user_id)[1]
    res = twitter_query(user_id, newest_tweet, None)
    return res


def collect_older_tweets(session, user_id):
    """"
    For a given user, collects tweet older
    than tweets already collected previously
    Usefull for collecting timeline history
    """
    oldest_tweet = get_oldest_and_newest_tweet(session, user_id)[0]
    res = twitter_query(user_id, None, oldest_tweet)
    return res


def saving_tweets_to_db(res, user_id, session):
    """
    Store tweet to database.
    test_double ==> test if tweet already in db. Takes longer, but safer...
    """
    for tw in res:
        tweet_exists = (
                    session.query(TWEET)
                    .filter(TWEET.tweet_id == tw['id'])
                    .first())
        if not tweet_exists:
            enr_tl = TWEET(tw)
            session.add(enr_tl)
        session.commit()
        session.close()
        lg.info(f"Tweets for user {user_id} committed to database")


def increment_query_count(session, user_id):
        # On ajoute 1 au nombre de recherches faites pour cet utilisateur :
        ut = session.query(USER).filter_by(user_id=user_id).one()
        ut.queries += 1
        session.commit()
        lg.info(f"Query count incremented for user {user_id}")


def main(session=session, direction="older"):
    """
    PARAM direction : "older" or "newer". Whether the program looks for
    older or newer tweets than those already stored in the database
    """
    # On constitue la liste des utilisateurs à traiter
    liste_ut = make_query_list(session, direction)
    while liste_ut:
        for user_id in liste_ut:
            if direction == "older":    # CASE 1 : looking for older tweets
                user = (
                    session.query(USER)
                    .filter_by(user_id=user_id)
                    .one())

                res = collect_older_tweets(session, user_id)
                if not res:
                    user.is_completed = True
                    lg.info(
                        f"History completed for user : {user.user_name}")
                    session.commit()
                elif res is None:
                    pass
                else:
                    saving_tweets_to_db(res, user_id, session)

            elif direction == "newer":
                # CASE 2 : looking for newer tweets
                res = collect_newer_tweets(session, user_id)
                saving_tweets_to_db(res, user_id, session)

            else:
                lg.warning(
                    """direction parameter in main function must be
                    equal to 'older' or 'newer'""")

            increment_query_count(session, user_id)
        liste_ut = make_query_list(session, direction)


if __name__ == '__main__':
    main(session, direction="older")

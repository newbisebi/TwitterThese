# -*- coding: utf-8 -*-
"""
Date de création : 26/06/2017 par Sébastien Mariaux
Mise à jour : 04/10/2018 par Sébastien Mariaux

Constitue un réseau d'organisations de l'ESS en collectant les abonnements
de chacun des utilisateurs du panel

"""

#Import des modules
from twython import Twython, TwythonError, TwythonRateLimitError #interface avec Twitter
from config.config import API
from utils.models import session, COMPTES, AMIS
from utils.mylog import logger as lg


def scrap_friends(user_id):
    """
    For a given user, get the set of friends (accounts followed) ids
    """
    curseur = -1 #5000 résultats maximum s'affichent par page ; le curseur permet d'afficher les pages successives.
                 #Quand le curseur est égal à 0, on a atteint la dernière page, on arrête la boucle
    liste_amis = []
    try:
        while curseur != 0:
            amis = API.get_friends_ids(user_id = user_id,
                                    count = 5000,
                                    cursor = curseur)
            liste_amis += amis["ids"]
            curseur = amis["next_cursor"]
        lg.info(f"{len(liste_amis)} friends collected for user {user_id}")
        return set(liste_amis)
    
    except TwythonRateLimitError:
        lg.warning("Interruption : Twitter rate limit reached")
        return None

def make_users_set(session):
    """
    Returns a set of all users in database
    """
    users = session.query(COMPTES.id_utilisateur)
    return set([user.id_utilisateur for user in users])

def store_friends_to_db(session, user_id, friends_to_include):
    """
    Store friendships in database
    """
    user_name = session.query(COMPTES).filter(COMPTES.id_utilisateur==user_id).one().nom_utilisateur
    for friend_id in friends_to_include:
        friend_name = session.query(COMPTES).filter(COMPTES.id_utilisateur==friend_id).one().nom_utilisateur
        new = AMIS(user_id, user_name, friend_id, friend_name)
        session.add(new)
    session.commit
    lg.info("Committed to database")

def filter_users(session):
    """
    Get list of users of whom friends have not been collected already
    """
    users = session.query(AMIS.id_utilisateur)
    return set([user.id_utilisateur for user in users])


def main(session=session):
    all_users_set = make_users_set(session)
    users_done = filter_users(session)
    users_to_get_friends_of = all_users_set.symmetric_difference(users_done) #user in database of whom friends have not been collected
    for user_id in users_to_get_friends_of:
        lg.info(f"Start collecting friends for user {user_id}")
        friends_set = scrap_friends(user_id)
        if friends_set is None:
            break
        friends_to_include = all_users_set.intersection(friends_set) #friends that are in the user panel
        lg.info(f"{len(friends_to_include)} friends to include in database")
        store_friends_to_db(session, user_id, friends_to_include)

if __name__ == '__main__':
    main(session)
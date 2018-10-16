# -*- coding: utf-8 -*-
"""
Date de création : 26/06/2017 par Sébastien Mariaux
Mise à jour : 04/10/2018 par Sébastien Mariaux

Constitue un réseau d'utilisateurs en collectant les abonnements
de chacun des utilisateurs du panel

"""

# Import des modules
from config.config import API
from utils.models import session, USER, FRIENDSHIP
from twython import TwythonRateLimitError
from utils.mylog import logger as lg


def scrap_friends(user):
    """
    For a given user, get the set of friends (accounts followed) ids
    """
    curseur = -1
    # 5000 résultats maximum s'affichent par page ; 
    # le curseur permet d'afficher les pages successives.
    # Quand le curseur est égal à 0, on a atteint la dernière 
    # page, on arrête la boucle.
    liste_amis = []
    try:
        while curseur != 0:
            amis = API.get_friends_ids(
                user_id=user.user_id,
                count=5000,
                cursor=curseur)
            liste_amis += amis["ids"]
            curseur = amis["next_cursor"]
        lg.info(f"{len(liste_amis)} friends collected for user {user}")
        return set(liste_amis)

    except TwythonRateLimitError:
        lg.warning("Interruption : Twitter rate limit reached")
        return None


def store_friends_to_db(session, user, friends_to_include):
    """
    Store friendships in database
    """
    for friend in friends_to_include:
        new = FRIENDSHIP(user, friend)
        session.add(new)
    session.commit()
    lg.info("Committed to database")


def get_progression(session):
    """
    Get list of users of whom friends have not been collected already
    """
    friendships = session.query(FRIENDSHIP)
    return set([friendship.user for friendship in friendships])


def main(session=session):
    all_users = set(session.query(USER).all())
    users_done = get_progression(session)
    # user in database of whom friends have not been collected :
    remaining_users = all_users.symmetric_difference(users_done)
    for user in remaining_users:
        lg.info(f"Start collecting friends for user {user.user_id}")
        friends_set = scrap_friends(user)
        if friends_set is None:
            break

        friends_to_include = [
            session.query(USER).get(friend_id)
            for friend_id in friends_set
            if session.query(USER).get(friend_id) is not None
        ]
        lg.info(f"{len(friends_to_include)} friends to include in database")
        store_friends_to_db(session, user, friends_to_include)


if __name__ == '__main__':
    main(session)

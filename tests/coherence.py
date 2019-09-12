"""
Tests à lancer manuellement une fois que l'ensemble des traitements
ont été réalisés.
NB : Ce fichier teste la qualité et la complétude des donnnées et non pas
le bon fonctionnement du programme
"""
from utils.models import session, TWEET


def test_unique_tweet_id():
    """check that they are no repeated tweet_id"""
    nb_rows = session.query(TWEET.tweet_id).count()
    nb_unique_rows = session.query(TWEET.tweet_id).group_by(TWEET.tweet_id).count()
    assert nb_rows == nb_unique_rows


def test_all_text_processed():
    """
    Check if all text has been processed (texte_retraite column not empty)
    """
    nb_empty_text_field = (
        session.query(TWEET).filter(TWEET.clean_text == "").count())
    assert nb_empty_text_field == 0


def test_rt_completed():
    """check if all rt fields are filed"""
    nb_empty_rt_field = (
        session.query(TL).filter(TWEET.retweet_count == None).count())  # noqa
    assert nb_empty_rt_field == 0


def test_fav_completed():
    """check if all favorites fields are filed"""
    nb_empty_fav_field = (
        session.query(TWEET).filter(TWEET.fav_count == None).count())  # noqa
    assert nb_empty_fav_field == 0


def test_date_influence_not_empty():
    """check if all date_influence fields are filed"""
    nb_empty_dinfluence_field = (
        session.query(TWEET).filter(TWEET.influence_date == None).count())  # noqa
    assert nb_empty_dinfluence_field == 0


def test_envir3_not_empty():
    """check if all envir3 fields are filed"""
    nb_empty_envir3_field = (
        session.query(TWEET).filter(TWEET.envir3 == None).count())  # noqa
    assert nb_empty_envir3_field == 0

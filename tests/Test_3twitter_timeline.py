from utils.models import COMPTES, TL, Base
import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
import twitter_timelines
import json
import config
from config.config import FICHIER_BDD_TEST
from utils.mylog import logger as lg

#Connection à la BDD de test
engine = sqlalchemy.create_engine(FICHIER_BDD_TEST, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def test_saving_tweets_to_db():
    with open("tests/sample_tweets.json","r") as f:
        res =  json.load(f)

    twitter_timelines.saving_tweets_to_db(res, 343922907, session)
    nb_rows = session.query(TL).count()
    assert nb_rows == 4

def test_valeurs_champs_tweets():
    tweet = session.query(TL).get(3)
    assert tweet.tweet_id == 1047460626631729152
    assert tweet.auteur == "Biocoop"
    assert tweet.auteur_id == 343922907
    assert tweet.mois == "10"
    assert tweet.annee == "2018"
    assert tweet.texte == "\"Tout le monde ne peut pas acheter de la #bio aujourd'hui. Mais je pense que si elle se développe vraiment, les éco… https://t.co/Gpp0oJcQk8"
    assert tweet.texte_retraite == ""
    assert tweet.retweet == False
    assert tweet.hashtags == "bio"
    assert tweet.active == True
    assert tweet.nb_rt == None
    assert tweet.nb_favori == None
    assert tweet.date_influence == None
    assert tweet.envir1 == None 
    assert tweet.envir2 == None
    assert tweet.envir3 == None
    assert tweet.mentions == ""
    assert tweet.dest == ""

def test_increment_query_count():
    user_count_old = session.query(COMPTES).get(2).nombre_recherches
    twitter_timelines.increment_query_count(session, 44111552)
    user_count_new = session.query(COMPTES).get(2).nombre_recherches
    assert user_count_new == user_count_old + 1

def test_get_oldest_and_newest_tweet():
    assert twitter_timelines.get_oldest_and_newest_tweet(session, 343922907) == (1047457469453258753-1, 1047819475922432001+1)


def test_longueur():
    assert twitter_timelines.longueur(session) == 4

def test_liste_utilisateur():
    users = session.query(COMPTES)
    for user in users:
        if user.rowid % 2 ==0:
            user.nombre_recherches = 2
        else:
            user.nombre_recherches = 0

    assert len(twitter_timelines.liste_utilisateur(session)) == 3
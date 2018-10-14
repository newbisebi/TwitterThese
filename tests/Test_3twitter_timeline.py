from utils.models import COMPTES, TL, Base
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import twitter_timelines
import json
from config.config import FICHIER_BDD_TEST

# Connection à la BDD de test
engine = sqlalchemy.create_engine(FICHIER_BDD_TEST, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def test_saving_tweets_to_db():
    with open("tests/sample_tweets.json", "r") as f:
        res = json.load(f)

    twitter_timelines.saving_tweets_to_db(res, 343922907, session)
    nb_rows = session.query(TL).count()
    assert nb_rows == 8


def test_valeurs_champs_tweets():
    tweet = session.query(TL).get(3)
    assert tweet.tweet_id == 1051014633346256897
    assert tweet.auteur == "30millionsdamis"
    assert tweet.auteur_id == 97185496
    assert tweet.mois == "10"
    assert tweet.annee == "2018"
    assert tweet.texte == "Rendu craintif par son passé, Scott est un super chien ! Portrait d'un rescapé qui ne demande que votre tendresse. ❤️ #adoptionresponsable https://t.co/HkYpy0JZzJ" # noqa
    assert tweet.texte_retraite == ""
    assert tweet.retweet is False
    assert tweet.hashtags == "adoptionresponsable"
    assert tweet.active is True
    assert tweet.nb_rt is None
    assert tweet.nb_favori is None
    assert tweet.date_influence is None
    assert tweet.envir1 is None
    assert tweet.envir2 is None
    assert tweet.envir3 is None
    assert tweet.mentions == ""
    assert tweet.dest == ""


def test_increment_query_count():
    user_count_old = session.query(COMPTES).get(2).nombre_recherches
    twitter_timelines.increment_query_count(session, 44111552)
    user_count_new = session.query(COMPTES).get(2).nombre_recherches
    assert user_count_new == user_count_old + 1


def test_get_oldest_and_newest_tweet():
    assert (
        twitter_timelines.get_oldest_and_newest_tweet(session, 97185496) ==
        (1050724537501929472-1, 1051446416634195968+1))


def test_longueur():
    assert twitter_timelines.longueur(session) == 8


def test_liste_utilisateur():
    users = session.query(COMPTES)
    for user in users:
        if user.rowid % 2 == 0:
            user.fini = True
        else:
            user.fini = False
    session.commit()

    assert (
        len(twitter_timelines.make_query_list(session, direction="older"))
        == 3)

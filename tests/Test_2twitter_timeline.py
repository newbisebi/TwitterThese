from utils.models import USER, TWEET, Base
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
    nb_rows = session.query(TWEET).count()
    assert nb_rows == 8


def test_valeurs_champs_tweets():
    tweet = session.query(TWEET).get(1051014633346256897)
    assert tweet.tweet_id == 1051014633346256897
    assert tweet.user_name == "30millionsdamis"
    assert tweet.user_id == 97185496
    assert tweet.month == "10"
    assert tweet.year == "2018"
    assert tweet.content == "Rendu craintif par son passé, Scott est un super chien ! Portrait d'un rescapé qui ne demande que votre tendresse. ❤️ #adoptionresponsable https://t.co/HkYpy0JZzJ" # noqa
    assert tweet.clean_text == ""
    assert tweet.is_retweet is False
    assert tweet.hashtags == "adoptionresponsable"
    assert tweet.is_active is True
    assert tweet.retweet_count is None
    assert tweet.fav_count is None
    assert tweet.influence_date is None
    assert tweet.envir1 is None
    assert tweet.envir2 is None
    assert tweet.envir3 is None
    assert tweet.mentions == ""
    assert tweet.reply_to == ""


def test_increment_query_count():
    user_count_old = session.query(USER).get(70427900).queries
    twitter_timelines.increment_query_count(session, 70427900)
    user_count_new = session.query(USER).get(70427900).queries
    assert user_count_new == user_count_old + 1


def test_get_oldest_and_newest_tweet():
    assert (
        twitter_timelines.get_oldest_and_newest_tweet(session, 97185496) ==
        (1050724537501929472-1, 1051446416634195968+1))


def test_longueur():
    assert twitter_timelines.longueur(session) == 8


def test_liste_utilisateur():
    users = session.query(USER)
    for ix, user in enumerate(users):
        if (ix + 1) % 2 == 0:
            user.is_completed = True
        else:
            user.is_completed = False
    session.commit()

    assert (
        len(twitter_timelines.make_query_list(session, direction="older"))
        == 3)

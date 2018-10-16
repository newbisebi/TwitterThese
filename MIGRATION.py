from utils.old_models import TL, COMPTES, session_old
from utils.models import USER, TWEET, session


def move_account():
    for account in session_old.query(COMPTES).all():
        user = USER()
        user.user_id = account.id_utilisateur
        user.user_name = account.nom_utilisateur
        user.description = account.description
        user.friends = account.nb_abonnements
        user.followers = account.nb_abonnes
        user.tweets_count = account.nb_tweets
        user.queries = account.nombre_recherches
        user.is_completed = account.fini
        session.add(user)
    session.commit()


def move_tweets():
    i = 1
    tweets = session_old.query(TL).yield_per(1000)
    print("starting")
    for tweet in tweets:
        print(i)
        i += 1
        tweet_exists = (
            session.query(TWEET.tweet_id)
            .filter(TWEET.tweet_id == tweet.tweet_id)).first()
        if not tweet_exists:
            new_tweet = TWEET()
            new_tweet.tweet_id = tweet.tweet_id
            new_tweet.user_id = tweet.auteur_id
            new_tweet.user_name = tweet.auteur
            new_tweet.date = tweet.date
            new_tweet.month = tweet.mois
            new_tweet.year = tweet.annee
            new_tweet.content = tweet.texte
            new_tweet.clean_text = tweet.texte_retraite
            new_tweet.is_retweet = tweet.retweet
            new_tweet.hashtags = tweet.hashtags
            new_tweet.is_active = tweet.active
            new_tweet.retweet_count = tweet.nb_rt
            new_tweet.fav_count = tweet.nb_favori
            new_tweet.influence_date = tweet.date_influence
            new_tweet.mentions = tweet.mentions
            new_tweet.reply_to = tweet.dest
            new_tweet.json = tweet.json
        
            session.add(new_tweet)
        else:
            print(f"Tweet déjà existant {tweet.tweet_id}")
        if i % 10000 == 0:
            session.commit()
    session.commit()


move_account()
move_tweets()

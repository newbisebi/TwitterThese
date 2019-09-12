import os
from utils.models import session, USER, TWEET
from config.config import BDD_DIR, BDD_FILE
from utils.decorateurs import timeur


@timeur
def print_stats():
    nb_tweets = session.query(TWEET).count()
    nb_comptes = (session.query(USER).count())
    nb_tweets_envir = (
        session.query(TWEET)
        .filter(TWEET.envir3 == True)
        .count()
    )
    nb_comptes_envir = (
        session.query(USER)
        .filter(USER.is_envir == True)
        .count()
    )

    print(f"Nombre de tweets : {nb_tweets}")
    print(f"Nombre de tweets environnementaux : {nb_tweets_envir}")
    print(f"Nombre de comptes d'utilisateurs : {nb_comptes}")
    print(f"Nombre de comptes environnementaux : {nb_comptes_envir}")


def print_bdd_size():
    filepath = os.path.join(BDD_DIR, BDD_FILE)
    size = os.path.getsize(filepath)

    if size < 1024:
        unite = "o"
    elif size < 1024 ** 2:
        size = size / 1024
        unite = "Ko"
    elif size < 1024 ** 3:
        size = size / 1024 ** 2
        unite = "Mo"
    else:
        size = size / 1024 ** 3
        unite = "Go"
    print(f"Taille du fichier de données : {round(size, 2)} {unite}")


def main():
    print_bdd_size()
    print_stats()


if __name__ == '__main__':
    print_bdd_size()
    print_stats()

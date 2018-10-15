from utils.models import session, COMPTES, TL


def print_stats():
    nb_tweets = session.query(TL).count()
    nb_comptes = session.query(COMPTES).count()

    print(f"Nombre de tweets : {nb_tweets}")
    print(f"Nombre de comptes d'utilisateurs : {nb_comptes}")


if __name__ == '__main__':
    print_stats()

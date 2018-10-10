# -*- coding: utf-8 -*-
"""
Date de création : 14/06/2017 par Sébastien Mariaux
Mise à jour : 03/10/2018 - Python3 par Sébastien Mariaux

Ce script a pour but de constituer une liste de compte Twitter à partir d'un compte de référence.

Tous les comptes "suivis" par ce compte de référence (abonnements) sont intégrés à la base de donnée

Le compte Twitter de référence est défini dans le fichier config
"""

#Import des modules
import time
from twython import Twython, TwythonError #interface avec Twitter
from datetime import datetime, date
from config.config import API, TARGET_ACCOUNT
from utils.models import session, COMPTES
from utils.mylog import logger as lg

#Détermination de la date actuelle
auj = time.strftime('%y_%m_%d', time.localtime())


def api_request(reference_account):
    """
    Query the Twitter API to get list of account followed by the target account 
    Returns the list of results
    """
    curseur = -1 #200 résultats maximum s'affiche par page ; le curseur permet d'afficher les pages successives.
        #Quand le curseur est égal à 0, on a atteint la dernière page, on arrête la boucle
    followed_accounts = []
    while curseur !=0:
        try:
            res = API.get_friends_list(screen_name =  reference_account, 
                                        count = 200,
                                        cursor = curseur)
            for user in res["users"]:
                followed_accounts.append(user)
            lg.info(f"Adding {len(res['users'])} accounts to account list")
        except TwythonError as e:
            lg.critical(f"Collecte des utilisateurs interrompue : {e}")
            break
        curseur = res["next_cursor"]

    lg.info(f"Account list completed : {len(followed_accounts)} accounts added")
    return followed_accounts

def write_account_to_db(user, session):
    """
    Write user (account) data to the sqlite database
    returns none
    """
    nom_utilisateur = user["screen_name"]
    description = user["description"]
    id_utilisateur = user["id"]
    nb_abonnements = user["friends_count"]
    nb_abonnes = user["followers_count"]
    nb_tweets = user["statuses_count"]

    #Enregistrement dans la base (si pas déjà existant) :
    user_exists = session.query(COMPTES).filter_by(id_utilisateur= id_utilisateur)
    if not user_exists.all(): #Si non existant on le créé
        account = COMPTES(nom_utilisateur=nom_utilisateur,
                            description = description,
                            nb_abonnements = nb_abonnements,
                            nb_abonnes = nb_abonnes,
                            nb_tweets = nb_tweets,
                            id_utilisateur=id_utilisateur)
        session.add(account)
        lg.info(f"committing user {nom_utilisateur} to db")
        session.commit()

    else : #Si existant on met à jour les infos
        user = user_exists.one()
        user.nb_abonnements = nb_abonnements
        user.nb_abonnes = nb_abonnes
        user.nb_tweets = nb_tweets
        user.date_maj = time.strftime('%Y/%m/%d',time.localtime())
        user.description = description
        session.commit()
        session.close()

def main(session=session, account=TARGET_ACCOUNT): 
    """
    session passed as parameter in order to be able to test on another database
    """
    followed_accounts = api_request(TARGET_ACCOUNT)
    if followed_accounts:
        lg.info("Recording user to db")
        for account in followed_accounts:
            write_account_to_db(account, session)
        lg.info("All users saved to db")
    
if __name__ == "__main__":
    main(session, TARGET_ACCOUNT)


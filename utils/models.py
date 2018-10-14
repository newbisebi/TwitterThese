# -*- coding: utf-8 -*-
"""
Format des tables utilisées dans la base de données
"""

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
import time
from datetime import datetime
from config.config import FICHIER_BDD

Base = declarative_base()


class COMPTES(Base):
    """
    Définit le format de la table dans laquelle sera stockée la liste des
    comptes Twitter d'organisations de l'ESS.
    """
    __tablename__ = 'Comptes_ESS'
    rowid = Column(Integer, primary_key=True)
    # Nom du compte twitter (sans le @)
    nom_utilisateur = Column(String)
    # Identifiant du compte
    id_utilisateur = Column(Integer)
    # Présentation de l'utilisateur
    description = Column(String)
    # Nombre de comptes suivis
    nb_abonnements = Column(Integer)
    # nombre de followers
    nb_abonnes = Column(Integer)
    # Nombre de tweets total (<>nombre collectés)
    nb_tweets = Column(Integer)
    # type d'organisation ou d'invididu --> codage manuel
    type_compte = Column(String)
    # Orga ayant rôle environnemental --> codage manuel
    compte_envir = Column(Boolean)
    # Date de mise à jour auto des infos
    date_maj = Column(String)
    # Colonne à des fins techinques :
    # Nombre de fois ou la TL de ce compte est collectée
    nombre_recherches = Column(Integer)
    # Colonne à des fins techinques :
    # Vrai si collecte terminée (=plus anciens tweets collectés)
    fini = Column(Boolean)

    def __init__(self, user):
        self.nom_utilisateur = user["screen_name"]
        self.description = user["description"]
        self.id_utilisateur = user["id"]
        self.nb_abonnements = user["friends_count"]
        self.nb_abonnes = user["followers_count"]
        self.nb_tweets = user["statuses_count"]
        self.date_maj = time.strftime('%Y/%m/%d', time.localtime())
        self.nombre_recherches = 0
        self.fini = False

    def update_compte(self, user):
        self.nb_abonnements = user["friends_count"]
        self.nb_abonnes = user["followers_count"]
        self.nb_tweets = user["statuses_count"]
        self.date_maj = time.strftime('%Y/%m/%d', time.localtime())
        self.description = user["description"]

    def __repr__(self):
        return self.nom_utilisateur


class TL(Base):
    """
    Format de la table dans laquelle vont être stockés les tweets
    """
    __tablename__ = 'timeline'
    rowid = Column(Integer, primary_key=True)
    tweet_id = Column(Integer)
    auteur = Column(String)
    auteur_id = Column(Integer)
    date = Column(DateTime)
    mois = Column(String)
    annee = Column(String)
    texte = Column(String)
    texte_retraite = Column(String)
    retweet = Column(Boolean)
    hashtags = Column(String)
    active = Column(Boolean)
    nb_rt = Column(Integer)
    nb_favori = Column(Integer)
    date_influence = Column(String)
    envir1 = Column(Boolean)
    envir2 = Column(Boolean)
    envir3 = Column(Boolean)
    mentions = Column(String)
    dest = Column(String)
    json = Column(String)

    def __init__(self, status):
        self.tweet_id = status["id"]
        self.auteur = status["user"]["screen_name"]
        self.auteur_id = status["user"]["id"]
        date = status["created_at"]
        date = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
        # date1 = date.strftime('%Y-%m-%d')
        self.mois = date.strftime('%m')
        self.annee = date.strftime('%Y')
        self.date = date
        self.texte = status["full_text"]
        self.texte_retraite = ""
        self.retweet = status["retweeted"]
        self.json = str(status)
        self.active = True
        hashtags = status["entities"]["hashtags"]
        if hashtags:
            self.hashtags = ', '.join([el['text'] for el in hashtags])
        else:
            self.hashtags = ""
        mentions = status["entities"]["user_mentions"]
        if mentions:
            self.mentions = ','.join(
                [f"{el['screen_name']} ({el['id']})" for el in mentions]
                )
        else:
            self.mentions = ""
        id_dest = status["in_reply_to_user_id"]
        nom_dest = status["in_reply_to_screen_name"]
        if id_dest:
            self.dest = f"{nom_dest} ({id_dest})"
        else:
            self.dest = ""


class AMIS(Base):
    """
    Format de la table dans laquelle vont être stockés les utilisateurs suivis
    """
    __tablename__ = 'amis'
    rowid = Column(Integer, primary_key=True)
    nom_utilisateur = Column(String)    # Nom du compte twitter 
    id_utilisateur = Column(Integer)    # Identifiant du compte
    id_ami = Column(Integer)
    nom_ami = Column(String)

    def __init__(self, id_utilisateur, nom_utilisateur, id_ami, nom_ami):
        self.id_utilisateur = id_utilisateur
        self.nom_utilisateur = nom_utilisateur
        self.id_ami = id_ami
        self.nom_ami = nom_ami

    def __repr__(self):
        return self.nom_utilisateur


# CONNECTION ET CREATION DES TABLES
engine = sqlalchemy.create_engine(FICHIER_BDD, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

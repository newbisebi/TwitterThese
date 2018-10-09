# -*- coding: utf-8 -*-
"""
Format des tables utilisées dans la base de données
"""

import sqlalchemy #Interface sqlite
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float, Boolean
from sqlalchemy.orm import mapper, sessionmaker
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float, Boolean
from sqlalchemy.orm import mapper, sessionmaker
import time
from config.config import FICHIER_BDD

Base = declarative_base()


class COMPTES(Base):
    """
    Définit le format de la table dans laquelle sera stockée la liste des
    comptes Twitter d'organisations de l'ESS.
    """
    __tablename__ = 'Comptes_ESS'
    rowid = Column(Integer, primary_key=True)
    nom_utilisateur = Column(String) #Nom du compte twitter (sans le @)
    id_utilisateur = Column(Integer)#Identifiant du compte
    description = Column(String) #Présentation de l'utilisateur
    nb_abonnements = Column(Integer) #Nombre de comptes suivis
    nb_abonnes = Column(Integer) #nombre de followers
    nb_tweets = Column(Integer) #Nombre de tweets total (<>nombre collectés)
    type_compte = Column(String) #type d'organisation ou d'invididu --> codage manuel
    compte_envir = Column(Boolean) #Orga ayant rôle environnemental --> codage manuel
    date_maj = Column(String) #Date de mise à jour auto des infos
    nombre_recherches = Column(Integer) #Colonne à des fins techinques : Nombre de fois ou la TL de ce compte est collectée
    fini = Column(Boolean) #Colonne à des fins techinques : Vrai si collecte terminée (=plus anciens tweets collectés)

    def __init__(self,nom_utilisateur, id_utilisateur, description, nb_abonnements, nb_abonnes, nb_tweets):
        self.nom_utilisateur = nom_utilisateur
        self.id_utilisateur = id_utilisateur
        self.description = description
        self.nb_abonnements = nb_abonnements
        self.nb_abonnes = nb_abonnes
        self.nb_tweets = nb_tweets
        self.date_maj = time.strftime('%Y/%m/%d',time.localtime())
        self.nombre_recherches = 0
        self.fini = False

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
    retweet = Column(Boolean) #On n'a pas collecté les RT
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


    def __init__(self, tweet_id, auteur, auteur_id, date, mois, annee, texte, rt, hashtags, mentions, dest, json):
        self.tweet_id = tweet_id
        self.auteur = auteur
        self.auteur_id = auteur_id
        self.date = date
        self.mois = mois
        self.annee = annee
        self.texte = texte
        self.texte_retraite = ""
        self.retweet=rt
        self.hashtags = hashtags
        self.active = True
        self.nb_favori = None
        self.nb_rt = None
        self.date_influence = None
        self.envir1 = None
        self.envir2 = None
        self.envir3 = None
        self.mentions = mentions
        self.dest = dest
        self.json=json


class AMIS(Base):
    """
    Format de la table dans laquelle vont être stockés les utilisateurs suivis
    """
    __tablename__ = 'amis'
    rowid = Column(Integer, primary_key=True)
    nom_utilisateur = Column(String) #Nom du compte twitter (sans le @)
    id_utilisateur = Column(Integer)#Identifiant du compte
    id_ami = Column(Integer)
    nom_ami = Column(String)

    def __init__(self, id_utilisateur, nom_utilisateur, id_ami, nom_ami):
        self.id_utilisateur = id_utilisateur
        self.nom_utilisateur = nom_utilisateur
        self.id_ami = id_ami
        self.nom_ami = nom_ami

    def __repr__(self):
        return self.nom_utilisateur

class MODUL(Base):
    """
    Format de la table dans laquelle vont être stockés les utilisateurs suivis
    """
    __tablename__ = 'Modularite'
    rowid = Column(Integer, primary_key=True)
    auteur = Column(String)
    classe = Column(String)


    def __repr__(self):
        return self.auteur, self.classe


#CONNECTION ET CREATION DES TABLES
engine = sqlalchemy.create_engine(FICHIER_BDD, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
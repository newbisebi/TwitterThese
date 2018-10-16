# -*- coding: utf-8 -*-
"""
Format des tables utilisées dans la base de données
"""

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import time
from datetime import datetime
from config.config import FICHIER_BDD

Base = declarative_base()


class USER(Base):
    """
    Définit le format de la table dans laquelle sera stockée la liste des
    comptes Twitter d'organisations de l'ESS.
    """
    __tablename__ = 'users'
    # Nom du compte twitter (sans le @)
    user_name = Column(String)
    # Identifiant du compte
    user_id = Column(Integer, primary_key=True)
    # Présentation de l'utilisateur
    description = Column(String)
    # Nombre de comptes suivis
    friends = Column(Integer)
    # nombre de followers
    followers = Column(Integer)
    # Nombre de tweets total (<>nombre collectés)
    tweets_count = Column(Integer)
    # type d'organisation ou d'invididu --> codage manuel
    account_type = Column(String)
    # Orga ayant rôle environnemental --> codage manuel
    is_envir = Column(Boolean)
    # Date de mise à jour auto des infos
    upd_date = Column(String)
    # Colonne à des fins techinques :
    # Nombre de fois ou la TL de ce compte est collectée
    queries = Column(Integer)
    # Colonne à des fins techinques :
    # Vrai si collecte terminée (=plus anciens tweets collectés)
    is_completed = Column(Boolean)

    def __init__(self, user):
        self.user_name = user["screen_name"]
        self.description = user["description"]
        self.user_id = user["id"]
        self.friends = user["friends_count"]
        self.followers = user["followers_count"]
        self.tweets_count = user["statuses_count"]
        self.upd_date = time.strftime('%Y/%m/%d', time.localtime())
        self.queries = 0
        self.is_completed = False

    def update_compte(self, user):
        self.friends = user["friends_count"]
        self.followers = user["followers_count"]
        self.tweets_count = user["statuses_count"]
        self.upd_date = time.strftime('%Y/%m/%d', time.localtime())
        self.description = user["description"]

    def __repr__(self):
        return self.user_name


class TWEET(Base):
    """
    Format de la table dans laquelle vont être stockés les tweets
    """
    __tablename__ = 'tweets'
    tweet_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_id = Column(Integer)
    date = Column(DateTime)
    month = Column(String)
    year = Column(String)
    content = Column(String)
    clean_text = Column(String)
    is_retweet = Column(Boolean)
    hashtags = Column(String)
    is_active = Column(Boolean)
    retweet_count = Column(Integer)
    fav_count = Column(Integer)
    influence_date = Column(String)
    envir1 = Column(Boolean)
    envir2 = Column(Boolean)
    envir3 = Column(Boolean)
    mentions = Column(String)
    reply_to = Column(String)
    json = Column(String)

    def __init__(self, status):
        self.tweet_id = status["id"]
        self.user_name = status["user"]["screen_name"]
        self.user_id = status["user"]["id"]
        date = status["created_at"]
        date = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
        # date1 = date.strftime('%Y-%m-%d')
        self.month = date.strftime('%m')
        self.year = date.strftime('%Y')
        self.date = date
        self.content = status["full_text"]
        self.clean_text = ""
        self.is_retweet = status["retweeted"]
        self.json = str(status)
        self.is_active = True
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
        reply_id = status["in_reply_to_user_id"]
        reply_name = status["in_reply_to_screen_name"]
        if reply_id:
            self.reply_to = f"{reply_name} ({reply_id})"
        else:
            self.reply_to = ""


class FRIENDSHIP(Base):
    __tablename__ = 'friendships'
    rowid = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    friend_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("USER", foreign_keys=[user_id])
    friend = relationship("USER", foreign_keys=[friend_id])

    def __init__(self, user, friend):
        self.user = user
        self.friend = friend

    def __repr__(self):
        return f"{self.user} is following {self.friend}"


# CONNECTION ET CREATION DES TABLES
engine = sqlalchemy.create_engine(FICHIER_BDD, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

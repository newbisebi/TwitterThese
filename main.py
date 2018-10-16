# -*- coding: utf-8 -*-

"""
Date de création : 03/10/2018 par Sébastien Mariaux

Regroupe les différentes opérations effectués dans le cadre de l'étude
- Création de la liste des utilisateurs
- Collecte des tweets
- Collecte des informations complémentaires
- Retraitement du texte
"""
from utils.models import session
import twitter_accounts # noqa
import twitter_timelines
import influence
import processing
import tweet_envir

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> COLLECTE DES DONNEES<<<<<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# ETAPE 1 : CREATION DE lA LISTE DES UTILISATEURS
twitter_accounts.main()

# ETAPE 2 : COLLECTE DES TWEETS DES UTILISATEURS
twitter_timelines.main(session=session, direction="older")

# # ETAPE 3 : COLLECTE DES INFORAMTIONS COMPLEMENTAIRES (nombre de RT et favoris)
# for annee in range(2006, 2018):
#     influence.main(annee)

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> RETRAITEMENT DES DONNEES<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# # ETAPE4 : RETRAITEMENT DU TEXTE
processing.main()   # lemmatisation etc.
tweet_envir.main()  # Détermination du caractère environnemental


"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> ANALYSE DES DONNEES<<<<<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

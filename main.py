# -*- coding: utf-8 -*-

"""
Date de création : 03/10/2018 par Sébastien Mariaux

Regroupe les différentes opérations effectués dans le cadre de l'étude
- Création de la liste des utilisateurs
- Collecte des tweets
- Collecte des informations complémentaires
- Retraitement du texte
"""
import twitter_accounts     # noqa
import twitter_timelines    # noqa
import twitter_network      # noqa
import influence            # noqa
import processing           # noqa
import tweet_envir          # noqa
from utils.models import session

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> COLLECTE DES DONNEES<<<<<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# # ETAPE 1 : CREATION DE lA LISTE DES UTILISATEURS
# twitter_accounts.main()

# # ETAPE 2 : COLLECTE DES TWEETS DES UTILISATEURS
# twitter_timelines.main(session=session, direction="older")

# ETAPE 3 : COLLECTE DES INFORAMTIONS COMPLEMENTAIRES (nombre de RT et favoris)
for annee in range(2006, 2018):
    print(annee)
    influence.main(annee, session=session)

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> RETRAITEMENT DES DONNEES<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# # ETAPE4 : RETRAITEMENT DU TEXTE
processing.main()   # lemmatisation etc.
tweet_envir.main()  # Détermination du caractère environnemental

# ETAPE 5 : CONSTITUTION DU RESEAU D'UTILISATEURS
twitter_network.main()

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> ANALYSE DES DONNEES<<<<<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

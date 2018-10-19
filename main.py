# -*- coding: utf-8 -*-

"""
Date de création : 03/10/2018 par Sébastien Mariaux

Regroupe les différentes opérations effectués dans le cadre de l'étude
- Création de la liste des utilisateurs
- Collecte des tweets
- Collecte des informations complémentaires
- Retraitement du texte
"""
import sys
from collecte import influence, twitter_network, twitter_accounts, twitter_timelines
from processtext import tweet_envir, processing
from utils import stats
from utils.models import session
from utils.mylog import logger as lg


class MainMenu():
    def get_choice(self):
        mainChoice = input("""
        --------------------------
        *** MENU PRINCIPAL ***
        --------------------------
        1 - Collecter des données
        2 - Retraiter les données 
        3 - Analyser des données
        4 - Afficher les infos de la BDD
        --------------------------
        9 - Quitter le programme
        --------------------------
        Entrez l'option souhaitée...
        """)
        return mainChoice

    def run_program(self):
        choice = None
        while not choice:
            choice = self.get_choice()
            if choice == "1":
                CollecteMenu().run_collecte()
                choice = None
            elif choice == "2":
                ProcessMenu().run_collecte()
                choice = None
            elif choice == "3":
                choice = None
            elif choice == "4":
                stats.main()
                choice = None
            elif choice == "9":
                sys.exit("Programme terminé")
            else:
                choice = None
                print("Veuillez choisir une option valide")


class CollecteMenu():
    def get_choice(self):
        collecteChoice = input("""
        --------------------------
        *** COLLECTE DES DONNEES TWITTER ***
        --------------------------
        1 - Créer / mettre à jour la liste des utilisateurs
        2 - Collecter les tweets
        3 - Collecter le réseau d'utilisateur
        4 - Collecter les données de performance des tweets
        --------------------------
        8 - Retour au Menu Principal
        9 - Quitter le programme
        --------------------------
        Entrez l'option souhaitée...
        --------------------------
        """)
        return collecteChoice


    def run_collecte(self):
        choice = None
        while not choice:
            choice = self.get_choice()
            if choice == "1":
                twitter_accounts.main()
                choice = None
            elif choice == "2":
                twitter_timelines.main()
                choice = None
            elif choice == "3":
                twitter_network.main()
                choice = None
            elif choice == "4":
                lg.info("WARNING : Collecte jusqu'en 2017 uniquement")
                for annee in range(2006, 2018):
                    influence.main(annee)
                choice = None
            elif choice == "8":
                MainMenu().run_program()
            elif choice == "9":
                sys.exit("Programme terminé")
            else:
                choice = None
                print("Veuillez choisir une option valide")


class ProcessMenu():
    def get_choice(self):
        collecteChoice = input("""
        --------------------------
        *** TRAITEMENT DES DONNEES ***
        --------------------------
        1 - Retraitement du texte (lemmatisation etc.)
        2 - Détermination du caractère environnemental
        --------------------------
        8 - Retour au Menu Principal
        9 - Quitter le programme
        --------------------------
        Entrez l'option souhaitée...
        --------------------------
        """)
        return collecteChoice

    def run_collecte(self):
        choice = None
        while not choice:
            choice = self.get_choice()
            if choice == "1":
                processing.main()
            elif choice == "2":
                tweet_envir.main()
            elif choice == "8":
                MainMenu().run_program()
            elif choice == "9":
                sys.exit("Programme terminé")
            else:
                choice = None
                print("Veuillez choisir une option valide")



MainMenu().run_program()

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> COLLECTE DES DONNEES<<<<<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# # ETAPE 1 : CREATION DE lA LISTE DES UTILISATEURS
# twitter_accounts.main()

# # ETAPE 2 : COLLECTE DES TWEETS DES UTILISATEURS
# twitter_timelines.main(session=session, direction="older")

# # ETAPE 3 : COLLECTE DES INFORAMTIONS COMPLEMENTAIRES (nombre de RT et favoris)
# for annee in range(2006, 2018):
#     print(annee)
#     influence.main(annee, session=session)

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> RETRAITEMENT DES DONNEES<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# # # ETAPE4 : RETRAITEMENT DU TEXTE
# processing.main()   # lemmatisation etc.
# tweet_envir.main()  # Détermination du caractère environnemental

# # ETAPE 5 : CONSTITUTION DU RESEAU D'UTILISATEURS
# twitter_network.main()

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
>>>>>>>>>>>>>>>>> ANALYSE DES DONNEES<<<<<<<<<<<<<<<<<<<<<<<<
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

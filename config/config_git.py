
# ###### RENAME FILE "config.py" ###########

import os
from twython import Twython

# FILL WITH YOUR TWITTER AUTH DETAILS
API = Twython(
    app_key='XXXX',
    app_secret='XXXX',
    oauth_token='XXXX',
    oauth_token_secret='XXXX')

current_dir = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(current_dir)

BDD_DIR = os.path.join(PROJECT_DIR, 'data')
BDD_FILE = 'tweets.sqlite'
FICHIER_BDD = os.path.join('sqlite:///', BDD_DIR, BDD_FILE)

FICHIER_BDD_TEST = os.path.join('sqlite:///', BDD_DIR, 'data_test.sqlite')

TARGET_ACCOUNT = "RechercheESS"

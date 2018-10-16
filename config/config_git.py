
# ###### RENAME FILE "config.py" ###########

from twython import Twython

# FILL WITH YOUR TWITTER AUTH DETAILS
API = Twython(
    app_key='XXXX',
    app_secret='XXXX',
    oauth_token='XXXX',
    oauth_token_secret='XXXX')

BDD_DIR = 'data/'
BDD_FILE = 'data.sqlite'
FICHIER_BDD = 'sqlite:///' + BDD_DIR + BDD_FILE

FICHIER_BDD_TEST = 'sqlite:///data_test.sqlite'

TARGET_ACCOUNT = ""

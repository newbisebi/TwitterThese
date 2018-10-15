
# ###### RENAME FILE "config.py" ###########

from twython import Twython

# FILL WITH YOUR TWITTER AUTH DETAILS
API = Twython(
    app_key='XXXX',
    app_secret='XXXX',
    oauth_token='XXXX',
    oauth_token_secret='XXXX')

FICHIER_BDD = 'sqlite:///data.sqlite'

FICHIER_BDD_TEST = 'sqlite:///data_test.sqlite'

TARGET_ACCOUNT = ""

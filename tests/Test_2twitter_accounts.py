from utils.models import COMPTES, Base
import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
import twitter_accounts
import json
import config
from config.config import FICHIER_BDD_TEST
from utils.mylog import logger as lg
import os



#Connection à la BDD de test
if os.path.exists("data_test.sqlite"):
    os.remove("data_test.sqlite") 
engine = sqlalchemy.create_engine(FICHIER_BDD_TEST, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def test_accounts_created(monkeypatch):
    def mockreturn(screen_name, count, cursor):
        with open("tests/sample_accounts.json","r") as f:
            res =  json.load(f)
        return res

    monkeypatch.setattr(config.config.API, 'get_friends_list', mockreturn)
    twitter_accounts.main(session)

    nb_rows = session.query(COMPTES).count()
    assert nb_rows == 5

def test_valeurs_champs_utilisateurs():
    user = session.query(COMPTES).get(4)
    assert user.nom_utilisateur == "ONGDEFI"
    assert user.id_utilisateur == 121390266
    assert user.description == "DEFI Développer Former Informer est une ONG de développement spécialisée dans l'éducation et la formation.  contact@ongdefi.org"
    assert user.nb_abonnes == 247
    assert user.nb_tweets == 274
    assert user.type_compte == None
    assert user.compte_envir == None
    assert user.nombre_recherches == 0
    assert user.fini == False
    
from utils.models import USER, Base
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from collecte import twitter_accounts
import json
import config
from config.config import FICHIER_BDD_TEST
import os


# Connection à la BDD de test
if os.path.exists("data/data_test.sqlite"):
    os.remove("data/data_test.sqlite")
engine = sqlalchemy.create_engine(FICHIER_BDD_TEST, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def test_accounts_created(monkeypatch):
    def mockreturn(screen_name, count, cursor):
        with open("tests/sample_accounts.json", "r") as f:
            res = json.load(f)
        return res

    monkeypatch.setattr(config.config.API, 'get_friends_list', mockreturn)
    twitter_accounts.main(session)

    nb_rows = session.query(USER).count()
    assert nb_rows == 5


def test_valeurs_champs_utilisateurs():
    user = session.query(USER).get(121390266)
    assert user.user_name == "ONGDEFI"
    assert user.user_id == 121390266
    assert user.description == "DEFI Développer Former Informer est une ONG de développement spécialisée dans l'éducation et la formation.  contact@ongdefi.org"    # noqa
    assert user.followers == 247
    assert user.tweets_count == 274
    assert user.account_type is None
    assert user.is_envir is None
    assert user.queries == 0
    assert user.is_completed is False

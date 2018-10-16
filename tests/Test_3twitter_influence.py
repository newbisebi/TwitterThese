from utils.models import TWEET, Base
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import influence
import json
import config
from config.config import FICHIER_BDD_TEST


# Connection à la BDD de test
engine = sqlalchemy.create_engine(FICHIER_BDD_TEST, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


def test_influence_collected(monkeypatch):
    def mockreturn(id):
        with open("tests/sample_influence.json", "r") as f:
            res = json.load(f)
        return res

    monkeypatch.setattr(config.config.API, 'lookup_status', mockreturn)
    influence.main(2018, session)

    tweet1 = session.query(TWEET).get(1050302617165983744)
    tweet2 = session.query(TWEET).get(1050303301911232513)
    tweet3 = session.query(TWEET).get(1051014633346256897)
    tweet4 = session.query(TWEET).get(1051446416634195968)

    assert tweet1.retweet_count == 4
    assert tweet2.retweet_count == 258
    assert tweet3.fav_count == 1404
    assert tweet4.fav_count == 14

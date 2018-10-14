from utils.models import TL, Base
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

    tweet1 = session.query(TL).get(1)
    tweet2 = session.query(TL).get(2)
    tweet3 = session.query(TL).get(6)
    tweet4 = session.query(TL).get(7)

    assert tweet1.nb_rt == 17
    assert tweet2.nb_rt == 0
    assert tweet3.nb_favori == 1524
    assert tweet4.nb_favori == 14

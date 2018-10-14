"""
# TODO
A supprimer car ne teste pas le programme mais les données
==> intégrer dans un script séparé des tests
"""
from utils.models import session, TL


# def test_all_text_processed():
#     """Check if all text has been processed (texte_retraite column not empty)"""
#     nb_empty_text_field = session.query(TL).filter(TL.texte_retraite=="").count()
#     assert nb_empty_text_field == 0 

# def test_rt_completed():
#     """check if all rt fields are filed"""
#     nb_empty_rt_field = session.query(TL).filter(TL.nb_rt==None).count()
#     assert nb_empty_rt_field == 0

# def test_fav_completed():
#     """check if all favorites fields are filed"""
#     nb_empty_fav_field = session.query(TL).filter(TL.nb_favori==None).count()
#     assert nb_empty_fav_field == 0

# def test_date_influence_not_empty():
#     """check if all date_influence fields are filed"""
#     nb_empty_dinfluence_field = session.query(TL).filter(TL.date_influence==None).count()
#     assert nb_empty_dinfluence_field == 0

# def test_envir3_not_empty():
#     """check if all envir3 fields are filed"""
#     nb_empty_envir3_field = session.query(TL).filter(TL.envir3==None).count()
#     assert nb_empty_envir3_field == 0

# def test_unique_tweet_id():
#     """check that they are no repeated tweet_id"""
#     nb_rows = session.query(TL.tweet_id).count()
#     nb_unique_rows = session.query(TL.tweet_id).group_by(TL.tweet_id).count()
#     assert nb_rows == nb_unique_rows
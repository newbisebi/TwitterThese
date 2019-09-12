import time
from .mylog import logger as lg


def timeur(func):
    def wrapper(*args, **kwargs):
        debut = time.clock()
        func(*args, **kwargs)
        fin = time.clock()
        temps = round(fin - debut, 2)
        lg.info(f"Fonction {func.__name__} exécutée en {temps} secondes")
    return wrapper

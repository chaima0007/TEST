"""Reprise sur erreur : backoff exponentiel pour les appels reseau.

Si un appel API echoue (timeout, surcharge, erreur reseau), on reessaie
plusieurs fois avec un delai croissant (2s, 4s, 8s, 16s) avant d'abandonner.
"""
import time
import functools


def avec_retry(tentatives=4, base=2.0, exceptions=(Exception,)):
    """Decorateur : reessaie la fonction avec un delai croissant.

    tentatives : nombre total d'essais
    base       : base du delai (2.0 -> 2s, 4s, 8s, 16s)
    exceptions : types d'erreurs qui declenchent une nouvelle tentative
    """
    def decorateur(fonction):
        @functools.wraps(fonction)
        def wrapper(*args, **kwargs):
            derniere_erreur = None
            for tentative in range(tentatives):
                try:
                    return fonction(*args, **kwargs)
                except exceptions as e:
                    derniere_erreur = e
                    if tentative < tentatives - 1:
                        time.sleep(base ** (tentative + 1))
            raise derniere_erreur
        return wrapper
    return decorateur

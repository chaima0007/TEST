"""Journaux structures en JSON : un evenement = une ligne JSON.

Pratique pour l'audit (qui a propose quoi, qui a valide) et pour l'analyse
ulterieure (Grafana/Loki, Datadog...).
"""
import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    """Formate chaque log en une ligne JSON lisible par une machine."""

    def format(self, record):
        evenement = {
            "niveau": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Champs additionnels passes via extra={"extra_data": {...}}
        if hasattr(record, "extra_data"):
            evenement.update(record.extra_data)
        return json.dumps(evenement, ensure_ascii=False)


def get_logger(nom="collab-ia"):
    logger = logging.getLogger(nom)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_event(logger, message, **donnees):
    """Journalise un evenement avec des champs structures.

    Exemple : log_event(logger, "tache_recue", task_id="001", modele="claude")
    """
    logger.info(message, extra={"extra_data": donnees})

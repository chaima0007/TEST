"""Planificateur : execute les taches a intervalle regulier (mode 24/7 local).

Lancement :
    python scheduler.py

Arret : appuyez sur Ctrl + C

L'intervalle se regle via la variable d'environnement INTERVAL_MINUTES
(par defaut : 60 minutes). La premiere tache s'execute immediatement, puis
le planificateur attend l'intervalle avant la suivante.

ATTENTION : chaque execution consomme un peu de credit API (Claude + Mistral).
Choisissez un intervalle raisonnable pour maitriser les couts.
"""
import os
import time

from core.config import load_config, ConfigError
from core.logging import get_logger, log_event
from llm.claude import ClientClaude
from llm.mistral import ClientMistral
from llm.verifier import DoubleControle
from orchestrator.orchestrator import Orchestrateur
from tasks.example_task import TACHE_EXEMPLE


def main():
    logger = get_logger()

    try:
        config = load_config()
    except ConfigError as e:
        print(f"ERREUR de configuration : {e}")
        print("Definissez vos cles (voir .env.example) puis relancez.")
        return

    intervalle_min = float(os.environ.get("INTERVAL_MINUTES", "60"))

    claude = ClientClaude(config.anthropic_api_key, config.claude_model)
    mistral = ClientMistral(config.mistral_api_key, config.mistral_model)
    orchestrateur = Orchestrateur(DoubleControle(claude, mistral), logger)

    log_event(logger, "planificateur_demarre", intervalle_minutes=intervalle_min)
    print(f"Planificateur lance : une tache toutes les {intervalle_min} min.")
    print("Appuyez sur Ctrl + C pour arreter.\n")

    compteur = 0
    try:
        while True:
            compteur += 1
            task_id = f"tache-{compteur:04d}"
            try:
                resultat = orchestrateur.traiter(task_id, TACHE_EXEMPLE)
                print(f"[{task_id}] Decision : {resultat.verdict}")
            except Exception as e:
                # Une tache qui echoue n'arrete PAS le planificateur.
                log_event(logger, "tache_en_erreur", task_id=task_id, erreur=str(e))
                print(f"[{task_id}] Erreur (le planificateur continue) : {e}")

            time.sleep(intervalle_min * 60)
    except KeyboardInterrupt:
        log_event(logger, "planificateur_arrete")
        print("\nPlanificateur arrete proprement. A bientot !")


if __name__ == "__main__":
    main()

"""Point d'entree : lance une tache d'exemple via le double controle Claude x Mistral.

Lancement :
    python main.py

Prerequis : variables d'environnement ANTHROPIC_API_KEY et MISTRAL_API_KEY
(voir le fichier .env.example).
"""
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

    log_event(logger, "demarrage", claude=config.claude_model, mistral=config.mistral_model)

    # Creation des deux clients
    claude = ClientClaude(config.anthropic_api_key, config.claude_model)
    mistral = ClientMistral(config.mistral_api_key, config.mistral_model)

    # Double controle : Claude propose, Mistral verifie
    double_controle = DoubleControle(proposeur=claude, verificateur=mistral)
    orchestrateur = Orchestrateur(double_controle, logger)

    resultat = orchestrateur.traiter("tache-001", TACHE_EXEMPLE)

    # Affichage lisible pour l'humain
    print("\n=== PROPOSITION (Claude) ===\n" + resultat.proposition)
    print("\n=== VERIFICATION (Mistral) ===\n" + resultat.justification)
    print("\n=== DECISION ===\n" + ("APPROUVE" if resultat.approuve else "REJETE"))


if __name__ == "__main__":
    main()

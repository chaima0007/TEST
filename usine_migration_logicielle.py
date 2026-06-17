import sys
from anthropic import Anthropic

client = Anthropic()
MODEL_NAME = "claude-opus-4-8"


def executer_agent(nom_agent, system_prompt, user_content, effort="high"):
    print(f"\n{'='*60}")
    print(f"[{nom_agent}] en cours...")
    print("=" * 60)

    texte = ""
    with client.messages.stream(
        model=MODEL_NAME,
        max_tokens=4000,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        for event in stream:
            if hasattr(event, "type"):
                if event.type == "content_block_start":
                    if getattr(event.content_block, "type", None) == "thinking":
                        print("[réflexion...]", flush=True)
                elif event.type == "content_block_delta":
                    delta = event.delta
                    if getattr(delta, "type", None) == "text_delta":
                        print(delta.text, end="", flush=True)
                        texte += delta.text

    print()
    return texte


def usine_migration_logicielle(code_obsolete_client):
    # AGENT 1: Architecte Analyste
    plan_migration = executer_agent(
        "Architecte Analyste",
        (
            "Tu es un Architecte Logiciel Senior, spécialiste de la modernisation "
            "de systèmes legacy. Analyse le code obsolète fourni et produis un plan "
            "de migration détaillé : technologies cibles, risques, dépendances à "
            "remplacer, et étapes de refactorisation."
        ),
        code_obsolete_client,
        effort="xhigh",
    )

    # AGENT 2: Ingénieur de Code
    code_migre = executer_agent(
        "Ingénieur de Code",
        (
            "Tu es un Ingénieur de Code principal. À partir du code legacy et du "
            "plan de migration fourni, réécris le code dans la stack cible en "
            "respectant les standards modernes (typage, async, gestion d'erreurs)."
        ),
        f"Code obsolète:\n{code_obsolete_client}\n\nPlan de migration:\n{plan_migration}",
    )

    # AGENT 3: Expert QA & Sécurité
    code_revise = executer_agent(
        "Expert QA & Sécurité",
        (
            "Tu es un Expert en Assurance Qualité et Sécurité Web. Audite le code "
            "migré ci-dessous : identifie les vulnérabilités (OWASP Top 10), les "
            "régressions fonctionnelles potentielles, et propose les correctifs "
            "nécessaires directement dans le code."
        ),
        code_migre,
    )

    # AGENT 4: Ingénieur de Tests
    suite_tests = executer_agent(
        "Ingénieur de Tests",
        (
            "Tu es un Ingénieur de Tests. Génère une suite de tests automatisés "
            "(unitaires et d'intégration) couvrant les cas nominaux, les cas limites "
            "et les correctifs de sécurité apportés au code ci-dessous."
        ),
        code_revise,
    )

    return {
        "plan_migration": plan_migration,
        "code_migre": code_revise,
        "suite_tests": suite_tests,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python usine_migration_logicielle.py <fichier_source>")
        print("       echo '<code>' | python usine_migration_logicielle.py -")
        sys.exit(1)

    chemin = sys.argv[1]
    if chemin == "-":
        code = sys.stdin.read()
    else:
        with open(chemin, "r", encoding="utf-8") as f:
            code = f.read()

    resultats = usine_migration_logicielle(code)

    print("\n" + "=" * 60)
    print("MIGRATION TERMINÉE")
    print("=" * 60)
    print(f"\nFichiers produits :")
    print(f"  - Plan de migration : {len(resultats['plan_migration'])} caractères")
    print(f"  - Code migré        : {len(resultats['code_migre'])} caractères")
    print(f"  - Suite de tests    : {len(resultats['suite_tests'])} caractères")

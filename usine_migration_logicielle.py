import os
from anthropic import Anthropic

client = Anthropic()
MODEL_NAME = "claude-opus-4-8"


def executer_agent(system_prompt, user_content, effort="high"):
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4000,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text


def usine_migration_logicielle(code_obsolete_client):
    # AGENT 1: Architecte Analyste
    system_architecte = (
        "Tu es un Architecte Logiciel Senior, spécialiste de la modernisation "
        "de systèmes legacy. Analyse le code obsolète fourni et produis un plan "
        "de migration détaillé : technologies cibles, risques, dépendances à "
        "remplacer, et étapes de refactorisation."
    )
    plan_migration = executer_agent(
        system_architecte, code_obsolete_client, effort="xhigh"
    )

    # AGENT 2: Ingénieur de Code
    system_ingenieur_code = (
        "Tu es un Ingénieur de Code principal. À partir du code legacy et du "
        "plan de migration fourni, réécris le code dans la stack cible en "
        "respectant les standards modernes (typage, async, gestion d'erreurs)."
    )
    code_migre = executer_agent(
        system_ingenieur_code,
        f"Code obsolète:\n{code_obsolete_client}\n\nPlan de migration:\n{plan_migration}",
    )

    # AGENT 3: Expert QA & Sécurité
    system_qa_securite = (
        "Tu es un Expert en Assurance Qualité et Sécurité Web. Audite le code "
        "migré ci-dessous : identifie les vulnérabilités (OWASP Top 10), les "
        "régressions fonctionnelles potentielles, et propose les correctifs "
        "nécessaires directement dans le code."
    )
    code_revise = executer_agent(system_qa_securite, code_migre)

    # AGENT 4: Ingénieur de Tests
    system_ingenieur_tests = (
        "Tu es un Ingénieur de Tests. Génère une suite de tests automatisés "
        "(unitaires et d'intégration) couvrant les cas nominaux, les cas limites "
        "et les correctifs de sécurité apportés au code ci-dessous."
    )
    suite_tests = executer_agent(system_ingenieur_tests, code_revise)

    return {
        "plan_migration": plan_migration,
        "code_migre": code_revise,
        "suite_tests": suite_tests,
    }

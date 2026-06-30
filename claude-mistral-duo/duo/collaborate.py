"""Modes de collaboration entre Claude et Mistral."""
from __future__ import annotations

from .clients import ClaudeClient, MistralClient


def chain(claude: ClaudeClient, mistral: MistralClient, question: str) -> str:
    """CHAÎNE : Claude répond, puis Mistral reformule/prolonge sa réponse."""
    print("🤖 Claude réfléchit…")
    rep_claude = claude.ask(question)
    print(f"\n🟣 CLAUDE :\n{rep_claude}\n")

    prompt = (
        "Voici une réponse rédigée par un autre assistant :\n\n"
        f'"""\n{rep_claude}\n"""\n\n'
        "Améliore-la : corrige les imprécisions, clarifie, et ajoute un exemple concret."
    )
    print("🟠 Mistral améliore…")
    rep_mistral = mistral.ask(prompt)
    print(f"\n🟠 MISTRAL :\n{rep_mistral}\n")
    return rep_mistral


def debate(claude: ClaudeClient, mistral: MistralClient, topic: str, rounds: int = 3) -> str:
    """DÉBAT : Claude défend le POUR, Mistral le CONTRE, sur plusieurs tours."""
    sys_claude = "Tu débats en défendant le POUR. Sois concis (3-4 phrases), courtois et argumenté."
    sys_mistral = "Tu débats en défendant le CONTRE. Sois concis (3-4 phrases), courtois et argumenté."

    transcript: list[str] = []
    dernier = f"Sujet du débat : {topic}\nOuvre le débat."
    for i in range(1, rounds + 1):
        c = claude.ask(dernier, system=sys_claude)
        print(f"\n🟣 CLAUDE (tour {i}, POUR) :\n{c}")
        transcript.append(f"POUR: {c}")

        m = mistral.ask(f"Ton adversaire vient de dire :\n{c}\n\nRéponds.", system=sys_mistral)
        print(f"\n🟠 MISTRAL (tour {i}, CONTRE) :\n{m}")
        transcript.append(f"CONTRE: {m}")
        dernier = f"Ton adversaire vient de dire :\n{m}\n\nRéponds."

    # Claude joue l'arbitre neutre et conclut.
    verdict = claude.ask(
        "Voici un débat. En tant qu'arbitre NEUTRE, résume les meilleurs arguments "
        "de chaque côté et donne une conclusion équilibrée :\n\n" + "\n".join(transcript),
        system="Tu es un arbitre impartial.",
    )
    print(f"\n⚖️  VERDICT (Claude, neutre) :\n{verdict}\n")
    return verdict


def critique_refine(claude: ClaudeClient, mistral: MistralClient, task: str, rounds: int = 2) -> str:
    """CRITIQUE-RÉVISION : Claude rédige, Mistral critique, Claude révise — en boucle."""
    draft = claude.ask(task)
    print(f"\n🟣 BROUILLON (Claude) :\n{draft}\n")

    for i in range(1, rounds + 1):
        critique = mistral.ask(
            "Critique ce texte de façon constructive (points faibles + suggestions précises), "
            "sans le réécrire :\n\n" + draft,
            system="Tu es un relecteur exigeant mais bienveillant.",
        )
        print(f"\n🟠 CRITIQUE {i} (Mistral) :\n{critique}\n")

        draft = claude.ask(
            f"Voici ton texte :\n{draft}\n\nVoici une critique :\n{critique}\n\n"
            "Réécris le texte en tenant compte de la critique."
        )
        print(f"\n🟣 RÉVISION {i} (Claude) :\n{draft}\n")
    return draft


def ensemble(claude: ClaudeClient, mistral: MistralClient, question: str) -> str:
    """ENSEMBLE : les deux répondent en parallèle, puis Claude fusionne le meilleur des deux."""
    rep_claude = claude.ask(question)
    rep_mistral = mistral.ask(question)
    print(f"\n🟣 CLAUDE :\n{rep_claude}\n\n🟠 MISTRAL :\n{rep_mistral}\n")

    fusion = claude.ask(
        f"Question : {question}\n\n"
        f"Réponse A (Claude) :\n{rep_claude}\n\n"
        f"Réponse B (Mistral) :\n{rep_mistral}\n\n"
        "Fusionne le meilleur des deux en UNE réponse finale, plus complète et plus juste.",
        system="Tu es un synthétiseur qui combine deux réponses en gardant le meilleur.",
    )
    print(f"\n✅ SYNTHÈSE FINALE :\n{fusion}\n")
    return fusion

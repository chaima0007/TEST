"""
Point d'entrée — fait collaborer Claude (Anthropic) et Mistral.

Exemples :
  python main.py chain    "Explique l'apprentissage par renforcement."
  python main.py debate   "Faut-il interdire les voitures en ville ?" --rounds 3
  python main.py critique "Rédige un court paragraphe de vente pour une montre."
  python main.py ensemble "Quelles sont les causes de l'inflation ?"
"""
from __future__ import annotations

import argparse

from duo import ClaudeClient, MistralClient, load_config
from duo.collaborate import chain, critique_refine, debate, ensemble


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Claude + Mistral travaillent ensemble.")
    p.add_argument(
        "mode",
        choices=["chain", "debate", "critique", "ensemble"],
        help="chain = Claude puis Mistral · debate = débat arbitré · "
             "critique = rédige/critique/révise · ensemble = synthèse des deux",
    )
    p.add_argument("prompt", help="La question, le sujet ou la tâche.")
    p.add_argument("--rounds", type=int, default=2, help="Nombre de tours (debate/critique).")
    return p


def main() -> None:
    args = build_parser().parse_args()
    cfg = load_config()

    claude = ClaudeClient(cfg.anthropic_key, model=cfg.claude_model)
    mistral = MistralClient(cfg.mistral_key, model=cfg.mistral_model)

    print(f"🧩 Mode : {args.mode}  |  Claude={cfg.claude_model}  Mistral={cfg.mistral_model}\n")

    if args.mode == "chain":
        chain(claude, mistral, args.prompt)
    elif args.mode == "debate":
        debate(claude, mistral, args.prompt, rounds=args.rounds)
    elif args.mode == "critique":
        critique_refine(claude, mistral, args.prompt, rounds=args.rounds)
    elif args.mode == "ensemble":
        ensemble(claude, mistral, args.prompt)


if __name__ == "__main__":
    main()

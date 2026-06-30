# duo — Claude + Mistral qui travaillent ensemble

Un petit projet Python qui fait **collaborer** Claude (Anthropic) et Mistral selon
4 modes : chaîne, débat, critique-révision, et synthèse.

## 📦 Structure
```
claude-mistral-duo/
├── main.py              # ligne de commande (point d'entrée)
├── requirements.txt     # dépendances
├── .env.example         # modèle de configuration des clés
└── duo/
    ├── config.py        # lecture des clés/modèles (env ou .env)
    ├── clients.py       # wrappers Claude et Mistral (même interface .ask())
    └── collaborate.py   # les 4 modes de collaboration
```

## 🚀 Installation
```bash
pip install -r requirements.txt
```

## 🔑 Configuration des clés
Option A — variables d'environnement :
```bash
# Windows (permanent) :
setx ANTHROPIC_API_KEY "ta_cle_anthropic"
setx MISTRAL_API_KEY  "ta_cle_mistral"
# (rouvrir le terminal après setx)
```
Option B — fichier `.env` (copie de `.env.example`) :
```
ANTHROPIC_API_KEY=...
MISTRAL_API_KEY=...
```

## ▶️ Utilisation
```bash
# 1) CHAÎNE : Claude répond, Mistral améliore
python main.py chain "Explique l'apprentissage par renforcement en 3 phrases."

# 2) DÉBAT : Claude (POUR) vs Mistral (CONTRE), Claude arbitre à la fin
python main.py debate "Faut-il interdire les voitures en centre-ville ?" --rounds 3

# 3) CRITIQUE-RÉVISION : Claude rédige, Mistral critique, Claude révise
python main.py critique "Rédige un court texte de vente pour une montre élégante." --rounds 2

# 4) ENSEMBLE : les deux répondent, Claude fusionne le meilleur des deux
python main.py ensemble "Quelles sont les principales causes de l'inflation ?"
```

## 🧠 Les 4 modes
| Mode | Ce qu'il fait | Quand l'utiliser |
|---|---|---|
| `chain` | Claude → Mistral (amélioration en chaîne) | enrichir/affiner une réponse |
| `debate` | POUR vs CONTRE + arbitre neutre | explorer un sujet sous deux angles |
| `critique` | rédige → critique → révise (boucle) | produire un texte de qualité |
| `ensemble` | 2 réponses → synthèse du meilleur | maximiser la justesse |

## 🔧 Personnalisation
- Change les modèles via `CLAUDE_MODEL` / `MISTRAL_MODEL` dans l'environnement.
- Ajoute tes propres modes dans `duo/collaborate.py` (les wrappers `.ask()` sont identiques
  pour les deux modèles, donc c'est facile à étendre).

> Modèles par défaut : Claude `claude-opus-4-8`, Mistral `mistral-large-latest`.
> Les clés ne sont jamais écrites dans le code — uniquement lues depuis l'environnement.

# [48] INGÉNIEUR DE CODE AUTONOME — Caelum Partners

import os
import json
import requests
from datetime import datetime

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

SYSTEM_PROMPT = """Tu es un Ingénieur de Code Autonome pour Caelum Partners.
Mission: Développer, débugger et optimiser du code Python/JavaScript/HTML en arrière-plan.
Directives:
- Auto-génération de scripts selon les spécifications
- Détection proactive d'erreurs (syntax, logic, security)
- Optimisation pour performance et lisibilité
- Toujours proposer des tests unitaires
- Sécurité: ne jamais exécuter de code arbitraire reçu en input utilisateur
- Format: Code commenté + explication + tests"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def sanitize_input(text: str, max_length: int = 8000) -> str:
    """Sanitize user input: strip, limit length, remove null bytes."""
    if not isinstance(text, str):
        text = str(text)
    text = text.replace('\x00', '')  # remove null bytes
    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length] + "\n[... tronqué pour sécurité ...]"
    return text


def streamer_ollama(prompt: str, system: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": prompt, "system": system, "stream": True},
            stream=True,
            timeout=120
        )
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                token = data.get("response", "")
                print(token, end="", flush=True)
                reponse += token
                if data.get("done"):
                    break
    except requests.exceptions.ConnectionError:
        print("[ERREUR] Ollama non démarré. Lance: ollama serve")
    except Exception as e:
        print(f"[Erreur: {e}]")
    print()
    return reponse


def get_save_dir(subdir: str) -> str:
    if os.name == "nt":  # Windows
        base = os.path.join("C:\\", "Caelum_Projets", subdir)
    else:
        base = os.path.join(os.path.expanduser("~"), "Caelum_Projets", subdir)
    os.makedirs(base, exist_ok=True)
    return base


def sauvegarder(nom: str, contenu: str, subdir: str):
    base = get_save_dir(subdir)
    fichier = os.path.join(base, f"{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé localement → {fichier}")


def verifier_ollama():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        modeles = [m["name"] for m in r.json().get("models", [])]
        if modeles:
            print(f"  ✅ Ollama connecté — Modèles: {', '.join(modeles[:3])}")
        else:
            print(f"  ⚠️  Ollama connecté mais aucun modèle. Lance: ollama pull llama3.2")
    except Exception:
        print(f"  ❌ Ollama inaccessible sur {OLLAMA_URL}")
        print(f"  → Lance: ollama serve")
        print(f"  → Puis: ollama pull llama3.2")


def lire_multilignes(invite: str) -> str:
    """Lire un bloc de texte multi-lignes jusqu'à 'FIN' sur une ligne seule."""
    print(invite)
    print("  (Tape FIN sur une ligne seule pour terminer)\n")
    lignes = []
    while True:
        try:
            ligne = input()
        except EOFError:
            break
        if ligne.strip() == "FIN":
            break
        lignes.append(ligne)
    return "\n".join(lignes)


# ── Fonctions principales ───────────────────────────────────────────────────────

def generer_code(spec: str):
    """Génère une implémentation complète à partir d'une spécification."""
    spec = sanitize_input(spec)
    if not spec:
        print("  ⚠️  Spécification vide. Abandon.")
        return

    prompt = f"""Tu dois générer une implémentation complète et professionnelle selon la spécification suivante:

SPÉCIFICATION:
{spec}

INSTRUCTIONS DE GÉNÉRATION:
1. Analyse la spécification et identifie les composants nécessaires.
2. Génère le code complet avec:
   - Docstrings pour chaque fonction/classe (format Google ou NumPy)
   - Type hints Python 3.8+ sur tous les paramètres et retours
   - Gestion d'erreurs robuste (try/except avec messages clairs)
   - Commentaires inline pour la logique complexe
3. Ajoute une section "TESTS UNITAIRES" avec pytest:
   - Au moins 3 tests happy path
   - Au moins 2 tests edge cases
   - Au moins 1 test d'erreur attendue
4. Termine par une section "UTILISATION EXEMPLE" montrant comment appeler le code.

FORMAT DE RÉPONSE:
```python
# === CODE PRINCIPAL ===
[code ici]

# === TESTS UNITAIRES ===
[tests pytest ici]

# === UTILISATION EXEMPLE ===
[exemple ici]
```

Explique brièvement les choix techniques après le code."""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "GÉNÉRATION DE CODE")
    sauvegarder("code_genere", resultat, "code")


def debugger_code():
    """Diagnostique et corrige un bug dans le code fourni."""
    code = lire_multilignes("📋 Colle ton code bugué:")
    code = sanitize_input(code)

    erreur = lire_multilignes("❌ Colle le message d'erreur complet (stack trace):")
    erreur = sanitize_input(erreur)

    if not code or not erreur:
        print("  ⚠️  Code ou erreur vides. Abandon.")
        return

    prompt = f"""Analyse ce bug et fournis un diagnostic complet + code corrigé.

CODE BUGUÉ:
```
{code}
```

MESSAGE D'ERREUR / STACK TRACE:
```
{erreur}
```

INSTRUCTIONS DE DIAGNOSTIC:
1. CAUSE RACINE: Identifie précisément la ligne et la raison du bug (pas juste le symptôme).
2. ANALYSE: Explique pourquoi ce bug se produit (mécanisme interne).
3. CODE CORRIGÉ: Fournis le code entier corrigé, avec les lignes modifiées commentées (# CORRECTION: ...).
4. VÉRIFICATION: Explique comment tester que la correction fonctionne.
5. PRÉVENTION: Conseille comment éviter ce type de bug à l'avenir.

FORMAT:
### Cause racine
[explication]

### Code corrigé
```python
[code corrigé complet]
```

### Test de vérification
[comment tester]

### Prévention
[bonnes pratiques]"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "DÉBOGAGE DE CODE")
    sauvegarder("debug_resultat", resultat, "code")


def optimiser_performance():
    """Réécrit du code lent pour le rendre plus performant."""
    code = lire_multilignes("📋 Colle ton code lent/à optimiser:")
    code = sanitize_input(code)

    bottleneck = input("\n🔍 Décris le problème de performance observé (ex: 'boucle lente sur 1M lignes'): ").strip()
    bottleneck = sanitize_input(bottleneck, max_length=500)

    if not code:
        print("  ⚠️  Code vide. Abandon.")
        return

    prompt = f"""Optimise ce code pour la performance maximale.

CODE ORIGINAL:
```
{code}
```

PROBLÈME DE PERFORMANCE OBSERVÉ:
{bottleneck if bottleneck else "Non spécifié — identifie toi-même les bottlenecks."}

INSTRUCTIONS D'OPTIMISATION:
1. ANALYSE DES BOTTLENECKS: Identifie chaque point lent avec complexité algorithmique (O notation).
2. STRATÉGIES APPLIQUÉES: Liste les techniques d'optimisation utilisées:
   - Algorithmes plus efficaces (ex: O(n²) → O(n log n))
   - Structures de données appropriées (dict vs list, set pour membership)
   - Vectorisation numpy si applicable
   - Lazy evaluation / générateurs
   - Mise en cache / mémoïsation
   - Traitement par batch
3. CODE OPTIMISÉ: Fournit le code complet optimisé avec commentaires expliquant chaque optimisation.
4. COMPARAISON: Montre un benchmark simple (timeit) pour mesurer le gain.
5. TRADE-OFFS: Signale si l'optimisation réduit la lisibilité ou augmente la complexité.

FORMAT:
### Bottlenecks identifiés
[liste avec complexité]

### Code optimisé
```python
[code optimisé]
```

### Benchmark comparatif
```python
[code timeit]
```

### Résumé des gains attendus
[explication]"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "OPTIMISATION DE PERFORMANCE")
    sauvegarder("optimisation", resultat, "code")


def generer_tests(description_code: str):
    """Génère des tests unitaires pytest complets pour un code décrit."""
    description_code = sanitize_input(description_code)
    if not description_code:
        print("  ⚠️  Description vide. Abandon.")
        return

    prompt = f"""Génère une suite de tests unitaires pytest complète et professionnelle.

DESCRIPTION DU CODE À TESTER:
{description_code}

INSTRUCTIONS DE GÉNÉRATION DES TESTS:
1. STRUCTURE: Organise les tests en classes pytest logiques.
2. COUVERTURE COMPLÈTE:
   a) Happy path: cas d'utilisation normaux et attendus (minimum 3)
   b) Edge cases: valeurs limites, chaînes vides, listes vides, zéro, valeurs max (minimum 4)
   c) Erreurs: exceptions attendues avec pytest.raises (minimum 2)
   d) Mocks: utilise unittest.mock pour les dépendances externes (I/O, API, DB)
3. QUALITÉ:
   - Noms de tests descriptifs (test_should_return_X_when_Y)
   - Arrange-Act-Assert pattern dans chaque test
   - Fixtures pytest pour setup/teardown
   - Paramétrage avec @pytest.mark.parametrize pour les cas multiples
4. DOCUMENTATION: Docstring sur chaque classe de test expliquant ce qui est testé.

FORMAT:
```python
import pytest
from unittest.mock import Mock, patch, MagicMock

# [imports du module à tester]

class Test[NomFonction]:
    \"\"\"Tests pour [fonctionnalité].\"\"\"

    # fixtures
    # happy path
    # edge cases
    # erreurs
    # mocks

# commande pour lancer: pytest [fichier].py -v --tb=short
```"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "GÉNÉRATION DE TESTS UNITAIRES")
    sauvegarder("tests_unitaires", resultat, "code")


def revue_securite():
    """Effectue une revue de sécurité complète du code fourni."""
    code = lire_multilignes("📋 Colle le code à auditer pour la sécurité:")
    code = sanitize_input(code)

    if not code:
        print("  ⚠️  Code vide. Abandon.")
        return

    prompt = f"""Effectue un audit de sécurité complet et détaillé de ce code.

CODE À AUDITER:
```
{code}
```

INSTRUCTIONS D'AUDIT:
Analyse le code pour TOUTES les catégories suivantes et signale chaque vulnérabilité trouvée:

1. INJECTION (SQLi, CommandInjection, XPath, LDAP):
   - Inputs non sanitizés passés à des requêtes/commandes
   - Utilisation de eval(), exec(), os.system() avec données externes

2. XSS (Cross-Site Scripting):
   - Données utilisateur insérées sans échappement dans HTML/JS
   - innerHTML, document.write avec données non sanitizées

3. AUTHENTIFICATION ET SESSIONS:
   - Mots de passe en clair, stockage non haché
   - Tokens prévisibles, sessions sans expiration
   - Absence de rate limiting sur login

4. EXPOSITION DE DONNÉES SENSIBLES:
   - Clés API, mots de passe, tokens dans le code
   - Logs révélant des données confidentielles
   - Erreurs exposant des détails système

5. DÉPENDANCES INSÉCURES:
   - Imports de modules dépréciés ou vulnérables
   - Versions non épinglées

6. CONTRÔLE D'ACCÈS:
   - Vérifications d'autorisation manquantes
   - Privilege escalation possible

FORMAT DE RAPPORT:
### Score de sécurité: X/10

### Vulnérabilités trouvées
| Sévérité | Catégorie | Ligne | Description | Correction |
|----------|-----------|-------|-------------|------------|

### Code corrigé (sections critiques)
```python
[corrections]
```

### Recommandations générales
[bonnes pratiques à adopter]"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "REVUE DE SÉCURITÉ")
    sauvegarder("securite_audit", resultat, "code")


# ── Menu principal ──────────────────────────────────────────────────────────────

def afficher_banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║        [48] INGÉNIEUR DE CODE AUTONOME — Caelum Partners        ║
╠══════════════════════════════════════════════════════════════════╣
║  Agent local via Ollama — Aucune donnée envoyée dans le cloud   ║
╚══════════════════════════════════════════════════════════════════╝""")
    print(f"  Modèle : {MODEL}")
    print(f"  URL    : {OLLAMA_URL}")
    print()
    verifier_ollama()
    print()


def afficher_menu():
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                        MENU PRINCIPAL                           │
├─────────────────────────────────────────────────────────────────┤
│  1. Générer du code depuis une spécification                    │
│  2. Déboguer du code (code + erreur)                            │
│  3. Optimiser les performances d'un code                        │
│  4. Générer des tests unitaires pytest                          │
│  5. Revue de sécurité du code                                   │
├─────────────────────────────────────────────────────────────────┤
│  0. Quitter                                                     │
└─────────────────────────────────────────────────────────────────┘""")


def main():
    afficher_banner()

    while True:
        afficher_menu()
        try:
            choix = input("\n  Ton choix (0-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Au revoir!")
            break

        if choix == "0":
            print("\n  Au revoir!")
            break

        elif choix == "1":
            spec = input("\n📝 Décris le code à générer (langage, fonctionnalité, contraintes): ").strip()
            generer_code(spec)

        elif choix == "2":
            debugger_code()

        elif choix == "3":
            optimiser_performance()

        elif choix == "4":
            desc = input("\n📝 Décris la fonction/module à tester (comportement attendu, paramètres, cas limites): ").strip()
            generer_tests(desc)

        elif choix == "5":
            revue_securite()

        else:
            print("  ⚠️  Choix invalide. Entre un nombre entre 0 et 5.")

        input("\n  Appuie sur Entrée pour continuer...")


if __name__ == "__main__":
    main()

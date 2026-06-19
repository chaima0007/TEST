# [49] TESTEUR DE SIMULATION (QA) — Caelum Partners

import os
import json
import requests
from datetime import datetime

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

SYSTEM_PROMPT = """Tu es un Expert QA (Quality Assurance) pour Caelum Partners.
Mission: Exécuter des tests en boucle, analyser les bugs, et appliquer des correctifs.
Directives:
- Générer des cas de test exhaustifs (happy path, edge cases, erreurs)
- Analyser les logs d'erreurs et identifier la cause racine
- Proposer des correctifs précis et testables
- Créer des rapports de test structurés
- Prioritiser les bugs par criticité (P0 critique → P3 mineur)
- Sécurité: tester les vulnérabilités OWASP Top 10"""


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

def generer_plan_test(fonctionnalite: str):
    """Génère un plan de test complet pour une fonctionnalité donnée."""
    fonctionnalite = sanitize_input(fonctionnalite)
    if not fonctionnalite:
        print("  ⚠️  Description de fonctionnalité vide. Abandon.")
        return

    prompt = f"""Génère un plan de test complet et professionnel pour la fonctionnalité suivante:

FONCTIONNALITÉ À TESTER:
{fonctionnalite}

INSTRUCTIONS DE GÉNÉRATION DU PLAN DE TEST:
1. OBJECTIFS DU TEST:
   - Définir ce qui doit être vérifié et pourquoi
   - Critères de succès mesurables
   - Risques couverts par les tests

2. PÉRIMÈTRE (SCOPE):
   - Fonctionnalités incluses dans le test
   - Fonctionnalités hors périmètre (out of scope)
   - Dépendances et prérequis

3. TYPES DE TESTS À EFFECTUER:
   a) Tests unitaires: fonctions/méthodes isolées
   b) Tests d'intégration: interactions entre composants
   c) Tests end-to-end (E2E): parcours utilisateur complets
   d) Tests de performance: temps de réponse, charge, stress
   e) Tests de sécurité: OWASP Top 10 applicable à cette fonctionnalité

4. CAS DE TEST DÉTAILLÉS:
   Pour chaque type de test, liste les cas avec:
   - ID du cas (TC-001, TC-002, ...)
   - Description
   - Données d'entrée
   - Étapes d'exécution
   - Résultat attendu
   - Criticité (P0/P1/P2/P3)

5. CRITÈRES D'ACCEPTATION:
   - Définition of Done (DoD) pour cette fonctionnalité
   - Seuils de performance acceptables
   - Taux de couverture minimum requis

FORMAT:
# Plan de Test — [Fonctionnalité]
## 1. Objectifs
## 2. Périmètre
## 3. Types de tests
## 4. Cas de test
| ID | Description | Données | Étapes | Résultat attendu | Criticité |
## 5. Critères d'acceptation"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "GÉNÉRATION DU PLAN DE TEST")
    sauvegarder("plan_test", resultat, "qa")


def analyser_log_erreur():
    """Analyse un log d'erreur ou stack trace pour identifier la cause racine."""
    log = lire_multilignes("📋 Colle le log d'erreur complet / stack trace:")
    log = sanitize_input(log)

    if not log:
        print("  ⚠️  Log vide. Abandon.")
        return

    prompt = f"""Analyse ce log d'erreur et fournis un diagnostic complet.

LOG D'ERREUR / STACK TRACE:
```
{log}
```

INSTRUCTIONS D'ANALYSE:
1. IDENTIFICATION RAPIDE:
   - Type d'erreur (exception, timeout, assertion, etc.)
   - Langage/framework concerné
   - Environnement probable (dev/staging/prod)

2. CAUSE RACINE (Root Cause Analysis):
   - Ligne/fichier précis où l'erreur se produit
   - Pourquoi cette erreur se produit (mécanisme)
   - Enchaînement d'appels menant à l'erreur (call chain)
   - Distinguer: symptôme vs cause réelle

3. COMPOSANT AFFECTÉ:
   - Module/service impacté
   - Autres composants potentiellement touchés (blast radius)
   - Impact utilisateur estimé

4. CORRECTIF SUGGÉRÉ:
   - Solution immédiate (quick fix)
   - Solution pérenne (long-term fix)
   - Exemple de code corrigé si applicable

5. PRÉVENTION:
   - Comment détecter ce problème plus tôt (monitoring, alertes)
   - Tests à ajouter pour prévenir la régression
   - Bonnes pratiques à adopter

FORMAT:
### Diagnostic rapide
[type erreur + localisation]

### Cause racine
[analyse détaillée]

### Composant affecté
[impact]

### Correctif
```
[code ou configuration]
```

### Plan de prévention
[actions concrètes]"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "ANALYSE DU LOG D'ERREUR")
    sauvegarder("analyse_log", resultat, "qa")


def creer_cas_test_edge():
    """Génère des cas de test aux limites et cas extrêmes pour une fonctionnalité."""
    description = lire_multilignes("📋 Décris la fonction/fonctionnalité pour laquelle créer des edge cases:")
    description = sanitize_input(description)

    if not description:
        print("  ⚠️  Description vide. Abandon.")
        return

    prompt = f"""Génère une liste exhaustive de cas de test aux limites (edge cases) pour:

FONCTION/FONCTIONNALITÉ:
{description}

INSTRUCTIONS DE GÉNÉRATION DES EDGE CASES:
Couvre TOUTES les catégories suivantes de manière exhaustive:

1. VALEURS LIMITES (Boundary Values):
   - Valeur minimale exacte
   - Valeur minimale - 1 (en dessous du minimum)
   - Valeur maximale exacte
   - Valeur maximale + 1 (au dessus du maximum)
   - Zéro (si numérique)
   - Valeurs négatives (si applicable)

2. INPUTS NULS ET VIDES:
   - None / null
   - Chaîne vide ""
   - Liste vide []
   - Dictionnaire vide {{}}
   - Zéro vs None (différence sémantique)

3. TYPES INATTENDUS:
   - Mauvais type (str où int attendu, etc.)
   - Float où int attendu
   - Très grand entier (overflow)
   - Caractères spéciaux et Unicode (émojis, accents, RTL)
   - Caractères de contrôle (\\n, \\t, \\x00)

4. INPUTS MALVEILLANTS (Sécurité):
   - Injection SQL: ' OR '1'='1
   - Injection script: <script>alert(1)</script>
   - Path traversal: ../../etc/passwd
   - Très longue chaîne (DoS par longueur)
   - JSON malformé

5. CONCURRENCE ET TIMING:
   - Appels simultanés (race conditions)
   - Timeout (opération très lente)
   - Retry sur échec

6. DONNÉES MÉTIER SPÉCIFIQUES:
   - Données cohérentes mais sémantiquement invalides
   - Doublons
   - Données manquantes (champs optionnels absents)

FORMAT:
```python
import pytest

@pytest.mark.parametrize("input_val, expected", [
    # === VALEURS LIMITES ===
    (cas_1, résultat_1),  # description du cas
    ...

    # === INPUTS NULS ===
    ...

    # === TYPES INATTENDUS ===
    ...

    # === SÉCURITÉ ===
    ...
])
def test_edge_cases(input_val, expected):
    # implémentation
    pass
```

Ajoute des commentaires expliquant pourquoi chaque edge case est important."""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "GÉNÉRATION DES EDGE CASES")
    sauvegarder("edge_cases", resultat, "qa")


def rapport_bug(description_bug: str):
    """Formate un rapport de bug structuré et professionnel."""
    description_bug = sanitize_input(description_bug)
    if not description_bug:
        print("  ⚠️  Description du bug vide. Abandon.")
        return

    prompt = f"""Rédige un rapport de bug structuré et professionnel basé sur cette description:

DESCRIPTION DU BUG:
{description_bug}

INSTRUCTIONS DE RÉDACTION:
Génère un rapport de bug complet selon le standard suivant:

1. TITRE: Une phrase concise décrivant le bug (max 80 caractères)
   Format: [Composant] Comportement incorrect dans [contexte]

2. SÉVÉRITÉ ET PRIORITÉ:
   Attribue une priorité parmi:
   - P0 CRITIQUE: Application inutilisable, perte de données, faille de sécurité
   - P1 MAJEUR: Fonctionnalité clé cassée, workaround difficile
   - P2 MOYEN: Fonctionnalité dégradée, workaround disponible
   - P3 MINEUR: Cosmétique, inconvénient mineur
   Justifie ton choix.

3. ENVIRONNEMENT:
   - OS et version
   - Navigateur/Runtime et version
   - Version de l'application
   - Données de test utilisées

4. ÉTAPES DE REPRODUCTION:
   Liste numérotée précise pour reproduire le bug à coup sûr.
   Chaque étape doit être atomique et vérifiable.

5. COMPORTEMENT ATTENDU:
   Ce qui devrait se passer selon les specs.

6. COMPORTEMENT ACTUEL:
   Ce qui se passe réellement (avec messages d'erreur exacts si disponibles).

7. IMPACT UTILISATEUR:
   Qui est affecté? Combien d'utilisateurs? Quel workflow est bloqué?

8. CORRECTIF PROPOSÉ:
   Hypothèse technique sur la cause et solution suggérée (si identifiable).

9. FICHIERS/COMPOSANTS CONCERNÉS:
   Liste les fichiers ou modules probablement impliqués.

FORMAT FINAL:
# BUG REPORT — [TITRE]
**Priorité:** P[X] [NIVEAU]
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## Environnement
## Étapes de reproduction
## Comportement attendu vs actuel
## Impact
## Correctif proposé
## Composants concernés"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "RAPPORT DE BUG")
    sauvegarder("rapport_bug", resultat, "qa")


def audit_qualite_code():
    """Évalue la qualité globale d'un code soumis."""
    code = lire_multilignes("📋 Colle le code à auditer pour la qualité:")
    code = sanitize_input(code)

    if not code:
        print("  ⚠️  Code vide. Abandon.")
        return

    prompt = f"""Effectue un audit de qualité complet et objectif de ce code.

CODE À AUDITER:
```
{code}
```

INSTRUCTIONS D'AUDIT QUALITÉ:
Évalue le code sur TOUTES les dimensions suivantes avec un score /10 et des justifications:

1. LISIBILITÉ (score /10):
   - Nommage des variables/fonctions/classes (expressif et cohérent?)
   - Longueur des fonctions (Single Responsibility Principle?)
   - Complexité cyclomatique (trop d'imbrications if/for/while?)
   - Commentaires (présents, utiles, non redondants?)
   - Formatage et style cohérent?

2. MAINTENABILITÉ (score /10):
   - DRY (Don't Repeat Yourself): duplication de code?
   - SOLID principles respectés?
   - Couplage faible / cohésion forte?
   - Facilité à modifier sans casser autre chose?
   - Gestion de configuration (pas de magic numbers?)

3. COUVERTURE DE TESTS ESTIMÉE (score /10):
   - Tests unitaires présents?
   - Tests d'intégration?
   - Couverture des edge cases?
   - Testabilité du code (injection de dépendances?)

4. SÉCURITÉ (score /10):
   - Validation des inputs?
   - Pas de secrets hardcodés?
   - Gestion sécurisée des erreurs?
   - Logging approprié?

5. DETTE TECHNIQUE (score /10, 10 = dette nulle):
   - Code obsolète ou déprécié?
   - TODOs/FIXMEs non résolus?
   - Abstractions manquantes?
   - Scalabilité du design?

FORMAT:
## Score Global: [X]/10

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Lisibilité | X/10 | ... |
| Maintenabilité | X/10 | ... |
| Tests | X/10 | ... |
| Sécurité | X/10 | ... |
| Dette technique | X/10 | ... |

## Points forts
[liste]

## Améliorations prioritaires (par ordre d'impact)
1. [action concrète + exemple de code corrigé]
2. ...

## Refactoring suggéré
```python
[exemple de code amélioré pour les parties les plus critiques]
```"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "AUDIT QUALITÉ DU CODE")
    sauvegarder("audit_qualite", resultat, "qa")


# ── Menu principal ──────────────────────────────────────────────────────────────

def afficher_banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║        [49] TESTEUR DE SIMULATION (QA) — Caelum Partners        ║
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
│  1. Générer un plan de test complet                             │
│  2. Analyser un log d'erreur / stack trace                      │
│  3. Créer des cas de test aux limites (edge cases)              │
│  4. Rédiger un rapport de bug structuré                         │
│  5. Audit qualité du code                                       │
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
            fonctionnalite = input("\n📝 Décris la fonctionnalité à tester (contexte, inputs/outputs attendus): ").strip()
            generer_plan_test(fonctionnalite)

        elif choix == "2":
            analyser_log_erreur()

        elif choix == "3":
            creer_cas_test_edge()

        elif choix == "4":
            desc = input("\n🐛 Décris le bug observé (comportement actuel vs attendu, contexte): ").strip()
            rapport_bug(desc)

        elif choix == "5":
            audit_qualite_code()

        else:
            print("  ⚠️  Choix invalide. Entre un nombre entre 0 et 5.")

        input("\n  Appuie sur Entrée pour continuer...")


if __name__ == "__main__":
    main()

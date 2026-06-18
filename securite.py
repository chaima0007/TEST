"""
SUITE SECURITE ENTREPRISE — Agents de Protection des Données
Propulsé par Google Gemini (gratuit)
Usage : python securite.py [fichier_a_auditer.py]
"""

import os
import sys
import re
import json
import subprocess
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Clé API manquante.")
    print("  set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# ─── Patterns de secrets à ne JAMAIS laisser dans le code ───
PATTERNS_SECRETS = {
    "Clé API Google":      r"AIza[0-9A-Za-z\-_]{35}",
    "Clé API Anthropic":   r"sk-ant-[a-zA-Z0-9\-_]{40,}",
    "Clé API OpenAI":      r"sk-[a-zA-Z0-9]{48}",
    "Token GitHub":        r"ghp_[a-zA-Z0-9]{36}",
    "Token GitHub (OAuth)":r"gho_[a-zA-Z0-9]{36}",
    "Mot de passe brut":   r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{4,}['\"]",
    "Connexion DB":        r"(?i)(mysql|postgresql|mongodb|sqlite)://[^\s\"']+",
    "Clé AWS":             r"AKIA[0-9A-Z]{16}",
    "Email exposé":        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    "IP privée exposée":   r"\b(192\.168|10\.\d+|172\.(1[6-9]|2\d|3[01]))\.\d+\.\d+\b",
}

VULNERABILITES_CODE = [
    (r"eval\s*\(",                    "Exécution de code dynamique (eval) — dangereux"),
    (r"exec\s*\(",                    "Exécution shell (exec) — risque injection"),
    (r"os\.system\s*\(",             "os.system — risque injection commande"),
    (r"subprocess\.call\s*\(",       "subprocess sans liste — risque injection"),
    (r"pickle\.loads?\s*\(",         "Désérialisation pickle — risque exécution code"),
    (r"SELECT.+\+.+",               "Possible injection SQL (concaténation)"),
    (r"md5|sha1",                    "Hash faible (MD5/SHA1) — utiliser bcrypt/SHA256"),
    (r"http://",                     "Connexion non chiffrée (HTTP) — utiliser HTTPS"),
    (r"verify\s*=\s*False",         "SSL désactivé — risque man-in-the-middle"),
    (r"debug\s*=\s*True",           "Mode debug activé — ne pas déployer en prod"),
    (r"SECRET_KEY\s*=\s*['\"][^'\"]{1,20}['\"]", "Clé secrète trop courte"),
    (r"ALLOWED_HOSTS\s*=\s*\[.*\*", "ALLOWED_HOSTS ouvert à tout le monde"),
]


def creer_agent_ia(instructions):
    return genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=genai.GenerationConfig(temperature=0.2, max_output_tokens=2048),
    )


def afficher_titre(titre):
    print(f"\n{'═'*60}")
    print(f"  {titre}")
    print(f"{'═'*60}")


# ─────────────────────────────────────────────────────────────
# AGENT 1 : DÉTECTEUR DE SECRETS ET FUITES DE DONNÉES
# ─────────────────────────────────────────────────────────────

def agent_detecteur_secrets(contenu, nom_fichier):
    afficher_titre("AGENT 1 — Détecteur de Secrets & Fuites")
    alertes = []

    for nom, pattern in PATTERNS_SECRETS.items():
        matches = re.findall(pattern, contenu)
        if matches:
            # Masquer partiellement pour ne pas exposer
            masques = [m[:6] + "***" + m[-4:] if len(m) > 10 else "***" for m in matches]
            alertes.append({"type": nom, "occurrences": len(matches), "apercu": masques[0]})
            print(f"  ⚠️  {nom} détecté ({len(matches)} fois) — {masques[0]}")

    if not alertes:
        print("  ✅ Aucun secret détecté dans ce fichier.")

    return alertes


# ─────────────────────────────────────────────────────────────
# AGENT 2 : SCANNER DE VULNÉRABILITÉS CODE
# ─────────────────────────────────────────────────────────────

def agent_scanner_vulnerabilites(contenu):
    afficher_titre("AGENT 2 — Scanner de Vulnérabilités (OWASP)")
    trouvees = []

    for pattern, description in VULNERABILITES_CODE:
        lignes = []
        for i, ligne in enumerate(contenu.split("\n"), 1):
            if re.search(pattern, ligne, re.IGNORECASE):
                lignes.append(i)
        if lignes:
            trouvees.append({"description": description, "lignes": lignes})
            print(f"  ⚠️  Ligne {lignes} — {description}")

    if not trouvees:
        print("  ✅ Aucune vulnérabilité évidente détectée.")

    return trouvees


# ─────────────────────────────────────────────────────────────
# AGENT 3 : AUDIT IA APPROFONDI
# ─────────────────────────────────────────────────────────────

def agent_audit_ia(contenu, secrets, vulns):
    afficher_titre("AGENT 3 — Audit IA Approfondi")

    agent = creer_agent_ia("""Tu es un Expert en Cybersécurité senior (OWASP, RGPD, ISO 27001).
Analyse le code et le rapport de vulnérabilités fourni.
Produis un rapport structuré avec :
1. NIVEAU DE RISQUE GLOBAL (Critique/Élevé/Moyen/Faible)
2. TOP 3 des risques les plus dangereux
3. Correctifs prioritaires avec exemples de code sécurisé
4. Recommandations RGPD si des données personnelles sont exposées
Sois direct et précis. Pas de blabla.""")

    prompt = f"""Code à auditer :
{contenu[:3000]}

Secrets détectés : {json.dumps(secrets, ensure_ascii=False)}
Vulnérabilités : {json.dumps(vulns, ensure_ascii=False)}

Produis le rapport de sécurité."""

    print()
    reponse = ""
    try:
        stream = agent.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"Erreur agent IA : {e}")
    print()
    return reponse


# ─────────────────────────────────────────────────────────────
# AGENT 4 : CORRECTEUR AUTOMATIQUE
# ─────────────────────────────────────────────────────────────

def agent_correcteur(contenu, rapport):
    afficher_titre("AGENT 4 — Correcteur Automatique de Sécurité")

    agent = creer_agent_ia("""Tu es un Ingénieur Sécurité.
Réécris le code fourni en corrigeant TOUTES les vulnérabilités identifiées.
Règles absolues :
- Remplace les concaténations SQL par des requêtes paramétrées
- Remplace MD5/SHA1 par bcrypt ou hashlib.sha256
- Supprime eval(), exec(), os.system()
- Remplace HTTP par HTTPS
- Ajoute validation des entrées utilisateur
- Retourne UNIQUEMENT le code corrigé, prêt à l'emploi.""")

    prompt = f"""Code original à corriger :
{contenu}

Rapport de sécurité :
{rapport[:1000]}

Retourne le code entièrement corrigé et sécurisé."""

    print()
    code_corrige = ""
    try:
        stream = agent.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                code_corrige += chunk.text
    except Exception as e:
        print(f"Erreur : {e}")
    print()
    return code_corrige


# ─────────────────────────────────────────────────────────────
# AGENT 5 : GÉNÉRATEUR DE RAPPORT FINAL
# ─────────────────────────────────────────────────────────────

def agent_rapport_final(nom_fichier, secrets, vulns, rapport_ia, code_corrige):
    afficher_titre("AGENT 5 — Rapport Final de Sécurité")

    score = 100
    score -= len(secrets) * 20
    score -= len(vulns) * 10
    score = max(0, score)

    niveau = "CRITIQUE" if score < 30 else "ÉLEVÉ" if score < 50 else "MOYEN" if score < 70 else "BON"
    couleur = "🔴" if score < 30 else "🟠" if score < 50 else "🟡" if score < 70 else "🟢"

    rapport = f"""
{'='*60}
RAPPORT DE SÉCURITÉ — {nom_fichier}
{'='*60}
Score de sécurité : {couleur} {score}/100 ({niveau})

Secrets détectés     : {len(secrets)}
Vulnérabilités code  : {len(vulns)}

ANALYSE IA :
{rapport_ia[:500]}...

RECOMMANDATION : {'Corriger immédiatement avant tout déploiement.' if score < 50 else 'Corriger les points signalés avant mise en production.'}
{'='*60}
"""
    print(rapport)

    # Sauvegarde
    base = os.path.splitext(nom_fichier)[0]
    with open(f"{base}_rapport_securite.txt", "w", encoding="utf-8") as f:
        f.write(rapport + "\n\nANALYSE COMPLÈTE :\n" + rapport_ia)

    if code_corrige:
        with open(f"{base}_securise.py", "w", encoding="utf-8") as f:
            f.write(code_corrige)
        print(f"  ✅ Code sécurisé sauvegardé → {base}_securise.py")

    print(f"  ✅ Rapport sauvegardé → {base}_rapport_securite.txt")


# ─────────────────────────────────────────────────────────────
# LANCEMENT
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage : python securite.py <fichier.py>")
        print("Exemple : python securite.py legacy_app.py")
        sys.exit(1)

    fichier = sys.argv[1]
    if not os.path.exists(fichier):
        print(f"Fichier introuvable : {fichier}")
        sys.exit(1)

    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    print(f"\n🔒 SUITE SÉCURITÉ ENTREPRISE")
    print(f"   Analyse de : {fichier} ({len(contenu)} caractères)\n")

    secrets   = agent_detecteur_secrets(contenu, fichier)
    vulns     = agent_scanner_vulnerabilites(contenu)
    rapport   = agent_audit_ia(contenu, secrets, vulns)
    code_sec  = agent_correcteur(contenu, rapport)
    agent_rapport_final(fichier, secrets, vulns, rapport, code_sec)

"""
AGENT FANTÔME — Audit silencieux, zéro trace
Inspecte les fichiers sensibles, détecte les anomalies,
vérifie l'intégrité du système. Ne laisse aucun fichier résiduel.

Usage : python agent_fantome.py
"""

import os
import sys
import json
import re
import hashlib
import tempfile
import shutil
from datetime import datetime
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

# ─── Patterns de détection ───────────────────────────────────
PATTERNS_SECRETS = [
    (r'(?i)(api[_-]?key|secret|password|passwd|token|pwd)\s*[=:]\s*["\']?[\w\-]{8,}', "SECRET"),
    (r'AIza[0-9A-Za-z\-_]{35}',         "CLE_GOOGLE"),
    (r'sk-[a-zA-Z0-9]{32,}',            "CLE_OPENAI"),
    (r'ghp_[a-zA-Z0-9]{36}',            "TOKEN_GITHUB"),
    (r'\b[A-Z0-9]{20}\b',               "AWS_KEY_CANDIDATE"),
    (r'-----BEGIN (RSA |EC )?PRIVATE KEY', "CLE_PRIVEE"),
    (r'(?i)mysql://\S+:\S+@',            "CONN_DB"),
    (r'(?i)postgresql://\S+:\S+@',       "CONN_DB"),
]

PATTERNS_INTRUSION = [
    (r'__import__\s*\(\s*["\']os["\']',  "IMPORT_OS_DYNAMIQUE"),
    (r'eval\s*\(',                        "EVAL_DANGEREUX"),
    (r'exec\s*\(',                        "EXEC_DANGEREUX"),
    (r'subprocess\.call\s*\(\s*["\']',   "SHELL_INJECTION"),
    (r'open\s*\([^)]*["\']w["\']',       "ECRITURE_FICHIER"),
    (r'socket\.connect',                  "CONNEXION_RESEAU"),
    (r'urllib\.request\|requests\.get',  "REQUETE_HTTP"),
    (r'os\.system\s*\(',                 "OS_SYSTEM"),
    (r'shutil\.rmtree',                  "SUPPRESSION_RECURSIVE"),
    (r'os\.remove|os\.unlink',           "SUPPRESSION_FICHIER"),
]

FICHIERS_SENSIBLES = [
    ".env", "config.json", "secrets.json", "credentials.json",
    "memoire_entreprise.json", "watchdog_sante.json",
    "index_projets.json",
]

EXTENSIONS_A_SCANNER = {".py", ".json", ".env", ".txt", ".sh", ".yaml", ".yml"}


def scanner_secrets(contenu, nom_fichier):
    """Scanne un contenu à la recherche de secrets."""
    trouvailles = []
    for pattern, type_secret in PATTERNS_SECRETS:
        for match in re.finditer(pattern, contenu):
            ligne = contenu[:match.start()].count('\n') + 1
            trouvailles.append({
                "type": type_secret,
                "ligne": ligne,
                "extrait": contenu[match.start():match.start()+40].replace('\n', '') + "...",
            })
    return trouvailles


def scanner_intrusion(contenu, nom_fichier):
    """Détecte les patterns d'intrusion ou de code malveillant."""
    trouvailles = []
    for pattern, type_menace in PATTERNS_INTRUSION:
        for match in re.finditer(pattern, contenu):
            ligne = contenu[:match.start()].count('\n') + 1
            trouvailles.append({
                "type": type_menace,
                "ligne": ligne,
                "extrait": contenu[match.start():match.start()+60].replace('\n', ''),
            })
    return trouvailles


def empreinte_fichier(chemin):
    """Calcule le hash MD5 + SHA256 d'un fichier."""
    try:
        with open(chemin, "rb") as f:
            data = f.read()
        return {
            "md5": hashlib.md5(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest()[:16],
            "taille": len(data),
        }
    except Exception:
        return {"md5": "", "sha256": "", "taille": 0}


def audit_silencieux():
    """
    Audit complet sans créer de fichier permanent.
    Résultats stockés uniquement en mémoire RAM, affichés puis effacés.
    """
    rapport = {
        "debut": datetime.now().isoformat(),
        "secrets_detectes": [],
        "menaces_detectees": [],
        "fichiers_sensibles": [],
        "fichiers_scannes": 0,
        "anomalies_count": 0,
    }

    print(f"\n{'═'*60}")
    print(f"  FANTÔME — Audit silencieux démarré")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} — Mode : ZÉRO TRACE")
    print(f"{'═'*60}\n")

    # 1. Scanner tous les fichiers Python et config
    for racine, dossiers, fichiers in os.walk("."):
        dossiers[:] = [d for d in dossiers if d not in {"__pycache__", ".git", "node_modules", "venv", ".venv"}]

        for fichier in fichiers:
            _, ext = os.path.splitext(fichier)
            if ext not in EXTENSIONS_A_SCANNER:
                continue

            chemin = os.path.join(racine, fichier)
            try:
                with open(chemin, "r", encoding="utf-8", errors="ignore") as f:
                    contenu = f.read()

                rapport["fichiers_scannes"] += 1

                secrets = scanner_secrets(contenu, fichier)
                menaces = scanner_intrusion(contenu, fichier)

                if secrets:
                    for s in secrets:
                        s["fichier"] = chemin
                        rapport["secrets_detectes"].append(s)
                        rapport["anomalies_count"] += 1

                if menaces:
                    for m in menaces:
                        m["fichier"] = chemin
                        rapport["menaces_detectees"].append(m)

            except Exception:
                pass

    # 2. Vérifier les fichiers sensibles
    for nom in FICHIERS_SENSIBLES:
        if os.path.exists(nom):
            empreinte = empreinte_fichier(nom)
            taille_kb = round(empreinte["taille"] / 1024, 1)
            rapport["fichiers_sensibles"].append({
                "fichier": nom,
                "taille_kb": taille_kb,
                "md5": empreinte["md5"],
            })

    # 3. Afficher les résultats
    print(f"  Fichiers scannés : {rapport['fichiers_scannes']}")
    print(f"  Anomalies totales : {rapport['anomalies_count']}\n")

    if rapport["secrets_detectes"]:
        print(f"  🔴 SECRETS DÉTECTÉS ({len(rapport['secrets_detectes'])}) :")
        for s in rapport["secrets_detectes"]:
            print(f"     └─ {s['fichier']} ligne {s['ligne']} → [{s['type']}]")
            print(f"        {s['extrait']}")
    else:
        print(f"  ✅ Aucun secret exposé détecté.")

    if rapport["menaces_detectees"]:
        print(f"\n  🟡 PATTERNS SUSPECTS ({len(rapport['menaces_detectees'])}) :")
        for m in rapport["menaces_detectees"]:
            print(f"     └─ {m['fichier']} ligne {m['ligne']} → [{m['type']}]")
    else:
        print(f"  ✅ Aucun pattern d'intrusion détecté.")

    if rapport["fichiers_sensibles"]:
        print(f"\n  🔒 FICHIERS SENSIBLES PRÉSENTS :")
        for f in rapport["fichiers_sensibles"]:
            print(f"     └─ {f['fichier']} ({f['taille_kb']} Ko) — MD5: {f['md5'][:8]}...")

    # 4. Analyse IA si anomalies
    if rapport["anomalies_count"] > 0:
        _analyse_ia_fantome(rapport)

    # 5. Nettoyer le rapport de la RAM (aucune écriture disque)
    fin = datetime.now().isoformat()
    print(f"\n  Audit terminé : {fin}")
    print(f"  Mode FANTÔME : aucun fichier créé. Données effacées.")

    # Effacement explicite
    rapport.clear()
    del rapport


def _analyse_ia_fantome(rapport):
    """Analyse IA en mémoire uniquement — ne sauvegarde rien."""
    print(f"\n{'─'*60}")
    print(f"  ► Analyse IA (mémoire uniquement)")
    print(f"{'─'*60}\n")

    resume = f"""Audit silencieux Caelum Partners :
- Fichiers scannés : {rapport['fichiers_scannes']}
- Secrets détectés : {len(rapport['secrets_detectes'])}
- Patterns suspects : {len(rapport['menaces_detectees'])}
- Détails : {json.dumps(rapport['secrets_detectes'][:3], ensure_ascii=False)}"""

    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction="""Tu es l'expert sécurité Zero-Trust de Caelum Partners.
Tu analyses les résultats d'un audit silencieux et donnes des actions correctives
précises et immédiates. Aucun blabla, que de l'action.""",
        generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=400),
    )
    try:
        for chunk in model.generate_content(resume, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
    except Exception as e:
        print(f"[IA indisponible : {e}]")
    print()


def verifier_integrite_agents():
    """
    Calcule les empreintes de tous les agents et détecte
    des modifications non autorisées par rapport à la dernière vérification.
    Résultat uniquement en RAM.
    """
    print(f"\n{'═'*60}")
    print(f"  FANTÔME — Contrôle d'intégrité des agents")
    print(f"{'═'*60}\n")

    # Fichier de référence temporaire (effacé après)
    ref_tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                           delete=False, encoding='utf-8')
    ref_path = ref_tmp.name

    # Charger référence précédente si elle existe
    ref_existante = {}
    ref_permanente = ".fantome_ref"
    if os.path.exists(ref_permanente):
        try:
            with open(ref_permanente, "r") as f:
                ref_existante = json.load(f)
        except Exception:
            pass

    empreintes_actuelles = {}
    modifications = []

    for fichier in [f for f in os.listdir(".") if f.endswith(".py")]:
        emp = empreinte_fichier(fichier)
        empreintes_actuelles[fichier] = emp["md5"]

        if fichier in ref_existante:
            if ref_existante[fichier] != emp["md5"]:
                modifications.append(fichier)
                print(f"  ⚠️  MODIFIÉ : {fichier}")
        else:
            print(f"  ➕ NOUVEAU : {fichier}")

    if not modifications:
        print(f"  ✅ Aucune modification non autorisée détectée.")
    else:
        print(f"\n  🔴 {len(modifications)} agent(s) modifié(s) depuis la dernière vérification.")

    # Sauvegarder nouvelle référence (fichier caché minimal)
    with open(ref_permanente, "w") as f:
        json.dump(empreintes_actuelles, f)
    print(f"\n  Référence mise à jour ({len(empreintes_actuelles)} agents).")

    # Nettoyer le tmp
    try:
        ref_tmp.close()
        os.unlink(ref_path)
    except Exception:
        pass

    # Effacer données sensibles de la RAM
    empreintes_actuelles.clear()
    ref_existante.clear()
    del empreintes_actuelles, ref_existante


def nettoyer_traces():
    """Supprime les fichiers temporaires et logs résiduels."""
    patterns_a_nettoyer = [
        "*.tmp", "*.log", "watchdog_sante.json",
    ]
    supprimes = []
    for pattern in patterns_a_nettoyer:
        import glob
        for f in glob.glob(pattern):
            try:
                os.remove(f)
                supprimes.append(f)
            except Exception:
                pass

    if supprimes:
        print(f"\n  🧹 Traces nettoyées : {', '.join(supprimes)}")
    else:
        print(f"\n  ✅ Aucune trace résiduelle trouvée.")


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT FANTÔME — Audit silencieux, zéro trace")
    print("  Caelum Partners — Sécurité Zero-Trust")
    print("═"*60)

    while True:
        print("\n  1. Audit silencieux complet (secrets + intrusions)")
        print("  2. Contrôle d'intégrité des agents")
        print("  3. Nettoyer toutes les traces résiduelles")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            audit_silencieux()
        elif choix == "2":
            verifier_integrite_agents()
        elif choix == "3":
            nettoyer_traces()
        else:
            print("  Choix invalide.")

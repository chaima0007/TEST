"""
AGENT DATA SCIENCE & BUSINESS INTELLIGENCE — AgentClaude Solutions
Expert en analyse de données, segmentation, prévisions et data storytelling.

Usage : python agent_data.py
"""

import os
import sys
import json
import csv
import statistics
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from google import genai
from google.genai import types

from memoire import charger_memoire, incrementer_stat

# ─── Configuration ────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécutez : export GEMINI_API_KEY=votre_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

ENTREPRISE = "AgentClaude Solutions"
DATA_DIR = os.path.join("fichiers", "data")
os.makedirs(DATA_DIR, exist_ok=True)

LARGEUR = 70


# ═══════════════════════════════════════════════════════════════
# UTILITAIRES COMMUNS
# ═══════════════════════════════════════════════════════════════

def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def _sep(car="═", n=LARGEUR):
    return car * n


def _titre(texte, car="═"):
    return f"\n{_sep(car)}\n  {texte}\n{_sep(car)}"


def _streamer(prompt: str, temperature: float = 0.5) -> str:
    """Appelle Gemini en streaming et retourne le texte complet."""
    modele = _creer_model(
        model_name=MODEL,
        system_instruction=(
            "Tu es un expert en data science et business intelligence pour "
            f"{ENTREPRISE}, spécialisée en agents IA autonomes. "
            "Tu réponds TOUJOURS en français. Tu es analytique, précis et orienté action."
        ),
        generation_config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=4096,
        ),
    )
    print()
    texte = ""
    for chunk in modele.generate_content(prompt, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            texte += chunk.text
    print("\n")
    return texte


def _sauvegarder_rapport(nom_fichier: str, contenu: str) -> str:
    """Sauvegarde un rapport dans fichiers/data/ et retourne le chemin."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(DATA_DIR, f"{nom_fichier}_{horodatage}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def _est_numerique(valeur: str) -> bool:
    """Vérifie si une chaîne représente un nombre."""
    try:
        float(valeur.replace(",", ".").replace(" ", ""))
        return True
    except (ValueError, AttributeError):
        return False


def _to_float(valeur: str) -> float:
    """Convertit une chaîne en float."""
    return float(valeur.replace(",", ".").replace(" ", ""))


def _quartile(data: list, q: float) -> float:
    """Calcule un quartile (q entre 0 et 1) sur une liste triée."""
    data_sorted = sorted(data)
    n = len(data_sorted)
    if n == 0:
        return 0.0
    index = q * (n - 1)
    lower = int(index)
    upper = lower + 1
    if upper >= n:
        return data_sorted[lower]
    fraction = index - lower
    return data_sorted[lower] + fraction * (data_sorted[upper] - data_sorted[lower])


def _regression_lineaire(x: list, y: list):
    """Régression linéaire simple. Retourne (pente, ordonnée_origine, r2)."""
    n = len(x)
    if n < 2:
        return 0.0, 0.0, 0.0
    moy_x = statistics.mean(x)
    moy_y = statistics.mean(y)
    num = sum((x[i] - moy_x) * (y[i] - moy_y) for i in range(n))
    den = sum((x[i] - moy_x) ** 2 for i in range(n))
    if den == 0:
        return 0.0, moy_y, 0.0
    pente = num / den
    origine = moy_y - pente * moy_x
    # Calcul R²
    y_pred = [pente * x[i] + origine for i in range(n)]
    ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y[i] - moy_y) ** 2 for i in range(n))
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0
    return pente, origine, r2


def _barre_ascii(valeur, maxi, largeur=30, car_plein="█", car_vide="░"):
    """Génère une barre ASCII proportionnelle."""
    if maxi == 0:
        rempli = 0
    else:
        rempli = int((valeur / maxi) * largeur)
    rempli = min(rempli, largeur)
    vide = largeur - rempli
    return f"[{car_plein * rempli}{car_vide * vide}]"


def _jours_depuis(date_str: str) -> int:
    """Calcule le nombre de jours depuis une date ISO."""
    try:
        date = datetime.fromisoformat(date_str)
        return (datetime.now() - date).days
    except Exception:
        return 0


# ═══════════════════════════════════════════════════════════════
# AGENT 1 — ANALYSEUR CSV
# ═══════════════════════════════════════════════════════════════

def agent_analyser_csv(chemin_fichier: str) -> str:
    """
    Lit un fichier CSV, calcule les statistiques descriptives complètes
    (min, max, moyenne, médiane, mode, IQR, outliers, valeurs manquantes,
    comptages catégoriels), puis envoie le résumé à Gemini pour des
    insights business et recommandations. Sauvegarde le rapport.

    Args:
        chemin_fichier : Chemin vers le fichier CSV à analyser
    """
    incrementer_stat("agent_data_analyser_csv")
    print(_titre(f"ANALYSEUR CSV — {ENTREPRISE}"))
    print(f"  Fichier : {chemin_fichier}\n")

    if not os.path.exists(chemin_fichier):
        print(f"  [ERREUR] Fichier introuvable : {chemin_fichier}")
        return ""

    # ── Lecture CSV ──
    lignes = []
    en_tetes = []
    try:
        with open(chemin_fichier, newline="", encoding="utf-8-sig") as f:
            lecteur = csv.DictReader(f)
            en_tetes = lecteur.fieldnames or []
            for ligne in lecteur:
                lignes.append(ligne)
    except Exception as e:
        print(f"  [ERREUR] Lecture CSV : {e}")
        return ""

    nb_lignes = len(lignes)
    nb_colonnes = len(en_tetes)
    print(f"  Lignes : {nb_lignes} | Colonnes : {nb_colonnes}")
    print(f"  Colonnes : {', '.join(en_tetes)}\n")

    # ── Classification colonnes ──
    colonnes_numeriques = {}
    colonnes_categoriques = {}

    for col in en_tetes:
        valeurs_brutes = [ligne[col] for ligne in lignes]
        valeurs_non_vides = [v for v in valeurs_brutes if v and v.strip()]
        nb_manquants = nb_lignes - len(valeurs_non_vides)

        if valeurs_non_vides and all(_est_numerique(v) for v in valeurs_non_vides):
            nums = [_to_float(v) for v in valeurs_non_vides]
            colonnes_numeriques[col] = {
                "valeurs": nums,
                "nb_manquants": nb_manquants,
            }
        else:
            colonnes_categoriques[col] = {
                "valeurs": valeurs_non_vides,
                "nb_manquants": nb_manquants,
            }

    # ── Statistiques numériques ──
    stats_numeriques = {}
    for col, info in colonnes_numeriques.items():
        nums = info["valeurs"]
        if not nums:
            continue
        q1 = _quartile(nums, 0.25)
        q3 = _quartile(nums, 0.75)
        iqr = q3 - q1
        borne_inf = q1 - 1.5 * iqr
        borne_sup = q3 + 1.5 * iqr
        outliers = [v for v in nums if v < borne_inf or v > borne_sup]
        try:
            mode_val = statistics.mode(nums)
        except statistics.StatisticsError:
            mode_val = None

        stats_numeriques[col] = {
            "count": len(nums),
            "manquants": info["nb_manquants"],
            "min": min(nums),
            "max": max(nums),
            "moyenne": statistics.mean(nums),
            "mediane": statistics.median(nums),
            "mode": mode_val,
            "ecart_type": statistics.stdev(nums) if len(nums) > 1 else 0,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "nb_outliers": len(outliers),
            "outliers_valeurs": sorted(outliers)[:10],
        }

    # ── Statistiques catégorielles ──
    stats_categoriques = {}
    for col, info in colonnes_categoriques.items():
        valeurs = info["valeurs"]
        comptage = Counter(valeurs)
        stats_categoriques[col] = {
            "count": len(valeurs),
            "manquants": info["nb_manquants"],
            "nb_uniques": len(comptage),
            "top_5": comptage.most_common(5),
        }

    # ── Affichage console ──
    print(_sep("─"))
    print("  COLONNES NUMÉRIQUES")
    print(_sep("─"))
    for col, s in stats_numeriques.items():
        pct_manquants = round(s["manquants"] / nb_lignes * 100, 1) if nb_lignes > 0 else 0
        print(f"\n  {col.upper()}")
        print(f"    Min={s['min']:.2f} | Max={s['max']:.2f} | Moyenne={s['moyenne']:.2f} | Médiane={s['mediane']:.2f}")
        print(f"    Mode={s['mode']} | Écart-type={s['ecart_type']:.2f}")
        print(f"    Q1={s['q1']:.2f} | Q3={s['q3']:.2f} | IQR={s['iqr']:.2f}")
        print(f"    Valeurs manquantes : {s['manquants']} ({pct_manquants}%)")
        if s["nb_outliers"] > 0:
            print(f"    Outliers (IQR) : {s['nb_outliers']} | Ex: {s['outliers_valeurs'][:5]}")

    print(f"\n{_sep('─')}")
    print("  COLONNES CATÉGORIELLES")
    print(_sep("─"))
    for col, s in stats_categoriques.items():
        pct_manquants = round(s["manquants"] / nb_lignes * 100, 1) if nb_lignes > 0 else 0
        print(f"\n  {col.upper()} ({s['nb_uniques']} valeurs uniques)")
        print(f"    Manquants : {s['manquants']} ({pct_manquants}%)")
        print(f"    Top valeurs : " + " | ".join(f"{v}({c})" for v, c in s["top_5"]))

    print(f"\n{_sep('═')}")

    # ── Résumé pour Gemini ──
    resume_stats = f"""ANALYSE DU FICHIER CSV : {os.path.basename(chemin_fichier)}
Lignes : {nb_lignes} | Colonnes : {nb_colonnes}
Date d'analyse : {datetime.now().strftime('%d/%m/%Y %H:%M')}

COLONNES NUMÉRIQUES ({len(stats_numeriques)}) :
"""
    for col, s in stats_numeriques.items():
        resume_stats += f"""
  - {col} : min={s['min']:.2f}, max={s['max']:.2f}, moyenne={s['moyenne']:.2f}, médiane={s['mediane']:.2f}
    écart-type={s['ecart_type']:.2f}, {s['manquants']} valeurs manquantes, {s['nb_outliers']} outliers détectés
"""

    resume_stats += f"\nCOLONNES CATÉGORIELLES ({len(stats_categoriques)}) :\n"
    for col, s in stats_categoriques.items():
        top = ", ".join(f"{v}({c})" for v, c in s["top_5"])
        resume_stats += f"  - {col} : {s['nb_uniques']} valeurs uniques, top valeurs : {top}\n"

    prompt = f"""Tu es un expert data scientist et business analyst chez {ENTREPRISE}.

Voici les statistiques complètes d'un fichier CSV analysé :

{resume_stats}

En français, génère un rapport d'analyse business approfondi avec :

1. VUE D'ENSEMBLE
   (Qualité des données, complétude, fiabilité globale)

2. PATTERNS IDENTIFIÉS
   (Tendances, corrélations potentielles, anomalies remarquables)

3. OUTLIERS & DONNÉES ABERRANTES
   (Interprétation business des valeurs extrêmes détectées)

4. INSIGHTS BUSINESS CLÉS
   (3-5 enseignements actionnables tirés des données)

5. RECOMMANDATIONS
   (Actions concrètes basées sur l'analyse — priorisées)

6. QUALITÉ DES DONNÉES
   (Évaluation /10, lacunes à combler, suggestions d'enrichissement)

Sois précis, quantifié et orienté décision.
"""

    print("\n  Analyse IA des insights business en cours...\n")
    print(_sep("─"))
    print("  INSIGHTS BUSINESS (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.4)

    # ── Sauvegarde rapport ──
    contenu_rapport = f"ANALYSE CSV — {ENTREPRISE}\n"
    contenu_rapport += f"Fichier : {chemin_fichier}\n"
    contenu_rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu_rapport += "=" * LARGEUR + "\n\n"
    contenu_rapport += resume_stats
    contenu_rapport += "\n\nINSIGHTS BUSINESS (IA) :\n" + reponse

    chemin = _sauvegarder_rapport("analyse_csv", contenu_rapport)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 2 — INSIGHTS MÉMOIRE
# ═══════════════════════════════════════════════════════════════

def agent_insights_memoire() -> str:
    """
    Analyse en profondeur toutes les données de memoire.json :
    acquisition clients, revenus, heatmap agents, entonnoir de conversion,
    cohortes mensuelles, scoring churn. Génère des insights actionnables.
    """
    incrementer_stat("agent_data_insights_memoire")
    memoire = charger_memoire()

    print(_titre(f"INSIGHTS MÉMOIRE — ANALYSE PROFONDE — {ENTREPRISE}"))
    print(f"  Analyse du {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")

    clients = memoire.get("clients", {})
    interactions = memoire.get("interactions", [])
    factures = memoire.get("factures", [])
    projets = memoire.get("projets", {})
    stats = memoire.get("stats", {})

    # ── Acquisition clients par mois (cohorte) ──
    cohortes = defaultdict(list)
    for nom, data in clients.items():
        date_ajout = data.get("date_ajout", "")
        if date_ajout:
            try:
                dt = datetime.fromisoformat(date_ajout)
                cle = dt.strftime("%Y-%m")
                cohortes[cle].append(nom)
            except Exception:
                pass

    # ── Revenus par mois ──
    revenus_par_mois = defaultdict(float)
    for f in factures:
        date_emission = f.get("date_emission", "")
        if date_emission:
            try:
                dt = datetime.fromisoformat(date_emission)
                cle = dt.strftime("%Y-%m")
                revenus_par_mois[cle] += f.get("total_ttc", 0)
            except Exception:
                pass

    # ── Heatmap utilisation agents ──
    agents_utilises = stats.get("agents_utilises", {})
    total_demandes = stats.get("total_demandes", 0)
    top_agents = sorted(agents_utilises.items(), key=lambda x: x[1], reverse=True)

    # ── Entonnoir de conversion ──
    nb_total = len(clients)
    nb_prospects = sum(1 for c in clients.values() if c.get("statut") == "prospect")
    nb_actifs = sum(1 for c in clients.values() if c.get("statut") == "actif")
    nb_inactifs = sum(1 for c in clients.values() if c.get("statut") not in ("prospect", "actif"))
    taux_conv = round(nb_actifs / nb_total * 100, 1) if nb_total > 0 else 0

    # ── Scoring churn ──
    # Clients actifs sans interaction récente
    churn_risques = []
    for nom, data in clients.items():
        if data.get("statut") == "actif":
            derniere_date = None
            inters_client = data.get("interactions", [])
            if inters_client:
                dates = [i.get("date", "") for i in inters_client if i.get("date")]
                if dates:
                    derniere_date = max(dates)
            if derniere_date:
                jours = _jours_depuis(derniere_date)
            else:
                jours = _jours_depuis(data.get("date_ajout", ""))

            score_churn = 0
            if jours > 90:
                score_churn = 90
            elif jours > 60:
                score_churn = 70
            elif jours > 30:
                score_churn = 40
            elif jours > 14:
                score_churn = 20

            if score_churn > 0:
                churn_risques.append({
                    "nom": nom,
                    "jours_inactif": jours,
                    "score_churn": score_churn,
                    "secteur": data.get("secteur", "N/A"),
                })

    churn_risques.sort(key=lambda x: x["score_churn"], reverse=True)

    # ── Secteurs ──
    secteurs = Counter(data.get("secteur", "N/A") for data in clients.values())

    # ── Affichage console ──
    print(_sep("─"))
    print("  ACQUISITION CLIENTS PAR MOIS (COHORTES)")
    print(_sep("─"))
    mois_triés = sorted(cohortes.keys())
    max_cohorte = max((len(v) for v in cohortes.values()), default=1)
    for mois in mois_triés:
        n = len(cohortes[mois])
        barre = _barre_ascii(n, max_cohorte, largeur=20)
        print(f"  {mois}  {barre} {n} client(s)")

    print(f"\n{_sep('─')}")
    print("  REVENUS PAR MOIS")
    print(_sep("─"))
    mois_rev_triés = sorted(revenus_par_mois.keys())
    max_rev = max(revenus_par_mois.values(), default=1)
    for mois in mois_rev_triés:
        rev = revenus_par_mois[mois]
        barre = _barre_ascii(rev, max_rev, largeur=20)
        print(f"  {mois}  {barre} {rev:,.0f}€")

    print(f"\n{_sep('─')}")
    print("  HEATMAP UTILISATION DES AGENTS")
    print(_sep("─"))
    if top_agents:
        max_agent = top_agents[0][1] if top_agents else 1
        for nom_agent, count in top_agents[:10]:
            barre = _barre_ascii(count, max_agent, largeur=25)
            pct = round(count / total_demandes * 100, 1) if total_demandes > 0 else 0
            print(f"  {nom_agent:<35} {barre} {count} ({pct}%)")
    else:
        print("  Aucune utilisation enregistrée.")

    print(f"\n{_sep('─')}")
    print("  ENTONNOIR DE CONVERSION")
    print(_sep("─"))
    max_funnel = max(nb_total, 1)
    print(f"  Total contacts  {_barre_ascii(nb_total, max_funnel, 25)} {nb_total}")
    print(f"  Prospects       {_barre_ascii(nb_prospects, max_funnel, 25)} {nb_prospects}")
    print(f"  Clients actifs  {_barre_ascii(nb_actifs, max_funnel, 25)} {nb_actifs}")
    print(f"\n  Taux de conversion global : {taux_conv}%")

    print(f"\n{_sep('─')}")
    print("  SCORING CHURN (clients à risque)")
    print(_sep("─"))
    if churn_risques:
        for r in churn_risques[:8]:
            barre = _barre_ascii(r["score_churn"], 100, largeur=15)
            print(f"  {r['nom']:<20} {barre} Risque:{r['score_churn']}% | {r['jours_inactif']}j inactif")
    else:
        print("  Aucun client à risque de churn détecté.")

    print(f"\n{_sep('═')}")

    # ── Résumé pour Gemini ──
    cohortes_str = "\n".join(f"  {m} : {len(cohortes[m])} nouveau(x) client(s)" for m in mois_triés) or "  Aucune donnée."
    revenus_str = "\n".join(f"  {m} : {revenus_par_mois[m]:,.0f}€" for m in mois_rev_triés) or "  Aucune donnée."
    agents_str = "\n".join(f"  {a} : {c} utilisations" for a, c in top_agents[:8]) or "  Aucune donnée."
    churn_str = "\n".join(f"  {r['nom']} ({r['secteur']}) : {r['jours_inactif']}j inactif, score={r['score_churn']}%" for r in churn_risques[:5]) or "  Aucun risque détecté."
    secteurs_str = "\n".join(f"  {s} : {n}" for s, n in secteurs.most_common()) or "  Aucune donnée."

    prompt = f"""Tu es le Chief Data Officer de {ENTREPRISE}, spécialisée en agents IA autonomes.

Voici une analyse complète des données d'entreprise :

COHORTES D'ACQUISITION CLIENTS (par mois) :
{cohortes_str}

REVENUS PAR MOIS :
{revenus_str}

HEATMAP AGENTS (top utilisés) :
{agents_str}
Total requêtes : {total_demandes}

ENTONNOIR DE CONVERSION :
- Contacts totaux : {nb_total}
- Prospects : {nb_prospects}
- Clients actifs : {nb_actifs}
- Taux conversion : {taux_conv}%

SCORING CHURN (clients à risque) :
{churn_str}

RÉPARTITION SECTORIELLE :
{secteurs_str}

En français, génère un rapport d'insights business approfondi :

1. TENDANCES D'ACQUISITION
   (Rythme de croissance, mois forts/faibles, saisonnalité détectée)

2. ANALYSE DES REVENUS
   (Évolution, pics, creux, corrélation avec acquisition)

3. UTILISATION DES AGENTS — ENSEIGNEMENTS
   (Quels agents sur/sous-utilisés ? Que dit la répartition ?)

4. ANALYSE DE L'ENTONNOIR
   (Où perd-on des prospects ? Comment améliorer la conversion ?)

5. STRATÉGIE ANTI-CHURN
   (Plan d'action pour les clients à risque identifiés)

6. RECOMMANDATIONS PRIORITAIRES (TOP 5 actions)
   (Classées par impact estimé)

Quantifie chaque insight avec les données disponibles. Sois stratégique et actionnable.
"""

    print("\n  Génération des insights IA en cours...\n")
    print(_sep("─"))
    print("  INSIGHTS STRATÉGIQUES (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.5)

    contenu_rapport = f"INSIGHTS MÉMOIRE — {ENTREPRISE}\n"
    contenu_rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu_rapport += "=" * LARGEUR + "\n\n"
    contenu_rapport += f"Clients totaux : {nb_total} | Actifs : {nb_actifs} | Prospects : {nb_prospects}\n"
    contenu_rapport += f"Taux conversion : {taux_conv}% | Total requêtes agents : {total_demandes}\n\n"
    contenu_rapport += "COHORTES :\n" + cohortes_str + "\n\n"
    contenu_rapport += "REVENUS PAR MOIS :\n" + revenus_str + "\n\n"
    contenu_rapport += "CHURN RISKS :\n" + churn_str + "\n\n"
    contenu_rapport += "\nINSIGHTS IA :\n" + reponse

    chemin = _sauvegarder_rapport("insights_memoire", contenu_rapport)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 3 — RAPPORT PERFORMANCE
# ═══════════════════════════════════════════════════════════════

def agent_rapport_performance(periode: str) -> str:
    """
    Génère un rapport de performance complet : taux d'utilisation des agents,
    temps de réponse estimés, patterns succès/échecs, goulots d'étranglement,
    opportunités d'optimisation, benchmarks sectoriels IA.

    Args:
        periode : Période d'analyse (ex: "7j", "30j", "90j", "tout")
    """
    incrementer_stat("agent_data_rapport_performance")
    memoire = charger_memoire()

    print(_titre(f"RAPPORT DE PERFORMANCE — {ENTREPRISE}"))
    print(f"  Période : {periode}\n")

    clients = memoire.get("clients", {})
    interactions = memoire.get("interactions", [])
    factures = memoire.get("factures", [])
    tickets = memoire.get("tickets", [])
    projets = memoire.get("projets", {})
    stats = memoire.get("stats", {})

    # ── Filtrage par période ──
    nb_jours = 9999
    if periode.endswith("j"):
        try:
            nb_jours = int(periode[:-1])
        except ValueError:
            pass
    elif periode == "tout":
        nb_jours = 9999

    interactions_filtrees = [
        i for i in interactions
        if _jours_depuis(i.get("date", "")) <= nb_jours
    ]
    factures_filtrees = [
        f for f in factures
        if _jours_depuis(f.get("date_emission", "")) <= nb_jours
    ]
    tickets_filtrees = [
        t for t in tickets
        if _jours_depuis(t.get("date", "")) <= nb_jours
    ]

    agents_utilises = stats.get("agents_utilises", {})
    total_demandes = stats.get("total_demandes", 0)
    top_agents = sorted(agents_utilises.items(), key=lambda x: x[1], reverse=True)

    # ── Métriques performance ──
    nb_tickets_total = len(tickets_filtrees)
    nb_tickets_resolus = sum(1 for t in tickets_filtrees if t.get("resolu"))
    taux_resolution = round(nb_tickets_resolus / nb_tickets_total * 100, 1) if nb_tickets_total > 0 else 0

    nb_factures = len(factures_filtrees)
    revenus_periode = sum(f.get("total_ttc", 0) for f in factures_filtrees)
    factures_payees = sum(1 for f in factures_filtrees if f.get("payee"))
    taux_paiement = round(factures_payees / nb_factures * 100, 1) if nb_factures > 0 else 0

    nb_interactions = len(interactions_filtrees)
    types_actions = Counter(i.get("action", "N/A") for i in interactions_filtrees)

    nb_projets_actifs = sum(1 for p in projets.values() if p.get("statut") not in ("terminé", "annulé"))
    nb_projets_termines = sum(1 for p in projets.values() if p.get("statut") == "terminé")

    # ── Taux d'utilisation agents ──
    nb_agents_connus = len(agents_utilises)
    agent_le_plus_utilise = top_agents[0] if top_agents else ("N/A", 0)
    concentration_top3 = sum(c for _, c in top_agents[:3]) / max(total_demandes, 1) * 100

    # ── Patterns tickets ──
    urgences = Counter(t.get("urgence", "N/A") for t in tickets_filtrees)
    types_tickets = Counter(t.get("type", "N/A") for t in tickets_filtrees)

    # ── Affichage console ──
    print(_sep("─"))
    print("  TAUX D'UTILISATION DES AGENTS")
    print(_sep("─"))
    if top_agents:
        max_val = top_agents[0][1] if top_agents else 1
        for nom_agent, count in top_agents[:8]:
            taux = round(count / total_demandes * 100, 1) if total_demandes > 0 else 0
            barre = _barre_ascii(count, max_val, largeur=20)
            print(f"  {nom_agent:<35} {barre} {taux}% ({count} req.)")
    print(f"\n  Concentration top 3 agents : {concentration_top3:.1f}% des requêtes")

    print(f"\n{_sep('─')}")
    print("  PERFORMANCE SUPPORT TICKETS")
    print(_sep("─"))
    print(f"  Tickets période   : {nb_tickets_total}")
    print(f"  Résolus           : {nb_tickets_resolus} ({taux_resolution}%)")
    print(f"  Urgences : " + " | ".join(f"{k}:{v}" for k, v in urgences.most_common()))

    print(f"\n{_sep('─')}")
    print("  PERFORMANCE FACTURATION")
    print(_sep("─"))
    print(f"  Factures émises   : {nb_factures} ({revenus_periode:,.0f}€)")
    print(f"  Taux paiement     : {taux_paiement}%")

    print(f"\n{_sep('─')}")
    print("  ACTIVITÉ INTERACTIONS")
    print(_sep("─"))
    print(f"  Interactions      : {nb_interactions}")
    if types_actions:
        print(f"  Types : " + " | ".join(f"{k}({v})" for k, v in types_actions.most_common(5)))

    print(f"\n{_sep('═')}")

    prompt = f"""Tu es un expert en performance opérationnelle pour des sociétés d'IA comme {ENTREPRISE}.

DONNÉES DE PERFORMANCE — Période : {periode}

AGENTS IA :
- Nombre d'agents actifs : {nb_agents_connus}
- Total requêtes : {total_demandes}
- Agent le plus utilisé : {agent_le_plus_utilise[0]} ({agent_le_plus_utilise[1]} requêtes)
- Concentration top 3 : {concentration_top3:.1f}% des requêtes
- Distribution : {", ".join(f"{a}:{c}" for a, c in top_agents[:6])}

SUPPORT :
- Tickets : {nb_tickets_total} | Résolus : {nb_tickets_resolus} ({taux_resolution}%)
- Répartition urgences : {dict(urgences.most_common())}

FACTURATION :
- Factures : {nb_factures} | Montant : {revenus_periode:,.0f}€
- Taux paiement : {taux_paiement}%

PROJETS :
- En cours : {nb_projets_actifs} | Terminés : {nb_projets_termines}

INTERACTIONS CLIENT :
- Volume : {nb_interactions}
- Types : {dict(types_actions.most_common(5))}

En français, génère un rapport de performance expert avec :

1. SYNTHÈSE DE PERFORMANCE — Période {periode}
   (Score global /10 avec justification)

2. TAUX D'UTILISATION DES AGENTS
   (Analyse de la répartition, agents sous/sur-sollicités, risque de concentration)

3. ESTIMATION DES TEMPS DE RÉPONSE
   (Basée sur le volume, comparaison avec standards du secteur IA)

4. PATTERNS SUCCÈS & ÉCHECS
   (Ce qui fonctionne, ce qui crée des frictions)

5. GOULOTS D'ÉTRANGLEMENT IDENTIFIÉS
   (Où l'opérationnel ralentit — avec preuves dans les données)

6. BENCHMARKS SECTORIELS
   (Comparaison avec standards industrie AI-as-a-Service : taux résolution, délais, conversion)

7. PLAN D'OPTIMISATION PRIORITAIRE
   (5 actions classées ROI, avec effort estimé : faible/moyen/élevé)

Utilise des données chiffrées. Sois technique et stratégique.
"""

    print("\n  Analyse de performance IA en cours...\n")
    print(_sep("─"))
    print("  RAPPORT PERFORMANCE (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.4)

    contenu_rapport = f"RAPPORT PERFORMANCE — {ENTREPRISE}\n"
    contenu_rapport += f"Période : {periode}\n"
    contenu_rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu_rapport += "=" * LARGEUR + "\n\n"
    contenu_rapport += f"Total requêtes : {total_demandes} | Agents : {nb_agents_connus}\n"
    contenu_rapport += f"Taux résolution tickets : {taux_resolution}% | Taux paiement : {taux_paiement}%\n\n"
    contenu_rapport += reponse

    chemin = _sauvegarder_rapport(f"performance_{periode}", contenu_rapport)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 4 — SEGMENTATION CLIENTS
# ═══════════════════════════════════════════════════════════════

def agent_segmentation_clients() -> str:
    """
    Analyse tous les clients en mémoire et les segmente selon :
    secteur, valeur (revenus), engagement, risque churn, potentiel de croissance.
    Génère un ICP (Ideal Customer Profile), des personas pour les 3 segments
    principaux, et des approches commerciales différenciées.
    """
    incrementer_stat("agent_data_segmentation_clients")
    memoire = charger_memoire()

    print(_titre(f"SEGMENTATION CLIENTS — {ENTREPRISE}"))
    print(f"  Analyse du {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")

    clients = memoire.get("clients", {})
    factures = memoire.get("factures", [])
    interactions = memoire.get("interactions", [])

    if not clients:
        print("  Aucun client en mémoire. Ajoutez des clients via agent_commercial.")
        return ""

    # ── Calcul revenus par client ──
    revenus_par_client = defaultdict(float)
    for f in factures:
        nom_client = f.get("client", {}).get("nom", "")
        if nom_client:
            revenus_par_client[nom_client] += f.get("total_ttc", 0)

    # ── Calcul engagement par client ──
    interactions_par_client = defaultdict(int)
    for i in interactions:
        nom = i.get("client", "")
        if nom:
            interactions_par_client[nom] += 1

    # ── Scoring churn ──
    churn_scores = {}
    for nom, data in clients.items():
        inters_client = data.get("interactions", [])
        if inters_client:
            dates = [i.get("date", "") for i in inters_client if i.get("date")]
            derniere_date = max(dates) if dates else data.get("date_ajout", "")
        else:
            derniere_date = data.get("date_ajout", "")
        jours_inactif = _jours_depuis(derniere_date)
        score = min(100, max(0, jours_inactif // 1))
        churn_scores[nom] = min(score, 100)

    # ── Segmentation multi-critères ──
    tous_revenus = list(revenus_par_client.values())
    seuil_haut_rev = _quartile(tous_revenus, 0.75) if tous_revenus else 0
    seuil_bas_rev = _quartile(tous_revenus, 0.25) if tous_revenus else 0

    tous_engagements = list(interactions_par_client.values())
    seuil_haut_eng = _quartile(tous_engagements, 0.75) if tous_engagements else 0

    segments = defaultdict(list)
    profils_clients = {}

    for nom, data in clients.items():
        rev = revenus_par_client.get(nom, 0)
        eng = interactions_par_client.get(nom, len(data.get("interactions", [])))
        churn = churn_scores.get(nom, 50)
        statut = data.get("statut", "prospect")
        secteur = data.get("secteur", "N/A")

        # Segment logique
        if statut == "prospect":
            segment = "PROSPECTS"
        elif rev >= seuil_haut_rev and eng >= seuil_haut_eng:
            segment = "CHAMPIONS"
        elif rev >= seuil_haut_rev:
            segment = "GRANDS COMPTES"
        elif eng >= seuil_haut_eng and churn < 30:
            segment = "FIDÈLES ENGAGÉS"
        elif churn > 60:
            segment = "À RISQUE"
        elif rev > 0:
            segment = "ACTIFS STANDARDS"
        else:
            segment = "DORMANTS"

        segments[segment].append(nom)
        profils_clients[nom] = {
            "segment": segment,
            "secteur": secteur,
            "revenus": rev,
            "engagement": eng,
            "churn_score": churn,
            "statut": statut,
            "besoin": data.get("besoin_principal", "N/A"),
        }

    # ── Affichage console ──
    print(_sep("─"))
    print("  SEGMENTS IDENTIFIÉS")
    print(_sep("─"))
    max_seg = max((len(v) for v in segments.values()), default=1)
    for seg, membres in sorted(segments.items(), key=lambda x: -len(x[1])):
        barre = _barre_ascii(len(membres), max_seg, largeur=20)
        print(f"  {seg:<22} {barre} {len(membres)} client(s)")
        for m in membres[:4]:
            p = profils_clients[m]
            print(f"    - {m} ({p['secteur']}) | Rev:{p['revenus']:,.0f}€ | Eng:{p['engagement']} | Churn:{p['churn_score']}%")

    print(f"\n{_sep('─')}")
    print("  RÉPARTITION SECTORIELLE PAR SEGMENT")
    print(_sep("─"))
    for seg in ["CHAMPIONS", "GRANDS COMPTES", "FIDÈLES ENGAGÉS"]:
        membres = segments.get(seg, [])
        if membres:
            secteurs_seg = Counter(profils_clients[m]["secteur"] for m in membres)
            print(f"\n  {seg} :")
            for s, n in secteurs_seg.most_common(5):
                print(f"    {s} : {n}")

    print(f"\n{_sep('═')}")

    # ── Construction résumé pour Gemini ──
    segments_str = ""
    for seg, membres in segments.items():
        if membres:
            revenus_seg = sum(profils_clients[m]["revenus"] for m in membres)
            eng_moyen = statistics.mean([profils_clients[m]["engagement"] for m in membres]) if membres else 0
            churn_moyen = statistics.mean([profils_clients[m]["churn_score"] for m in membres]) if membres else 0
            secteurs_seg = Counter(profils_clients[m]["secteur"] for m in membres)
            besoins_seg = Counter(profils_clients[m]["besoin"] for m in membres)
            segments_str += f"""
SEGMENT "{seg}" — {len(membres)} client(s) :
  Revenus totaux : {revenus_seg:,.0f}€
  Engagement moyen : {eng_moyen:.1f} interactions
  Score churn moyen : {churn_moyen:.0f}%
  Secteurs : {dict(secteurs_seg.most_common(3))}
  Besoins principaux : {dict(besoins_seg.most_common(3))}
  Membres : {", ".join(membres[:5])}{"..." if len(membres) > 5 else ""}
"""

    prompt = f"""Tu es un expert en stratégie commerciale et segmentation client pour {ENTREPRISE}, spécialisée en agents IA autonomes.

Voici la segmentation complète de la base clients :

{segments_str}

En français, génère une analyse de segmentation stratégique complète :

1. PORTRAIT DE CHAQUE SEGMENT
   (Qui sont-ils ? Comportement, valeur, risque, potentiel — pour chaque segment)

2. ICP — IDEAL CUSTOMER PROFILE
   (Portrait précis du client idéal pour {ENTREPRISE} : secteur, taille, besoin, comportement d'achat, signaux d'achat)

3. PERSONAS DES 3 SEGMENTS PRINCIPAUX
   Pour chacun : prénom fictif, titre, entreprise type, motivations, freins, canal préféré, message clé

4. APPROCHE COMMERCIALE DIFFÉRENCIÉE
   Pour chaque segment : stratégie, fréquence de contact, offre recommandée, KPI de succès

5. PLAN D'ACTION PRIORISÉ
   - Segment à développer en priorité (et pourquoi)
   - 3 actions concrètes pour les 30 prochains jours

6. POTENTIEL DE REVENUS PAR SEGMENT
   (Estimation du potentiel non capturé, upsell/cross-sell opportunités)

Sois précis, créatif et très concret dans les recommandations.
"""

    print("\n  Analyse de segmentation IA en cours...\n")
    print(_sep("─"))
    print("  SEGMENTATION STRATÉGIQUE (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.6)

    contenu_rapport = f"SEGMENTATION CLIENTS — {ENTREPRISE}\n"
    contenu_rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu_rapport += "=" * LARGEUR + "\n\n"
    contenu_rapport += f"Clients analysés : {len(clients)} | Segments identifiés : {len(segments)}\n\n"
    contenu_rapport += segments_str
    contenu_rapport += "\nANALYSE IA :\n" + reponse

    chemin = _sauvegarder_rapport("segmentation_clients", contenu_rapport)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 5 — PRÉVISION VENTES
# ═══════════════════════════════════════════════════════════════

def agent_prevision_ventes(donnees_historiques_texte: str) -> str:
    """
    Analyse des données historiques fournies en texte libre, identifie la
    saisonnalité et le taux de croissance, calcule des prévisions via
    régression linéaire manuelle, génère un rapport avec intervalles de
    confiance et scénarios optimiste/réaliste/pessimiste.

    Args:
        donnees_historiques_texte : Données historiques en texte
                                     (ex: "Jan 2024: 5000, Fév 2024: 6200, ...")
    """
    incrementer_stat("agent_data_prevision_ventes")
    print(_titre(f"PRÉVISION VENTES — {ENTREPRISE}"))
    print(f"  Analyse du {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")

    # ── Parsing des données historiques ──
    import re
    # Tentative de parsing: cherche des paires (label: valeur)
    pattern = re.compile(r'([A-Za-zÀ-ÿ]+\s*\d{4}|T[1-4]\s*\d{4}|\d{4}-\d{2}|mois\s*\d+|\w+)\s*[:\-=]\s*([\d\s.,]+)', re.IGNORECASE)
    correspondances = pattern.findall(donnees_historiques_texte)

    # Si pas de correspondances, essayer format simple nombre par ligne
    if not correspondances:
        valeurs_brutes = re.findall(r'[\d]+(?:[.,][\d]+)?', donnees_historiques_texte)
        correspondances = [(f"Période {i+1}", v) for i, v in enumerate(valeurs_brutes)]

    series_temporelle = []
    for label, valeur_str in correspondances:
        valeur_str_clean = valeur_str.replace(" ", "").replace(",", ".")
        try:
            valeur = float(valeur_str_clean)
            series_temporelle.append((label.strip(), valeur))
        except ValueError:
            pass

    if not series_temporelle:
        print("  [ERREUR] Impossible de parser les données historiques.")
        print("  Format attendu : 'Jan 2024: 5000, Fév 2024: 6200'")
        return ""

    labels = [s[0] for s in series_temporelle]
    valeurs = [s[1] for s in series_temporelle]
    n = len(valeurs)

    print(f"  Données parsées : {n} points\n")
    print(_sep("─"))
    print("  DONNÉES HISTORIQUES")
    print(_sep("─"))
    max_val = max(valeurs) if valeurs else 1
    for label, val in series_temporelle:
        barre = _barre_ascii(val, max_val, largeur=25)
        print(f"  {label:<20} {barre} {val:,.0f}€")

    # ── Régression linéaire ──
    x = list(range(1, n + 1))
    pente, origine, r2 = _regression_lineaire(x, valeurs)

    # ── Statistiques de base ──
    moy_val = statistics.mean(valeurs) if valeurs else 0
    ecart_type_val = statistics.stdev(valeurs) if len(valeurs) > 1 else 0

    # ── Détection saisonnalité simple (variation par rapport à tendance) ──
    residus = [valeurs[i] - (pente * (i + 1) + origine) for i in range(n)]
    amplitude_saisonnalite = max(residus) - min(residus) if residus else 0
    pct_saisonnalite = round(amplitude_saisonnalite / moy_val * 100, 1) if moy_val > 0 else 0

    # ── Taux de croissance ──
    if n >= 2 and valeurs[0] > 0:
        taux_croissance_global = (valeurs[-1] - valeurs[0]) / valeurs[0] * 100
        taux_croissance_moyen = taux_croissance_global / (n - 1)
    else:
        taux_croissance_global = 0
        taux_croissance_moyen = 0

    # ── Prévisions sur 6 prochaines périodes ──
    previsions = []
    for i in range(1, 7):
        x_futur = n + i
        val_prevue = pente * x_futur + origine
        # Intervalle de confiance basé sur écart-type des résidus
        marge = ecart_type_val * 1.96  # ~95% IC
        previsions.append({
            "periode": f"P+{i}",
            "prevision": max(0, val_prevue),
            "ic_bas": max(0, val_prevue - marge),
            "ic_haut": val_prevue + marge,
        })

    # ── Scénarios ──
    facteur_opt = 1 + max(taux_croissance_moyen / 100 * 2, 0.1)
    facteur_pes = 1 - max(min(abs(taux_croissance_moyen) / 100, 0.15), 0.05)

    # ── Affichage console ──
    print(f"\n{_sep('─')}")
    print("  ANALYSE STATISTIQUE")
    print(_sep("─"))
    print(f"  Moyenne historique  : {moy_val:,.0f}€")
    print(f"  Écart-type          : {ecart_type_val:,.0f}€")
    print(f"  Pente (tendance)    : {pente:+.1f}€/période")
    print(f"  R² régression       : {r2:.3f} ({'fort' if r2 > 0.7 else 'modéré' if r2 > 0.4 else 'faible'})")
    print(f"  Croissance globale  : {taux_croissance_global:+.1f}%")
    print(f"  Croissance/période  : {taux_croissance_moyen:+.1f}%")
    print(f"  Saisonnalité détect.: {pct_saisonnalite}% d'amplitude")

    print(f"\n{_sep('─')}")
    print("  PRÉVISIONS (6 prochaines périodes)")
    print(_sep("─"))
    max_prev = max(p["ic_haut"] for p in previsions) if previsions else 1
    for p in previsions:
        barre = _barre_ascii(p["prevision"], max_prev, largeur=20)
        print(f"  {p['periode']:<8} {barre} {p['prevision']:>10,.0f}€  IC:[{p['ic_bas']:,.0f} — {p['ic_haut']:,.0f}]")

    print(f"\n{_sep('═')}")

    # ── Prépare données pour Gemini ──
    historique_str = "\n".join(f"  {l} : {v:,.0f}€" for l, v in series_temporelle)
    previsions_str = "\n".join(
        f"  {p['periode']} : {p['prevision']:,.0f}€ [IC95%: {p['ic_bas']:,.0f}€ — {p['ic_haut']:,.0f}€]"
        for p in previsions
    )

    total_prev_reel = sum(p["prevision"] for p in previsions)
    total_prev_opt = total_prev_reel * facteur_opt
    total_prev_pes = total_prev_reel * facteur_pes

    prompt = f"""Tu es un analyste financier et commercial senior chez {ENTREPRISE}, spécialisée en agents IA.

DONNÉES HISTORIQUES ANALYSÉES :
{historique_str}

MODÈLE DE RÉGRESSION LINÉAIRE :
- Pente : {pente:+.1f}€ par période
- Ordonnée à l'origine : {origine:.0f}€
- R² (qualité d'ajustement) : {r2:.3f}
- Croissance globale : {taux_croissance_global:+.1f}%
- Croissance moyenne par période : {taux_croissance_moyen:+.1f}%
- Saisonnalité estimée : {pct_saisonnalite}%

PRÉVISIONS CALCULÉES (régression linéaire) :
{previsions_str}

SCÉNARIOS 6 PÉRIODES :
- Optimiste  : {total_prev_opt:,.0f}€ (facteur {facteur_opt:.2f}x)
- Réaliste   : {total_prev_reel:,.0f}€ (régression pure)
- Pessimiste : {total_prev_pes:,.0f}€ (facteur {facteur_pes:.2f}x)

En français, génère un rapport de prévision ventes complet :

1. ANALYSE DE LA TENDANCE
   (Interprétation de la pente, du R², de la qualité du modèle)

2. SAISONNALITÉ IDENTIFIÉE
   (Patterns détectés dans les résidus, périodes fortes/faibles)

3. PRÉVISIONS PAR SCÉNARIO
   Tableau mensuel avec :
   - Scénario optimiste (hypothèses)
   - Scénario réaliste (base)
   - Scénario pessimiste (hypothèses)

4. INTERVALLES DE CONFIANCE
   (Interprétation des IC, niveaux de certitude)

5. FACTEURS DE RISQUE
   (Ce qui pourrait faire dévier les prévisions — positif et négatif)

6. RECOMMANDATIONS COMMERCIALES
   (Objectifs à fixer par période, actions pour dépasser le scénario réaliste)

7. INDICATEURS DE SUIVI
   (KPIs à tracker mensuellement pour valider les prévisions)

Sois précis, chiffré, et adapte les recommandations au contexte d'une entreprise d'agents IA.
"""

    print("\n  Génération des prévisions IA en cours...\n")
    print(_sep("─"))
    print("  RAPPORT PRÉVISIONNEL (IA)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.4)

    contenu_rapport = f"PRÉVISION VENTES — {ENTREPRISE}\n"
    contenu_rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu_rapport += "=" * LARGEUR + "\n\n"
    contenu_rapport += "DONNÉES HISTORIQUES :\n" + historique_str + "\n\n"
    contenu_rapport += f"Pente : {pente:+.1f} | R² : {r2:.3f} | Croissance : {taux_croissance_global:+.1f}%\n\n"
    contenu_rapport += "PRÉVISIONS :\n" + previsions_str + "\n\n"
    contenu_rapport += "ANALYSE IA :\n" + reponse

    chemin = _sauvegarder_rapport("prevision_ventes", contenu_rapport)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# AGENT 6 — DATA STORY
# ═══════════════════════════════════════════════════════════════

def agent_data_story(question_metier: str) -> str:
    """
    Transforme les données de la mémoire en narrative data story autour
    d'une question business : Contexte → Découverte → Et alors ? → Action.
    Format accessible aux non-techniciens, style consultant McKinsey.

    Args:
        question_metier : La question business à investiguer
                          (ex: "Pourquoi nos revenus stagnent-ils ?")
    """
    incrementer_stat("agent_data_data_story")
    memoire = charger_memoire()

    print(_titre(f"DATA STORY — {ENTREPRISE}"))
    print(f"  Question : {question_metier}\n")

    clients = memoire.get("clients", {})
    factures = memoire.get("factures", [])
    interactions = memoire.get("interactions", [])
    projets = memoire.get("projets", {})
    stats = memoire.get("stats", {})
    tickets = memoire.get("tickets", [])

    # ── Compilation des faits clés ──
    nb_clients_actifs = sum(1 for c in clients.values() if c.get("statut") == "actif")
    nb_prospects = sum(1 for c in clients.values() if c.get("statut") == "prospect")
    taux_conv = round(nb_clients_actifs / max(len(clients), 1) * 100, 1)

    revenus_total = sum(f.get("total_ttc", 0) for f in factures)
    revenus_encaisses = sum(f.get("total_ttc", 0) for f in factures if f.get("payee"))
    revenus_en_attente = revenus_total - revenus_encaisses

    agents_utilises = stats.get("agents_utilises", {})
    total_demandes = stats.get("total_demandes", 0)
    top_agents = sorted(agents_utilises.items(), key=lambda x: x[1], reverse=True)[:5]

    secteurs = Counter(data.get("secteur", "N/A") for data in clients.values())
    top_secteurs = secteurs.most_common(5)

    tickets_resolus = sum(1 for t in tickets if t.get("resolu"))
    taux_resolution = round(tickets_resolus / max(len(tickets), 1) * 100, 1)

    nb_projets_actifs = sum(1 for p in projets.values() if p.get("statut") not in ("terminé", "annulé"))

    # Revenus par mois (dernier trimestre)
    revenus_par_mois = defaultdict(float)
    for f in factures:
        date_str = f.get("date_emission", "")
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str)
                cle = dt.strftime("%Y-%m")
                revenus_par_mois[cle] += f.get("total_ttc", 0)
            except Exception:
                pass
    mois_recents = sorted(revenus_par_mois.keys())[-3:]
    tendance_revenus = [revenus_par_mois[m] for m in mois_recents]
    if len(tendance_revenus) >= 2:
        evolution_rev = (tendance_revenus[-1] - tendance_revenus[0]) / max(tendance_revenus[0], 1) * 100
    else:
        evolution_rev = 0

    # Churn risk count
    churn_elevé = sum(
        1 for nom, data in clients.items()
        if data.get("statut") == "actif" and _jours_depuis(max(
            [i.get("date", "") for i in data.get("interactions", []) if i.get("date")] or [data.get("date_ajout", "")],
            default=data.get("date_ajout", "")
        )) > 60
    )

    # ── Affichage des données compilées ──
    print(_sep("─"))
    print("  DONNÉES MOBILISÉES POUR L'ANALYSE")
    print(_sep("─"))
    print(f"  Clients actifs      : {nb_clients_actifs}")
    print(f"  Prospects           : {nb_prospects}")
    print(f"  Taux conversion     : {taux_conv}%")
    print(f"  Revenus total       : {revenus_total:,.0f}€")
    print(f"  Revenus encaissés   : {revenus_encaisses:,.0f}€")
    print(f"  Évolution revenus   : {evolution_rev:+.1f}% (3 derniers mois)")
    print(f"  Clients churn risk  : {churn_elevé}")
    print(f"  Tickets résolus     : {taux_resolution}%")
    print(f"  Requêtes agents     : {total_demandes}")
    print()

    prompt = f"""Tu es un consultant senior chez McKinsey & Company, expert en stratégie et data storytelling pour {ENTREPRISE}, spécialisée en agents IA autonomes.

Un dirigeant te pose cette question : "{question_metier}"

Voici TOUTES les données disponibles sur l'entreprise :

CLIENTS & ACQUISITION :
- Clients actifs : {nb_clients_actifs}
- Prospects en pipeline : {nb_prospects}
- Taux de conversion : {taux_conv}%
- Clients à risque churn élevé : {churn_elevé}
- Top secteurs clients : {", ".join(f"{s}({n})" for s, n in top_secteurs)}

REVENUS :
- Revenus totaux facturés : {revenus_total:,.0f}€
- Revenus encaissés : {revenus_encaisses:,.0f}€
- Revenus en attente de paiement : {revenus_en_attente:,.0f}€
- Évolution récente (3 mois) : {evolution_rev:+.1f}%
- Derniers mois : {", ".join(f"{m}:{revenus_par_mois[m]:,.0f}€" for m in mois_recents)}

OPÉRATIONS :
- Projets actifs : {nb_projets_actifs}
- Taux résolution tickets : {taux_resolution}%
- Total requêtes agents : {total_demandes}
- Agents les plus utilisés : {", ".join(f"{a}({c})" for a, c in top_agents)}

En français, transforme ces données en une DATA STORY complète pour un dirigeant non-technique :

═══════════════════════════════════
1. LE CONTEXTE (Slide 1 McKinsey)
   "Voici où nous en sommes aujourd'hui..."
   (État actuel en 3 chiffres clés percutants avec leur interprétation)

2. LA DÉCOUVERTE (Slide 2 McKinsey)
   "Voici ce que les données révèlent..."
   (Le fait central qui répond à la question — surprenant ou contre-intuitif)

3. LES PREUVES (Slide 3 McKinsey)
   "Voici les 3 signaux qui confirment..."
   (3 data points précis qui soutiennent la découverte)

4. ET ALORS ? — L'ENJEU (Slide 4 McKinsey)
   "Si on ne fait rien, voici ce qui se passe..."
   (Conséquences chiffrées de l'inaction — opportunité manquée ou risque)

5. LA RECOMMANDATION (Slide 5 McKinsey)
   "Voici notre recommandation unique..."
   (UNE action prioritaire claire, avec timing et responsable)

6. LE PLAN D'ACTION (Slide 6 McKinsey)
   "Voici les 3 prochaines étapes concrètes..."
   (30j / 60j / 90j avec indicateur de succès pour chacune)

═══════════════════════════════════

Règles :
- Langage clair, accessible à un non-technicien
- Chaque section = 2-4 phrases maximum (comme une vraie slide)
- Commence chaque section par une phrase choc/accroche
- Utilise les données disponibles — cite des chiffres précis
- Ton : confiant, stratégique, orienté action
"""

    print("  Création de la data story en cours...\n")
    print(_sep("─"))
    print("  DATA STORY (IA — Style McKinsey)")
    print(_sep("─"))
    reponse = _streamer(prompt, temperature=0.65)

    contenu_rapport = f"DATA STORY — {ENTREPRISE}\n"
    contenu_rapport += f"Question : {question_metier}\n"
    contenu_rapport += f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    contenu_rapport += "=" * LARGEUR + "\n\n"
    contenu_rapport += reponse

    chemin = _sauvegarder_rapport("data_story", contenu_rapport)
    print(f"  Rapport sauvegardé → {chemin}\n")

    return reponse


# ═══════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def afficher_menu():
    print("\n" + "═" * LARGEUR)
    print(f"  AGENT DATA SCIENCE & BI — {ENTREPRISE}")
    print(f"  Expert en analyse, segmentation et prévisions")
    print("═" * LARGEUR)
    print("  1. Analyser un fichier CSV")
    print("  2. Insights profonds — Mémoire entreprise")
    print("  3. Rapport de performance (agents, support, revenus)")
    print("  4. Segmentation clients & ICP")
    print("  5. Prévision des ventes (régression linéaire)")
    print("  6. Data Story — Question business en narrative")
    print("  0. Quitter")
    print("═" * LARGEUR)


def menu():
    while True:
        afficher_menu()
        choix = input("\n  Votre choix → ").strip()

        if choix == "0":
            print("\n  Au revoir. Les rapports sont disponibles dans fichiers/data/\n")
            break

        elif choix == "1":
            print("\n  Analyse de fichier CSV")
            print("  " + "─" * 40)
            chemin = input("  Chemin du fichier CSV → ").strip()
            if not chemin:
                print("  Chemin requis.")
                continue
            agent_analyser_csv(chemin)

        elif choix == "2":
            agent_insights_memoire()

        elif choix == "3":
            print("\n  Rapport de performance")
            print("  " + "─" * 40)
            print("  Périodes disponibles : 7j, 30j, 90j, tout")
            periode = input("  Période → ").strip()
            if not periode:
                periode = "30j"
                print(f"  Période par défaut : {periode}")
            agent_rapport_performance(periode)

        elif choix == "4":
            agent_segmentation_clients()

        elif choix == "5":
            print("\n  Prévision des ventes")
            print("  " + "─" * 40)
            print("  Entrez vos données historiques (format libre) :")
            print("  Exemple : 'Jan 2024: 5000, Fév 2024: 6200, Mars 2024: 5800'")
            print("  Ou copiez plusieurs lignes (terminez par une ligne vide) :")
            lignes = []
            while True:
                ligne = input("  → ").strip()
                if not ligne:
                    break
                lignes.append(ligne)
            donnees = ", ".join(lignes)
            if not donnees:
                print("  Données requises.")
                continue
            agent_prevision_ventes(donnees)

        elif choix == "6":
            print("\n  Data Story — Question Business")
            print("  " + "─" * 40)
            print("  Exemples : 'Pourquoi nos revenus stagnent-ils ?'")
            print("             'Comment améliorer notre taux de conversion ?'")
            print("             'Quels clients devons-nous prioriser ?'")
            question = input("  Votre question → ").strip()
            if not question:
                print("  Question requise.")
                continue
            agent_data_story(question)

        else:
            print("  Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    menu()

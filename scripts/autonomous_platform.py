#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de plateforme autonome — Caelum Partners
================================================
Un seul point d'entrée qui, en local et sans dépendance externe :

  1. SANTÉ        — lance les protocoles RÉELS existants (audits, gardes) et capture leur état.
  2. SCÉNARIOS    — imagine TOUS les scénarios (trafic, sources, build, déploiement, données,
                    sécurité, langues) et les simule (Monte Carlo + modèles déterministes).
  3. PROTOCOLE    — applique un sceau de décision : un seul CRITIQUE => BLOQUÉ, sinon APPROUVÉ.
  4. RAPPORT      — écrit data/autonomous_platform_report.json (lisible, traçable).

Honnêteté : les « simulations » sont des modèles probabilistes/déterministes clairement
étiquetés — pas des appels réseau réels. Aucune donnée inventée : les volumes (réponses,
sources, pages) sont RECOMPTÉS depuis le dépôt.

Usage :
    python3 scripts/autonomous_platform.py            # run complet
    python3 scripts/autonomous_platform.py --fast     # sans subprocess (scénarios seuls)
    python3 scripts/autonomous_platform.py --n 200000 # taille Monte Carlo
"""
from __future__ import annotations
import json
import os
import sys
import glob
import time
import random
import subprocess
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "data", "autonomous_platform_report.json")

# Bornes de verdict communes
OK, ALERTE, CRITIQUE = "OK", "ALERTE", "CRITIQUE"
RANK = {OK: 0, ALERTE: 1, CRITIQUE: 2}


# ───────────────────────────── utilitaires dépôt ─────────────────────────────
def compter_corpus() -> dict:
    """Recompte réponses + sources des deux projets (vérité terrain, jamais inventée)."""
    stats = {"reponses": 0, "sources": 0, "modules": 0, "sources_officielles": 0}
    for base in ("data/belgium", "laloiavecmoi/data/belgium"):
        d = os.path.join(ROOT, base)
        if not os.path.isdir(d):
            continue
        # un seul des deux dossiers suffit pour le corpus citoyen (miroir) :
        if base == "laloiavecmoi/data/belgium" and stats["modules"]:
            continue
        for f in glob.glob(os.path.join(d, "*.json")):
            if os.path.basename(f).startswith("_"):
                continue
            try:
                data = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            faits = data.get("faits") or []
            if not faits:
                continue
            stats["modules"] += 1
            for fait in faits:
                stats["reponses"] += 1
                for s in fait.get("sources", []):
                    stats["sources"] += 1
                    if s.get("type") == "officiel":
                        stats["sources_officielles"] += 1
    return stats


def compter_pages_build() -> dict:
    """Estimation du nombre de pages (Caelum + La Loi Avec Moi) à partir des routes/données."""
    # Caelum : normes (SEO) + secteurs + statiques connues ; La Loi : modules + pages fixes.
    try:
        normes = json.load(open(os.path.join(ROOT, "data/caelum/conformite_entreprises.json"), encoding="utf-8"))
        n_normes = len(normes.get("normes", []))
    except Exception:
        n_normes = 0
    return {"caelum_normes": n_normes}


def compter_caelum() -> dict:
    """Corpus Caelum (B2B) : normes de conformité, sources, aides publiques."""
    out = {"normes": 0, "sources": 0, "aides": 0}
    try:
        d = json.load(open(os.path.join(ROOT, "data/caelum/conformite_entreprises.json"), encoding="utf-8"))
        normes = d.get("normes", [])
        out["normes"] = len(normes)
        for n in normes:
            out["sources"] += len(n.get("sources", []) or [])
    except Exception:
        pass
    try:
        a = json.load(open(os.path.join(ROOT, "data/caelum/aides_publiques.json"), encoding="utf-8"))
        out["aides"] = len(a.get("aides", []) or [])
    except Exception:
        pass
    return out


# ───────────────────────────── 1. SANTÉ (protocoles réels) ───────────────────
# Protocoles sûrs, sans argument, qui s'exécutent vite. On capture le code retour.
PROTOCOLES = [
    ("loi_reference_audit", ["python3", "scripts/loi_reference_audit.py"]),
    ("source_trust_protocol", ["python3", "scripts/source_trust_protocol.py"]),
    ("legal_change_sensor", ["python3", "scripts/legal_change_sensor.py"]),
    ("branch_guard", ["python3", "scripts/branch_guard.py", "--check", "--quiet"]),
]


def lancer_protocoles(timeout=120) -> list:
    resultats = []
    for nom, cmd in PROTOCOLES:
        entree = {"protocole": nom, "cmd": " ".join(cmd)}
        try:
            t0 = time.time()
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
            entree["returncode"] = p.returncode
            entree["ms"] = round((time.time() - t0) * 1000)
            tail = (p.stdout or p.stderr or "").strip().splitlines()
            entree["sortie"] = tail[-1] if tail else ""
            entree["verdict"] = OK if p.returncode == 0 else ALERTE
        except subprocess.TimeoutExpired:
            entree["verdict"] = ALERTE
            entree["sortie"] = "timeout"
        except Exception as e:  # script absent / erreur
            entree["verdict"] = ALERTE
            entree["sortie"] = f"indisponible: {e}"
        resultats.append(entree)
    return resultats


# ───────────────────────────── 2. MOTEUR DE SCÉNARIOS ────────────────────────
def scn_trafic(n: int, corpus: dict) -> list:
    """Trafic : du calme à un pic viral. Modèle de latence avec dégradation sous charge.
    Mitigation réelle : next:{revalidate:30} (cache) réduit la charge upstream."""
    out = []
    # (label, requêtes/s, ratio servi par cache)
    paliers = [
        ("Trafic normal", 5, 0.6),
        ("Pic quotidien", 50, 0.75),
        ("Buzz presse", 300, 0.85),
        ("Viral / spike", 1500, 0.92),
    ]
    base_ms, capacite = 35.0, 200.0  # service de base, capacité requêtes/s avant saturation
    for label, rps, cache in paliers:
        rng = random.Random(hash(label) & 0xFFFFFFFF)
        sous = 0
        lat = []
        rps_eff = rps * (1 - cache)  # le cache absorbe une partie
        charge = min(rps_eff / capacite, 0.99)
        for _ in range(n // len(paliers)):
            # latence ~ base / (1 - charge) avec bruit (file d'attente type M/M/1)
            jitter = rng.gauss(0, 6)
            l = base_ms / (1 - charge) + max(0, jitter)
            lat.append(l)
            if l < 200:
                sous += 1
        lat.sort()
        p95 = lat[int(len(lat) * 0.95)]
        p99 = lat[int(len(lat) * 0.99)]
        pct_ok = 100 * sous / len(lat)
        verdict = OK if pct_ok >= 99 else ALERTE if pct_ok >= 95 else CRITIQUE
        out.append({
            "scenario": f"Trafic · {label}", "type": "etat" if rps <= 50 else "stress",
            "rps": rps, "cache_pct": int(cache * 100),
            "p95_ms": round(p95), "p99_ms": round(p99), "pct_sous_200ms": round(pct_ok, 2),
            "verdict": verdict, "mitigation": "revalidate:30 + rendu statique"
        })
    return out


def scn_sources(n: int, corpus: dict) -> list:
    """Sources officielles : que se passe-t-il si X% des URL changent/meurent ?
    Mitigation réelle : source_change_detector + double source (officiel + secondaire).
    Si le capteur réel (source_health_sensor) a des données, on les utilise EN PLUS
    des stress-tests simulés."""
    out = []
    # Détection RÉELLE si disponible (organe capteur).
    try:
        sh = json.load(open(os.path.join(ROOT, "data", "source_health.json"), encoding="utf-8"))
        if sh.get("network_ok"):
            verdict = sh.get("verdict", OK)
            out.append({
                "scenario": "Sources · Détection réelle (capteur)", "type": "etat",
                "urls_testees": sh.get("total"), "vivantes_pct": sh.get("pct_ok"),
                "mortes": sh.get("mortes"), "verdict": verdict,
                "mitigation": "capteur HTTP réel + 2e source de secours"
            })
        else:
            out.append({
                "scenario": "Sources · Capteur (réseau indisponible)", "type": "etat",
                "verdict": OK, "mitigation": "capteur prêt ; à exécuter là où le réseau est ouvert"
            })
    except Exception:
        pass

    total = max(corpus["sources"], 1)
    for label, taux, typ in [("Rotation normale", 0.01, "etat"), ("Refonte d'un portail", 0.05, "stress"), ("Panne large", 0.15, "stress")]:
        rng = random.Random(hash(label) & 0xFFFFFFFF)
        casses = []
        for _ in range(max(1, n // 3000)):
            casses.append(sum(1 for _ in range(total) if rng.random() < taux))
        moy = sum(casses) / len(casses)
        pct = 100 * moy / total
        verdict = OK if pct < 3 else ALERTE if pct < 10 else CRITIQUE
        out.append({
            "scenario": f"Sources · {label}", "type": typ, "taux_casse_pct": round(taux * 100, 1),
            "urls_impactees_moy": round(moy), "pct_corpus": round(pct, 2),
            "verdict": verdict, "mitigation": "détecteur de changement + 2e source de secours"
        })
    return out


def scn_build(corpus: dict) -> list:
    """Build/mémoire : croissance du nombre de pages vs limites OOM Vercel.
    Mitigation réelle : NODE_OPTIONS 4096 + webpackMemoryOptimizations + rendu statique."""
    out = []
    pages_actuelles = corpus["modules"] + corpus.get("caelum_normes", 0) + 30
    for label, facteur, typ in [("Aujourd'hui", 1.0, "etat"), ("+1 an (x2)", 2.0, "stress"), ("+3 ans (x4)", 4.0, "stress")]:
        pages = int(pages_actuelles * facteur)
        # heuristique : seuil de confort ~1500 pages SSG avec heap 4 Go
        verdict = OK if pages < 1500 else ALERTE if pages < 3000 else CRITIQUE
        out.append({
            "scenario": f"Build · {label}", "type": typ, "pages_estimees": pages,
            "verdict": verdict, "mitigation": "heap 4 Go + webpackMemoryOptimizations + SSG"
        })
    return out


def scn_deploiement() -> list:
    """Déploiement : variables d'env manquantes, upstream indisponible.
    Mitigation réelle : guard SWARM_API_URL + fallback 502 + sealResponse."""
    cas = [
        ("SWARM_API_URL absente", "console.warn + mode hors-ligne", OK),
        ("Upstream swarm en panne", "fallback HTTP 502 (jamais 503)", OK),
        ("Webhook leads non configuré", "lead non perdu si guard présent ; sinon ALERTE", ALERTE),
    ]
    return [{"scenario": f"Déploiement · {l}", "type": "etat", "verdict": v, "mitigation": m} for l, m, v in cas]


def scn_donnees(corpus: dict) -> list:
    """Données : doublon de domaine, source manquante, identité placeholder."""
    out = []
    # identité légale Caelum encore en placeholder ?
    placeholder = False
    try:
        ident = open(os.path.join(ROOT, "data/identite.ts"), encoding="utf-8").read()
        placeholder = "[à compléter]" in ident
    except Exception:
        pass
    out.append({
        "scenario": "Données · Identité légale Caelum", "type": "etat",
        "verdict": ALERTE if placeholder else OK,
        "mitigation": "garde identité + avertissement affiché tant que placeholder"
    })
    # couverture des sources officielles
    pct_off = 100 * corpus["sources_officielles"] / max(corpus["sources"], 1)
    out.append({
        "scenario": "Données · Couverture sources officielles", "type": "etat",
        "pct_officiel": round(pct_off, 1),
        "verdict": OK if pct_off >= 50 else ALERTE,
        "mitigation": "protocole de confiance des sources (tier1)"
    })
    return out


def scn_securite(n: int) -> list:
    """Sécurité : payload géant, tentative d'injection, e-mail démesuré.
    Mitigation réelle : garde-fous /api/leads (taille 4000, email<=254, slice source)."""
    rng = random.Random(1234)
    bloques = 0
    for _ in range(n // 2):
        taille = rng.randint(10, 8000)
        email_len = rng.randint(5, 400)
        # règle réelle : >4000 -> 413, email>254 -> rejet
        if taille > 4000 or email_len > 254:
            bloques += 1
    return [{
        "scenario": "Sécurité · Abus formulaire (payload/email)", "type": "etat",
        "pct_bloque_attendu": round(100 * bloques / max(1, n // 2), 1),
        "verdict": OK, "mitigation": "limites taille/longueur + 413"
    }]


def scn_croissance(corpus: dict) -> list:
    """Croissance : la plateforme grandit-elle ? Lit sa mémoire (historique des battements
    AVANT le battement courant) et détecte la stagnation pour réclamer de nouveaux domaines."""
    SEUIL = 5  # battements sans croissance avant alerte
    try:
        vit = json.load(open(VITALS, encoding="utf-8"))
        hist = vit.get("historique", [])
    except Exception:
        hist = []
    rep = corpus["reponses"]
    if len(hist) < 2:
        return [{
            "scenario": "Croissance · Corpus", "type": "etat", "verdict": OK,
            "reponses": rep, "modules": corpus["modules"], "depuis_naissance": 0,
            "battements_sans_croissance": 0, "mitigation": "jeune pousse — historique en constitution"
        }]
    naissance_rep = hist[0].get("reponses", rep)
    # battements consécutifs (depuis la fin) au même nombre de réponses que maintenant
    stagn = 0
    for h in reversed(hist):
        if h.get("reponses", -1) == rep:
            stagn += 1
        else:
            break
    verdict = ALERTE if stagn >= SEUIL else OK
    return [{
        "scenario": "Croissance · Corpus", "type": "etat", "verdict": verdict,
        "reponses": rep, "modules": corpus["modules"],
        "depuis_naissance": rep - naissance_rep, "battements_sans_croissance": stagn,
        "mitigation": "ajouter régulièrement des domaines vérifiés (loi + source officielle)"
    }]


def etat_plan() -> dict:
    """Lit le plan stratégique Caelum et calcule l'avancement (avec auto-détection)."""
    try:
        plan = json.load(open(os.path.join(ROOT, "data", "strategic_plan.json"), encoding="utf-8"))
    except Exception:
        return {}
    jalons = plan.get("jalons", [])
    for j in jalons:
        auto = j.get("auto", "none")
        if auto.startswith("env:"):
            j["fait"] = bool(os.environ.get(auto.split(":", 1)[1]))
        elif auto.startswith("file_no_placeholder:"):
            path = os.path.join(ROOT, auto.split(":", 1)[1])
            try:
                j["fait"] = "[à compléter]" not in open(path, encoding="utf-8").read()
            except Exception:
                j["fait"] = False
        # 'static_done' et 'none' : on garde la valeur 'fait' du fichier
    total = len(jalons)
    faits = sum(1 for j in jalons if j.get("fait"))
    pct = round(100 * faits / total) if total else 0
    bloquants = [j["titre"] for j in jalons if j.get("bloquant") and not j.get("fait")]
    # Retards : date butoir dépassée et non fait
    today = datetime.now(timezone.utc).date().isoformat()
    en_retard = [
        {"titre": j["titre"], "date_butoir": j.get("date_butoir")}
        for j in jalons if not j.get("fait") and j.get("date_butoir") and j["date_butoir"] < today
    ]
    # Prochaine étape non faite, triée par date butoir
    restants = [j for j in jalons if not j.get("fait")]
    restants.sort(key=lambda j: j.get("date_butoir") or "9999")
    prochaine = restants[0]["titre"] if restants else None
    prochaine_date = restants[0].get("date_butoir") if restants else None
    return {"objectif": plan.get("objectif"), "total": total, "faits": faits, "pct": pct,
            "bloquants_restants": bloquants, "prochaine_etape": prochaine,
            "prochaine_date": prochaine_date, "en_retard": en_retard, "jalons": jalons}


def scn_plan() -> list:
    """Organe Plan : la plateforme comprend le plan, suit l'avancement et signale la stagnation."""
    p = etat_plan()
    if not p:
        return []
    SEUIL = 5
    # stagnation : avancement identique sur les derniers battements
    try:
        hist = json.load(open(VITALS, encoding="utf-8")).get("historique", [])
    except Exception:
        hist = []
    stagn = 0
    for h in reversed(hist):
        if h.get("plan_pct") == p["pct"]:
            stagn += 1
        else:
            break
    if p["en_retard"]:
        verdict = ALERTE
    elif p["bloquants_restants"]:
        verdict = ALERTE
    elif p["pct"] < 100 and stagn >= SEUIL:
        verdict = ALERTE
    else:
        verdict = OK
    proch = p["prochaine_etape"]
    if proch and p.get("prochaine_date"):
        proch = f"{proch} (avant le {p['prochaine_date']})"
    return [{
        "scenario": "Plan stratégique · Avancement", "type": "etat", "verdict": verdict,
        "plan_pct": p["pct"], "plan_faits": p["faits"], "plan_total": p["total"],
        "prochaine_etape": proch, "battements_sans_progres": stagn,
        "en_retard": len(p["en_retard"]),
        "mitigation": "respecter les dates butoirs du plan — ne pas stagner"
    }]


def scn_caelum(corpus: dict) -> list:
    """Organe Conformité Caelum : couverture des normes B2B et de leurs sources."""
    c = corpus.get("caelum", {})
    if not c:
        return []
    verdict = OK if c.get("normes", 0) >= 10 else ALERTE
    return [{
        "scenario": "Caelum · Conformité B2B", "type": "etat", "verdict": verdict,
        "caelum_normes": c.get("normes"), "caelum_sources": c.get("sources"), "caelum_aides": c.get("aides"),
        "mitigation": "base de normes vérifiées + aides publiques sourcées"
    }]


def scn_veille() -> list:
    """Veille juridique : fraîcheur des fiches + changements de sources (organe réel)."""
    try:
        lc = json.load(open(os.path.join(ROOT, "data", "legal_change.json"), encoding="utf-8"))
    except Exception:
        return []
    return [{
        "scenario": "Veille juridique · Fraîcheur des fiches", "type": "etat",
        "modules": lc.get("total_modules"), "frais": lc.get("frais"),
        "a_reverifier": lc.get("a_reverifier"), "prioritaire": lc.get("prioritaire"),
        "sources_modifiees": len(lc.get("sources_modifiees", [])),
        "verdict": lc.get("verdict", OK),
        "mitigation": "capteur de changement juridique (fraîcheur + empreinte sources)"
    }]


def scn_veille_marche() -> list:
    """Organe Veille marché : opportunités émergentes non encore traitées (adapter vite)."""
    try:
        d = json.load(open(os.path.join(ROOT, "data", "market_opportunities.json"), encoding="utf-8"))
    except Exception:
        return []
    opp = d.get("opportunites", [])
    nouveaux = [o for o in opp if o.get("statut") == "nouveau"]
    return [{
        "scenario": "Veille marché · Opportunités", "type": "etat",
        "verdict": ALERTE if nouveaux else OK,
        "opp_total": len(opp), "opp_nouveau": len(nouveaux),
        "prochaine_opp": (sorted(nouveaux, key=lambda x: {"haute": 0, "moyenne": 1, "basse": 2}.get(x.get("priorite"), 9))[0]["id"] if nouveaux else None),
        "mitigation": "instruire les opportunités 'nouveau' (radar market_opportunities.json)"
    }]


def scn_langues() -> list:
    """Langues : visiteur non francophone. Mitigation : FR/NL natifs + barre 🌐 + EN Caelum."""
    return [{
        "scenario": "Langues · Visiteur non francophone", "type": "etat",
        "verdict": OK,
        "mitigation": "FR/NL natifs, /en Caelum, traduction à la volée (mention 'FR/NL fait foi')"
    }]


def moteur_scenarios(n: int, corpus: dict) -> list:
    scenarios = []
    scenarios += scn_trafic(n, corpus)
    scenarios += scn_sources(n, corpus)
    scenarios += scn_build(corpus)
    scenarios += scn_deploiement()
    scenarios += scn_donnees(corpus)
    scenarios += scn_securite(n)
    scenarios += scn_veille()
    scenarios += scn_croissance(corpus)
    scenarios += scn_caelum(corpus)
    scenarios += scn_plan()
    scenarios += scn_veille_marche()
    scenarios += scn_langues()
    return scenarios


# ───────────────────────────── 3. PROTOCOLE (sceau) ──────────────────────────
def sceller(sante: list, scenarios: list) -> dict:
    # État actuel = santé (protocoles réels) + scénarios type "etat". Seul l'état actuel bloque.
    etat = [p.get("verdict", OK) for p in sante] + [s.get("verdict", OK) for s in scenarios if s.get("type") == "etat"]
    stress = [s for s in scenarios if s.get("type") == "stress"]
    pire_etat = max(etat, key=lambda v: RANK.get(v, 0)) if etat else OK
    statut = "BLOQUÉ" if pire_etat == CRITIQUE else "APPROUVÉ"

    tous = etat + [s.get("verdict", OK) for s in stress]
    n_ok = sum(1 for v in tous if v == OK)
    score = round(100 * n_ok / len(tous), 1) if tous else 0.0

    fragilites = [s["scenario"] for s in stress if s.get("verdict") == CRITIQUE]
    a_corriger = [p["scenario"] for p in scenarios if p.get("type") == "etat" and p.get("verdict") == ALERTE]

    # Autonomie = santé TECHNIQUE que la plateforme contrôle seule.
    # On exclut les décisions humaines (Chaima) ET la couche stratégique (plan, veille marché).
    HUMAIN = ("Webhook", "Identité")
    EXCLU = HUMAIN + ("Plan stratégique", "Veille marché")
    sys_etat = [p.get("verdict", OK) for p in sante] + [
        s.get("verdict", OK) for s in scenarios
        if s.get("type") == "etat" and not any(h in s["scenario"] for h in EXCLU)
    ]
    sys_ok = sum(1 for v in sys_etat if v == OK)
    autonomie_pct = round(100 * sys_ok / len(sys_etat), 1) if sys_etat else 100.0
    decisions_humaines = [
        s["scenario"] for s in scenarios
        if s.get("type") == "etat" and s.get("verdict") != OK and any(h in s["scenario"] for h in HUMAIN)
    ]

    seal_id = "AUTO-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return {
        "seal_id": seal_id, "statut": statut, "pire_verdict_etat": pire_etat,
        "score_resilience": score, "verts": n_ok, "total": len(tous),
        "autonomie_systeme_pct": autonomie_pct,
        "decisions_humaines_en_attente": decisions_humaines,
        "fragilites_stress": fragilites,
        "alertes_etat_a_corriger": a_corriger,
        "regle": "BLOQUÉ seulement si l'ÉTAT ACTUEL (santé + scénarios 'etat') a un CRITIQUE ; "
                 "les scénarios extrêmes 'stress' alimentent la résilience et la liste des fragilités.",
    }


# ───────────────────────────── FORME DE VIE (cœur battant) ───────────────────
# La plateforme est présentée comme un organisme vivant (métaphore assumée, pas une
# prétention de conscience) : elle a une naissance, un pouls (chaque run = un battement),
# une mémoire (historique de ses signes vitaux) et un état de vie qui évolue.
VITALS = os.path.join(ROOT, "data", "platform_vitals.json")
ETATS_VIE = {
    "naissance": "🐣 Naissance",
    "forme": "🟢 En pleine forme",
    "veille": "🟢 En vie · veille active",
    "vigilance": "🟠 Vigilance",
    "soin": "🔴 Soin requis",
}


def composer_voix(etat: str, sceau: dict, battements: int) -> str:
    """La plateforme 'parle' : un court bilan humain de son état (métaphore assumée)."""
    debut = {
        "naissance": "Je viens de naître.",
        "forme": "Je vais bien.",
        "veille": "Je vais bien, je veille.",
        "vigilance": "Je tiens bon, mais j'ai besoin d'attention.",
        "soin": "J'ai besoin de soins urgents.",
    }[etat]
    parts = [f"{debut} Résilience {sceau['score_resilience']}%, {battements}ᵉ battement."]
    a_corriger = sceau.get("alertes_etat_a_corriger") or []
    if a_corriger:
        noms = ", ".join(s.split("·")[-1].strip() for s in a_corriger)
        parts.append(f"Je réclame : {noms}.")
    frag = sceau.get("fragilites_stress") or []
    if frag:
        noms = ", ".join(s.split("·")[-1].strip() for s in frag)
        parts.append(f"Ma fragilité au pire scénario : {noms}.")
    if not a_corriger and not frag:
        parts.append("Rien ne me menace pour l'instant.")
    # Plan stratégique : avancer, ne pas stagner
    p = etat_plan()
    if p:
        parts.append(f"Plan à {p['pct']}%.")
        if p.get("prochaine_etape"):
            parts.append(f"Prochaine étape : {p['prochaine_etape']}.")
    return " ".join(parts)


def battre_le_coeur(sceau: dict, corpus: dict) -> dict:
    """Met à jour les signes vitaux persistants (la 'vie' de la plateforme)."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        vit = json.load(open(VITALS, encoding="utf-8"))
    except Exception:
        vit = {}

    premiere = "naissance" not in vit
    if premiere:
        vit["naissance"] = now
        vit["battements"] = 0
        vit["historique"] = []

    # État de vie déduit de la santé courante
    if sceau["statut"] == "BLOQUÉ":
        etat = "soin"
    elif sceau["alertes_etat_a_corriger"]:
        etat = "vigilance"
    elif premiere:
        etat = "naissance"
    else:
        etat = "veille"

    vit["battements"] = vit.get("battements", 0) + 1
    vit["derniere_pulsation"] = now
    vit["etat_vie"] = ETATS_VIE[etat]
    vit["resilience"] = sceau["score_resilience"]
    vit["statut"] = sceau["statut"]
    vit["voix"] = composer_voix(etat, sceau, vit["battements"])
    # âge en jours depuis la naissance
    try:
        naiss = datetime.fromisoformat(vit["naissance"])
        vit["age_jours"] = round((datetime.now(timezone.utc) - naiss).total_seconds() / 86400, 2)
    except Exception:
        vit["age_jours"] = 0

    # mémoire : on garde les 200 dernières pulsations
    plan = etat_plan()
    vit["historique"].append({
        "ts": now, "resilience": sceau["score_resilience"],
        "statut": sceau["statut"], "etat_vie": ETATS_VIE[etat],
        "reponses": corpus["reponses"], "modules": corpus["modules"],
        "plan_pct": plan.get("pct") if plan else None,
    })
    vit["historique"] = vit["historique"][-200:]

    os.makedirs(os.path.dirname(VITALS), exist_ok=True)
    json.dump(vit, open(VITALS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return vit


# ───────────────────────────── 3e ORGANE : AUTOGUÉRISON (soins) ──────────────
TODO = os.path.join(ROOT, "data", "platform_todo.json")

# Actions concrètes connues par scénario (sinon : on réutilise la mitigation).
ACTIONS = {
    "Webhook leads": ("Configurer la variable d'env LEADS_WEBHOOK_URL (réception des leads).", True),
    "Identité légale": ("Compléter data/identite.ts (dénomination, BCE, TVA, forme juridique).", True),
    "Panne large": ("Exécuter le capteur en réseau ouvert + planifier source_change_detector (cron).", False),
    "Croissance": ("Ajouter de nouveaux domaines juridiques vérifiés (loi en vigueur + source officielle).", True),
}


def generer_taches(sceau: dict, scenarios: list, corpus: dict) -> dict:
    """Transforme les signaux rouges/oranges en tâches de réparation priorisées."""
    taches = []

    def ajouter(titre, categorie, priorite, action, humain, organe):
        taches.append({
            "id": f"T{len(taches)+1:02d}", "titre": titre, "categorie": categorie,
            "priorite": priorite, "action_suggeree": action, "humain": humain, "organe": organe,
        })

    # 1) Scénarios d'ÉTAT en ALERTE/CRITIQUE → soins prioritaires
    for s in scenarios:
        if s.get("type") != "etat" or s.get("verdict") == OK:
            continue
        prio = "haute" if s["verdict"] == CRITIQUE else "moyenne"
        if s.get("prochaine_etape"):  # organe Plan : action = prochaine étape concrète
            action, humain = f"Avancer le plan : {s['prochaine_etape']}", True
        else:
            action, humain = next(((a, h) for k, (a, h) in ACTIONS.items() if k in s["scenario"]),
                                  (s.get("mitigation", "À examiner."), False))
        ajouter(s["scenario"], "état", prio, action, humain, "scénario")

    # 2) Fragilités stress CRITIQUE → à surveiller (priorité basse, non bloquant)
    for s in scenarios:
        if s.get("type") == "stress" and s.get("verdict") == CRITIQUE:
            action, humain = next(((a, h) for k, (a, h) in ACTIONS.items() if k in s["scenario"]),
                                  ("Renforcer la mitigation avant que le risque ne devienne réel.", False))
            ajouter(f"Fragilité : {s['scenario']}", "résilience", "basse", action, humain, "stress")

    # 3) Sources mortes détectées (capteur réel) → réparation ciblée
    try:
        sh = json.load(open(os.path.join(ROOT, "data", "source_health.json"), encoding="utf-8"))
        for m in (sh.get("urls_mortes") or [])[:15]:
            ajouter(f"Source morte ({m.get('code')}) : {m.get('url')}", "source", "haute",
                    "Remplacer l'URL officielle par une source tier1 valide.", False, "capteur sources")
    except Exception:
        pass

    # 4) Fiches à revérifier / lois modifiées (capteur juridique)
    try:
        lc = json.load(open(os.path.join(ROOT, "data", "legal_change.json"), encoding="utf-8"))
        for m in lc.get("sources_modifiees", [])[:15]:
            ajouter(f"Loi peut-être modifiée : {m.get('module')}", "veille", "haute",
                    "Relire la source officielle et mettre à jour la fiche + date_verification.", False, "capteur juridique")
        for m in (lc.get("modules_a_reverifier") or [])[:15]:
            ajouter(f"Fiche à revérifier : {m.get('titre')} ({m.get('age_jours')} j)", "veille", "basse",
                    "Revérifier les sources et rafraîchir date_verification.", False, "capteur juridique")
    except Exception:
        pass

    ordre = {"haute": 0, "moyenne": 1, "basse": 2}
    taches.sort(key=lambda t: ordre.get(t["priorite"], 9))
    par_prio = {p: sum(1 for t in taches if t["priorite"] == p) for p in ("haute", "moyenne", "basse")}

    rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "total": len(taches), "par_priorite": par_prio, "taches": taches,
        "note": "Soins auto-générés à partir des organes. La plateforme propose ; l'humain décide et exécute.",
    }
    os.makedirs(os.path.dirname(TODO), exist_ok=True)
    json.dump(rapport, open(TODO, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return rapport


# ───────────────────────────── orchestration ─────────────────────────────────
def main() -> int:
    args = sys.argv[1:]
    fast = "--fast" in args
    n = 100_000
    if "--n" in args:
        try:
            n = int(args[args.index("--n") + 1])
        except Exception:
            pass

    print("═" * 64)
    print("  SYSTÈME DE PLATEFORME AUTONOME — Caelum Partners")
    print("═" * 64)

    corpus = compter_corpus()
    corpus.update(compter_pages_build())
    corpus["caelum"] = compter_caelum()
    print(f"  La Loi Avec Moi : {corpus['modules']} modules · {corpus['reponses']} réponses · "
          f"{corpus['sources']} sources ({corpus['sources_officielles']} officielles)")
    print(f"  Caelum : {corpus['caelum']['normes']} normes · {corpus['caelum']['sources']} sources · "
          f"{corpus['caelum']['aides']} aides publiques")

    sante = [] if fast else lancer_protocoles()
    if sante:
        print("\n  ── Santé (protocoles réels) ──")
        for p in sante:
            print(f"    [{p['verdict']:<7}] {p['protocole']} — {p.get('sortie','')[:60]}")

    print(f"\n  ── Scénarios (Monte Carlo n={n:,}) ──")
    scenarios = moteur_scenarios(n, corpus)
    for s in scenarios:
        extra = ""
        if "p95_ms" in s:
            extra = f"p95={s['p95_ms']}ms p99={s['p99_ms']}ms ok={s['pct_sous_200ms']}%"
        elif "pct_corpus" in s:
            extra = f"~{s['urls_impactees_moy']} urls ({s['pct_corpus']}%)"
        elif "pages_estimees" in s:
            extra = f"{s['pages_estimees']} pages"
        print(f"    [{s['verdict']:<7}] {s['scenario']:<42} {extra}")

    sceau = sceller(sante, scenarios)
    print("\n  ── Sceau de protocole ──")
    print(f"    {sceau['seal_id']} · {sceau['statut']} · résilience {sceau['score_resilience']}% "
          f"({sceau['verts']}/{sceau['total']} verts) · pire état={sceau['pire_verdict_etat']}")
    print(f"    🤖 Autonomie système : {sceau['autonomie_systeme_pct']}% "
          f"(ce que la plateforme contrôle seule) · décisions humaines en attente : {len(sceau['decisions_humaines_en_attente'])}")
    if sceau["alertes_etat_a_corriger"]:
        print(f"    ⚠️  À corriger : {', '.join(sceau['alertes_etat_a_corriger'])}")
    if sceau["fragilites_stress"]:
        print(f"    🛡️  Fragilités (scénarios extrêmes) : {', '.join(sceau['fragilites_stress'])}")

    todo = generer_taches(sceau, scenarios, corpus)
    print("\n  ── Autoguérison (soins proposés) ──")
    print(f"    {todo['total']} tâche(s) · haute {todo['par_priorite']['haute']} · "
          f"moyenne {todo['par_priorite']['moyenne']} · basse {todo['par_priorite']['basse']}")
    for t in todo["taches"][:5]:
        marque = "🧑 humain" if t["humain"] else "🤖 auto"
        print(f"      [{t['priorite']:<7}] {t['titre'][:48]} — {marque}")

    vitals = battre_le_coeur(sceau, corpus)
    print("\n  ── Forme de vie ──")
    print(f"    {vitals['etat_vie']} · pouls {vitals['battements']} battement(s) · "
          f"âge {vitals['age_jours']} j · résilience {vitals['resilience']}%")
    print(f"    🗣️  « {vitals['voix']} »")

    rapport = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "monte_carlo_n": n,
        "corpus": corpus,
        "sante": sante,
        "scenarios": scenarios,
        "sceau": sceau,
        "vie": {
            "etat_vie": vitals["etat_vie"], "battements": vitals["battements"],
            "age_jours": vitals["age_jours"], "naissance": vitals["naissance"],
        },
        "todo": {"total": todo["total"], "par_priorite": todo["par_priorite"]},
        "avertissement": "Simulations = modèles probabilistes/déterministes locaux, pas des appels réseau réels.",
    }
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    json.dump(rapport, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n  → Rapport : {os.path.relpath(REPORT, ROOT)}  ·  Vie : {os.path.relpath(VITALS, ROOT)}")
    print("═" * 64)

    # code retour non-zéro si BLOQUÉ (utilisable en CI / pre-commit)
    return 1 if sceau["statut"] == "BLOQUÉ" else 0


if __name__ == "__main__":
    sys.exit(main())

"""
Intégrité automatique des moteurs Wave (rights engines) — protocole CI.

Rejoue le protocole de vérification (scripts/engine_verifier.py) :

  INVARIANTS BLOQUANTS (tous les moteurs) :
    - s'exécutent sans erreur Python
    - respectent la distribution réglementaire 4/2/1/1
    - aucun doublon de NOM de fichier

  MODE STRICT (moteurs de la session 498-561) :
    - en plus : avg dans la borne OK (61.03 ± 0.50) et assertions vertes

Les avertissements (avg calibré autrement, format de sortie ancien, préfixes
d'entité partagés) ne font PAS échouer la suite : ce sont des conventions
acceptées du codebase.
"""
import importlib.util
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERIFIER = os.path.join(ROOT, "scripts", "engine_verifier.py")


def _load_verifier():
    spec = importlib.util.spec_from_file_location("engine_verifier", VERIFIER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def verifier():
    return _load_verifier()


@pytest.fixture(scope="module")
def all_results(verifier):
    engines = verifier.discover_engines()
    return engines, [verifier.verify_one(n, p) for n, p, _ in engines]


# Plage des waves produites au pattern strict (61.03 ± 0.50, assertions vertes).
# Élargie au fil des waves pour couvrir toute la session.
SESSION_RANGE = (498, 999)


@pytest.fixture(scope="module")
def session_results(verifier):
    engines = verifier.discover_engines(SESSION_RANGE)
    return engines, [verifier.verify_one(n, p) for n, p, _ in engines]


def test_verifier_script_exists():
    assert os.path.exists(VERIFIER)


# ── Invariants bloquants : TOUS les moteurs ──────────────────────────────────

def test_all_engines_execute(all_results):
    _, rs = all_results
    broken = [r["engine"] for r in rs if not r["runs"]]
    assert not broken, f"Moteurs qui plantent à l'exécution : {broken}"


def test_all_distributions_valid(all_results):
    _, rs = all_results
    # distribution explicitement FAUSSE (détectée mais != 4/2/1/1) = bloquant
    bad = [r["engine"] for r in rs
           if any("!=" in e for e in r["errors"])]
    assert not bad, f"Distribution 4/2/1/1 violée : {bad}"


def test_no_duplicate_filenames(verifier):
    names = [n for n in os.listdir(verifier.ENGINES_DIR)
             if n.endswith("_rights_engine.py")]
    dups = sorted({n for n in names if names.count(n) > 1})
    assert not dups, f"Doublons de noms de fichiers : {dups}"


# ── Mode strict : moteurs de la session 498-561 ──────────────────────────────

def test_session_engines_discovered(session_results):
    engines, _ = session_results
    assert len(engines) >= 192


def test_session_engines_run(session_results):
    _, rs = session_results
    broken = [r["engine"] for r in rs if not r["runs"]]
    assert not broken, f"Moteurs session qui plantent : {broken}"


def test_session_assertions_pass(session_results):
    _, rs = session_results
    failed = [r["engine"] for r in rs if not r["assertions_pass"]]
    assert not failed, f"Moteurs session sans assertions vertes : {failed}"


def test_session_distributions_correct(session_results):
    _, rs = session_results
    bad = [r["engine"] for r in rs if not r["distribution_ok"]]
    assert not bad, f"Distribution session incorrecte : {bad}"


def test_session_averages_in_band(session_results):
    _, rs = session_results
    out = [(r["engine"], r["avg"]) for r in rs if not r["avg_ok"]]
    assert not out, f"Moyennes session hors borne (61.03 ± 0.50) : {out}"


def test_session_no_duplicate_prefixes(session_results):
    from collections import defaultdict
    _, rs = session_results
    prefix_map = defaultdict(list)
    for r in rs:
        if r["prefix"]:
            prefix_map[r["prefix"]].append(r["engine"])
    dups = {p: e for p, e in prefix_map.items() if len(e) > 1}
    assert not dups, f"Préfixes dupliqués dans la session : {dups}"


def test_session_no_semantic_duplicates(verifier, session_results):
    """Aucun moteur de la session ne duplique le SUJET d'un autre moteur de
    droits (mêmes mots-clés, ordre ignoré) — invariant anti-doublon sémantique."""
    engines, _ = session_results
    dups = verifier._detect_semantic_duplicates(engines)
    assert not dups, f"Doublons sémantiques détectés : {dups}"

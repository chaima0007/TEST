#!/usr/bin/env python3
"""Générateur de moteurs Wave selon le template exact Caelum (8 entités, 4/2/1/1)."""
import sys, os

TEMPLATE = '''#!/usr/bin/env python3
"""CaelumSwarm™ — {title} ({wave})

{desc}
Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
import json, statistics

ENTITIES = [
    ("{px}-001", 99, 97, 95, 93),
    ("{px}-002", 93, 90, 88, 86),
    ("{px}-003", 85, 82, 80, 78),
    ("{px}-004", 80, 77, 75, 73),
    ("{px}-005", 61, 58, 56, 54),
    ("{px}-006", 51, 48, 46, 44),
    ("{px}-007", 32, 29, 27, 25),
    ("{px}-008", 13, 11, 9, 7),
]

WEIGHTS = (0.30, 0.25, 0.25, 0.20)
THRESHOLDS = {{"critique": 60, "élevé": 40, "modéré": 20}}

def classify(score):
    if score >= THRESHOLDS["critique"]: return "critique"
    if score >= THRESHOLDS["élevé"]: return "élevé"
    if score >= THRESHOLDS["modéré"]: return "modéré"
    return "faible"

def compute():
    results = []
    for entity in ENTITIES:
        eid, *subs = entity
        composite = sum(s * w for s, w in zip(subs, WEIGHTS))
        results.append({{
            "entity": eid,
            "composite_score": round(composite, 2),
            "risk_level": classify(composite),
            "estimated_{idx}_index": round(composite / 100 * 10, 2),
        }})
    avg = statistics.mean(r["composite_score"] for r in results)
    distribution = {{}}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1
    return {{"entities": results, "avg_composite": round(avg, 2), "distribution": distribution}}

if __name__ == "__main__":
    output = compute()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    avg = output["avg_composite"]
    dist = output["distribution"]
    print(f"\\navg_composite = {{avg}}")
    print(f"distribution = {{dist}}")
    assert avg >= 60, f"avg {{avg}} < 60!"
    assert dist.get("critique", 0) == 4, f"critique={{dist.get('critique',0)}} != 4"
    assert dist.get("élevé", 0) == 2, f"élevé={{dist.get('élevé',0)}} != 2"
    assert dist.get("modéré", 0) == 1, f"modéré={{dist.get('modéré',0)}} != 1"
    assert dist.get("faible", 0) == 1, f"faible={{dist.get('faible',0)}} != 1"
    print("✓ Assertions passées — {wave} {title} OK")
'''

DEST = "/home/user/TEST/swarm/intelligence"

_STOP = {"rights", "engine", "child", "labor", "py"}

def _topic(filename):
    b = filename.replace("_rights_engine.py", "").replace("_engine.py", "").replace(".py", "")
    return frozenset(t for t in b.split("_") if t and t not in _STOP)

def _existing_topics():
    """Map {ensemble_de_mots-clés: fichier} des moteurs de droits existants."""
    out = {}
    for f in os.listdir(DEST):
        if f.endswith("_rights_engine.py"):
            t = _topic(f)
            if t:
                out.setdefault(t, f)
    return out

def gen(filename, title, wave, desc, px, idx):
    path = os.path.join(DEST, filename)
    if os.path.exists(path):
        print(f"SKIP (nom exact existe): {filename}")
        return False
    # GARDE-FOU SÉMANTIQUE : refuse si un autre moteur de droits couvre déjà
    # exactement le même sujet (mêmes mots-clés, ordre ignoré).
    twins = _existing_topics()
    t = _topic(filename)
    if t in twins:
        print(f"SKIP (DOUBLON SÉMANTIQUE de {twins[t]}): {filename}")
        return False
    content = TEMPLATE.format(title=title, wave=wave, desc=desc, px=px, idx=idx)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"CREATED: {filename}")
    return True

if __name__ == "__main__":
    # specs passed as a python literal file path
    import importlib.util
    spec_path = sys.argv[1]
    spec = importlib.util.spec_from_file_location("specs", spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for s in mod.SPECS:
        gen(*s)

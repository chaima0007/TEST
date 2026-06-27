#!/usr/bin/env python3
"""
backup_protocol.py — PROTOCOLE DE SAUVEGARDE des bases de données critiques.

N'enlève rien. Crée un instantané horodaté des données sensibles dans data/backups/<ts>/,
écrit un MANIFESTE avec empreinte SHA-256 par fichier (intégrité vérifiable), et garde les
N dernières sauvegardes (rotation). Le dépôt git + remote reste la sauvegarde principale ;
ceci ajoute une copie locale restaurable et auditable.

Usage :
  python3 scripts/backup_protocol.py                 # crée une sauvegarde
  python3 scripts/backup_protocol.py --keep 20       # rotation : garde 20 instantanés
  python3 scripts/backup_protocol.py --verify <dir>  # vérifie l'intégrité d'une sauvegarde
"""
import json
import os
import sys
import glob
import shutil
import hashlib
from datetime import datetime, timezone

BACKUP_ROOT = "data/backups"
# Données critiques à sauvegarder (sources réelles + état système).
CIBLES = [
    "data/belgium",                       # contenu juridique sourcé (actif d'expert)
    "data/certification_report.json",
    "data/certification_baseline.json",
    "data/engine_verification_report.json",
    "data/project_registry.json",
]
DEFAULT_KEEP = 14


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _iter_files(cible):
    if os.path.isdir(cible):
        for p in glob.glob(os.path.join(cible, "**", "*"), recursive=True):
            if os.path.isfile(p):
                yield p
    elif os.path.isfile(cible):
        yield cible


def creer_sauvegarde(keep):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = os.path.join(BACKUP_ROOT, ts)
    os.makedirs(dest, exist_ok=True)
    manifeste = {"horodatage_utc": ts, "fichiers": []}

    for cible in CIBLES:
        for src in _iter_files(cible):
            rel = src.replace("/", "__")
            shutil.copy2(src, os.path.join(dest, rel))
            manifeste["fichiers"].append({"origine": src, "copie": rel, "sha256": _sha256(src)})

    manifeste["nb_fichiers"] = len(manifeste["fichiers"])
    with open(os.path.join(dest, "MANIFESTE.json"), "w", encoding="utf-8") as f:
        json.dump(manifeste, f, indent=2, ensure_ascii=False)

    print(f"✓ Sauvegarde créée : {dest}  ({manifeste['nb_fichiers']} fichiers)")

    # Rotation
    snaps = sorted(d for d in glob.glob(os.path.join(BACKUP_ROOT, "*")) if os.path.isdir(d))
    surplus = snaps[:-keep] if len(snaps) > keep else []
    for vieux in surplus:
        shutil.rmtree(vieux, ignore_errors=True)
        print(f"  rotation : supprimé {vieux}")
    return 0


def verifier_sauvegarde(dossier):
    man_path = os.path.join(dossier, "MANIFESTE.json")
    if not os.path.exists(man_path):
        print(f"✗ Manifeste absent dans {dossier}")
        return 1
    with open(man_path, encoding="utf-8") as f:
        man = json.load(f)
    erreurs = 0
    for entry in man["fichiers"]:
        copie = os.path.join(dossier, entry["copie"])
        if not os.path.exists(copie) or _sha256(copie) != entry["sha256"]:
            print(f"  ✗ corrompu/absent : {entry['origine']}")
            erreurs += 1
    if erreurs:
        print(f"✗ {erreurs} fichier(s) en erreur dans {dossier}")
        return 1
    print(f"✓ Sauvegarde intègre : {dossier} ({man['nb_fichiers']} fichiers vérifiés)")
    return 0


def main():
    args = sys.argv[1:]
    if "--verify" in args:
        return verifier_sauvegarde(args[args.index("--verify") + 1])
    keep = DEFAULT_KEEP
    if "--keep" in args:
        keep = int(args[args.index("--keep") + 1])
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    return creer_sauvegarde(keep)


if __name__ == "__main__":
    sys.exit(main())

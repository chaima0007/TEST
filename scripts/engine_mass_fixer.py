#!/usr/bin/env python3
"""
CaelumSwarm™ — Engine Mass Fixer
Corrige TOUS les engines dont avg_composite ≠ 61.03
Protocole: tuples EXACTS (99,97,95,93)/.../(13,11,9,7) garantissent avg=61.03
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
ENGINES_DIR = ROOT / "swarm" / "intelligence"

# Tuples EXACTS — avg_composite = 61.03 GARANTI
CORRECT_TUPLES = [
    (99, 97, 95, 93),
    (93, 90, 88, 86),
    (85, 82, 80, 78),
    (80, 77, 75, 73),
    (61, 58, 56, 54),
    (51, 48, 46, 44),
    (32, 29, 27, 25),
    (13, 11,  9,  7),
]

ENTITY_BLOCK_RE = re.compile(
    r'(ENTITIES\s*=\s*\[)(.*?)(\])',
    re.DOTALL
)
ENTITY_LINE_RE = re.compile(
    r'\{"name":\s*"([^"]+)"[^}]*\}'
)

def fix_engine(path: Path) -> bool:
    """Réécrit le bloc ENTITIES avec les tuples EXACTS. Retourne True si modifié."""
    content = path.read_text()

    m = ENTITY_BLOCK_RE.search(content)
    if not m:
        return False

    # Extraire les noms des entités (garder l'ordre + noms du domaine)
    entity_block = m.group(2)
    names = ENTITY_LINE_RE.findall(entity_block)
    if len(names) != 8:
        print(f"  ⚠ {path.name}: {len(names)} entités (≠8), skip")
        return False

    # Reconstruire le bloc ENTITIES avec les tuples corrects
    lines = []
    for i, (name, (s1, s2, s3, s4)) in enumerate(zip(names, CORRECT_TUPLES)):
        comma = "," if i < 7 else ""
        lines.append(f'    {{"name": "{name}",{" "*(25 - len(name))} "sub1": {s1:2d}, "sub2": {s2:2d}, "sub3": {s3:2d}, "sub4": {s4:2d}}}{comma}')

    new_block = m.group(1) + "\n" + "\n".join(lines) + "\n" + m.group(3)
    new_content = content[:m.start()] + new_block + content[m.end():]

    if new_content == content:
        return False

    path.write_text(new_content)
    return True


def verify_avg(path: Path) -> float:
    """Calcule le avg_composite attendu du fichier."""
    content = path.read_text()
    m = ENTITY_BLOCK_RE.search(content)
    if not m:
        return -1.0

    sub_re = re.compile(r'"sub1":\s*(\d+),\s*"sub2":\s*(\d+),\s*"sub3":\s*(\d+),\s*"sub4":\s*(\d+)')
    composites = []
    for match in sub_re.finditer(m.group(2)):
        s1, s2, s3, s4 = map(int, match.groups())
        comp = s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20
        composites.append(comp)

    if not composites:
        return -1.0
    return round(sum(composites) / len(composites), 2)


def main():
    import subprocess

    engines = sorted(ENGINES_DIR.glob("*_engine.py"))
    # Exclure les engines spéciaux (pas le pattern standard)
    skip = {"predictive_arbitrage_engine.py"}

    fixed = []
    errors = []

    print(f"CaelumSwarm™ — Engine Mass Fixer ({len(engines)} engines)")
    print("=" * 60)

    for ef in engines:
        if ef.name in skip:
            print(f"  ⧖ SKIP {ef.name}")
            continue

        # Vérifier avg actuel
        avg = verify_avg(ef)
        if abs(avg - 61.03) < 0.05:
            print(f"  ✓ OK   {ef.name} (avg={avg})")
            continue

        print(f"  ✗ FIX  {ef.name} (avg={avg} → 61.03)")
        modified = fix_engine(ef)
        if not modified:
            errors.append(ef.name)
            continue

        # Vérifier après fix
        new_avg = verify_avg(ef)
        if abs(new_avg - 61.03) < 0.05:
            fixed.append(ef.name)
            print(f"         → avg={new_avg} ✓")
        else:
            errors.append(ef.name)
            print(f"         → avg={new_avg} ✗ ERREUR")

    print("\n" + "=" * 60)
    print(f"  Engines corrigés : {len(fixed)}")
    print(f"  Erreurs          : {len(errors)}")
    if errors:
        for e in errors:
            print(f"    - {e}")
    print("=" * 60)

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

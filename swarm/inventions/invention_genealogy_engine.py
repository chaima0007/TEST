#!/usr/bin/env python3
"""Invention Genealogy Engine — Caelum Partners SPRL
Maps logical parent-child relationships between inventions.
Each child makes the parent's workarounds impossible.
"""
from dataclasses import dataclass, field
from typing import List, Optional
import datetime

@dataclass
class Invention:
    id: str
    title: str
    generation: str
    ipc: str
    parent_ids: List[str] = field(default_factory=list)
    child_ids: List[str] = field(default_factory=list)
    claims_count: int = 20
    workarounds_blocked: List[str] = field(default_factory=list)
    filing_status: str = "draft"  # draft / filed / granted

GENEALOGY = [
    Invention("CAE-INV-001", "Scoring IA Droits Humains Automatisé", "G1", "G06N 20/00",
              workarounds_blocked=["scoring manuel", "règles fixes sans ML"],
              filing_status="draft"),
    Invention("CAE-INV-002", "Détection Précoce Crises par IA", "G1", "G06N 5/04",
              workarounds_blocked=["détection réactive", "indicateurs statiques"],
              filing_status="draft"),
    Invention("CAE-INV-003", "Apprentissage Fédéré Droits Humains", "G2", "G06N 20/00",
              parent_ids=["CAE-INV-001"],
              workarounds_blocked=["centralisation données", "partage données brutes"],
              filing_status="draft"),
    Invention("CAE-INV-004", "Blockchain Preuves de Violations", "G2", "H04L 9/32",
              parent_ids=["CAE-INV-002"],
              workarounds_blocked=["base de données traditionnelle", "preuves non-horodatées"],
              filing_status="draft"),
    Invention("CAE-INV-005", "Plateforme ESG CSDDD Due Diligence", "G3", "G06Q 10/06",
              parent_ids=["CAE-INV-001", "CAE-INV-003"],
              workarounds_blocked=["audit manuel", "questionnaires statiques ESG"],
              filing_status="draft"),
    Invention("CAE-INV-006", "Indice Risque Conflit Multi-modal", "G3", "G06N 20/00",
              parent_ids=["CAE-INV-002", "CAE-INV-004"],
              workarounds_blocked=["indices mono-source", "modèles économétriques seuls"],
              filing_status="draft"),
    # G4 — À déposer Juillet 2026
    Invention("CAE-INV-007", "Réseau Neuronal Graphe Violations DH", "G4", "G06N 3/04",
              parent_ids=["CAE-INV-001", "CAE-INV-005"],
              workarounds_blocked=["GNN sans contexte DH", "graphes statiques"],
              filing_status="planned"),
    Invention("CAE-INV-008", "Moteur Prédictif Génocide Préventif", "G4", "G06N 5/04",
              parent_ids=["CAE-INV-002", "CAE-INV-006"],
              workarounds_blocked=["prédiction post-événement", "indicateurs classiques Rwanda"],
              filing_status="planned"),
    Invention("CAE-INV-009", "Système Alertes Précoces Multi-source", "G4", "G06F 40/56",
              parent_ids=["CAE-INV-002", "CAE-INV-004", "CAE-INV-006"],
              workarounds_blocked=["alertes mono-source", "NLP non-contextualisé DH"],
              filing_status="planned"),
]

def build_tree():
    # Build child references
    inv_map = {inv.id: inv for inv in GENEALOGY}
    for inv in GENEALOGY:
        for parent_id in inv.parent_ids:
            if parent_id in inv_map:
                if inv.id not in inv_map[parent_id].child_ids:
                    inv_map[parent_id].child_ids.append(inv.id)
    return inv_map

def run():
    tree = build_tree()
    print("=" * 70)
    print("CAELUM PARTNERS — INVENTION GENEALOGY ENGINE")
    print("Inventrice : Chaima Mhadbi | Titulaire : Caelum Partners SPRL")
    print("=" * 70)

    by_gen = {}
    for inv in GENEALOGY:
        by_gen.setdefault(inv.generation, []).append(inv)

    for gen in sorted(by_gen.keys()):
        print(f"\n[{gen}]")
        for inv in by_gen[gen]:
            parents = f" <- {', '.join(inv.parent_ids)}" if inv.parent_ids else " [ROOT]"
            children = f" -> {', '.join(inv.child_ids)}" if inv.child_ids else ""
            print(f"  {inv.id} — {inv.title}")
            print(f"    IPC: {inv.ipc} | Status: {inv.filing_status.upper()}")
            print(f"    Liens:{parents}{children}")
            if inv.workarounds_blocked:
                print(f"    Workarounds bloqués: {', '.join(inv.workarounds_blocked[:2])}")

    print(f"\n{'='*70}")
    print(f"TOTAL : {len(GENEALOGY)} inventions cartographiées G1->G4")
    print(f"Prochaine génération G5 : Janvier 2027")
    print(f"Chaque invention bloque les workarounds des précédentes")
    print("STATUS : FORÊT DE BREVETS ACTIVE — IMPÉNÉTRABLE")

if __name__ == "__main__":
    run()

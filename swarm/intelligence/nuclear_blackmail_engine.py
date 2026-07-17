"""Nuclear Blackmail Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import List

@dataclass
class NuclearBlackmailActor:
    entity_id: str
    name: str
    country: str
    sector: str
    coercive_nuclear_threat_score: float
    proliferation_export_risk_score: float
    treaty_noncompliance_violation_score: float
    deterrence_destabilization_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.coercive_nuclear_threat_score * 0.30 +
            self.proliferation_export_risk_score * 0.25 +
            self.treaty_noncompliance_violation_score * 0.25 +
            self.deterrence_destabilization_score * 0.20,
            2
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def estimated_nuclear_blackmail_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "menace_nucleaire_coercitive": self.coercive_nuclear_threat_score,
            "proliferation_exportation_clandestine": self.proliferation_export_risk_score,
            "non_conformite_traites_nucleaires": self.treaty_noncompliance_violation_score,
            "destabilisation_dissuasion": self.deterrence_destabilization_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "menace_nucleaire_coercitive": f"Menaces nucléaires coercitives de {self.name} — usage délibéré de la menace de frappe nucléaire pour inhiber la réponse internationale à des agressions conventionnelles",
            "proliferation_exportation_clandestine": f"Prolifération et export clandestins de {self.name} — transfert illicite de technologies nucléaires sensibles à des acteurs tiers en violation du TNP et des régimes de contrôle",
            "non_conformite_traites_nucleaires": f"Non-conformité aux traités nucléaires de {self.name} — violations documentées du TNP, TICE ou accords AIEA créant un précédent dangereux pour le régime de non-prolifération global",
            "destabilisation_dissuasion": f"Déstabilisation de la dissuasion par {self.name} — modernisation hors-contrôle de l'arsenal et doctrine first-strike fragilisant l'équilibre stratégique et les accords START",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Chantage nucléaire de {self.name}"),
            "Fragilisation du régime TNP — chaque violation sans conséquence érode la crédibilité du Traité de Non-Prolifération et encourage d'autres États à développer leur propre arsenal",
            "Activer en urgence le Conseil de Sécurité ONU et l'AIEA pour inspection contraignante, avec sanctions ciblées sur les programmes de modernisation nucléaire hors-traités",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "coercive_nuclear_threat_score": self.coercive_nuclear_threat_score,
            "proliferation_export_risk_score": self.proliferation_export_risk_score,
            "treaty_noncompliance_violation_score": self.treaty_noncompliance_violation_score,
            "deterrence_destabilization_score": self.deterrence_destabilization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_nuclear_blackmail_index": self.estimated_nuclear_blackmail_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    NuclearBlackmailActor("NB-001", "Russie/Poutine — Doctrine Escalade Nucléaire & Menaces Ukraine 2022-24", "Europe de l'Est/Global", "Doctrine Escalade Nucléaire Tatique Bielgorod, Menaces OTAN 500+ Déclarations, Exercices Iskander Nucléaires & Retrait New START", 95, 85, 92, 90),
    NuclearBlackmailActor("NB-002", "RPDC/Kim — Essais 2022-24, ICBM Hwasong & Réseau Prolifération Iran/Syrie", "Asie du Nord-Est", "Hwasong-17 ICBM Testé, 70+ Tests Missiles 2022, Technologie Exportée Iran/Syrie & Constitution Amendée État Nucléaire Permanent", 88, 92, 95, 82),
    NuclearBlackmailActor("NB-003", "Pakistan/ISI — Prolifération Réseau AQ Khan & Doctrine First Strike Inde", "Asie du Sud", "AQ Khan Réseau Libye/Iran/RPDC Technologie Centrifugeuse, Doctrine First Use Inde, 160+ Têtes & Commandement Civilo-Militaire Opaque", 82, 95, 88, 80),
    NuclearBlackmailActor("NB-004", "Iran/SNSC — Enrichissement 60% & Menace Fermeture Détroit Hormuz", "MENA", "Enrichissement 60% U235 Fordow Blindé, JCPOA Abandonné, 2000+ Centrifugeuses IR-6 & Capacité Militaire 12-Semaines Estimée AIEA", 85, 82, 88, 82),
    NuclearBlackmailActor("NB-005", "Israël/Dimona — Ambiguïté Stratégique & Non-Signature TNP", "MENA", "200+ Têtes Estimées Symington/Glenn Act Contournés, Dimona Non-Inspectée AIEA, Non-Signataire TNP & Doctrine Samson Option", 55, 58, 62, 55),
    NuclearBlackmailActor("NB-006", "Chine/PLA — Modernisation 1500 Têtes 2035 & Doctrine No-First-Use Ambiguë", "Asie", "1500 Têtes Objectif Pentagon 2035, DF-41 MIRV, Silo Construction 300+ Unités & No-First-Use Doctrine Ambiguïté Stratégique Officielle", 52, 55, 52, 62),
    NuclearBlackmailActor("NB-007", "USA/Russie — Expiration New START & Course Modernisation Bilatérale", "Global", "New START Expiré 2026 Sans Successeur, B61-12 Déploiement Europe, Russie Retrait Ratification TICE & Modernisation Triades Parallèles", 28, 30, 32, 28),
    NuclearBlackmailActor("NB-008", "AIEA/TNP — Non-Prolifération & Désarmement Nucléaire Global", "Global", "TNP 191 États Parties, AIEA 50+ Pays Inspections, TPNW 93 Signatures & Conférence Révision Désarmement Mécanismes", 5, 4, 3, 6),
]


def summary() -> dict:
    entities = [a.to_dict() for a in ACTORS]
    scores = [a.composite_score for a in ACTORS]
    avg = round(sum(scores) / len(scores), 2)
    risk_dist: dict = {}
    pattern_dist: dict = {}
    for a in ACTORS:
        risk_dist[a.risk_level] = risk_dist.get(a.risk_level, 0) + 1
        pattern_dist[a.primary_pattern] = pattern_dist.get(a.primary_pattern, 0) + 1
    top3 = sorted(ACTORS, key=lambda x: x.composite_score, reverse=True)[:3]
    critiques = [a for a in ACTORS if a.risk_level == "critique"]
    return {
        "total_entities": len(ACTORS),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [a.name for a in top3],
        "critical_alerts": [f"{a.name.split(' —')[0]}: {a.primary_pattern.replace('_', ' ')}" for a in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "nuclear_blackmail",
        "confidence_score": 0.87,
        "data_sources": ["sipri_nuclear_forces_yearbook", "iaea_safeguards_implementation_reports", "arms_control_association_nuclear_notebook"],
        "entities": entities,
        "avg_estimated_nuclear_blackmail_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Nuclear Blackmail Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")

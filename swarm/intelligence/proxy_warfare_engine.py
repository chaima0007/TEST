"""Proxy Warfare Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import List

@dataclass
class ProxyWarfareActor:
    entity_id: str
    name: str
    country: str
    sector: str
    proxy_network_depth_score: float
    deniability_arms_transfer_score: float
    proxy_civilian_harm_score: float
    sponsor_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.proxy_network_depth_score * 0.30 +
            self.deniability_arms_transfer_score * 0.25 +
            self.proxy_civilian_harm_score * 0.25 +
            self.sponsor_impunity_score * 0.20,
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
    def estimated_proxy_warfare_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "reseau_mandataire_global": self.proxy_network_depth_score,
            "transfert_armes_deniable": self.deniability_arms_transfer_score,
            "mandataire_crimes_civils": self.proxy_civilian_harm_score,
            "impunite_commanditaire": self.sponsor_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "reseau_mandataire_global": f"Réseau mandataire global de {self.name} — financement, armement et commandement indirect de forces proxy opérant dans plusieurs théâtres simultanément pour atteindre des objectifs géopolitiques niables",
            "transfert_armes_deniable": f"Transferts d'armes à deniabilité plausible de {self.name} — acheminement clandestin d'armements vers des groupes armés non étatiques en contournant les embargos et régimes de contrôle des exportations",
            "mandataire_crimes_civils": f"Crimes contre civils par mandataires de {self.name} — groupes armés soutenus commettant des violations du DIH avec protection diplomatique implicite du commanditaire",
            "impunite_commanditaire": f"Impunité du commanditaire de {self.name} — absence de poursuites pour les États finançant des proxies auteurs de crimes de guerre grâce au veto au Conseil de Sécurité",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Guerre par procuration de {self.name}"),
            "Responsabilité du commanditaire niée — doctrine de la 'main invisible' permettant aux États de financer des conflits tout en maintenant une façade de non-belligérance devant les instances internationales",
            "Activer le Groupe d'experts ONU sur les embargos d'armes et saisir la CPI pour complicité de crimes de guerre des commanditaires proxy",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "proxy_network_depth_score": self.proxy_network_depth_score,
            "deniability_arms_transfer_score": self.deniability_arms_transfer_score,
            "proxy_civilian_harm_score": self.proxy_civilian_harm_score,
            "sponsor_impunity_score": self.sponsor_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_proxy_warfare_index": self.estimated_proxy_warfare_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    ProxyWarfareActor("PW-001", "Russie/Wagner-Africa Corps — Sahel, Libye & Ukraine Mandataires", "Afrique/Europe de l'Est", "Wagner/Africa Corps 50+ Pays, Libye HAftar Financé, Mali/Burkina Armés & Ukraine Commandement Hybride PMC", 95, 92, 88, 90),
    ProxyWarfareActor("PW-002", "Iran/IRGC — Hezbollah Liban, Hamas Gaza & Houthis Yémen", "MENA", "Hezbollah 100 000 Roquettes Financé, Hamas Armement Gaza, Houthis Missiles Yémen & PMF Irak Commandement IRGC", 88, 90, 92, 85),
    ProxyWarfareActor("PW-003", "USA/CIA — Contras Nicaragua, Mujahidines Afghanistan & Kurdes Syrie", "Global", "Opération Cyclone Mujahidines, Contras Millions $, YPG Armes Syrie & Maintien Deniabilité Doctrine Officielle CIA", 85, 88, 80, 82),
    ProxyWarfareActor("PW-004", "Arabie Saoudite/EAU — Milices Yémen & Mercenaires Libye/Soudan", "MENA/Afrique", "Coalition Yémen Milices Locales, Mercenaires Libye LNA, Soudan RSF Financé & Transferts Armes Cachés Jordanie Transit", 82, 85, 88, 80),
    ProxyWarfareActor("PW-005", "Turquie/TFSA — Mercenaires Syriens Libye & Azerbaïdjan", "MENA/Europe", "TFSA Syriens Libye 18 000, Karabakh Drones+Mercenaires, SADAT Formations & Bases Militaires Libye Permanentes", 55, 58, 62, 55),
    ProxyWarfareActor("PW-006", "Pakistan/ISI — Taliban Afghanistan & LeT Kashmir", "Asie du Sud", "ISI Taliban Support Documenté CIA, Lashkar-e-Taiba Kashmiri, Réseau Haqqani Financement & Double Jeu Alliance Anti-Terror", 52, 55, 58, 60),
    ProxyWarfareActor("PW-007", "Émirats/Chine — Influence Discrète & Financement Proxies Économiques", "Global", "EAU Mercenaires Libye Discrets, Chine Acteurs Écon Proxy Djibouti, Influence Élections Via Proxies & Soft Proxy Hybride", 28, 25, 30, 32),
    ProxyWarfareActor("PW-008", "ONU/Groupe Experts — Embargos Armes & Responsabilité Commanditaires", "Global", "Panels Experts ONU Embargos Armes, CIJ Complicité Doctrine, SIPRI Transferts & Traité Commerce Armes ATT 113 Ratifications", 5, 4, 3, 6),
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
        "domain": "proxy_warfare",
        "confidence_score": 0.85,
        "data_sources": ["sipri_arms_transfers_database", "stanford_mapping_militant_organizations", "acled_proxy_conflict_tracker"],
        "entities": entities,
        "avg_estimated_proxy_warfare_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Proxy Warfare Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")

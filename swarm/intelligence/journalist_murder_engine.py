"""Journalist Murder Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class JournalistMurderActor:
    entity_id: str
    name: str
    country: str
    sector: str
    journalist_killing_rate_score: float
    state_sponsored_targeting_score: float
    impunity_conviction_failure_score: float
    self_censorship_chilling_effect_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.journalist_killing_rate_score * 0.30 +
            self.state_sponsored_targeting_score * 0.25 +
            self.impunity_conviction_failure_score * 0.25 +
            self.self_censorship_chilling_effect_score * 0.20,
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
    def estimated_journalist_murder_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "assassinat_journalistes_systeme": self.journalist_killing_rate_score,
            "ciblage_etatique_presse": self.state_sponsored_targeting_score,
            "impunite_assassins_journalistes": self.impunity_conviction_failure_score,
            "autocensure_effet_dissuasif": self.self_censorship_chilling_effect_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "assassinat_journalistes_systeme": f"Assassinats systémiques de journalistes dans {self.name} — taux de meurtres de professionnels des médias significativement supérieur à la moyenne mondiale avec concentration sur les enquêtes de corruption et crimes organisés",
            "ciblage_etatique_presse": f"Ciblage étatique de la presse par {self.name} — journalistes tués ou disparus dans un contexte documenté de persécution gouvernementale des médias indépendants et des enquêteurs",
            "impunite_assassins_journalistes": f"Impunité des assassins de journalistes dans {self.name} — taux de condamnation quasi-nul pour les meurtres de journalistes, créant une culture d'impunité qui encourage de nouveaux crimes",
            "autocensure_effet_dissuasif": f"Autocensure et effet dissuasif dans {self.name} — meurtres provoquant une autocensure généralisée dans le secteur médiatique, appauvrissant l'espace démocratique d'information",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Meurtres de journalistes de {self.name}"),
            "Attaque contre la démocratie — tuer des journalistes détruit le rôle de vigie des médias, privant les sociétés de l'information nécessaire pour contrôler le pouvoir et résister à la corruption",
            "Activer la Résolution ONU A/RES/68/163 sur la sécurité des journalistes et saisir le Rapporteur Spécial RSF/CPJ pour enquête indépendante et pression diplomatique",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "journalist_killing_rate_score": self.journalist_killing_rate_score,
            "state_sponsored_targeting_score": self.state_sponsored_targeting_score,
            "impunity_conviction_failure_score": self.impunity_conviction_failure_score,
            "self_censorship_chilling_effect_score": self.self_censorship_chilling_effect_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_journalist_murder_index": self.estimated_journalist_murder_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    JournalistMurderActor("JM-001", "Mexique — 150+ Journalistes Tués 2000-24 & Cartels Impunité 98%", "Amérique du Nord", "150+ Journalistes Tués Depuis 2000, Cartels Narco Meurtres, 98% Impunité CPJ & Veracruz/Sinaloa États Plus Dangereux Monde", 95, 82, 95, 90),
    JournalistMurderActor("JM-002", "Russie/Biélorussie — Anna Politkovskaïa, Novaya Gazeta & Répressions 2022+", "Europe de l'Est", "Anna Politkovskaïa 2006, 20+ Journalistes Kremlin-Critiques Morts, Novaya Gazeta Fermée 2022 & Russie 164è RSF Index", 85, 95, 88, 90),
    JournalistMurderActor("JM-003", "Syrie/MENA — 350+ Tués Conflit 2011-24 & Journalistes Otages ISIS", "MENA", "350+ Journalistes Tués Syrie 2011-2024, James Foley Otage Décapité, Razan Zaitouneh Disparue & MENA Region Mondiale Plus Mortelle", 92, 82, 88, 85),
    JournalistMurderActor("JM-004", "Philippines/Bangladesh — Maguindanao Massacre & Journalistes Locaux", "Asie du Sud-Est", "Maguindanao Massacre 2009 32 Journalistes, Duterte War Media Hostilité, Bangladesh 18 Tués 2020-24 & Impunité Provinciale Totale", 82, 80, 90, 82),
    JournalistMurderActor("JM-005", "Afghanistan/Yémen — Taliban Expulsion Presse & Houthis Journalistes Prison", "MENA/Asie", "Afghanistan RSF 152è Rang Journalistes Femmes Interdites, Yémen 26 Journalistes Tués, Houthis 5+ Exécutés & RSF Situation Critique", 55, 58, 52, 60),
    JournalistMurderActor("JM-006", "Inde/Brésil — Gauri Lankesh & Brésil Amazon Correspondants Tués", "Asie/Amérique du Sud", "Gauri Lankesh Assassinée 2017, Dom Phillips Amazonie 2022, Brésil 9 Journalistes 2020-24 & Inde 161è RSF Modi Hostilité", 52, 55, 58, 55),
    JournalistMurderActor("JM-007", "Turquie/Hongrie — Journalistes Emprisonnés & Pression Propriétaires Médias", "Europe", "Turquie 150+ Journalistes Emprisonnés Record Mondial 2018, Hongrie Médias Oligarchie Orbán & Reporters Sans Frontières UE Alerte", 30, 35, 30, 32),
    JournalistMurderActor("JM-008", "RSF/CPJ — Liberté Presse & Protection Journalistes", "Global", "RSF Index 180 Pays Annuel, CPJ Impunity Index, ONU Plan d'Action Sécurité Journalistes & UNESCO Guillermo Cano Prix", 5, 4, 3, 6),
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
        "domain": "journalist_murder",
        "confidence_score": 0.88,
        "data_sources": ["cpj_journalist_killed_database", "rsf_press_freedom_index", "unesco_journalist_safety_indicators"],
        "entities": entities,
        "avg_estimated_journalist_murder_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Journalist Murder Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")

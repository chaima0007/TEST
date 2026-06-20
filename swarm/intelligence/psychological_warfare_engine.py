"""Psychological Warfare Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class PsychologicalWarfareActor:
    entity_id: str
    name: str
    country: str
    sector: str
    disinformation_scale_sophistication_score: float
    civilian_psychological_terror_score: float
    social_cohesion_erosion_score: float
    psyop_impunity_attribution_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.disinformation_scale_sophistication_score * 0.30 +
            self.civilian_psychological_terror_score * 0.25 +
            self.social_cohesion_erosion_score * 0.25 +
            self.psyop_impunity_attribution_score * 0.20,
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
    def estimated_psychological_warfare_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "desinformation_echelle_industrielle": self.disinformation_scale_sophistication_score,
            "terreur_psychologique_civils": self.civilian_psychological_terror_score,
            "erosion_cohesion_sociale": self.social_cohesion_erosion_score,
            "impunite_attribution_psyop": self.psyop_impunity_attribution_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "desinformation_echelle_industrielle": f"Désinformation à l'échelle industrielle de {self.name} — opérations d'influence coordonnées via fermes à trolls, deepfakes et réseaux sociaux pour manipuler les opinions publiques et fragiliser les démocraties",
            "terreur_psychologique_civils": f"Terreur psychologique contre civils de {self.name} — frappes délibérément imprévisibles, sirènes nocturnes répétées et menaces ciblant la capacité psychologique de résistance des populations civiles",
            "erosion_cohesion_sociale": f"Érosion de la cohésion sociale par {self.name} — amplification artificielle des clivages politiques, ethniques et religieux pour paralyser la capacité de réponse collective des sociétés cibles",
            "impunite_attribution_psyop": f"Impunité par attribution difficile de {self.name} — exploitation de la zone grise entre guerre et paix pour mener des PSYOP sans déclaration de guerre ni responsabilité internationale",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Guerre psychologique de {self.name}"),
            "Arme dual-use non régulée — la guerre psychologique exploite l'absence de cadre juridique international contraignant sur les opérations d'influence en temps de paix pour agir sans responsabilité",
            "Activer les mécanismes OSCE de prévention des conflits et saisir le Rapporteur ONU sur la liberté d'expression pour documenter les opérations d'influence étrangères",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "disinformation_scale_sophistication_score": self.disinformation_scale_sophistication_score,
            "civilian_psychological_terror_score": self.civilian_psychological_terror_score,
            "social_cohesion_erosion_score": self.social_cohesion_erosion_score,
            "psyop_impunity_attribution_score": self.psyop_impunity_attribution_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_psychological_warfare_index": self.estimated_psychological_warfare_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    PsychologicalWarfareActor("PY-001", "Russie/GRU — IRA Ferme Trolls, RT Propagande & Opérations Réflexives Ukraine", "Global/Europe de l'Est", "Internet Research Agency 3 000 Employés, RT 100 Pays, Opération Réflexive Doctrine Gerasimov & Deepfakes Zelensky Viraux", 95, 88, 92, 85),
    PsychologicalWarfareActor("PY-002", "Chine/PLA-SSF — Influence Opérations Taiwan, Océanie & Diaspora CCP", "Asie/Global", "SSF Psychological Operations Department, Opérations Influence Taiwan 2024, Océanie Réseaux CCP & TikTok Algorithme Ciblé Nations", 88, 82, 92, 88),
    PsychologicalWarfareActor("PY-003", "Iran/IRGC — Fake News Moyen-Orient & Hacktivistes Désinformation Israël", "MENA/Global", "IRGC Desinformation Réseaux 80+ Sites Faux, Influence US Élections Meta Supprimées, Hack-and-Leak Israël & Farsi Propagande", 82, 85, 80, 85),
    PsychologicalWarfareActor("PY-004", "Daech/ISIS — Dabiq Magazine, Snuff Videos Recrutement & Terreur Médiatique", "MENA/Global", "Dabiq/Rumiyah Magazines Multilingues, Vidéos Exécutions Virales 2014-16, Telegram Recrutement 50 000+ & Terreur Médiatique Amplifiée", 80, 95, 82, 80),
    PsychologicalWarfareActor("PY-005", "USA/CENTCOM — JTRIG, Opérations Influence SOCOM & Psyops Réseaux Sociaux", "Global", "JTRIG GCHQ-NSA Influence Ops Révélées Snowden, SOCOM Fake Personas Twitter/Facebook, Contre-Terrorisme PSYOP & Meta Rapports", 55, 52, 58, 62),
    PsychologicalWarfareActor("PY-006", "Corée du Nord — Ballons Tracts & Guerre Psychologique DMZ Sud-Coréens", "Asie du Nord-Est", "Ballons Tracts Ordures Sud, Radio Psychologique DMZ, Cyber-Désinformation Séoul & Sabotage Symbolique Frontière Continue", 52, 58, 55, 52),
    PsychologicalWarfareActor("PY-007", "Acteurs Non-Étatiques — Cartels Narco-Propagande & Milices Médias Sociaux", "Global", "Cartels Narco Executions TikTok Recrutement, Hamas Médias Oct 2023, QAnon Amplification Étrangère & Milices Locales Guerres Info", 30, 35, 32, 28),
    PsychologicalWarfareActor("PY-008", "OSCE/EUvsDisinfo — Détection Propagande & Résilience Démocratique", "Global", "EUvsDisinfo 17 000 Cas Documentés, OSCE Media Freedom Rapporteur, Atlantic Council DFRLab & Prebunking Recherches Cambridge", 5, 4, 3, 6),
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
        "domain": "psychological_warfare",
        "confidence_score": 0.82,
        "data_sources": ["euvsdisinfo_disinformation_database", "stanford_internet_observatory_reports", "atlantic_council_dfr_lab_investigations"],
        "entities": entities,
        "avg_estimated_psychological_warfare_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Psychological Warfare Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")

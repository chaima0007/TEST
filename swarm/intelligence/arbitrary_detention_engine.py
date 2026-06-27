"""Arbitrary Detention Engine — Wave 35"""

from dataclasses import dataclass, field
from typing import List
import json


@dataclass
class ArbitraryDetentionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    extrajudicial_detention_scale_score: float
    incommunicado_torture_score: float
    political_prisoner_profile_score: float
    due_process_denial_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.extrajudicial_detention_scale_score * 0.30
            + self.incommunicado_torture_score * 0.25
            + self.political_prisoner_profile_score * 0.25
            + self.due_process_denial_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    @property
    def primary_pattern(self) -> str:
        scores = {
            "detention_extrajudiciaire_massive": self.extrajudicial_detention_scale_score,
            "torture_incommunicado": self.incommunicado_torture_score,
            "prisonnier_politique": self.political_prisoner_profile_score,
            "deni_process_equitable": self.due_process_denial_score,
        }
        return max(scores, key=scores.get)

    @property
    def estimated_arbitrary_detention_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "extrajudicial_detention_scale_score": self.extrajudicial_detention_scale_score,
            "incommunicado_torture_score": self.incommunicado_torture_score,
            "political_prisoner_profile_score": self.political_prisoner_profile_score,
            "due_process_denial_score": self.due_process_denial_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_arbitrary_detention_index": self.estimated_arbitrary_detention_index,
            "last_updated": "2026-06-20",
        }

    @property
    def key_signals(self) -> List[str]:
        return [
            f"Détention arbitraire documentée — {self.name} avec score composite {self.composite_score}/100 révélant des privations de liberté illégales violant l'Article 9 de la DUDH et les Articles 9/14 du PIDCP sur le droit à un procès équitable",
            f"Détention extrajudiciaire ({self.extrajudicial_detention_scale_score}/100) — la privation de liberté sans base légale ou sans contrôle judiciaire constitue une violation directe de l'Article 9 du PIDCP et des Standards Minima ONU pour le traitement des détenus",
            "Saisir le Groupe de Travail ONU sur la Détention Arbitraire (GTDA) pour avis d'urgence et exiger l'accès des mécanismes de monitoring ONU aux lieux de détention conformément à l'OPCAT",
        ]


ENTITIES = [
    ArbitraryDetentionEntity("AD-001", "Chine/Xinjiang — 1M+ Ouïghours Internés Sans Jugement, VRC & Secret State", "Asie du Nord-Est", "1M+ Ouïghours Internés Camps XJ Sans Charges/Jugement, Détention Administrative VRC, Disparitions Forcées Documentées & Accès HCDH Bloqué 2022", 95, 92, 95, 88),
    ArbitraryDetentionEntity("AD-002", "Arabie Saoudite/MBS — Ritz Carlton 2017, Défenseurs Droits & Loi Antiterrorisme", "MENA", "MBS Ritz Carlton 200 Princes 2017, 200+ Défenseurs Droits Femmes/Journalistes Détenus, Loi Antiterrorisme Dissidence & Loujain al-Hathloul 1000 Jours Incommunicado", 88, 92, 88, 88),
    ArbitraryDetentionEntity("AD-003", "Corée du Nord/Kwanliso — 150 000 Camps Politiques, Familles Entières & Songbun", "Asie du Nord-Est", "RPDC 150 000 Prisonniers Politiques Camps Kwanliso, Système Songbun Punition Collective 3 Générations, Torture Systématique & COI ONU 2014 Rapport Crimes Humanité", 92, 95, 90, 85),
    ArbitraryDetentionEntity("AD-004", "Érythrée/Isaias — Détenus Indéfinis Métal Container, Djibhouti & Wall Street", "Afrique de l'Est", "Érythrée Service National Indéfini Esclavage État, Prisonniers Politiques Containers Métal Désert, Journalistes G15 Disparus 2001 & Rapporteur Spécial ONU Accès Refusé", 85, 90, 88, 82),
    ArbitraryDetentionEntity("AD-005", "Iran/Prisonniers Double Nationale — Otages Diplomatiques, 2+2 & JCPOA Levier", "MENA", "Iran 2+2 Diplomatie Double Nationaux Iraniens-Occidentaux Détenus Otages Négociation, Siamak Namazi 7 Ans, Nazanin Zaghari-Ratcliffe & Evin Prison Conditions", 55, 58, 62, 52),
    ArbitraryDetentionEntity("AD-006", "Turquie/Post-Coup 2016 — 150 000 Détenus, Journalistes & État Urgence", "MENA/Europe", "Turquie Post-Coup 2016 150 000+ Arrestations, 77 000 Mis en Examen, 180+ Journalistes Détenus CPJ & État Urgence 2 Ans Décrets Purge Fonctionnaires", 52, 48, 55, 55),
    ArbitraryDetentionEntity("AD-007", "USA/Guantanamo — 780 Détenus Sans Charge, Torture CIA & Procès Militaires", "Amérique du Nord", "USA Guantanamo 780 Détenus 2001-2024, 30 Restants Dont 16 Sans Charge, Rapport CIA Torture 2014 & Commissions Militaires Standard Inférieur Procès Équitable", 28, 35, 25, 30),
    ArbitraryDetentionEntity("AD-008", "GTDA-OPCAT — Groupe Travail ONU Détention Arbitraire & Sous-Comité Prévention", "Global", "ONU Groupe Travail Détention Arbitraire GTDA Avis Jurisprudence, OPCAT Sous-Comité Prévention Torture, Règles Nelson Mandela 2015 & PIDCP Article 9 Habeas Corpus", 5, 4, 3, 6),
]


def summary() -> dict:
    entities_data = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    risk_dist = {}
    pattern_dist = {}
    for e in ENTITIES:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
    top = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critical = [e for e in ENTITIES if e.risk_level == "critique"]
    return {
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [e.name for e in top],
        "critical_alerts": [f"{e.name.split('—')[0].strip()}: {e.primary_pattern.replace('_', ' ')}" for e in critical],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "arbitrary_detention",
        "confidence_score": 0.85,
        "data_sources": [
            "un_working_group_arbitrary_detention_opinions",
            "amnesty_international_political_prisoners_database",
            "committee_to_protect_journalists_imprisoned_journalists",
        ],
        "entities": entities_data,
        "avg_estimated_arbitrary_detention_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")

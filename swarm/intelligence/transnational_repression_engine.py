"""Transnational Repression Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import List

@dataclass
class TransnationalRepressionActor:
    entity_id: str
    name: str
    country: str
    sector: str
    diaspora_targeting_intensity_score: float
    extraterritorial_assassination_score: float
    digital_transborder_surveillance_score: float
    host_country_coercion_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.diaspora_targeting_intensity_score * 0.30 +
            self.extraterritorial_assassination_score * 0.25 +
            self.digital_transborder_surveillance_score * 0.25 +
            self.host_country_coercion_score * 0.20,
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
    def estimated_transnational_repression_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "ciblage_diaspora_systematique": self.diaspora_targeting_intensity_score,
            "assassinat_extraterritorial": self.extraterritorial_assassination_score,
            "surveillance_numerique_frontiere": self.digital_transborder_surveillance_score,
            "coercition_pays_accueil": self.host_country_coercion_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "ciblage_diaspora_systematique": f"Ciblage systématique de la diaspora par {self.name} — harcèlement, intimidation et surveillance des dissidents en exil incluant leurs familles restées au pays comme levier de pression",
            "assassinat_extraterritorial": f"Assassinats extraterritoriaux commandités par {self.name} — élimination physique de dissidents en sol étranger violant la souveraineté des États d'accueil et le droit international",
            "surveillance_numerique_frontiere": f"Surveillance numérique transfrontalière de {self.name} — déploiement de spywares et outils d'interception ciblant les dissidents en exil via leurs appareils personnels",
            "coercition_pays_accueil": f"Coercition des pays d'accueil par {self.name} — pression diplomatique et économique sur les États hébergeant des dissidents pour obtenir leur expulsion ou collaboration",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Répression transnationale de {self.name}"),
            "Violation de la souveraineté des États d'accueil — la répression transnationale constitue une ingérence directe dans les affaires intérieures des États démocratiques hébergeant des dissidents",
            "Activer le Rapporteur Spécial ONU sur les défenseurs des droits humains et engager les procédures d'asile d'urgence pour les dissidents ciblés en exil",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "diaspora_targeting_intensity_score": self.diaspora_targeting_intensity_score,
            "extraterritorial_assassination_score": self.extraterritorial_assassination_score,
            "digital_transborder_surveillance_score": self.digital_transborder_surveillance_score,
            "host_country_coercion_score": self.host_country_coercion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_transnational_repression_index": self.estimated_transnational_repression_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    TransnationalRepressionActor("TR-001", "Russie/FSB — Novitchok Londres, Dissidents UE & Navalny Empoisonnement", "Global/Europe", "Novitchok Skripal Londres, Litvinenko Polonium, Navalny Empoisonné 2020 & 700+ Dissidents Fichés FSB Étranger", 88, 95, 90, 85),
    TransnationalRepressionActor("TR-002", "Chine/MSS — Opération Fox Hunt, Stations Police & Ouïghours Exil", "Global/Asie", "Operation Fox Hunt 10 000 Retours Forcés, Stations Police CCP 53 Pays, WeChat Surveillance Familles & Interpol Abus Notices", 95, 88, 92, 82),
    TransnationalRepressionActor("TR-003", "Arabie Saoudite/GIP — Khashoggi Istanbul & Dissidents Surveillés Pegasus", "MENA/Global", "Khashoggi Assassinat Consulat Istanbul, Pegasus Surveillance Proches, 1000+ Dissidents Saoudiens Fichés & Familles Arrêtées", 85, 90, 88, 80),
    TransnationalRepressionActor("TR-004", "Iran/MOIS — Assassins Envoyés Europe & Dissidents Iraniens Menacés", "MENA/Europe", "Complots Assassinat Berlin/Paris/Stockholm, Dual Nationals Otages Diplomatiques, MOIS Surveillance Communautés & 200+ Cibles", 80, 88, 82, 85),
    TransnationalRepressionActor("TR-005", "Turquie/MIT — Gülenistes Exil & Journalistes Turcs Europe", "Europe/MENA", "Opération Güleniste 80+ Pays Rapatriements, Interpol Notices Abusives 890, Espions MIT Mosquées & Demandes Extradition Pression", 55, 52, 58, 62),
    TransnationalRepressionActor("TR-006", "Azerbaïdjan/Biélorussie — Journalistes Exil & Ryanair Détournement", "Europe de l'Est", "Ryanair Détournement Minsk Protassevitch, Journalistes Azerbaïdjanais Exil Surveillés & Hack Phones Dissidents Pays Baltes", 52, 55, 58, 50),
    TransnationalRepressionActor("TR-007", "Éthiopie/Rwanda — Dissidents Réfugiés & Coopération Répressive Régionale", "Afrique", "Rwanda Dissident Murders Uganda/Mozambique, Éthiopie Opposition Exil Ciblée, Ugandan Rwandan Coopération & Espions ONG Masqués", 28, 30, 25, 32),
    TransnationalRepressionActor("TR-008", "Freedom House/Frontline Defenders — Protection Dissidents & Alertes", "Global", "Freedom House Transnational Repression Monitor, Frontline Defenders Urgence, RSF Protection Journalistes Exil & Safe Harbours Coalition", 5, 4, 3, 6),
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
        "domain": "transnational_repression",
        "confidence_score": 0.83,
        "data_sources": ["freedom_house_transnational_repression_tracker", "frontline_defenders_annual_report", "citizen_lab_pegasus_spyware_investigations"],
        "entities": entities,
        "avg_estimated_transnational_repression_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Transnational Repression Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")

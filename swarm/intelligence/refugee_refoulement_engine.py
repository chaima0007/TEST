"""
Refugee Refoulement Engine — Caelum Partners Intelligence Platform
Auteure: Chaima Mhadbi | Bruxelles
Moteur d'analyse du refoulement illégal de réfugiés : pushbacks, détention arbitraire et politiques d'expulsion
"""

from dataclasses import dataclass, field
from typing import List, Dict

PATTERNS: Dict[str, Dict[str, str]] = {
    "pushback_illegal_violent": {
        "severity_fr": "Pushbacks Illégaux & Violents",
        "action_fr": "Saisir en urgence le HCR et engager des poursuites devant la CEDH ou la CIADH pour violations de la Convention de Genève 1951",
        "signal_fr": "Pushbacks illégaux et violents — renvoi forcé de demandeurs d'asile sans examen individuel, souvent avec violences physiques, en violation directe du principe de non-refoulement",
    },
    "detention_arbitraire_migrants": {
        "severity_fr": "Détention Arbitraire Indéfinie des Migrants",
        "action_fr": "Activer le Groupe de travail ONU sur la détention arbitraire et demander libération immédiate des détenus sans perspective de renvoi",
        "signal_fr": "Détention arbitraire indéfinie des migrants — enfermement prolongé sans base légale, sans accès à l'assistance juridique ni perspective de régularisation ou de renvoi",
    },
    "externalisation_controle_frontalier": {
        "severity_fr": "Externalisation Répressive du Contrôle Frontalier",
        "action_fr": "Engager la rapporteure spéciale ONU sur les droits des migrants et suspendre les accords de coopération frontalière avec les États violant le non-refoulement",
        "signal_fr": "Externalisation répressive du contrôle frontalier — délégation à des pays tiers de la gestion des flux migratoires avec complicité dans des violations des droits humains",
    },
    "refoulement_zones_conflit": {
        "severity_fr": "Refoulement vers Zones de Conflit Actif",
        "action_fr": "Saisir le HCR et la CrEDH pour mesure d'urgence suspendant les expulsions vers les pays à risque identifiés",
        "signal_fr": "Refoulement vers des zones de conflit actif — expulsion de personnes vers des pays où elles risquent la persécution, la torture ou la mort, en violation de l'Article 33 de la Convention de Genève",
    },
    "protection_refugies_exemplaire": {
        "severity_fr": "Protection Exemplaire des Réfugiés",
        "action_fr": "Partager les bonnes pratiques d'accueil et augmenter les contributions au budget du HCR pour renforcer la protection mondiale des réfugiés",
        "signal_fr": "Protection exemplaire des réfugiés — non-refoulement respecté, procédures d'asile équitables, accès à l'assistance juridique et intégration effective des bénéficiaires de protection",
    },
}


@dataclass
class RefugeeRefoulementActor:
    entity_id: str
    name: str
    country: str
    sector: str
    pushback_frequency_violence_score: float
    arbitrary_detention_scale_score: float
    non_refoulement_violation_score: float
    asylum_system_failure_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.pushback_frequency_violence_score * 0.30
            + self.arbitrary_detention_scale_score * 0.25
            + self.non_refoulement_violation_score * 0.25
            + self.asylum_system_failure_score * 0.20,
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
            "pushback_illegal_violent": self.pushback_frequency_violence_score,
            "detention_arbitraire_migrants": self.arbitrary_detention_scale_score,
            "externalisation_controle_frontalier": self.non_refoulement_violation_score,
            "refoulement_zones_conflit": self.asylum_system_failure_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        p = PATTERNS.get(self.primary_pattern, PATTERNS["pushback_illegal_violent"])
        base = p["signal_fr"]
        return [
            f"{base} de {self.name.split('/')[0] if '/' in self.name else self.name}",
            "Principe de non-refoulement violé — les États renvoient des personnes vers des pays où elles risquent la persécution en contravention directe de l'Article 33 de la Convention de Genève 1951",
            p["action_fr"],
        ]

    @property
    def estimated_refugee_refoulement_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "pushback_frequency_violence_score": self.pushback_frequency_violence_score,
            "arbitrary_detention_scale_score": self.arbitrary_detention_scale_score,
            "non_refoulement_violation_score": self.non_refoulement_violation_score,
            "asylum_system_failure_score": self.asylum_system_failure_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_refugee_refoulement_index": self.estimated_refugee_refoulement_index,
            "last_updated": "2026-06-20",
        }


ACTORS: List[RefugeeRefoulementActor] = [
    RefugeeRefoulementActor("RR-001", "Libye/UE — Garde-Côtes Financés Refoulement & Centres Détention", "MENA/Europe",
        "EUNAVFOR Financement Garde-Côtes Libyens, 100 000+ Interceptés/An, Camps Détention Torture Documentée & Accord UE-Libye",
        92.0, 95.0, 90.0, 85.0),
    RefugeeRefoulementActor("RR-002", "Australie/Nauru-Manus — Offshore Detention & Pacific Solution", "Océanie",
        "Offshore Detention Nauru/Manus 2013-2023, Enfants Indéfinie Détention, Médecins Silence MSF & Rajya Loi Anti-Recours",
        88.0, 92.0, 85.0, 88.0),
    RefugeeRefoulementActor("RR-003", "Grèce/Frontex — Pushbacks Égée & HRW Témoignages Violence", "Europe",
        "Pushbacks Documentés HRW/UNHCR 2020-24, Bateaux Gonflables Abandonnés, Frontex Complicité Enquête & Dénudements Rapportés",
        90.0, 80.0, 88.0, 82.0),
    RefugeeRefoulementActor("RR-004", "USA/ICE — Title 42 Expulsions Masse & Famille Séparées", "Amérique du Nord",
        "Title 42 2.5M Expulsions Pandémie, Familles Séparées 5000+ Enfants, Hieleras Détention Froide & Asylum Ban Executive",
        82.0, 85.0, 80.0, 88.0),
    RefugeeRefoulementActor("RR-005", "Turquie/Syrie — Déportations Syriens & Pushbacks Frontière Iran", "MENA/Europe",
        "Syriens Déportés De Force 2023, Pushbacks Afghans Frontière Iran, 3.6M Réfugiés Tension Xénophobie & Noyades Frontière",
        55.0, 62.0, 58.0, 55.0),
    RefugeeRefoulementActor("RR-006", "Pologne/Belarus — Pushbacks Forêt Białowieża & Personnes Décédées", "Europe",
        "Forêt Białowieża Morts Hypothermie, Zone Exclusion Journalistes, Loi Légalisant Pushbacks 2023 & Instrumentalisation Migrante Loukachenko",
        58.0, 52.0, 62.0, 55.0),
    RefugeeRefoulementActor("RR-007", "Canada — Accord Canada-USA Tiers Pays Sûr & Roxham Road", "Amérique du Nord",
        "Accord Tiers Pays Sûr USA Étendu 2023, Roxham Road Fermée, Haïtiens Expulsés & Systèmes Asile Engorgés 12+ Mois",
        25.0, 28.0, 30.0, 32.0),
    RefugeeRefoulementActor("RR-008", "HCR/CEDH — Convention Réfugiés 1951 & Non-Refoulement", "Global",
        "Convention 1951 149 États, Protocole 1967, CEDH Arrêts Refoulement & HCR Budget 10B$/An Protection",
        5.0, 4.0, 3.0, 6.0),
]


def analyze_refugee_refoulement() -> dict:
    entities = [a.to_dict() for a in ACTORS]
    avg = round(sum(e["composite_score"] for e in entities) / len(entities), 2)
    risk_dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: Dict[str, int] = {}
    for e in entities:
        risk_dist[e["risk_level"]] = risk_dist.get(e["risk_level"], 0) + 1
        pattern_dist[e["primary_pattern"]] = pattern_dist.get(e["primary_pattern"], 0) + 1

    top_risk = sorted(entities, key=lambda x: x["composite_score"], reverse=True)[:3]
    critiques = [e for e in entities if e["risk_level"] == "critique"]

    return {
        "total_entities": len(entities),
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": [e["name"] for e in top_risk],
        "critical_alerts": [f"{e['name'].split('—')[0].strip()}: {PATTERNS.get(e['primary_pattern'], {}).get('severity_fr', e['primary_pattern'])}" for e in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "refugee_refoulement",
        "confidence_score": 0.84,
        "data_sources": [
            "unhcr_global_trends_forced_displacement",
            "hrw_pushback_documentation_database",
            "bordermonitoring_eu_incident_reports",
        ],
        "entities": entities,
        "avg_estimated_refugee_refoulement_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    result = analyze_refugee_refoulement()
    print(f"Refugee Refoulement Engine — {result['total_entities']} acteurs, avg risque: {result['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:60]} — score {e['composite_score']}")
    print(f"Distribution: {result['risk_distribution']}")

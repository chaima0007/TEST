"""
Caelum Partners — Transnational Crime Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Le crime organisé transnational : quand les mafias défient les États.
Le crime organisé transnational génère 2 700Md$ annuellement selon l'ONUDC —
soit 3,6% du PIB mondial. Il corrompt les institutions, finance les guerres
civiles, alimente le terrorisme et constitue une menace existentielle pour
la gouvernance démocratique dans des dizaines d'États. Les cartels, mafias
et réseaux criminels opèrent désormais comme des multinationales avec des
chaînes logistiques mondiales, des services financiers parallèles et des
capacités militaires rivalisant avec celles des armées régulières.

Le cartel CJNG (Jalisco Nueva Generación) s'est imposé comme la plus puissante
organisation criminelle mondiale, exportant le fentanyl synthétique depuis
le Mexique vers 35+ pays (110 000 morts/an aux USA). Le Myanmar est devenu
la capitale mondiale de la fraude en ligne via les Scam Compounds — des
centres d'escroquerie opérés par des cartels birmans et chinois employing
100 000+ travailleurs forcés générant 64Md$ annuellement. La Ndrangheta
calabraise contrôle 80% du marché de la cocaïne européen (37Md$) via des
réseaux en Espagne, Pays-Bas et Belgique. Le Venezuela de Maduro est devenu
un narco-État avec la complicité des FARC dissidentes et du cartel dels Soles.

Risk levels (crime organisé transnational et capture étatique criminelle) :
  critique  → composite ≥ 60  (capture criminelle — État infiltré ou territoire contrôlé par le crime organisé)
  élevé     → composite ≥ 40  (criminalité transnationale active — réseaux déstabilisateurs à portée internationale)
  modéré    → composite ≥ 20  (corridors criminels — transit de flux illicites sans contrôle effectif)
  faible    → composite < 20  (coopération judiciaire exemplaire — lutte efficace contre le crime organisé)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "capture_etatique_criminelle": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions ciblées anti-narco-État — Magnitsky Act étendu aux réseaux criminels, gel des avoirs des oligarques complices et aide aux procureurs indépendants",
        "signal_fr": "narco_state_capture_score > 85 AND money_laundering_score > 85 — capture étatique par le crime organisé avec blanchiment systémique institutionnalisé",
    },
    "traite_humaine_industrielle": {
        "severity_fr": "Critique",
        "action_fr": "Coalition anti-traite — task forces mixtes internationales, sanctions contre les pays de transit et financement des centres d'accueil pour victimes de traite",
        "signal_fr": "human_trafficking_network_score > 85 — réseaux de traite humaine industrielle opérant à grande échelle avec protection de complicités étatiques",
    },
    "blanchiment_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Coopération judiciaire renforcée — partage automatique des informations financières, fermeture des paradis fiscaux complices et confiscation des avoirs criminels",
        "signal_fr": "money_laundering_score > 85 — blanchiment systématique à grande échelle transitant par des juridictions non coopératives",
    },
    "criminalite_transnationale_active": {
        "severity_fr": "Élevé",
        "action_fr": "Renforcement INTERPOL — capacités analytiques renforcées, bases de données partagées et programmes de protection des témoins internationaux",
        "signal_fr": "Criminalité transnationale active — organisations criminelles à portée internationale sans capture étatique avérée",
    },
    "cooperation_judiciaire_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Partager les modèles de coopération judiciaire — financement d'INTERPOL, de l'ONUDC et des procureurs anticorruption dans les États vulnérables",
        "signal_fr": "composite_score < 20 — coopération judiciaire exemplaire contre le crime organisé — INTERPOL, FATF et entraide pénale internationale efficaces",
    },
}


@dataclass
class TransnationalCrimeEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    narco_state_capture_score: float
    money_laundering_score: float
    human_trafficking_network_score: float
    criminal_governance_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_transnational_crime_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.narco_state_capture_score * 0.30
            + self.money_laundering_score * 0.25
            + self.human_trafficking_network_score * 0.25
            + self.criminal_governance_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_transnational_crime_index = round(self.composite_score / 100 * 10, 2)

    def _risk(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    def _pattern(self) -> str:
        if self.narco_state_capture_score >= 85 and self.money_laundering_score >= 85:
            return "capture_etatique_criminelle"
        if self.human_trafficking_network_score >= 85:
            return "traite_humaine_industrielle"
        if self.money_laundering_score >= 85:
            return "blanchiment_systematique"
        if self.composite_score >= 20:
            return "criminalite_transnationale_active"
        return "cooperation_judiciaire_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Capture étatique criminelle de {n} — institutions infiltrées ou territoires sous gouvernance de facto des organisations criminelles",
                "Narco-État ou État mafieux — complicité institutionnelle systémique entre élites politiques et réseaux criminels transnationaux",
                "Déstabilisation régionale — les capacités financières et militaires des cartels dépassent celles de l'État dans certaines zones",
            ]
        if self.risk_level == "élevé":
            return [
                f"Criminalité transnationale active de {n} — organisations criminelles à portée internationale déstabilisant les États voisins",
                "Corridors criminels prospères — trafic de drogues, d'armes et d'êtres humains transitant sans entrave par le territoire",
                "Blanchiment facilité — secteur bancaire ou immobilier utilisé pour recycler les produits du crime organisé",
            ]
        if self.risk_level == "modéré":
            return [
                f"Corridors criminels de {n} — transit de flux illicites sans contrôle effectif mais sans capture étatique établie",
                "Vulnérabilités institutionnelles — corruption localisée et déficits de gouvernance exploités par les réseaux criminels",
                "Risque d'aggravation — conditions économiques et sécuritaires favorisant l'implantation d'organisations criminelles",
            ]
        return [
            f"{n} incarne la coopération judiciaire exemplaire — INTERPOL efficace, entraide pénale active et conformité FATF",
            "Lutte anti-blanchiment rigoureuse — registres des bénéficiaires effectifs et coopération financière internationale sur les avoirs criminels",
            "Modèle de justice transnationale à exporter — formation des procureurs, protection des témoins et confiscation systématique des avoirs illicites",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "narco_state_capture_score": self.narco_state_capture_score,
            "money_laundering_score": self.money_laundering_score,
            "human_trafficking_network_score": self.human_trafficking_network_score,
            "criminal_governance_score": self.criminal_governance_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_transnational_crime_index": self.estimated_transnational_crime_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[TransnationalCrimeEntity] = [
    TransnationalCrimeEntity("TC-001", "Mexique — CJNG/Sinaloa & Capture Étatique Narco", "Amérique du Nord", "CJNG 35 Pays Export Fentanyl, Sinaloa 4 Continents & 30% Territoire sous Contrôle Cartel Effectif", 92.0, 88.0, 82.0, 85.0),
    TransnationalCrimeEntity("TC-002", "Myanmar — Scam Compounds & Traite 100K Travailleurs Forcés", "Asie du Sud-Est", "KK Park/Myawaddy 100K+ Travailleurs Forcés, 64Md$ Fraude Annuelle & Junte Complice Recrutement", 85.0, 82.0, 90.0, 78.0),
    TransnationalCrimeEntity("TC-003", "Venezuela & RDC — Narco-État & Minerais Illicites", "Amérique du Sud/Afrique", "Maduro FARC TREN DE ARAGUA, RDC FDLR/M23 Coltan & Gold Mining Milices Sans Poursuite", 88.0, 85.0, 72.0, 80.0),
    TransnationalCrimeEntity("TC-004", "Albanie & Balkans — Ndrangheta & Cocaïne Europe", "Europe du Sud-Est", "Ndrangheta 80% Cocaïne Europe 37Md$, Clans Albanais Dubaï/Duisbourg & Clandestins Via Balkans", 80.0, 88.0, 78.0, 72.0),
    TransnationalCrimeEntity("TC-005", "Nigéria — Yahoo Boys & Fraude BEC 10Md$ Mondial", "Afrique de l'Ouest", "BEC Business Email Compromise 10Md$/An, Romance Scam Diaspora & Pig Butchering Crypto Nigérian", 55.0, 62.0, 48.0, 52.0),
    TransnationalCrimeEntity("TC-006", "Maroc & Turquie — Transit Hash & Héroïne Europe", "MENA/Europe", "Maroc 70% Cannabis Européen, Turquie Route Balkanique Héroïne Afghane & Blanchiment Istanbul", 52.0, 55.0, 58.0, 48.0),
    TransnationalCrimeEntity("TC-007", "Libye & Sahel — Corridors Migrants & Crime Organisé", "Afrique du Nord", "Libye Hub Migration Irrégulière, Sahel Corridors Cocaïne/Or & Djihadisme-Crime Nexus GSIM", 30.0, 28.0, 38.0, 35.0),
    TransnationalCrimeEntity("TC-008", "INTERPOL & ONUDC — Coopération Judiciaire Mondiale", "Global", "INTERPOL 196 Membres, ONUDC Conventions Palerme/Vienne & FATF Standards AML/CFT", 5.0, 4.0, 3.0, 6.0),
]


def summary() -> dict[str, Any]:
    entities = MOCK_ENTITIES
    n = len(entities)
    avg = round(sum(e.composite_score for e in entities) / n, 2)

    risk_dist: dict[str, int] = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    pattern_dist: dict[str, int] = {k: 0 for k in PATTERNS}
    critical_alerts: list[str] = []
    top_risk: list[str] = []

    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1
        if e.risk_level == "critique":
            critical_alerts.append(f"{e.name}: {e.primary_pattern.replace('_', ' ')}")
            top_risk.append(e.name)

    return {
        "total_entities": n,
        "avg_composite": avg,
        "risk_distribution": risk_dist,
        "pattern_distribution": pattern_dist,
        "top_risk_entities": top_risk,
        "critical_alerts": critical_alerts,
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "transnational_crime",
        "confidence_score": 0.82,
        "data_sources": ["unodc_world_drug_report", "global_initiative_organized_crime", "fatf_money_laundering_monitor"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_transnational_crime_index": round(avg / 100 * 10, 2),
    }


def analyze_transnational_crime() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Transnational Crime Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")

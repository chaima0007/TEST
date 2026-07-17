"""
Caelum Partners — Political Assassination Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Assassinats politiques : l'élimination ciblée de dissidents comme outil de gouvernance.
L'assassinat politique désigne l'élimination délibérée de leaders politiques,
journalistes, activistes ou opposants par des acteurs étatiques ou para-étatiques.
Contrairement aux exécutions extrajudiciaires de masse, les assassinats politiques
ciblent des individus spécifiques pour neutraliser des voix dissidentes.

La Russie a élevé l'assassinat politique au rang d'instrument d'État structuré.
Le FSB et le GRU disposent d'unités spécialisées (Unité 29155) documentées par
Bellingcat pour des assassinats en sol étranger : Sergei Skripal (Salisbury, 2018,
Novichok), Alexander Litvinenko (Londres, 2006, Polonium-210), Alexei Navalny
(colonie pénitentiaire, 2024). Plus de 50 dissidents et journalistes russes ont
été tués depuis 2000 selon le Comité pour la protection des journalistes.

L'assassinat de Jamal Khashoggi dans le consulat saoudien d'Istanbul (2018) par
une équipe de 15 agents des services saoudiens sur ordre direct du prince héritier
Mohammed bin Salman — selon le rapport de la CIA — a provoqué une crise diplomatique
mondiale sans entraîner de sanctions significatives. L'Iran vise systématiquement
sa diaspora intellectuelle et politique : assassinats de scientifiques nucléaires,
tentatives contre des ressortissants aux États-Unis et en Europe.

Risk levels (assassinats politiques et élimination ciblée de dissidents) :
  critique  -> composite >= 60  (terrorisme assassinat — programme étatique d'élimination de dissidents)
  élevé     -> composite >= 40  (liquidation sélective — éliminations documentées avec impunité partielle)
  modéré    -> composite >= 20  (risque dissidence — menaces documentées sans programme systémique)
  faible    -> composite < 20   (protection dissidents exemplaire — garanties effectives des voix critiques)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "assassinat_etatique_transfrontalier": {
        "severity_fr": "Critique",
        "action_fr": "Sanctions Magnitsky transnationales — gel des avoirs des services de renseignement impliqués, expulsion de diplomates et mécanisme de protection des dissidents en exil",
        "signal_fr": "state_sponsored_assassination_score > 85 AND cross_border_targeting_score > 85 — assassinats d'État transfrontaliers: élimination de dissidents sur sol étranger par des agents gouvernementaux",
    },
    "elimination_journalistes_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Mécanisme UNESCO protection journalistes — enquêtes indépendantes mandatoires pour tout journaliste tué, sanctions aux gouvernements complices et fonds de protection des reporters menacés",
        "signal_fr": "journalist_activist_elimination_score > 85 — élimination systématique de journalistes et activistes: ciblage délibéré des voix critiques et indépendantes par des acteurs étatiques",
    },
    "terreur_diplomatique_assassinat": {
        "severity_fr": "Critique",
        "action_fr": "Convention internationale anti-assassinat — protocole additionnel sur la responsabilité étatique pour les assassinats extrajudiciaires et mécanisme de vérification indépendant",
        "signal_fr": "state_sponsored_assassination_score > 85 — programme d'assassinat étatique domestique ou transfrontalier sans atteindre simultanément le seuil de ciblage transfrontalier",
    },
    "liquidation_politique_active": {
        "severity_fr": "Élevé",
        "action_fr": "Mécanismes de protection spéciaux — visas de protection d'urgence pour les dissidents menacés, réseau de diplomatie d'asile et listes noires des agents de renseignement impliqués",
        "signal_fr": "Liquidation politique active — éliminations documentées d'opposants et de journalistes sans programme étatique systémique d'assassinat pleinement structuré",
    },
    "protection_dissidents_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter la protection de la dissidence — financement Freedom House, coopération renseignement anti-assassinat et aide aux programmes de protection des journalistes",
        "signal_fr": "composite_score < 20 — protection exemplaire des dissidents: garanties effectives des voix critiques, liberté de presse réelle et responsabilité pénale des agents violents",
    },
}


@dataclass
class PoliticalAssassinationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    state_sponsored_assassination_score: float
    cross_border_targeting_score: float
    journalist_activist_elimination_score: float
    assassination_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_political_assassination_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.state_sponsored_assassination_score * 0.30
            + self.cross_border_targeting_score * 0.25
            + self.journalist_activist_elimination_score * 0.25
            + self.assassination_impunity_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_political_assassination_index = round(self.composite_score / 100 * 10, 2)

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
        if self.state_sponsored_assassination_score >= 85 and self.cross_border_targeting_score >= 85:
            return "assassinat_etatique_transfrontalier"
        if self.journalist_activist_elimination_score >= 85:
            return "elimination_journalistes_systematique"
        if self.state_sponsored_assassination_score >= 85:
            return "terreur_diplomatique_assassinat"
        if self.composite_score >= 20:
            return "liquidation_politique_active"
        return "protection_dissidents_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Assassinat politique critique de {n} — programme structuré d'élimination de dissidents, journalistes et opposants par des services de renseignement étatiques avec impunité diplomatique",
                "Crime de droit international — l'assassinat d'État transfrontalier constitue une violation de la souveraineté étrangère et du droit à la vie garanti par le PIDCP",
                "Effet dissuasif global — chaque assassinat politique non sanctionné encourage d'autres régimes à adopter la même stratégie d'élimination des voix critiques",
            ]
        if self.risk_level == "élevé":
            return [
                f"Liquidation politique active de {n} — éliminations documentées d'opposants et journalistes par des acteurs liés à l'État sans programme d'assassinat pleinement institutionnalisé",
                "Journalistes en danger mortel — l'absence de protection effective des journalistes d'investigation crée une zone d'impunité exploitée par les acteurs étatiques et criminels",
                "Exil forcé comme substitut — les menaces d'assassinat contraignent les dissidents à fuir leur pays, créant un exode intellectuel qui affaiblit la société civile",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque dissidence documenté de {n} — menaces et harcèlement des voix critiques sans éliminations physiques systémiques attestées par des preuves solides",
                "Autocensure généralisée — même sans assassinats systématiques, la simple menace suffit à réduire au silence journalistes et activistes par la peur des représailles",
                "Vulnérabilité institutionnelle — les faiblesses de l'État de droit permettent aux acteurs violents d'agir contre les dissidents avec une impunité partielle",
            ]
        return [
            f"{n} incarne la protection exemplaire des dissidents — liberté de presse effective, garanties judiciaires solides et responsabilité pénale des agents de l'État violents",
            "Journalisme libre et protégé — mécanismes de protection des sources, accès à l'information garanti et poursuites effectives contre les auteurs de violences contre les journalistes",
            "Modèle de pluralisme à exporter — financement CPJ/RSF, formation des forces de sécurité et aide aux États pour renforcer la protection des voix dissidentes",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "state_sponsored_assassination_score": self.state_sponsored_assassination_score,
            "cross_border_targeting_score": self.cross_border_targeting_score,
            "journalist_activist_elimination_score": self.journalist_activist_elimination_score,
            "assassination_impunity_score": self.assassination_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_political_assassination_index": self.estimated_political_assassination_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[PoliticalAssassinationEntity] = [
    PoliticalAssassinationEntity("PA-001", "Russie/FSB-GRU — Unité 29155, Novichok & Navalny Assassiné", "Europe de l'Est", "Navalny 2024 Colonie Pénitentiaire, Skripal Novichok 2018, Litvinenko Polonium 2006 & 50+ Dissidents", 95.0, 92.0, 88.0, 90.0),
    PoliticalAssassinationEntity("PA-002", "Arabie Saoudite/MBS — Khashoggi Consulat Istanbul & Dissidents", "MENA", "Khashoggi 15 Agents Consulat 2018, CIA Rapport MBS Direct, Jamal Murdered & Omar Abdulaziz Harcelé", 88.0, 82.0, 85.0, 88.0),
    PoliticalAssassinationEntity("PA-003", "Iran/IRGC — Diaspora Ciblée, Scientifiques & Opposants Europe", "MENA", "Scientifiques Nucléaires Assassinés, Complots USA/UE IRGC, Ali Khamenei Opposants & Dissidents Paris Vienne", 85.0, 80.0, 82.0, 88.0),
    PoliticalAssassinationEntity("PA-004", "Chine/MSS — Ouïghours Diaspora, HK Militants & Espions Étudiants", "Asie", "MSS Police Stations Étrangères, Ouïghours Ciblés Diaspora, HK 1000+ Arrestations & Journalistes Disparus", 80.0, 82.0, 82.0, 85.0),
    PoliticalAssassinationEntity("PA-005", "Turquie/MIT — Journalistes Kurdes & Opposants Erdogan Étrangers", "MENA/Europe", "MIT Opérations Kurdes Irak, Journalistes Assassinés, Gülenistes Extraditions & Can Dündar Tentative Berlin", 55.0, 58.0, 52.0, 60.0),
    PoliticalAssassinationEntity("PA-006", "Inde/BJP — Journalistes RTI, Activistes & Lynchages Politiques", "Asie du Sud", "80+ Journalistes Tués Inde, Gauri Lankesh 2017, Dalite Activistes & RSS Violences Politiques Impunies", 50.0, 45.0, 55.0, 58.0),
    PoliticalAssassinationEntity("PA-007", "Mexique/Cartels — Journalistes Tués & Politiques Assassinés Élections", "Amérique du Nord", "Mexico 150+ Journalistes Tués 20 Ans, Politiques Élections Assassinés, Impunité 95% & Cartel-État Nexus", 28.0, 25.0, 32.0, 35.0),
    PoliticalAssassinationEntity("PA-008", "CPJ/RSF/Interpol — Protection Journalistes & Responsabilité Pénale", "Global", "CPJ 1500+ Journalistes Tués, RSF Classement Liberté Presse, Interpol Notice Rouge Assassins & CPTJournalistes", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "political_assassination",
        "confidence_score": 0.86,
        "data_sources": ["committee_protect_journalists_database", "reporters_without_borders_tracker", "bellingcat_assassination_investigations"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_political_assassination_index": round(avg / 100 * 10, 2),
    }


def analyze_political_assassination() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Political Assassination Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")

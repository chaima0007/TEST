"""
Caelum Partners — Forced Sterilization Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
Stérilisations forcées : le contrôle coercitif de la reproduction comme arme d'État.
Les stérilisations forcées constituent une violation grave des droits reproductifs
reconnus par les conventions internationales, notamment la Convention CEDAW et le
Programme d'Action du Caire (1994). La CPI les reconnaît comme crime contre
l'humanité lorsqu'elles sont commises dans le cadre d'une attaque systématique
et généralisée contre des populations civiles.

La Chine pratique des stérilisations forcées massives contre les femmes ouïghoures
du Xinjiang : le taux de natalité dans la région a chuté de 84% entre 2015 et
2018 selon les données officielles chinoises. Des témoignages documentés par
l'Institut australien de politique stratégique (ASPI) décrivent des stérilisations
et la pose de dispositifs intra-utérins contraints lors des détentions dans les
camps de "rééducation". L'administration Biden a qualifié ces pratiques de génocide.

En Inde, les campagnes de stérilisation forcée des années 1970-2023 ont ciblé
préférentiellement les femmes pauvres, dalits et rurales. En 2014, la mort de
13 femmes lors d'une opération de stérilisation en masse en Chhattisgarh a révélé
des conditions sanitaires désastreuses et des quotas imposés aux médecins. Les
programmes de stérilisation massive persistent dans certains États indiens.

Risk levels (stérilisations forcées et contrôle coercitif de la reproduction) :
  critique  -> composite >= 60  (stérilisation génocidaire — ciblage ethnique systématique de la reproduction)
  élevé     -> composite >= 40  (contrôle reproductif coercitif — programmes étatiques imposés sans consentement)
  modéré    -> composite >= 20  (risque reproductif — pratiques coercitives documentées sans politique systémique)
  faible    -> composite < 20   (droits reproductifs garantis — consentement éclairé effectif et accès universel)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "sterilisation_genocide_ethnique": {
        "severity_fr": "Critique",
        "action_fr": "Qualification CPI génocide — crime contre l'humanité reproductif, sanctions ciblées sur les responsables médicaux et étatiques, aide d'urgence aux communautés ciblées",
        "signal_fr": "coercive_reproductive_control_score > 85 AND ethnic_targeted_sterilization_score > 85 — stérilisation génocidaire: ciblage ethnique explicite et contrôle coercitif systémique de la reproduction",
    },
    "controle_reproductif_etatique": {
        "severity_fr": "Critique",
        "action_fr": "Mécanisme CEDAW renforcé — procédures spéciales ONU droits reproductifs, conditionnalité de l'aide médicale et poursuites des États violant la souveraineté corporelle",
        "signal_fr": "coercive_reproductive_control_score > 85 — contrôle reproductif étatique systémique: programmes de stérilisation obligatoires ou sous contrainte économique et judiciaire",
    },
    "complicite_medicale_systematique": {
        "severity_fr": "Critique",
        "action_fr": "Déontologie médicale renforcée — sanctions disciplinaires des médecins complices, formation aux droits reproductifs et protection des lanceurs d'alerte dans le secteur médical",
        "signal_fr": "state_medical_complicity_score > 85 — complicité médicale institutionnalisée: corps médical utilisé comme instrument d'État pour des stérilisations non consenties",
    },
    "sterilisation_forcee_active": {
        "severity_fr": "Élevé",
        "action_fr": "Plan d'action UNFPA — accès universel à la contraception choisie, élimination des quotas de stérilisation et aide aux victimes de stérilisations non consenties",
        "signal_fr": "Stérilisations forcées actives — pratiques de stérilisation sans consentement plein et éclairé documentées sans systématisation génocidaire ou politique étatique explicite",
    },
    "droits_reproductifs_exemplaires": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les standards reproductifs — financement UNFPA, formation des personnels médicaux aux droits reproductifs et aide aux réformes législatives dans les États défaillants",
        "signal_fr": "composite_score < 20 — droits reproductifs effectifs: consentement éclairé obligatoire, accès universel à la contraception et protection légale contre les stérilisations forcées",
    },
}


@dataclass
class ForcedSterilizationEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    coercive_reproductive_control_score: float
    ethnic_targeted_sterilization_score: float
    state_medical_complicity_score: float
    sterilization_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_forced_sterilization_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.coercive_reproductive_control_score * 0.30
            + self.ethnic_targeted_sterilization_score * 0.25
            + self.state_medical_complicity_score * 0.25
            + self.sterilization_impunity_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_forced_sterilization_index = round(self.composite_score / 100 * 10, 2)

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
        if self.coercive_reproductive_control_score >= 85 and self.ethnic_targeted_sterilization_score >= 85:
            return "sterilisation_genocide_ethnique"
        if self.coercive_reproductive_control_score >= 85:
            return "controle_reproductif_etatique"
        if self.state_medical_complicity_score >= 85:
            return "complicite_medicale_systematique"
        if self.composite_score >= 20:
            return "sterilisation_forcee_active"
        return "droits_reproductifs_exemplaires"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Stérilisation forcée critique de {n} — violation systémique de la souveraineté corporelle des femmes par des programmes étatiques de contrôle de la reproduction sans consentement",
                "Crime contre l'humanité reproductif — la stérilisation forcée constitue un crime contre l'humanité selon le Statut de Rome et un crime de génocide lorsqu'elle cible un groupe ethnique",
                "Destruction générationnelle — les stérilisations forcées ethniquement ciblées visent à éliminer une population en réduisant délibérément sa capacité de reproduction",
            ]
        if self.risk_level == "élevé":
            return [
                f"Contrôle reproductif coercitif de {n} — programmes de stérilisation sous contrainte économique, judiciaire ou médicale sans ciblage ethnique explicite documenté",
                "Consentement structurellement impossible — la pauvreté, l'analphabétisme et la dépendance aux systèmes de santé étatiques rendent le consentement libre et éclairé illusoire",
                "Impunité médicale et institutionnelle — l'absence de poursuites contre les médecins pratiquant des stérilisations non consenties perpétue les violations des droits reproductifs",
            ]
        if self.risk_level == "modéré":
            return [
                f"Risque reproductif documenté de {n} — pratiques coercitives isolées ou passées sans politique étatique systémique de contrôle de la reproduction",
                "Héritage de l'eugénisme — des pratiques historiques de stérilisation forcée continuent d'affecter les communautés victimes sans reconnaissance officielle ni réparations",
                "Vulnérabilités persistantes — certaines populations marginalisées restent exposées à des pressions informelles pour accepter une stérilisation non souhaitée",
            ]
        return [
            f"{n} incarne la protection exemplaire des droits reproductifs — consentement éclairé obligatoire, accès universel à la contraception et protection légale effective",
            "Standards CEDAW appliqués — mécanismes de plainte accessibles aux victimes de violations reproductives et sanctions effectives contre les contrevenants",
            "Modèle de droits reproductifs à exporter — financement UNFPA, formation médicale aux droits reproductifs et aide aux réformes dans les États défaillants",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "coercive_reproductive_control_score": self.coercive_reproductive_control_score,
            "ethnic_targeted_sterilization_score": self.ethnic_targeted_sterilization_score,
            "state_medical_complicity_score": self.state_medical_complicity_score,
            "sterilization_impunity_score": self.sterilization_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_forced_sterilization_index": self.estimated_forced_sterilization_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[ForcedSterilizationEntity] = [
    ForcedSterilizationEntity("FS-001", "Chine/Ouïghours — Natalité -84% Xinjiang & DIU Forcés Camps", "Asie", "Natalité Ouïghoure -84% 2015-18, ASPI Témoignages DIU Forcés, Génocide Biden Qualifié & BPC Camps Preuves", 95.0, 98.0, 92.0, 88.0),
    ForcedSterilizationEntity("FS-002", "Inde/Campagnes Masse — Quotas Médecins & Chhattisgarh 13 Mortes", "Asie du Sud", "13 Femmes Mortes Chhattisgarh 2014, Quotas Médecins État, Dalites & Rurales Ciblées & Camp Stérilisation Bihar", 88.0, 82.0, 85.0, 80.0),
    ForcedSterilizationEntity("FS-003", "USA/Californie/ICE — Prisons Stérilisations & Immigrantes Détenues", "Amérique du Nord", "ICE Centres Détention Stérilisations, Californie 1909-1979 20 000 Prisonniers, Pénitenciers Consentement Fictif", 80.0, 82.0, 88.0, 80.0),
    ForcedSterilizationEntity("FS-004", "Pérou/Fujimori — 272 000 Stérilisations Forcées Programme Nacional", "Amérique du Sud", "272 000 Stérilisations 1996-2001, Femmes Rurales Quechua Ciblées, Médecins Quotas & Fujimori Poursuite CPI", 82.0, 78.0, 75.0, 85.0),
    ForcedSterilizationEntity("FS-005", "Slovaquie/Roms — Stérilisations Hôpitaux & Décisions ECtHR", "Europe de l'Est", "Cour EDH Condamnations Multiples, Femmes Roms Stérilisées Accouchements, Gouvernement Nie & Hôpitaux Complices", 55.0, 58.0, 52.0, 60.0),
    ForcedSterilizationEntity("FS-006", "Namibie/HIV — Femmes Séropositives Stérilisées Sans Consentement", "Afrique Australe", "Femmes VIH+ Stérilisées Hôpitaux, Aveux Infirmières Documentés ONU, Jurisprudence LNE vs Namibie & Impunité", 50.0, 52.0, 48.0, 58.0),
    ForcedSterilizationEntity("FS-007", "Suède/Eugenisme Historique — 63 000 Stérilisés 1935-1975", "Europe du Nord", "63 000 Stérilisations Loi Eugeniste 1935, Femmes Handicapées & Autochtones Sami Ciblées & Réparations 1999", 28.0, 25.0, 32.0, 35.0),
    ForcedSterilizationEntity("FS-008", "OMS/UNFPA — Droits Reproductifs & Santé Sexuelle Universelle", "Global", "CEDAW 189 États, Programme Caire 1994, UNFPA 155 Pays & Directive OMS Consentement Éclairé Stérilisation", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "forced_sterilization",
        "confidence_score": 0.82,
        "data_sources": ["un_special_rapporteur_reproductive_rights", "hrw_forced_sterilization_reports", "unfpa_state_world_population"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_forced_sterilization_index": round(avg / 100 * 10, 2),
    }


def analyze_forced_sterilization() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Forced Sterilization Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} -> {e.risk_level} ({e.composite_score})")

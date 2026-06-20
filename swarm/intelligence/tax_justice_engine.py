from __future__ import annotations

from dataclasses import dataclass


DOMAIN = "taxjustice"
SLUG   = "tax-justice-engine"

PATTERNS: list[dict] = [
    {
        "name":        "Évasion Fiscale Systémique",
        "severity_fr": "critique",
        "action_fr":   "signalement_autorités_fiscales_urgence",
        "signal_fr":   "🔴 Évasion fiscale systémique détectée — intervention immédiate requise",
    },
    {
        "name":        "Optimisation Abusive Offshore",
        "severity_fr": "critique",
        "action_fr":   "audit_offshore_structures_urgence",
        "signal_fr":   "🔴 Optimisation offshore abusive — restructuration fiscale obligatoire",
    },
    {
        "name":        "Contournement Réglementaire",
        "severity_fr": "élevé",
        "action_fr":   "audit_conformité_fiscale_renforcé",
        "signal_fr":   "🟠 Contournement réglementaire actif — audit de conformité requis",
    },
    {
        "name":        "Inégalité Fiscale Structurelle",
        "severity_fr": "modéré",
        "action_fr":   "révision_politique_fiscale_équité",
        "signal_fr":   "🟡 Inégalité fiscale structurelle — révision politique fiscale recommandée",
    },
    {
        "name":        "Risque Réputation Fiscale",
        "severity_fr": "faible",
        "action_fr":   "veille_réputation_fiscale",
        "signal_fr":   "🟢 Risque réputation fiscale contenu — surveillance standard",
    },
]


@dataclass
class TaxJusticeEntity:
    entity_id:                  str
    name:                       str
    country:                    str
    sector:                     str
    evasion_score:              float
    avoidance_score:            float
    offshore_score:             float
    inequality_score:           float
    primary_pattern:            str
    key_signals:                list[str]
    # derived / computed
    composite_score:            float = 0.0
    risk_level:                 str   = "faible"
    estimated_taxjustice_index: float = 0.0
    last_updated:               str   = "2026-06-20"
    alerts:                     list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.alerts is None:
            self.alerts = []

    def to_dict(self) -> dict:
        return {
            "entity_id":                  self.entity_id,                    # 1
            "name":                       self.name,                         # 2
            "country":                    self.country,                      # 3
            "sector":                     self.sector,                       # 4
            "composite_score":            self.composite_score,              # 5
            "evasion_score":              self.evasion_score,                # 6
            "avoidance_score":            self.avoidance_score,              # 7
            "offshore_score":             self.offshore_score,               # 8
            "inequality_score":           self.inequality_score,             # 9
            "risk_level":                 self.risk_level,                   # 10
            "primary_pattern":            self.primary_pattern,              # 11
            "key_signals":                self.key_signals,                  # 12
            "estimated_taxjustice_index": self.estimated_taxjustice_index,   # 13
            "last_updated":               self.last_updated,                 # 14
            "alerts":                     self.alerts,                       # 15
        }


class TaxJusticeEngine:
    def __init__(self) -> None:
        self._entities: list[TaxJusticeEntity] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def analyze(self, entity: TaxJusticeEntity) -> TaxJusticeEntity:
        composite = round(
            entity.evasion_score   * 0.30
            + entity.avoidance_score * 0.25
            + entity.offshore_score  * 0.25
            + entity.inequality_score * 0.20,
            2,
        )
        composite = max(0.0, min(100.0, composite))
        entity.composite_score            = composite
        entity.risk_level                 = self._risk_level(composite)
        entity.estimated_taxjustice_index = round(composite / 100 * 10, 2)
        entity.alerts                     = self._build_alerts(entity)
        self._entities.append(entity)
        return entity

    def analyze_batch(self, entities: list[TaxJusticeEntity]) -> list[TaxJusticeEntity]:
        return [self.analyze(e) for e in entities]

    def reset(self) -> None:
        self._entities.clear()

    # ── helpers ─────────────────────────────────────────────────────────────────

    def _risk_level(self, composite: float) -> str:
        if composite >= 60:
            return "critique"
        if composite >= 40:
            return "élevé"
        if composite >= 20:
            return "modéré"
        return "faible"

    def _build_alerts(self, entity: TaxJusticeEntity) -> list[str]:
        alerts: list[str] = []
        if entity.risk_level == "critique":
            alerts.append(
                f"ALERTE CRITIQUE: {entity.name} — évasion fiscale systémique confirmée"
            )
            alerts.append(
                f"Signalement obligatoire aux autorités fiscales de {entity.country}"
            )
        elif entity.risk_level == "élevé":
            alerts.append(
                f"ALERTE ÉLEVÉE: {entity.name} — structures offshore suspectes détectées"
            )
        return alerts

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._entities)
        if n == 0:
            return {
                "total_entities":                0,
                "avg_composite":                 0.0,
                "risk_distribution":             {},
                "pattern_distribution":          {},
                "top_risk_entities":             [],
                "critical_alerts":               [],
                "last_analysis":                 "2026-06-20",
                "engine_version":                "tax-justice-engine-v1.0",
                "domain":                        DOMAIN,
                "confidence_score":              0.0,
                "data_sources":                  [
                    "OCDE",
                    "Tax Justice Network",
                    "OpenCorporates",
                    "ICIJ Offshore Leaks",
                ],
                "entities":                      [],
                "avg_estimated_taxjustice_index": 0.0,
            }

        risk_distribution:    dict[str, int] = {}
        pattern_distribution: dict[str, int] = {}
        total_composite    = 0.0
        critical_alerts:   list[str] = []
        top_risk_entities: list[dict] = []

        for e in self._entities:
            risk_distribution[e.risk_level] = (
                risk_distribution.get(e.risk_level, 0) + 1
            )
            pattern_distribution[e.primary_pattern] = (
                pattern_distribution.get(e.primary_pattern, 0) + 1
            )
            total_composite += e.composite_score
            if e.risk_level == "critique":
                critical_alerts.extend(e.alerts)
                top_risk_entities.append(
                    {
                        "entity_id":     e.entity_id,
                        "name":          e.name,
                        "composite_score": e.composite_score,
                        "risk_level":    e.risk_level,
                    }
                )

        avg_composite = round(total_composite / n, 2)

        return {
            "total_entities":                n,
            "avg_composite":                 avg_composite,
            "risk_distribution":             risk_distribution,
            "pattern_distribution":          pattern_distribution,
            "top_risk_entities":             top_risk_entities,
            "critical_alerts":               critical_alerts,
            "last_analysis":                 "2026-06-20",
            "engine_version":                "tax-justice-engine-v1.0",
            "domain":                        DOMAIN,
            "confidence_score":              round(min(95.0, 60.0 + n * 4.0), 2),
            "data_sources":                  [
                "OCDE",
                "Tax Justice Network",
                "OpenCorporates",
                "ICIJ Offshore Leaks",
            ],
            "entities":                      [e.to_dict() for e in self._entities],
            "avg_estimated_taxjustice_index": round(avg_composite / 100 * 10, 2),
        }


# ── pre-built mock raw data ──────────────────────────────────────────────────
# composite = evasion*0.30 + avoidance*0.25 + offshore*0.25 + inequality*0.20
#
# TAX-001  88*0.30 + 82*0.25 + 90*0.25 + 75*0.20 = 26.4+20.5+22.5+15.0 = 84.40  → critique
# TAX-002  72*0.30 + 85*0.25 + 78*0.25 + 68*0.20 = 21.6+21.25+19.5+13.6 = 75.95 → critique
# TAX-003  80*0.30 + 76*0.25 + 82*0.25 + 65*0.20 = 24.0+19.0+20.5+13.0 = 76.50  → critique
# TAX-004  55*0.30 + 60*0.25 + 52*0.25 + 45*0.20 = 16.5+15.0+13.0+9.0  = 53.50  → élevé
# TAX-005  58*0.30 + 62*0.25 + 55*0.25 + 42*0.20 = 17.4+15.5+13.75+8.4 = 55.05  → élevé
# TAX-006  28*0.30 + 32*0.25 + 25*0.25 + 38*0.20 = 8.4+8.0+6.25+7.6   = 30.25   → modéré
# TAX-007   8*0.30 + 12*0.25 +  6*0.25 + 10*0.20 = 2.4+3.0+1.5+2.0    =  8.90   → faible
# TAX-008   5*0.30 +  8*0.25 +  4*0.25 +  7*0.20 = 1.5+2.0+1.0+1.4    =  5.90   → faible

_RAW_ENTITIES: list[dict] = [
    {
        "entity_id":      "TAX-001",
        "name":           "MegaCorp Cayman Holdings",
        "country":        "Cayman Islands",
        "sector":         "Finance",
        "evasion_score":    88.0,
        "avoidance_score":  82.0,
        "offshore_score":   90.0,
        "inequality_score": 75.0,
        "primary_pattern":  "Évasion Fiscale Systémique",
        "key_signals": [
            "Transferts massifs vers paradis fiscal (Cayman Islands)",
            "Absence totale de substance économique locale",
            "Montages price-transfer vers filiales offshore",
        ],
    },
    {
        "entity_id":      "TAX-002",
        "name":           "TechGiant Ireland LLC",
        "country":        "Ireland",
        "sector":         "Technology",
        "evasion_score":    72.0,
        "avoidance_score":  85.0,
        "offshore_score":   78.0,
        "inequality_score": 68.0,
        "primary_pattern":  "Optimisation Abusive Offshore",
        "key_signals": [
            "Double Irish — structure hybride IP routing",
            "Taux effectif impôts < 2% sur bénéfices mondiaux",
            "Royalties IP transférées vers Bermudes sans activité réelle",
        ],
    },
    {
        "entity_id":      "TAX-003",
        "name":           "LuxHolding SA",
        "country":        "Luxembourg",
        "sector":         "Real Estate",
        "evasion_score":    80.0,
        "avoidance_score":  76.0,
        "offshore_score":   82.0,
        "inequality_score": 65.0,
        "primary_pattern":  "Évasion Fiscale Systémique",
        "key_signals": [
            "Rulings fiscaux secrets avec administration luxembourgeoise",
            "Structures holding opaques multi-couches",
            "Concentration immobilière sans imposition locale",
        ],
    },
    {
        "entity_id":      "TAX-004",
        "name":           "ShellCompany BV",
        "country":        "Netherlands",
        "sector":         "Consulting",
        "evasion_score":    55.0,
        "avoidance_score":  60.0,
        "offshore_score":   52.0,
        "inequality_score": 45.0,
        "primary_pattern":  "Contournement Réglementaire",
        "key_signals": [
            "Utilisation des treaty networks néerlandais pour minimisation fiscale",
            "Facturation intergroupe avec marges artificielles",
            "Boite aux lettres — 0 employés effectifs déclarés",
        ],
    },
    {
        "entity_id":      "TAX-005",
        "name":           "PharmaOffset AG",
        "country":        "Switzerland",
        "sector":         "Pharmaceuticals",
        "evasion_score":    58.0,
        "avoidance_score":  62.0,
        "offshore_score":   55.0,
        "inequality_score": 42.0,
        "primary_pattern":  "Optimisation Abusive Offshore",
        "key_signals": [
            "Propriété intellectuelle pharmaceutique délocalisée en Suisse",
            "Transfer pricing agressif sur brevets médicaux",
            "Taux effectif 5% malgré marges opérationnelles >40%",
        ],
    },
    {
        "entity_id":      "TAX-006",
        "name":           "RetailGroup SARL",
        "country":        "France",
        "sector":         "Retail",
        "evasion_score":    28.0,
        "avoidance_score":  32.0,
        "offshore_score":   25.0,
        "inequality_score": 38.0,
        "primary_pattern":  "Inégalité Fiscale Structurelle",
        "key_signals": [
            "Crédit d'impôt recherche utilisé de manière abusive",
            "Taux d'imposition effectif inférieur à PME concurrentes",
            "Optimisation TVA sur e-commerce transfrontalier",
        ],
    },
    {
        "entity_id":      "TAX-007",
        "name":           "Nordic Fair AS",
        "country":        "Denmark",
        "sector":         "Renewable Energy",
        "evasion_score":    8.0,
        "avoidance_score":  12.0,
        "offshore_score":   6.0,
        "inequality_score": 10.0,
        "primary_pattern":  "Risque Réputation Fiscale",
        "key_signals": [
            "Transparence fiscale conforme aux standards CbCR OCDE",
            "Taux effectif d'imposition aligné sur taux légal danois",
            "Aucune entité dans paradis fiscaux identifiés",
        ],
    },
    {
        "entity_id":      "TAX-008",
        "name":           "Transparent Corp",
        "country":        "Germany",
        "sector":         "Manufacturing",
        "evasion_score":    5.0,
        "avoidance_score":  8.0,
        "offshore_score":   4.0,
        "inequality_score": 7.0,
        "primary_pattern":  "Risque Réputation Fiscale",
        "key_signals": [
            "Rapports fiscaux publiés volontairement selon GRI 207",
            "Coopération complète avec les autorités fiscales allemandes",
            "Contribution fiscale totale représente 28% du résultat brut",
        ],
    },
]


def analyze_taxjustice() -> dict:
    """Main entry point: analyse all mock entities and return the summary dict."""
    engine = TaxJusticeEngine()
    for raw in _RAW_ENTITIES:
        e = TaxJusticeEntity(
            entity_id=raw["entity_id"],
            name=raw["name"],
            country=raw["country"],
            sector=raw["sector"],
            evasion_score=raw["evasion_score"],
            avoidance_score=raw["avoidance_score"],
            offshore_score=raw["offshore_score"],
            inequality_score=raw["inequality_score"],
            primary_pattern=raw["primary_pattern"],
            key_signals=raw["key_signals"],
        )
        engine.analyze(e)
    return engine.summary()


if __name__ == "__main__":
    import json

    result = analyze_taxjustice()
    print(json.dumps(result, ensure_ascii=False, indent=2))

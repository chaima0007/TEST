"""Forced Disappearance Engine — Caelum Partners Intelligence Swarm"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class ForcedDisappearanceActor:
    entity_id: str
    name: str
    country: str
    sector: str
    state_enforced_disappearance_score: float
    secret_detention_network_score: float
    family_notification_denial_score: float
    disappearance_impunity_score: float

    @property
    def composite_score(self) -> float:
        return round(
            self.state_enforced_disappearance_score * 0.30 +
            self.secret_detention_network_score * 0.25 +
            self.family_notification_denial_score * 0.25 +
            self.disappearance_impunity_score * 0.20,
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
    def estimated_forced_disappearance_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def primary_pattern(self) -> str:
        scores = {
            "disparition_forcee_etatique": self.state_enforced_disappearance_score,
            "reseau_detention_secrete": self.secret_detention_network_score,
            "deni_famille_information": self.family_notification_denial_score,
            "impunite_perpetrateurs_disparition": self.disappearance_impunity_score,
        }
        return max(scores, key=scores.get)

    @property
    def key_signals(self) -> List[str]:
        SIGNAL_MAP = {
            "disparition_forcee_etatique": f"Disparitions forcées étatiques de {self.name} — arrestations sans notification aux familles, détenus maintenus hors de toute procédure légale dans des lieux secrets",
            "reseau_detention_secrete": f"Réseau de détention secrète de {self.name} — infrastructure clandestine de lieux de détention non déclarés où les disparus sont maintenus hors de tout contrôle judiciaire",
            "deni_famille_information": f"Déni d'information aux familles par {self.name} — refus systématique de confirmer le sort des disparus, laissant les familles dans un état de deuil suspendu indéfini",
            "impunite_perpetrateurs_disparition": f"Impunité totale des auteurs de disparitions de {self.name} — absence de poursuites malgré les disparitions documentées, créant une culture d'impunité institutionnelle",
        }
        return [
            SIGNAL_MAP.get(self.primary_pattern, f"Disparitions forcées de {self.name}"),
            "Crime continu jusqu'à l'établissement du sort — la disparition forcée est un crime permanent tant que le sort de la victime reste inconnu, engageant la responsabilité internationale continue de l'État",
            "Activer le Groupe de travail ONU sur les disparitions forcées pour visites urgentes et saisir le Comité des droits de l'homme pour mesures provisoires",
        ]

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "state_enforced_disappearance_score": self.state_enforced_disappearance_score,
            "secret_detention_network_score": self.secret_detention_network_score,
            "family_notification_denial_score": self.family_notification_denial_score,
            "disappearance_impunity_score": self.disappearance_impunity_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_forced_disappearance_index": self.estimated_forced_disappearance_index,
            "last_updated": "2026-06-20",
        }


ACTORS = [
    ForcedDisappearanceActor("FD-001", "RPDC — Kwanliso Camps, Disparitions Politiques & Familles Séparées 70 Ans", "Asie du Nord-Est", "Kwanliso Camps Secrets 200 000 Détenus, Familles Séparées Guerres Corée, Rapatriements Forcés Chine & Songbun Système Punition", 95, 92, 95, 88),
    ForcedDisappearanceActor("FD-002", "Syrie/Assad — Sites Détention Secrète, 100 000+ Disparus & Torture Caesar", "MENA", "Saydnaya Prison Secrète, 100 000+ Détenus Disparus, Photos Caesar 11 000 Corps Torturés & Familles Sans Information 10 Ans", 92, 95, 90, 85),
    ForcedDisappearanceActor("FD-003", "Chine/Xinjiang — Disparitions Ouïghours, Camps ETIM & Séparations Familiales", "Asie", "1M+ Ouïghours Camps Internement, Familles Australie/Europe Sans Contact, Disparitions Activistes Taïwan & Rendan Système", 88, 85, 90, 88),
    ForcedDisappearanceActor("FD-004", "Argentine/Amérique Latine — Héritage Opération Condor & 30 000 Disparus", "Amérique du Sud", "30 000 Disparus Argentine 1976-83, Opération Condor 6 Pays, Abuelas Plaza Mayo & Impunité Partielle Procès Tardifs", 85, 82, 88, 80),
    ForcedDisappearanceActor("FD-005", "Mexique/Cartels — 100 000 Disparus & Fosses Communes Jalisco", "Amérique du Nord", "100 000+ Disparus Officiels Mexique 2006-2024, Fosses Communes Jalisco 3 000 Corps, Familles Chercheuses & CNDH Impuissance", 55, 52, 62, 58),
    ForcedDisappearanceActor("FD-006", "Russie/Tchétchénie — Filtrages, Disparitions Ukraine & Sites Secrets FSB", "Europe de l'Est", "Filtrations Tchétchénie 2000-09, Disparitions Ukrainiens 2022 HRW, Pits Mozdok Charniers & FSB Sites Detention Documentés HRW", 52, 58, 55, 55),
    ForcedDisappearanceActor("FD-007", "Sri Lanka/Colombie — Post-Conflit Disparitions & Commission Vérité Partielle", "Asie/Amérique du Sud", "Sri Lanka Fin LTTE 2009 Milliers Disparus, Colombie FARC 80 000 Disparus, Commissions Vérité Incomplètes & Familles Attente", 28, 32, 30, 28),
    ForcedDisappearanceActor("FD-008", "ONU-WGEID/ICMP — Identification Victimes & Convention Disparitions", "Global", "WGEID ONU 45+ Ans, Convention 2010 73 États Parties, ICMP ADN Identification Victimes & Bases Données Familles", 5, 4, 3, 6),
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
        "domain": "forced_disappearance",
        "confidence_score": 0.84,
        "data_sources": ["un_wgeid_annual_report", "amnesty_international_disappearances_database", "icmp_missing_persons_global_statistics"],
        "entities": entities,
        "avg_estimated_forced_disappearance_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Forced Disappearance Engine — {s['total_entities']} acteurs, avg risque: {s['avg_composite']}")
    for e in s["entities"]:
        print(f"  [{e['risk_level'].upper()}] {e['name'][:50]} — score {e['composite_score']}")
    print(f"Distribution: {s['risk_distribution']}")

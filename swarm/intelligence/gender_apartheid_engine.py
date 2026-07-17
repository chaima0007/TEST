"""
Caelum Partners — Gender Apartheid Intelligence Engine
Propriété exclusive de Chaima Mhadbi · Bruxelles
L'apartheid de genre : la discrimination systémique des femmes comme politique d'État.
Le terme "gender apartheid" — emprunté à l'apartheid racial sud-africain —
désigne les régimes qui institutionnalisent la discrimination sexuelle comme
système de gouvernance intégral. L'ONU l'a formellement reconnu pour décrire
le traitement des femmes par les Taliban en Afghanistan depuis 2021 : interdiction
de l'école au-delà de la 6ème, interdiction de travailler, interdiction de
sortir sans mahram, interdiction des espaces publics.

L'Afghanistan des Taliban représente l'expression la plus radicale de l'apartheid
de genre au monde : 14 millions de femmes vivant sous 80+ interdictions formelles,
l'éducation féminine interdite depuis 2021 créant une génération de femmes non
éduquées. La Résolution du CSNU de décembre 2022 reconnaît ce traitement comme
violation du droit international. La CPI enquête sur les traitements comme crime
contre l'humanité potentiel.

L'Iran maintient un système d'apartheid de genre moins total mais systémique :
police des mœurs, port du hijab obligatoire sous peine d'emprisonnement,
discrimination légale massive. Le mouvement "Femme, Vie, Liberté" (2022) a
exposé mondialement ces violences. L'Arabie Saoudite a partiellement réformé
son système de tutelle masculine mais maintient une discrimination légale
structurelle. Le Nigeria et le Sahel combinent loi islamique et violence de genre
institutionnalisée dans les zones sous contrôle djihadiste.

Risk levels (apartheid de genre et oppression systémique des femmes) :
  critique  → composite ≥ 60  (apartheid de genre — discrimination institutionnelle totale et violences d'État)
  élevé     → composite ≥ 40  (oppression genrée structurelle — discrimination légale et violences documentées)
  modéré    → composite ≥ 20  (inégalité persistante — discrimination genrée sans appareil répressif étatique)
  faible    → composite < 20  (égalité de genre avancée — parité légale, judiciaire et économique effective)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


PATTERNS: dict[str, dict] = {
    "apartheid_genre_total": {
        "severity_fr": "Critique",
        "action_fr": "Criminalisation de l'apartheid de genre — protocole additionnel CPI, sanctions ciblées sur les responsables, aide directe aux femmes via des canaux ONG et pression sur les États reconnaissant les Taliban",
        "signal_fr": "women_mobility_restriction_score > 85 AND women_education_denial_score > 85 — apartheid de genre total: interdictions systémiques de mobilité ET d'éducation imposées aux femmes par l'État",
    },
    "violence_genre_institutionnalisee": {
        "severity_fr": "Critique",
        "action_fr": "Mécanisme ONU violence de genre — rapporteur spécial renforcé, tribunal international pour crimes de genre et sanctions sectorielles ciblant les États pratiquant la violence institutionnalisée",
        "signal_fr": "gender_violence_institutionalized_score > 85 — violence de genre institutionnalisée par l'État: lapidation, mutilations, mariage forcé légalisés ou impunis systémiquement",
    },
    "subjugation_legale_systemique": {
        "severity_fr": "Critique",
        "action_fr": "Conditionnalité des relations diplomatiques — suspension des accords commerciaux avec les États maintenant une subjugation légale des femmes et aide aux réformes constitutionnelles",
        "signal_fr": "women_legal_subjugation_score > 85 — subjugation légale systémique: tutelle masculine obligatoire, témoignage invalide, héritage discriminatoire et absence de droits civils",
    },
    "discrimination_genre_structurelle": {
        "severity_fr": "Élevé",
        "action_fr": "Plan d'action genre ONU — conditionnalité de l'aide au développement aux progrès de l'égalité de genre, soutien aux mouvements féministes locaux et accès aux institutions judiciaires",
        "signal_fr": "Discrimination de genre structurelle — inégalités légales et sociales documentées sans appareil répressif totalisant les violations des droits des femmes",
    },
    "egalite_genre_exemplaire": {
        "severity_fr": "Faible",
        "action_fr": "Exporter les modèles d'égalité — financement d'ONU Femmes, coopération sur les réformes législatives de genre et aide aux mouvements féministes dans les pays à score critique",
        "signal_fr": "composite_score < 20 — égalité de genre avancée: parité légale, judiciaire et représentation politique équitable effectivement garanties",
    },
}


@dataclass
class GenderApartheidEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    women_mobility_restriction_score: float
    women_education_denial_score: float
    women_legal_subjugation_score: float
    gender_violence_institutionalized_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = field(init=False)
    key_signals: list[str] = field(init=False)
    estimated_gender_apartheid_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self) -> None:
        self.composite_score = round(
            self.women_mobility_restriction_score * 0.30
            + self.women_education_denial_score * 0.25
            + self.women_legal_subjugation_score * 0.25
            + self.gender_violence_institutionalized_score * 0.20,
            2,
        )
        self.risk_level = self._risk()
        self.primary_pattern = self._pattern()
        self.key_signals = self._signals()
        self.estimated_gender_apartheid_index = round(self.composite_score / 100 * 10, 2)

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
        if self.women_mobility_restriction_score >= 85 and self.women_education_denial_score >= 85:
            return "apartheid_genre_total"
        if self.gender_violence_institutionalized_score >= 85:
            return "violence_genre_institutionnalisee"
        if self.women_legal_subjugation_score >= 85:
            return "subjugation_legale_systemique"
        if self.composite_score >= 20:
            return "discrimination_genre_structurelle"
        return "egalite_genre_exemplaire"

    def _signals(self) -> list[str]:
        n = self.name
        if self.risk_level == "critique":
            return [
                f"Apartheid de genre de {n} — discrimination institutionnelle totale des femmes via un appareil législatif, judiciaire et policier systémiquement oppressif",
                "Crime contre l'humanité potentiel — la CPI enquête sur les traitements infligés aux femmes comme crime contre l'humanité sous le régime de persécution basée sur le genre",
                "Génération sacrifiée — l'interdiction de l'éducation crée une génération entière de femmes exclues de la vie économique, politique et sociale pour des décennies",
            ]
        if self.risk_level == "élevé":
            return [
                f"Oppression genrée structurelle de {n} — discrimination légale documentée, violences d'État tolérées et restrictions systémiques des droits des femmes",
                "Impunité institutionnalisée — les auteurs de violences de genre bénéficient d'une protection de facto via des systèmes juridiques discriminatoires ou défaillants",
                "Mouvement de résistance réprimé — les militantes des droits des femmes font face à des arrestations, harcèlement et violences d'État pour leur activisme",
            ]
        if self.risk_level == "modéré":
            return [
                f"Inégalité persistante de {n} — disparités de genre structurelles sans appareil répressif total mais avec des obstacles légaux, culturels et économiques documentés",
                "Gap d'application — les droits formellement reconnus restent inaccessibles faute de mécanismes d'enforcement et de recours judiciaires effectifs",
                "Risque de régression — pressions conservatrices ou religieuses pouvant compromettre les acquis de l'égalité de genre dans un contexte politique instable",
            ]
        return [
            f"{n} incarne l'égalité de genre avancée — parité légale effective, représentation politique significative et mécanismes de protection contre les violences",
            "Justice genrée exemplaire — tribunaux spécialisés sur les violences de genre, protection des lanceurs d'alerte et sanctions effectives contre les discriminateurs",
            "Modèle d'égalité à exporter — financement d'ONU Femmes, transfert de bonnes pratiques et coopération avec les mouvements féministes dans les États à haute oppression",
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "women_mobility_restriction_score": self.women_mobility_restriction_score,
            "women_education_denial_score": self.women_education_denial_score,
            "women_legal_subjugation_score": self.women_legal_subjugation_score,
            "gender_violence_institutionalized_score": self.gender_violence_institutionalized_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_gender_apartheid_index": self.estimated_gender_apartheid_index,
            "last_updated": self.last_updated,
        }


MOCK_ENTITIES: list[GenderApartheidEntity] = [
    GenderApartheidEntity("GA-001", "Afghanistan — Taliban 80+ Interdictions Femmes & Éducation Bannie", "Asie", "14M Femmes 80+ Interdictions Formelles, École Interdite 2021, Mahram Obligatoire & CSNU Résolution 2022", 95.0, 98.0, 95.0, 92.0),
    GenderApartheidEntity("GA-002", "Iran — Hijab Obligatoire, Police Mœurs & Révolution Mahsa Amini", "MENA", "Gasht-e-Ershad Police Mœurs, Mahsa Amini 2022 Morte, 500+ Manifestants Tués & Discrimination Légale Systémique", 85.0, 75.0, 82.0, 90.0),
    GenderApartheidEntity("GA-003", "Arabie Saoudite — Réformes MBS & Tutelle Masculine Résiduelle", "MENA", "Vision 2030 Réformes Partielles, Tutelle Masculine Persiste, Loujain Al-Hathloul Emprisonnée & Discrimination Légale", 80.0, 72.0, 88.0, 75.0),
    GenderApartheidEntity("GA-004", "Soudan & Somalie — Charia, MGF & Violence Genre Institutionnalisée", "Afrique", "MGF 88% Somalie 98% Djibouti, Mariage Enfant Légal 9-15 Ans, Al-Shabaab Contrôle 40% & RSF Viols Guerre", 78.0, 80.0, 75.0, 82.0),
    GenderApartheidEntity("GA-005", "Pakistan — Lois Blasphème, Mariage Enfant & Zones Tribales FATA", "Asie du Sud", "Karo-Kari Assassinats Honneur 1000+/An, FATA Coutumes Anti-Femmes, Mariage Enfant 21% & Blasphème Persecution", 55.0, 52.0, 58.0, 62.0),
    GenderApartheidEntity("GA-006", "Nigéria & Sahel — Boko Haram, Chibok & Djihadisme Anti-Genre", "Afrique de l'Ouest", "Boko Haram 276 Chibok Girls 2014, GSIM Anti-Éducation Filles, FGM 25% & Mariage Forcé Zones Rurales", 52.0, 48.0, 55.0, 58.0),
    GenderApartheidEntity("GA-007", "Inde — Dowry Deaths, Féminicides & Gaps Genre Persistants", "Asie du Sud", "6000 Dowry Deaths/An, Infanticide Féminin, 27% Femmes Actives Économiquement & Écart Salarial 34%", 28.0, 25.0, 32.0, 35.0),
    GenderApartheidEntity("GA-008", "Islande & Scandinavie — Parité Légale & Égalité Genre Exemplaire", "Europe du Nord", "Islande 1ère Égalité Genre 15 Ans Consécutifs, Congé Parental Partagé, 48% Femmes Parlement & Pay Gap <5%", 5.0, 4.0, 3.0, 6.0),
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
        "domain": "gender_apartheid",
        "confidence_score": 0.84,
        "data_sources": ["un_women_progress_report", "freedom_house_gender_discrimination", "human_rights_watch_gender_apartheid"],
        "entities": [e.to_dict() for e in entities],
        "avg_estimated_gender_apartheid_index": round(avg / 100 * 10, 2),
    }


def analyze_gender_apartheid() -> dict[str, Any]:
    """Entry point for the Caelum Partners swarm orchestrator."""
    return summary()


if __name__ == "__main__":
    r = summary()
    print(f"Gender Apartheid Engine — {r['total_entities']} acteurs, avg risque: {r['avg_composite']}")
    for e in MOCK_ENTITIES:
        print(f"  {e.entity_id}: {e.name} → {e.risk_level} ({e.composite_score})")

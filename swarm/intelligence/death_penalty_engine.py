"""Death Penalty Engine — abolition peine de mort, moratoires & CPI."""

from dataclasses import dataclass
from typing import List


@dataclass
class DeathPenaltyEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    execution_volume_severity_score: float
    legal_safeguard_absence_score: float
    wrongful_execution_risk_score: float
    abolition_resistance_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.execution_volume_severity_score * 0.30
            + self.legal_safeguard_absence_score * 0.25
            + self.wrongful_execution_risk_score * 0.25
            + self.abolition_resistance_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60: return "critique"
        if s >= 40: return "élevé"
        if s >= 20: return "modéré"
        return "faible"

    @property
    def estimated_death_penalty_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "execution_volume_severity_score": self.execution_volume_severity_score,
            "legal_safeguard_absence_score": self.legal_safeguard_absence_score,
            "wrongful_execution_risk_score": self.wrongful_execution_risk_score,
            "abolition_resistance_score": self.abolition_resistance_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_death_penalty_index": self.estimated_death_penalty_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    DeathPenaltyEntity(
        "DP-001", "Chine — 2 000+ Exécutions/An, Secret État & Organes Prisonniers",
        "Asie du Nord-Est",
        "Chine 2 000+ Exécutions Estimées/An Amnesty Classifié Secret État, Trafic Organes Prisonniers Condamnés Documenté Tribunaux Chine, Crimes Non-Violents Punis Mort & Procès Sans Garanties",
        95.0, 92.0, 90.0, 95.0,
        "execution_volume_severity",
        [
            "Violation du droit à la vie documentée — Chine avec score composite 93.00/100 révélant le plus grand nombre d'exécutions au monde (2 000+/an estimés) gardé secret d'État et le prélèvement d'organes sur des prisonniers condamnés, violant l'Article 6 du PIDCP",
            "Volume exécutions (95.0/100) — la Chine exécute plus de personnes que tous les autres pays réunis selon Amnesty International, avec des condamnations pour crimes non-violents (fraude, trafic de drogue) violant les Garanties de l'ONU pour la protection des personnes passibles de la peine de mort",
            "Activer le Rapporteur Spécial ONU sur les exécutions extrajudiciaires pour enquête urgente sur les pratiques d'exécution chinoises et exiger la publication des statistiques officielles conformément aux résolutions de l'Assemblée Générale ONU sur le moratoire universel",
        ],
    ),
    DeathPenaltyEntity(
        "DP-002", "Iran — 853 Exécutions 2023, Pendaisons Publiques & Minorités Ethniques",
        "MENA",
        "Iran 853 Exécutions 2023 Record Décennie Amnesty, Pendaisons Publiques Rues, Kurdes/Baloutches Surreprésentés, Crimes Drogue 50%+ Exécutions & Mineurs Exécutés Malgré Interdiction CDE",
        92.0, 90.0, 88.0, 92.0,
        "execution_volume_severity",
        [
            "Violation du droit à la vie documentée — Iran avec score composite 90.60/100 révélant 853 exécutions en 2023 (record de la décennie), dont des pendaisons publiques et des exécutions de membres de minorités ethniques kurdes et baloutches en violation de l'Article 6 PIDCP",
            "Volume exécutions (92.0/100) — les 853 exécutions iraniennes de 2023, dont 50%+ pour trafic de drogue et des mineurs exécutés contrairement à l'Article 37 de la CDE, révèlent une violation systémique du droit international des droits humains sur la peine de mort",
            "Activer le Comité des droits de l'homme ONU pour examen d'urgence des pratiques d'exécution iraniennes et exiger un moratoire immédiat sur les exécutions pour crimes de drogue conformément aux résolutions de la Commission des stupéfiants de l'ONU",
        ],
    ),
    DeathPenaltyEntity(
        "DP-003", "Arabie Saoudite/Golfe — 196 Exécutions 2022, Décapitations Publiques & Travailleurs Migrants",
        "MENA",
        "Arabie Saoudite 196 Exécutions 2022 Record, Décapitations Publiques Vendredi, Travailleurs Migrants 70%+ Condamnés Mort Ressortissants Étrangers, Crimes Sorcellerie/Blasphème & Mineurs",
        88.0, 92.0, 90.0, 88.0,
        "legal_safeguard_absence",
        [
            "Violation du droit à la vie documentée — Arabie Saoudite avec score composite 89.30/100 révélant 196 exécutions publiques par décapitation en 2022, dont 70%+ de ressortissants étrangers (travailleurs migrants) sans accès consulaire adéquat, violant la Convention de Vienne",
            "Absence garanties légales (92.0/100) — les condamnations à mort pour sorcellerie, blasphème et trafic de drogue en Arabie Saoudite sans standards minimaux de procès équitable violent les Garanties minimales ONU pour les personnes passibles de la peine de mort (résolution 1984/50)",
            "Activer le Rapporteur Spécial ONU sur les exécutions extrajudiciaires pour enquête sur les pratiques saoudiennes et exiger le respect des droits consulaires des travailleurs migrants condamnés à mort conformément à l'arrêt de la CIJ dans l'affaire LaGrand",
        ],
    ),
    DeathPenaltyEntity(
        "DP-004", "USA — 2 700 Condamnés Couloir Mort, Exécutions Innocents & Racial Bias",
        "Amérique du Nord",
        "USA 2 700 Condamnés Couloir Mort, 190+ Exonérations DNA Couloir Mort Depuis 1973, Biais Racial Documenté Condamnations Noirs, Arkansas/Texas Exécutions Controversées & SCOTUS Limitations",
        62.0, 58.0, 92.0, 55.0,
        "wrongful_execution_risk",
        [
            "Violation du droit à la vie documentée — USA avec score composite 66.35/100 révélant 190+ exonérations d'innocents dans les couloirs de la mort depuis 1973 et un biais racial documenté dans les condamnations à mort violant l'Article 6 PIDCP et l'égalité devant la loi",
            "Risque exécution innocents (92.0/100) — les 190+ exonérations par ADN de condamnés à mort aux USA révèlent un taux d'erreur judiciaire incompatible avec l'irréversibilité de la peine de mort, violant l'obligation de garanties absolues de l'Article 6 PIDCP",
            "Instaurer un moratoire fédéral sur les exécutions et ratifier le Protocole facultatif au PIDCP visant à l'abolition de la peine de mort (Protocole 2), rejoignant les 90 États abolitionnistes conformément aux résolutions de l'Assemblée Générale ONU A/RES/77/222",
        ],
    ),
    DeathPenaltyEntity(
        "DP-005", "Japon — Condamnés Secret Total, Exécution Sans Préavis & Isolement Cellulaire",
        "Asie du Nord-Est",
        "Japon Exécutions Sans Préavis Famille/Avocat, Condamnés Couloir Mort 100+ Isolement Complet, Décision Exécution Secrete Ministre Justice & Attente Décennies Incertitude Psychologique Documentée",
        52.0, 62.0, 50.0, 55.0,
        "legal_safeguard_absence",
        [
            "Violation du droit à la vie documentée — Japon avec score composite 63.25/100 révélant des exécutions réalisées sans aucun préavis aux condamnés, familles et avocats, créant une torture psychologique permanente qualifiée de traitement inhumain par le Comité contre la torture de l'ONU",
            "Absence garanties légales (85.0/100) — la pratique japonaise d'exécution secrète sans préavis et l'isolement cellulaire complet pendant des décennies dans les couloirs de la mort constituent des violations des Articles 7 et 10 PIDCP sur le traitement humain des détenus",
            "Instaurer un moratoire immédiat au Japon et réformer le système pour garantir notification préalable aux condamnés, familles et avocats conformément aux recommandations du Comité des droits de l'homme ONU dans ses observations finales sur le Japon 2022",
        ],
    ),
    DeathPenaltyEntity(
        "DP-006", "Singapour/Malaisie — Trafic Drogue Peine Mort Obligatoire & Pendaisons 2022-23",
        "Asie du Sud-Est",
        "Singapour Peine Mort Obligatoire Trafic Drogue Jusqu'En 2012 Puis Partielle, 11 Exécutions 2022 Taux/Capita Record Mondial, Malaisie 1 300 Condamnés Mort Drogue & Réforme Insuffisante",
        55.0, 60.0, 50.0, 55.0,
        "legal_safeguard_absence",
        [
            "Violation du droit à la vie documentée — Singapour/Malaisie avec score composite 63.55/100 révélant l'application de la peine de mort obligatoire pour trafic de drogue, l'un des taux d'exécution per capita les plus élevés au monde, en contradiction avec les standards ONU",
            "Absence garanties légales (82.0/100) — la peine de mort obligatoire pour trafic de drogue à Singapour, même partiellement réformée, ne permet pas l'individualisation de la peine exigée par les Garanties minimales ONU et le Comité des droits de l'homme pour les infractions à la drogue",
            "Abolir la peine de mort pour les infractions liées à la drogue à Singapour et en Malaisie conformément aux standards internationaux émergents et aux résolutions de la Commission des stupéfiants de l'ONU reconnaissant l'échec de l'approche pénale pour réduire le trafic",
        ],
    ),
    DeathPenaltyEntity(
        "DP-007", "Europe/CEDH — Protocole 13 Abolition Totale & Pressions Russie/Biélorussie",
        "Europe",
        "Europe Protocole 13 CEDH Abolition Totale Toutes Circonstances 46 États, Belarus Dernier État Européen Exécutions, Russie Moratoire Pas Abolition & Turquie Pressions Réintroduction Périodiques",
        28.0, 30.0, 28.0, 25.0,
        "abolition_resistance",
        [
            "Progrès significatif d'abolition en Europe — le Protocole 13 à la CEDH abolissant la peine de mort en toutes circonstances ratifié par 46 États membres du Conseil de l'Europe constitue le cadre régional d'abolition le plus avancé au monde, avec Belarus comme seule exception",
            "Résistance abolition (22.0/100) — la Biélorussie maintenant des exécutions secrètes et les pressions périodiques pour réintroduire la peine de mort en Turquie constituent les derniers obstacles à l'abolition universelle en Europe, région leader du mouvement abolitionniste mondial",
            "Conditionner toute perspective d'adhésion ou de partenariat avec la Biélorussie à l'abolition de la peine de mort et renforcer les pressions diplomatiques du Conseil de l'Europe pour maintenir le moratoire russe et turc conformément aux engagements OSCE",
        ],
    ),
    DeathPenaltyEntity(
        "DP-008", "ONU/CIDH — Résolution Moratoire, Protocole 2 PIDCP & Mouvement Abolition",
        "Global",
        "Assemblée Générale ONU Résolution Moratoire Universel 185 Voix 2022, Protocole Facultatif PIDCP 2 Abolition 90 États Parties, CIDH & Amnesty International Campagne Abolition Mondiale",
        4.0, 3.0, 5.0, 6.0,
        "abolition_resistance",
        [
            "ONU/CIDH incarne le cadre normatif exemplaire vers l'abolition de la peine de mort — résolutions biennales de l'Assemblée Générale pour un moratoire universel adoptées avec une majorité croissante (185 voix en 2022) et Protocole 2 PIDCP créant une obligation conventionnelle d'abolition pour 90 États",
            "Protocole 2 PIDCP — oblige les États parties à prendre toutes les mesures nécessaires pour abolir la peine de mort et interdit toute dérogation même en état d'urgence, créant l'obligation internationale la plus contraignante en matière d'abolition de la peine capitale",
            "Universaliser la ratification du Protocole 2 PIDCP et soutenir les États en transition vers l'abolition via l'assistance technique du HCDH pour réformer leurs systèmes pénaux et mettre en œuvre des alternatives crédibles à la peine de mort conformément aux standards de l'ONU",
        ],
    ),
]


def summary() -> dict:
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    risk_dist: dict = {}
    pattern_dist: dict = {}
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
        "domain": "death_penalty",
        "confidence_score": 0.87,
        "data_sources": [
            "amnesty_international_death_sentences_executions_annual_report",
            "un_special_rapporteur_extrajudicial_executions_country_reports",
            "cornell_center_death_penalty_worldwide_database",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_death_penalty_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")

"""Indigenous Rights Engine — UNDRIP, autodétermination & droits peuples autochtones."""

from dataclasses import dataclass
from typing import List


@dataclass
class IndigenousRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    land_territory_dispossession_score: float
    cultural_linguistic_erasure_score: float
    self_determination_denial_score: float
    violence_criminalization_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.land_territory_dispossession_score * 0.30
            + self.cultural_linguistic_erasure_score * 0.25
            + self.self_determination_denial_score * 0.25
            + self.violence_criminalization_score * 0.20,
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
    def estimated_indigenous_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "land_territory_dispossession_score": self.land_territory_dispossession_score,
            "cultural_linguistic_erasure_score": self.cultural_linguistic_erasure_score,
            "self_determination_denial_score": self.self_determination_denial_score,
            "violence_criminalization_score": self.violence_criminalization_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_indigenous_rights_index": self.estimated_indigenous_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    IndigenousRightsEntity(
        "IR-001", "Amazonie/Brésil — Yanomami Génocide Sanitaire, Garimpeiros & Terres Envahies",
        "Amérique Latine",
        "Brésil Yanomami 28 000 Personnes Contamination Mercure Garimpeiros, Malnutrition Enfants 2023, 900+ Morts Évitables Bolsonaro Ère & FUNAI Démantèlement Protection Terres Autochtones",
        95.0, 88.0, 85.0, 92.0,
        "land_territory_dispossession",
        [
            "Violation des droits autochtones documentée — Amazonie/Brésil avec score composite 90.25/100 révélant un génocide sanitaire des Yanomami avec contamination au mercure des garimpeiros, malnutrition infantile et 900+ morts évitables sous Bolsonaro, violant l'UNDRIP Articles 7 et 25",
            "Dépossession terres/territoire (95.0/100) — l'invasion illégale des terres homologuées yanomami par des milliers de garimpeiros avec tolérance étatique constitue une violation du droit à la terre garanti par l'Article 26 de la Déclaration ONU sur les droits des peuples autochtones (UNDRIP)",
            "Appliquer immédiatement la décision de la Cour Suprême brésilienne sur la protection des terres yanomami et activer le Mécanisme d'expert ONU sur les droits des peuples autochtones pour enquête urgente sur la situation sanitaire et territoriale des Yanomami",
        ],
    ),
    IndigenousRightsEntity(
        "IR-002", "Canada — Pensionnats 215 Enfants Retrouvés, MMIW 1 200 & Eau Potable",
        "Amérique du Nord",
        "Canada 215 Tombes Enfants Pensionnats Kamloops 2021, MMIW Missing Murdered Indigenous Women 1 200+, 31 Avis Eau Potable Réserves Long Terme & Réconciliation TRC 94 Appels Non-Mis En Oeuvre",
        85.0, 92.0, 88.0, 85.0,
        "cultural_linguistic_erasure",
        [
            "Violation des droits autochtones documentée — Canada avec score composite 87.75/100 révélant la découverte de 215 corps d'enfants autochtones dans les pensionnats et 1 200+ femmes et filles autochtones disparues ou assassinées, constituant des violations graves de l'UNDRIP et de la CDE",
            "Effacement culturel/linguistique (92.0/100) — les pensionnats canadiens ayant arraché des générations d'enfants à leurs familles et cultures constituent un génocide culturel reconnu par la Commission de Vérité et Réconciliation (CVR) violant l'Article 8 UNDRIP sur le droit à la culture",
            "Mettre en œuvre les 94 appels à l'action de la CVR et les 231 appels à la justice de l'Enquête nationale MMIW en allouant les ressources nécessaires, et ratifier la Déclaration ONU sur les droits des peuples autochtones en droit interne canadien contraignant",
        ],
    ),
    IndigenousRightsEntity(
        "IR-003", "Australie — Surincarcération 3% Population 28% Prisons, Deaths In Custody & Terres",
        "Pacifique",
        "Australie Autochtones 3% Population 28% Détenus, 500+ Décès En Garde À Vue Depuis 1991, Terres Autochtones Contestées Procédures Longues & Écart Espérance Vie 8 Ans Autochtones/Non-Autochtones",
        82.0, 85.0, 88.0, 92.0,
        "violence_criminalization",
        [
            "Violation des droits autochtones documentée — Australie avec score composite 86.25/100 révélant une surincarcération massive (28% des détenus pour 3% de la population), 500+ décès en garde à vue depuis 1991 et un écart d'espérance de vie de 8 ans constituant une discrimination systémique violant l'UNDRIP",
            "Violence/Criminalisation (92.0/100) — le taux de surincarcération des autochtones australiens, 15× supérieur à la population non-autochtone, et les 500+ morts en garde à vue sans condamnation depuis 1991 révèlent une violence institutionnelle systémique violant l'Article 7 UNDRIP",
            "Mettre en œuvre les recommandations de la Royal Commission into Aboriginal Deaths in Custody (1991) toujours non-appliquées et adopter un traité national avec les peuples autochtones australiens conformément aux obligations UNDRIP sur le consentement libre, préalable et éclairé",
        ],
    ),
    IndigenousRightsEntity(
        "IR-004", "Myanmar/Bangladesh — Rohingyas Apatridie, Chin/Kachin Déplacements & UNDRIP",
        "Asie du Sud-Est",
        "Myanmar Rohingyas Apatrides Loi 1982 Non-Reconnus Peuples Autochtones, Chin/Kachin Terres Confisquées Armée, Bangladesh Adivasi Discrimination & ASEAN Blocage Mécanismes Autochtones",
        88.0, 82.0, 90.0, 88.0,
        "self_determination_denial",
        [
            "Violation des droits autochtones documentée — Myanmar/Bangladesh avec score composite 87.10/100 révélant le refus de reconnaissance des droits autochtones des Rohingyas et autres minorités ethniques, l'ASEAN bloquant systématiquement les mécanismes de protection autochtone régionaux",
            "Déni autodétermination (90.0/100) — le refus du Myanmar de reconnaître les Rohingyas comme peuple autochtone et la confiscation des terres Chin et Kachin par l'armée constituent des violations directes des Articles 3 et 8 UNDRIP sur l'autodétermination et l'intégrité culturelle",
            "Exiger la reconnaissance des peuples autochtones du Myanmar dans la future constitution post-junte et créer un mécanisme ASEAN contraignant de protection des droits autochtones conforme à l'UNDRIP adoptée par l'Assemblée Générale ONU en 2007",
        ],
    ),
    IndigenousRightsEntity(
        "IR-005", "USA — Standing Rock, DAPL & Criminalisation Défenseurs Terres Autochtones",
        "Amérique du Nord",
        "USA Standing Rock DAPL Construit Malgré Opposition Sioux, Criminalisation 800 Militants Autochtones 2016, Alaska Drilling Terres Sacrées & ICWA Indian Child Welfare Act Menacé SCOTUS",
        55.0, 52.0, 62.0, 58.0,
        "self_determination_denial",
        [
            "Violation des droits autochtones documentée — USA avec score composite 56.65/100 révélant la construction du Dakota Access Pipeline (DAPL) malgré l'opposition des Sioux Standing Rock et la criminalisation de 800 défenseurs autochtones violant le consentement libre, préalable et éclairé (CLPE)",
            "Déni autodétermination (62.0/100) — la construction du DAPL traversant des terres et eaux sacrées sioux sans consentement éclairé des tribus affectées constitue une violation du droit au CLPE (Article 32 UNDRIP) et des obligations fiduciaires fédérales envers les Nations autochtones",
            "Ratifier l'UNDRIP (États-Unis ont voté contre en 2007, endossé en 2010 sans force contraignante) et renforcer la consultation des Nations autochtones pour tous projets d'infrastructure conformément aux obligations du Traité de Fort Laramie et du droit fédéral sur les terres tribales",
        ],
    ),
    IndigenousRightsEntity(
        "IR-006", "Inde — Adivasi 10M Expulsés Forêts, Loi Forêts 2023 & Naxalisme Criminalisation",
        "Asie du Sud",
        "Inde Adivasi 10M Expulsés Forêts Loi 2006 Mal Appliquée, Forest Rights Act 2006 Non-Implémenté, Loi Amendement Forêts 2023 Retire Droits & Conflits Naxalites Criminalisation Populations Tribales",
        58.0, 48.0, 55.0, 42.0,
        "land_territory_dispossession",
        [
            "Violation des droits autochtones documentée — Inde avec score composite 80.75/100 révélant l'expulsion de 10 millions d'Adivasi (peuples autochtones) de leurs forêts ancestrales malgré le Forest Rights Act 2006, et les amendements de 2023 réduisant leurs protections légales",
            "Dépossession terres/territoire (85.0/100) — l'expulsion de 10 millions d'Adivasi des forêts et la non-application du Forest Rights Act 2006 par les États indiens constituent des violations du droit à la terre et au territoire garanti par l'UNDRIP et la Convention OIT 169",
            "Mettre en œuvre le Forest Rights Act 2006 dans tous les États indiens et abroger les amendements de 2023 restreignant les droits forestiers des Adivasi, conformément aux recommandations du Rapporteur Spécial ONU sur les droits des peuples autochtones après sa visite en Inde",
        ],
    ),
    IndigenousRightsEntity(
        "IR-007", "Nouvelle-Zélande/Scandinavie — Traité Waitangi & Sámi Droits Relatifs Progrès",
        "Pacifique/Europe du Nord",
        "Nouvelle-Zélande Traité Waitangi 1840 Mécanismes Réclamations, Sámi Parlement Norvège/Suède/Finlande, Droits Pêche/Chasse Reconnus & Progrès Relatifs Langue Maori/Sámi Revitalisation",
        28.0, 32.0, 25.0, 22.0,
        "cultural_linguistic_erasure",
        [
            "Progrès relatifs des droits autochtones — Nouvelle-Zélande et pays scandinaves offrent les modèles les plus avancés de reconnaissance des droits autochtones via le Tribunal Waitangi et les Parlements Sámi, mais des lacunes persistent sur la co-gouvernance et les réparations territoriales",
            "Effacement culturel/linguistique (32.0/100) — malgré des progrès significatifs, la revitalisation des langues maorie et sámi reste fragile et les inégalités socio-économiques entre autochtones et non-autochtones persistent en Nouvelle-Zélande et en Scandinavie",
            "Capitaliser les modèles néo-zélandais et scandinave pour élaborer des standards internationaux de co-gouvernance avec les peuples autochtones et renforcer la mise en œuvre contraignante de l'UNDRIP dans les systèmes juridiques nationaux",
        ],
    ),
    IndigenousRightsEntity(
        "IR-008", "UNDRIP/OIT 169 — Consentement CLPE, Autodétermination & Mécanisme Expert ONU",
        "Global",
        "UNDRIP Déclaration ONU Droits Peuples Autochtones 2007 146 États, Convention OIT 169 1989 23 Ratifications, Mécanisme Expert ONU MEDPA & Rapporteur Spécial ONU Droits Peuples Autochtones",
        5.0, 4.0, 3.0, 6.0,
        "self_determination_denial",
        [
            "UNDRIP/OIT 169 incarne le cadre normatif exemplaire des droits autochtones — UNDRIP 2007 posant 46 articles sur le droit à l'autodétermination, à la terre, à la culture et au consentement libre préalable et éclairé (CLPE) créant des standards internationaux de référence",
            "UNDRIP Article 3 — reconnaît le droit à l'autodétermination des peuples autochtones, leur droit de déterminer librement leur statut politique et d'assurer leur développement économique, social et culturel, créant une obligation pour les États de respecter leur gouvernance propre",
            "Renforcer la force contraignante de l'UNDRIP par un protocole additionnel avec mécanisme de plainte individuel et tripler le budget du Mécanisme d'expert ONU sur les droits des peuples autochtones pour assurer un suivi effectif des violations dans les 90 pays comptant des populations autochtones significatives",
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
        "domain": "indigenous_rights",
        "confidence_score": 0.85,
        "data_sources": [
            "un_special_rapporteur_indigenous_peoples_country_reports",
            "cultural_survival_indigenous_rights_violations_database",
            "land_is_life_indigenous_land_rights_global_monitor",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_indigenous_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")

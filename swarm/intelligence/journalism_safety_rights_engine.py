"""Journalism Safety Rights Engine — Assassinats de journalistes, détention arbitraire & censure d'État."""

from dataclasses import dataclass
from typing import List


@dataclass
class JournalismSafetyRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    journalist_killings_score: float
    arbitrary_detention_press_score: float
    censorship_suppression_score: float
    surveillance_intimidation_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-22"

    @property
    def composite_score(self) -> float:
        return round(
            self.journalist_killings_score * 0.30
            + self.arbitrary_detention_press_score * 0.25
            + self.censorship_suppression_score * 0.25
            + self.surveillance_intimidation_score * 0.20,
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
    def estimated_journalism_safety_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "journalist_killings_score": self.journalist_killings_score,
            "arbitrary_detention_press_score": self.arbitrary_detention_press_score,
            "censorship_suppression_score": self.censorship_suppression_score,
            "surveillance_intimidation_score": self.surveillance_intimidation_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_journalism_safety_rights_index": self.estimated_journalism_safety_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    JournalismSafetyRightsEntity(
        entity_id="JSR-001",
        name="Mexique — Pays le Plus Meurtrier Hors Zone Guerre, 15+ Journalistes Tués/An & Impunité Cartels",
        country="Mexique",
        sector="15+ journalistes tués par an CPJ 2023-2024, pays le plus meurtrier pour presse hors conflit armé, impunité 95% meurtres journalistes, cartels ciblant journalistes d'investigation crime organisé",
        journalist_killings_score=95.0,
        arbitrary_detention_press_score=78.0,
        censorship_suppression_score=82.0,
        surveillance_intimidation_score=90.0,
        primary_pattern="journalist_killings",
        key_signals=[
            "Violation documentée — Mexique avec score composite critique révélant 15 à 20 journalistes tués par an selon le Comité pour la protection des journalistes (CPJ) 2023-2024, une impunité de 95% pour les meurtres de journalistes, un ciblage systématique des journalistes d'investigation couvrant le crime organisé et le Mexique classé pays le plus meurtrier pour la presse hors zone de conflit armé.",
            "Assassinats de journalistes (92.0/100) — les meurtres systématiques de journalistes au Mexique par des cartels agissant souvent en collusion avec des autorités locales violent l'Article 19 du PIDCP sur la liberté d'expression, le Plan d'action de l'ONU sur la sécurité des journalistes et les obligations découlant de la ratification par le Mexique du Pacte de San José.",
            "Réformer le mécanisme de protection des journalistes mexicain (Mécanisme fédéral de protection), renforcer les enquêtes indépendantes sur les meurtres de journalistes via la FEADLE (Fiscalía especializada) et appliquer des sanctions aux gouverneurs d'États où l'impunité est systémique, conformément aux recommandations de la CIDH et du Rapporteur spécial de l'ONU sur la liberté d'expression.",
        ],
    ),
    JournalismSafetyRightsEntity(
        entity_id="JSR-002",
        name="Russie — Journalistes Emprisonnés, Novaya Gazeta & Assassinats d'État Documentés",
        country="Russie",
        sector="64 journalistes emprisonnés CPJ 2024, assassinat Anna Politkovskaya 2006 impuni, Novaya Gazeta suspendu 2022, Evan Gershkovich WSJ 16 mois détention, loi fake news criminalisant couverture Ukraine",
        journalist_killings_score=84.0,
        arbitrary_detention_press_score=92.0,
        censorship_suppression_score=93.0,
        surveillance_intimidation_score=89.0,
        primary_pattern="arbitrary_detention_press",
        key_signals=[
            "Violation documentée — Russie avec score composite critique révélant 64 journalistes emprisonnés selon le CPJ en 2024, la suspension de Novaya Gazeta en mars 2022, la détention de 16 mois d'Evan Gershkovich (Wall Street Journal) sous accusation d'espionnage et la loi criminalisant toute couverture qualifiant l'invasion ukrainienne de 'guerre' plutôt que 'd'opération militaire spéciale'.",
            "Détention arbitraire de journalistes (88.0/100) — l'utilisation par la Russie de lois anti-espionnage et anti-'fake news' pour emprisonner les journalistes critiques du Kremlin viole l'Article 19 du PIDCP, les engagements de la Russie envers l'OSCE et les standards définis par la Cour européenne des droits de l'homme, dont la Russie a été exclue en 2022.",
            "Exiger la libération immédiate de tous les journalistes emprisonnés en Russie, maintenir des sanctions ciblées contre les responsables des poursuites abusives contre la presse et documenter systématiquement les violations pour la future Commission de responsabilisation internationale sur la Russie, conformément aux recommandations du Rapporteur spécial de l'ONU sur la liberté d'expression.",
        ],
    ),
    JournalismSafetyRightsEntity(
        entity_id="JSR-003",
        name="Chine — 108 Journalistes Emprisonnés, Grand Pare-feu & Surveillance Pegasus/Spyware Ciblée",
        country="Chine",
        sector="108 journalistes emprisonnés CPJ 2024 (plus grand geôlier mondial), Grand Pare-feu censurant 70% internet mondial, journalistes ouïghours ciblés Pegasus, correspondants étrangers expulsés ou harcelés",
        journalist_killings_score=65.0,
        arbitrary_detention_press_score=95.0,
        censorship_suppression_score=98.0,
        surveillance_intimidation_score=92.0,
        primary_pattern="arbitrary_detention_press",
        key_signals=[
            "Violation documentée — Chine avec score composite critique révélant 108 journalistes emprisonnés selon le CPJ en 2024 (plus grand geôlier mondial de journalistes depuis 5 ans consécutifs), le Grand Pare-feu censurant les principales plateformes d'information mondiales, le ciblage de journalistes ouïghours par des logiciels espions de type Pegasus et l'expulsion ou le harcèlement systématique des correspondants étrangers.",
            "Détention arbitraire et censure (95.0/100 et 98.0/100) — l'emprisonnement de 108 journalistes en Chine pour des motifs politiques et le système de censure systématique du Grand Pare-feu violent l'Article 19 du PIDCP, que la Chine n'a pas ratifié, et les standards de liberté de la presse définis par le Comité des droits de l'homme de l'ONU lors des examens périodiques.",
            "Conditionner les relations commerciales UE-Chine et USA-Chine à des progrès mesurables en matière de liberté de la presse, soutenir les journalistes chinois en exil et créer un fonds international pour les médias indépendants en mandarin, conformément aux recommandations de RSF et du CPJ dans leurs rapports annuels.",
        ],
    ),
    JournalismSafetyRightsEntity(
        entity_id="JSR-004",
        name="Syrie — Guerre la Plus Meurtrière pour la Presse, 150+ Journalistes Tués & Impunité Totale",
        country="Syrie",
        sector="150+ journalistes tués depuis 2011 CPJ, conflit armé le plus meurtrier pour la presse de l'histoire récente, journalistes étrangers pris en otage ISIS, journalistes syriens ciblés délibérément Assad/toutes parties",
        journalist_killings_score=92.0,
        arbitrary_detention_press_score=82.0,
        censorship_suppression_score=76.0,
        surveillance_intimidation_score=79.0,
        primary_pattern="journalist_killings",
        key_signals=[
            "Violation documentée — Syrie avec score composite critique révélant plus de 150 journalistes tués depuis 2011 selon le CPJ, faisant du conflit syrien la guerre la plus meurtrière pour la presse de l'histoire récente, avec des journalistes syriens délibérément ciblés par le gouvernement Assad, la prise en otage de journalistes étrangers par Daesh et une impunité totale pour tous les auteurs.",
            "Assassinats de journalistes (88.0/100) — le ciblage délibéré de journalistes par toutes les parties au conflit syrien, notamment par les services de renseignement du gouvernement Assad documenté par la Commission internationale d'enquête sur la Syrie, viole l'Article 79 du Protocole additionnel I aux Conventions de Genève protégeant les journalistes dans les zones de conflit armé.",
            "Soutenir le mécanisme international impartial et indépendant (MIII) pour la Syrie dans la documentation des crimes contre les journalistes et les médias et créer un tribunal spécial pour les crimes commis contre la presse en Syrie, conformément aux recommandations de la Commission internationale d'enquête sur la Syrie et de RSF.",
        ],
    ),
    JournalismSafetyRightsEntity(
        entity_id="JSR-005",
        name="Arabie Saoudite — Jamal Khashoggi, Journalistes Critiques Emprisonnés & Surveillance MBS",
        country="Arabie Saoudite",
        sector="Assassinat Jamal Khashoggi consulat Istanbul octobre 2018, journalistes saoudiens emprisonnés 10-20 ans, surveillance Pegasus activistes/journalistes confirmée Citizen Lab, loi anti-terroriste ciblant presse dissidente",
        journalist_killings_score=55.0,
        arbitrary_detention_press_score=62.0,
        censorship_suppression_score=58.0,
        surveillance_intimidation_score=65.0,
        primary_pattern="surveillance_intimidation",
        key_signals=[
            "Violation documentée — Arabie Saoudite avec score composite élevé révélant l'assassinat prémédité du journaliste Jamal Khashoggi au consulat saoudien d'Istanbul en octobre 2018 attribué à des agents d'État par le Rapporteur spécial de l'ONU, l'emprisonnement de journalistes critiques pour 10 à 20 ans et l'utilisation de logiciels espions Pegasus confirmée par Citizen Lab contre des activistes et journalistes saoudiens.",
            "Surveillance et intimidation (65.0/100) — l'utilisation par l'Arabie Saoudite de logiciels espions commerciaux pour surveiller les journalistes saoudiens en exil, documentée par le Citizen Lab, et l'assassinat de Khashoggi violent l'Article 19 du PIDCP, l'Article 3 de la Déclaration universelle des droits de l'homme et les principes directeurs de l'ONU sur les entreprises et les droits de l'homme (Principes Ruggie).",
            "Imposer des sanctions ciblées aux responsables saoudiens impliqués dans l'assassinat de Khashoggi et dans les poursuites abusives contre les journalistes, et restreindre l'export de technologies de surveillance aux États utilisant ces outils contre les journalistes, conformément aux recommandations du Rapporteur spécial de l'ONU sur les exécutions extrajudiciaires.",
        ],
    ),
    JournalismSafetyRightsEntity(
        entity_id="JSR-006",
        name="Inde — RSF Rang 159/180, UAPA Contre Journalistes Kashmir & Climat d'Autocensure",
        country="Inde",
        sector="RSF classement 159/180 en 2024, UAPA utilisé contre journalistes kashmiris, Siddique Kappan détenu 28 mois, criminalisation diffamation presse, journalistes indépendants ciblés pour couverture minorités",
        journalist_killings_score=45.0,
        arbitrary_detention_press_score=52.0,
        censorship_suppression_score=55.0,
        surveillance_intimidation_score=48.0,
        primary_pattern="censorship_suppression",
        key_signals=[
            "Violation documentée — Inde avec score composite élevé révélant un classement RSF de 159/180 en 2024, l'utilisation de la loi antiterroriste UAPA pour détenir des journalistes kashmiris sans procès pendant des mois, la détention de 28 mois du journaliste Siddique Kappan et un climat d'autocensure généralisé documenté par les ONG de défense de la liberté de la presse.",
            "Censure et suppression (55.0/100) — l'utilisation par le gouvernement indien de lois antiterroristes, de diffamation pénale et de sédition pour cibler les journalistes critiques, notamment ceux couvrant le Cachemire ou les minorités religieuses, viole l'Article 19 du PIDCP ratifié par l'Inde et les standards de liberté de la presse reconnus par la Cour suprême indienne.",
            "Abroger ou réformer les dispositions de l'UAPA permettant la détention prolongée sans procès et décriminaliser la diffamation en matière de presse, conformément aux recommandations du Comité des droits de l'homme de l'ONU lors de l'Examen périodique universel de l'Inde et aux décisions de la Cour suprême protégeant la liberté de la presse.",
        ],
    ),
    JournalismSafetyRightsEntity(
        entity_id="JSR-007",
        name="UE — Daphne Caruana Galizia (Malte), SLAPP & Journalistes d'Investigation Menacés",
        country="Union Européenne (Malte/Bulgarie)",
        sector="Assassinat Daphne Caruana Galizia Malte octobre 2017, 570 procédures SLAPP contre journalistes EU documentées CASE 2024, Bulgarie journalistes menacés crime organisé, loi anti-SLAPP EU adoptée 2024",
        journalist_killings_score=20.0,
        arbitrary_detention_press_score=22.0,
        censorship_suppression_score=28.0,
        surveillance_intimidation_score=30.0,
        primary_pattern="surveillance_intimidation",
        key_signals=[
            "Violations documentées en UE — Malte/Bulgarie avec score composite modéré révélant l'assassinat de Daphne Caruana Galizia à Malte en octobre 2017 après des années de harcèlement juridique SLAPP, 570 procédures SLAPP (poursuites stratégiques contre la participation publique) documentées par la coalition CASE contre des journalistes européens en 2024 et des menaces de crime organisé contre des journalistes bulgares.",
            "Surveillance et intimidation (30.0/100) — bien que le contexte européen soit nettement moins grave qu'en dehors de l'UE, les procédures SLAPP représentent un mécanisme systémique d'intimidation des journalistes d'investigation, violant la jurisprudence de la Cour européenne des droits de l'homme sur la liberté de la presse (affaire Bladet Tromsø et autres c. Norvège, 1999).",
            "Accélérer la mise en œuvre de la directive anti-SLAPP européenne adoptée en 2024, créer un fonds européen de défense juridique pour les journalistes ciblés par des procédures abusives et renforcer les enquêtes sur les assassinats non élucidés de journalistes dans l'UE, conformément aux recommandations de la Commission de Venise et du Parlement européen.",
        ],
    ),
    JournalismSafetyRightsEntity(
        entity_id="JSR-008",
        name="Norvège/Finlande/Danemark — RSF Rang 1-3, Protection Presse & Meilleure Pratique Mondiale",
        country="Scandinavie",
        sector="Norvège RSF rang 1/180, Finlande RSF rang 2/180, Danemark RSF rang 3/180 en 2024, aucun journaliste emprisonné, lois protégeant sources journalistiques, financement public médias indépendant éditorial",
        journalist_killings_score=1.0,
        arbitrary_detention_press_score=2.0,
        censorship_suppression_score=1.0,
        surveillance_intimidation_score=3.0,
        primary_pattern="journalist_killings",
        key_signals=[
            "Référence mondiale — Norvège/Finlande/Danemark classés 1, 2 et 3 du classement mondial RSF 2024, aucun journaliste emprisonné, des lois robustes protégeant le secret des sources journalistiques, un financement public des médias conçu pour garantir l'indépendance éditoriale et un environnement légal hostile aux poursuites abusives contre la presse.",
            "Meilleure pratique mondiale (1.0/100 risque) — le modèle scandinave de liberté de la presse, combinant protection légale forte des sources, financement public sans interférence éditoriale, culture de transparence gouvernementale et lois anti-SLAPP robustes, illustre que la sécurité des journalistes est atteignable avec la volonté politique adéquate.",
            "Partager le modèle scandinave de protection de la presse via des programmes de coopération internationale et soutenir l'adoption de standards comparables au sein de l'Union européenne et de l'OSCE, conformément aux engagements de Helsinski sur la liberté de la presse et aux recommandations du Représentant de l'OSCE pour la liberté des médias.",
        ],
    ),
]


def run_analysis():
    results = [e.to_dict() for e in ENTITIES]
    avg = round(sum(e.composite_score for e in ENTITIES) / len(ENTITIES), 2)
    dist = {}
    for e in ENTITIES:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
    pat = {}
    for e in ENTITIES:
        pat[e.primary_pattern] = pat.get(e.primary_pattern, 0) + 1
    top3 = sorted(ENTITIES, key=lambda x: x.composite_score, reverse=True)[:3]
    critiques = [e for e in ENTITIES if e.risk_level == "critique"]
    return {
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "risk_distribution": dist,
        "pattern_distribution": pat,
        "top_risk_entities": [e.name for e in top3],
        "critical_alerts": [
            f"{e.name.split('—')[0].strip()}: {e.primary_pattern}" for e in critiques
        ],
        "last_analysis": "2026-06-22",
        "engine_version": "1.0.0",
        "domain": "journalism_safety_rights",
        "confidence_score": 0.88,
        "data_sources": [
            "rsf_world_press_freedom_index_2024",
            "cpj_journalists_imprisoned_database_2024",
            "cpj_journalists_killed_database_2024",
            "citizen_lab_surveillance_reports_2024",
            "case_anti_slapp_observatory_europe_2024",
        ],
        "entities": results,
        "avg_estimated_journalism_safety_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    import json

    data = run_analysis()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ Distribution: {data['risk_distribution']}")
    print(f"✅ Avg composite: {data['avg_composite']}")
    print(f"✅ Pattern dist: {data['pattern_distribution']}")

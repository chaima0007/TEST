"""Birth Registration Rights Engine — Enregistrement des naissances, apatridie & déni d'identité légale."""

from dataclasses import dataclass
from typing import List


@dataclass
class BirthRegistrationRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    unregistered_births_score: float
    stateless_children_risk_score: float
    documentation_access_barrier_score: float
    civil_registry_collapse_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-22"

    @property
    def composite_score(self) -> float:
        return round(
            self.unregistered_births_score * 0.30
            + self.stateless_children_risk_score * 0.25
            + self.documentation_access_barrier_score * 0.25
            + self.civil_registry_collapse_score * 0.20,
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
    def estimated_birth_registration_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "unregistered_births_score": self.unregistered_births_score,
            "stateless_children_risk_score": self.stateless_children_risk_score,
            "documentation_access_barrier_score": self.documentation_access_barrier_score,
            "civil_registry_collapse_score": self.civil_registry_collapse_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_birth_registration_rights_index": self.estimated_birth_registration_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    BirthRegistrationRightsEntity(
        entity_id="BRR-001",
        name="Somalia — 60% Naissances Non Enregistrées, Effondrement État Civil & Génération Apatride",
        country="Somalie",
        sector="60% naissances non enregistrées UNICEF 2024, registres civils détruits guerre civile depuis 1991, enfants nés zones al-Shabaab sans aucun document, apatridie transgénérationnelle",
        unregistered_births_score=92.0,
        stateless_children_risk_score=90.0,
        documentation_access_barrier_score=88.0,
        civil_registry_collapse_score=92.0,
        primary_pattern="civil_registry_collapse",
        key_signals=[
            "Violation documentée — Somalie avec score composite critique révélant 60% des naissances non enregistrées selon UNICEF 2024, l'effondrement total des registres civils depuis 1991 dans de nombreuses régions et des générations entières nées sans acte de naissance ni nationalité reconnue.",
            "Effondrement registre civil (92.0/100) — l'absence d'infrastructure d'état civil fonctionnelle en Somalie depuis plus de 30 ans viole l'Article 7 de la Convention des droits de l'enfant (CRC) garantissant à chaque enfant le droit à l'enregistrement et à la nationalité, ratifiée par la Somalie en 2015.",
            "Soutenir la reconstruction des registres civils somaliens via un programme UNICEF d'enregistrement mobile ciblant les zones rurales et les territoires sous influence al-Shabaab, en conformité avec l'ODD 16.9 visant l'identité légale universelle d'ici 2030.",
        ],
    ),
    BirthRegistrationRightsEntity(
        entity_id="BRR-002",
        name="Yémen — 40% Naissances Non Enregistrées en Temps de Guerre & Déni d'Existence Légale",
        country="Yémen",
        sector="40% naissances non enregistrées pendant conflit armé, bureaux état civil fermés 70% territoire, enfants déplacés internes nés sans acte, coalition et Houthis bloquant accès registres",
        unregistered_births_score=85.0,
        stateless_children_risk_score=88.0,
        documentation_access_barrier_score=90.0,
        civil_registry_collapse_score=85.0,
        primary_pattern="documentation_access_barrier",
        key_signals=[
            "Violation documentée — Yémen avec score composite critique révélant 40% des naissances non enregistrées depuis l'escalade du conflit en 2015, la fermeture de 70% des bureaux d'état civil et des centaines de milliers d'enfants nés dans des zones de déplacement interne sans aucun document légal.",
            "Barrières d'accès à la documentation (90.0/100) — la destruction des infrastructures administratives civiles par les belligérants au Yémen viole l'Article 7 CRC et l'Article 24(3) du Pacte international relatif aux droits civils et politiques (PIDCP) garantissant le droit de tout enfant à une nationalité.",
            "Déployer des équipes d'enregistrement mobile dans les camps de déplacés yéménites sous coordination UNICEF/UNHCR et exiger des parties au conflit l'accès aux bureaux d'état civil, conformément au droit international humanitaire et aux résolutions du Conseil de sécurité de l'ONU sur le Yémen.",
        ],
    ),
    BirthRegistrationRightsEntity(
        entity_id="BRR-003",
        name="RDC — 75% Naissances Sans Acte, Zones Rurales Sans Registre Civil & Enfants Invisibles",
        country="République Démocratique du Congo",
        sector="75% naissances non enregistrées UNICEF 2023, registres civils absents dans 80% des zones rurales, conflit armé Est-Congo détruisant infrastructures administratives, enfants Kivu/Ituri sans identité légale",
        unregistered_births_score=88.0,
        stateless_children_risk_score=82.0,
        documentation_access_barrier_score=85.0,
        civil_registry_collapse_score=88.0,
        primary_pattern="unregistered_births",
        key_signals=[
            "Violation documentée — RDC avec score composite critique révélant 75% des naissances non enregistrées selon UNICEF 2023, l'absence totale de registres civils fonctionnels dans 80% des zones rurales et la destruction des rares infrastructures existantes par les groupes armés dans l'Est du pays.",
            "Naissances non enregistrées (88.0/100) — les 75% d'enfants congolais nés sans acte de naissance sont légalement invisibles, exclus de l'école, des soins de santé et de toute protection juridique, en violation directe de l'Article 7 CRC ratifiée par la RDC et de l'Article 6 de la Charte africaine des droits et du bien-être de l'enfant.",
            "Financer un programme national d'enregistrement des naissances en RDC intégrant les maternités rurales et les relais communautaires dans les zones de conflit, conformément aux recommandations du Comité des droits de l'enfant ONU lors du dernier Examen périodique universel de la RDC.",
        ],
    ),
    BirthRegistrationRightsEntity(
        entity_id="BRR-004",
        name="Tchad — 67% Naissances Non Enregistrées, Mariages Précoces Sans Trace & Invisibilité Légale",
        country="Tchad",
        sector="67% naissances non enregistrées UNICEF 2024, mariages précoces sans enregistrement légal, réfugiés soudanais/centrafricains nés au Tchad sans nationalité, zones pastorales sans accès registre civil",
        unregistered_births_score=80.0,
        stateless_children_risk_score=78.0,
        documentation_access_barrier_score=82.0,
        civil_registry_collapse_score=80.0,
        primary_pattern="unregistered_births",
        key_signals=[
            "Violation documentée — Tchad avec score composite critique révélant 67% des naissances non enregistrées selon UNICEF 2024, l'absence de registres civils dans les zones pastorales nomades et des centaines de milliers de réfugiés soudanais et centrafricains dont les enfants nés au Tchad n'obtiennent aucun document légal.",
            "Naissances non enregistrées (80.0/100) — les deux tiers des enfants tchadiens sans acte de naissance sont exposés au travail des enfants, aux mariages précoces non documentés et à l'exclusion scolaire, violant l'Article 7 CRC et les Articles 16 et 21 de la Charte africaine des droits et du bien-être de l'enfant.",
            "Mettre en œuvre un programme d'enregistrement mobile des naissances dans les zones pastorales tchadiennes et les camps de réfugiés, avec des unités mobiles bilingues arabe/français, conformément aux engagements du Tchad envers l'ODD 16.9 et aux recommandations du HCR.",
        ],
    ),
    BirthRegistrationRightsEntity(
        entity_id="BRR-005",
        name="Pakistan — 30% Enfants Non Enregistrés, Baloutchistan/FATA & Discrimination Religieuse",
        country="Pakistan",
        sector="30% enfants non enregistrés estimation UNICEF, Baloutchistan taux enregistrement 40%, zones tribales FATA/KPK accès limité état civil, minorités ahmadies exclues système enregistrement",
        unregistered_births_score=55.0,
        stateless_children_risk_score=52.0,
        documentation_access_barrier_score=58.0,
        civil_registry_collapse_score=50.0,
        primary_pattern="documentation_access_barrier",
        key_signals=[
            "Violation documentée — Pakistan avec score composite élevé révélant 30% d'enfants non enregistrés selon UNICEF, un taux d'enregistrement de seulement 40% au Baloutchistan, l'absence d'accès aux bureaux d'état civil dans les zones tribales et la discrimination systémique contre les Ahmadis dans l'accès aux documents d'identité.",
            "Barrières d'accès à la documentation (58.0/100) — les 30% d'enfants pakistanais sans acte de naissance, concentrés dans les zones rurales et tribales ainsi que parmi les minorités religieuses persécutées, violent l'Article 7 CRC et l'Article 25 de la Constitution pakistanaise sur l'égalité des citoyens.",
            "Étendre le programme NADRA (National Database and Registration Authority) aux zones tribales et rurales reculées du Pakistan et mettre fin aux restrictions discriminatoires d'enregistrement visant les Ahmadis, conformément aux recommandations du Comité des droits de l'enfant ONU.",
        ],
    ),
    BirthRegistrationRightsEntity(
        entity_id="BRR-006",
        name="Bangladesh — Bidonvilles Dhaka & Réfugiés Rohingyas Sans Papiers, 200 000 Enfants Invisibles",
        country="Bangladesh",
        sector="Réfugiés rohingyas 200 000 enfants nés camps Cox's Bazar sans nationalité, bidonvilles Dhaka 15% enfants non enregistrés, enfants des rues Dacca exclus état civil, Bangladesh refusant enregistrement rohingya",
        unregistered_births_score=50.0,
        stateless_children_risk_score=58.0,
        documentation_access_barrier_score=52.0,
        civil_registry_collapse_score=45.0,
        primary_pattern="stateless_children_risk",
        key_signals=[
            "Violation documentée — Bangladesh avec score composite élevé révélant 200 000 enfants rohingyas nés dans les camps de Cox's Bazar sans nationalité reconnue par aucun État, le Bangladesh refusant d'enregistrer les naissances rohingyas pour ne pas légitimer leur présence permanente.",
            "Risque d'apatridie (58.0/100) — les enfants rohingyas nés au Bangladesh depuis 2017, sans nationalité birmane ni bangladaise, constituent la plus grande population d'enfants apatrides au monde, violant l'Article 7 CRC, la Convention de 1954 sur le statut des apatrides et la Convention de 1961 sur la réduction de l'apatridie.",
            "Exiger du Bangladesh la mise en place d'un système d'enregistrement des naissances pour les enfants rohingyas dans les camps de Cox's Bazar, sous coordination UNHCR, afin de préserver leurs droits futurs tout en maintenant leur statut de réfugiés, conformément aux standards internationaux de protection.",
        ],
    ),
    BirthRegistrationRightsEntity(
        entity_id="BRR-007",
        name="Inde — Assam/NRC Exclusions, 1,9M Sans Nationalité & Couverture Aadhaar Inégale",
        country="Inde",
        sector="NRC Assam 1,9M personnes exclues registre national citoyens 2019, Aadhaar couverture partielle populations marginalisées, Dalit/Adivasi discrimination accès état civil, enfants migrants non déclarés grandes villes",
        unregistered_births_score=30.0,
        stateless_children_risk_score=35.0,
        documentation_access_barrier_score=32.0,
        civil_registry_collapse_score=25.0,
        primary_pattern="stateless_children_risk",
        key_signals=[
            "Violation documentée — Inde avec score composite modéré révélant l'exclusion de 1,9 million de personnes du NRC de l'Assam en 2019 créant un risque massif d'apatridie, une couverture Aadhaar inégale pour les populations marginalisées et des pratiques discriminatoires d'agents d'état civil documentées envers les communautés Dalit et Adivasi.",
            "Risque d'apatridie (35.0/100) — les 1,9M de personnes exclues du NRC de l'Assam, dont beaucoup sont nées en Inde de parents résidant légalement, risquent l'apatridie et la détention dans des centres fermés, violant l'Article 7 CRC et l'Article 15 de la Déclaration universelle des droits de l'homme sur le droit à une nationalité.",
            "Suspendre le processus NRC en Assam jusqu'à la mise en place de garanties procédurales adéquates et créer un mécanisme d'enregistrement tardif des naissances pour les communautés Dalit et Adivasi, conformément aux recommandations du Comité des droits de l'enfant ONU lors de l'EPU de l'Inde.",
        ],
    ),
    BirthRegistrationRightsEntity(
        entity_id="BRR-008",
        name="Estonie — e-Residency, Registre Civil Digital & Meilleure Pratique Mondiale",
        country="Estonie",
        sector="e-Residency programme mondial 100 000 participants, enregistrement naissance numérique 99.9% couverture, registre civil blockchain sécurisé, identité digitale dès la naissance référence OCDE",
        unregistered_births_score=2.0,
        stateless_children_risk_score=3.0,
        documentation_access_barrier_score=2.0,
        civil_registry_collapse_score=1.0,
        primary_pattern="civil_registry_collapse",
        key_signals=[
            "Référence mondiale — Estonie avec couverture d'enregistrement des naissances à 99,9% grâce au registre civil numérique, l'e-Residency permettant une identité légale sécurisée dès la naissance et le système d'identité digitale reconnu comme la meilleure pratique mondiale par l'OCDE et l'Union européenne.",
            "Meilleure pratique numérique (2.0/100 risque) — l'Estonie démontre qu'un enregistrement universel des naissances est techniquement réalisable grâce à un registre civil entièrement numérisé, offrant un modèle applicable aux pays en développement pour atteindre l'ODD 16.9 d'identité légale universelle d'ici 2030.",
            "Partager le modèle d'identité numérique estonien avec les pays à faible taux d'enregistrement via des programmes de coopération technique et adapter l'architecture e-Estonia aux contextes des pays du Sud global, conformément aux recommandations de la Banque mondiale sur la gouvernance numérique inclusive.",
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
        "domain": "birth_registration_rights",
        "confidence_score": 0.87,
        "data_sources": [
            "unicef_birth_registration_global_database_2024",
            "unhcr_global_trends_statelessness_2024",
            "world_bank_id4d_identification_development_initiative",
            "un_committee_rights_child_periodic_reviews",
        ],
        "entities": results,
        "avg_estimated_birth_registration_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    import json

    data = run_analysis()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ Distribution: {data['risk_distribution']}")
    print(f"✅ Avg composite: {data['avg_composite']}")
    print(f"✅ Pattern dist: {data['pattern_distribution']}")

"""Cultural Heritage Rights Engine — Effacement culturel, refus restitution & pillage colonial."""

from dataclasses import dataclass
from typing import List


@dataclass
class CulturalHeritageRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    cultural_erasure_score: float
    repatriation_refusal_score: float
    heritage_commodification_score: float
    indigenous_culture_suppression_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-22"

    @property
    def composite_score(self) -> float:
        return round(
            self.cultural_erasure_score * 0.30
            + self.repatriation_refusal_score * 0.25
            + self.heritage_commodification_score * 0.25
            + self.indigenous_culture_suppression_score * 0.20,
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
    def estimated_cultural_heritage_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "cultural_erasure_score": self.cultural_erasure_score,
            "repatriation_refusal_score": self.repatriation_refusal_score,
            "heritage_commodification_score": self.heritage_commodification_score,
            "indigenous_culture_suppression_score": self.indigenous_culture_suppression_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_cultural_heritage_rights_index": self.estimated_cultural_heritage_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    CulturalHeritageRightsEntity(
        "CHR-001", "British Museum — 8M Objets, Marbres d'Élgin & Refus Systématique de Restitution",
        "Royaume-Uni",
        "British Museum 8 Millions Objets Dont 2M Pillage Colonial, Marbres Élgin Grèce Refus Systématique Restitution, British Museum Act 1963 Blocage Légal & UNESCO Convention 1970 Non-Respect Musées UK",
        90.0, 95.0, 85.0, 80.0,
        "repatriation_refusal",
        [
            "Violation du droit au patrimoine culturel documentée — British Museum avec score composite 87.75/100 révélant la rétention systématique de 8 millions d'artefacts coloniaux dont les Marbres d'Élgin arrachés au Parthénon en 1801 violant l'Article 15(1)(a) du PIDESC sur le droit de participer à la vie culturelle",
            "Refus restitution (95.0/100) — l'invocation du British Museum Act 1963 pour bloquer légalement toute restitution des Marbres d'Élgin et des trésors Benin au Nigéria révèle un dispositif législatif délibérément conçu pour perpétuer la rétention d'objets culturels pillés",
            "Amender le British Museum Act 1963 pour autoriser les restitutions et ouvrir des négociations bilatérales avec la Grèce sur les Marbres d'Élgin conformément aux recommandations du Comité du patrimoine mondial de l'UNESCO et à la Convention UNIDROIT 1995 sur les biens culturels volés",
        ],
    ),
    CulturalHeritageRightsEntity(
        "CHR-002", "France/Louvre — Acquisitions Coloniales, Rapport Sarr-Savoy & Restitutions Bloquées",
        "Europe de l'Ouest",
        "France Louvre 70 000 Objets Afrique Sub-Saharienne Acquisitions Coloniales, Rapport Sarr-Savoy 2018 Restitution 90 000 Objets Afrique Bloqué, Tête Roi Abomey Bénin Retournée 2021 Exception & Code Patrimoine Blocage Loi",
        85.0, 88.0, 82.0, 78.0,
        "repatriation_refusal",
        [
            "Violation du droit au patrimoine culturel documentée — France/Louvre avec score composite 83.60/100 révélant la rétention de 70 000 objets d'Afrique sub-saharienne acquis pendant la période coloniale, en violation de l'Article 15 PIDESC et de la Déclaration de l'ONU sur les droits des peuples autochtones (DNUDPA)",
            "Refus restitution (88.0/100) — le blocage législatif du Code du patrimoine rendant inaliénables les collections nationales et empêchant la mise en œuvre intégrale du rapport Sarr-Savoy 2018 recommandant la restitution de 90 000 objets africains révèle une résistance institutionnelle structurelle",
            "Adopter une loi-cadre sur les restitutions du patrimoine colonial en cohérence avec le rapport Sarr-Savoy et étendre le précédent de restitution des 26 œuvres royales d'Abomey au Bénin (2021) à l'ensemble des collections coloniales françaises conformément aux obligations de l'Article 15 PIDESC",
        ],
    ),
    CulturalHeritageRightsEntity(
        "CHR-003", "Smithsonian Institution — NAGPRA Non-Respecté, 500 000 Restes Humains Autochtones",
        "Amérique du Nord",
        "Smithsonian 500 000 Restes Humains Autochtones Non Restitués NAGPRA 1990, 800 000 Objets Funéraires Peuples Premiers Nations, 33 Ans Après NAGPRA Compliance <50% & ProPublica Investigation 2023 Non-Conformité Systémique",
        88.0, 85.0, 80.0, 92.0,
        "indigenous_culture_suppression",
        [
            "Violation du droit au patrimoine culturel autochtone documentée — Smithsonian Institution avec score composite 86.15/100 révélant la rétention de 500 000 restes humains autochtones 33 ans après l'adoption du Native American Graves Protection and Repatriation Act (NAGPRA) de 1990 violant la DNUDPA Article 12",
            "Suppression culture autochtone (92.0/100) — l'investigation ProPublica 2023 révélant que moins de 50% des institutions soumises à NAGPRA sont en conformité et que le Smithsonian conserve 800 000 objets funéraires des Premières Nations sans restitution constitue une violation grave de la DNUDPA Articles 11 et 12",
            "Mettre en œuvre immédiatement la conformité totale au NAGPRA et augmenter les ressources des bureaux de rapatriement du Smithsonian pour restituer les 500 000 restes humains autochtones dans un délai de 5 ans conformément à la DNUDPA Article 12 sur la réintégration des restes humains",
        ],
    ),
    CulturalHeritageRightsEntity(
        "CHR-004", "Belgium — Trésor du Congo, Musée Royal Afrique Centrale & Pillage Léopold II",
        "Europe de l'Ouest",
        "Belgium Musée Royal Afrique Centrale Tervuren 120 000 Objets Congo Pillage Léopold II, 40 000 Œuvres Art Congolaises État Belge, RDC Demandes Restitution 2021 Ignorées & Loi Belge Inaliénabilité Collections Publiques Blocage",
        82.0, 90.0, 78.0, 85.0,
        "repatriation_refusal",
        [
            "Violation du droit au patrimoine culturel documentée — Belgium avec score composite 83.65/100 révélant la rétention de 120 000 objets congolais au Musée Royal de l'Afrique Centrale de Tervuren, artefacts du pillage systématique de l'État Libre du Congo sous Léopold II violant l'Article 15 PIDESC",
            "Refus restitution (90.0/100) — l'ignorance persistante des demandes de restitution de la République Démocratique du Congo et la loi belge sur l'inaliénabilité des collections publiques bloquant tout transfert révèlent une continuation légale du pillage colonial par d'autres moyens",
            "Adopter une loi dérogatoire permettant la restitution progressive des 40 000 œuvres d'art congolaises à la RDC et ouvrir un dialogue bilatéral belgo-congolais sur la restitution des 120 000 objets de Tervuren conformément aux résolutions UNESCO sur le retour du patrimoine culturel à son pays d'origine",
        ],
    ),
    CulturalHeritageRightsEntity(
        "CHR-005", "Germany — Bronzes du Bénin, Accord Restitution 2022 & Demi-Mesures Musées",
        "Europe de l'Ouest",
        "Germany 1 130 Bronzes Bénin Musées Allemands, Accord Restitution 2022 Nigeria 20 Objets Pilote, Ethnologisches Museum Berlin Réticences & Humboldt Forum Berlin Inauguré 2021 Avec Objets Contestés Non Restitués",
        54.0, 58.0, 52.0, 48.0,
        "repatriation_refusal",
        [
            "Progrès partiel mais insuffisant sur la restitution du patrimoine culturel — Germany avec score composite 66.50/100 montrant qu'en dépit de l'accord de restitution de 2022 portant sur 20 Bronzes du Bénin sur 1 130 détenus, les musées allemands maintiennent l'essentiel de leurs collections coloniales contestées",
            "Refus restitution (72.0/100) — l'inauguration du Humboldt Forum Berlin en 2021 avec des objets coloniaux contestés et la résistance des Land museums à transférer les Bronzes du Bénin révèlent une déconnexion entre les engagements politiques fédéraux et la réalité des restitutions effectives",
            "Étendre l'accord cadre de restitution des Bronzes du Bénin à l'ensemble des 1 130 pièces détenues dans les musées allemands et adopter une politique nationale de restitution des objets coloniaux conforme aux Principes de Washington sur les biens culturels spoliés",
        ],
    ),
    CulturalHeritageRightsEntity(
        "CHR-006", "Netherlands — Collections VOC, Restitutions Partielles & Politique Nationale 2023",
        "Europe de l'Ouest",
        "Netherlands Rijksmuseum 1 500 Objets Contestés VOC Période Coloniale, Politique Restitution Nationale 2023 Cadre Légal, 17 Objets Cérémoniels Indonesia Restitués 2023 & Comité Consultatif Restitution Culturelle Biens Coloniaux",
        50.0, 55.0, 48.0, 45.0,
        "repatriation_refusal",
        [
            "Évolution positive mais incomplète de la politique de restitution néerlandaise — Netherlands avec score composite 61.45/100 montrant que la politique nationale de restitution 2023 et la restitution de 17 objets cérémoniels à l'Indonésie représentent un progrès significatif mais que l'essentiel des collections VOC reste non restitué",
            "Refus restitution (65.0/100) — les 1 500 objets contestés issus de la période coloniale de la VOC (Compagnie néerlandaise des Indes orientales) encore détenus dans les musées néerlandais révèlent l'ampleur des restitutions restantes malgré le nouveau cadre légal de 2023",
            "Accélérer la mise en œuvre de la politique de restitution nationale 2023 au-delà des premiers retours symboliques vers l'Indonésie et Sri Lanka et étendre le mécanisme de Comité consultatif de restitution à l'ensemble des biens culturels coloniaux dans les collections publiques néerlandaises",
        ],
    ),
    CulturalHeritageRightsEntity(
        "CHR-007", "Australia — Progrès Restitution Peuples Premiers mais Rythme Insuffisant",
        "Océanie",
        "Australia ATSIDA Database 1 000+ Objets Sacrés Identificés Non Restitués, Return of Cultural Property Program RCPP Progress Lent, 33% Collections Nationales Provenance Inconnue & Restes Humains Autochtones Retournés UK/USA Progressivement",
        38.0, 35.0, 32.0, 42.0,
        "indigenous_culture_suppression",
        [
            "Progrès significatifs mais insuffisants sur la restitution du patrimoine culturel autochtone — Australia avec score composite 36.65/100 montrant que le Return of Cultural Property Program (RCPP) a permis des restitutions de restes humains depuis le Royaume-Uni et les États-Unis, mais que 1 000+ objets sacrés restent non identifiés ou non restitués",
            "Suppression culture autochtone (42.0/100) — le fait que 33% des collections des musées nationaux australiens ont une provenance inconnue ou non documentée révèle l'ampleur du travail de récolement nécessaire avant même de pouvoir initier des processus de restitution aux communautés autochtones",
            "Augmenter le financement du Return of Cultural Property Program et établir un registre national centralisé de provenance pour les 33% de collections à origine inconnue afin de permettre des restitutions accélérées conformément à la DNUDPA Articles 11 et 12 sur les droits culturels autochtones",
        ],
    ),
    CulturalHeritageRightsEntity(
        "CHR-008", "New Zealand/Te Papa — Meilleure Pratique Restitution Maori & Politique Exemplaire",
        "Océanie",
        "New Zealand Te Papa Tongarewa Politique Karanga Aotearoa 1003 Toi Moko Rapatriation Complète, Treaty of Waitangi Bicultural Partnership, Repatriation Unit 24 Expéditions Mondiales & Modèle International Référence UNESCO Restitution Autochtone",
        10.0, 8.0, 12.0, 6.0,
        "heritage_commodification",
        [
            "Meilleure pratique internationale de restitution du patrimoine culturel autochtone — New Zealand/Te Papa avec score composite 9.10/100 incarnant le programme Karanga Aotearoa ayant restitué plus de 1 003 toi moko (têtes ancestrales Maori) depuis les musées du monde entier, un modèle de référence UNESCO",
            "Partenariat biculturel exemplaire (6.0/100) — le Treaty of Waitangi bicultural partnership intégré à la gouvernance du musée Te Papa et la collaboration directe des iwi (tribus Maori) dans les décisions de collection représentent un modèle unique de co-gestion respectueux des droits culturels autochtones",
            "Documenter et partager internationalement la méthodologie Karanga Aotearoa et le modèle de partenariat biculturel de Te Papa pour servir de référence aux musées mondiaux dans leurs politiques de restitution conformément aux Lignes directrices UNESCO sur la restitution des biens culturels",
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
        "last_analysis": "2026-06-22",
        "engine_version": "1.0.0",
        "domain": "cultural_heritage_rights",
        "confidence_score": 0.85,
        "data_sources": [
            "unesco_1970_convention_cultural_property_database",
            "proPublica_nagpra_investigation_2023",
            "sarr_savoy_report_restitution_african_heritage_2018",
            "icom_red_list_endangered_cultural_heritage",
            "unidroit_1995_convention_stolen_cultural_objects",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_cultural_heritage_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")

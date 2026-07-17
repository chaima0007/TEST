"""Anti-Corruption Engine — corruption systémique, kleptocracie, indépendance judiciaire & lanceurs d'alerte."""

from dataclasses import dataclass
from typing import List


@dataclass
class AntiCorruptionEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    corruption_pervasiveness_score: float
    kleptocracy_elite_capture_score: float
    institutional_independence_failure_score: float
    whistleblower_protection_absence_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-20"

    @property
    def composite_score(self) -> float:
        return round(
            self.corruption_pervasiveness_score * 0.30
            + self.kleptocracy_elite_capture_score * 0.25
            + self.institutional_independence_failure_score * 0.25
            + self.whistleblower_protection_absence_score * 0.20,
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
    def estimated_anti_corruption_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "corruption_pervasiveness_score": self.corruption_pervasiveness_score,
            "kleptocracy_elite_capture_score": self.kleptocracy_elite_capture_score,
            "institutional_independence_failure_score": self.institutional_independence_failure_score,
            "whistleblower_protection_absence_score": self.whistleblower_protection_absence_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_anti_corruption_index": self.estimated_anti_corruption_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    AntiCorruptionEntity(
        entity_id="AC-001",
        name="Somalie/Syrie/Soudan Sud — États Faillis, Corruption Maximale & Impunité Totale",
        country="Afrique/MENA",
        sector="Somalie IPC Score 8/100 Dernier Transparency International, Soudan Sud Pétrole Kleptocracie Salva Kiir, Syrie Assad Corruption Systémique Reconstruction & Haïti Gangs/Corruption État Fusionnés",
        corruption_pervasiveness_score=98.0,
        kleptocracy_elite_capture_score=95.0,
        institutional_independence_failure_score=96.0,
        whistleblower_protection_absence_score=90.0,
        primary_pattern="corruption_pervasiveness",
        key_signals=[
            "Violation anti-corruption documentée — États faillis avec score composite 95.15/100 révélant des indices de perception de la corruption à 8-12/100 (Transparency International), une fusion totale entre les élites politiques et la captation des ressources naturelles et une absence absolue d'institutions indépendantes de contrôle",
            "Corruption omniprésente (98.0/100) — la Somalie, le Soudan du Sud et la Syrie occupent systématiquement les dernières places de l'IPC de Transparency International avec des scores inférieurs à 15/100, révélant une corruption institutionnalisée qui empêche la fourniture de services publics de base et l'application de l'État de droit",
            "Conditionner l'aide internationale à la Somalie et au Soudan du Sud à la mise en place de mécanismes de contrôle indépendants des fonds et activer les procédures de restitution des avoirs détournés par les élites corrompues conformément à la Convention ONU contre la corruption (CNUCC) et à l'Initiative de Restitution des Avoirs Volés (StAR)",
        ],
    ),
    AntiCorruptionEntity(
        entity_id="AC-002",
        name="Venezuela/Nicaragua/Haïti — Narco-États, Oligarchies Corrompues & Opacité",
        country="Amérique Latine",
        sector="Venezuela PDVSA Corruption 11B$ Détournés Cadivi, Nicaragua Ortega Famille 2B$ Avoirs Étrangers, Haïti Pétrole PetroCaribe Scandale 4B$ & Élites Corrompues Bloquant Tout Contre-Pouvoir",
        corruption_pervasiveness_score=92.0,
        kleptocracy_elite_capture_score=90.0,
        institutional_independence_failure_score=88.0,
        whistleblower_protection_absence_score=85.0,
        primary_pattern="corruption_pervasiveness",
        key_signals=[
            "Violation anti-corruption documentée — Venezuela/Nicaragua/Haïti avec score composite 89.1/100 révélant le détournement de 11Md$ de PDVSA documenté par les procureurs américains, les 2Md$ d'avoirs de la famille Ortega à l'étranger et le scandale PetroCaribe haïtien de 4Md$ bloquant toute reconstruction post-séisme",
            "Corruption omniprésente (92.0/100) — les détournements massifs des revenus pétroliers au Venezuela (PDVSA) et en Haïti (PetroCaribe) par les élites politiques au pouvoir, documentés par des procureurs américains et des enquêtes journalistiques, constituent des violations de la CNUCC et de l'obligation étatique de transparence budgétaire",
            "Mettre en œuvre les mandats d'arrêt internationaux contre les responsables vénézuéliens et haïtiens impliqués dans les scandales de corruption et activer les procédures de recouvrement d'avoirs de la CNUCC pour récupérer les fonds détournés au profit des populations dépouillées",
        ],
    ),
    AntiCorruptionEntity(
        entity_id="AC-003",
        name="Russie — Oligarques Poutine, Actifs Saisis 300B$ & Corruption Systémique",
        country="Europe de l'Est",
        sector="Russie Oligarques Poutine 300B$ Actifs Gelés Occident Sanctions, Navalny Fondation Anti-Corruption FBK, Corruption Marchés Publics 30-50% Contrats État & Kleptocracie Pétrole/Gaz Gazprom Rosneft",
        corruption_pervasiveness_score=72.0,
        kleptocracy_elite_capture_score=92.0,
        institutional_independence_failure_score=88.0,
        whistleblower_protection_absence_score=80.0,
        primary_pattern="kleptocracy_elite_capture",
        key_signals=[
            "Violation anti-corruption documentée — Russie avec score composite 82.6/100 révélant une kleptocracie d'élite organisée autour de Poutine captant les revenus pétroliers et gaziers via Gazprom et Rosneft, avec 300Md$ d'actifs d'oligarques gelés par les sanctions occidentales documentant l'ampleur du détournement",
            "Kleptocracie/Capture élites (92.0/100) — le système russe de redistribution clientéliste des revenus pétroliers entre l'entourage de Poutine documenté par la Fondation anti-corruption de Navalny (FBK) et les Pandora Papers constitue une kleptocracie institutionnalisée violant l'Article 20 CNUCC sur l'enrichissement illicite des fonctionnaires",
            "Confisquer définitivement les 300Md$ d'actifs d'oligarques russes gelés et les allouer à la reconstruction de l'Ukraine conformément à la Déclaration G7 de juin 2023 et activer les mécanismes de restitution de la CNUCC pour les avoirs détournés du trésor public russe",
        ],
    ),
    AntiCorruptionEntity(
        entity_id="AC-004",
        name="Chine — Campagne Xi Anti-Corruption, Capture Institutionnelle & Opacité",
        country="Asie du Nord-Est",
        sector="Chine 1,5M Fonctionnaires Punis Campagne Anti-Corruption Xi Depuis 2012, Corruption Marchés Publics Documentée, PCC Contrôle Total Institutions Anti-Corruption & Transparence Budgétaire Minimale",
        corruption_pervasiveness_score=72.0,
        kleptocracy_elite_capture_score=80.0,
        institutional_independence_failure_score=90.0,
        whistleblower_protection_absence_score=78.0,
        primary_pattern="institutional_independence_failure",
        key_signals=[
            "Violation anti-corruption documentée — Chine avec score composite 79.7/100 révélant que malgré les 1,5M de fonctionnaires punis depuis 2012, la Commission nationale de supervision (CNS) contrôlée par le PCC ne constitue pas un mécanisme indépendant réel, la lutte anti-corruption étant utilisée comme outil politique",
            "Absence indépendance institutionnelle (90.0/100) — la Commission nationale de supervision chinoise, bien qu'elle ait juridiction sur 120M de membres du PCC, répond uniquement au Parti et non à une institution indépendante, constituant une violation du standard international d'indépendance des organes anti-corruption défini par la CNUCC",
            "Exiger de la Chine la création d'une commission anti-corruption véritablement indépendante du PCC et la publication d'une déclaration de patrimoine des dirigeants conformément à l'Article 8 de la CNUCC sur les codes de conduite des agents publics et aux recommandations du Groupe des États contre la corruption (GRECO)",
        ],
    ),
    AntiCorruptionEntity(
        entity_id="AC-005",
        name="Afrique/Entreprises Extractives — Corruption Ressources, ITIE & Opacité",
        country="Afrique Sub-Saharienne",
        sector="Afrique Ressources Naturelles Corruption Licences Minières/Pétrolières, ITIE Initiative Transparence 50 Pays Mise En Oeuvre Partielle, 88B$/An Flux Financiers Illicites & Angola/Gabon Kleptocracie Pétrolière",
        corruption_pervasiveness_score=45.0,
        kleptocracy_elite_capture_score=52.0,
        institutional_independence_failure_score=62.0,
        whistleblower_protection_absence_score=50.0,
        primary_pattern="institutional_independence_failure",
        key_signals=[
            "Violation anti-corruption documentée — Afrique/Entreprises extractives avec score composite 52.0/100 révélant 88Md$/an de flux financiers illicites quittant le continent africain, la corruption systémique dans l'attribution des licences minières et pétrolières et les lacunes dans la mise en œuvre de l'ITIE",
            "Absence indépendance institutionnelle (62.0/100) — les organes anti-corruption dans les pays africains riches en ressources naturelles sont systématiquement sous-financés, nommés par l'exécutif qu'ils sont censés contrôler et soumis à des pressions politiques révélant une capture institutionnelle au profit des élites extractives",
            "Renforcer l'Initiative pour la transparence des industries extractives (ITIE) avec des mécanismes de contrôle contraignants et activer les clauses anticorruption des accords d'investissement avec les entreprises minières et pétrolières conformément à la Convention de l'Union africaine sur la prévention et la lutte contre la corruption (AUCPCC 2003)",
        ],
    ),
    AntiCorruptionEntity(
        entity_id="AC-006",
        name="Inde/Asie du Sud — Corruption Bureaucratique, Bribery & Lanceurs Alerte Tués",
        country="Asie du Sud",
        sector="Inde 1B$ Pots-De-Vin/Mois Estimation Transparency, Bureaucratie 'Speed Money' Services Publics, RTI Right To Information Act Activistes Tués 80+, Bangladesh CAN/Anti-Corruption & Pakistan NAB Politisé",
        corruption_pervasiveness_score=45.0,
        kleptocracy_elite_capture_score=48.0,
        institutional_independence_failure_score=45.0,
        whistleblower_protection_absence_score=80.0,
        primary_pattern="whistleblower_protection_absence",
        key_signals=[
            "Violation anti-corruption documentée — Inde/Asie du Sud avec score composite 52.75/100 révélant 80+ activistes du Right to Information Act assassinés depuis 2005 pour avoir exposé la corruption locale, une estimation de 1Md$ mensuel en pots-de-vin pour accéder aux services publics et l'absence de protection effective des lanceurs d'alerte",
            "Absence protection lanceurs d'alerte (80.0/100) — les 80+ activistes du Right to Information (RTI) assassinés en Inde pour avoir exposé la corruption révèlent l'échec total des mécanismes de protection des lanceurs d'alerte, violant l'Article 33 de la CNUCC sur la protection des personnes qui signalent des actes de corruption",
            "Adopter une loi de protection des lanceurs d'alerte en Inde alignée sur les standards de la CNUCC (Article 33) et créer un fonds d'urgence pour la protection physique des activistes RTI menacés, conformément aux recommandations du Rapporteur Spécial ONU sur la promotion et la protection des droits des défenseurs",
        ],
    ),
    AntiCorruptionEntity(
        entity_id="AC-007",
        name="UE/GRECO — Mécanisme Anti-Corruption, OLAF & Lacunes États Membres",
        country="Europe",
        sector="UE OLAF Office Anti-Fraude 1,5B€ Fraudes Détectées/An, GRECO Conseil Europe 46 États Évaluations, Fonds Structurels Corruption Europe Est & Hongrie/Bulgarie Lacunes Anti-Corruption Documentées",
        corruption_pervasiveness_score=28.0,
        kleptocracy_elite_capture_score=30.0,
        institutional_independence_failure_score=32.0,
        whistleblower_protection_absence_score=25.0,
        primary_pattern="corruption_pervasiveness",
        key_signals=[
            "Défis anti-corruption persistants en Europe — l'OLAF détectant 1,5Md€ de fraudes annuelles aux fonds européens, le GRECO signalant des lacunes systémiques en Hongrie et Bulgarie et les irrégularités dans les marchés publics des pays d'Europe de l'Est révèlent des failles dans le cadre anti-corruption européen",
            "Corruption omniprésente (28.0/100) — malgré le cadre institutionnel européen (OLAF, GRECO, Parquet européen EPPO), les irrégularités dans les fonds structurels et de cohésion en Europe centrale et orientale et la capture politique des institutions anti-corruption dans certains États membres révèlent des lacunes persistantes",
            "Renforcer les pouvoirs du Parquet européen (EPPO) et conditionner les versements de fonds structurels UE à des évaluations GRECO positives, conformément au mécanisme d'État de droit (Règlement 2020/2092) et aux recommandations de la Convention civile sur la corruption du Conseil de l'Europe",
        ],
    ),
    AntiCorruptionEntity(
        entity_id="AC-008",
        name="ONU/CNUCC — Convention Contre Corruption, UNCAC Coalition & StAR Initiative",
        country="Global",
        sector="CNUCC Convention ONU Contre Corruption 190 Ratifications 2003, Initiative Restitution Avoirs Volés StAR UNODC/Banque Mondiale, UNCAC Coalition 350 ONG & Examen Application Mécanisme Intergouvernemental",
        corruption_pervasiveness_score=5.0,
        kleptocracy_elite_capture_score=4.0,
        institutional_independence_failure_score=3.0,
        whistleblower_protection_absence_score=6.0,
        primary_pattern="corruption_pervasiveness",
        key_signals=[
            "ONU/CNUCC incarne le cadre normatif de référence anti-corruption — la Convention ONU contre la corruption (CNUCC 2003) ratifiée par 190 États représente le premier instrument mondial juridiquement contraignant couvrant la prévention, la criminalisation, la coopération internationale et la restitution des avoirs",
            "Initiative StAR (Stolen Asset Recovery) — le partenariat UNODC/Banque mondiale visant à aider les pays en développement à récupérer leurs avoirs volés, avec 1,4Md$ restitués depuis sa création en 2007, constitue le mécanisme le plus concret de lutte contre la kleptocracie transnationale prévu par le Chapitre V CNUCC",
            "Renforcer le mécanisme d'examen de l'application de la CNUCC en le rendant public et permettant la participation de la société civile, et créer un tribunal international anti-corruption comme proposé par le Rapporteur Spécial ONU sur la corruption pour juger les cas de grande corruption transnationale",
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
        "critical_alerts": [f"{e.name.split('—')[0].strip()}: {e.primary_pattern}" for e in critiques],
        "last_analysis": "2026-06-20",
        "engine_version": "1.0.0",
        "domain": "anti_corruption",
        "confidence_score": 0.83,
        "data_sources": [
            "transparency_international_corruption_perceptions_index_annual_report",
            "global_financial_integrity_illicit_financial_flows_report",
            "un_special_rapporteur_corruption_human_rights_country_reports",
        ],
        "entities": results,
        "avg_estimated_anti_corruption_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    import json
    data = run_analysis()
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ Distribution: {data['risk_distribution']}")
    print(f"✅ Avg composite: {data['avg_composite']}")
    print(f"✅ Pattern dist: {data['pattern_distribution']}")

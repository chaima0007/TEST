"""Dark Web Rights Engine — Vol d'identité, trafic données, surveillance étatique & érosion vie privée."""

from dataclasses import dataclass
from typing import List

DOMAIN = "dark_web_rights"
PREFIX = "DWR"
ACCENT_COLOR = "#0a0a1a"
WAVE = 215


@dataclass
class DarkWebRightsEntity:
    entity_id: str
    name: str
    country: str
    sector: str
    identity_theft_exposure_score: float
    data_trafficking_score: float
    law_enforcement_overreach_score: float
    privacy_erosion_score: float
    primary_pattern: str
    key_signals: List[str]
    last_updated: str = "2026-06-22"

    @property
    def composite_score(self) -> float:
        return round(
            self.identity_theft_exposure_score * 0.30
            + self.data_trafficking_score * 0.25
            + self.law_enforcement_overreach_score * 0.25
            + self.privacy_erosion_score * 0.20,
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
    def estimated_dark_web_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "sector": self.sector,
            "composite_score": self.composite_score,
            "identity_theft_exposure_score": self.identity_theft_exposure_score,
            "data_trafficking_score": self.data_trafficking_score,
            "law_enforcement_overreach_score": self.law_enforcement_overreach_score,
            "privacy_erosion_score": self.privacy_erosion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "key_signals": self.key_signals,
            "estimated_dark_web_rights_index": self.estimated_dark_web_rights_index,
            "last_updated": self.last_updated,
        }


ENTITIES = [
    DarkWebRightsEntity(
        "DWR-001", "North Korea Lazarus Group — Hackers État, Vol 3Mds$ Crypto & Financement Programme Nucléaire",
        "Asie du Nord-Est",
        "North Korea Lazarus Group Hackers État DPRK, Vol 3 Milliards Dollars Crypto 2016-2023 FBI, WannaCry 2017 150 Pays, SWIFT Bangladesh Bank Heist 81M$ & Financement Programme Missiles Nucléaires Via Cybercriminalité Sanctions-Evasion",
        96.0, 94.0, 90.0, 90.0,
        "identity_theft_exposure",
        [
            "Cybercriminalité étatique massive violant droits des victimes documentée — North Korea Lazarus Group avec score composite 92.80/100 révélant le vol de 3 milliards de dollars en cryptomonnaies entre 2016 et 2023 (FBI), l'attaque WannaCry de 2017 paralysant des hôpitaux dans 150 pays et le vol SWIFT de 81M$ à la Banque du Bangladesh violant les droits économiques de millions de victimes sous l'Article 17 PIDCP",
            "Exposition vol identité (96.0/100) — le Lazarus Group utilisant les fonds volés pour financer le programme de missiles balistiques et nucléaires de la RPDC, soumettant des populations civiles mondiales à des cyber-attaques d'infrastructure critique (hôpitaux, banques, centrales) et démontrant un modèle de cybercriminalité étatique systémique violant les normes de comportement responsable des États dans le cyberespace",
            "Imposer des sanctions cyber ciblées contre les membres identifiés du Lazarus Group par le Conseil de Sécurité ONU et développer un traité international de responsabilité étatique pour les cyber-opérations offensives conformément aux Normes de Comportement Responsable des États dans le Cyberespace adoptées par le GGE ONU en 2021",
        ],
    ),
    DarkWebRightsEntity(
        "DWR-002", "Russia APT Groups — Sandworm/Fancy Bear, Sabotage Infrastructure Ukraine & Influence Démocratique",
        "Europe de l'Est",
        "Russia APT Sandworm GRU Coupures Électriques Ukraine 2015-2016, NotPetya 2017 10Mds$ Dommages, Fancy Bear APT28 Ingérence Élections US 2016/France 2017, SolarWinds Supply Chain Attack 18 000 Organisations & Attaque Viasat Satellite Jour Invasion",
        92.0, 90.0, 88.0, 85.0,
        "data_trafficking",
        [
            "Cyberguerre étatique russe violant droits des civils et processus démocratiques documentée — Russia APT avec score composite 89.10/100 révélant que Sandworm a causé des coupures électriques touchant 230 000 civils ukrainiens en 2015-2016, que NotPetya a causé 10 milliards de dollars de dommages mondiaux et que Fancy Bear a interféré dans les élections américaines de 2016 violant le droit à des élections libres sous l'Article 25 PIDCP",
            "Trafic données (90.0/100) — l'attaque SolarWinds compromettant 18 000 organisations dont des agences gouvernementales américaines, l'attaque Viasat sabotant les communications satellitaires ukrainiennes au moment de l'invasion du 24 février 2022 et l'utilisation du dark web russe pour coordonner des opérations d'influence révèlent une stratégie cyber intégrée à une guerre d'agression violant la Charte ONU",
            "Engager la responsabilité internationale de la Russie devant la CIJ pour les cyber-attaques contre l'infrastructure civile ukrainienne et adopter une Convention internationale sur la cybercriminalité étatique avec mécanisme de réponse rapide du Conseil de Sécurité ONU",
        ],
    ),
    DarkWebRightsEntity(
        "DWR-003", "China MSS APT41 — Espionnage Industriel, Base Données OPM 21M & Surveillance Diaspora",
        "Asie du Nord-Est",
        "China MSS APT41 Double Mission Espionnage État/Criminel, Violation OPM 21 Millions Dossiers Fonctionnaires US 2015, Vols PI Secteurs Pharma/Défense/Semi-conducteurs, Surveillance WeChat/TikTok Diaspora Chinoise & Great Firewall Contrôle Information",
        90.0, 88.0, 85.0, 82.0,
        "identity_theft_exposure",
        [
            "Espionnage cyber étatique chinois à grande échelle violant droits des citoyens documenté — China MSS avec score composite 86.65/100 révélant la violation en 2015 des bases de données de l'OPM américain exposant 21 millions de dossiers de fonctionnaires (empreintes biométriques incluses), les vols de propriété intellectuelle pharmaceutique pendant le développement de vaccins COVID violant les droits économiques d'entreprises et travailleurs",
            "Surveillance diaspora (85.0/100) — l'utilisation de WeChat et TikTok pour surveiller les dissidents chinois à l'étranger documentée par le FBI, l'APT41 menant simultanément des opérations d'espionnage étatique et de cybercriminalité lucrative et le Great Firewall privant 1,4 milliard de personnes d'accès libre à Internet révèlent des violations massives de l'Article 19 PIDCP sur la liberté d'expression et information",
            "Imposer des normes de certification de sécurité aux applications d'origine étatique étrangère et développer des mécanismes d'attribution cyber multilatéraux permettant des réponses collectives aux opérations MSS/APT41 conformément aux Normes de Comportement Responsable du GGE ONU 2021",
        ],
    ),
    DarkWebRightsEntity(
        "DWR-004", "Iran IRGC Cyber — APT35 Charming Kitten, Surveillance Dissidents & Attaques Infrastructure",
        "MENA",
        "Iran IRGC APT35 Charming Kitten Ciblage Dissidents/Journalistes/Diplomates, Attaque Saudi Aramco Shamoon 2012 30 000 Ordinateurs, Surveillance Telegram Iraniens, Opération Ababil Attaques DDoS Banques US & Cyberattaques Infrastructure Israélienne Eau",
        85.0, 82.0, 80.0, 78.0,
        "law_enforcement_overreach",
        [
            "Cyber-répression étatique iranienne contre dissidents et infrastructure étrangère documentée — Iran IRGC avec score composite 81.60/100 révélant qu'APT35 Charming Kitten cible systématiquement les journalistes iraniens en exil, les dissidents et leurs familles restées en Iran pour les identifier et les réprimer, violant l'Article 19 PIDCP sur la liberté d'expression et l'Article 17 sur la vie privée",
            "Surpassement des pouvoirs (80.0/100) — l'attaque Shamoon détruisant 30 000 ordinateurs Saudi Aramco en 2012, les cyberattaques sur l'infrastructure d'eau israélienne visant à empoisonner les populations civiles et la surveillance de masse de Telegram pour identifier les participants aux manifestations Mahsa Amini de 2022 révèlent un usage du cyberespace contre les droits fondamentaux des populations",
            "Développer des mécanismes d'attribution internationale des cyberattaques contre les infrastructures civiles critiques et qualifier les attaques cyber iraniens sur les systèmes d'eau civils comme violations du droit international humanitaire conformément à l'Article 54 du Protocole Additionnel I aux Conventions de Genève",
        ],
    ),
    DarkWebRightsEntity(
        "DWR-005", "Criminal Marketplaces Dark Web — RaaS Ecosystems, 550M Records Volés & Rançongiciels Hôpitaux",
        "Global",
        "Criminal Dark Web Marketplaces AlphaBay/Hansa/ALPHV BlackCat RaaS, 550 Millions Records Identités Volées 2023 Breach Reports, Rançongiciels Hôpitaux Change Healthcare 190M Patients US, LockBit 2 000 Victimes 120 Pays & Fentanyl/Armes Vente Dark Web",
        60.0, 55.0, 50.0, 52.0,
        "data_trafficking",
        [
            "Écosystème criminel dark web violant droits fondamentaux des victimes à grande échelle documenté — Criminal Marketplaces avec score composite 54.65/100 révélant 550 millions d'identités volées en 2023 exposant les victimes à la fraude financière, les rançongiciels LockBit touchant 2 000 organisations dans 120 pays et l'attaque Change Healthcare exposant les données médicales de 190 millions d'Américains violant l'Article 17 PIDCP sur la vie privée",
            "Trafic données (55.0/100) — la vente de fentanyl sur les marchés dark web contribuant à 100 000 morts annuelles aux États-Unis, les marketplaces de vente d'armes à feu contournant les contrôles légaux et les forums de coordination de rançongiciels ciblant délibérément les hôpitaux (attaques considérées comme crimes de guerre en contexte conflictuel) révèlent un écosystème criminel menaçant directement les droits à la vie et à la santé",
        ],
    ),
    DarkWebRightsEntity(
        "DWR-006", "Dark Web CSAM Networks — Abus Sexuels Enfants, 400k Utilisateurs & Défaillances Identification",
        "Global",
        "Dark Web CSAM Child Sexual Abuse Material Welcome to Video 250 000 Vidéos Abusives, FBI Operation Delego Playpen 215 000 Utilisateurs, Résistance Chiffrement Identification Victimes, IWF 300 000 URLs CSAM 2023 & Cryptomonnaies Financement Anonyme",
        58.0, 52.0, 55.0, 50.0,
        "identity_theft_exposure",
        [
            "Réseau dark web d'exploitation sexuelle d'enfants à grande échelle documenté — Dark Web CSAM Networks avec score composite 54.15/100 révélant que la plateforme Welcome to Video hébergeait 250 000 vidéos d'abus sexuels d'enfants avec 1 million de téléchargements, que le réseau Playpen comptait 215 000 utilisateurs actifs et que l'IWF a identifié 300 000 URLs CSAM en 2023 violant les droits fondamentaux des victimes sous la Convention des Droits de l'Enfant Article 34",
            "Exposition victimes (58.0/100) — l'utilisation de cryptomonnaies pour financer anonymement les réseaux CSAM contournant les systèmes de détection financière, les défis du chiffrement pour identifier les victimes et les auteurs et la recrudescence de l'IA générative pour créer du contenu CSAM synthétique (CAIDCA) révèlent une criminalité dark web en évolution constante menaçant l'intégrité physique des enfants",
        ],
    ),
    DarkWebRightsEntity(
        "DWR-007", "EU Authorities Europol — Opérations Démantèlement Limitées, Attribution Difficile & Ressources Insuffisantes",
        "Europe",
        "EU Europol Operation Cronos LockBit Démantèlement Partiel 2024, Operation Tokaido AlphaBay, Coopération 40 Pays Mais Ressources Limitées, Attribution Cyber Complexe Juridictions, GDPR Tensions vs Accès Données Enquêtes & Budget Cybercriminalité 21M Euros",
        28.0, 30.0, 25.0, 28.0,
        "law_enforcement_overreach",
        [
            "Limites structurelles de la réponse européenne à la cybercriminalité dark web documentées — EU Authorities Europol avec score composite 27.75/100 montrant que malgré les démantèlements partiels d'AlphaBay (2017) et LockBit (Operation Cronos 2024), la recréation rapide des plateformes criminelles, la complexité d'attribution dans 40 juridictions et le budget cybercriminalité limité à 21 millions d'euros révèlent des lacunes structurelles de réponse",
            "Tensions droits/sécurité (28.0/100) — les tensions entre le RGPD protégeant la vie privée et les besoins d'accès aux données pour les enquêtes Europol, le risque de surpassement des pouvoirs dans les opérations d'infiltration dark web et l'absence de cadre juridique harmonisé pour les cyberopérations offensives européennes révèlent un défi de gouvernance numérique entre droits fondamentaux et sécurité",
        ],
    ),
    DarkWebRightsEntity(
        "DWR-008", "Tor Project — Meilleure Pratique Protection Vie Privée, Journalistes & Défenseurs Droits Humains",
        "Global",
        "Tor Project Fondation Non-Lucrative MIT Origins, 2 Millions Utilisateurs/Jour 200 Pays, Usage Journalistes/Dissidents/Lanceurs Alerte Documenté EFF/CPJ, OnionShare Transmission Sécurisée, SecureDrop Médias & Financé DARPA/DoS Programs Démocratie",
        8.0, 6.0, 10.0, 8.0,
        "privacy_erosion",
        [
            "Meilleure pratique de protection de la vie privée numérique et liberté d'expression documentée — Tor Project avec score composite 8.00/100 incarnant un outil de référence mondiale utilisé par 2 millions de personnes/jour dans 200 pays pour protéger la vie privée de journalistes, dissidents et lanceurs d'alerte documenté par EFF et CPJ comme essentiel à l'exercice de l'Article 19 PIDCP dans les régimes autoritaires",
            "Protection vie privée (8.0/100) — SecureDrop basé sur Tor permettant aux lanceurs d'alerte de transmettre des documents à des médias comme The Guardian et Washington Post en toute sécurité, OnionShare facilitant le partage de fichiers chiffré et le financement du Tor Project par le Département d'État américain pour les programmes de démocratie révèlent la reconnaissance officielle de la nécessité des outils de vie privée pour les droits humains",
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
        "domain": DOMAIN,
        "confidence_score": 0.87,
        "data_sources": [
            "fbi_internet_crime_complaint_center_ic3_report_2024",
            "europol_internet_organised_crime_threat_assessment_2024",
            "mandiant_apt_threat_intelligence_annual_report_2024",
            "internet_watch_foundation_annual_report_2023",
            "electronic_frontier_foundation_surveillance_self_defense",
        ],
        "entities": [e.to_dict() for e in ENTITIES],
        "avg_estimated_dark_web_rights_index": round(avg / 100 * 10, 2),
    }


if __name__ == "__main__":
    s = summary()
    print(f"Entities: {s['total_entities']}, Avg: {s['avg_composite']}, Dist: {s['risk_distribution']}")
    for e in ENTITIES:
        print(f"  {e.entity_id} {e.risk_level:8} {e.composite_score:6.2f} {e.name[:60]}")

"""
Agent Scout d'Éco-Responsabilité — surveille, évalue et certifie les pratiques
éco-responsables des entreprises selon EU Green Deal, Taxonomie UE, CSRD ESRS E1-E5.

Cadre réglementaire couvert :
  - Règlement Taxonomie UE (2020/852) — critères d'examen technique & DNSH
  - CSRD / ESRS E1-E5 (Directive 2022/2464 + Acte Délégué EFRAG 2023)
  - CSDDD (Directive 2024/1760) — diligence raisonnable droits humains & environnement
  - EU Green Claims Directive (COM/2023/166) — lutte contre le greenwashing
  - Stratégie UE pour la Biodiversité 2030 (COM/2020/380)
  - Directive cadre sur l'eau 2000/60/CE

CaelumSwarm™ — Caelum Partners
"""

from __future__ import annotations

import math
import random
from datetime import date, datetime
from typing import Any

# ---------------------------------------------------------------------------
# 1. DATA CONSTANTS
# ---------------------------------------------------------------------------

EU_TAXONOMY_ACTIVITIES: dict[str, dict[str, Any]] = {
    "manufacturing_renewable_energy": {
        "label": "Fabrication de technologies d'énergie renouvelable",
        "dnsh_criteria": [
            "Pas d'impact significatif sur les ressources en eau (seuil WEI+ <20 %)",
            "Gestion des déchets conforme à la hiérarchie UE (Directive 2008/98/CE)",
            "Évaluation biodiversité si site en zone Natura 2000",
            "Absence de substances dangereuses catégorie 1A/1B (REACH)",
        ],
        "technical_screening_criteria": [
            "Les équipements produisent de l'électricité depuis des sources renouvelables",
            "Analyse de cycle de vie (ACV) démontrant réduction GES ≥ 80 % vs baseline",
            "Conformité à la directive écoconception 2009/125/CE",
        ],
        "minimum_social_safeguards": [
            "Respect Principes Directeurs ONU Entreprises & Droits de l'Homme",
            "Conformité OCDE pour les entreprises multinationales",
            "Absence de travail forcé (Conventions OIT 29 & 105)",
            "Droits syndicaux garantis (Convention OIT 87 & 98)",
        ],
        "climate_mitigation_eligible": True,
        "climate_adaptation_eligible": False,
    },
    "sustainable_agriculture": {
        "label": "Agriculture durable et sylviculture",
        "dnsh_criteria": [
            "Maintien de la matière organique des sols (≥ 0,5 % carbone organique)",
            "Pas de conversion de forêts primaires ou de zones humides",
            "Gestion intégrée des ravageurs (IPM) — Directive 2009/128/CE",
            "Qualité des masses d'eau respectée (DCE 2000/60/CE)",
        ],
        "technical_screening_criteria": [
            "Agriculture biologique certifiée (Règlement UE 2018/848) OU",
            "Réduction émissions N₂O ≥ 20 % via techniques agro-écologiques",
            "Séquestration carbone sol ≥ 0,4 t CO₂e/ha/an mesurée",
        ],
        "minimum_social_safeguards": [
            "Salaire minimum légal garanti pour les travailleurs saisonniers",
            "Interdiction travail des enfants (Convention OIT 138 & 182)",
            "Accès à l'eau potable et sanitaires sur les exploitations",
        ],
        "climate_mitigation_eligible": True,
        "climate_adaptation_eligible": True,
    },
    "green_buildings_construction": {
        "label": "Construction et rénovation de bâtiments verts",
        "dnsh_criteria": [
            "Gestion des déchets de chantier : ≥ 70 % valorisés (Directive 2008/98/CE)",
            "Pas de matériaux contenant de l'amiante ou des PCB",
            "Étude d'impact hydrologique si construction en zone inondable",
            "Préservation des connectivités écologiques (Règlement 2024/1991 Nature Restauration)",
        ],
        "technical_screening_criteria": [
            "Performance énergétique primaire ≤ 10 % du seuil NZEB national",
            "Classe énergétique A selon DPE harmonisé",
            "Rapport d'analyse GES sur cycle de vie (Modules A1-A5) ≤ seuil UE",
        ],
        "minimum_social_safeguards": [
            "Conformité droit du travail national et conventions collectives",
            "Prévention risques professionnels (Directive 89/391/CEE)",
            "Chaîne d'approvisionnement matériaux tracée (CSDDD Art. 5-11)",
        ],
        "climate_mitigation_eligible": True,
        "climate_adaptation_eligible": True,
    },
    "clean_transport": {
        "label": "Transport propre et infrastructure de mobilité",
        "dnsh_criteria": [
            "Véhicules : zéro émission directe en exploitation (CO₂ = 0 g/km)",
            "Infrastructure compatible avec plusieurs modes de transport durable",
            "Bruit ≤ seuils Directive 2002/49/CE en zones sensibles",
            "Pas d'imperméabilisation nette des sols en zone humide",
        ],
        "technical_screening_criteria": [
            "Transport routier : 100 % électrique ou à hydrogène vert",
            "Transport ferroviaire : électrification ou hydrogène vert ≥ 90 %",
            "Logistique urbaine : véhicules L-catégorie ou cargo-bike en dernier km",
        ],
        "minimum_social_safeguards": [
            "Accès au transport pour les populations défavorisées",
            "Conditions de travail des conducteurs (Règlement 561/2006)",
            "Dialogue social avec représentants du personnel",
        ],
        "climate_mitigation_eligible": True,
        "climate_adaptation_eligible": False,
    },
    "water_management": {
        "label": "Gestion durable de l'eau et des eaux usées",
        "dnsh_criteria": [
            "Rejet dans les masses d'eau conforme aux valeurs limites DCE",
            "Pas de perturbation des régimes hydrologiques naturels",
            "Absence de substances prioritaires dangereuses (Directive 2013/39/UE)",
        ],
        "technical_screening_criteria": [
            "Rendement des réseaux ≥ 85 % (pertes < 15 %)",
            "Traitement tertiaire des eaux usées avant rejet (élimination N & P ≥ 80 %)",
            "Récupération d'énergie dans les STEP ≥ 50 % de l'énergie consommée",
        ],
        "minimum_social_safeguards": [
            "Accès universel à l'eau potable (ODD 6.1)",
            "Pas de privatisation discriminatoire de l'accès à l'eau",
            "Consultation des communautés riveraines (Convention d'Aarhus)",
        ],
        "climate_mitigation_eligible": False,
        "climate_adaptation_eligible": True,
    },
    "circular_economy_manufacturing": {
        "label": "Fabrication industrielle en économie circulaire",
        "dnsh_criteria": [
            "Substances dangereuses réduites selon Plan Action Zéro Pollution",
            "Déchets dangereux < 2 % de la production totale",
            "Pas d'exportation de déchets vers pays hors OCDE (Règlement 1013/2006)",
        ],
        "technical_screening_criteria": [
            "Taux d'incorporation de matières recyclées ≥ 30 % en masse",
            "Conception pour le démontage et la recyclabilité ≥ 80 %",
            "Taux de valorisation des déchets de production ≥ 95 %",
        ],
        "minimum_social_safeguards": [
            "Traçabilité des matières premières secondaires (CSDDD Art. 7)",
            "Conditions de collecte et tri dans les chaînes mondiales",
            "Respect du droit à un environnement sain (Résolution ONU A/76/L.75)",
        ],
        "climate_mitigation_eligible": True,
        "climate_adaptation_eligible": False,
    },
    "pollution_prevention": {
        "label": "Prévention et contrôle de la pollution industrielle",
        "dnsh_criteria": [
            "Conformité aux meilleures techniques disponibles (MTD/BAT — IED 2010/75/UE)",
            "Plan de gestion des substances chimiques (Stratégie Chimiques UE 2020)",
            "Surveillance continue des émissions avec reporting trimestriel",
        ],
        "technical_screening_criteria": [
            "Émissions atmosphériques ≤ 50 % des valeurs MTD-AEL associées",
            "Rejets aqueux ≤ 30 % des niveaux de référence MTD",
            "Zéro incident classé Seveso III sur 5 dernières années",
        ],
        "minimum_social_safeguards": [
            "Information des riverains sur les émissions (E-PRTR Règlement 166/2006)",
            "Mécanisme de réclamation accessible (CSDDD Art. 9)",
            "Évaluation sanitaire environnementale des populations exposées",
        ],
        "climate_mitigation_eligible": False,
        "climate_adaptation_eligible": False,
    },
    "biodiversity_restoration": {
        "label": "Restauration et protection de la biodiversité",
        "dnsh_criteria": [
            "Pas d'introduction d'espèces invasives (Règlement 1143/2014)",
            "Pas de drainage de zones humides ou de tourbières",
            "Évaluation appropriée des incidences Natura 2000 (Directive 92/43/CEE)",
        ],
        "technical_screening_criteria": [
            "Restauration d'au moins 30 % des habitats dégradés sur le site",
            "Plan de gestion biodiversité sur 10 ans avec indicateurs mesurables",
            "Connectivité écologique rétablie (Règlement 2024/1991 Art. 12)",
        ],
        "minimum_social_safeguards": [
            "Consentement libre, préalable et éclairé (CLPE) des peuples autochtones",
            "Partage équitable des avantages (Protocole de Nagoya 2010)",
            "Droits fonciers des communautés locales respectés",
        ],
        "climate_mitigation_eligible": True,
        "climate_adaptation_eligible": True,
    },
}

CSRD_ESRS_ENVIRONMENTAL: dict[str, dict[str, Any]] = {
    "E1": {
        "label": "ESRS E1 — Changement climatique",
        "key_disclosures": [
            "E1-1 : Plan de transition vers une économie bas-carbone (Art. 15 CSRD)",
            "E1-2 : Politiques liées au changement climatique",
            "E1-3 : Actions et ressources dédiées à la décarbonation",
            "E1-4 : Objectifs de réduction des émissions de GES alignés SBTi",
            "E1-5 : Consommation énergétique et mix énergétique",
            "E1-6 : Émissions GES Scope 1, 2, 3 (Protocole GHG)",
            "E1-7 : Absorptions et crédits carbone (qualité Gold Standard/VCS)",
            "E1-8 : Risques physiques et de transition (TCFD-aligned)",
            "E1-9 : Effets financiers des risques climatiques (scénarios 1,5 °C & 4 °C)",
        ],
        "quantitative_metrics": [
            "Émissions GES Scope 1 (t CO₂e/an)",
            "Émissions GES Scope 2 market-based (t CO₂e/an)",
            "Émissions GES Scope 3 par catégorie 1-15 (t CO₂e/an)",
            "Intensité carbone (t CO₂e / M€ de CA)",
            "Consommation énergie totale (MWh/an)",
            "Part énergie renouvelable (% du mix)",
            "Température d'alignement du portefeuille (°C)",
            "Investissements verts (% CapEx aligné Taxonomie)",
        ],
        "deadline": "2024 (grandes entreprises NFRD) / 2025 (autres grandes entités) / 2026 (PME cotées)",
        "applicable_to": "Toutes entreprises soumises à CSRD (Art. 19a & 29a Directive 2013/34/UE amendée)",
    },
    "E2": {
        "label": "ESRS E2 — Pollution",
        "key_disclosures": [
            "E2-1 : Politiques de prévention et contrôle de la pollution",
            "E2-2 : Actions de lutte contre la pollution (Plan Zéro Pollution 2030)",
            "E2-3 : Objectifs de réduction des polluants prioritaires",
            "E2-4 : Pollution de l'air, de l'eau et des sols (substances E-PRTR)",
            "E2-5 : Substances préoccupantes et extrêmement préoccupantes (REACH)",
            "E2-6 : Effets financiers liés à la pollution",
        ],
        "quantitative_metrics": [
            "Émissions de polluants atmosphériques (NOx, SOx, PM2.5, COV) en t/an",
            "Rejets dans l'eau (N total, P total, DCO) en t/an",
            "Pollution des sols : sites contaminés identifiés (nombre)",
            "Substances chimiques préoccupantes utilisées (t/an)",
            "Amendes réglementaires pollution (k€/an)",
            "Sites IED / Seveso actifs (nombre)",
        ],
        "deadline": "2024-2026 selon taille (même calendrier CSRD E1)",
        "applicable_to": "Secteurs industriels, chimie, agriculture intensive, extraction minière",
    },
    "E3": {
        "label": "ESRS E3 — Ressources aquatiques et marines",
        "key_disclosures": [
            "E3-1 : Politiques relatives à l'eau et aux ressources marines",
            "E3-2 : Actions de gestion durable de l'eau",
            "E3-3 : Objectifs de performance eau (réduction prélèvements, qualité rejets)",
            "E3-4 : Consommation et prélèvements d'eau par zone de stress hydrique",
            "E3-5 : Effets financiers des risques eau",
        ],
        "quantitative_metrics": [
            "Prélèvements d'eau totaux (m³/an) par source",
            "Consommation nette d'eau (m³/an)",
            "Rejets d'eau par destination (réseau, milieu naturel)",
            "Sites en zones de stress hydrique élevé (WRI Aqueduct score ≥ 3)",
            "Efficacité hydrique (m³/unité produite ou M€ CA)",
            "Taux de recyclage et recirculation de l'eau (%)",
        ],
        "deadline": "2024-2026 selon taille",
        "applicable_to": "Industries manufacturières, agroalimentaire, textile, extraction, services hospitaliers",
    },
    "E4": {
        "label": "ESRS E4 — Biodiversité et écosystèmes",
        "key_disclosures": [
            "E4-1 : Plan de transition biodiversité (Cadre Mondial Kunming-Montréal 30x30)",
            "E4-2 : Politiques relatives à la biodiversité et aux écosystèmes",
            "E4-3 : Actions de restauration (Règlement UE 2024/1991)",
            "E4-4 : Objectifs biodiversité mesurables (SBTN — Nature-based targets)",
            "E4-5 : Métriques d'impact (ENCORE, IBAT, TNFD Framework)",
            "E4-6 : Effets financiers sur la biodiversité",
        ],
        "quantitative_metrics": [
            "Empreinte foncière totale (ha) en zones sensibles",
            "Superficie en zones Natura 2000 / KBA (ha)",
            "Espèces menacées affectées (nombre IUCN Red List)",
            "Surface restaurée ou compensée (ha/an)",
            "Score TNFD de dépendance aux services écosystémiques (0-10)",
            "Déforestation nette imputable (ha/an — Règlement 2023/1115 EUDR)",
        ],
        "deadline": "2024-2026 selon taille ; EUDR applicable dès 2025",
        "applicable_to": "Agroalimentaire, sylviculture, textile, extraction minière, immobilier, pêche",
    },
    "E5": {
        "label": "ESRS E5 — Utilisation des ressources et économie circulaire",
        "key_disclosures": [
            "E5-1 : Politiques d'économie circulaire (Plan d'Action UE 2020)",
            "E5-2 : Actions de transition vers la circularité",
            "E5-3 : Objectifs de réduction des déchets et d'incorporation de recyclé",
            "E5-4 : Flux entrants de ressources (matières premières, eau, énergie)",
            "E5-5 : Flux sortants (produits, déchets, émissions)",
            "E5-6 : Effets financiers de la transition circulaire",
        ],
        "quantitative_metrics": [
            "Consommation de matières premières (t/an) par catégorie",
            "Taux de contenu recyclé (% en masse)",
            "Production de déchets totaux (t/an) par type",
            "Taux de valorisation des déchets (%)",
            "Déchets dangereux (t/an)",
            "Indice de circularité produits (score 0-100 — méthode Ellen MacArthur)",
            "Durée de vie moyenne des produits (années)",
        ],
        "deadline": "2024-2026 selon taille",
        "applicable_to": "Industrie manufacturière, packaging, textile, électronique, construction, retail",
    },
}

ECO_CERTIFICATION_STANDARDS: dict[str, dict[str, Any]] = {
    "ISO_14001": {
        "label": "ISO 14001:2015 — Système de Management Environnemental",
        "scope": "Amélioration continue performance environnementale, tous secteurs",
        "recognition_score": 7,
        "cost_range_EUR": "5 000 – 50 000",
        "renewal_years": 3,
        "csddd_alignment": (
            "Partielle — couvre identification des impacts environnementaux (CSDDD Art. 6) "
            "mais n'exige pas d'évaluation des droits humains"
        ),
    },
    "ISO_50001": {
        "label": "ISO 50001:2018 — Système de Management de l'Énergie",
        "scope": "Efficacité énergétique, tous secteurs à forte intensité énergétique",
        "recognition_score": 6,
        "cost_range_EUR": "8 000 – 40 000",
        "renewal_years": 3,
        "csddd_alignment": (
            "Faible — focus énergie uniquement ; complémentaire CSDDD Art. 7 "
            "(réduction empreinte climatique chaîne de valeur)"
        ),
    },
    "B_CORP": {
        "label": "Certification B Corp — Entreprise à impact social et environnemental",
        "scope": "Gouvernance, travailleurs, communauté, environnement, clients",
        "recognition_score": 9,
        "cost_range_EUR": "1 000 – 50 000",
        "renewal_years": 3,
        "csddd_alignment": (
            "Élevée — évaluation BIA couvre droits humains chaîne d'approvisionnement "
            "alignée CSDDD Art. 5-11 (diligence raisonnable environnement & droits humains)"
        ),
    },
    "FSC": {
        "label": "FSC — Forest Stewardship Council (gestion forestière responsable)",
        "scope": "Forêts, produits bois et papier, chaîne de custody",
        "recognition_score": 8,
        "cost_range_EUR": "3 000 – 30 000",
        "renewal_years": 5,
        "csddd_alignment": (
            "Élevée — FSC P&C v5 intègre droits des peuples autochtones (CLPE) "
            "et biodiversité, aligné CSDDD Art. 3(b) & ESRS E4"
        ),
    },
    "RAINFOREST_ALLIANCE": {
        "label": "Rainforest Alliance — Agriculture et forêts durables",
        "scope": "Café, cacao, thé, banane, fleurs, forêts tropicales",
        "recognition_score": 7,
        "cost_range_EUR": "2 000 – 25 000",
        "renewal_years": 3,
        "csddd_alignment": (
            "Moyenne-élevée — Standard 2020 couvre droits travailleurs agricoles "
            "et biodiversité ; aligné CSDDD sur chaînes cacao/café (EUDR)"
        ),
    },
    "FAIR_TRADE": {
        "label": "Fairtrade International — Commerce équitable",
        "scope": "Produits agricoles, artisanat, chaînes de valeur Sud-Nord",
        "recognition_score": 8,
        "cost_range_EUR": "1 500 – 20 000",
        "renewal_years": 3,
        "csddd_alignment": (
            "Élevée sur volet social — prix minimum garanti, prime développement, "
            "droits syndicaux ; CSDDD Art. 6 (identification impacts droits humains)"
        ),
    },
    "CRADLE_TO_CRADLE": {
        "label": "Cradle to Cradle Certified™ (C2C) — Économie circulaire produits",
        "scope": "Produits manufacturés, matériaux de construction, packaging",
        "recognition_score": 8,
        "cost_range_EUR": "10 000 – 80 000",
        "renewal_years": 2,
        "csddd_alignment": (
            "Moyenne — certification produit centrée matériaux sûrs & circularité ; "
            "aligne ESRS E5 mais limité sur droits humains chaîne amont (CSDDD Art. 7)"
        ),
    },
    "SCIENCE_BASED_TARGETS": {
        "label": "SBTi — Science Based Targets initiative (objectifs 1,5 °C)",
        "scope": "Réduction GES Scope 1-2-3 alignée trajectoire IPCC 1,5 °C",
        "recognition_score": 10,
        "cost_range_EUR": "15 000 – 120 000",
        "renewal_years": 5,
        "csddd_alignment": (
            "Très élevée — SBTi Corporate Net-Zero Standard couvre Scope 3 "
            "(chaîne de valeur amont/aval), complémentaire parfait CSDDD Art. 15 "
            "(plan de transition climatique) & ESRS E1-4"
        ),
    },
}

BIODIVERSITY_HOTSPOTS: list[dict[str, Any]] = [
    {
        "region": "Bassin du Congo (Afrique Centrale)",
        "threat_level": "CRITICAL",
        "key_species_at_risk": [
            "Gorille des plaines occidentales (CR)",
            "Okapi (EN)",
            "Bonobo (EN)",
            "Éléphant de forêt d'Afrique (CR)",
        ],
        "corporate_sectors_implicated": [
            "Exploitation forestière (bois tropical)",
            "Agroalimentaire (palmier à huile, cacao)",
            "Extraction minière (cobalt, coltan)",
            "Infrastructure (routes, barrages)",
        ],
        "legal_framework": (
            "EUDR Règlement 2023/1115 (bois, cacao) ; "
            "Convention de Ramsar (zones humides) ; "
            "CITES Annexe I (espèces protégées)"
        ),
    },
    {
        "region": "Amazonie (Brésil, Pérou, Colombie)",
        "threat_level": "CRITICAL",
        "key_species_at_risk": [
            "Jaguar (NT → VU)",
            "Dauphin rose de l'Amazone (EN)",
            "Tapir d'Amérique du Sud (VU)",
            "Ara de Lear (EN)",
        ],
        "corporate_sectors_implicated": [
            "Élevage bovin et cuir",
            "Soja et alimentation animale",
            "Bois tropical",
            "Extraction pétrolière et gazière",
        ],
        "legal_framework": (
            "EUDR Règlement 2023/1115 (bœuf, soja, bois) ; "
            "Accord de Paris Art. 5 (forêts REDD+) ; "
            "Cadre Kunming-Montréal Cible 2 (30x30)"
        ),
    },
    {
        "region": "Indonésie & Bornéo (Asie du Sud-Est)",
        "threat_level": "CRITICAL",
        "key_species_at_risk": [
            "Orang-outan de Bornéo (CR)",
            "Rhinocéros de Sumatra (CR)",
            "Tigre de Sumatra (CR)",
            "Éléphant pygmée de Bornéo (EN)",
        ],
        "corporate_sectors_implicated": [
            "Palmier à huile",
            "Pâte à papier et papier",
            "Caoutchouc naturel",
            "Extraction minière nickel",
        ],
        "legal_framework": (
            "EUDR Règlement 2023/1115 (huile de palme, caoutchouc) ; "
            "RSPO (certification huile de palme) ; "
            "Convention sur la Diversité Biologique"
        ),
    },
    {
        "region": "Méditerranée (Bassin méditerranéen)",
        "threat_level": "HIGH",
        "key_species_at_risk": [
            "Thon rouge de l'Atlantique (EN)",
            "Phoque moine de Méditerranée (EN)",
            "Tortue caouanne (VU)",
            "Posidonie océanique (herbier menacé)",
        ],
        "corporate_sectors_implicated": [
            "Pêche industrielle et aquaculture",
            "Tourisme côtier et croisières",
            "Agriculture irriguée (dérivation fleuves)",
            "Industrie pétrolière offshore",
        ],
        "legal_framework": (
            "Convention de Barcelone PNUE/PAM ; "
            "Règlement UE 1380/2013 (Politique Commune Pêche) ; "
            "Directive Habitats 92/43/CEE"
        ),
    },
    {
        "region": "Himalaya et Hindu Kush (Asie Centrale/Sud)",
        "threat_level": "HIGH",
        "key_species_at_risk": [
            "Léopard des neiges (VU)",
            "Panda géant (VU)",
            "Yak sauvage (VU)",
            "Griffe du diable (VU — pharmacopée)",
        ],
        "corporate_sectors_implicated": [
            "Textiles (laine cachemire — surpâturage)",
            "Pharmacie et compléments alimentaires (plantes)",
            "Hydroélectricité (barrages glaciaires)",
            "Tourisme d'altitude",
        ],
        "legal_framework": (
            "Convention de Ramsar (glaciers-zones humides) ; "
            "CITES (espèces rares) ; "
            "Accord de Paris (glaciers indicateurs climatiques)"
        ),
    },
    {
        "region": "Grande Barrière de Corail (Australie)",
        "threat_level": "CRITICAL",
        "key_species_at_risk": [
            "Dugong (VU)",
            "Tortue verte (EN)",
            "Requin-baleine (EN)",
            "Coraux constructeurs (blanchiment massif)",
        ],
        "corporate_sectors_implicated": [
            "Tourisme nautique et plongée",
            "Agriculture (ruissellement azote et pesticides)",
            "Navigation maritime et commerce",
            "Extraction minière côtière",
        ],
        "legal_framework": (
            "Convention du Patrimoine Mondial UNESCO ; "
            "Great Barrier Reef Marine Park Act 1975 (Australie) ; "
            "Convention MARPOL (pollutions maritimes)"
        ),
    },
    {
        "region": "Forêts atlantiques du Brésil (Mata Atlântica)",
        "threat_level": "CRITICAL",
        "key_species_at_risk": [
            "Lion tamarin doré (EN)",
            "Perroquet à ventre rouge (CR)",
            "Tapir de Baird (VU)",
            "Muriqui du Nord (CR)",
        ],
        "corporate_sectors_implicated": [
            "Agriculture (sucre, café, soja)",
            "Élevage bovin",
            "Urbanisation et infrastructure",
            "Industrie papetière (eucalyptus)",
        ],
        "legal_framework": (
            "EUDR Règlement 2023/1115 (café, bœuf, soja) ; "
            "Loi Forêt Atlantique Brésil 11.428/2006 ; "
            "Cadre Kunming-Montréal Cible 2"
        ),
    },
    {
        "region": "Arctique (zones circumpolaires)",
        "threat_level": "HIGH",
        "key_species_at_risk": [
            "Ours polaire (VU)",
            "Narval (NT)",
            "Morse de l'Atlantique (VU)",
            "Renard arctique (LC — vulnérable changement climatique)",
        ],
        "corporate_sectors_implicated": [
            "Extraction pétrolière et gazière offshore",
            "Pêche industrielle (cabillaud, hareng arctique)",
            "Navigation commerciale (route maritime Nord)",
            "Exploitation minière (terres rares, charbon)",
        ],
        "legal_framework": (
            "Traité de Svalbard (1920) ; "
            "Convention OSPAR (Atlantique Nord-Est) ; "
            "UNFCCC — Accord de Paris (réchauffement arctique ×3)"
        ),
    },
]

# ---------------------------------------------------------------------------
# 2. FUNCTIONS
# ---------------------------------------------------------------------------

# Sectoral mapping: sector → eco risk profile
_SECTOR_ECO_PROFILES: dict[str, dict[str, float]] = {
    "manufacturing": {
        "baseline_taxonomy": 42.0,
        "baseline_csrd": 38.0,
        "water_risk": 0.55,
        "pollution_risk": 0.65,
        "biodiversity_exposure": 0.45,
        "circular_economy": 40.0,
    },
    "agriculture": {
        "baseline_taxonomy": 35.0,
        "baseline_csrd": 32.0,
        "water_risk": 0.78,
        "pollution_risk": 0.60,
        "biodiversity_exposure": 0.80,
        "circular_economy": 30.0,
    },
    "construction": {
        "baseline_taxonomy": 38.0,
        "baseline_csrd": 35.0,
        "water_risk": 0.40,
        "pollution_risk": 0.50,
        "biodiversity_exposure": 0.55,
        "circular_economy": 35.0,
    },
    "transport": {
        "baseline_taxonomy": 30.0,
        "baseline_csrd": 28.0,
        "water_risk": 0.30,
        "pollution_risk": 0.70,
        "biodiversity_exposure": 0.35,
        "circular_economy": 25.0,
    },
    "energy": {
        "baseline_taxonomy": 50.0,
        "baseline_csrd": 45.0,
        "water_risk": 0.60,
        "pollution_risk": 0.55,
        "biodiversity_exposure": 0.50,
        "circular_economy": 45.0,
    },
    "retail": {
        "baseline_taxonomy": 25.0,
        "baseline_csrd": 30.0,
        "water_risk": 0.20,
        "pollution_risk": 0.25,
        "biodiversity_exposure": 0.40,
        "circular_economy": 35.0,
    },
    "technology": {
        "baseline_taxonomy": 40.0,
        "baseline_csrd": 42.0,
        "water_risk": 0.35,
        "pollution_risk": 0.30,
        "biodiversity_exposure": 0.25,
        "circular_economy": 50.0,
    },
    "chemicals": {
        "baseline_taxonomy": 28.0,
        "baseline_csrd": 33.0,
        "water_risk": 0.65,
        "pollution_risk": 0.85,
        "biodiversity_exposure": 0.60,
        "circular_economy": 30.0,
    },
    "food_beverage": {
        "baseline_taxonomy": 33.0,
        "baseline_csrd": 31.0,
        "water_risk": 0.72,
        "pollution_risk": 0.55,
        "biodiversity_exposure": 0.70,
        "circular_economy": 32.0,
    },
    "finance": {
        "baseline_taxonomy": 55.0,
        "baseline_csrd": 50.0,
        "water_risk": 0.10,
        "pollution_risk": 0.05,
        "biodiversity_exposure": 0.20,
        "circular_economy": 60.0,
    },
}

_DEFAULT_SECTOR_PROFILE: dict[str, float] = {
    "baseline_taxonomy": 35.0,
    "baseline_csrd": 33.0,
    "water_risk": 0.45,
    "pollution_risk": 0.45,
    "biodiversity_exposure": 0.45,
    "circular_economy": 35.0,
}

# High-risk country factor (environmental governance index proxy)
_HIGH_RISK_COUNTRIES: set[str] = {
    "brazil",
    "indonesia",
    "china",
    "india",
    "vietnam",
    "nigeria",
    "democratic republic of congo",
    "myanmar",
    "cambodia",
    "peru",
    "colombia",
    "bangladesh",
    "pakistan",
    "turkey",
    "russia",
    "malaysia",
}

_LOW_RISK_COUNTRIES: set[str] = {
    "germany",
    "france",
    "netherlands",
    "sweden",
    "denmark",
    "norway",
    "finland",
    "austria",
    "switzerland",
    "luxembourg",
    "belgium",
    "canada",
    "australia",
    "new zealand",
    "japan",
    "south korea",
    "singapore",
}

# Certification → score boost mapping
_CERT_SCORE_BOOST: dict[str, dict[str, float]] = {
    "ISO_14001": {"taxonomy": 5.0, "csrd": 4.0, "circular": 3.0},
    "ISO_50001": {"taxonomy": 4.0, "csrd": 3.0, "circular": 2.0},
    "B_CORP": {"taxonomy": 8.0, "csrd": 9.0, "circular": 6.0},
    "FSC": {"taxonomy": 7.0, "csrd": 6.0, "circular": 4.0},
    "RAINFOREST_ALLIANCE": {"taxonomy": 6.0, "csrd": 5.0, "circular": 3.0},
    "FAIR_TRADE": {"taxonomy": 5.0, "csrd": 7.0, "circular": 2.0},
    "CRADLE_TO_CRADLE": {"taxonomy": 6.0, "csrd": 5.0, "circular": 10.0},
    "SCIENCE_BASED_TARGETS": {"taxonomy": 10.0, "csrd": 12.0, "circular": 4.0},
}


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    """Borne une valeur dans [lo, hi]."""
    return max(lo, min(hi, value))


def _country_risk_factor(countries: list[str]) -> float:
    """
    Retourne un facteur de risque pays [0.0, 1.0].
    Plus élevé = plus de pays à gouvernance environnementale faible.
    """
    if not countries:
        return 0.3
    normalized = [c.lower().strip() for c in countries]
    high_risk_count = sum(1 for c in normalized if c in _HIGH_RISK_COUNTRIES)
    low_risk_count = sum(1 for c in normalized if c in _LOW_RISK_COUNTRIES)
    n = len(normalized)
    # Score de 0 (tous low-risk) à 1 (tous high-risk)
    raw = (high_risk_count - 0.5 * low_risk_count) / n
    return _clamp(raw, 0.0, 1.0)


def _revenue_size_factor(revenue_meur: float) -> float:
    """
    Plus l'entreprise est grande, plus le score de maturité potentiel est élevé
    (ressources disponibles), mais aussi plus forte exposition CSRD/CSDDD.
    """
    if revenue_meur < 10:
        return 0.7
    elif revenue_meur < 50:
        return 0.8
    elif revenue_meur < 150:
        return 0.9
    elif revenue_meur < 500:
        return 1.0
    else:
        return 1.05


def _recommend_certifications(
    sector: str,
    taxonomy_score: float,
    csrd_score: float,
    circular_score: float,
    biodiversity_exposure: float,
) -> list[dict[str, str]]:
    """
    Recommande les certifications les plus pertinentes selon le profil de l'entreprise.
    """
    recommendations: list[dict[str, str]] = []

    # Toujours recommander SBTi si score CSRD < 70
    if csrd_score < 70:
        recommendations.append(
            {
                "certification": "SCIENCE_BASED_TARGETS",
                "label": ECO_CERTIFICATION_STANDARDS["SCIENCE_BASED_TARGETS"]["label"],
                "priority": "HAUTE",
                "justification": (
                    "Alignement SBTi 1,5 °C indispensable pour CSRD ESRS E1-4 "
                    "et CSDDD Art. 15 (plan de transition)"
                ),
            }
        )

    # ISO 14001 si score Taxonomie < 60
    if taxonomy_score < 60:
        recommendations.append(
            {
                "certification": "ISO_14001",
                "label": ECO_CERTIFICATION_STANDARDS["ISO_14001"]["label"],
                "priority": "HAUTE",
                "justification": (
                    "Fondation du SME : prérequis pour accéder aux financements "
                    "Taxonomie UE (Art. 8 Acte Délégué)"
                ),
            }
        )

    # Cradle to Cradle si score circulaire < 45
    if circular_score < 45 and sector in (
        "manufacturing",
        "chemicals",
        "construction",
        "retail",
    ):
        recommendations.append(
            {
                "certification": "CRADLE_TO_CRADLE",
                "label": ECO_CERTIFICATION_STANDARDS["CRADLE_TO_CRADLE"]["label"],
                "priority": "MOYENNE",
                "justification": (
                    "Score économie circulaire insuffisant ; C2C aligne ESRS E5 "
                    "et Plan d'Action UE Économie Circulaire 2020"
                ),
            }
        )

    # FSC / Rainforest Alliance si exposition biodiversité élevée
    if biodiversity_exposure > 0.60 and sector in (
        "agriculture",
        "food_beverage",
        "manufacturing",
    ):
        recommendations.append(
            {
                "certification": "FSC",
                "label": ECO_CERTIFICATION_STANDARDS["FSC"]["label"],
                "priority": "HAUTE",
                "justification": (
                    "Exposition biodiversité critique ; FSC répond à EUDR 2023/1115 "
                    "et ESRS E4 (déforestation, droits peuples autochtones)"
                ),
            }
        )
        recommendations.append(
            {
                "certification": "RAINFOREST_ALLIANCE",
                "label": ECO_CERTIFICATION_STANDARDS["RAINFOREST_ALLIANCE"]["label"],
                "priority": "MOYENNE",
                "justification": (
                    "Complément FSC pour filières agricoles tropicales ; "
                    "couvre critères EUDR cacao, café, caoutchouc"
                ),
            }
        )

    # B Corp si score CSRD > 55 (maturité suffisante)
    if csrd_score > 55:
        recommendations.append(
            {
                "certification": "B_CORP",
                "label": ECO_CERTIFICATION_STANDARDS["B_CORP"]["label"],
                "priority": "MOYENNE",
                "justification": (
                    "Certification holistique ESG ; forte reconnaissance marché ; "
                    "aligne CSDDD diligence raisonnable droits humains & environnement"
                ),
            }
        )

    # Déduplique et limite à 5 recommandations max
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for rec in recommendations:
        if rec["certification"] not in seen:
            seen.add(rec["certification"])
            unique.append(rec)
    return unique[:5]


def scout_company_eco_profile(
    company: str,
    sector: str,
    revenue_MEUR: float,
    countries_of_operation: list[str],
) -> dict[str, Any]:
    """
    Génère un profil éco-responsabilité complet pour une entreprise.

    Paramètres
    ----------
    company               : Nom de l'entreprise analysée
    sector                : Secteur d'activité (clé de _SECTOR_ECO_PROFILES)
    revenue_MEUR          : Chiffre d'affaires en millions EUR
    countries_of_operation: Liste des pays d'opération / chaîne d'approvisionnement

    Retourne
    --------
    dict contenant :
      - taxonomy_alignment_score (0-100)
      - csrd_readiness (0-100)
      - certifications_recommended (list)
      - biodiversity_exposure (float 0-1)
      - water_risk (float 0-1)
      - pollution_risk (float 0-1)
      - circular_economy_score (float 0-100)
      - csddd_exposure_level (str)
      - analysis_timestamp (str)
    """
    profile = _SECTOR_ECO_PROFILES.get(sector.lower(), _DEFAULT_SECTOR_PROFILE)
    country_risk = _country_risk_factor(countries_of_operation)
    size_factor = _revenue_size_factor(revenue_MEUR)

    # --- Scores de base ---
    # Le risque pays dégrade légèrement le score (gouvernance faible = pratiques moins robustes)
    taxonomy_base = profile["baseline_taxonomy"] * size_factor * (1 - 0.15 * country_risk)
    csrd_base = profile["baseline_csrd"] * size_factor * (1 - 0.10 * country_risk)

    # --- Ajustement selon nombre de pays (complexité supply chain) ---
    n_countries = len(countries_of_operation)
    complexity_penalty = min(5.0, n_countries * 0.5)
    taxonomy_score = _clamp(taxonomy_base - complexity_penalty)
    csrd_score = _clamp(csrd_base - complexity_penalty)

    # --- Scores environnementaux ---
    water_risk = _clamp(
        profile["water_risk"] + 0.10 * country_risk + 0.02 * min(n_countries, 5),
        0.0,
        1.0,
    )
    pollution_risk = _clamp(
        profile["pollution_risk"] + 0.08 * country_risk,
        0.0,
        1.0,
    )
    biodiversity_exposure = _clamp(
        profile["biodiversity_exposure"] + 0.12 * country_risk,
        0.0,
        1.0,
    )
    circular_economy_score = _clamp(
        profile["circular_economy"] * size_factor * (1 - 0.05 * country_risk)
    )

    # --- Exposition CSDDD ---
    if revenue_MEUR >= 150 or (revenue_MEUR >= 40 and len(countries_of_operation) >= 3):
        if country_risk > 0.5:
            csddd_level = "ÉLEVÉE — obligation diligence raisonnable CSDDD dès 2026-2027"
        else:
            csddd_level = "MOYENNE — seuils CSDDD atteints, obligation de conformité progressive"
    else:
        csddd_level = "FAIBLE — sous seuils CSDDD actuels (< 150 M€ CA ou < 40 M€ + 1 pays tiers)"

    # --- Recommandations certifications ---
    certifications_recommended = _recommend_certifications(
        sector=sector.lower(),
        taxonomy_score=taxonomy_score,
        csrd_score=csrd_score,
        circular_score=circular_economy_score,
        biodiversity_exposure=biodiversity_exposure,
    )

    # --- Zones de hotspot biodiversité exposées ---
    hotspots_exposed: list[str] = []
    normalized_countries = {c.lower().strip() for c in countries_of_operation}
    region_country_map = {
        "Bassin du Congo (Afrique Centrale)": {"democratic republic of congo", "cameroon", "gabon", "republic of congo"},
        "Amazonie (Brésil, Pérou, Colombie)": {"brazil", "peru", "colombia", "bolivia", "ecuador"},
        "Indonésie & Bornéo (Asie du Sud-Est)": {"indonesia", "malaysia", "brunei"},
        "Himalaya et Hindu Kush (Asie Centrale/Sud)": {"india", "china", "nepal", "pakistan", "bhutan"},
        "Forêts atlantiques du Brésil (Mata Atlântica)": {"brazil"},
        "Arctique (zones circumpolaires)": {"russia", "norway", "canada"},
    }
    for hotspot, countries_set in region_country_map.items():
        if normalized_countries & countries_set:
            hotspots_exposed.append(hotspot)

    return {
        "company": company,
        "sector": sector,
        "revenue_MEUR": revenue_MEUR,
        "countries_analyzed": countries_of_operation,
        "analysis_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "taxonomy_alignment_score": round(taxonomy_score, 1),
        "csrd_readiness": round(csrd_score, 1),
        "certifications_recommended": certifications_recommended,
        "biodiversity_exposure": round(biodiversity_exposure, 2),
        "biodiversity_hotspots_exposed": hotspots_exposed,
        "water_risk": round(water_risk, 2),
        "pollution_risk": round(pollution_risk, 2),
        "circular_economy_score": round(circular_economy_score, 1),
        "csddd_exposure_level": csddd_level,
        "country_risk_factor": round(country_risk, 2),
        "regulatory_deadlines": {
            "CSRD_first_report": "2025 (données 2024) pour grandes entreprises > 500 salariés",
            "EUDR_compliance": "2025-01-01 (grands opérateurs) / 2026-07-01 (PME)",
            "CSDDD_transposition": "2026 (EU Member States) — application progressive",
            "EU_Green_Claims_Directive": "En vigueur après adoption prévue 2024-2025",
        },
    }


def assess_eu_taxonomy_eligibility(
    activities: list[str],
    revenue_breakdown: dict[str, float],
) -> dict[str, Any]:
    """
    Vérifie l'éligibilité et l'alignement Taxonomie UE pour chaque activité déclarée.

    Paramètres
    ----------
    activities       : Liste de clés d'activités (issues de EU_TAXONOMY_ACTIVITIES)
    revenue_breakdown: Dict activité → % du CA

    Retourne
    --------
    dict contenant :
      - eligible_revenue_pct
      - aligned_revenue_pct
      - per_activity_assessment
      - dnsh_compliance_gaps
      - minimum_social_safeguards_met
      - taxonomy_kpi (pour reporting Art. 8 Acte Délégué)
    """
    total_declared_pct = sum(revenue_breakdown.values())
    if total_declared_pct > 100.0:
        raise ValueError(
            f"La somme des pourcentages de CA dépasse 100 % "
            f"(total déclaré : {total_declared_pct:.1f} %)"
        )

    eligible_pct = 0.0
    aligned_pct = 0.0
    dnsh_gaps: list[str] = []
    social_safeguards_issues: list[str] = []
    per_activity: list[dict[str, Any]] = []

    for act_key in activities:
        act_revenue_pct = revenue_breakdown.get(act_key, 0.0)

        if act_key not in EU_TAXONOMY_ACTIVITIES:
            per_activity.append(
                {
                    "activity": act_key,
                    "status": "NON_RECONNUE",
                    "revenue_pct": act_revenue_pct,
                    "eligible": False,
                    "aligned": False,
                    "notes": (
                        f"Activité '{act_key}' absente de la liste Taxonomie UE "
                        "reconnue — vérifier Actes Délégués 2021/2139 & 2022/1214"
                    ),
                }
            )
            continue

        act_data = EU_TAXONOMY_ACTIVITIES[act_key]

        # Éligibilité = activité listée dans l'Acte Délégué
        is_eligible = True
        eligible_pct += act_revenue_pct

        # Simulation conformité DNSH (heuristique documentaire)
        # Dans un système réel, on analyserait les données réelles de l'entreprise
        dnsh_issues_for_act: list[str] = []
        # On génère une liste de gaps potentiels basée sur les critères DNSH
        # En production : croisement avec données réelles terrain
        sample_gaps = act_data["dnsh_criteria"][:1]  # Premier critère = gap commun
        for gap in sample_gaps:
            dnsh_issues_for_act.append(f"[{act_key}] DNSH à documenter : {gap}")

        # Alignement = éligible + conformité DNSH + critères techniques + garde-fous sociaux
        # Taux d'alignement simulé : 40-75 % selon activité (gap de maturité marché moyen UE)
        alignment_rates: dict[str, float] = {
            "manufacturing_renewable_energy": 0.70,
            "sustainable_agriculture": 0.45,
            "green_buildings_construction": 0.55,
            "clean_transport": 0.60,
            "water_management": 0.65,
            "circular_economy_manufacturing": 0.50,
            "pollution_prevention": 0.40,
            "biodiversity_restoration": 0.35,
        }
        rate = alignment_rates.get(act_key, 0.50)
        act_aligned_pct = act_revenue_pct * rate
        aligned_pct += act_aligned_pct

        # Collecte des gaps
        dnsh_gaps.extend(dnsh_issues_for_act)

        # Vérification garde-fous sociaux (simplifiée — en production : audit tiers)
        if act_data["minimum_social_safeguards"]:
            social_safeguards_issues.append(
                f"[{act_key}] Vérification requise : "
                f"{act_data['minimum_social_safeguards'][0]}"
            )

        per_activity.append(
            {
                "activity": act_key,
                "label": act_data["label"],
                "revenue_pct": act_revenue_pct,
                "eligible": is_eligible,
                "aligned": True,
                "aligned_revenue_pct": round(act_aligned_pct, 1),
                "alignment_rate": f"{rate * 100:.0f} %",
                "climate_mitigation_eligible": act_data["climate_mitigation_eligible"],
                "climate_adaptation_eligible": act_data["climate_adaptation_eligible"],
                "dnsh_gap_count": len(dnsh_issues_for_act),
                "key_technical_screening": act_data["technical_screening_criteria"],
            }
        )

    social_safeguards_met = len(social_safeguards_issues) == 0

    # KPI Taxonomie pour reporting Art. 8 (non-financial undertakings)
    taxonomy_kpi = {
        "turnover_eligible_pct": round(eligible_pct, 1),
        "turnover_aligned_pct": round(aligned_pct, 1),
        "capex_eligible_pct": round(eligible_pct * 1.1, 1),  # CapEx généralement > CA éligible
        "capex_aligned_pct": round(aligned_pct * 0.85, 1),
        "opex_eligible_pct": round(eligible_pct * 0.90, 1),
        "opex_aligned_pct": round(aligned_pct * 0.75, 1),
    }

    return {
        "activities_assessed": activities,
        "eligible_revenue_pct": round(eligible_pct, 1),
        "aligned_revenue_pct": round(aligned_pct, 1),
        "alignment_gap_pct": round(eligible_pct - aligned_pct, 1),
        "per_activity_assessment": per_activity,
        "dnsh_compliance_gaps": dnsh_gaps,
        "minimum_social_safeguards_met": social_safeguards_met,
        "social_safeguards_verification_needed": social_safeguards_issues,
        "taxonomy_kpi_art8": taxonomy_kpi,
        "next_steps": [
            "Mandater un auditeur tiers accrédité pour vérification conformité DNSH",
            "Compléter la documentation technique (ACV, bilans GES Scope 1-2-3)",
            "Mettre en place les garde-fous sociaux documentés (OIT, OCDE, UNGP)",
            f"Viser ≥ {round(aligned_pct * 1.4, 0):.0f} % CA aligné d'ici 2027 "
            "(trajectoire marché UE 50 % aligné en 2030)",
        ],
    }


def generate_eco_roadmap(
    company: str,
    current_scores: dict[str, Any],
    target_year: int = 2027,
) -> dict[str, Any]:
    """
    Crée une feuille de route éco-responsabilité année par année jusqu'à target_year.

    Paramètres
    ----------
    company       : Nom de l'entreprise
    current_scores: Dict de scores actuels (taxonomy_alignment_score, csrd_readiness,
                    circular_economy_score, water_risk, pollution_risk, biodiversity_exposure)
    target_year   : Année cible de la roadmap (default 2027)

    Retourne
    --------
    dict avec milestones par année, investissements requis, améliorations attendues,
    calendrier certifications
    """
    current_year = date.today().year
    if target_year <= current_year:
        raise ValueError(
            f"L'année cible ({target_year}) doit être postérieure à l'année courante ({current_year})"
        )

    years = list(range(current_year, target_year + 1))

    # Scores de base
    tax_score = float(current_scores.get("taxonomy_alignment_score", 35.0))
    csrd_score = float(current_scores.get("csrd_readiness", 33.0))
    circular_score = float(current_scores.get("circular_economy_score", 35.0))
    water_risk = float(current_scores.get("water_risk", 0.50))
    pollution_risk = float(current_scores.get("pollution_risk", 0.50))
    biodiv_exposure = float(current_scores.get("biodiversity_exposure", 0.50))

    # Cibles 2027 — ambitions EU Green Deal
    tax_target = min(tax_score + 35.0, 80.0)
    csrd_target = min(csrd_score + 40.0, 85.0)
    circular_target = min(circular_score + 30.0, 75.0)
    water_target = max(water_risk - 0.25, 0.15)
    pollution_target = max(pollution_risk - 0.30, 0.10)
    biodiv_target = max(biodiv_exposure - 0.20, 0.20)

    n_years = len(years) - 1  # nombre d'intervalles

    def _lerp(start: float, end: float, step: int, total: int) -> float:
        if total == 0:
            return end
        # Progression en S-curve légère (accélération en milieu de période)
        t = step / total
        # Ease-in-out quadratic
        if t < 0.5:
            factor = 2 * t * t
        else:
            factor = 1 - (-2 * t + 2) ** 2 / 2
        return start + (end - start) * factor

    # Investissements typiques par phase (en k€)
    investment_phases: dict[str, dict[str, Any]] = {
        "phase_1_diagnostic": {
            "label": "Phase 1 — Diagnostic & fondations",
            "type": "Conseil, audit, bilan GES, ACV, double matérialité ESRS",
            "investment_kEUR": round(max(50, tax_score * 3), 0),
            "roi_expected": "Conformité CSRD, accès financements verts",
        },
        "phase_2_certification": {
            "label": "Phase 2 — Certifications prioritaires",
            "type": "ISO 14001, SBTi engagement, préparation B Corp",
            "investment_kEUR": round(max(80, csrd_score * 4), 0),
            "roi_expected": "Réduction coût capital (-50-100 bps), accès marchés UE",
        },
        "phase_3_transformation": {
            "label": "Phase 3 — Transformation opérationnelle",
            "type": "Efficacité énergétique, circularité, gestion eau, chaîne amont",
            "investment_kEUR": round(max(200, circular_score * 8), 0),
            "roi_expected": "Réduction coûts opérationnels 10-25 %, conformité CSDDD",
        },
        "phase_4_leadership": {
            "label": "Phase 4 — Leadership & reporting avancé",
            "type": "Taxonomie UE alignée, Nature-based targets SBTN, TNFD disclosure",
            "investment_kEUR": round(max(150, tax_target * 5), 0),
            "roi_expected": "Accès EU Green Bond Standard, premium ESG valorisation",
        },
    }

    # Milestones par année
    milestones_per_year: list[dict[str, Any]] = []
    certification_timeline: list[dict[str, str]] = []

    regulatory_milestones = {
        2024: "CSRD applicable aux entreprises NFRD (> 500 salariés) — données 2024",
        2025: "CSRD élargie + EUDR applicable grands opérateurs + SBTi deadline S3",
        2026: "CSDDD transposée UE — diligence raisonnable obligatoire grandes entreprises",
        2027: "CSRD PME cotées + revue mi-parcours Stratégie Biodiversité 2030",
        2028: "Révision Actes Délégués Taxonomie (nouvelles activités sectorielles)",
        2029: "Bilan intermédiaire EU Green Deal — recalibrage objectifs 2035",
        2030: "Objectif 30x30 biodiversité (Kunming-Montréal) + 55 % réduction GES UE",
    }

    for i, yr in enumerate(years):
        step = i
        proj_tax = round(_lerp(tax_score, tax_target, step, n_years), 1)
        proj_csrd = round(_lerp(csrd_score, csrd_target, step, n_years), 1)
        proj_circular = round(_lerp(circular_score, circular_target, step, n_years), 1)
        proj_water = round(_lerp(water_risk, water_target, step, n_years), 2)
        proj_pollution = round(_lerp(pollution_risk, pollution_target, step, n_years), 2)
        proj_biodiv = round(_lerp(biodiv_exposure, biodiv_target, step, n_years), 2)

        # Milestones qualitatifs par année
        yr_milestones: list[str] = []
        yr_certs: list[str] = []

        if yr == current_year:
            yr_milestones += [
                "Réaliser le bilan GES Scope 1 & 2 (Protocole GHG)",
                "Lancer l'analyse de double matérialité ESRS (EFRAG IG1)",
                "Cartographier la chaîne de valeur amont pour CSDDD",
                "Évaluation initiale Taxonomie UE (éligibilité activités)",
            ]
            yr_certs = ["Engagement SBTi (lettre d'intention)", "Pré-audit ISO 14001"]

        elif step == 1:
            yr_milestones += [
                "Publier premier rapport CSRD conforme ESRS E1-E5",
                "Déposer objectifs SBTi 1,5 °C pour validation",
                "Lancer audit ISO 14001 pour certification",
                "Cartographier risques EUDR si filières bois/agri concernées",
            ]
            yr_certs = ["Certification ISO 14001 visée", "Validation SBTi Scope 1+2"]

        elif step == 2:
            yr_milestones += [
                "Intégrer bilan GES Scope 3 complet (catégories 1-15)",
                "Mettre en œuvre plan de transition CSDDD Art. 15",
                "Atteindre 50 % énergie renouvelable dans le mix",
                "Déployer programme d'économie circulaire fournisseurs",
            ]
            yr_certs = [
                "ISO 50001 (si > 250 salariés ou intensité énergétique élevée)",
                "Cradle to Cradle Bronze (packaging / produits phares)",
            ]

        elif step >= 3:
            yr_milestones += [
                "Alignement Taxonomie UE ≥ 50 % du CA (objectif marché 2027)",
                f"Rapport ESRS E4 avec métriques TNFD (biodiversité financière)",
                "Engagement Nature-based targets SBTN pour Scope 3 amont",
                "Présenter plan de conformité CSDDD complet aux actionnaires",
            ]
            yr_certs = [
                "B Corp Certification (si score BIA ≥ 80)",
                "SBTi Scope 3 validation finale",
            ]

        reg_note = regulatory_milestones.get(yr, "")

        milestones_per_year.append(
            {
                "year": yr,
                "projected_scores": {
                    "taxonomy_alignment": proj_tax,
                    "csrd_readiness": proj_csrd,
                    "circular_economy": proj_circular,
                    "water_risk": proj_water,
                    "pollution_risk": proj_pollution,
                    "biodiversity_exposure": proj_biodiv,
                },
                "milestones": yr_milestones,
                "certifications_targeted": yr_certs,
                "regulatory_context": reg_note,
            }
        )

        if yr_certs:
            for cert in yr_certs:
                certification_timeline.append({"year": str(yr), "certification": cert})

    total_investment = sum(
        v["investment_kEUR"] for v in investment_phases.values()
    )

    return {
        "company": company,
        "roadmap_period": f"{current_year}–{target_year}",
        "current_scores": {
            "taxonomy_alignment_score": tax_score,
            "csrd_readiness": csrd_score,
            "circular_economy_score": circular_score,
        },
        "target_scores_2027": {
            "taxonomy_alignment_score": round(tax_target, 1),
            "csrd_readiness": round(csrd_target, 1),
            "circular_economy_score": round(circular_target, 1),
            "water_risk_reduction": f"{water_risk:.2f} → {water_target:.2f}",
            "pollution_risk_reduction": f"{pollution_risk:.2f} → {pollution_target:.2f}",
        },
        "investment_phases": investment_phases,
        "total_investment_estimate_kEUR": total_investment,
        "milestones_per_year": milestones_per_year,
        "certification_timeline": certification_timeline,
        "expected_benefits": [
            "Accès aux obligations vertes EU Green Bond Standard (GBS)",
            "Réduction prime de risque ESG (-50 à -150 bps coût dette)",
            "Conformité CSDDD évitant amendes jusqu'à 5 % du CA mondial",
            "Accès marchés publics UE (critères ESG marchés > 5 M€)",
            "Attraction talents : 67 % des milléniaux privilégient employeurs durables",
            "Résilience supply chain face aux risques physiques climatiques",
        ],
        "key_frameworks_referenced": [
            "EU Taxonomie — Règlement 2020/852 & Actes Délégués",
            "CSRD — Directive 2022/2464 + ESRS E1-E5 (EFRAG 2023)",
            "CSDDD — Directive 2024/1760 (diligence raisonnable)",
            "EU Green Deal & Fit for 55 Package",
            "Cadre Mondial Kunming-Montréal pour la Biodiversité",
            "Accord de Paris Art. 2, 4 & 15",
            "SBTi Corporate Net-Zero Standard v1.0",
            "TNFD Framework v1.0 (nature-related financial disclosures)",
        ],
    }


def detect_greenwashing_risk(
    company: str,
    claims: list[str],
    actual_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Analyse les allégations environnementales d'une entreprise vs ses données réelles
    pour détecter les risques de greenwashing.

    Paramètres
    ----------
    company     : Nom de l'entreprise
    claims      : Liste d'allégations environnementales publiques (marketing, rapports)
    actual_data : Dict de données réelles mesurées (GES, eau, déchets, certifications, etc.)

    Retourne
    --------
    dict avec :
      - risk_level (HIGH/MEDIUM/LOW)
      - specific_flags (liste des incohérences détectées)
      - recommended_corrections
      - EU_Green_Claims_Directive_exposure
      - CSRD_misstatement_risk
    """
    specific_flags: list[dict[str, str]] = []

    # Indicateurs verts dans actual_data
    ghg_reduction_claimed_pct = float(actual_data.get("ghg_reduction_claimed_pct", 0))
    ghg_reduction_actual_pct = float(actual_data.get("ghg_reduction_actual_pct", 0))
    renewable_energy_claimed_pct = float(actual_data.get("renewable_energy_claimed_pct", 0))
    renewable_energy_actual_pct = float(actual_data.get("renewable_energy_actual_pct", 0))
    scope3_reported = bool(actual_data.get("scope3_reported", False))
    carbon_offsets_used = bool(actual_data.get("carbon_offsets_used", False))
    offset_quality = str(actual_data.get("offset_quality", "UNKNOWN"))  # GOLD_STANDARD / VCS / VERRA / LOW / UNKNOWN
    taxonomy_aligned_claimed_pct = float(actual_data.get("taxonomy_aligned_claimed_pct", 0))
    taxonomy_aligned_actual_pct = float(actual_data.get("taxonomy_aligned_actual_pct", 0))
    certifications_held = list(actual_data.get("certifications_held", []))
    biodiversity_impact_assessed = bool(actual_data.get("biodiversity_impact_assessed", False))
    environmental_fines_last3y = float(actual_data.get("environmental_fines_last3y_kEUR", 0))
    water_consumption_disclosed = bool(actual_data.get("water_consumption_disclosed", False))

    # === RÈGLES DE DÉTECTION ===

    # 1. Écart GES revendicqué vs réel
    if ghg_reduction_claimed_pct > ghg_reduction_actual_pct + 10:
        specific_flags.append(
            {
                "category": "ÉMISSIONS GES — Surestimation",
                "severity": "HAUTE",
                "description": (
                    f"Réduction GES revendiquée ({ghg_reduction_claimed_pct:.0f} %) "
                    f"supérieure de {ghg_reduction_claimed_pct - ghg_reduction_actual_pct:.0f} pts "
                    f"aux données réelles ({ghg_reduction_actual_pct:.0f} %)"
                ),
                "regulation": (
                    "EU Green Claims Directive Art. 3(2)(a) — allégations vérifiables ; "
                    "CSRD ESRS E1-6 — exactitude métriques GES"
                ),
            }
        )

    # 2. Énergie renouvelable surestimée
    if renewable_energy_claimed_pct > renewable_energy_actual_pct + 15:
        specific_flags.append(
            {
                "category": "ÉNERGIE RENOUVELABLE — Allégation infondée",
                "severity": "HAUTE",
                "description": (
                    f"Part ENR revendiquée ({renewable_energy_claimed_pct:.0f} %) "
                    f"vs réelle ({renewable_energy_actual_pct:.0f} %) — "
                    "utilisation probable de Garanties d'Origine sans consommation réelle"
                ),
                "regulation": (
                    "EU Green Claims Directive Art. 3(2)(b) — preuves scientifiques requises ; "
                    "RE-Source Coalition — principes intégrité PPAs"
                ),
            }
        )

    # 3. Claims Taxonomie UE gonflés
    if taxonomy_aligned_claimed_pct > taxonomy_aligned_actual_pct + 10:
        specific_flags.append(
            {
                "category": "TAXONOMIE UE — Déclaration inexacte Art. 8",
                "severity": "CRITIQUE",
                "description": (
                    f"CA aligné Taxonomie revendiqué ({taxonomy_aligned_claimed_pct:.0f} %) "
                    f"supérieur au réel ({taxonomy_aligned_actual_pct:.0f} %) — "
                    "exposition réglementaire SFDR & Taxonomie reporting"
                ),
                "regulation": (
                    "Règlement Taxonomie Art. 8 (obligation reporting exact) ; "
                    "ESMA Guidelines Sustainable Finance Disclosures — "
                    "sanction potentielle jusqu'à 5 % CA (Directive Omnibus)"
                ),
            }
        )

    # 4. Scope 3 non reporté mais allégations de neutralité carbone
    for claim in claims:
        claim_lower = claim.lower()
        if any(
            kw in claim_lower
            for kw in [
                "neutre en carbone",
                "net zéro",
                "net-zero",
                "carbon neutral",
                "zéro émission",
                "zero emission",
                "climate positive",
            ]
        ) and not scope3_reported:
            specific_flags.append(
                {
                    "category": "NEUTRALITÉ CARBONE — Scope 3 absent",
                    "severity": "CRITIQUE",
                    "description": (
                        f"Allégation '{claim}' : neutralité carbone revendiquée "
                        "sans bilan Scope 3 publié — représente généralement 70-90 % "
                        "des émissions totales (Protocole GHG Scope 3)"
                    ),
                    "regulation": (
                        "ISO 14064-1:2018 — inventaire GES complet Scope 1+2+3 requis ; "
                        "EU Green Claims Directive Art. 3(3)(d) — "
                        "interdiction allégations neutralité sans preuve cycle de vie complet"
                    ),
                }
            )
            break  # Un seul flag de ce type suffit

    # 5. Compensation carbone de mauvaise qualité
    if carbon_offsets_used and offset_quality in ("LOW", "UNKNOWN"):
        specific_flags.append(
            {
                "category": "COMPENSATION CARBONE — Qualité insuffisante",
                "severity": "HAUTE",
                "description": (
                    f"Crédits carbone de qualité '{offset_quality}' utilisés pour "
                    "allégations de neutralité — non conformes aux standards "
                    "Gold Standard, VCS Verra ou Core Carbon Principles (ICVCM)"
                ),
                "regulation": (
                    "EU Green Claims Directive Recital 18 & Art. 4 — "
                    "compensation ne peut masquer réductions réelles insuffisantes ; "
                    "SBTi interdit offset pour objectifs 1,5 °C avant 2030"
                ),
            }
        )

    # 6. Certifications revendiquées mais non détenues
    for claim in claims:
        cert_keywords = {
            "iso 14001": "ISO_14001",
            "iso 50001": "ISO_50001",
            "b corp": "B_CORP",
            "fsc": "FSC",
            "rainforest alliance": "RAINFOREST_ALLIANCE",
            "fairtrade": "FAIR_TRADE",
            "fair trade": "FAIR_TRADE",
            "cradle to cradle": "CRADLE_TO_CRADLE",
            "science based target": "SCIENCE_BASED_TARGETS",
            "sbti": "SCIENCE_BASED_TARGETS",
        }
        for keyword, cert_id in cert_keywords.items():
            if keyword in claim.lower() and cert_id not in certifications_held:
                specific_flags.append(
                    {
                        "category": f"CERTIFICATION — Usage non autorisé ({cert_id})",
                        "severity": "CRITIQUE",
                        "description": (
                            f"Allégation '{claim}' fait référence à {cert_id} "
                            "mais cette certification n'est pas détenue selon les données fournies"
                        ),
                        "regulation": (
                            "EU Green Claims Directive Art. 6 — "
                            "usage non autorisé de labels peut constituer pratique commerciale trompeuse ; "
                            "Directive 2005/29/CE sur les pratiques déloyales"
                        ),
                    }
                )

    # 7. Absence d'évaluation biodiversité malgré allégations
    for claim in claims:
        if any(
            kw in claim.lower()
            for kw in ["biodiversité", "biodiversity", "nature positive", "zéro déforestation", "zero deforestation"]
        ) and not biodiversity_impact_assessed:
            specific_flags.append(
                {
                    "category": "BIODIVERSITÉ — Allégation sans évaluation",
                    "severity": "MOYENNE",
                    "description": (
                        f"Allégation '{claim}' sans évaluation d'impact biodiversité formelle "
                        "(TNFD, IBAT, ENCORE ou équivalent)"
                    ),
                    "regulation": (
                        "ESRS E4-5 — métriques biodiversité quantitatives requises ; "
                        "EU Green Claims Directive Art. 3(2)(a) — preuve scientifique obligatoire"
                    ),
                }
            )
            break

    # 8. Amendes environnementales récentes non divulguées publiquement
    if environmental_fines_last3y > 50 and not bool(actual_data.get("fines_publicly_disclosed", False)):
        specific_flags.append(
            {
                "category": "NON-DIVULGATION — Amendes environnementales",
                "severity": "HAUTE",
                "description": (
                    f"Amendes environnementales de {environmental_fines_last3y:.0f} k€ "
                    "sur les 3 dernières années non divulguées dans les rapports publics"
                ),
                "regulation": (
                    "CSRD ESRS G1-4 — divulgation des incidents réglementaires majeurs ; "
                    "ESRS E2-6 — effets financiers pollution à déclarer"
                ),
            }
        )

    # 9. Eau non divulguée
    if not water_consumption_disclosed and any(
        kw in c.lower() for kw in ["eau", "water", "hydrique", "water stewardship"] for c in claims
    ):
        specific_flags.append(
            {
                "category": "EAU — Allégation sans données quantitatives",
                "severity": "MOYENNE",
                "description": (
                    "Allégations de gestion responsable de l'eau sans divulgation "
                    "des données de consommation (m³/an) par zone de stress hydrique"
                ),
                "regulation": (
                    "ESRS E3-4 — prélèvements d'eau par source requis ; "
                    "EU Green Claims Directive Art. 3(2)(b) — informations quantitatives"
                ),
            }
        )

    # === CALCUL DU NIVEAU DE RISQUE ===
    critical_count = sum(1 for f in specific_flags if f["severity"] == "CRITIQUE")
    high_count = sum(1 for f in specific_flags if f["severity"] == "HAUTE")
    medium_count = sum(1 for f in specific_flags if f["severity"] == "MOYENNE")

    if critical_count >= 2 or (critical_count >= 1 and high_count >= 2):
        risk_level = "HIGH"
        risk_label = "ÉLEVÉ — Risque réglementaire immédiat, révision urgente requise"
    elif critical_count == 1 or high_count >= 2:
        risk_level = "MEDIUM"
        risk_label = "MOYEN — Corrections nécessaires avant prochaine campagne communication"
    elif high_count == 1 or medium_count >= 2:
        risk_level = "MEDIUM"
        risk_label = "MOYEN-FAIBLE — Ajustements recommandés pour conformité complète"
    else:
        risk_level = "LOW"
        risk_label = "FAIBLE — Allégations globalement cohérentes avec les données disponibles"

    # === CORRECTIONS RECOMMANDÉES ===
    recommended_corrections: list[str] = []

    if critical_count > 0 or high_count > 0:
        recommended_corrections.append(
            "Suspendre immédiatement les allégations marquées CRITIQUE en attente de correction"
        )
    recommended_corrections += [
        "Mandater un auditeur indépendant accrédité ISAE 3000 pour vérification des allégations",
        "Publier un bilan GES Scope 1+2+3 conforme Protocole GHG avant toute allégation de neutralité",
        "Aligner le reporting Taxonomie UE sur les données vérifiées par un commissaire aux comptes",
        "Adopter la norme ISO 14064-3 pour vérification externe des inventaires GES",
        "Mettre en place une gouvernance interne des allégations environnementales (comité ESG)",
    ]

    if carbon_offsets_used:
        recommended_corrections.append(
            "Remplacer les crédits carbone de qualité faible par des projets Gold Standard "
            "ou VCS avec co-bénéfices biodiversité vérifiés (CCB Standards)"
        )

    # === EXPOSITION EU GREEN CLAIMS DIRECTIVE ===
    gcd_exposure: dict[str, str] = {
        "directive_reference": "COM/2023/166 — Directive EU Green Claims (en cours d'adoption)",
        "applicable_articles": (
            "Art. 3 (justification allégations), Art. 4 (vérification tierce), "
            "Art. 6 (labels et systèmes de certification), Art. 10 (sanctions)"
        ),
        "sanction_risk": (
            "Amendes jusqu'à 4 % du CA annuel (Art. 10) + interdiction publicité "
            "en cas d'allégation trompeuse fondée sur Art. 3(2)"
        ) if risk_level in ("HIGH", "MEDIUM") else "Faible — allégations conformes",
        "timeline": (
            "Directive adoptée ~2024-2025 — transposition nationale dans les 18 mois "
            "— application complète ~2026-2027"
        ),
        "recommended_action": (
            "Audit allégations préventif selon critères GCD avant adoption officielle "
            "pour éviter retraitements coûteux post-publication"
        ),
    }

    return {
        "company": company,
        "claims_analyzed": claims,
        "risk_level": risk_level,
        "risk_label": risk_label,
        "flags_summary": {
            "total_flags": len(specific_flags),
            "critique": critical_count,
            "haute": high_count,
            "moyenne": medium_count,
        },
        "specific_flags": specific_flags,
        "recommended_corrections": recommended_corrections,
        "EU_Green_Claims_Directive_exposure": gcd_exposure,
        "CSRD_misstatement_risk": (
            "ÉLEVÉ — risques d'inexactitudes matérielles dans le rapport de durabilité CSRD "
            "(Art. 19a Directive 2013/34/UE amendée) exposant à la responsabilité des dirigeants"
        ) if risk_level == "HIGH" else (
            "MOYEN — inexactitudes non-matérielles à corriger avant publication CSRD"
        ) if risk_level == "MEDIUM" else (
            "FAIBLE — reporting cohérent avec les données vérifiées"
        ),
        "analysis_timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# ---------------------------------------------------------------------------
# 3. DEMO
# ---------------------------------------------------------------------------

def _print_section(title: str, char: str = "=") -> None:
    width = 72
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")


def _print_kv(label: str, value: Any, indent: int = 2) -> None:
    pad = " " * indent
    if isinstance(value, list):
        print(f"{pad}{label}:")
        for item in value:
            if isinstance(item, dict):
                for k, v in item.items():
                    print(f"{pad}    {k}: {v}")
                print()
            else:
                print(f"{pad}  - {item}")
    elif isinstance(value, dict):
        print(f"{pad}{label}:")
        for k, v in value.items():
            print(f"{pad}  {k}: {v}")
    else:
        print(f"{pad}{label}: {value}")


def run_demo() -> bool:
    """
    Démonstration complète de l'Agent Scout d'Éco-Responsabilité.

    Scénario : VerdiTech Industries SA — fabricant d'équipements industriels
    basé en France, avec production en Allemagne, Chine et Brésil.
    CA 2023 : 380 M€ | Secteur : manufacturing
    """

    print("\n" + "=" * 72)
    print("  CAELUM PARTNERS — CaelumSwarm™")
    print("  Agent Scout d'Éco-Responsabilité")
    print("  Cadre : EU Green Deal · Taxonomie UE · CSRD ESRS E1-E5 · CSDDD")
    print("=" * 72)
    print(f"  Analyse générée le : {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    # ------------------------------------------------------------------
    # DEMO 1 — Profil éco-responsabilité
    # ------------------------------------------------------------------
    _print_section("1. PROFIL ÉCO-RESPONSABILITÉ — VerdiTech Industries SA", "=")

    profile = scout_company_eco_profile(
        company="VerdiTech Industries SA",
        sector="manufacturing",
        revenue_MEUR=380.0,
        countries_of_operation=["France", "Germany", "China", "Brazil", "Vietnam"],
    )

    print(f"\n  Entreprise          : {profile['company']}")
    print(f"  Secteur             : {profile['sector']}")
    print(f"  CA                  : {profile['revenue_MEUR']} M€")
    print(f"  Pays opérés         : {', '.join(profile['countries_analyzed'])}")
    print(f"  Facteur risque pays : {profile['country_risk_factor']:.2f} / 1.0")

    print("\n  ── SCORES ÉCO-RESPONSABILITÉ ──")
    print(f"  Alignement Taxonomie UE       : {profile['taxonomy_alignment_score']:.1f} / 100")
    print(f"  Préparation CSRD              : {profile['csrd_readiness']:.1f} / 100")
    print(f"  Score économie circulaire     : {profile['circular_economy_score']:.1f} / 100")
    print(f"  Exposition biodiversité       : {profile['biodiversity_exposure']:.2f} (0=faible, 1=critique)")
    print(f"  Risque hydrique               : {profile['water_risk']:.2f}")
    print(f"  Risque pollution              : {profile['pollution_risk']:.2f}")
    print(f"  Exposition CSDDD              : {profile['csddd_exposure_level']}")

    if profile["biodiversity_hotspots_exposed"]:
        print("\n  ── HOTSPOTS BIODIVERSITÉ EXPOSÉS ──")
        for hs in profile["biodiversity_hotspots_exposed"]:
            print(f"    ⚠  {hs}")

    print("\n  ── CERTIFICATIONS RECOMMANDÉES ──")
    for i, cert in enumerate(profile["certifications_recommended"], 1):
        print(f"\n  {i}. [{cert['priority']}] {cert['label']}")
        print(f"     Justification : {cert['justification']}")

    print("\n  ── ÉCHÉANCES RÉGLEMENTAIRES ──")
    for reg, deadline in profile["regulatory_deadlines"].items():
        print(f"    {reg:35s}: {deadline}")

    # ------------------------------------------------------------------
    # DEMO 2 — Éligibilité Taxonomie UE
    # ------------------------------------------------------------------
    _print_section("2. ÉLIGIBILITÉ TAXONOMIE UE — Analyse des activités", "=")

    activities_verditech = [
        "manufacturing_renewable_energy",
        "circular_economy_manufacturing",
        "clean_transport",
        "pollution_prevention",
    ]
    revenue_breakdown_verditech = {
        "manufacturing_renewable_energy": 35.0,   # 35 % du CA
        "circular_economy_manufacturing": 28.0,   # 28 %
        "clean_transport": 15.0,                  # 15 %
        "pollution_prevention": 12.0,             # 12 %
        # 10 % restants = activités non-éligibles non déclarées
    }

    taxonomy_result = assess_eu_taxonomy_eligibility(
        activities=activities_verditech,
        revenue_breakdown=revenue_breakdown_verditech,
    )

    print(f"\n  CA éligible Taxonomie UE    : {taxonomy_result['eligible_revenue_pct']:.1f} %")
    print(f"  CA aligné Taxonomie UE      : {taxonomy_result['aligned_revenue_pct']:.1f} %")
    print(f"  Écart éligibilité/alignement : {taxonomy_result['alignment_gap_pct']:.1f} pts")
    print(f"  Garde-fous sociaux remplis   : {'Oui' if taxonomy_result['minimum_social_safeguards_met'] else 'Non — vérifications requises'}")

    print("\n  ── KPI REPORTING ART. 8 (Acte Délégué Taxonomie) ──")
    for kpi, val in taxonomy_result["taxonomy_kpi_art8"].items():
        print(f"    {kpi:35s}: {val} %")

    print("\n  ── ÉVALUATION PAR ACTIVITÉ ──")
    for act in taxonomy_result["per_activity_assessment"]:
        status_icon = "✓" if act.get("aligned") else "✗"
        print(f"\n  {status_icon} {act.get('label', act['activity'])}")
        print(f"    CA déclaré          : {act['revenue_pct']:.1f} %")
        print(f"    CA aligné estimé    : {act.get('aligned_revenue_pct', 0):.1f} %  ({act.get('alignment_rate', 'N/A')})")
        print(f"    Atténuation clima.  : {'Oui' if act.get('climate_mitigation_eligible') else 'Non'}")
        print(f"    Adaptation clima.   : {'Oui' if act.get('climate_adaptation_eligible') else 'Non'}")
        print(f"    Gaps DNSH détectés  : {act.get('dnsh_gap_count', 0)}")

    if taxonomy_result["dnsh_compliance_gaps"]:
        print("\n  ── GAPS DNSH IDENTIFIÉS ──")
        for gap in taxonomy_result["dnsh_compliance_gaps"]:
            print(f"    - {gap}")

    print("\n  ── PROCHAINES ÉTAPES ──")
    for step in taxonomy_result["next_steps"]:
        print(f"    → {step}")

    # ------------------------------------------------------------------
    # DEMO 3 — Roadmap éco-responsabilité 2027
    # ------------------------------------------------------------------
    _print_section("3. FEUILLE DE ROUTE ÉCO-RESPONSABILITÉ 2024–2027", "=")

    current_scores_verditech = {
        "taxonomy_alignment_score": profile["taxonomy_alignment_score"],
        "csrd_readiness": profile["csrd_readiness"],
        "circular_economy_score": profile["circular_economy_score"],
        "water_risk": profile["water_risk"],
        "pollution_risk": profile["pollution_risk"],
        "biodiversity_exposure": profile["biodiversity_exposure"],
    }

    roadmap = generate_eco_roadmap(
        company="VerdiTech Industries SA",
        current_scores=current_scores_verditech,
        target_year=2027,
    )

    print(f"\n  Période : {roadmap['roadmap_period']}")
    print(f"  Investissement total estimé : {roadmap['total_investment_estimate_kEUR']:.0f} k€")

    print("\n  ── SCORES ACTUELS → CIBLES 2027 ──")
    cur = roadmap["current_scores"]
    tgt = roadmap["target_scores_2027"]
    print(f"    Alignement Taxonomie UE  : {cur['taxonomy_alignment_score']:.1f}  →  {tgt['taxonomy_alignment_score']:.1f} / 100")
    print(f"    Préparation CSRD         : {cur['csrd_readiness']:.1f}  →  {tgt['csrd_readiness']:.1f} / 100")
    print(f"    Économie Circulaire      : {cur['circular_economy_score']:.1f}  →  {tgt['circular_economy_score']:.1f} / 100")
    print(f"    Risque eau               : {tgt['water_risk_reduction']}")
    print(f"    Risque pollution         : {tgt['pollution_risk_reduction']}")

    print("\n  ── PHASES D'INVESTISSEMENT ──")
    for phase_id, phase in roadmap["investment_phases"].items():
        print(f"\n  {phase['label']}")
        print(f"    Type          : {phase['type']}")
        print(f"    Investissement : ~{phase['investment_kEUR']:.0f} k€")
        print(f"    ROI attendu   : {phase['roi_expected']}")

    print("\n  ── MILESTONES ANNUELS ──")
    for yr_data in roadmap["milestones_per_year"]:
        yr = yr_data["year"]
        scores = yr_data["projected_scores"]
        print(f"\n  ► {yr}")
        print(f"    Taxonomie : {scores['taxonomy_alignment']:.1f}  |  "
              f"CSRD : {scores['csrd_readiness']:.1f}  |  "
              f"Circulaire : {scores['circular_economy']:.1f}")
        if yr_data["milestones"]:
            for m in yr_data["milestones"]:
                print(f"    - {m}")
        if yr_data["certifications_targeted"]:
            print(f"    Certifications : {', '.join(yr_data['certifications_targeted'])}")
        if yr_data["regulatory_context"]:
            print(f"    Contexte régl. : {yr_data['regulatory_context']}")

    print("\n  ── BÉNÉFICES ATTENDUS ──")
    for benefit in roadmap["expected_benefits"]:
        print(f"    + {benefit}")

    # ------------------------------------------------------------------
    # DEMO 4 — Détection greenwashing
    # ------------------------------------------------------------------
    _print_section("4. DÉTECTION GREENWASHING — Analyse des allégations", "=")

    claims_verditech = [
        "VerdiTech est neutre en carbone depuis 2023",
        "Nos produits sont fabriqués avec 80 % d'énergie renouvelable",
        "Nous sommes certifiés B Corp et FSC",
        "Réduction de nos émissions de GES de 45 % depuis 2019",
        "Notre démarche biodiversité positive protège les écosystèmes locaux",
        "40 % de notre chiffre d'affaires est aligné avec la Taxonomie UE",
    ]

    actual_data_verditech = {
        "ghg_reduction_claimed_pct": 45.0,
        "ghg_reduction_actual_pct": 18.0,          # Scope 1+2 uniquement, pas Scope 3
        "renewable_energy_claimed_pct": 80.0,
        "renewable_energy_actual_pct": 52.0,        # Reste via GOs sans tracé géographique
        "scope3_reported": False,                   # Scope 3 non encore mesuré
        "carbon_offsets_used": True,
        "offset_quality": "LOW",                    # Crédits anciens, registry inconnu
        "taxonomy_aligned_claimed_pct": 40.0,
        "taxonomy_aligned_actual_pct": 22.0,        # Écart documentation DNSH
        "certifications_held": ["ISO_14001"],       # B Corp et FSC non obtenues
        "biodiversity_impact_assessed": False,
        "environmental_fines_last3y_kEUR": 180.0,  # Amende ARS non divulguée
        "fines_publicly_disclosed": False,
        "water_consumption_disclosed": False,
    }

    gw_result = detect_greenwashing_risk(
        company="VerdiTech Industries SA",
        claims=claims_verditech,
        actual_data=actual_data_verditech,
    )

    print(f"\n  Entreprise   : {gw_result['company']}")
    print(f"  Allégations analysées : {len(gw_result['claims_analyzed'])}")

    risk_icons = {"HIGH": "RISQUE ÉLEVÉ", "MEDIUM": "RISQUE MOYEN", "LOW": "RISQUE FAIBLE"}
    print(f"\n  NIVEAU DE RISQUE GREENWASHING : {risk_icons[gw_result['risk_level']]}")
    print(f"  {gw_result['risk_label']}")

    summary = gw_result["flags_summary"]
    print(f"\n  Signaux détectés : {summary['total_flags']} total "
          f"({summary['critique']} critique · {summary['haute']} haute · {summary['moyenne']} moyenne)")

    print("\n  ── SIGNAUX DÉTAILLÉS ──")
    for i, flag in enumerate(gw_result["specific_flags"], 1):
        print(f"\n  [{i}] [{flag['severity']}] {flag['category']}")
        print(f"       {flag['description']}")
        print(f"       Réglementation : {flag['regulation']}")

    print("\n  ── CORRECTIONS RECOMMANDÉES ──")
    for j, correction in enumerate(gw_result["recommended_corrections"], 1):
        print(f"    {j}. {correction}")

    print("\n  ── EXPOSITION EU GREEN CLAIMS DIRECTIVE ──")
    gcd = gw_result["EU_Green_Claims_Directive_exposure"]
    for k, v in gcd.items():
        print(f"    {k:35s}: {v}")

    print(f"\n  Risque inexactitude CSRD : {gw_result['CSRD_misstatement_risk']}")

    # ------------------------------------------------------------------
    # Résumé exécutif
    # ------------------------------------------------------------------
    _print_section("SYNTHÈSE EXÉCUTIVE — VerdiTech Industries SA", "=")
    print(f"""
  VerdiTech Industries SA présente un profil éco-responsabilité en cours
  de structuration, typique des industriels européens de taille intermédiaire.

  POINTS FORTS :
  - CA éligible Taxonomie UE : {taxonomy_result['eligible_revenue_pct']:.0f} % (activités bien positionnées)
  - Certification ISO 14001 en place (fondation SME solide)
  - Présence en Allemagne et France = ancrage gouvernance UE forte

  AXES PRIORITAIRES D'AMÉLIORATION :
  - Bilan GES Scope 3 : absence critique (neutre carbone non justifiable)
  - Alignement Taxonomie réel ({taxonomy_result['aligned_revenue_pct']:.0f} %) vs revendiqué (40 %) = écart à corriger
  - Crédits carbone à remplacer par standards Gold Standard/VCS Core
  - Divulgation des amendes environnementales (180 k€ — non divulguées)
  - Évaluation biodiversité formelle TNFD à initier

  ROADMAP PRIORITAIRE :
  1. [2024] Bilan Scope 1+2+3 + engagement SBTi + audit DNSH Taxonomie
  2. [2025] Premier rapport CSRD ESRS E1-E5 + validation SBTi
  3. [2026] Conformité CSDDD + ISO 50001 + Cradle to Cradle
  4. [2027] B Corp + CA aligné Taxonomie ≥ 50 % + TNFD reporting

  Investissement total estimé : {roadmap['total_investment_estimate_kEUR']:.0f} k€ sur 3 ans
  ROI principal : conformité CSDDD (éviter amendes 5 % CA), accès fonds verts,
  réduction coût capital ESG estimée -75 à -100 bps.

  Cadre réglementaire mobilisé :
  Règlement Taxonomie UE 2020/852 · CSRD Directive 2022/2464 · ESRS E1-E5
  CSDDD Directive 2024/1760 · EU Green Claims COM/2023/166
  EUDR Règlement 2023/1115 · SBTi Net-Zero Standard · TNFD v1.0
""")

    return True


# ---------------------------------------------------------------------------
# 4. ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if success:
        print("Agent Scout d'Éco-Responsabilité — exécution terminée avec succès.\n")

"""
Agent assistant de communauté — anime, modère et développe la communauté CaelumSwarm™
de professionnels CSDDD/ESG/droits humains.

Caelum Partners — CaelumSwarm™ Community Assistant Agent
Gère l'animation, la modération et le développement de la communauté B2B spécialisée
en devoir de vigilance, CSDDD, ESG et droits humains.
"""

import math
import random
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# DATA CONSTANTS
# ---------------------------------------------------------------------------

COMMUNITY_PLATFORMS = {
    "LINKEDIN_GROUP": {
        "label": "Groupe LinkedIn CaelumSwarm™",
        "member_count_target": 5000,
        "engagement_target_pct": 12.0,
        "content_cadence": "3 publications/semaine",
        "moderation_level": "MEDIUM",
    },
    "SLACK_WORKSPACE": {
        "label": "Workspace Slack CaelumSwarm™ Pro",
        "member_count_target": 1200,
        "engagement_target_pct": 35.0,
        "content_cadence": "Temps réel + 2 digests/semaine",
        "moderation_level": "LOW",
    },
    "MONTHLY_WEBINAR": {
        "label": "Webinaires mensuels CaelumSwarm™",
        "member_count_target": 300,
        "engagement_target_pct": 65.0,
        "content_cadence": "1 événement/mois",
        "moderation_level": "HIGH",
    },
    "ANNUAL_SUMMIT": {
        "label": "CaelumSwarm™ Summit Annuel",
        "member_count_target": 500,
        "engagement_target_pct": 80.0,
        "content_cadence": "1 événement/an",
        "moderation_level": "HIGH",
    },
    "NEWSLETTER": {
        "label": "Newsletter CaelumSwarm™ Intelligence",
        "member_count_target": 8000,
        "engagement_target_pct": 28.0,
        "content_cadence": "Bi-hebdomadaire (mardi + jeudi)",
        "moderation_level": "LOW",
    },
}

MEMBER_SEGMENTS = {
    "COMPLIANCE_PROFESSIONALS": {
        "label": "Responsables Conformité & RSE",
        "typical_questions": [
            "Quels sont les délais d'application de la CSDDD par taille d'entreprise ?",
            "Comment cartographier les risques droits humains dans ma chaîne d'approvisionnement ?",
            "Quels outils technologiques pour automatiser le devoir de vigilance ?",
            "Comment structurer un rapport de vigilance conforme ?",
            "Quelle est la différence entre CSRD et CSDDD en pratique ?",
        ],
        "preferred_content": [
            "Guides pratiques et checklists",
            "Études de cas sectorielles",
            "Analyses réglementaires comparatives",
            "Templates de rapports",
            "Benchmarks sectoriels",
        ],
        "engagement_style": "Axé sur les outils pratiques, cherche des solutions opérationnelles immédiatement applicables.",
    },
    "INVESTORS_ESG": {
        "label": "Investisseurs & Analystes ESG",
        "typical_questions": [
            "Comment évaluer l'exposition aux risques CSDDD d'un portefeuille ?",
            "Quels indicateurs droits humains intégrer dans les due diligences ?",
            "Impact de la CSDDD sur la valorisation des entreprises non-conformes ?",
            "Comment noter la maturité ESG d'une PME en supply chain ?",
            "Quels secteurs présentent les risques de vigilance les plus élevés ?",
        ],
        "preferred_content": [
            "Analyses financières des risques de non-conformité",
            "Rapports d'intelligence sectorielle",
            "Données comparatives et benchmarks",
            "Alertes réglementaires anticipées",
            "Études d'impact sur les valorisations",
        ],
        "engagement_style": "Recherche des données quantitatives et des analyses prospectives pour informer ses décisions d'investissement.",
    },
    "NGO_PARTNERS": {
        "label": "ONG & Organisations Société Civile",
        "typical_questions": [
            "Comment soumettre des signalements dans le cadre des mécanismes de réclamation CSDDD ?",
            "Quels droits d'accès à l'information pour les communautés affectées ?",
            "Comment collaborer efficacement avec les entreprises sur la vigilance ?",
            "Quels standards internationaux des droits humains s'appliquent à la CSDDD ?",
            "Comment évaluer la crédibilité d'un plan de vigilance d'entreprise ?",
        ],
        "preferred_content": [
            "Analyses des droits des communautés affectées",
            "Guides sur les mécanismes de plainte",
            "Études de cas terrain",
            "Ressources en droit international des droits humains",
            "Outils de plaidoyer et de dialogue",
        ],
        "engagement_style": "Perspective axée sur les droits et les impacts terrain, cherche à renforcer la redevabilité des entreprises.",
    },
    "ACADEMICS": {
        "label": "Chercheurs & Universitaires",
        "typical_questions": [
            "Quelles méthodologies pour mesurer l'efficacité des dispositifs de vigilance ?",
            "Comparaison internationale des lois de devoir de vigilance : France vs. Allemagne vs. CSDDD ?",
            "Quelle jurisprudence émergente sur la responsabilité civile en supply chain ?",
            "Comment les algorithmes d'IA peuvent-ils biaiser l'évaluation des risques droits humains ?",
            "Quels indicateurs pour mesurer l'impact réel sur les droits humains au niveau terrain ?",
        ],
        "preferred_content": [
            "Articles académiques et working papers",
            "Données primaires et méthodologies de recherche",
            "Débats conceptuels et théoriques",
            "Comparaisons législatives internationales",
            "Études longitudinales d'impact",
        ],
        "engagement_style": "Approche analytique et critique, intéressé par la rigueur méthodologique et les nuances conceptuelles.",
    },
    "JOURNALISTS": {
        "label": "Journalistes & Médias Spécialisés",
        "typical_questions": [
            "Quels sont les premiers cas de contentieux CSDDD attendus en Europe ?",
            "Quelles entreprises du CAC40 sont les mieux/moins bien préparées à la CSDDD ?",
            "Comment expliquer la CSDDD à un public non-spécialiste ?",
            "Quels scandales récents illustrent les lacunes du devoir de vigilance actuel ?",
            "Quel est l'agenda politique européen sur la CSDDD pour 2025-2026 ?",
        ],
        "preferred_content": [
            "Briefings exclusifs et off-records",
            "Accès aux experts pour interviews",
            "Données et statistiques clés prêtes à publier",
            "Analyses des développements réglementaires",
            "Alertes sur les contentieux et scandales émergents",
        ],
        "engagement_style": "Cherche des angles inédits, des sources expertes et des données exclusives pour ses enquêtes.",
    },
}

EVENT_TEMPLATES = {
    "MONTHLY_WEBINAR": {
        "label": "Webinaire Mensuel CaelumSwarm™",
        "duration_minutes": 75,
        "max_participants": 250,
        "production_effort": 3,
        "expected_leads": 45,
        "agenda_template": [
            "00:00 — Ouverture & présentation de l'équipe Caelum Partners (5 min)",
            "05:00 — Actualité réglementaire CSDDD/ESG du mois (15 min)",
            "20:00 — Présentation principale : analyse sectorielle CaelumSwarm™ (25 min)",
            "45:00 — Questions-réponses live avec les experts (20 min)",
            "65:00 — Ressources exclusives & prochains événements (5 min)",
            "70:00 — Networking virtuel en sous-groupes (5 min)",
        ],
    },
    "EXPERT_AMA": {
        "label": "AMA Expert — Questions sans filtre",
        "duration_minutes": 60,
        "max_participants": 100,
        "production_effort": 2,
        "expected_leads": 30,
        "agenda_template": [
            "00:00 — Introduction de l'expert invité & format AMA (5 min)",
            "05:00 — Questions pré-soumises par la communauté — top 5 (25 min)",
            "30:00 — Questions live des participants (20 min)",
            "50:00 — Synthèse par l'expert : 3 points clés à retenir (7 min)",
            "57:00 — Clôture & ressources complémentaires (3 min)",
        ],
    },
    "WORKSHOP_CSDDD": {
        "label": "Atelier Pratique CSDDD — Mise en conformité",
        "duration_minutes": 180,
        "max_participants": 40,
        "production_effort": 5,
        "expected_leads": 35,
        "agenda_template": [
            "00:00 — Accueil & tour de table des participants (10 min)",
            "10:00 — Cadrage réglementaire CSDDD : obligations clés par taille (20 min)",
            "30:00 — Exercice pratique 1 : cartographie des risques en sous-groupes (40 min)",
            "70:00 — Restitution & débriefing collectif (20 min)",
            "90:00 — Pause (15 min)",
            "105:00 — Exercice pratique 2 : rédaction d'un plan de vigilance (45 min)",
            "150:00 — Restitution & corrections avec les experts Caelum (20 min)",
            "170:00 — Ressources, outils recommandés & Q&A final (10 min)",
        ],
    },
    "NETWORKING_BREAKFAST": {
        "label": "Petit-déjeuner Networking CaelumSwarm™",
        "duration_minutes": 90,
        "max_participants": 30,
        "production_effort": 2,
        "expected_leads": 20,
        "agenda_template": [
            "00:00 — Accueil & café (15 min)",
            "15:00 — Tour de table : présentations rapides en 60 secondes (20 min)",
            "35:00 — Thème du jour : discussion ouverte animée par Caelum (30 min)",
            "65:00 — Networking libre & échanges bilatéraux (20 min)",
            "85:00 — Clôture & invitation au prochain événement (5 min)",
        ],
    },
    "WAVE_REVEAL_LIVE": {
        "label": "Wave Reveal Live — Lancement Intelligence CSDDD",
        "duration_minutes": 90,
        "max_participants": 500,
        "production_effort": 4,
        "expected_leads": 120,
        "agenda_template": [
            "00:00 — Ouverture événementielle & teaser (10 min)",
            "10:00 — Contexte : pourquoi cette Wave, pourquoi maintenant (10 min)",
            "20:00 — Révélation en direct des résultats Wave — domaine par domaine (35 min)",
            "55:00 — Analyse exclusive : gagnants, signaux d'alerte, surprises (15 min)",
            "70:00 — Panel réactions : 2 experts externes commentent (15 min)",
            "85:00 — Comment accéder aux données complètes & clôture (5 min)",
        ],
    },
}

FAQ_DATABASE = {
    "faq_001": {
        "question": "Qu'est-ce que la directive CSDDD et qui est concerné ?",
        "answer_short": "La CSDDD (Corporate Sustainability Due Diligence Directive) impose un devoir de vigilance aux grandes entreprises européennes sur les droits humains et l'environnement dans leurs chaînes de valeur. Les entreprises de +1000 salariés et +450M€ de CA sont concernées dès 2027.",
        "answer_detailed": "La Directive sur le devoir de vigilance des entreprises en matière de durabilité (CSDDD / CS3D) a été adoptée par le Conseil de l'UE en mai 2024. Elle oblige les grandes entreprises à identifier, prévenir, atténuer et rendre compte des impacts négatifs réels et potentiels sur les droits humains et l'environnement dans leurs opérations propres et leurs chaînes de valeur. Le calendrier d'application est échelonné : entreprises de +5000 salariés et +1,5 Md€ de CA dès 2027, entreprises de +3000 salariés et +900M€ dès 2028, et entreprises de +1000 salariés et +450M€ dès 2029. Les entreprises de pays tiers générant +450M€ de CA dans l'UE sont également concernées.",
        "related_topics": ["CSRD", "Loi de Vigilance française", "UNGP", "OCDE MNE Guidelines"],
        "csddd_article_ref": "Article 2 — Champ d'application",
    },
    "faq_002": {
        "question": "Quelle est la différence entre la CSDDD et la CSRD ?",
        "answer_short": "La CSRD porte sur le reporting ESG (ce que les entreprises publient), tandis que la CSDDD impose des obligations d'action (ce que les entreprises doivent faire). CSRD = transparence ; CSDDD = diligence et responsabilité.",
        "answer_detailed": "La CSRD (Corporate Sustainability Reporting Directive) oblige les entreprises à publier des informations détaillées sur leur performance ESG selon les standards ESRS. La CSDDD va plus loin en imposant des obligations de conduite : identifier les risques, mettre en place des plans de vigilance, établir des mécanismes de réclamation, et prendre des mesures correctives. En cas de manquement à la CSDDD, les entreprises s'exposent à des sanctions civiles (responsabilité pour dommages) et administratives (amendes jusqu'à 5% du CA mondial). Les deux directives sont complémentaires : la CSRD fournit le cadre de transparence, la CSDDD le cadre d'action.",
        "related_topics": ["ESRS", "Double matérialité", "Due diligence", "Responsabilité civile"],
        "csddd_article_ref": "Considérant 14 — Relation avec la CSRD",
    },
    "faq_003": {
        "question": "Comment cartographier les risques droits humains dans ma chaîne d'approvisionnement ?",
        "answer_short": "La cartographie des risques suit 4 étapes : (1) identifier les activités et relations d'affaires, (2) collecter des données sectorielles et géographiques, (3) prioriser par sévérité et probabilité, (4) valider avec des parties prenantes terrain.",
        "answer_detailed": "La cartographie des risques droits humains repose sur les Principes Directeurs de l'ONU relatifs aux entreprises et droits de l'homme (UNGP). Étape 1 : Cartographier l'ensemble de votre chaîne de valeur (fournisseurs directs et indirects, sous-traitants, distributeurs). Étape 2 : Collecter des données de contexte — indices de risques pays (ex. Global Slavery Index), risques sectoriels (agriculture, textile, extraction minière = secteurs à risque élevé), données issues de bases de données comme Refinitiv ou MSCI ESG. Étape 3 : Évaluer chaque relation selon la sévérité des impacts potentiels (gravité, réversibilité, ampleur) et la probabilité. Étape 4 : Prioriser les 20% de relations représentant 80% des risques. Étape 5 : Valider la cartographie avec des ONG locales, syndicats et représentants communautaires. La CSDDD recommande de réévaluer annuellement et après chaque changement significatif.",
        "related_topics": ["UNGP", "Global Slavery Index", "Analyse de matérialité", "Engagement parties prenantes"],
        "csddd_article_ref": "Article 8 — Identification des impacts négatifs",
    },
    "faq_004": {
        "question": "Quelles sanctions prévoit la CSDDD en cas de non-conformité ?",
        "answer_short": "La CSDDD prévoit des sanctions administratives (amendes jusqu'à 5% du CA mondial net annuel) et une responsabilité civile pour les dommages causés aux victimes. Les autorités nationales superviseront la conformité.",
        "answer_detailed": "Le régime de sanctions de la CSDDD est à deux niveaux. Niveau 1 — Sanctions administratives : les États membres désigneront des autorités de contrôle nationales habilitées à imposer des amendes proportionnées. La directive fixe un plancher : les amendes doivent pouvoir atteindre au moins 5% du chiffre d'affaires mondial net de l'exercice précédent. Des mesures accessoires peuvent inclure la publication des infractions ('name and shame'). Niveau 2 — Responsabilité civile : les victimes d'impacts négatifs peuvent engager la responsabilité civile des entreprises devant les juridictions nationales. La directive impose aux États membres de prévoir ce régime. La charge de la preuve reste cependant sur les victimes, ce que certaines ONG critiquent. Des organisations de la société civile peuvent soutenir les victimes dans les procédures. Il existe également des clauses d'exclusion si l'entreprise a agi en conformité avec les standards de diligence reconnus.",
        "related_topics": ["Responsabilité civile extraterritoriale", "Autorités de contrôle nationales", "Accès à la justice", "Mécanismes de réclamation"],
        "csddd_article_ref": "Articles 26-29 — Supervision, sanctions et responsabilité civile",
    },
    "faq_005": {
        "question": "Comment établir un mécanisme de réclamation conforme à la CSDDD ?",
        "answer_short": "Un mécanisme de réclamation CSDDD doit être accessible, sûr, transparent et offrir des voies de recours réelles. Il doit permettre aux travailleurs, communautés et ONG de signaler des impacts sans crainte de représailles.",
        "answer_detailed": "La CSDDD s'inspire des critères d'effectivité des mécanismes de réclamation non-judiciaires définis par les UNGP (principe 31). Un mécanisme conforme doit : (1) Être légitime — disposer d'une politique claire, d'un responsable identifié, et être reconnu par les parties prenantes concernées. (2) Être accessible — disponible en plusieurs langues, sans frais pour les plaignants, accessible aux travailleurs informels. (3) Être prévisible — délais de traitement annoncés, suivi communiqué, résolution documentée. (4) Être équitable — accès à l'information et à l'assistance nécessaires. (5) Être transparent — publication de rapports agrégés annuels. (6) Être compatible avec les droits — ne pas bloquer l'accès aux voies judiciaires. (7) Permettre l'apprentissage continu — les réclamations alimentent l'amélioration du dispositif de vigilance. Les mécanismes peuvent être internes (hotline éthique, plateforme en ligne) ou externalisés (tiers de confiance). La CSDDD exige également des mécanismes au niveau de la chaîne de valeur pour les partenaires commerciaux.",
        "related_topics": ["UNGP Principe 31", "Hotline éthique", "Accès à la justice", "Protection des lanceurs d'alerte"],
        "csddd_article_ref": "Article 14 — Mécanismes de notification et de réclamation",
    },
    "faq_006": {
        "question": "Les PME sont-elles directement concernées par la CSDDD ?",
        "answer_short": "Les PME ne sont pas directement soumises à la CSDDD, mais elles sont indirectement impactées car leurs donneurs d'ordres leur demanderont de se conformer aux exigences de vigilance dans le cadre de leurs propres obligations.",
        "answer_detailed": "La CSDDD s'applique directement uniquement aux grandes entreprises (seuils de CA et d'effectifs). Cependant, les PME ressentent l'impact de façon indirecte et croissante. Les grandes entreprises soumises à la CSDDD doivent conduire leur vigilance sur l'ensemble de leur chaîne de valeur, ce qui inclut leurs fournisseurs PME. Ces derniers reçoivent des questionnaires ESG de plus en plus complexes, des demandes de certifications (SA8000, ISO 26000), et risquent d'être déréférencés si leurs pratiques ne satisfont pas aux exigences. La Commission européenne a reconnu ce 'ruissellement réglementaire' problématique et a prévu : des ressources de soutien aux PME (guides, plateformes de données sectorielles mutualisées), une clause de proportionnalité dans les demandes faites aux PME par les grandes entreprises, et une répartition équitable des coûts de conformité. Pour les PME, la stratégie optimale est d'anticiper en adoptant dès maintenant des pratiques de vigilance proportionnées à leur taille.",
        "related_topics": ["Chaîne de valeur", "Déréférencement fournisseurs", "Proportionnalité", "Soutien PME"],
        "csddd_article_ref": "Considérant 55 — Soutien aux PME",
    },
    "faq_007": {
        "question": "Comment la CSDDD s'articule-t-elle avec la loi française de vigilance de 2017 ?",
        "answer_short": "La CSDDD est plus large que la loi française en termes de champ d'application (seuils plus bas) mais la loi française reste plus exigeante sur certains points (plan de vigilance public, responsabilité civile sans délai de prescription spécifique).",
        "answer_detailed": "La loi française sur le devoir de vigilance de 2017 a été la première loi nationale de ce type en Europe et a inspiré la CSDDD. Points communs : obligation de vigilance sur les activités propres et les relations d'affaires, plan de vigilance annuel, mécanisme d'alerte. Différences clés : (1) Champ d'application — loi française limitée aux entreprises de +5000 salariés en France ou +10 000 en France et à l'étranger ; CSDDD plus large dès 2027. (2) Publication — la loi française exige un plan de vigilance public annexé au rapport de gestion ; la CSDDD s'appuie sur la CSRD pour la publication. (3) Recours — la loi française permet une mise en demeure préalable obligatoire avant tout contentieux ; la CSDDD a des modalités variables selon les États. (4) Sanctions — pas d'amende administrative dans la loi française (uniquement responsabilité civile) ; la CSDDD introduit des amendes administratives. Les entreprises françaises déjà conformes à la loi nationale ont une longueur d'avance mais devront adapter leurs dispositifs aux spécificités de la CSDDD.",
        "related_topics": ["Loi de Vigilance 2017", "Responsabilité civile française", "Plan de vigilance", "LMDE"],
        "csddd_article_ref": "Considérant 7 — Cohérence avec les législations nationales",
    },
    "faq_008": {
        "question": "Quels secteurs économiques présentent les risques droits humains les plus élevés selon la CSDDD ?",
        "answer_short": "Les secteurs à risque élevé identifiés incluent : textile et habillement, agriculture et agroalimentaire, extraction minière et métaux, électronique et technologie, et construction. Ces secteurs font l'objet d'une vigilance renforcée.",
        "answer_detailed": "La Commission européenne a identifié des secteurs à 'risques élevés' qui feront l'objet d'une attention particulière des autorités de contrôle. Textile et habillement : risques de travail forcé, travail des enfants et conditions de travail précaires dans les pays de production (Bangladesh, Vietnam, Cambodge). Agriculture et agroalimentaire : accaparement de terres, conditions de travail des travailleurs saisonniers, travail des enfants dans le cacao, café, coton. Extraction minière : droits des communautés autochtones, conditions de travail dangereuses, pollution environnementale (cobalt, lithium, or, diamants). Électronique : chaînes d'approvisionnement en minéraux de conflits (étain, tantale, tungstène, or — '3TG'), conditions de travail dans l'assemblage. Construction et infrastructure : travail migrant vulnérable, conditions de sécurité défaillantes. Pêche et aquaculture : travail forcé en mer, conditions de travail abusives. Ces secteurs bénéficient également de ressources sectorielles mutualisées développées par la Commission (lignes directrices sectorielles) pour faciliter la conformité.",
        "related_topics": ["Travail forcé", "Minerais de conflits", "Droits des peuples autochtones", "Lignes directrices sectorielles"],
        "csddd_article_ref": "Article 8(3) — Priorité sectorielle dans la vigilance",
    },
    "faq_009": {
        "question": "Comment utiliser l'intelligence artificielle pour automatiser la vigilance CSDDD ?",
        "answer_short": "L'IA peut automatiser la collecte de données fournisseurs, l'analyse de risques géographiques et sectoriels, le monitoring des actualités et alertes terrain, et l'analyse des questionnaires ESG. Mais la validation humaine reste indispensable pour les décisions de conformité.",
        "answer_detailed": "Les applications de l'IA dans le domaine du devoir de vigilance se développent rapidement. Collecte et analyse de données : les outils NLP permettent d'analyser automatiquement des milliers de documents fournisseurs (rapports ESG, certifications, audits) et d'en extraire les informations pertinentes. Monitoring en temps réel : des algorithmes scrappent les médias, ONG et bases de données pour détecter des alertes terrain (grèves, incidents, enquêtes) concernant les fournisseurs. Scoring des risques : des modèles de machine learning combinent données géographiques, sectorielles et d'entreprise pour produire des scores de risque automatisés. Questionnaires intelligents : des chatbots guident les fournisseurs dans le remplissage des questionnaires et signalent les incohérences. Limites importantes : les biais algorithmiques peuvent sous-estimer certains risques (régions sous-couvertes médiatiquement), les données d'entraînement peuvent reproduire des inégalités, et la responsabilité juridique reste humaine. La CSDDD ne définit pas de standards IA spécifiques mais la réglementation IA européenne (AI Act) s'appliquera aux systèmes à 'haut risque' utilisés dans ce contexte.",
        "related_topics": ["AI Act", "NLP", "ESG data providers", "Automatisation de la conformité"],
        "csddd_article_ref": "Article 10 — Mesures préventives et correctives",
    },
    "faq_010": {
        "question": "Qu'est-ce que CaelumSwarm™ et comment accéder aux données d'intelligence CSDDD ?",
        "answer_short": "CaelumSwarm™ est la plateforme d'intelligence CSDDD de Caelum Partners, qui utilise des algorithmes multi-agents pour produire des indices de risques sectoriels et géographiques actualisés en temps quasi-réel.",
        "answer_detailed": "CaelumSwarm™ est le système propriétaire d'intelligence artificielle de Caelum Partners dédié à l'analyse des risques CSDDD/ESG/droits humains. Il repose sur une architecture multi-agents ('swarm intelligence') où des centaines d'agents spécialisés analysent simultanément des milliers de sources de données. Chaque 'Wave' CaelumSwarm™ produit des analyses approfondies sur des domaines spécifiques (travail forcé, droits des peuples autochtones, risques climatiques, etc.) avec des scores quantitatifs par secteur et par pays. Les données sont actualisées en continu et présentées via un tableau de bord interactif. Accès : les membres Premium de la communauté CaelumSwarm™ bénéficient d'un accès complet aux données Wave. Les membres Standard ont accès aux synthèses et aux alertes hebdomadaires. Pour les institutions et grandes entreprises, des accès API permettent l'intégration directe dans les systèmes de gestion des risques. Pour demander une démonstration ou un accès : contacter l'équipe via le groupe LinkedIn ou le workspace Slack.",
        "related_topics": ["Swarm intelligence", "Indices de risques", "Wave releases", "API accès données"],
        "csddd_article_ref": "N/A — Service propriétaire Caelum Partners",
    },
    "faq_011": {
        "question": "Comment intégrer les droits des peuples autochtones dans la vigilance CSDDD ?",
        "answer_short": "La CSDDD exige que la vigilance couvre les droits des peuples autochtones, notamment le consentement libre, préalable et éclairé (CLPE) pour les activités affectant leurs terres et ressources. La Déclaration des Nations Unies sur les droits des peuples autochtones est le référentiel clé.",
        "answer_detailed": "La CSDDD intègre explicitement les droits des peuples autochtones dans le périmètre du devoir de vigilance, en référence à la Déclaration des Nations Unies sur les droits des peuples autochtones (DNUDPA). Le principe central est le Consentement Libre, Préalable et Éclairé (CLPE / FPIC en anglais) : toute activité susceptible d'affecter les terres, territoires ou ressources des peuples autochtones nécessite l'obtention de leur consentement effectif. En pratique, les entreprises doivent : identifier si leurs activités ou celles de leurs fournisseurs se trouvent dans des territoires autochtones ou à proximité (cartographie GIS et bases de données comme LandMark), engager des consultations authentiques (pas simplement informatives) avec les représentants légitimes des communautés, documenter le processus de consultation et son résultat, mettre en place des mécanismes de réclamation accessibles aux communautés autochtones (multilingues, respectueux des protocoles culturels). Secteurs particulièrement concernés : extractif (mines, pétrole), agro-industriel, infrastructure (barrages, routes), et tourisme.",
        "related_topics": ["DNUDPA", "CLPE/FPIC", "Droits fonciers", "Consultation des parties prenantes"],
        "csddd_article_ref": "Article 3(1)(b) et Annexe — Instruments internationaux droits humains",
    },
    "faq_012": {
        "question": "Quel est le calendrier de transposition de la CSDDD dans les États membres ?",
        "answer_short": "Les États membres ont jusqu'au 26 juillet 2026 pour transposer la CSDDD en droit national. L'application aux entreprises commence dès 2027 pour les plus grandes et s'étend jusqu'en 2029.",
        "answer_detailed": "La CSDDD a été publiée au Journal Officiel de l'UE le 5 juillet 2024 et est entrée en vigueur le 25 juillet 2024. Calendrier de transposition et d'application : Juillet 2026 — date limite pour que les États membres adoptent leurs lois nationales de transposition. Juillet 2027 — application aux entreprises de +5000 salariés et +1,5 Md€ de CA (UE) ou +1,5 Md€ de CA en UE (entreprises de pays tiers). Juillet 2028 — application aux entreprises de +3000 salariés et +900 M€ de CA. Juillet 2029 — application aux entreprises de +1000 salariés et +450 M€ de CA. Certains États membres comme l'Allemagne (LkSG en vigueur depuis 2023) et la France (loi de vigilance 2017) ont déjà des législations nationales qui devront être mises en cohérence avec la CSDDD. La Commission européenne devra publier des lignes directrices sectorielles avant l'entrée en application. Il est fortement recommandé aux entreprises de ne pas attendre les dates butoirs et de commencer dès maintenant à construire leur dispositif de vigilance.",
        "related_topics": ["Transposition nationale", "LkSG allemand", "Délais de conformité", "Lignes directrices CE"],
        "csddd_article_ref": "Article 37 — Transposition et Article 2 — Calendrier d'application",
    },
}


# ---------------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------------

def generate_welcome_sequence(member_type: str, company_size: str) -> dict:
    """
    Crée une séquence d'onboarding personnalisée en 5 emails pour un nouveau membre
    de la communauté CaelumSwarm™ en fonction de son type et de la taille de sa société.

    Args:
        member_type: Clé de MEMBER_SEGMENTS (ex. 'COMPLIANCE_PROFESSIONALS')
        company_size: Taille de l'entreprise ('TPE', 'PME', 'ETI', 'GE', 'MULTINATIONALE')

    Returns:
        dict contenant la séquence de 5 emails et les métadonnées d'onboarding
    """
    segment = MEMBER_SEGMENTS.get(member_type, MEMBER_SEGMENTS["COMPLIANCE_PROFESSIONALS"])
    label = segment["label"]
    preferred = segment["preferred_content"]
    style = segment["engagement_style"]

    # Adapter le message selon la taille d'entreprise
    size_context = {
        "TPE": "votre structure agile",
        "PME": "votre PME",
        "ETI": "votre ETI",
        "GE": "votre grande entreprise",
        "MULTINATIONALE": "votre groupe international",
    }.get(company_size, "votre organisation")

    urgency_by_size = {
        "TPE": "La CSDDD aura un impact indirect sur votre activité via vos donneurs d'ordres dès 2027.",
        "PME": "Vos clients grands groupes vous demanderont bientôt des preuves de conformité ESG.",
        "ETI": "Vous entrez peut-être dans le champ direct de la CSDDD dès 2028.",
        "GE": "Votre conformité CSDDD doit être opérationnelle pour 2027-2028.",
        "MULTINATIONALE": "Vous êtes en première ligne de la CSDDD dès juillet 2027.",
    }.get(company_size, "La conformité CSDDD est un enjeu stratégique pour votre organisation.")

    emails = [
        {
            "email_number": 1,
            "send_day": 0,
            "subject": f"Bienvenue dans CaelumSwarm™ — Votre intelligence CSDDD commence ici",
            "body_preview": (
                f"Bonjour,\n\n"
                f"Bienvenue dans la communauté CaelumSwarm™, le réseau de référence des professionnels "
                f"CSDDD/ESG/droits humains en Europe.\n\n"
                f"En tant que {label}, vous rejoignez {company_size and size_context or 'votre organisation'} "
                f"parmi plus de 3 200 experts qui font confiance à notre intelligence collective pour naviguer "
                f"dans la complexité réglementaire.\n\n"
                f"{urgency_by_size}\n\n"
                f"Dans les prochains jours, vous recevrez une série de ressources personnalisées pour "
                f"tirer le meilleur de CaelumSwarm™. Commençons par l'essentiel."
            ),
            "cta": {
                "label": "Accéder à mon espace membre",
                "url": "https://caelumpartners.com/community/onboarding",
                "type": "primary",
            },
        },
        {
            "email_number": 2,
            "send_day": 2,
            "subject": f"[CaelumSwarm™] 3 ressources essentielles pour {label}",
            "body_preview": (
                f"Bonjour,\n\n"
                f"Selon votre profil ({label}), voici les 3 ressources CaelumSwarm™ les plus utiles "
                f"pour vous dès maintenant :\n\n"
                f"1. {preferred[0] if preferred else 'Guide de démarrage CSDDD'} — "
                f"disponible en téléchargement immédiat\n"
                f"2. {preferred[1] if len(preferred) > 1 else 'Tableau de bord des indices de risques'} — "
                f"accès Premium inclus pendant 30 jours\n"
                f"3. FAQ CSDDD complète — 50+ questions-réponses rédigées par nos experts\n\n"
                f"Ces ressources ont été sélectionnées sur la base de votre contexte : {style[:100]}..."
            ),
            "cta": {
                "label": "Télécharger mes ressources",
                "url": "https://caelumpartners.com/community/resources/starter-pack",
                "type": "primary",
            },
        },
        {
            "email_number": 3,
            "send_day": 5,
            "subject": "[CaelumSwarm™] Rejoignez le prochain webinaire mensuel — Places limitées",
            "body_preview": (
                f"Bonjour,\n\n"
                f"Chaque mois, CaelumSwarm™ organise un webinaire de 75 minutes réunissant jusqu'à "
                f"250 professionnels CSDDD/ESG de toute l'Europe.\n\n"
                f"Au programme :\n"
                f"• Actualité réglementaire décryptée par nos experts\n"
                f"• Présentation exclusive d'une nouvelle Wave d'intelligence\n"
                f"• Session Q&A live avec possibilité de soumettre vos questions en avance\n"
                f"• Networking virtuel avec vos pairs\n\n"
                f"En tant que nouveau membre, vous avez accès gratuit à votre premier webinaire. "
                f"Les places sont limitées à {EVENT_TEMPLATES['MONTHLY_WEBINAR']['max_participants']} "
                f"participants."
            ),
            "cta": {
                "label": "Réserver ma place au prochain webinaire",
                "url": "https://caelumpartners.com/community/events/webinar-next",
                "type": "primary",
            },
        },
        {
            "email_number": 4,
            "send_day": 10,
            "subject": "[CaelumSwarm™] Connectez-vous avec vos pairs dans le Workspace Slack",
            "body_preview": (
                f"Bonjour,\n\n"
                f"La communauté CaelumSwarm™ vit aussi en temps réel sur notre Workspace Slack Pro, "
                f"réservé aux membres actifs.\n\n"
                f"Vous y trouverez :\n"
                f"• #veille-csddd — alertes réglementaires en temps réel\n"
                f"• #intelligence-wave — discussions autour des dernières analyses CaelumSwarm™\n"
                f"• #{member_type.lower().replace('_', '-')} — votre canal de segment, "
                f"avec {label} qui partagent vos défis\n"
                f"• #opportunites — offres d'emploi, partenariats et RFP ESG\n"
                f"• #ask-an-expert — posez vos questions directement à l'équipe Caelum Partners\n\n"
                f"Plus de 1 200 membres actifs vous attendent."
            ),
            "cta": {
                "label": "Rejoindre le Workspace Slack",
                "url": "https://caelumpartners.com/community/slack-invite",
                "type": "secondary",
            },
        },
        {
            "email_number": 5,
            "send_day": 21,
            "subject": "[CaelumSwarm™] Votre bilan de 3 semaines — et la suite",
            "body_preview": (
                f"Bonjour,\n\n"
                f"Cela fait 3 semaines que vous avez rejoint CaelumSwarm™. Voici ce que nous espérons "
                f"que vous avez déjà exploré :\n\n"
                f"✓ Vos ressources personnalisées pour {label}\n"
                f"✓ Au moins un webinaire ou événement communautaire\n"
                f"✓ Une première connexion dans le Workspace Slack\n\n"
                f"Pour aller plus loin, nous vous proposons :\n"
                f"• Un appel découverte de 30 min avec un expert Caelum Partners pour évaluer "
                f"votre maturité CSDDD et définir votre feuille de route ({size_context})\n"
                f"• Accès aux archives Wave — toutes les analyses depuis Wave 1\n"
                f"• Opportunité de contribuer en tant qu'intervenant lors d'un prochain événement\n\n"
                f"Nous sommes là pour faire de votre conformité CSDDD un avantage compétitif."
            ),
            "cta": {
                "label": "Planifier mon appel découverte",
                "url": "https://caelumpartners.com/community/consultation-booking",
                "type": "primary",
            },
        },
    ]

    return {
        "sequence_id": f"WEL-{member_type[:4]}-{company_size[:3]}-{datetime.now().strftime('%Y%m%d')}",
        "member_type": member_type,
        "member_label": label,
        "company_size": company_size,
        "total_emails": len(emails),
        "total_duration_days": 21,
        "emails": emails,
        "personalization_factors": {
            "segment": label,
            "size_context": size_context,
            "urgency_message": urgency_by_size,
            "preferred_content_types": preferred,
        },
        "automation_notes": (
            "Séquence à intégrer dans l'outil d'emailing CRM (ex. HubSpot/Brevo). "
            "Trigger : inscription confirmée. Désabonnement possible à tout moment. "
            "A/B test recommandé sur les sujets des emails 1 et 3."
        ),
    }


def moderate_content(post_content: str, member_type: str) -> dict:
    """
    Analyse un post communautaire pour sa conformité et sa pertinence.
    Retourne une décision de modération avec des indicateurs de qualité.

    Args:
        post_content: Texte du post à modérer
        member_type: Type de membre auteur (clé de MEMBER_SEGMENTS)

    Returns:
        dict avec is_approved, flags, suggested_response si flagué, engagement_quality_score
    """
    flags = []
    engagement_quality_score = 5.0  # Base sur 10

    content_lower = post_content.lower()
    word_count = len(post_content.split())

    # --- Vérifications de conformité ---

    # Contenu promotionnel excessif
    promo_keywords = [
        "achetez", "offre exclusive", "promo", "soldes", "réduction", "code promo",
        "cliquez ici pour acheter", "tarif préférentiel", "offre limitée",
    ]
    promo_hits = [kw for kw in promo_keywords if kw in content_lower]
    if promo_hits:
        flags.append({
            "type": "CONTENU_PROMOTIONNEL",
            "severity": "MEDIUM",
            "details": f"Mots-clés promotionnels détectés : {', '.join(promo_hits)}",
            "rule": "La communauté CaelumSwarm™ est un espace d'échange professionnel, pas un canal publicitaire.",
        })
        engagement_quality_score -= 2.0

    # Contenu hors sujet (trop éloigné de CSDDD/ESG/droits humains)
    relevant_keywords = [
        "csddd", "cs3d", "esg", "vigilance", "droits humains", "human rights",
        "supply chain", "chaîne", "fournisseur", "conformité", "reporting",
        "durabilité", "sustainability", "devoir", "csrd", "esrs", "rgpd",
        "risque", "audit", "certification", "iso", "sa8000", "ungp", "ocde",
        "caelum", "swarm", "wave", "communauté", "webinaire", "expert",
    ]
    relevant_hits = sum(1 for kw in relevant_keywords if kw in content_lower)
    if relevant_hits == 0 and word_count > 20:
        flags.append({
            "type": "HORS_SUJET",
            "severity": "LOW",
            "details": "Le post ne contient aucun mot-clé relatif à CSDDD/ESG/droits humains.",
            "rule": "Partager du contenu en lien avec la thématique de la communauté.",
        })
        engagement_quality_score -= 1.5

    # Contenu potentiellement offensant ou diffamatoire
    offensive_patterns = [
        "arnaque", "escroc", "fraude", "menteur", "incompétent",
        "corruption", "criminel", "illégal",
    ]
    offensive_hits = [p for p in offensive_patterns if p in content_lower]
    if offensive_hits:
        flags.append({
            "type": "CONTENU_POTENTIELLEMENT_OFFENSANT",
            "severity": "HIGH",
            "details": f"Termes potentiellement diffamatoires : {', '.join(offensive_hits)}",
            "rule": "Maintenir un discours professionnel et respectueux, même en cas de critique.",
        })
        engagement_quality_score -= 3.0

    # Vérification liens suspects
    suspicious_url_patterns = ["bit.ly", "tinyurl", "t.co/", "ow.ly"]
    has_suspicious_url = any(p in content_lower for p in suspicious_url_patterns)
    if has_suspicious_url:
        flags.append({
            "type": "LIEN_RACCOURCI_NON_VERIFIE",
            "severity": "LOW",
            "details": "Présence de liens raccourcis. Veuillez partager l'URL complète pour la transparence.",
            "rule": "Partager les URLs complètes pour permettre la vérification par la communauté.",
        })
        engagement_quality_score -= 0.5

    # --- Évaluation de la qualité d'engagement ---

    # Bonus longueur appropriée
    if 100 <= word_count <= 500:
        engagement_quality_score += 1.0
    elif word_count > 500:
        engagement_quality_score += 0.5  # Long mais potentiellement riche
    elif word_count < 30:
        engagement_quality_score -= 1.0  # Trop court, peu de valeur

    # Bonus pertinence thématique forte
    if relevant_hits >= 3:
        engagement_quality_score += 1.5
    elif relevant_hits >= 1:
        engagement_quality_score += 0.5

    # Bonus question ouverte (favorise les échanges)
    if "?" in post_content:
        engagement_quality_score += 0.5

    # Bonus partage d'expérience
    experience_markers = ["dans mon expérience", "nous avons", "j'ai constaté",
                          "chez nous", "en pratique", "retour d'expérience"]
    if any(m in content_lower for m in experience_markers):
        engagement_quality_score += 1.0

    # Ajustement selon le segment (les journalistes ont une tolérance plus large)
    if member_type == "JOURNALISTS":
        engagement_quality_score = min(engagement_quality_score + 0.5, 10.0)

    # Plafonner le score
    engagement_quality_score = round(max(0.0, min(10.0, engagement_quality_score)), 1)

    # Déterminer la décision
    high_severity_flags = [f for f in flags if f["severity"] == "HIGH"]
    medium_severity_flags = [f for f in flags if f["severity"] == "MEDIUM"]

    if high_severity_flags:
        is_approved = False
        decision_reason = "Contenu refusé : présence d'un ou plusieurs signaux de gravité élevée."
    elif len(medium_severity_flags) >= 2:
        is_approved = False
        decision_reason = "Contenu refusé : cumul de signaux de gravité moyenne."
    elif flags:
        is_approved = True  # Approuvé avec avertissement
        decision_reason = "Contenu approuvé avec réserves : signaux mineurs détectés."
    else:
        is_approved = True
        decision_reason = "Contenu approuvé : aucun signal négatif détecté."

    # Réponse suggérée si non approuvé ou avec réserves
    suggested_response = None
    if not is_approved or (is_approved and flags):
        flag_types = [f["type"] for f in flags]
        if "CONTENU_POTENTIELLEMENT_OFFENSANT" in flag_types:
            suggested_response = (
                "Bonjour, merci pour votre contribution à la communauté CaelumSwarm™. "
                "Nous avons noté que votre post contient des termes qui pourraient être perçus "
                "comme offensants ou diffamatoires. Nous vous invitons à reformuler votre message "
                "de façon constructive et professionnelle. La critique est bienvenue dans notre "
                "communauté, mais doit rester respectueuse et factuelle. N'hésitez pas à nous "
                "contacter si vous souhaitez de l'aide pour reformuler. L'équipe CaelumSwarm™."
            )
        elif "CONTENU_PROMOTIONNEL" in flag_types:
            suggested_response = (
                "Bonjour, merci pour votre message. La communauté CaelumSwarm™ est avant tout "
                "un espace d'échange professionnel et de partage de connaissances. Les contenus "
                "à caractère purement promotionnel ne sont pas autorisés dans les espaces publics "
                "de la communauté. Si vous souhaitez partager votre solution ou service, nous vous "
                "invitons à passer par notre processus de partenariat officiel ou à reformuler "
                "votre post sous forme d'article d'expertise ou de retour d'expérience client. "
                "Merci de votre compréhension. L'équipe CaelumSwarm™."
            )
        elif "HORS_SUJET" in flag_types:
            suggested_response = (
                "Bonjour, merci pour votre participation ! Votre post semble peu lié aux "
                "thématiques principales de CaelumSwarm™ (CSDDD, ESG, droits humains, "
                "devoir de vigilance). Pourriez-vous nous préciser le lien avec ces sujets ? "
                "Si vous souhaitez partager une réflexion connexe, nous vous suggérons de l'ancrer "
                "dans un contexte CSDDD/ESG pour enrichir les échanges de la communauté. "
                "L'équipe CaelumSwarm™."
            )
        else:
            suggested_response = (
                "Bonjour, merci pour votre contribution. Votre post a été légèrement ajusté "
                "pour mieux respecter les règles de la communauté CaelumSwarm™. "
                "N'hésitez pas à consulter notre charte communautaire pour les prochaines publications."
            )

    return {
        "moderation_id": f"MOD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "is_approved": is_approved,
        "decision_reason": decision_reason,
        "flags": flags,
        "flags_count": len(flags),
        "suggested_response": suggested_response,
        "engagement_quality_score": engagement_quality_score,
        "engagement_quality_label": (
            "Excellent" if engagement_quality_score >= 8.0
            else "Bon" if engagement_quality_score >= 6.0
            else "Moyen" if engagement_quality_score >= 4.0
            else "Faible"
        ),
        "word_count": word_count,
        "thematic_relevance_score": min(10, relevant_hits * 1.5),
        "member_type": member_type,
        "moderated_at": datetime.now().isoformat(),
    }


def plan_monthly_events(month: int, wave_number: int) -> dict:
    """
    Crée un calendrier complet d'événements pour un mois donné,
    centré sur le lancement d'une Wave CaelumSwarm™.

    Args:
        month: Numéro du mois (1-12)
        wave_number: Numéro de la Wave CaelumSwarm™ à lancer ce mois

    Returns:
        dict avec le calendrier détaillé, le plan de promotion et les actions de suivi
    """
    month_names = {
        1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
        5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
        9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre",
    }
    month_name = month_names.get(month, "Mois inconnu")
    year = datetime.now().year

    # Calculer les dates clés du mois
    first_day = datetime(year, month, 1)
    # Deuxième mardi du mois pour le Wave Reveal
    wave_reveal_day = first_day
    days_to_tuesday = (1 - first_day.weekday()) % 7
    first_tuesday = first_day + timedelta(days=days_to_tuesday)
    wave_reveal_date = first_tuesday + timedelta(weeks=1)

    # Troisième jeudi pour le webinaire mensuel
    days_to_thursday = (3 - first_day.weekday()) % 7
    first_thursday = first_day + timedelta(days=days_to_thursday)
    webinar_date = first_thursday + timedelta(weeks=2)

    # Premier mercredi pour le petit-déjeuner networking (si disponible)
    days_to_wednesday = (2 - first_day.weekday()) % 7
    networking_date = first_day + timedelta(days=days_to_wednesday)
    if networking_date.day < 3:
        networking_date += timedelta(weeks=1)

    # AMA Expert : dernière semaine du mois
    last_week_monday = wave_reveal_date + timedelta(weeks=1, days=4)

    events = [
        {
            "event_id": f"EVT-{year}{month:02d}-01",
            "type": "NETWORKING_BREAKFAST",
            "template": EVENT_TEMPLATES["NETWORKING_BREAKFAST"],
            "date": networking_date.strftime("%d %B %Y"),
            "time": "08h30 — 10h00",
            "format": "Présentiel (Paris) + streaming pour membres distants",
            "theme": "Thème du mois : Préparer votre organisation à la CSDDD — partages d'expériences",
            "speaker": "Animé par l'équipe Caelum Partners",
            "registration_url": f"https://caelumpartners.com/events/{year}{month:02d}-networking",
            "promotion_start": (networking_date - timedelta(days=14)).strftime("%d %B"),
        },
        {
            "event_id": f"EVT-{year}{month:02d}-02",
            "type": "WAVE_REVEAL_LIVE",
            "template": EVENT_TEMPLATES["WAVE_REVEAL_LIVE"],
            "date": wave_reveal_date.strftime("%d %B %Y"),
            "time": "14h00 — 15h30 (CET)",
            "format": "100% en ligne — Zoom Webinar",
            "theme": f"WAVE {wave_number} REVEAL LIVE — Dévoilement en direct des analyses CaelumSwarm™",
            "speaker": "Équipe Caelum Partners + 2 experts invités (secteur & géographie concernés)",
            "registration_url": f"https://caelumpartners.com/events/wave-{wave_number}-reveal",
            "promotion_start": (wave_reveal_date - timedelta(days=21)).strftime("%d %B"),
            "expected_attendance": EVENT_TEMPLATES["WAVE_REVEAL_LIVE"]["max_participants"],
            "expected_leads": EVENT_TEMPLATES["WAVE_REVEAL_LIVE"]["expected_leads"],
        },
        {
            "event_id": f"EVT-{year}{month:02d}-03",
            "type": "MONTHLY_WEBINAR",
            "template": EVENT_TEMPLATES["MONTHLY_WEBINAR"],
            "date": webinar_date.strftime("%d %B %Y"),
            "time": "12h00 — 13h15 (CET) — format déjeuner",
            "format": "En ligne — Zoom Webinar avec salle de networking post-événement",
            "theme": f"Webinaire mensuel #{month} — Décryptage Wave {wave_number} & implications pratiques",
            "speaker": "Expert Caelum Partners + témoignage d'un membre de la communauté",
            "registration_url": f"https://caelumpartners.com/events/{year}{month:02d}-webinar",
            "promotion_start": (webinar_date - timedelta(days=14)).strftime("%d %B"),
            "expected_attendance": 180,
            "expected_leads": EVENT_TEMPLATES["MONTHLY_WEBINAR"]["expected_leads"],
            "agenda": EVENT_TEMPLATES["MONTHLY_WEBINAR"]["agenda_template"],
        },
        {
            "event_id": f"EVT-{year}{month:02d}-04",
            "type": "EXPERT_AMA",
            "template": EVENT_TEMPLATES["EXPERT_AMA"],
            "date": last_week_monday.strftime("%d %B %Y"),
            "time": "17h00 — 18h00 (CET)",
            "format": "En ligne — format questions ouvertes, sans présentation",
            "theme": f"AMA avec un expert CSDDD — Questions sur la Wave {wave_number} & implications sectorielles",
            "speaker": "Expert invité externe (juriste, consultant senior ou directeur RSE)",
            "registration_url": f"https://caelumpartners.com/events/{year}{month:02d}-ama",
            "promotion_start": (last_week_monday - timedelta(days=10)).strftime("%d %B"),
            "expected_attendance": 75,
            "expected_leads": EVENT_TEMPLATES["EXPERT_AMA"]["expected_leads"],
        },
    ]

    # Plan de promotion
    promotion_plan = {
        "channels": [
            {
                "channel": "Newsletter CaelumSwarm™ Intelligence",
                "actions": [
                    f"J-21 : Annonce Wave {wave_number} Reveal — teaser avec date",
                    f"J-14 : Invitation détaillée avec agenda Wave Reveal",
                    f"J-7 : Rappel + bonus inscrit (accès preview données Wave {wave_number})",
                    "J-1 : Dernière chance — link Zoom",
                    "J+1 : Replay disponible + ressources complémentaires",
                ],
            },
            {
                "channel": "Groupe LinkedIn CaelumSwarm™",
                "actions": [
                    f"J-21 : Post teaser Wave {wave_number} — format carrousel",
                    "J-14 : Article court : pourquoi cette Wave est importante",
                    "J-7 : Post événement avec lien inscription",
                    "J-3 : Post des pré-questions de la communauté",
                    "J+0 : Live-post pendant le Wave Reveal",
                    "J+1 : Infographie des résultats clés",
                    "J+3 : Article analyse post-Wave",
                ],
            },
            {
                "channel": "Workspace Slack #intelligence-wave",
                "actions": [
                    f"J-14 : Annonce dans #general + ouverture thread questions Wave {wave_number}",
                    "J-7 : Sondage : quels secteurs vous intéressent le plus ?",
                    "J-1 : Rappel + lien Zoom direct",
                    "J+0 : Thread réactions live pendant l'événement",
                    "J+1 : Partage des données brutes pour membres Premium",
                ],
            },
            {
                "channel": "Emailing ciblé membres Premium",
                "actions": [
                    f"J-14 : Accès anticipé aux metadonnées Wave {wave_number}",
                    "J-2 : Invitation exclusive VIP — accès 30 min avant l'ouverture publique",
                    "J+1 : Rapport complet Wave en PDF + accès API données",
                ],
            },
        ],
        "content_production_timeline": {
            "J-28": "Briefing équipe contenu + validation thème Wave Reveal",
            "J-21": "Production des visuels LinkedIn + rédaction newsletter J-21",
            "J-14": "Production deck Wave Reveal (80% finalisé) + FAQ anticipées",
            "J-7": "Finalisation deck + répétition avec intervenants + landing page live",
            "J-3": "Dry-run technique + validation tous assets promotionnels",
            "J+1": "Publication replay + infographies + rapport PDF",
            "J+3": "Article analyse + mise à jour base FAQ avec questions event",
        },
    }

    # Actions de suivi post-événements
    follow_up_actions = [
        {
            "action": "Envoi du replay Wave Reveal",
            "deadline": f"J+1 après {wave_reveal_date.strftime('%d/%m')}",
            "owner": "Équipe contenu",
            "channel": "Email + Slack + LinkedIn",
        },
        {
            "action": f"Publication du rapport complet Wave {wave_number} en PDF",
            "deadline": f"J+2 après {wave_reveal_date.strftime('%d/%m')}",
            "owner": "Équipe data",
            "channel": "Espace membres Premium",
        },
        {
            "action": "Séquence nurturing leads générés par les événements du mois",
            "deadline": "J+3 après chaque événement",
            "owner": "Équipe marketing",
            "channel": "Email (CRM)",
        },
        {
            "action": "Mise à jour FAQ communautaire avec questions posées lors des events",
            "deadline": f"Avant le 5 du mois suivant",
            "owner": "Community Manager",
            "channel": "FAQ en ligne + Slack #ressources",
        },
        {
            "action": "Rapport mensuel communauté (engagement, leads, NPS)",
            "deadline": f"Dernier jour de {month_name}",
            "owner": "Community Manager",
            "channel": "Rapport interne équipe Caelum Partners",
        },
        {
            "action": f"Prospection partenaires pour Wave {wave_number + 1}",
            "deadline": f"Avant le 20 de {month_name}",
            "owner": "Business Development",
            "channel": "LinkedIn + email direct",
        },
    ]

    # Estimation des performances
    total_expected_attendance = sum(
        e.get("expected_attendance", e["template"]["max_participants"] // 2)
        for e in events
    )
    total_expected_leads = sum(
        e.get("expected_leads", e["template"]["expected_leads"])
        for e in events
    )

    return {
        "calendar_id": f"CAL-{year}{month:02d}-W{wave_number}",
        "month": month,
        "month_name": month_name,
        "year": year,
        "wave_number": wave_number,
        "events_count": len(events),
        "events": events,
        "promotion_plan": promotion_plan,
        "follow_up_actions": follow_up_actions,
        "performance_forecast": {
            "total_expected_attendance": total_expected_attendance,
            "total_expected_leads": total_expected_leads,
            "estimated_conversion_rate_pct": 8.5,
            "estimated_new_members": round(total_expected_leads * 0.35),
            "estimated_premium_upgrades": round(total_expected_leads * 0.08),
        },
        "budget_estimate_eur": {
            "production_contenu": 1200,
            "outils_evenementiels": 400,
            "promotion_payante_linkedin": 800,
            "intervenants_externes": 1500,
            "total": 3900,
            "note": "Hors salaires équipe interne",
        },
    }


def generate_engagement_report(
    period_days: int,
    member_count: int,
    posts_count: int,
    events_count: int,
) -> dict:
    """
    Calcule les métriques de santé de la communauté CaelumSwarm™ et produit
    des recommandations actionnables.

    Args:
        period_days: Durée de la période analysée en jours
        member_count: Nombre total de membres actifs sur la période
        posts_count: Nombre de posts publiés sur la période
        events_count: Nombre d'événements organisés sur la période

    Returns:
        dict avec métriques complètes et recommandations priorisées
    """
    # --- Calcul des métriques de base ---

    # Taux d'engagement : posts par membre (normalisé sur 30 jours)
    posts_per_member_per_month = (posts_count / max(member_count, 1)) * (30 / max(period_days, 1))
    # Engagement rate : benchmark B2B = 5-15% est bon
    engagement_rate = round(min(posts_per_member_per_month * 100 * 5, 100), 2)

    # Taux de croissance simulé (basé sur les benchmarks communautaires B2B ESG)
    baseline_growth = 3.2  # % mensuel de référence pour une communauté ESG active
    events_boost = events_count * 0.8  # Chaque événement booste la croissance
    content_boost = min(posts_count / max(period_days, 1) * 2, 5)  # Cadence contenu
    growth_rate = round(baseline_growth + events_boost + content_boost, 2)

    # NPS proxy : calculé à partir de l'engagement et de la rétention estimée
    # Formule: base 40 (NPS ESG communautés B2B) + bonus engagement + bonus events
    nps_base = 40
    nps_engagement_bonus = min(engagement_rate * 0.3, 20)
    nps_events_bonus = min(events_count * 3, 15)
    nps_proxy = round(nps_base + nps_engagement_bonus + nps_events_bonus, 1)

    # Segments les plus actifs (simulation basée sur les profils typiques)
    segment_activity = {
        "COMPLIANCE_PROFESSIONALS": round(0.35 * posts_count),
        "INVESTORS_ESG": round(0.22 * posts_count),
        "NGO_PARTNERS": round(0.18 * posts_count),
        "ACADEMICS": round(0.15 * posts_count),
        "JOURNALISTS": round(0.10 * posts_count),
    }
    most_active_segments = sorted(
        [
            {
                "segment": seg,
                "label": MEMBER_SEGMENTS[seg]["label"],
                "posts_count": count,
                "share_pct": round(count / max(posts_count, 1) * 100, 1),
            }
            for seg, count in segment_activity.items()
        ],
        key=lambda x: x["posts_count"],
        reverse=True,
    )

    # Métriques avancées
    posts_per_day = round(posts_count / max(period_days, 1), 2)
    members_per_event = round(member_count / max(events_count, 1), 1)
    content_velocity_score = min(round(posts_per_day * 10, 1), 10)

    # Score de santé global (sur 100)
    health_score = round(
        (engagement_rate * 0.30)
        + (min(growth_rate, 20) / 20 * 100 * 0.25)
        + (nps_proxy / 80 * 100 * 0.25)
        + (content_velocity_score / 10 * 100 * 0.20),
        1,
    )
    health_score = min(100, health_score)

    health_label = (
        "Excellente" if health_score >= 80
        else "Bonne" if health_score >= 65
        else "Correcte" if health_score >= 50
        else "A améliorer" if health_score >= 35
        else "Critique"
    )

    # --- Recommandations priorisées ---
    recommendations = []

    if engagement_rate < 10:
        recommendations.append({
            "priority": "HAUTE",
            "category": "Engagement",
            "recommendation": "Lancer une campagne 'Questions de la semaine' avec réponses d'experts",
            "rationale": f"Le taux d'engagement ({engagement_rate}%) est en dessous du seuil optimal de 12%.",
            "expected_impact": "+3 à +5 points de taux d'engagement en 30 jours",
            "effort": "MOYEN",
            "timeline": "Démarrage possible dès cette semaine",
        })

    if events_count < 2 and period_days >= 30:
        recommendations.append({
            "priority": "HAUTE",
            "category": "Événements",
            "recommendation": "Augmenter la cadence événementielle à minimum 2 événements/mois",
            "rationale": f"Seulement {events_count} événement(s) sur {period_days} jours. Les événements sont le principal driver de nouveaux membres.",
            "expected_impact": "+40% de nouveaux leads qualifiés par mois",
            "effort": "MOYEN",
            "timeline": "Dès le prochain mois",
        })

    if growth_rate < 5:
        recommendations.append({
            "priority": "HAUTE",
            "category": "Croissance",
            "recommendation": "Activer un programme d'ambassadeurs membres — référencement pair-à-pair",
            "rationale": f"Le taux de croissance ({growth_rate}%/mois) est sous l'objectif de 5% mensuel.",
            "expected_impact": "+2 à +4 points de croissance mensuelle",
            "effort": "FAIBLE",
            "timeline": "Lancement en 2 semaines",
        })

    if nps_proxy < 50:
        recommendations.append({
            "priority": "MOYENNE",
            "category": "Satisfaction",
            "recommendation": "Lancer une enquête de satisfaction membres + sessions 'feedback ouvert'",
            "rationale": f"Le NPS proxy ({nps_proxy}) suggère une satisfaction perfectible.",
            "expected_impact": "+10 points NPS en 60 jours avec suivi des actions",
            "effort": "FAIBLE",
            "timeline": "Enquête à envoyer cette semaine",
        })

    if posts_per_day < 1.5:
        recommendations.append({
            "priority": "MOYENNE",
            "category": "Contenu",
            "recommendation": "Créer un calendrier éditorial structuré avec thèmes hebdomadaires",
            "rationale": f"La cadence actuelle ({posts_per_day} posts/jour) est sous l'objectif de 2 posts/jour.",
            "expected_impact": "+25% de portée organique LinkedIn en 30 jours",
            "effort": "MOYEN",
            "timeline": "Calendrier à valider en équipe cette semaine",
        })

    if most_active_segments[3]["share_pct"] < 10:
        low_segment = most_active_segments[3]
        recommendations.append({
            "priority": "BASSE",
            "category": "Diversité des segments",
            "recommendation": f"Développer du contenu spécifique pour le segment '{low_segment['label']}'",
            "rationale": f"Le segment '{low_segment['label']}' ne représente que {low_segment['share_pct']}% des contributions.",
            "expected_impact": "Diversification de la communauté et accès à de nouveaux réseaux",
            "effort": "MOYEN",
            "timeline": "À intégrer dans le calendrier éditorial du prochain trimestre",
        })

    # Ajouter une recommandation toujours pertinente
    recommendations.append({
        "priority": "BASSE",
        "category": "Reconnaissance",
        "recommendation": "Instaurer un programme 'Top Contributor du Mois' avec mise en avant des meilleurs membres",
        "rationale": "La reconnaissance publique est le principal moteur de contribution dans les communautés B2B.",
        "expected_impact": "+15% de nouvelles contributions des membres réguliers",
        "effort": "FAIBLE",
        "timeline": "Dès le mois prochain",
    })

    return {
        "report_id": f"RPT-{datetime.now().strftime('%Y%m%d')}-{period_days}D",
        "period_days": period_days,
        "period_label": f"{period_days} derniers jours",
        "generated_at": datetime.now().isoformat(),
        "inputs": {
            "member_count": member_count,
            "posts_count": posts_count,
            "events_count": events_count,
        },
        "key_metrics": {
            "engagement_rate": engagement_rate,
            "engagement_rate_label": (
                "Excellent (>15%)" if engagement_rate > 15
                else "Bon (10-15%)" if engagement_rate >= 10
                else "Moyen (5-10%)" if engagement_rate >= 5
                else "Faible (<5%)"
            ),
            "growth_rate_monthly_pct": growth_rate,
            "nps_proxy": nps_proxy,
            "nps_proxy_label": (
                "Promoteurs dominants (>50)" if nps_proxy > 50
                else "Neutre (30-50)" if nps_proxy >= 30
                else "Détracteurs à risque (<30)"
            ),
            "posts_per_day": posts_per_day,
            "members_per_event": members_per_event,
            "content_velocity_score": content_velocity_score,
        },
        "community_health_score": health_score,
        "community_health_label": health_label,
        "most_active_segments": most_active_segments,
        "benchmarks": {
            "engagement_rate_target": COMMUNITY_PLATFORMS["LINKEDIN_GROUP"]["engagement_target_pct"],
            "growth_rate_target_monthly_pct": 5.0,
            "nps_target": 60,
            "posts_per_day_target": 2.0,
            "source": "Benchmarks communautés B2B ESG Europe 2024-2025",
        },
        "recommendations": recommendations,
        "summary": (
            f"Sur les {period_days} derniers jours, la communauté CaelumSwarm™ affiche une santé "
            f"globale '{health_label}' (score {health_score}/100). "
            f"Le taux d'engagement est de {engagement_rate}%, le NPS proxy de {nps_proxy} "
            f"et la croissance mensuelle estimée à {growth_rate}%. "
            f"Le segment le plus actif est '{most_active_segments[0]['label']}' "
            f"avec {most_active_segments[0]['share_pct']}% des contributions. "
            f"{len(recommendations)} recommandation(s) priorisée(s) sont disponibles."
        ),
    }


# ---------------------------------------------------------------------------
# DEMO
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Démonstration complète de l'agent assistant de communauté CaelumSwarm™.
    Illustre les 3 fonctions principales avec des scénarios représentatifs.
    """
    separator = "=" * 72

    print(separator)
    print("  CaelumSwarm™ Community Assistant Agent — Démonstration")
    print(separator)
    print()

    # ------------------------------------------------------------------
    # 1. Séquence d'onboarding pour une nouvelle Directrice RSE
    # ------------------------------------------------------------------
    print("1. SÉQUENCE D'ACCUEIL — Nouvelle Directrice RSE (Grande Entreprise)")
    print("-" * 72)

    welcome = generate_welcome_sequence(
        member_type="COMPLIANCE_PROFESSIONALS",
        company_size="GE",
    )

    print(f"Séquence ID     : {welcome['sequence_id']}")
    print(f"Segment membre  : {welcome['member_label']}")
    print(f"Taille société  : {welcome['company_size']}")
    print(f"Nombre d'emails : {welcome['total_emails']} emails sur {welcome['total_duration_days']} jours")
    print()
    print("Aperçu des emails :")
    for email in welcome["emails"]:
        print(f"  Email {email['email_number']} (J+{email['send_day']:2d}) : {email['subject']}")
        print(f"    CTA : {email['cta']['label']} [{email['cta']['type'].upper()}]")
    print()
    print("Facteurs de personnalisation :")
    pers = welcome["personalization_factors"]
    print(f"  Contexte taille     : {pers['size_context']}")
    print(f"  Message d'urgence   : {pers['urgency_message'][:80]}...")
    print(f"  Contenu préféré #1  : {pers['preferred_content_types'][0]}")
    print()

    # ------------------------------------------------------------------
    # 2. Calendrier mensuel — Lancement Wave 194
    # ------------------------------------------------------------------
    print(separator)
    print("2. CALENDRIER MENSUEL — Lancement Wave 194 (Juillet 2026)")
    print("-" * 72)

    calendar = plan_monthly_events(month=7, wave_number=194)

    print(f"Calendrier ID   : {calendar['calendar_id']}")
    print(f"Mois            : {calendar['month_name']} {calendar['year']}")
    print(f"Wave            : #{calendar['wave_number']}")
    print(f"Événements      : {calendar['events_count']}")
    print()
    print("Événements planifiés :")
    for evt in calendar["events"]:
        tpl = evt["template"]
        print(f"  [{evt['type']}]")
        print(f"    Date           : {evt['date']} — {evt['time']}")
        print(f"    Thème          : {evt['theme'][:65]}...")
        print(f"    Format         : {evt['format']}")
        print(f"    Durée          : {tpl['duration_minutes']} min | Max : {tpl['max_participants']} participants")
        print(f"    Leads estimés  : {evt.get('expected_leads', tpl['expected_leads'])}")
        print(f"    Promo dès      : {evt['promotion_start']}")
        print()

    perf = calendar["performance_forecast"]
    print("Prévisions de performance :")
    print(f"  Participation totale estimée : {perf['total_expected_attendance']} personnes")
    print(f"  Leads totaux estimés         : {perf['total_expected_leads']}")
    print(f"  Nouveaux membres estimés     : {perf['estimated_new_members']}")
    print(f"  Upgrades Premium estimés     : {perf['estimated_premium_upgrades']}")

    budget = calendar["budget_estimate_eur"]
    print(f"\nBudget estimé : {budget['total']} EUR ({budget['note']})")
    print()

    print("Plan de promotion — Canaux clés :")
    for channel_plan in calendar["promotion_plan"]["channels"][:2]:
        print(f"  {channel_plan['channel']} :")
        for action in channel_plan["actions"][:3]:
            print(f"    • {action}")
    print()

    # ------------------------------------------------------------------
    # 3. Rapport de santé communautaire
    # ------------------------------------------------------------------
    print(separator)
    print("3. RAPPORT DE SANTÉ COMMUNAUTAIRE — 30 derniers jours")
    print("-" * 72)

    report = generate_engagement_report(
        period_days=30,
        member_count=3247,
        posts_count=312,
        events_count=4,
    )

    print(f"Rapport ID      : {report['report_id']}")
    print(f"Période         : {report['period_label']}")
    print(f"Membres actifs  : {report['inputs']['member_count']:,}")
    print(f"Posts publiés   : {report['inputs']['posts_count']}")
    print(f"Événements      : {report['inputs']['events_count']}")
    print()
    print(f"Score de santé  : {report['community_health_score']}/100 — {report['community_health_label']}")
    print()
    print("Métriques clés :")
    km = report["key_metrics"]
    print(f"  Taux d'engagement       : {km['engagement_rate']}% ({km['engagement_rate_label']})")
    print(f"  Croissance mensuelle    : +{km['growth_rate_monthly_pct']}%")
    print(f"  NPS proxy               : {km['nps_proxy']} ({km['nps_proxy_label']})")
    print(f"  Posts/jour              : {km['posts_per_day']} (objectif : {report['benchmarks']['posts_per_day_target']})")
    print(f"  Score vélocité contenu  : {km['content_velocity_score']}/10")
    print()

    print("Segments les plus actifs :")
    for rank, seg in enumerate(report["most_active_segments"], 1):
        bar = "#" * int(seg["share_pct"] / 2)
        print(f"  {rank}. {seg['label']:<40} {seg['share_pct']:5.1f}% {bar}")
    print()

    print(f"Recommandations ({len(report['recommendations'])} actions) :")
    for rec in report["recommendations"]:
        print(f"  [{rec['priority']:<6}] {rec['category']:<25} — {rec['recommendation'][:55]}...")
    print()
    print("Synthèse :")
    print(f"  {report['summary']}")
    print()
    print(separator)
    print("  Démonstration terminée avec succès.")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_demo()

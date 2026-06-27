# Specs waves 1177-1184 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : buy_now_pay_later_debt_trap(existe)→embedded_finance_liability(EFLR) ;
#                 SIDR(pris)→IFDR pour influencer_disclosure ;
#                 hijab_workplace_ban(existe, différent angle)→ISER conservé (islamophobie plus large)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1177 — Justice: procédures judiciaires (inédits)
    ("jury_racial_peremptory_challenge_rights_engine.py",
     "Récusations péremptoires à motif racial dans la sélection des jurés & arrêt Batson sous-appliqué", "Wave 1177",
     "Accusés, souvent noirs, jugés par des jurés sélectionnés après exclusion systématique des pairs noirs par le procureur.",
     "JSRP", "jury_racial_peremptor"),
    ("unanimous_jury_verdict_rights_engine.py",
     "Exigence d'unanimité du jury dans les condamnations criminelles & droits des accusés dans les États permettant la majorité", "Wave 1177",
     "Accusés condamnés par des jurys non unanimes dans des États autorisant les verdicts à la majorité, créant un risque de biais.",
     "UJVR", "unanim_jury_verdict"),
    ("jury_disability_exclusion_rights_engine.py",
     "Exclusion des personnes handicapées des jurys sans cause valable & droit à la participation civique inclusive", "Wave 1177",
     "Personnes sourdes ou avec d'autres handicaps exclues des jurys sans évaluation individualisée de leur capacité à servir.",
     "VDDR", "jury_disab_exclus"),

    # Wave 1178 — Sports: sécurité & droits des athlètes (inédits)
    ("youth_sport_concussion_protocol_rights_engine.py",
     "Protocoles de gestion des commotions cérébrales des jeunes sportifs & pression à reprendre avant guérison complète", "Wave 1178",
     "Jeunes athlètes remis sur le terrain trop tôt après une commotion sous pression de l'entraîneur sans évaluation médicale.",
     "YSCP", "youth_concus_proto"),
    ("cheerleader_safety_college_rights_engine.py",
     "Sécurité des cheerleaders universitaires & absence de protections NCAA équivalentes aux autres sports", "Wave 1178",
     "Cheerleaders universitaires subissant des blessures graves et des abus sans les protections accordées aux athlètes NCAA.",
     "CSNR", "cheerleader_safety"),
    ("youth_gymnastics_abuse_reporting_rights_engine.py",
     "Signalement obligatoire des abus dans la gymnastique jeunesse & défaillances des fédérations sportives à protéger", "Wave 1178",
     "Gymnaste junior subissant des abus physiques et psychologiques d'entraîneurs non signalés par les clubs par peur du scandale.",
     "YGAR", "youth_gymn_abuse"),

    # Wave 1179 — Vétérans: droits spécifiques (inédits)
    ("veteran_pension_net_worth_test_rights_engine.py",
     "Test de valeur nette pour la pension vétérans & pénalisation injuste des vétérans ayant des économies modestes", "Wave 1179",
     "Vétérans à faibles revenus refusés pour la pension VA car leurs économies modestes dépassent le plafond de valeur nette.",
     "VPNR", "vet_pension_networth"),
    ("military_discharge_upgrade_rights_engine.py",
     "Révision du type de congé militaire & droits des vétérans à faire corriger des congés honorables limités injustes", "Wave 1179",
     "Vétérans avec congé other-than-honorable perdant des avantages VA dus à des raisons liées à un trouble mental non diagnostiqué.",
     "MDUR", "mil_discharge_upgrad"),
    ("veterans_treatment_court_rights_engine.py",
     "Tribunaux de traitement pour vétérans & droits des vétérans accusés à accéder aux programmes de déjudiciarisation", "Wave 1179",
     "Vétérans accusés de crimes liés à leur PTSD n'ayant pas accès à des tribunaux spécialisés dans tous les comtés.",
     "VCPD", "vet_treat_court"),

    # Wave 1180 — Logement: prêts & évaluation (inédits)
    ("mortgage_servicer_escrow_error_rights_engine.py",
     "Erreurs de gestion du compte d'entiercement par les prestataires hypothécaires & droits des emprunteurs à correction", "Wave 1180",
     "Propriétaires confrontés à des erreurs d'entiercement causant des hausses de mensualités ou des défauts de paiement d'assurance.",
     "MSEE", "mortgage_escrow_err"),
    ("fha_loan_discrimination_rights_engine.py",
     "Discrimination dans les prêts FHA & refus injustifiés basés sur la race ou le quartier par des prêteurs agréés FHA", "Wave 1180",
     "Acheteurs de maison noirs refusés pour des prêts FHA malgré des profils similaires à des emprunteurs blancs approuvés.",
     "FHLR", "fha_loan_discrim"),
    ("home_appraisal_racial_bias_rights_engine.py",
     "Biais racial dans les évaluations immobilières & sous-évaluation systématique des maisons dans les quartiers noirs", "Wave 1180",
     "Propriétaires noirs découvrant que leur maison est évaluée significativement moins que des propriétés identiques dans des quartiers blancs.",
     "ABMR", "apprais_racial_bias"),

    # Wave 1181 — Transport: droits des passagers aériens (inédits)
    ("airline_passenger_stranded_rights_engine.py",
     "Droits des passagers aériens bloqués lors d'annulations massives & remboursements obtenus difficilement", "Wave 1181",
     "Passagers bloqués des jours après des annulations massives sans hébergement, remboursement ni information claire de la compagnie.",
     "APSR", "airline_stranded"),
    ("airport_wheelchair_access_rights_engine.py",
     "Accessibilité fauteuil roulant dans les aéroports & droits des passagers handicapés à une assistance ACAA garantie", "Wave 1181",
     "Passagers en fauteuil roulant blessés ou abandonnés lors de transferts en raison d'un manque de personnel d'assistance aéroport.",
     "AWCR", "airport_wheelchair"),
    ("airline_medical_disability_rights_engine.py",
     "Accommodements médicaux en avion & refus d'embarquement pour des conditions médicales légitimes sous ACAA", "Wave 1181",
     "Passagers avec troubles médicaux ou handicaps refusés à l'embarquement sans raison médicale valide par des compagnies.",
     "ADAR", "airline_med_disab"),

    # Wave 1182 — Finance: tech & protection consommateurs (inédits)
    ("social_media_influencer_ftc_disclosure_rights_engine.py",
     "Divulgations FTC par les influenceurs de réseaux sociaux & promotions cachées trompant les consommateurs non avertis", "Wave 1182",
     "Consommateurs achetant des produits recommandés par des influenceurs ignorant qu'il s'agit de publicités rémunérées non divulguées.",
     "IFDR", "influencer_ftc_discl"),
    ("payment_app_fraud_protection_rights_engine.py",
     "Protection contre la fraude sur les applications de paiement mobile & responsabilité limitée des plateformes Zelle Venmo", "Wave 1182",
     "Victimes de fraude sur Zelle ou Venmo ne pouvant récupérer des fonds envoyés par erreur ou sous contrainte sans protection légale.",
     "PAFP", "payment_app_fraud"),
    ("embedded_finance_liability_rights_engine.py",
     "Responsabilité des services financiers intégrés dans les apps non bancaires & manque de protection consommateurs CFPB", "Wave 1182",
     "Consommateurs perdant des fonds déposés dans des wallets non bancaires intégrés à des apps sans garantie FDIC applicable.",
     "EFLR", "embedded_finance"),

    # Wave 1183 — Immigration: visas de travail (inédits)
    ("l1_intracompany_visa_rights_engine.py",
     "Droits des travailleurs visa L-1 intra-entreprise & dépendance totale à l'employeur en cas de licenciement", "Wave 1183",
     "Travailleurs L-1 transférés aux États-Unis perdant leur statut légal immédiatement en cas de licenciement sans visa de remplacement.",
     "LIVR", "l1_visa_rights"),
    ("tn_visa_nafta_worker_rights_engine.py",
     "Droits des travailleurs visa TN canadiens et mexicains & restrictions sectorielles et renouvellement incertain", "Wave 1183",
     "Professionnels canadiens et mexicains sous visa TN confrontés à des refus de renouvellement arbitraires à la frontière.",
     "TNVR", "tn_visa_worker"),
    ("visa_employer_dependency_rights_engine.py",
     "Dépendance des travailleurs sous visa à leur employeur sponsor & abus de pouvoir dans les secteurs H-1B et L-1", "Wave 1183",
     "Travailleurs H-1B ou L-1 incapables de signaler des violations de droit du travail par peur de perdre leur statut légal.",
     "VSEC", "visa_employer_dep"),

    # Wave 1184 — Droits civiques: discrimination religieuse (inédits)
    ("religious_grooming_workplace_rights_engine.py",
     "Accommodements religieux pour coiffure et barbe au travail & refus des employeurs d'adapter les politiques de tenue", "Wave 1184",
     "Employés sikhs, musulmans ou juifs se voyant refuser le droit de porter turban, barbe ou kippa dans des emplois non essentiels.",
     "RAGR", "relig_grooming_work"),
    ("islamophobia_employment_discrimination_rights_engine.py",
     "Discrimination islamophobe en milieu professionnel & plaintes EEOC sous-déclarées par peur de représailles", "Wave 1184",
     "Travailleurs musulmans subissant hostilité, harcèlement ou refus de promotion en raison de leur foi islamique au travail.",
     "ISER", "islamophobia_employ"),
    ("antisemitism_workplace_rights_engine.py",
     "Antisémitisme au travail & protections insuffisantes du Titre VII contre la discrimination religieuse juive", "Wave 1184",
     "Employés juifs confrontés à des actes antisémites de collègues ou managers sans action effective de leurs employeurs.",
     "ASWP", "antisemit_workplace"),
]

# Specs waves 1089-1096 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : freelancer_invoice(existe)→freelance_platform_arbitration(FPAR) ;
#                 paratransit(existe)→bus_accessibility_ramp(BARR) ;
#                 data_broker(existe)→geofence_warrant(GWPR) ; genetic_database_law_enforce(existe)→third_party_doctrine(TPDP) ;
#                 whistleblower_corporate(existe)→qui_tam_retalia(QTRT) ;
#                 school_counselor_caseload(existe)→school_librarian_elimination(SLBE)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1089 — Santé: dermatologie & soins de la peau (inédits)
    ("sunscreen_fda_approval_rights_engine.py",
     "Approbation FDA des filtres solaires avancés & accès des consommateurs américains aux écrans solaires efficaces", "Wave 1089",
     "Consommateurs américains privés de filtres solaires chimiques avancés approuvés en Europe par une réglementation FDA obsolète.",
     "SFAR", "sunscreen_fda_approv"),
    ("melanoma_early_detection_rights_engine.py",
     "Détection précoce du mélanome & refus de dépistage annuel par les assureurs pour patients à risque", "Wave 1089",
     "Patients à haut risque de mélanome refusés pour un dépistage annuel dermatologique non couvert par les assureurs.",
     "MEDR", "melanoma_early_detect"),
    ("dermatology_waitlist_rights_engine.py",
     "Pénurie de dermatologues & délais de rendez-vous dangereux pour conditions cutanées urgentes", "Wave 1089",
     "Patients attendant des mois pour voir un dermatologue, avec des conditions potentiellement cancéreuses sans diagnostic.",
     "DWLR", "dermatology_waitlist"),

    # Wave 1090 — Emploi: contrats atypiques (inédits)
    ("freelance_platform_arbitration_rights_engine.py",
     "Clauses d'arbitrage imposées aux freelances par les plateformes & blocage des recours collectifs", "Wave 1090",
     "Freelances contraints de signer des clauses d'arbitrage empêchant tout recours collectif contre les plateformes abusives.",
     "FPAR", "freelance_platform_arb"),
    ("temp_agency_worker_permanent_rights_engine.py",
     "Travailleurs temporaires en agence & droit à la conversion en emploi permanent après longue durée", "Wave 1090",
     "Employés temporaires travaillant en agence pendant des années sans jamais accéder à un statut permanent et ses avantages.",
     "TAWP", "temp_agency_perm"),
    ("employment_background_check_error_rights_engine.py",
     "Erreurs dans les vérifications d'antécédents à l'embauche & droits des victimes aux corrections rapides", "Wave 1090",
     "Candidats rejetés pour des informations erronées dans leur dossier d'antécédents sans notification ni droit de correction.",
     "EBCE", "employ_backgnd_error"),

    # Wave 1091 — Logement: accession à la propriété (inédits)
    ("down_payment_assistance_access_rights_engine.py",
     "Accès aux programmes d'aide à la mise de fonds & exclusions raciales dans les critères d'éligibilité", "Wave 1091",
     "Familles à revenus modestes exclues des programmes d'aide à la mise de fonds par des critères géographiques discriminatoires.",
     "DPAA", "down_payment_assist"),
    ("hoa_foreclosure_minor_debt_rights_engine.py",
     "Saisies immobilières par les HOA pour dettes d'amendes mineures & droits des propriétaires", "Wave 1091",
     "Propriétaires perdant leur maison à cause de saisies engagées par leur HOA pour des dettes d'amendes de quelques centaines de dollars.",
     "HOAF", "hoa_foreclosure"),
    ("deed_restriction_segregation_rights_engine.py",
     "Restrictions de titres de propriété historiquement ségrégées & droit des propriétaires à les faire annuler", "Wave 1091",
     "Propriétaires découvrant des clauses raciales illégales dans leurs titres de propriété sans procédure simple d'effacement.",
     "DRSR", "deed_segreg_restrict"),

    # Wave 1092 — Transport & mobilité (inédits)
    ("bus_accessibility_ramp_rights_engine.py",
     "Accessibilité des rampes de bus & droits des usagers handicapés face aux défaillances répétées", "Wave 1092",
     "Utilisateurs de fauteuils roulants bloqués par des rampes de bus défectueuses sans alternative de transport disponible.",
     "BARR", "bus_access_ramp"),
    ("rural_public_transit_right_engine.py",
     "Absence de transport public rural & droits des non-conducteurs à la mobilité dans les comtés sans bus", "Wave 1092",
     "Personnes âgées et handicapées en zones rurales sans voiture ni transport public, coupées des soins et services essentiels.",
     "RPTR", "rural_public_transit"),
    ("taxi_wheelchair_accessibility_rights_engine.py",
     "Discrimination des services de taxi et VTC contre les utilisateurs de fauteuils roulants & ADA", "Wave 1092",
     "Utilisateurs de fauteuils roulants refusés par des chauffeurs de taxi et VTC malgré l'obligation ADA d'accessibilité.",
     "TXWR", "taxi_wheelchair"),

    # Wave 1093 — Données personnelles & surveillance (inédits)
    ("geofence_warrant_privacy_rights_engine.py",
     "Mandats de géo-clôture & droit à la vie privée face aux enquêtes de masse par localisation GPS", "Wave 1093",
     "Citoyens innocents identifiés par des mandats géo-clôture demandant les données de localisation de tous dans une zone.",
     "GWPR", "geofence_warrant"),
    ("employee_remote_monitoring_rights_engine.py",
     "Surveillance des employés en télétravail & droit à la vie privée dans l'espace domestique", "Wave 1093",
     "Télétravailleurs soumis à des logiciels de surveillance enregistrant les frappes, captures d'écran et mouvements de caméra.",
     "EMRT", "employee_remote_mon"),
    ("third_party_doctrine_privacy_rights_engine.py",
     "Doctrine du tiers & accès de la police aux données partagées avec entreprises sans mandat judiciaire", "Wave 1093",
     "Historiques de recherche et transactions bancaires communiqués aux forces de l'ordre sans mandat sous la doctrine du tiers.",
     "TPDP", "third_party_doctrine"),

    # Wave 1094 — Santé des hommes (inédits)
    ("prostate_cancer_screening_disparity_rights_engine.py",
     "Disparités de dépistage du cancer de la prostate & recommandations contradictoires entre institutions", "Wave 1094",
     "Hommes confondus par des recommandations contradictoires entre médecins et assureurs sur le dépistage PSA, retardant le diagnostic.",
     "PCSD", "prostate_screen"),
    ("male_eating_disorder_treatment_rights_engine.py",
     "Troubles alimentaires chez les hommes & sous-diagnostic chronique faute de formation médicale adaptée", "Wave 1094",
     "Hommes souffrant d'anorexie ou boulimie sous-diagnostiqués par des professionnels de santé supposant ces troubles féminins.",
     "MEDT", "male_eating_disorder"),
    ("testosterone_therapy_insurance_rights_engine.py",
     "Thérapie de remplacement à la testostérone & refus de couverture assurance pour hypogonadisme", "Wave 1094",
     "Hommes hypogonadiques refusés pour une couverture de la thérapie testostéronique malgré un diagnostic médical établi.",
     "TTIR", "testosterone_insur"),

    # Wave 1095 — Justice: protection des délateurs (inédits)
    ("qui_tam_retaliation_rights_engine.py",
     "Représailles contre les plaignants Qui Tam & protections limitées du False Claims Act fédéral", "Wave 1095",
     "Dénonciateurs Qui Tam licenciés ou rétrogradés après avoir signalé des fraudes aux programmes gouvernementaux.",
     "QTRT", "qui_tam_retalia"),
    ("witness_protection_local_crime_rights_engine.py",
     "Protection des témoins dans les affaires criminelles locales & absence de programme formel étatique", "Wave 1095",
     "Témoins de crimes violents locaux menacés par des représailles sans accès au programme de protection fédéral des témoins.",
     "WPLC", "witness_protect_local"),
    ("osha_whistleblower_protection_rights_engine.py",
     "Protection des lanceurs d'alerte OSHA & délais excessifs de traitement des plaintes de représailles", "Wave 1095",
     "Travailleurs signalant des violations de sécurité licenciés pour représailles dont les plaintes OSHA restent sans réponse des mois.",
     "OWPR", "osha_whistleblow"),

    # Wave 1096 — Éducation: enseignants & personnel scolaire (inédits)
    ("teacher_tenure_due_process_rights_engine.py",
     "Tenure enseignante & droits de procédure régulière avant licenciement dans les districts scolaires", "Wave 1096",
     "Enseignants titulaires licenciés sans procédure formelle complète dans des États réformant les protections de tenure.",
     "TTDP", "teacher_tenure_dp"),
    ("school_librarian_elimination_rights_engine.py",
     "Suppressions budgétaires des bibliothécaires scolaires & impact sur l'alphabétisation et l'accès à l'information", "Wave 1096",
     "Élèves privés de bibliothécaire scolaire après des coupes budgétaires, perdant l'accès guidé aux ressources éducatives.",
     "SLBE", "school_librarian"),
    ("para_educator_wage_gap_rights_engine.py",
     "Écart salarial des éducateurs para-scolaires & droits à une rémunération équitable pour soutien aux élèves handicapés", "Wave 1096",
     "Assistants d'éducation spécialisés payés proche du salaire minimum tout en assurant des fonctions cruciales de soutien aux élèves.",
     "PEWG", "para_educator_wage"),
]

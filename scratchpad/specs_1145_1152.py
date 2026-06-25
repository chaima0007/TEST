# Specs waves 1145-1152 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : rural_hospital_closure(existe)→rural_lawyer_access(RLAR) ;
#                 elder_guardianship_exploitation(existe)→professional_guardian_oversight(PGOR) ;
#                 TCPR(pris)→TICP ; CPFL(pris)→CPFC ; CPRR(pris)→CPFC(utilisé)→CPFR ;
#                 RASR(pris)→REMR
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1145 — Santé: maladies auto-immunes (inédits)
    ("lupus_diagnosis_delay_rights_engine.py",
     "Retard diagnostique du lupus chez les femmes noires & biais médical systémique dans la détection auto-immune", "Wave 1145",
     "Femmes noires attendant en moyenne des années un diagnostic de lupus malgré des symptômes classiques minimisés par les médecins.",
     "LDDP", "lupus_diag_delay"),
    ("multiple_sclerosis_treatment_access_rights_engine.py",
     "Accès aux traitements modificateurs de la SEP & refus de couverture pour les thérapies de première ligne", "Wave 1145",
     "Patients atteints de sclérose en plaques refusés pour les traitements modificateurs de la maladie les plus efficaces par étapes d'assurance.",
     "MSTA", "ms_treat_access"),
    ("myalgic_encephalomyelitis_recognition_rights_engine.py",
     "ME/CFS comme maladie grave sous-reconnue & droits des patients à des soins appropriés et à l'assurance invalidité", "Wave 1145",
     "Patients atteints de ME/SFC refusés pour l'assurance invalidité et les soins spécialisés par manque de reconnaissance médicale officielle.",
     "MERR", "me_cfs_recognit"),

    # Wave 1146 — Justice: droits des accusés (inédits)
    ("public_defender_caseload_crisis_rights_engine.py",
     "Crise de surcharge des défenseurs publics & droit des accusés à une représentation effective garantie", "Wave 1146",
     "Accusés représentés par des défenseurs publics gérant des centaines de dossiers sans temps suffisant pour chaque client.",
     "PDCC", "pub_def_caseload"),
    ("courtroom_interpreter_quality_rights_engine.py",
     "Qualité insuffisante des interprètes judiciaires & droits des accusés non anglophones à une interprétation précise", "Wave 1146",
     "Accusés dans des procédures pénales graves représentés par des interprètes non certifiés commettant des erreurs matérielles.",
     "CIQR", "court_interp_qual"),
    ("mental_competency_restoration_rights_engine.py",
     "Délais de rétablissement de la compétence mentale & incarcération prolongée des accusés inaptes à comparaître", "Wave 1146",
     "Accusés déclarés inaptes à comparaître attendant des années une place en établissement de restauration de la compétence.",
     "MCRR", "mental_comp_restore"),

    # Wave 1147 — Travail: équité & discrimination (inédits)
    ("caregiver_discrimination_workplace_rights_engine.py",
     "Discrimination des aidants familiaux au travail & préjugés contre les employés avec responsabilités de soin", "Wave 1147",
     "Employés aidant des proches malades ou handicapés pénalisés lors de promotions ou licenciés après avoir demandé de la flexibilité.",
     "CDWR", "caregiver_discrim"),
    ("name_based_hiring_discrimination_rights_engine.py",
     "Discrimination à l'embauche basée sur le prénom à connotation raciale & audit sociaux montrant un biais persistant", "Wave 1147",
     "Candidats avec des prénoms à connotation afro-américaine recevant moins de rappels que des profils identiques avec prénoms blancs.",
     "NBHD", "name_hire_discrim"),
    ("pregnancy_accommodation_workplace_rights_engine.py",
     "Accommodements raisonnables pour grossesses au travail & droits renforcés par le PWFA de 2023 mal appliqués", "Wave 1147",
     "Femmes enceintes refusées pour des accommodements simples comme des pauses ou des sièges par des employeurs ignorant le PWFA.",
     "PWFA", "pregnant_work_accom"),

    # Wave 1148 — Finance: propriété & transmission (inédits)
    ("heirs_property_legal_title_rights_engine.py",
     "Propriété héritée sans titre légal clair & vulnérabilité des familles noires rurales face à la perte de terres ancestrales", "Wave 1148",
     "Familles noires rurales possédant des terres depuis des générations sans titre légal clair, vulnérables aux saisies et tax sales.",
     "HPTL", "heirs_prop_title"),
    ("estate_recovery_medicaid_rights_engine.py",
     "Récupération des frais Medicaid sur successions & impact sur les héritages des familles à faibles revenus", "Wave 1148",
     "Familles de bénéficiaires Medicaid surprises par des réclamations de l'État récupérant des dizaines de milliers sur la succession.",
     "ERMR", "estate_medicaid_rec"),
    ("tenancy_in_common_partition_rights_engine.py",
     "Partage judiciaire des biens en indivision & ventes forcées des parts des co-propriétaires refusant la partition", "Wave 1148",
     "Copropriétaires en indivision contraints de vendre leur bien suite à des actions en partition initiées par un seul co-propriétaire.",
     "TICP", "tenancy_common_part"),

    # Wave 1149 — Environnement: pesticides & chimiques (inédits)
    ("pesticide_school_proximity_rights_engine.py",
     "Exposition aux pesticides agricoles dans les écoles rurales proches des champs & droits des élèves à la protection", "Wave 1149",
     "Élèves dans des écoles rurales exposés à des dérivées de pesticides agricoles appliqués sur des champs voisins sans zones tampon.",
     "PSER", "pestic_school_prox"),
    ("glyphosate_cancer_liability_rights_engine.py",
     "Responsabilité civile pour cancers liés au glyphosate & droits des victimes aux recours contre les fabricants", "Wave 1149",
     "Travailleurs agricoles et jardiniers développant des lymphomes non hodgkiniens liés au glyphosate sans compensation adéquate.",
     "GCLR", "glyphosate_cancer"),
    ("chemical_plant_fenceline_community_rights_engine.py",
     "Communautés vivant en bordure d'usines chimiques & droits à la surveillance de l'air et à l'information environnementale", "Wave 1149",
     "Résidents vivant à moins de 500 mètres d'usines chimiques sans accès aux données de surveillance de qualité de l'air en temps réel.",
     "CPFC", "chem_plant_fence"),

    # Wave 1150 — Santé: accès aux spécialistes (inédits)
    ("rheumatology_specialist_shortage_rights_engine.py",
     "Pénurie de rhumatologues & délais d'accès dangereux pour les maladies auto-immunes et arthritiques", "Wave 1150",
     "Patients atteints d'arthrite rhumatoïde ou de maladies auto-immunes attendant des mois un rendez-vous avec un rhumatologue.",
     "RSSR", "rheumatol_shortage"),
    ("endocrinology_access_rural_rights_engine.py",
     "Accès aux endocrinologues en zones rurales & droits des diabétiques à un suivi spécialisé adéquat", "Wave 1150",
     "Patients diabétiques en zones rurales ne pouvant accéder à un endocrinologue pour une gestion optimale de leur maladie.",
     "EARR", "endocrinol_rural"),
    ("neurology_wait_time_stroke_rights_engine.py",
     "Délais neurologiques post-AVC & droit à une récupération optimale avec rééducation spécialisée en temps utile", "Wave 1150",
     "Survivants d'AVC attendant des mois un neurologue pour la gestion post-AVC, retardant la rééducation critique dans la fenêtre d'or.",
     "NWTS", "neurol_wait_stroke"),

    # Wave 1151 — Droits des seniors: besoins spécifiques (inédits)
    ("senior_technology_isolation_rights_engine.py",
     "Isolement numérique des seniors & exclusion des services essentiels désormais uniquement disponibles en ligne", "Wave 1151",
     "Personnes âgées sans compétences numériques incapables d'accéder aux prestations, soins et services migrés exclusivement en ligne.",
     "SITR", "senior_tech_isolat"),
    ("professional_guardian_oversight_rights_engine.py",
     "Surveillance des tuteurs professionnels pour seniors & abus de pouvoir sur les actifs des personnes sous tutelle", "Wave 1151",
     "Seniors sous tutelle légale dont les tuteurs professionnels exploitent les actifs sans surveillance judiciaire adéquate.",
     "PGOR", "prof_guardian_over"),
    ("senior_snap_access_barriers_rights_engine.py",
     "Barrières à l'accès au programme SNAP pour seniors & complexité administrative excluant les aînés éligibles", "Wave 1151",
     "Seniors éligibles au SNAP incapables de naviguer les processus de candidature en ligne ou de se déplacer aux bureaux.",
     "SHSA", "senior_snap_barrier"),

    # Wave 1152 — Communautés rurales: droits spécifiques (inédits)
    ("rural_legal_desert_access_rights_engine.py",
     "Déserts juridiques ruraux & droits des résidents ruraux à un avocat abordable pour leurs litiges locaux", "Wave 1152",
     "Résidents ruraux dans des comtés sans avocat disponible, obligés de parcourir des heures pour accéder à une aide juridique.",
     "RLAR", "rural_legal_desert"),
    ("rural_emergency_medical_response_rights_engine.py",
     "Temps de réponse ambulancière en zone rurale & droits des résidents à des soins d'urgence dans des délais vitaux", "Wave 1152",
     "Résidents ruraux attendant 30 à 60 minutes une ambulance lors d'urgences cardiaques ou traumatiques potentiellement mortelles.",
     "REMR", "rural_emerg_medic"),
    ("rural_grocery_food_access_rights_engine.py",
     "Déserts alimentaires ruraux & droits des communautés rurales à une alimentation saine et abordable localement", "Wave 1152",
     "Résidents ruraux sans accès à un supermarché dans un rayon de 10 miles, dépendant de stations-service pour leur alimentation.",
     "RGFA", "rural_grocery_food"),
]

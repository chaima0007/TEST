# Specs waves 1065-1072 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : pfas_water(existe)→private_well_contamination ; nursing_home_arbitration(existe)→memory_care_unit ;
#                 nursing_home_understaffing(existe)→long_term_care_ombudsman ;
#                 medical_bankruptcy(existe)→hospital_lien_accident ; medical_debt_bankruptcy(existe)→hospital_charity_care
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1065 — Travailleurs domestiques (inédits)
    ("domestic_worker_overtime_rights_engine.py",
     "Heures supplémentaires refusées aux aides à domicile & exclusions légales persistantes", "Wave 1065",
     "Aides à domicile exclus des lois sur les heures supplémentaires dans plusieurs États sans protection fédérale.",
     "DWOR", "domestic_worker_overtime"),
    ("nanny_wage_theft_rights_engine.py",
     "Vol de salaire des nounous & absence de contrat écrit formalisé", "Wave 1065",
     "Nounous et aides à domicile non payées ou sous-payées sans contrat écrit ni recours légal accessible.",
     "NWTR", "nanny_wage_theft"),
    ("caregiver_deportation_fear_rights_engine.py",
     "Peur de déportation chez les aides à domicile sans papiers & exploitation par les employeurs", "Wave 1065",
     "Aides à domicile sans papiers exploitées par des employeurs abusifs sachant qu'elles ne signaleront pas les violations.",
     "CDFT", "caregiver_deport_fear"),

    # Wave 1066 — Eau & assainissement spécifique (inédits)
    ("lead_pipe_rental_disclosure_rights_engine.py",
     "Canalisations en plomb dans les logements locatifs & obligation de divulgation au locataire", "Wave 1066",
     "Locataires non informés des canalisations en plomb dans leur logement, exposés au plomb sans recours contre les propriétaires.",
     "LPDW", "lead_pipe_disclose"),
    ("private_well_contamination_rights_engine.py",
     "Contamination des puits privés par les entreprises voisines & absence de régulation fédérale", "Wave 1066",
     "Propriétaires de puits privés contaminés par des activités industrielles voisines sans obligation de test ni compensation.",
     "PWCR", "private_well_contam"),
    ("rural_septic_failure_rights_engine.py",
     "Défaillances des fosses septiques rurales & absence d'aide financière pour les ménages pauvres", "Wave 1066",
     "Familles rurales avec fosses septiques défectueuses incapables de financer les réparations obligatoires coûteuses.",
     "RSFR", "rural_septic_fail"),

    # Wave 1067 — Discrimination à l'embauche (inédits)
    ("height_weight_employment_bias_rights_engine.py",
     "Discrimination à l'embauche selon la taille et le poids & protections légales insuffisantes", "Wave 1067",
     "Candidats rejetés en raison de leur poids ou taille sans protection anti-discrimination dans la majorité des États.",
     "HWEB", "height_weight_bias"),
    ("accent_discrimination_workplace_rights_engine.py",
     "Discrimination à l'accent au travail & droits des travailleurs immigrants", "Wave 1067",
     "Employés immigrants pénalisés ou licenciés à cause de leur accent étranger malgré des compétences professionnelles avérées.",
     "ADWR", "accent_discrim_work"),
    ("credit_check_hiring_rights_engine.py",
     "Vérification de crédit à l'embauche & discrimination financière contre les candidats pauvres", "Wave 1067",
     "Candidats refusés pour un emploi en raison d'un mauvais historique de crédit sans lien avec le poste visé.",
     "CCHR", "credit_check_hire"),

    # Wave 1068 — Santé préventive & sensorielle (inédits)
    ("dental_school_clinic_access_rights_engine.py",
     "Accès aux cliniques dentaires universitaires pour patients à faibles revenus & listes d'attente", "Wave 1068",
     "Patients sans assurance dentaire contraints d'attendre des mois dans des cliniques universitaires surchargées.",
     "DSCA", "dental_school_clinic"),
    ("dry_eye_disease_coverage_rights_engine.py",
     "Maladie des yeux secs chronique & refus de couverture assurance pour les traitements innovants", "Wave 1068",
     "Patients souffrant d'yeux secs sévères refusés pour des gouttes prescrites ou dispositifs thérapeutiques coûteux.",
     "DEDC", "dry_eye_coverage"),
    ("tinnitus_disability_rights_engine.py",
     "Acouphènes chroniques & absence de reconnaissance en handicap professionnel et couverture assurance", "Wave 1068",
     "Travailleurs développant des acouphènes sévères suite à l'exposition au bruit sans indemnisation ou traitement couvert.",
     "TNDS", "tinnitus_disability"),

    # Wave 1069 — Justice criminelle post-incarcération (inédits)
    ("felony_disenfranchisement_rights_engine.py",
     "Suppression du droit de vote des condamnés & barrières permanentes à la réintégration civique", "Wave 1069",
     "Anciens détenus privés du droit de vote à vie dans certains États, exclus définitivement de la démocratie.",
     "FDEV", "felony_disenfranchise"),
    ("occupational_license_felony_rights_engine.py",
     "Licences professionnelles refusées aux anciens détenus & barrières permanentes à l'emploi", "Wave 1069",
     "Personnes ayant purgé leur peine incapables d'obtenir une licence professionnelle en raison de leur casier.",
     "OLFR", "occup_license_felon"),
    ("halfway_house_condition_rights_engine.py",
     "Conditions de vie dans les maisons de transition & droits des libérés conditionnels", "Wave 1069",
     "Ex-détenus en liberté conditionnelle dans des maisons de transition surpeuplées avec des règles arbitraires et punitives.",
     "HHCR", "halfway_house_cond"),

    # Wave 1070 — Santé reproductive avancée (inédits)
    ("vasectomy_reversal_coverage_rights_engine.py",
     "Couverture des réversions de vasectomie & inégalités de genre dans les assurances reproductives", "Wave 1070",
     "Hommes désireux d'inverser une vasectomie refusés pour une couverture alors que des procédures féminines sont couvertes.",
     "VRCV", "vasectomy_reversal"),
    ("ivf_multiple_embryo_transfer_rights_engine.py",
     "Transfert d'embryons multiples en FIV & pression institutionnelle sur les patients", "Wave 1070",
     "Patients de FIV poussés à transférer plusieurs embryons par pression financière, augmentant les risques de grossesses multiples.",
     "IMTR", "ivf_multi_embryo"),
    ("egg_freezing_employer_coverage_rights_engine.py",
     "Congélation d'ovules & couverture inégale par les assureurs des employeurs", "Wave 1070",
     "Femmes souhaitant congeler leurs ovules pour préserver leur fertilité sans couverture d'assurance employeur systématique.",
     "EFEC", "egg_freeze_coverage"),

    # Wave 1071 — Résidences seniors & maisons de retraite (inédits)
    ("memory_care_unit_rights_engine.py",
     "Unités de soins mémoire & qualité des soins pour patients Alzheimer en résidence", "Wave 1071",
     "Résidents Alzheimer dans des unités mémoire sans personnel formé ni activités thérapeutiques adaptées.",
     "MCUR", "memory_care_unit"),
    ("assisted_living_eviction_rights_engine.py",
     "Évictions des résidences assistées & droits des seniors sans recours légal clair", "Wave 1071",
     "Seniors évincés de résidences assistées sans préavis suffisant ni procédure d'appel équitable.",
     "ALER", "assisted_living_evict"),
    ("long_term_care_ombudsman_rights_engine.py",
     "Médiateurs des soins longue durée & accès insuffisant aux recours pour les résidents", "Wave 1071",
     "Résidents de maisons de retraite ignorant l'existence des médiateurs légalement requis pour défendre leurs droits.",
     "LTCO", "ltc_ombudsman"),

    # Wave 1072 — Dettes médicales & recours financiers (inédits)
    ("medical_debt_credit_score_rights_engine.py",
     "Dettes médicales sur le score de crédit & impact disproportionné sur les ménages vulnérables", "Wave 1072",
     "Patients dont les dettes médicales impactent leur score de crédit, bloquant l'accès au logement et à l'emploi.",
     "MDCS", "medical_debt_credit"),
    ("hospital_lien_accident_rights_engine.py",
     "Liens hospitaliers sur les indemnités d'accidents & droits des victimes blessées", "Wave 1072",
     "Victimes d'accidents recevant moins d'indemnisation après que les hôpitaux ont placé des liens sur leurs règlements.",
     "HLAR", "hospital_lien_accident"),
    ("hospital_charity_care_rights_engine.py",
     "Soins de charité hospitaliers & opacité des critères d'éligibilité pour patients démunis", "Wave 1072",
     "Patients sans revenu ignorant leur éligibilité aux soins de charité que les hôpitaux sont légalement tenus de proposer.",
     "HCHR", "hospital_charity"),
]

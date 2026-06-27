# Specs waves 1097-1104 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : lead_paint_child(existe)→radon_gas_rental_disclosure(RGRD) ;
#                 carbon_monoxide_detector(existe)→building_code_inspection(BCIF) ;
#                 mental_health_parity(existe)→mental_health_network_adequacy(MHNA) ;
#                 juvenile_record_sealing(existe)→criminal_record_occupational_ban(CROB)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1097 — Réinsertion & justice post-carcérale (inédits)
    ("prison_reentry_public_housing_rights_engine.py",
     "Accès au logement public après incarcération & politique One Strike d'exclusion automatique", "Wave 1097",
     "Anciens détenus exclus des logements sociaux par la politique One Strike, rendant la réinsertion impossible.",
     "REPH", "reentry_public_hous"),
    ("colorism_employment_rights_engine.py",
     "Discrimination basée sur la teinte de peau au travail & absence de protection légale explicite", "Wave 1097",
     "Employés à peau plus foncée traités différemment de collègues à peau plus claire de même origine ethnique.",
     "CLEM", "colorism_employ"),
    ("criminal_record_occupational_ban_rights_engine.py",
     "Interdictions professionnelles permanentes pour anciens condamnés & barrières à la réhabilitation", "Wave 1097",
     "Anciens condamnés interdits à vie d'exercer certaines professions sans relation avec leur infraction passée.",
     "CROB", "criminal_occup_ban"),

    # Wave 1098 — Santé des femmes: hormones & spécifique (inédits)
    ("female_pattern_baldness_treatment_rights_engine.py",
     "Alopécie féminine de type andrогénétique & refus de couverture assurance pour traitements médicaux", "Wave 1098",
     "Femmes souffrant d'alopécie androgénétique refusées pour une couverture des traitements prescrits par leur médecin.",
     "FPBT", "female_pattern_bald"),
    ("pcos_diagnosis_delay_rights_engine.py",
     "Retard de diagnostic du SOPK & minimisation des symptômes par les professionnels de santé", "Wave 1098",
     "Femmes attendant des années un diagnostic de syndrome des ovaires polykystiques malgré des symptômes évidents.",
     "PCOD", "pcos_diag_delay"),
    ("premenstrual_dysphoric_disorder_rights_engine.py",
     "TDPM & accès aux traitements psychiatriques couverts pour trouble dysphorique prémenstruel reconnu", "Wave 1098",
     "Femmes diagnostiquées avec un TDPM refusées pour une couverture des antidépresseurs ou contraceptifs prescrites.",
     "PMDD", "pmdd_treatment"),

    # Wave 1099 — Santé: accès aux médicaments (inédits)
    ("pharmacy_benefit_manager_rights_engine.py",
     "Gestionnaires d'avantages pharmaceutiques (PBM) & pratiques opaques augmentant les coûts des médicaments", "Wave 1099",
     "Patients payant plus cher leurs médicaments à cause des pratiques de manipulation de prix des PBM non réglementées.",
     "PBMR", "pharmacy_benefit_mgr"),
    ("drug_coupon_copay_accumulator_rights_engine.py",
     "Accumulateurs de copaiement & invalidation des coupons fabricants pour les médicaments de marque", "Wave 1099",
     "Patients utilisant des coupons fabricants dont les paiements ne s'accumulent plus vers le déductible annuel.",
     "DCCA", "drug_coupon_accum"),
    ("telehealth_controlled_substance_rights_engine.py",
     "Prescriptions de substances contrôlées via télémédecine & restrictions DEA post-pandémie", "Wave 1099",
     "Patients souffrant de douleur chronique ou ADHD perdant l'accès aux prescriptions en ligne avec la fin des règles COVID.",
     "TCSR", "telehealth_control_rx"),

    # Wave 1100 — Droits des enfants: tutelle & adoption (inédits)
    ("international_adoption_disruption_rights_engine.py",
     "Perturbation des adoptions internationales & droits des enfants abandonnés par les familles adoptives", "Wave 1100",
     "Enfants adoptés à l'étranger remis à l'État américain par des parents adoptifs sans conséquences légales claires.",
     "IADR", "intl_adopt_disrupt"),
    ("child_support_incarceration_rights_engine.py",
     "Pension alimentaire pendant l'incarcération du parent & accumulation d'une dette impossible à rembourser", "Wave 1100",
     "Parents incarcérés accumulant des dettes de pension alimentaire pendant leur détention sans suspension automatique.",
     "CSIR", "child_support_incar"),
    ("medical_consent_minor_rights_engine.py",
     "Consentement médical des mineurs matures & droits aux soins de santé sans accord parental obligatoire", "Wave 1100",
     "Adolescents incapables d'accéder à des soins de santé essentiels sans consentement parental dans des États restrictifs.",
     "MCMR", "medical_consent_minor"),

    # Wave 1101 — Logement: réparations & inspections (inédits)
    ("habitability_standard_enforcement_rights_engine.py",
     "Application des standards d'habitabilité & délais excessifs de réparation imposés aux propriétaires", "Wave 1101",
     "Locataires vivant dans des logements insalubres attendant des mois des réparations sans mécanisme d'exécution efficace.",
     "HSER", "habitability_enforce"),
    ("radon_gas_rental_disclosure_rights_engine.py",
     "Divulgation du radon dans les logements locatifs & droit des locataires à des tests obligatoires", "Wave 1101",
     "Locataires vivant dans des logements à fort taux de radon sans information ni obligation de décontamination du propriétaire.",
     "RGRD", "radon_rental_disclos"),
    ("building_code_inspection_frequency_rights_engine.py",
     "Fréquence des inspections du code du bâtiment & droits des locataires à des inspections régulières", "Wave 1101",
     "Bâtiments résidentiels jamais inspectés entre leur construction et une catastrophe, avec des violations accumulées.",
     "BCIF", "building_code_insp"),

    # Wave 1102 — Emploi: harcèlement & représailles avancés (inédits)
    ("third_party_harassment_employer_rights_engine.py",
     "Responsabilité de l'employeur pour harcèlement par des clients ou fournisseurs tiers & obligations légales", "Wave 1102",
     "Employés harcelés par des clients ou vendeurs dont les employeurs refusent d'agir par peur de perdre des contrats.",
     "TPHL", "third_party_harass"),
    ("social_media_political_retaliation_rights_engine.py",
     "Licenciement pour publications politiques personnelles sur réseaux sociaux & protections du premier amendement", "Wave 1102",
     "Employés licenciés pour des posts politiques personnels sur les réseaux sociaux en dehors des heures de travail.",
     "SMPR", "social_media_politic"),
    ("non_disparagement_settlement_rights_engine.py",
     "Clauses de non-dénigrement dans les accords de règlement & droits des victimes à partager leur expérience", "Wave 1102",
     "Victimes de harcèlement ou discrimination contraintes de signer des clauses les empêchant d'alerter d'autres employés.",
     "NDCR", "non_disparagement"),

    # Wave 1103 — Santé mentale: système d'assurance (inédits)
    ("mental_health_network_adequacy_rights_engine.py",
     "Adéquation du réseau de santé mentale & ratio insuffisant de prestataires dans la plupart des plans", "Wave 1103",
     "Assurés cherchant un thérapeute en réseau attendant des mois car le réseau de prestataires est largement insuffisant.",
     "MHNA", "mental_health_network"),
    ("out_of_network_mental_health_rights_engine.py",
     "Remboursement des soins psychiatriques hors réseau & taux insuffisants imposés par les assureurs", "Wave 1103",
     "Patients contraints de voir un psychiatre hors réseau remboursés à des taux si bas que les soins deviennent inaccessibles.",
     "OONM", "oon_mental_health"),
    ("step_therapy_psychiatric_rights_engine.py",
     "Protocoles step therapy pour les médicaments psychiatriques & obligation d'échec sur des médicaments inadaptés", "Wave 1103",
     "Patients psychiatriques contraints d'échouer avec des médicaments génériques inadaptés avant l'accès au traitement prescrit.",
     "STMH", "step_therapy_psych"),

    # Wave 1104 — Technologie: algorithmes & discriminations (inédits)
    ("algorithmic_credit_discrimination_rights_engine.py",
     "Discrimination algorithmique dans les décisions de crédit & manque de transparence des modèles", "Wave 1104",
     "Emprunteurs refusés pour des crédits par des algorithmes opaques reproduisant des biais raciaux sans recours possible.",
     "ALCD", "algo_credit_discrim"),
    ("social_media_shadowban_rights_engine.py",
     "Shadowban sur les réseaux sociaux & impact économique sur les créateurs et militants sans recours", "Wave 1104",
     "Créateurs de contenu et militants dont la visibilité est réduite par des algorithmes sans notification ni explication.",
     "SMSB", "shadowban_rights"),
    ("algorithmic_rental_price_rights_engine.py",
     "Logiciels de fixation algorithmique des loyers & entente implicite entre propriétaires concurrents", "Wave 1104",
     "Locataires subissant des hausses coordonnées de loyers générées par des algorithmes partagés entre propriétaires concurrents.",
     "ARPR", "algo_rental_price"),
]

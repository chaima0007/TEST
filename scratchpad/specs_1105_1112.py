# Specs waves 1105-1112 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : torture_survivor(existe)→international_extradition_rights(IERR) ;
#                 conversion_therapy_adult_ban(existe)→lgbtq_foster_family_rights(LGFR) ;
#                 bank_account_closure_discrimin(existe)→check_cashing_fee_unbanked(CCFR) ;
#                 unaccompanied_minor_border(existe)→asylum_backlog_court_rights(ABLR) ;
#                 mandatory_retirement_age(existe)→age_discrimin_performance_review(ADPR)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1105 — Santé: urgences & hospitalisation (inédits)
    ("psychiatric_emergency_hold_rights_engine.py",
     "Hospitalisations psychiatriques involontaires & droits à la représentation légale des patients", "Wave 1105",
     "Patients placés en hospitalisation involontaire sans avocat ni audience judiciaire dans des délais raisonnables.",
     "PEHR", "psych_emerg_hold"),
    ("trauma_center_closure_rights_engine.py",
     "Fermetures de centres de traumatologie & impact sur la survie dans les zones rurales et urbaines pauvres", "Wave 1105",
     "Patients victimes de traumatismes graves mourant faute de centre de traumatologie après des fermetures budgétaires.",
     "TCCR", "trauma_center_close"),
    ("patient_restraint_hospital_rights_engine.py",
     "Utilisation de contentions physiques et chimiques en hôpital & droits des patients à la liberté de mouvement", "Wave 1105",
     "Patients hospitalisés soumis à des contentions arbitraires sans protocoles clairs ni justification médicale documentée.",
     "PRHR", "patient_restraint"),

    # Wave 1106 — Justice: peine de mort & extradition (inédits)
    ("execution_drug_shortage_rights_engine.py",
     "Pénuries de drogues létales & expérimentations sur les condamnés à mort sans consentement éclairé", "Wave 1106",
     "Condamnés à mort exécutés avec des drogues non testées causant des souffrances documentées pendant l'exécution.",
     "EXPT", "execution_drug_short"),
    ("international_extradition_rights_engine.py",
     "Extradition internationale de ressortissants américains & droits constitutionnels des accusés extradés", "Wave 1106",
     "Citoyens américains extradés vers des pays sans garanties de procès équitable ou soumis à des conditions inhumaines.",
     "IERR", "intl_extradition"),
    ("solitary_mental_illness_rights_engine.py",
     "Isolement cellulaire des détenus souffrant de maladies mentales sévères & violations des standards médicaux", "Wave 1106",
     "Détenus psychotiques ou dépressifs placés à l'isolement aggravant leur état sans alternative thérapeutique.",
     "SIML", "solitary_mental_ill"),

    # Wave 1107 — Droits LGBTQ+: spécifiques (inédits)
    ("transgender_prison_placement_rights_engine.py",
     "Placement des détenus transgenres en prisons séparées selon le genre & sécurité et dignité", "Wave 1107",
     "Détenus trans placés dans des prisons correspondant à leur genre de naissance, exposés à des violences et humiliations.",
     "TPPR", "trans_prison_place"),
    ("lgbtq_senior_care_rights_engine.py",
     "Soins des seniors LGBTQ+ dans les maisons de retraite & discrimination des prestataires", "Wave 1107",
     "Seniors LGBTQ+ dans des maisons de retraite confrontés à un personnel refusant de respecter leur identité ou partenaire.",
     "LSCR", "lgbtq_senior_care"),
    ("lgbtq_foster_family_rights_engine.py",
     "Familles LGBTQ+ candidates à l'accueil d'enfants placés & refus discriminatoires par agences religieuses", "Wave 1107",
     "Familles LGBTQ+ qualifiées refusées comme familles d'accueil par des agences d'adoption financées par l'État.",
     "LGFR", "lgbtq_foster_fam"),

    # Wave 1108 — Santé: spécialités médicales (inédits)
    ("chronic_pain_opioid_taper_rights_engine.py",
     "Réduction forcée des opioïdes des patients souffrant de douleur chronique & crise thérapeutique", "Wave 1108",
     "Patients douleur chronique stabilisés dont les médecins réduisent brutalement les opioïdes sous pression réglementaire.",
     "CPOT", "chronic_pain_taper"),
    ("sleep_apnea_cpap_coverage_rights_engine.py",
     "Couverture des dispositifs CPAP pour l'apnée du sommeil & critères d'assurance restrictifs", "Wave 1108",
     "Patients avec apnée du sommeil diagnostiquée refusés pour un dispositif CPAP par des critères d'utilisation contraignants.",
     "SACR", "sleep_apnea_cpap"),
    ("inflammatory_bowel_biologic_rights_engine.py",
     "Accès aux biothérapies pour les maladies inflammatoires de l'intestin & refus de couverture par step therapy", "Wave 1108",
     "Patients Crohn ou rectocolite refusés pour des biologiques en première intention obligés d'échouer avec des immunosuppresseurs.",
     "IBBR", "ibd_biologic"),

    # Wave 1109 — Immigration: familles & procédures (inédits)
    ("mixed_status_family_benefit_rights_engine.py",
     "Familles à statut migratoire mixte & peur de perdre des aides fédérales pour les membres citoyens", "Wave 1109",
     "Citoyens américains dans des familles mixtes évitant les aides auxquelles ils ont droit par peur des conséquences.",
     "MSFB", "mixed_status_family"),
    ("asylum_court_backlog_rights_engine.py",
     "Arriéré des tribunaux d'immigration & délais de décision d'asile de plusieurs années", "Wave 1109",
     "Demandeurs d'asile attendant 3 à 7 ans une décision définitive dans un système judiciaire d'immigration en surcharge.",
     "ABLR", "asylum_court_backlog"),
    ("immigration_judge_shortage_rights_engine.py",
     "Pénurie de juges d'immigration & violations du droit à une audience dans des délais raisonnables", "Wave 1109",
     "Personnes en procédure d'expulsion attendant des années une audience par manque de juges d'immigration disponibles.",
     "IJSR", "immig_judge_short"),

    # Wave 1110 — Finance personnelle: banque & crédit (inédits)
    ("overdraft_fee_trap_rights_engine.py",
     "Frais de découvert excessifs & pratiques prédatrices des banques ciblant les ménages vulnérables", "Wave 1110",
     "Clients bancaires payant des frais de découvert répétés sur de petites transactions par des politiques de reordering.",
     "ODFT", "overdraft_fee_trap"),
    ("check_cashing_fee_unbanked_rights_engine.py",
     "Frais de cambiste pour les non-bancarisés & absence d'alternative bancaire abordable", "Wave 1110",
     "Personnes sans compte bancaire payant des frais élevés de cambiste pour encaisser leurs chèques de paie.",
     "CCFR", "check_cash_unbanked"),
    ("secured_credit_fraud_protection_rights_engine.py",
     "Fraude sur les cartes de crédit sécurisées pour mauvais crédit & droits des victimes aux remboursements", "Wave 1110",
     "Consommateurs avec mauvais crédit utilisant des cartes sécurisées victimes de fraude sans protection égale au crédit ordinaire.",
     "SCFR", "secured_credit_fraud"),

    # Wave 1111 — Éducation: besoins spéciaux & inclusion (inédits)
    ("iep_dispute_resolution_rights_engine.py",
     "Litiges sur les Plans d'Éducation Individualisés & obstacles aux droits des familles d'enfants handicapés", "Wave 1111",
     "Parents d'enfants handicapés incapables de faire appliquer les plans IEP par les districts scolaires récalcitrants.",
     "IEDR", "iep_dispute"),
    ("gifted_education_access_rights_engine.py",
     "Accès aux programmes pour enfants surdoués & inégalités raciales dans l'identification des élèves", "Wave 1111",
     "Enfants noirs et latinos sous-représentés dans les programmes surdoués par des critères d'identification biaisés.",
     "GEAR", "gifted_educ_access"),
    ("section_504_college_rights_engine.py",
     "Plans 504 au niveau universitaire & droits des étudiants handicapés aux aménagements raisonnables", "Wave 1111",
     "Étudiants universitaires avec handicaps documentés refusés pour des aménagements académiques raisonnables demandés.",
     "FPCR", "section504_college"),

    # Wave 1112 — Droits des aînés & discrimination par l'âge (inédits)
    ("elder_financial_abuse_bank_rights_engine.py",
     "Abus financiers des aînés & responsabilité bancaire dans la détection et la prévention", "Wave 1112",
     "Banques n'alertant pas les familles lors de transactions suspectes sur les comptes de seniors, facilitant les abus.",
     "EFAB", "elder_bank_abuse"),
    ("age_discrimination_tech_sector_rights_engine.py",
     "Discrimination par l'âge dans le secteur technologique & biais des recruteurs contre les candidats seniors", "Wave 1112",
     "Travailleurs de plus de 50 ans systématiquement exclus des recrutements technologiques malgré des compétences actualisées.",
     "ADTS", "age_discrim_tech"),
    ("age_discrimination_performance_review_rights_engine.py",
     "Discrimination par l'âge dans les évaluations de performance & licenciements déguisés de travailleurs seniors", "Wave 1112",
     "Travailleurs seniors recevant des évaluations soudainement mauvaises avant un licenciement massif ciblant les plus âgés.",
     "ADPR", "age_discrim_perform"),
]

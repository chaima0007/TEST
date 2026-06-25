# Specs waves 1073-1080 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : urban_heat_island(existe)→brownfield_redevelopment(BRDR) ; jail_phone(existe)→prison_video_visit(PVVF) ;
#                 sperm_donor(existe)→embryo_donation_adoption(EDAP) ; court_interpreter(existe)→pro_se_litigant(PSLR) ;
#                 eco_anxiety(existe)→long_covid_mental(LCMH) ; social_media_teen(existe)→gaming_disorder_treatment(GDTA)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1073 — Éducation des adultes & reconversion (inédits)
    ("community_college_transfer_credit_rights_engine.py",
     "Transfert de crédits des community colleges & perte de crédits à l'université", "Wave 1073",
     "Étudiants transférant d'un community college à une université perdant des crédits non reconnus, allongeant leurs études.",
     "CCTC", "college_transfer_credit"),
    ("adult_literacy_program_funding_rights_engine.py",
     "Financement des programmes d'alphabétisation adulte & listes d'attente chroniques", "Wave 1073",
     "Adultes illettrés en attente de programmes d'alphabétisation pendant des mois faute de financement suffisant.",
     "ALPF", "adult_literacy_fund"),
    ("trade_school_accreditation_rights_engine.py",
     "Accréditation des écoles de métiers & non-reconnaissance des diplômes par les employeurs", "Wave 1073",
     "Diplômés d'écoles de métiers non accréditées incapables d'utiliser leur formation pour accéder aux emplois ciblés.",
     "TSAC", "trade_school_accred"),

    # Wave 1074 — Travailleurs de plateforme (inédits)
    ("rideshare_driver_deactivation_rights_engine.py",
     "Désactivation arbitraire des chauffeurs de covoiturage & absence de procédure d'appel", "Wave 1074",
     "Chauffeurs Uber/Lyft désactivés sans explication ni procédure d'appel transparente, perdant leur source de revenu principale.",
     "RDDR", "rideshare_deactivate"),
    ("gig_worker_expense_reimbursement_rights_engine.py",
     "Remboursement des frais professionnels des travailleurs gig & absence de protection légale", "Wave 1074",
     "Livreurs et travailleurs gig absorbant les frais de carburant, téléphone et assurance sans remboursement ni déduction.",
     "GWER", "gig_expense_reimb"),
    ("platform_worker_age_discrimination_rights_engine.py",
     "Discrimination par l'âge dans les algorithmes de plateforme & exclusion des travailleurs seniors", "Wave 1074",
     "Travailleurs seniors progressivement déprioritisés par les algorithmes de distribution sans recours anti-discrimination.",
     "PWAD", "platform_age_discrim"),

    # Wave 1075 — Santé au travail: milieux non-traditionnels (inédits)
    ("tattoo_artist_chemical_exposure_rights_engine.py",
     "Exposition chimique des tatoueurs & lacunes de protection OSHA pour les travailleurs indépendants", "Wave 1075",
     "Tatoueurs indépendants exposés à des encres et produits chimiques dangereux sans protection réglementaire OSHA.",
     "TACE", "tattoo_chem_exposure"),
    ("hairdresser_repetitive_strain_rights_engine.py",
     "Troubles musculo-squelettiques des coiffeurs & absence de protections ergonomiques professionnelles", "Wave 1075",
     "Coiffeurs développant des syndromes du canal carpien et douleurs chroniques sans protection worker's comp adéquate.",
     "HRSR", "hairdresser_strain"),
    ("funeral_worker_formaldehyde_rights_engine.py",
     "Exposition au formaldéhyde des embaumeurs & risque de cancer professionnel sous-reconnu", "Wave 1075",
     "Embaumeurs exposés quotidiennement au formaldéhyde cancérigène avec des équipements de protection insuffisants.",
     "FWFR", "funeral_formaldehyde"),

    # Wave 1076 — Droits des prisonniers: communications (inédits)
    ("prison_video_visit_fee_rights_engine.py",
     "Frais excessifs des visites vidéo en prison & barrières financières pour les familles", "Wave 1076",
     "Familles de détenus payant des tarifs de vidéo-visite exorbitants imposés par des entreprises privées sous contrat.",
     "PVVF", "prison_video_visit"),
    ("jail_mail_censorship_rights_engine.py",
     "Censure du courrier en prison & violation des droits constitutionnels des détenus", "Wave 1076",
     "Détenus dont le courrier personnel et juridique est censuré ou retardé de manière abusive par l'administration.",
     "JMCR", "jail_mail_censor"),
    ("incarcerated_email_surveillance_rights_engine.py",
     "Surveillance des emails des détenus par les entreprises privées & vie privée carcérale", "Wave 1076",
     "Emails des détenus lus et analysés par des entreprises privées sous contrat sans consentement éclairé.",
     "IESV", "incarcerated_email"),

    # Wave 1077 — Environnement & santé urbaine (inédits)
    ("brownfield_redevelopment_rights_engine.py",
     "Réaménagement des friches industrielles & droits des communautés exposées aux résidus toxiques", "Wave 1077",
     "Résidents vivant près de friches industrielles réaménagées sans décontamination complète, exposés à des métaux lourds.",
     "BRDR", "brownfield_redevelop"),
    ("noise_pollution_industrial_rights_engine.py",
     "Pollution sonore industrielle chronique & droits des riverains à un environnement sonore sain", "Wave 1077",
     "Résidents subissant un bruit industriel continu dépassant les seuils OMS sans recours légal efficace contre les entreprises.",
     "NPIR", "noise_pollut_industr"),
    ("electromagnetic_field_powerline_rights_engine.py",
     "Champs électromagnétiques des lignes électriques & droits des riverains à la santé", "Wave 1077",
     "Propriétaires refusant des lignes à haute tension près de leurs maisons sans compensation ni recours réglementaire.",
     "EMFP", "emf_powerline"),

    # Wave 1078 — Droit de la famille: reproduction assistée (inédits)
    ("surrogate_contract_enforcement_rights_engine.py",
     "Exécution des contrats de gestation pour autrui & droits des parties en cas de litige", "Wave 1078",
     "Mères porteuses ou parents intentionnels dans des États sans loi de GPA, vulnérables en cas de rupture de contrat.",
     "SCER", "surrogate_contract"),
    ("embryo_donation_adoption_rights_engine.py",
     "Adoption d'embryons congelés & droits légaux des donneurs, receveurs et enfants nés", "Wave 1078",
     "Familles utilisant des embryons donnés dans un vide légal, sans statut clair pour les parents génétiques ou adoptifs.",
     "EDAP", "embryo_donation"),
    ("posthumous_reproduction_rights_engine.py",
     "Reproduction post-mortem & utilisation des gamètes congelés d'un conjoint décédé", "Wave 1078",
     "Veuves ou veufs souhaitant utiliser les gamètes congelés de leur conjoint décédé face à des lois incohérentes entre États.",
     "PSTR", "posthumous_reprod"),

    # Wave 1079 — Accès à la justice: coûts & représentation (inédits)
    ("small_claims_court_access_rights_engine.py",
     "Accès aux juridictions de proximité & complexité procédurale pour les justiciables non représentés", "Wave 1079",
     "Plaignants sans avocat dans des juridictions de petites créances faisant face à des règles complexes et des délais impossibles.",
     "SCCA", "small_claims_access"),
    ("legal_aid_waitlist_rights_engine.py",
     "Listes d'attente des services d'aide juridique & pénurie d'avocats pro bono disponibles", "Wave 1079",
     "Justiciables à faibles revenus attendant des mois une représentation légale gratuite, perdant leurs droits en attendant.",
     "LAWR", "legal_aid_waitlist"),
    ("pro_se_litigant_rights_engine.py",
     "Droits des justiciables non représentés & obstacles systémiques dans les tribunaux", "Wave 1079",
     "Personnes se représentant elles-mêmes devant des juges peu accommodants et des greffes inaccessibles sans avocat.",
     "PSLR", "pro_se_litigant"),

    # Wave 1080 — Santé mentale: populations émergentes (inédits)
    ("long_covid_mental_health_rights_engine.py",
     "Santé mentale des patients Covid long & absence de couverture spécialisée par les assureurs", "Wave 1080",
     "Patients Covid long souffrant d'anxiété, de dépression et de brouillard cérébral refusés pour un suivi psychiatrique.",
     "LCMH", "long_covid_mental"),
    ("gaming_disorder_treatment_access_rights_engine.py",
     "Troubles du jeu vidéo & accès au traitement spécialisé non couvert par les assureurs", "Wave 1080",
     "Adolescents et adultes diagnostiqués avec un trouble du jeu vidéo refusés pour un traitement spécialisé non remboursé.",
     "GDTA", "gaming_disorder_treat"),
    ("disaster_survivor_ptsd_rights_engine.py",
     "PTSD des survivants de catastrophes naturelles & accès insuffisant aux soins de santé mentale", "Wave 1080",
     "Survivants d'ouragans, tornades et incendies développant un PTSD sans accès aux soins de santé mentale d'urgence.",
     "DPTA", "disaster_ptsd"),
]

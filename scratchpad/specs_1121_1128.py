# Specs waves 1121-1128 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : prosecutorial_misconduct(existe)→judicial_recusal_bias(JRBS) ;
#                 agricultural_child_labor(existe)→migrant_worker_paycheck_deduction(MWPD) ;
#                 homeless_student_school(existe)→school_suspension_academic_loss(SSAL) ;
#                 credit_invisible_financial(existe)→auto_insurance_redlining(AIRP) ;
#                 rent_to_own_trap(existe)→credit_life_insurance_predatory(CLIP) ;
#                 AMHR(pris)→AMHP ; CSAR(pris)→CPSA ; SCBL(pris)→ZDSL
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1121 — Santé: déficience sensorielle (inédits)
    ("white_cane_pedestrian_priority_rights_engine.py",
     "Priorité aux piétons malvoyants avec canne blanche & refus des conducteurs d'obéir aux lois de sécurité", "Wave 1121",
     "Personnes malvoyantes utilisant une canne blanche ignorées par des conducteurs ne respectant pas la priorité obligatoire.",
     "WCPP", "white_cane_priority"),
    ("braille_signage_public_building_rights_engine.py",
     "Signalétique braille dans les bâtiments publics & non-conformité ADA des propriétaires négligents", "Wave 1121",
     "Personnes aveugles naviguant des bâtiments publics dépourvus de signalétique braille requise par l'ADA.",
     "BRSB", "braille_sign_pub"),
    ("low_vision_eyeglass_coverage_rights_engine.py",
     "Couverture des lunettes pour basse vision & refus des assureurs pour correction optique médicalement nécessaire", "Wave 1121",
     "Patients atteints de basse vision sévère refusés pour une couverture des lunettes prescrites par leur ophtalmologue.",
     "LVEC", "low_vision_eyeglass"),

    # Wave 1122 — Justice: preuves & défense (inédits)
    ("bite_mark_forensic_evidence_rights_engine.py",
     "Preuves forensiques de morsures & manque de fiabilité scientifique des expertises odontologiques en procès", "Wave 1122",
     "Accusés condamnés sur la base d'expertises en morsures désavouées par la communauté scientifique sans voie d'appel.",
     "BMFE", "bite_mark_forensic"),
    ("jailhouse_informant_testimony_rights_engine.py",
     "Témoignages de délateurs détenus & droits des accusés à contester la fiabilité des témoins en échange d'avantages", "Wave 1122",
     "Accusés condamnés par des délateurs incarcérés recevant des réductions de peine sans divulgation complète au jury.",
     "JITR", "jailhouse_inform"),
    ("judicial_recusal_bias_rights_engine.py",
     "Récusation des juges pour conflit d'intérêts & droit des justiciables à un tribunal impartial garanti", "Wave 1122",
     "Justiciables confrontés à des juges refusant de se récuser malgré des liens financiers ou personnels avec une partie.",
     "JRBS", "judicial_recusal"),

    # Wave 1123 — Travail: conditions sectorielles (inédits)
    ("rideshare_driver_vehicle_cost_rights_engine.py",
     "Frais véhicule non remboursés aux chauffeurs de covoiturage & calcul du revenu net en-dessous du salaire minimum", "Wave 1123",
     "Chauffeurs VTC supportant seuls les coûts d'entretien, d'assurance et d'amortissement sans remboursement de la plateforme.",
     "RDVC", "rideshare_veh_cost"),
    ("hotel_tip_pooling_wage_rights_engine.py",
     "Partage des pourboires dans l'hôtellerie & droits des employés face aux politiques de pooling abusives", "Wave 1123",
     "Personnel hôtelier dont les pourboires sont redistribués à des superviseurs ou à la direction dans des systèmes de pooling illégaux.",
     "HTPW", "hotel_tip_pool"),
    ("migrant_worker_paycheck_deduction_rights_engine.py",
     "Déductions abusives sur salaires des travailleurs migrants pour logement & transport imposés par l'employeur", "Wave 1123",
     "Travailleurs migrants logés par leur employeur subissant des déductions de logement excessives réduisant le salaire net sous le minimum.",
     "MWPD", "migrant_worker_pay"),

    # Wave 1124 — Logement: propriété & saisie (inédits)
    ("zombie_foreclosure_property_rights_engine.py",
     "Propriétés zombie entre procédures de saisie & responsabilité du propriétaire nominal non notifié", "Wave 1124",
     "Propriétaires croyant avoir perdu leur maison dans une saisie mais restant légalement responsables des impôts et amendes.",
     "ZFPR", "zombie_foreclos"),
    ("land_bank_property_redemption_rights_engine.py",
     "Droit de rédemption des propriétés saisies par les land banks & délais insuffisants pour les propriétaires originaux", "Wave 1124",
     "Propriétaires seniors ou malades ayant perdu leur bien pour petites dettes fiscales sans information sur le droit de rachat.",
     "LBRR", "land_bank_redempt"),
    ("condo_special_assessment_rights_engine.py",
     "Charges spéciales de copropriété imposées sans vote régulier & droits des copropriétaires à contester", "Wave 1124",
     "Copropriétaires soumis à des charges spéciales de dizaines de milliers de dollars imposées sans vote démocratique conforme.",
     "CPSA", "condo_spec_assess"),

    # Wave 1125 — Santé: pédiatrique & adolescent (inédits)
    ("pediatric_dental_medicaid_rights_engine.py",
     "Couverture dentaire Medicaid pour enfants & refus de prestataires de traiter les bénéficiaires Medicaid", "Wave 1125",
     "Enfants Medicaid incapables de trouver un dentiste acceptant leur couverture dans des déserts dentaires urbains.",
     "PDMR", "pediatric_dental"),
    ("childhood_obesity_insurance_rights_engine.py",
     "Programmes de gestion de l'obésité pédiatrique & refus de couverture assurance pour traitements multidisciplinaires", "Wave 1125",
     "Enfants obèses avec complications médicales refusés pour des programmes multidisciplinaires de gestion du poids couverts.",
     "COIR", "childhood_obes"),
    ("adolescent_mental_health_hospitalization_rights_engine.py",
     "Hospitalisations psychiatriques des adolescents & refus d'admission malgré une crise aiguë documentée", "Wave 1125",
     "Adolescents en crise suicidaire aiguë refusés par des établissements psychiatriques faute de lits disponibles en réseau.",
     "AMHP", "adoles_mh_hosp"),

    # Wave 1126 — Éducation: discrimination & accès (inédits)
    ("school_dress_code_racial_hair_rights_engine.py",
     "Codes vestimentaires scolaires ciblant les coiffures afro & discrimination raciale institutionnelle non reconnue", "Wave 1126",
     "Élèves noirs suspendus ou punis pour des coiffures naturelles ou afro culturellement significatives par des codes vestimentaires.",
     "SDHR", "school_dress_hair"),
    ("english_learner_academic_tracking_rights_engine.py",
     "Relégation des apprenants d'anglais dans des voies non académiques & droits à une éducation équitable", "Wave 1126",
     "Élèves apprenant l'anglais systématiquement orientés vers des voies non académiques limitant leurs perspectives à long terme.",
     "ELTA", "english_learn_track"),
    ("school_suspension_academic_loss_rights_engine.py",
     "Suspensions scolaires cumulées & pertes académiques irréparables pour élèves marginalisés suspendus à répétition", "Wave 1126",
     "Élèves, surtout noirs et à besoins spéciaux, accumulant des semaines de suspension sans instruction alternative.",
     "SSAL", "school_suspen_acad"),

    # Wave 1127 — Finance: assurances & protection consommateurs (inédits)
    ("auto_insurance_redlining_rights_engine.py",
     "Tarification discriminatoire de l'assurance automobile selon le code postal & corrélation avec la race", "Wave 1127",
     "Conducteurs dans des quartiers minoritaires payant des primes auto significativement plus élevées pour le même profil de risque.",
     "AIRP", "auto_insur_redlin"),
    ("credit_life_insurance_predatory_rights_engine.py",
     "Assurance-vie crédit imposée sur les prêts à la consommation & manque de transparence des coûts cachés", "Wave 1127",
     "Emprunteurs à faibles revenus souscrivant des prêts avec assurance-vie obligatoire coûteuse sans consentement éclairé.",
     "CLIP", "credit_life_insur"),
    ("zombie_debt_statute_limitation_rights_engine.py",
     "Relance de dettes prescrites par des agences de recouvrement & droits des consommateurs à la prescription", "Wave 1127",
     "Consommateurs harcelés pour des dettes expirées depuis des années ou décennies ignorant leurs droits à la prescription légale.",
     "ZDSL", "zombie_debt_statut"),

    # Wave 1128 — Immigration: statuts spécifiques (inédits)
    ("humanitarian_parole_uncertainty_rights_engine.py",
     "Parole humanitaire révocable & absence de voie vers la résidence permanente pour bénéficiaires en attente", "Wave 1128",
     "Bénéficiaires de parole humanitaire vivant dans l'incertitude d'une révocation sans possibilité d'ajustement de statut.",
     "HPUR", "human_parole"),
    ("cuban_haitian_entrant_benefits_rights_engine.py",
     "Bénéfices limités des entrants cubains et haïtiens & inégalités avec d'autres statuts d'admission", "Wave 1128",
     "Cubains et Haïtiens ayant un statut d'entrant inéligibles à certaines aides fédérales accessibles aux réfugiés admis.",
     "CHEB", "cuban_haitian_entry"),
    ("immigration_medical_deferred_action_rights_engine.py",
     "Action différée médicale & expulsion de patients en traitement vital sans examen humanitaire suffisant", "Wave 1128",
     "Patients sans papiers sous dialyse, chimiothérapie ou traitement vital menacés d'expulsion sans mécanisme formel de protection.",
     "IMDA", "immig_medical_defer"),
]

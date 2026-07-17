# Specs waves 1137-1144 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : voter_registration_purge(existe)→ranked_choice_voting_access(RCVA) ;
#                 voting_machine_paper_audit(existe)→absentee_ballot_witness(ABWR) ;
#                 worker_misclassification(existe)→overtime_white_collar_exemption(OWCE) ;
#                 charity_fraud_donation(existe)→investment_fraud_promissory_note(IFPN) ;
#                 elder_scam_ai_voice(existe)→grandparent_scam_wire_transfer(GSWT) ;
#                 drought_water_rationing(existe)→water_rights_prior_appropriation(WRPA) ;
#                 stormwater_fee_low_income(existe)→combined_sewer_overflow(CSOR) ;
#                 public_housing_waitlist(existe)→housing_choice_voucher_portability(HCVP) ;
#                 inclusionary_zoning_weak(existe)→affordable_housing_trust_fund(AHTF) ;
#                 HLAR(pris)→AHTF
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1137 — Justice: droits électoraux (inédits)
    ("felon_voting_rights_restoration_rights_engine.py",
     "Restauration des droits de vote après libération & obstacles administratifs dans les États restrictifs", "Wave 1137",
     "Ex-détenus libérés ignorant que leurs droits de vote sont automatiquement restaurés ou bloqués dans leur État de résidence.",
     "FVRR", "felon_vote_restore"),
    ("ranked_choice_voting_access_rights_engine.py",
     "Accès au vote préférentiel & droits des électeurs à utiliser des systèmes alternatifs adoptés démocratiquement", "Wave 1137",
     "Électeurs dans des États ayant adopté le vote préférentiel bloqués par des législatures annulant les résultats de référendum.",
     "RCVA", "ranked_choice_vote"),
    ("absentee_ballot_witness_requirement_rights_engine.py",
     "Exigences de témoins pour bulletins d'absence & impact sur les seniors et les électeurs handicapés isolés", "Wave 1137",
     "Électeurs âgés ou handicapés incapables de trouver un témoin requis pour leur bulletin d'absence annulé pour vice de forme.",
     "ABWR", "absent_ballot_witn"),

    # Wave 1138 — Travail: avantages & exemptions (inédits)
    ("employee_non_compete_agreement_rights_engine.py",
     "Accords de non-concurrence abusifs & restriction injustifiée de la mobilité professionnelle des travailleurs", "Wave 1138",
     "Travailleurs à bas salaires liés par des accords de non-concurrence les empêchant de changer d'employeur dans leur secteur.",
     "ENCA", "employee_non_compete"),
    ("pension_freeze_private_employer_rights_engine.py",
     "Gel des pensions à prestations définies par des employeurs privés & droits des employés aux avantages acquis", "Wave 1138",
     "Employés à mi-carrière voyant leur pension gelée et convertie en 401k sans compensation pour la réduction des avantages futurs.",
     "PFPE", "pension_freeze_priv"),
    ("overtime_white_collar_exemption_rights_engine.py",
     "Exemption d'heures supplémentaires pour cols blancs & abus du seuil de salaire pour refuser l'overtime", "Wave 1138",
     "Employés reclassés comme managers exempts sans vraie autorité managériale pour éviter de payer les heures supplémentaires.",
     "OWCE", "overtime_white_col"),

    # Wave 1139 — Logement: bruit & nuisances de voisinage (inédits)
    ("neighbor_noise_ordinance_enforcement_rights_engine.py",
     "Application des ordonnances sur le bruit du voisinage & inaction des municipalités face aux plaintes répétées", "Wave 1139",
     "Résidents déposant des dizaines de plaintes pour bruit excessif sans que les autorités locales n'imposent de sanctions.",
     "NNOE", "neighbor_noise_ord"),
    ("condo_short_term_rental_nuisance_rights_engine.py",
     "Nuisances des locataires Airbnb dans les copropriétés & droits des copropriétaires à faire respecter le règlement", "Wave 1139",
     "Copropriétaires subissant des nuisances de locataires Airbnb dans des immeubles sans interdiction efficace des locations courtes.",
     "CSTR", "condo_str_nuisance"),
    ("construction_noise_residential_rights_engine.py",
     "Bruit de construction prolongé dans les zones résidentielles & droits des riverains à des horaires limités", "Wave 1139",
     "Résidents proches de chantiers de construction avec bruit excessif avant 7h ou après 22h sans recours municipal efficace.",
     "CNRR", "construct_noise_res"),

    # Wave 1140 — Santé mentale au travail (inédits)
    ("employee_assistance_program_confidentiality_rights_engine.py",
     "Confidentialité des programmes d'aide aux employés & risques de divulgation à l'employeur par les prestataires", "Wave 1140",
     "Employés hésitant à utiliser les PAE par crainte que leurs problèmes de santé mentale soient partagés avec leur employeur.",
     "EAPC", "emp_assist_confid"),
    ("workplace_mental_health_disclosure_rights_engine.py",
     "Divulgation de la santé mentale au travail & risques de discrimination malgré les protections ADA et GINA", "Wave 1140",
     "Employés atteints de troubles mentaux hésitant à divulguer leur état pour obtenir des accommodements par peur des représailles.",
     "WMHD", "work_mh_disclos"),
    ("psychiatric_service_dog_workplace_rights_engine.py",
     "Chiens de service psychiatriques en milieu professionnel & droits des travailleurs face aux refus des employeurs", "Wave 1140",
     "Travailleurs avec PTSD ou anxiété sévère se voyant refuser leur chien de service psychiatrique certifié par l'employeur.",
     "PSDR", "psych_svc_dog_work"),

    # Wave 1141 — Finance: arnaques & fraude consommateurs (inédits)
    ("investment_fraud_promissory_note_rights_engine.py",
     "Fraude aux billets à ordre pour petits investisseurs âgés & récupération des fonds perdus via la régulation", "Wave 1141",
     "Seniors victimes de fraudes aux faux billets à ordre promettant des rendements élevés sans recours efficace contre les fraudeurs.",
     "IFPN", "invest_fraud_promiss"),
    ("grandparent_scam_wire_transfer_rights_engine.py",
     "Arnaque au grand-parent par virement bancaire & responsabilité des banques dans la détection des transferts suspects", "Wave 1141",
     "Seniors envoyant des milliers de dollars par virement à des arnaqueurs se faisant passer pour un petit-enfant en détresse.",
     "GSWT", "grandpar_scam_wire"),
    ("social_security_impersonation_scam_rights_engine.py",
     "Usurpation d'identité de la SSA par téléphone & droits des victimes à la récupération de leurs pertes financières", "Wave 1141",
     "Contribuables bernés par des arnaqueurs se présentant comme agents de la SSA menaçant de suspension de prestations.",
     "SSGR", "ss_impersonation"),

    # Wave 1142 — Immigration: enfants & famille (inédits)
    ("unaccompanied_minor_legal_guardian_rights_engine.py",
     "Tuteurs légaux pour mineurs non accompagnés en procédures d'immigration & absence de représentation garantie", "Wave 1142",
     "Enfants mineurs seuls en procédures d'immigration sans avocat garanti face à des procureurs gouvernementaux expérimentés.",
     "UMGR", "unacomp_minor_guard"),
    ("us_citizen_child_deported_parent_rights_engine.py",
     "Enfants citoyens américains séparés de parents déportés & droits à l'unité familiale et à la garde", "Wave 1142",
     "Enfants nés aux États-Unis contraints de suivre leurs parents déportés ou de rester seuls sans tuteur légal désigné.",
     "UCDP", "citizen_child_deport"),
    ("immigrant_children_school_access_rights_engine.py",
     "Accès à l'école publique pour enfants sans statut légal & garanties Plyler vs Doe menacées par les États", "Wave 1142",
     "Enfants de familles sans papiers confrontés à des demandes de preuve de statut légal pour s'inscrire à l'école publique.",
     "ICER", "immig_child_school"),

    # Wave 1143 — Environnement: eau & contamination (inédits)
    ("agricultural_runoff_nitrate_well_rights_engine.py",
     "Contamination des puits ruraux par le ruissellement agricole nitrate & droits des propriétaires à l'eau potable", "Wave 1143",
     "Propriétaires de puits ruraux avec eau contaminée par les nitrates agricoles dépassant les normes EPA sans compensation.",
     "ARNW", "agri_nitrate_well"),
    ("water_rights_prior_appropriation_rights_engine.py",
     "Droits d'eau en régime d'appropriation préalable & petits agriculteurs évincés par grands utilisateurs seniors", "Wave 1143",
     "Petits agriculteurs dans des États à doctrine d'appropriation perdant leur accès à l'eau au profit de détenteurs de droits anciens.",
     "WRPA", "water_prior_approp"),
    ("combined_sewer_overflow_resident_rights_engine.py",
     "Déversements d'égouts combinés dans les cours d'eau & droits des riverains à la qualité de l'eau et à l'indemnisation", "Wave 1143",
     "Résidents vivant près de cours d'eau contaminés par des débordements d'égouts combinés lors de fortes pluies sans recours.",
     "CSOR", "combined_sewer_over"),

    # Wave 1144 — Logement: accès & modifications (inédits)
    ("housing_choice_voucher_portability_rights_engine.py",
     "Portabilité des bons Section 8 entre comtés & obstacles administratifs limitant les choix résidentiels", "Wave 1144",
     "Bénéficiaires de vouchers Section 8 incapables de déménager dans des comtés plus riches en raison d'obstacles administratifs.",
     "HCVP", "voucher_portability"),
    ("fair_housing_disability_modification_rights_engine.py",
     "Modifications raisonnables du logement pour personnes handicapées & refus illégaux des propriétaires privés", "Wave 1144",
     "Locataires handicapés refusés pour des modifications raisonnables par des propriétaires ignorant leurs obligations légales.",
     "FHDM", "fair_hous_disab_mod"),
    ("affordable_housing_trust_fund_rights_engine.py",
     "Fonds fiduciaires de logement abordable sous-financés & impact sur la production de logements accessibles locaux", "Wave 1144",
     "Municipalités détournant les fonds fiduciaires de logement abordable sans construire les unités promises aux résidents pauvres.",
     "AHTF", "afford_hous_trust"),
]

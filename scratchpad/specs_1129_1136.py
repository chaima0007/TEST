# Specs waves 1129-1136 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : ai_hiring_bias(existe)→biometric_data_employee(BDER) ;
#                 ai_performance_termination(existe)→employer_social_media_screening(ESMS) ;
#                 source_of_income_discrimin(existe)→rental_applicant_criminal_history(RACR) ;
#                 college_athlete_nil(existe)→student_athlete_scholarship_renewal(SASH) ;
#                 fetal_personhood_law(existe)→emergency_abortion_emtala(EAER) ;
#                 miscarriage_criminal_prosecution(existe)→ivf_embryo_destruction(IEDP) ;
#                 medication_abortion_access(existe)→abortion_travel_workplace_rights(ATWR)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1129 — Santé: conditions chroniques émergentes (inédits)
    ("lyme_disease_chronic_diagnosis_rights_engine.py",
     "Maladie de Lyme chronique & déni diagnostique par les assureurs et guidelines médicaux restrictifs", "Wave 1129",
     "Patients souffrant de symptômes persistants de Lyme chronique refusés pour des traitements prolongés non reconnus par les assureurs.",
     "LCDR", "lyme_chronic_diag"),
    ("mold_illness_tenant_disclosure_rights_engine.py",
     "Moisissures toxiques dans les logements locatifs & obligation de divulgation du propriétaire non appliquée", "Wave 1129",
     "Locataires développant des maladies respiratoires chroniques dans des logements à moisissures cachées sans recours légal efficace.",
     "MITD", "mold_tenant_disclos"),
    ("long_covid_disability_workplace_rights_engine.py",
     "Long COVID comme handicap reconnu & droits aux accommodements raisonnables au travail refusés", "Wave 1129",
     "Travailleurs atteints de long COVID demandant des accommodements de travail refusés par des employeurs niant le diagnostic.",
     "LCDW", "long_covid_work"),

    # Wave 1130 — Justice: système carcéral avancé (inédits)
    ("prison_classification_housing_rights_engine.py",
     "Classement des détenus & placement abusif en unités de haute sécurité sans procédure contradictoire", "Wave 1130",
     "Détenus classés à tort dans des niveaux de sécurité élevés sans possibilité de contestation ou de révision équitable.",
     "PCSR", "prison_classif"),
    ("gang_validation_prison_rights_engine.py",
     "Validation de gang en prison & placement à l'isolement sans preuves suffisantes ni voie d'appel formelle", "Wave 1130",
     "Détenus désignés membres de gang sur la base de tatouages ou d'associations et placés en isolement indéfini sans audience.",
     "GVPR", "gang_valid_prison"),
    ("parole_technical_violation_rights_engine.py",
     "Révocations de liberté conditionnelle pour violations techniques & réincarcération disproportionnée", "Wave 1130",
     "Libérés conditionnels réincarcérés pour des violations techniques mineures sans rapport avec de nouveaux crimes violents.",
     "PRTR", "parole_tech_violat"),

    # Wave 1131 — Technologie: surveillance & droits numériques (inédits)
    ("biometric_data_employee_collection_rights_engine.py",
     "Collecte de données biométriques des employés sans consentement éclairé & protection insuffisante BIPA", "Wave 1131",
     "Employés soumis à la reconnaissance faciale ou aux scans d'empreintes pour le pointage sans option de refus.",
     "BDER", "biometric_employ"),
    ("employer_social_media_screening_rights_engine.py",
     "Vérification des réseaux sociaux des candidats à l'embauche & discrimination cachée sur bases protégées", "Wave 1131",
     "Employeurs fouillant les profils personnels des candidats et discriminant sur des caractéristiques protégées découvertes en ligne.",
     "ESMS", "employ_social_screen"),
    ("ring_camera_police_data_sharing_rights_engine.py",
     "Partage de données de caméras Ring avec les forces de l'ordre sans mandat & atteinte à la vie privée", "Wave 1131",
     "Résidents dont les vidéos de caméras connectées sont partagées automatiquement avec la police sans leur consentement explicite.",
     "RCPS", "ring_police_share"),

    # Wave 1132 — Logement: discrimination locative (inédits)
    ("rental_applicant_criminal_history_rights_engine.py",
     "Refus de logement locatif pour casier judiciaire ancien & absence de politique équitable de second chance", "Wave 1132",
     "Ex-détenus réhabilités refusés systématiquement par des propriétaires vérifiant les casiers sans politique individualisée.",
     "RACR", "rental_crim_hist"),
    ("rental_application_fee_abuse_rights_engine.py",
     "Frais de candidature locative non remboursés après refus & pratiques prédatrices des grands propriétaires", "Wave 1132",
     "Candidats locataires payant des frais de candidature à répétition à des propriétaires qui n'ont jamais l'intention de louer.",
     "RAFA", "rental_app_fee"),
    ("rental_history_report_error_rights_engine.py",
     "Erreurs dans les rapports d'historique locatif & droit des candidats à contester les informations inexactes", "Wave 1132",
     "Candidats refusés pour des logements en raison d'erreurs dans leurs rapports d'historique locatif sans mécanisme de correction.",
     "RHER", "rental_hist_err"),

    # Wave 1133 — Droits reproductifs: post-Roe niches (inédits)
    ("abortion_travel_workplace_leave_rights_engine.py",
     "Droits des employés à prendre congé pour voyage vers un État autorisant l'avortement & protections fédérales", "Wave 1133",
     "Employées dans des États restrictifs forcées de voyager pour des soins reproductifs et risquant leur emploi pour ce faire.",
     "ATWR", "abort_travel_work"),
    ("ivf_embryo_legal_status_rights_engine.py",
     "Statut juridique des embryons FIV & impact des lois sur la personnalité fœtale sur les droits des patients", "Wave 1133",
     "Patients FIV confrontés à la destruction ou à l'impossibilité de disposer des embryons gelés sous des lois d'État restrictives.",
     "IEDP", "ivf_embryo_legal"),
    ("emergency_abortion_emtala_rights_engine.py",
     "Conflit EMTALA vs lois anti-avortement & droits des femmes en urgence obstétricale dans les États restrictifs", "Wave 1133",
     "Femmes en urgence obstétricale dans des États restrictifs confrontées à des médecins refusant d'intervenir par peur légale.",
     "EAER", "emtala_abort_emerg"),

    # Wave 1134 — Santé: assurance & couverture niches (inédits)
    ("experimental_treatment_appeal_rights_engine.py",
     "Appel contre refus de traitements expérimentaux par les assureurs & accès aux essais cliniques non couverts", "Wave 1134",
     "Patients en fin de vie refusés pour des traitements expérimentaux prometteurs non couverts sans voie d'appel rapide.",
     "ETAR", "exp_treat_appeal"),
    ("insurance_overpayment_clawback_rights_engine.py",
     "Récupération des trop-perçus d'assurance auprès des médecins & impact sur la continuité des soins patients", "Wave 1134",
     "Patients dont les médecins arrêtent de les soigner après que les assureurs ont massivement récupéré des trop-perçus.",
     "ICOP", "insur_overp_claw"),
    ("prior_authorization_emergency_rights_engine.py",
     "Délais d'autorisation préalable en situation d'urgence médicale & droits des patients à des soins immédiats", "Wave 1134",
     "Patients en urgence médicale confrontés à des délais d'autorisation préalable retardant un traitement potentiellement salvateur.",
     "PADE", "prior_auth_emerg"),

    # Wave 1135 — Éducation: financement & opportunités (inédits)
    ("school_funding_property_tax_inequity_rights_engine.py",
     "Inégalités de financement scolaire basées sur l'impôt foncier & droit constitutionnel à l'éducation équitable", "Wave 1135",
     "Élèves dans des districts pauvres recevant un financement scolaire per capita plusieurs fois inférieur aux districts riches.",
     "SFPE", "school_fund_prop"),
    ("vocational_education_access_rights_engine.py",
     "Accès à la formation professionnelle dans les lycées pauvres & suppression des programmes CTE par manque de budget", "Wave 1135",
     "Élèves dans les lycées à faibles revenus privés de programmes de formation professionnelle par manque de financement fédéral.",
     "VEAR", "vocat_educ_access"),
    ("student_athlete_scholarship_renewal_rights_engine.py",
     "Renouvellement des bourses sportives universitaires & révocations pour blessure ou désaccord avec l'entraîneur", "Wave 1135",
     "Athlètes universitaires perdant leurs bourses après blessures ou conflits avec l'entraîneur sans procédure d'appel formelle.",
     "SASH", "stud_athlete_schol"),

    # Wave 1136 — Communautés: droits spécifiques (inédits)
    ("deaf_prisoner_interpretation_rights_engine.py",
     "Droit des détenus sourds à l'interprétation en langue des signes & accès aux procédures judiciaires", "Wave 1136",
     "Détenus sourds sans interprète en langue des signes lors des audiences disciplinaires ou judiciaires en prison.",
     "DPIR", "deaf_prison_interp"),
    ("native_american_voter_id_rights_engine.py",
     "Lois d'identité électorale discriminant les Amérindiens sans adresse fixe ou résidant dans des réserves", "Wave 1136",
     "Membres de tribus amérindiennes ne pouvant voter faute d'adresse de rue sur leur ID pour des réserves sans numérotation.",
     "NAVR", "native_voter_id"),
    ("lgbtq_homeless_youth_shelter_rights_engine.py",
     "Hébergement des jeunes LGBTQ+ sans domicile & refus des refuges religieux d'accepter les mineurs trans", "Wave 1136",
     "Jeunes trans et queer mineurs sans domicile refusés par des refuges subventionnés refusant leur identité de genre.",
     "LHYS", "lgbtq_youth_shelter"),
]

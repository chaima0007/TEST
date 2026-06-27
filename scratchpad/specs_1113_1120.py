# Specs waves 1113-1120 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : deepfake_intimate(existe)→online_harassment_civil_remedy(OHCR) ;
#                 revenge_porn(existe)→image_based_abuse_app(IBAA) ;
#                 refugee_resettlement_backlog(existe)→daca_marriage_green_card(DMGC) ;
#                 CCSW(pris)→CCWL ; SPSS(pris)→SPSC ; LPRR(pris)→LPNR
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1113 — Travailleurs: exploitation spécifique (inédits)
    ("supply_chain_worker_safety_rights_engine.py",
     "Sécurité des travailleurs de la chaîne d'approvisionnement & violations OSHA non sanctionnées", "Wave 1113",
     "Travailleurs d'entrepôts et centres de distribution exposés à des risques graves sans inspections OSHA régulières.",
     "SWLS", "supply_chain_safety"),
    ("prison_medical_copay_rights_engine.py",
     "Copaiements médicaux en prison & barrière financière aux soins pour détenus sans revenu", "Wave 1113",
     "Détenus malades incapables de consulter en raison de copaiements médicaux représentant des semaines de salaire carcéral.",
     "PRMC", "prison_medical_copay"),
    ("social_worker_caseload_burnout_rights_engine.py",
     "Surcharge des travailleurs sociaux & épuisement professionnel systémique dans les services de protection", "Wave 1113",
     "Travailleurs sociaux gérant des centaines de cas à la fois, incapables de protéger adéquatement les enfants vulnérables.",
     "SCBT", "social_worker_burnout"),

    # Wave 1114 — Santé: maternité & fertilité (inédits)
    ("midwife_licensing_restriction_rights_engine.py",
     "Restrictions de licence des sages-femmes indépendantes & criminalisation des accouchements à domicile", "Wave 1114",
     "Sages-femmes expérimentées criminalisées dans des États refusant de les licencier pour des accouchements à domicile sécurisés.",
     "MWLC", "midwife_licensing"),
    ("fertility_cancer_preservation_rights_engine.py",
     "Préservation de la fertilité pendant le traitement du cancer & refus de couverture par les assureurs", "Wave 1114",
     "Patients en chimiothérapie refusés pour une couverture de la congélation d'ovocytes ou de sperme avant le traitement.",
     "FPCN", "fertility_cancer"),
    ("postpartum_depression_coverage_rights_engine.py",
     "Dépression post-partum & accès insuffisant au dépistage et traitement pour les nouvelles mères", "Wave 1114",
     "Nouvelles mères souffrant de dépression post-partum sévère refusées pour un traitement couvert par leur assureur.",
     "PPDC", "postpartum_depression"),

    # Wave 1115 — Technologie & abus numériques (inédits)
    ("stalkerware_domestic_violence_rights_engine.py",
     "Stalkerware et logiciels de surveillance dans les relations abusives & droits des victimes à la détection", "Wave 1115",
     "Victimes de violence domestique surveillées via des applications de stalkerware cachées sur leur téléphone sans recours.",
     "SBDV", "stalkerware_dv"),
    ("image_based_abuse_deepfake_rights_engine.py",
     "Abus basés sur des images deepfake intimes & absence de lois fédérales de protection des victimes", "Wave 1115",
     "Victimes de deepfakes pornographiques non consentis créés avec l'IA sans recours légal uniforme entre États.",
     "IBAA", "image_abuse_deepfake"),
    ("online_harassment_civil_remedy_rights_engine.py",
     "Harcèlement en ligne & droits des victimes à des recours civils efficaces contre les harceleurs anonymes", "Wave 1115",
     "Victimes de campagnes de harcèlement en ligne coordonnées incapables d'identifier et poursuivre les harceleurs anonymes.",
     "OHCR", "online_harass_civil"),

    # Wave 1116 — Infrastructure & accessibilité urbaine (inédits)
    ("sidewalk_accessibility_wheelchair_rights_engine.py",
     "Accessibilité des trottoirs pour les utilisateurs de fauteuils roulants & obligation municipale d'entretien", "Wave 1116",
     "Personnes en fauteuil roulant bloquées par des trottoirs défectueux ou inexistants sans voie de recours municipale.",
     "SWAR", "sidewalk_wheelchair"),
    ("crosswalk_pedestrian_safety_rights_engine.py",
     "Sécurité des piétons aux carrefours & responsabilité municipale pour les traversées dangereuses non sécurisées", "Wave 1116",
     "Piétons tués ou blessés à des carrefours signalés dangereux depuis longtemps sans action municipale correctrice.",
     "CPSR", "crosswalk_safe"),
    ("urban_tree_heat_equity_rights_engine.py",
     "Équité dans la plantation d'arbres urbains & désert de végétation dans les quartiers défavorisés", "Wave 1116",
     "Quartiers à majorité minoritaire subissant des températures estivales plus élevées par manque d'arbres et espaces verts.",
     "UTHE", "urban_tree_equity"),

    # Wave 1117 — Finance: impôts & fraude fiscale (inédits)
    ("tax_preparer_fraud_rights_engine.py",
     "Fraude des préparateurs de déclarations fiscales & droits des victimes à récupérer les remboursements volés", "Wave 1117",
     "Contribuables à faibles revenus victimes de préparateurs fiscaux non réglementés détournant leurs remboursements IRS.",
     "TPFD", "tax_preparer_fraud"),
    ("irs_audit_racial_bias_rights_engine.py",
     "Biais racial dans les audits IRS & sur-représentation des déclarants du crédit EITC parmi les audités", "Wave 1117",
     "Contribuables noirs et pauvres audités à des taux disproportionnés par des algorithmes IRS ciblant les crédits d'impôt.",
     "IRAB", "irs_audit_racial"),
    ("tax_lien_property_rights_engine.py",
     "Privilèges fiscaux sur propriétés & saisies abusives pour petites dettes d'impôt foncier impayées", "Wave 1117",
     "Propriétaires âgés perdant leur maison familiale saisie par des investisseurs pour de petites dettes fiscales impayées.",
     "TLPR", "tax_lien_prop"),

    # Wave 1118 — Environnement: nuisances voisinage (inédits)
    ("industrial_farm_odor_rights_engine.py",
     "Odeurs des fermes industrielles porcines et aviaires & droits des riverains à la qualité de vie", "Wave 1118",
     "Résidents vivant près de grandes fermes industrielles subissant des odeurs d'ammoniaque sans recours légal efficace.",
     "IFOD", "industrial_farm_odor"),
    ("light_pollution_residential_rights_engine.py",
     "Pollution lumineuse excessive des installations commerciales & impact sur la santé et le sommeil des riverains", "Wave 1118",
     "Riverains dont le sommeil est perturbé par des enseignes commerciales ou parkings éclairés toute la nuit sans limites.",
     "LPNR", "light_pollut_resident"),
    ("gun_range_neighbor_rights_engine.py",
     "Pollution sonore des stands de tir en plein air & droits des riverains à un environnement calme", "Wave 1118",
     "Riverains de stands de tir en plein air subissant des tirs quotidiens sans protection légale contre le bruit excessif.",
     "GRNR", "gun_range_noise"),

    # Wave 1119 — Droits des parents & famille (inédits)
    ("parental_leave_small_employer_rights_engine.py",
     "Congé parental pour les employés des petits employeurs & exclusions des lois FMLA et PFML étatiques", "Wave 1119",
     "Nouveaux parents travaillant pour des employeurs de moins de 50 personnes exclus des congés parentaux protégés.",
     "PLSE", "parental_leave_small"),
    ("single_parent_school_schedule_rights_engine.py",
     "Parents monoparentaux & obstacles aux horaires scolaires contraignants sans flexibilité au travail", "Wave 1119",
     "Parents seuls risquant leur emploi à chaque fermeture scolaire ou rendez-vous obligatoire sans flexibilité patronale.",
     "SPSC", "single_parent_sched"),
    ("child_care_subsidy_waitlist_rights_engine.py",
     "Listes d'attente des subventions publiques pour la garde d'enfants & années d'attente pour les familles pauvres", "Wave 1119",
     "Familles à faibles revenus éligibles aux subventions de garde d'enfants attendant des années sur des listes d'attente.",
     "CCWL", "childcare_subsidy_wait"),

    # Wave 1120 — Immigration: communautés spécifiques (inédits)
    ("haitian_tps_rights_engine.py",
     "Statut de protection temporaire des Haïtiens & instabilité des renouvellements selon l'administration", "Wave 1120",
     "Ressortissants haïtiens sous TPS menacés de perte de statut à chaque changement d'administration sans solution durable.",
     "HTPS", "haitian_tps"),
    ("daca_marriage_green_card_rights_engine.py",
     "Bénéficiaires DACA mariés à des citoyens américains & blocage de la voie vers la résidence permanente", "Wave 1120",
     "Bénéficiaires DACA mariés à des citoyens incapables d'ajuster leur statut sans quitter les États-Unis sous peine de bannissement.",
     "DMGC", "daca_marriage_gc"),
    ("visa_overstay_family_hardship_rights_engine.py",
     "Dépassement de visa par des personnes aux attaches familiales profondes & droit à l'examen des situations exceptionnelles", "Wave 1120",
     "Personnes ayant dépassé leur visa avec des enfants citoyens et des décennies de vie américaine soumises à l'expulsion.",
     "VOFH", "visa_overstay_family"),
]

# Specs waves 1169-1176 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : dark_pattern_website(existe×5)→social_media_autoplay_addiction(SMAA) ;
#                 subscription_cancellation(existe×3)→free_trial_auto_renewal(FTAR) ;
#                 ira_rollover_fraud(existe)→deferred_compensation_457_plan(DCPR) ;
#                 retirement_401k_fee(existe)→pension_multiemployer_insolvency(PMIS) ;
#                 mandatory_reporter_failure(existe)→child_protective_services_investigation(CPSI) ;
#                 tenant_sublease_prohibition(existe)→tenant_lease_assignment(TLAR)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1169 — Santé: femmes (niches inédites)
    ("ovarian_cancer_screening_rights_engine.py",
     "Dépistage du cancer de l'ovaire & absence de test validé et refus de couverture pour tests de surveillance", "Wave 1169",
     "Femmes à risque élevé de cancer de l'ovaire sans test de dépistage approuvé couvert et sans surveillance adaptée.",
     "OCSR", "ovarian_cancer_screen"),
    ("breast_density_notification_rights_engine.py",
     "Notification obligatoire de la densité mammaire & droits des femmes à une information sur leur risque de cancer", "Wave 1169",
     "Femmes avec seins très denses non informées du risque accru de cancer et de la limite de la mammographie standard.",
     "BDIN", "breast_density_notif"),
    ("gynecology_access_rural_rights_engine.py",
     "Accès aux gynécologues en zones rurales & droits des femmes à des soins gynécologiques de base près de chez elles", "Wave 1169",
     "Femmes en zones rurales parcourant des heures pour accéder à un gynécologue pour des soins préventifs et reproductifs essentiels.",
     "GARR", "gynecol_rural"),

    # Wave 1170 — Justice: droits pénitentiaires (inédits)
    ("prison_law_library_access_rights_engine.py",
     "Accès aux bibliothèques juridiques en prison & droit constitutionnel des détenus à l'assistance judiciaire", "Wave 1170",
     "Détenus pro se incapables de préparer leurs recours en raison de bibliothèques juridiques supprimées ou d'accès limité.",
     "PLLR", "prison_law_lib"),
    ("prison_work_program_rights_engine.py",
     "Programmes de travail carcéral & droits des détenus à des compensations équitables et conditions de sécurité", "Wave 1170",
     "Détenus obligés de travailler pour des entreprises privées via des programmes de prison labor sans droits du travail applicables.",
     "PWPR", "prison_work_prog"),
    ("prison_education_program_rights_engine.py",
     "Programmes éducatifs en prison & droit à l'alphabétisation et à la formation professionnelle pendant la détention", "Wave 1170",
     "Détenus dans des établissements ayant supprimé les programmes d'éducation par manque de budget sans alternative de formation.",
     "PEPR", "prison_educ_prog"),

    # Wave 1171 — Emploi: protection contre les représailles (inédits)
    ("nlrb_union_organizing_retaliation_rights_engine.py",
     "Représailles lors de l'organisation syndicale & protections NLRB trop lentes pour protéger les organisateurs", "Wave 1171",
     "Travailleurs licenciés pour avoir organisé un syndicat avec des procédures NLRB trop longues pour être un deterrent efficace.",
     "NRUO", "nlrb_union_retaliat"),
    ("protected_concerted_activity_rights_engine.py",
     "Activités concertées protégées des employés & licenciements pour discussions salariales entre collègues", "Wave 1171",
     "Employés licenciés pour avoir discuté de leurs salaires avec des collègues, une activité protégée par la loi fédérale NLRA.",
     "PCAR", "protect_conc_activ"),
    ("workers_compensation_retaliation_rights_engine.py",
     "Représailles contre les employés demandant des compensations accidents du travail & licenciements déguisés", "Wave 1171",
     "Travailleurs blessés sur le lieu de travail licenciés ou rétrogradés peu après avoir déposé une demande de compensation.",
     "WCRR", "workers_comp_retal"),

    # Wave 1172 — Finance: retraite & investissements (inédits)
    ("pension_multiemployer_insolvency_rights_engine.py",
     "Insolvabilité des régimes de retraite multiemployeurs & menace sur les retraites des travailleurs syndiqués", "Wave 1172",
     "Travailleurs d'industries en déclin confrontés à des réductions de pension de 40-60% suite à l'insolvabilité de leur régime.",
     "PMIS", "pension_multiemploy"),
    ("deferred_compensation_457_plan_rights_engine.py",
     "Plans de rémunération différée 457 pour employés publics & risques de saisie en cas de faillite de l'employeur", "Wave 1172",
     "Employés municipaux découvrant que leurs économies 457 sont des actifs non protégés en cas de faillite de leur ville.",
     "DCPR", "defer_comp_457"),
    ("broker_fiduciary_duty_retirement_rights_engine.py",
     "Devoir fiduciaire des conseillers financiers pour les comptes retraite & conflits d'intérêts cachés aux clients", "Wave 1172",
     "Retraités perdant des milliers de dollars suite à des recommandations intéressées de conseillers sans obligation fiduciaire.",
     "BFDR", "broker_fiduc_retire"),

    # Wave 1173 — Santé: fin de vie & soins palliatifs (inédits)
    ("hospice_curative_treatment_access_rights_engine.py",
     "Accès aux traitements curatifs pour les patients en soins palliatifs & obligation de choisir entre hospice et traitement", "Wave 1173",
     "Patients en phase terminale contraints d'abandonner les traitements curatifs pour accéder aux soins palliatifs couverts.",
     "HDCT", "hospice_curative"),
    ("palliative_care_early_access_rights_engine.py",
     "Accès précoce aux soins palliatifs & résistance des oncologues à l'intégration des soins de confort simultanément", "Wave 1173",
     "Patients atteints de cancer avancé privés de soins palliatifs précoces par des médecins qui les réservent aux dernières semaines.",
     "PCEA", "palliat_early_acc"),
    ("death_with_dignity_access_rights_engine.py",
     "Accès à l'aide médicale à mourir dans les États autorisant la mort dans la dignité & barrières pratiques persistantes", "Wave 1173",
     "Patients souffrant de maladies terminales dans des États autorisant la mort assistée incapables de trouver un médecin coopérant.",
     "DWDR", "death_dignity_acc"),

    # Wave 1174 — Technologie: vie privée & manipulation (inédits)
    ("social_media_autoplay_addiction_rights_engine.py",
     "Autoplay et design addictif des réseaux sociaux & droits des mineurs à une protection contre les techniques manipulatrices", "Wave 1174",
     "Adolescents dont la santé mentale est affectée par des fonctionnalités addictives de scrolling infini et d'autoplay conçues délibérément.",
     "SMAA", "social_autoplay_addict"),
    ("free_trial_auto_renewal_trap_rights_engine.py",
     "Piège des essais gratuits avec renouvellement automatique & droits des consommateurs à la résiliation sans obstacles", "Wave 1174",
     "Consommateurs abonnés automatiquement à prix plein après un essai gratuit avec processus de résiliation délibérément complexe.",
     "FTAR", "free_trial_auto"),
    ("children_online_privacy_coppa_rights_engine.py",
     "Protection COPPA de la vie privée des enfants en ligne & violations massives par des apps non conformes", "Wave 1174",
     "Enfants de moins de 13 ans dont les données personnelles sont collectées par des apps non conformes à COPPA sans sanctions effectives.",
     "COPR", "child_online_privacy"),

    # Wave 1175 — Logement: locataires niches (inédits)
    ("tenant_lease_assignment_rights_engine.py",
     "Cession de bail à un successeur & refus arbitraires des propriétaires bloquant les transitions légitimes", "Wave 1175",
     "Locataires devant quitter leur logement incapables de céder leur bail à un tiers qualifié sans raison valable du propriétaire.",
     "TLAR", "tenant_lease_assign"),
    ("domestic_violence_lease_break_rights_engine.py",
     "Résiliation de bail pour victimes de violence domestique & droits légaux de quitter le logement partagé sans pénalité", "Wave 1175",
     "Victimes de violence domestique incapables de quitter le logement commun sans payer des mois de loyer en pénalité de résiliation.",
     "RDVR", "dv_lease_break"),
    ("lease_early_termination_fee_rights_engine.py",
     "Frais de résiliation anticipée abusifs dans les baux résidentiels & absence de plafonnement légal dans de nombreux États", "Wave 1175",
     "Locataires devant payer plusieurs mois de loyer en frais de résiliation anticipée pour des circonstances inévitables comme un emploi.",
     "LETR", "lease_early_term"),

    # Wave 1176 — Droits des enfants: protection (inédits)
    ("child_witness_testimony_trauma_rights_engine.py",
     "Droits des enfants témoins dans les procédures pénales & traumatisme de la confrontation avec l'accusé", "Wave 1176",
     "Enfants victimes ou témoins contraints de témoigner face à face avec leur agresseur adulte dans les tribunaux pénaux.",
     "CWTR", "child_witness_test"),
    ("child_protective_services_investigation_rights_engine.py",
     "Droits des familles lors d'investigations CPS & risques d'intervention disproportionnée dans des familles pauvres", "Wave 1176",
     "Familles pauvres faisant l'objet d'enquêtes CPS basées sur des signalements de pauvreté confondue avec de la négligence.",
     "CPSI", "cps_investigation"),
    ("child_abduction_hague_convention_rights_engine.py",
     "Enlèvements parentaux internationaux & application incomplète de la Convention de La Haye par des pays signataires", "Wave 1176",
     "Parents dont l'enfant a été emmené à l'étranger par l'autre parent confrontés à des pays ignorant les demandes de retour Hague.",
     "CAHC", "hague_abduct"),
]

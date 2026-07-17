# Specs waves 1153-1160 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : qualified_immunity_police(existe)→consent_decree_police_reform(CDPR) ;
#                 stop_frisk_racial(existe)→bank_account_levy_judgment(BALJ) ;
#                 civil_forfeiture_reform(existe)→(évité en Wave 1154) ;
#                 ergonomic_injury_warehouse(existe)→poultry_worker_injury(PWIR) ;
#                 nurse_staffing_ratio(existe)→dental_hygienist_ergonomic(DHER) ;
#                 wildfire_evacuation_poor(existe)→wildfire_smoke_indoor_air(WSIAR) ;
#                 dental_school_clinic_access(existe)→vision_care_medicare(VCMR conservé, différent)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1153 — Santé: assurance invalidité ERISA (inédits)
    ("long_term_disability_insurance_erisa_rights_engine.py",
     "Refus de pensions d'invalidité long terme ERISA & procédures d'appel biaisées en faveur des assureurs", "Wave 1153",
     "Assurés atteints de maladies chroniques graves dont les pensions d'invalidité long terme sont refusées ou révoquées par ERISA.",
     "LTDE", "lte_disab_erisa"),
    ("erisa_mental_health_parity_rights_engine.py",
     "Parité santé mentale sous ERISA & applications insuffisantes aux plans d'assurance autoassurés des grandes entreprises", "Wave 1153",
     "Employés de grandes entreprises avec plans autoassurés se voyant refuser la parité de couverture santé mentale garantie par ERISA.",
     "EMHP", "erisa_mh_parity"),
    ("short_term_disability_pregnancy_rights_engine.py",
     "Assurance invalidité court terme pour grossesse & exclusions préexistantes dans les États sans PFML", "Wave 1153",
     "Femmes enceintes dans des États sans loi de congé payé familly medical leave incapables d'accéder à l'assurance court terme.",
     "STDP", "short_disab_preg"),

    # Wave 1154 — Justice: droits civils & police (inédits)
    ("civil_commitment_sex_offender_rights_engine.py",
     "Engagement civil indéfini des délinquants sexuels après peine purgée & double punition sans fondement clinique", "Wave 1154",
     "Délinquants sexuels ayant purgé leur peine emprisonnés à nouveau par engagement civil pour des années sans voie de libération.",
     "CCSO", "civil_commit_sex"),
    ("consent_decree_police_reform_rights_engine.py",
     "Consentements decree pour réforme policière & droits des communautés à l'application effective des engagements pris", "Wave 1154",
     "Communautés vivant sous des décrets de consentement policiers dont les réformes promises ne sont pas implémentées par les services.",
     "CDPR", "consent_decr_police"),
    ("bank_account_levy_judgment_rights_engine.py",
     "Prélèvements bancaires pour dettes judiciaires & gel de comptes sans notification adéquate préalable des débiteurs", "Wave 1154",
     "Débiteurs découvrant leur compte bancaire gelé du jour au lendemain pour des jugements anciens sans notification préalable.",
     "BALJ", "bank_levy_judgment"),

    # Wave 1155 — Finance: cryptomonnaies & actifs numériques (inédits)
    ("crypto_exchange_investor_recovery_rights_engine.py",
     "Récupération pour investisseurs victimes de faillites d'exchanges crypto & statut de créancier non sécurisé", "Wave 1155",
     "Investisseurs ayant perdu des économies dans des faillites d'exchanges crypto classés comme créanciers non prioritaires.",
     "CIER", "crypto_exch_invest"),
    ("nft_fraud_buyer_protection_rights_engine.py",
     "Fraudes aux NFTs & absence de protection légale adéquate pour les acheteurs victimes d'arnaques et rug pulls", "Wave 1155",
     "Investisseurs en NFTs victimes de rug pulls ou de collections frauduleuses sans recours légal contre les créateurs anonymes.",
     "NFTF", "nft_fraud_buyer"),
    ("crypto_tax_compliance_small_investor_rights_engine.py",
     "Conformité fiscale crypto pour petits investisseurs & complexité disproportionnée des obligations de déclaration IRS", "Wave 1155",
     "Petits investisseurs crypto submergés par des obligations de déclaration de chaque transaction même minime à l'IRS.",
     "CTRR", "crypto_tax_small"),

    # Wave 1156 — Santé dentaire & visuelle (inédits)
    ("adult_dental_medicaid_coverage_rights_engine.py",
     "Couverture dentaire Medicaid pour adultes & absences dans de nombreux États laissant des millions sans soins oraux", "Wave 1156",
     "Adultes pauvres dans des États sans couverture dentaire Medicaid incapables d'accéder à des soins oraux préventifs essentiels.",
     "ADMC", "adult_dental_medicaid"),
    ("vision_care_medicare_coverage_rights_engine.py",
     "Absence de couverture visuelle dans Medicare standard & accès insuffisant aux lunettes pour seniors", "Wave 1156",
     "Bénéficiaires Medicare découvrant que leur assurance ne couvre pas les examens de vue ni les lunettes de prescription.",
     "VCMR", "vision_medicare_cov"),
    ("dental_emergency_hospital_rights_engine.py",
     "Urgences dentaires dans les salles d'urgence hospitalières & absence de traitement réel pour douleurs orales aiguës", "Wave 1156",
     "Patients se rendant aux urgences pour des abcès dentaires sévères renvoyés avec des antibiotiques sans traitement dentaire.",
     "DEHR", "dental_emerg_hosp"),

    # Wave 1157 — Éducation: enseignement supérieur & équité (inédits)
    ("first_generation_college_student_rights_engine.py",
     "Étudiants de première génération & manque de soutien institutionnel pour naviguer l'enseignement supérieur", "Wave 1157",
     "Étudiants dont aucun parent n'est allé à l'université ignorant des processus d'aide financière, de bourse et d'académique.",
     "FGCS", "first_gen_college"),
    ("college_legacy_admission_equity_rights_engine.py",
     "Admissions préférentielles pour enfants d'anciens élèves & impact sur l'équité des candidats de première génération", "Wave 1157",
     "Candidats qualifiés rejetés par des universités favorisant les enfants d'anciens élèves et de donateurs dans leurs admissions.",
     "CLAE", "legacy_admit_equity"),
    ("community_college_funding_inequity_rights_engine.py",
     "Sous-financement des community colleges & inégalités de ressources avec les universités de recherche de l'État", "Wave 1157",
     "Étudiants dans des community colleges recevant nettement moins de financement par étudiant que leurs pairs dans les universités d'État.",
     "CCFI", "comm_coll_fund_ineq"),

    # Wave 1158 — Immigration: procédures spéciales (inédits)
    ("diversity_visa_lottery_backlog_rights_engine.py",
     "Arriéré de la loterie de visas de diversité & délais d'interview consulaire prolongeant l'incertitude des gagnants", "Wave 1158",
     "Gagnants de la loterie de visas de diversité incapables d'obtenir leur visa avant l'expiration annuelle de leur sélection.",
     "VLDB", "div_visa_backlog"),
    ("naturalization_processing_delay_rights_engine.py",
     "Délais de traitement de la naturalisation & impact sur le droit de vote et les avantages réservés aux citoyens", "Wave 1158",
     "Résidents permanents attendant des années la finalisation de leur naturalisation malgré des dossiers complets et approuvés.",
     "NDLR", "natural_proc_delay"),
    ("consular_visa_interview_backlog_rights_engine.py",
     "Arriéré des interviews de visa consulaire & séparations familiales prolongées pour immigrants en attente", "Wave 1158",
     "Familles séparées pendant des années car les interviews de visa d'immigrant sont repoussées de plusieurs années dans de nombreux consulats.",
     "CIBR", "consular_visa_back"),

    # Wave 1159 — Travail: sécurité & conditions spécifiques (inédits)
    ("poultry_worker_injury_rights_engine.py",
     "Blessures des travailleurs d'abattoirs avicoles & protections OSHA insuffisantes dans l'industrie de la volaille", "Wave 1159",
     "Travailleurs d'abattoirs de volaille souffrant de lésions musculosquelettiques chroniques sur des chaînes de vitesse excessive.",
     "PWIR", "poultry_work_injury"),
    ("heat_stress_outdoor_construction_rights_engine.py",
     "Stress thermique des travailleurs de la construction en extérieur & absence de norme OSHA nationale sur la chaleur", "Wave 1159",
     "Travailleurs du bâtiment exposés à des températures extrêmes sans pauses eau-ombre-repos imposées par une norme fédérale.",
     "HSOC", "heat_stress_constr"),
    ("dental_hygienist_ergonomic_workplace_rights_engine.py",
     "Conditions ergonomiques des hygiénistes dentaires & troubles musculosquelettiques chroniques ignorés par les cabinets", "Wave 1159",
     "Hygiénistes dentaires développant des troubles du canal carpien et de la nuque chroniques sans accommodements ergonomiques.",
     "DHER", "dental_hyg_ergo"),

    # Wave 1160 — Environnement: justice climatique (inédits)
    ("heat_emergency_cooling_center_rights_engine.py",
     "Droit aux centres de refroidissement lors de canicules & fermetures de centres et transports insuffisants pour les vulnérables", "Wave 1160",
     "Personnes âgées et pauvres sans climatisation mourant de chaleur car les centres de refroidissement publics sont inaccessibles.",
     "HECC", "heat_cool_center"),
    ("floodplain_insurance_nfip_affordability_rights_engine.py",
     "Primes d'assurance inondation NFIP inabordables & obligation d'assurance pour les propriétaires en zone inondable", "Wave 1160",
     "Propriétaires en zone inondable contraints d'acheter une assurance NFIP dont les primes ont triplé les rendant insolvables.",
     "FINR", "floodplain_nfip"),
    ("wildfire_smoke_indoor_air_rights_engine.py",
     "Qualité de l'air intérieur pendant les feux de forêt & droits des locataires à des logements avec filtration adéquate", "Wave 1160",
     "Locataires dans des unités sans filtration d'air adéquate exposés à la fumée de feux de forêt sans recours contre le propriétaire.",
     "WSIAR", "wildfire_smoke_air"),
]

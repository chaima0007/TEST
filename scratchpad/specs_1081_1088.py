# Specs waves 1081-1088 — 24 nouveaux moteurs de droits humains
# Préfixes vérifiés : 0 collision externe, 0 doublon interne
# Remplacements : immigration_bond_hearing(existe)→immigration_detention_medical(IDMR) ;
#                 rare_disease_clinical_trial(existe)→enzyme_replacement_therapy_access(ERTA) ;
#                 ai_art_copyright(existe)→fashion_design_copyright(FDCP)
# (filename, title, wave, desc, prefix, idx)
SPECS = [
    # Wave 1081 — Sécurité des armes à feu (inédits)
    ("firearm_safe_storage_mandate_rights_engine.py",
     "Lois de stockage sécurisé des armes à feu & obligations des propriétaires en matière de sécurité", "Wave 1081",
     "Propriétaires d'armes poursuivis après qu'un enfant a accédé à l'arme familiale mal sécurisée, sans loi claire.",
     "FSSG", "firearm_safe_storage"),
    ("ghost_gun_victim_rights_engine.py",
     "Victimes de ghost guns sans numéro de série & absence de recours contre les fabricants de kits", "Wave 1081",
     "Victimes de crimes commis avec des ghost guns incapables de poursuivre les fabricants de pièces non réglementées.",
     "GGVR", "ghost_gun_victim"),
    ("red_flag_law_due_process_rights_engine.py",
     "Lois Red Flag de confiscation temporaire & droits de procédure régulière pour les propriétaires", "Wave 1081",
     "Propriétaires d'armes dont les armes sont saisies sous des ordres Red Flag sans représentation légale préalable.",
     "RFDP", "red_flag_due_process"),

    # Wave 1082 — Logement mobile & précaire (inédits)
    ("mobile_home_park_rent_increase_rights_engine.py",
     "Augmentations de loyer dans les parcs de maisons mobiles & droits des résidents propriétaires de mobile homes", "Wave 1082",
     "Résidents propriétaires de leur mobile home mais locataires du terrain subissant des hausses de loyer illimitées.",
     "MHRL", "mobile_home_rent"),
    ("hotel_tenant_eviction_rights_engine.py",
     "Évictions des locataires d'hôtels et motels résidentiels & droits des résidents de longue durée", "Wave 1082",
     "Personnes vivant dans des hôtels à la semaine acquérant des droits de locataire après 30 jours mais expulsées sans procédure.",
     "HTEV", "hotel_tenant_evict"),
    ("car_dwelling_enforcement_rights_engine.py",
     "Application des lois anti-campement contre les personnes vivant dans leur véhicule & droits civils", "Wave 1082",
     "Personnes sans domicile vivant dans leur voiture confrontées à des amendes répétées et saisies de véhicule sans alternative.",
     "CDEW", "car_dwelling_enforce"),

    # Wave 1083 — Droits des vétérans (inédits)
    ("veteran_disability_rating_error_rights_engine.py",
     "Erreurs dans l'évaluation du taux d'invalidité des vétérans & appels du système VA", "Wave 1083",
     "Vétérans recevant des taux d'invalidité sous-évalués par le VA, perdant des prestations mensuelles significatives.",
     "VDRE", "veteran_disab_rating"),
    ("veteran_caregiver_support_rights_engine.py",
     "Soutien aux aidants naturels des vétérans gravement blessés & lacunes du programme Program of Comprehensive Assistance", "Wave 1083",
     "Aidants de vétérans grièvement blessés exclus ou désincrits des programmes de soutien du VA sans explication.",
     "VCSR", "veteran_caregiver"),
    ("veteran_fiduciary_abuse_rights_engine.py",
     "Abus fiduciaires par les gestionnaires de pension des vétérans inaptes & responsabilité VA", "Wave 1083",
     "Vétérans déclarés inaptes sous tutelle de fiduciaires désignés par le VA exploitant leurs pensions sans surveillance.",
     "VFAB", "veteran_fiduciary"),

    # Wave 1084 — Alimentation & consommation (inédits)
    ("organic_food_fraud_labeling_rights_engine.py",
     "Fraude aux étiquettes biologiques sur les aliments importés & protection insuffisante des consommateurs", "Wave 1084",
     "Consommateurs achetant des aliments certifiés bio importés frauduleusement étiquetés sans vérification sérieuse.",
     "OFFD", "organic_food_fraud"),
    ("gmo_food_labeling_rights_engine.py",
     "Étiquetage des aliments génétiquement modifiés & droit des consommateurs à l'information sur l'origine", "Wave 1084",
     "Consommateurs incapables d'identifier les aliments OGM en raison d'un système d'étiquetage numérique inaccessible.",
     "GMLB", "gmo_food_label"),
    ("dark_pattern_food_subscription_rights_engine.py",
     "Dark patterns dans les abonnements alimentaires & résiliation impossible pour les consommateurs", "Wave 1084",
     "Abonnés à des services de livraison alimentaire piégés dans des abonnements indésirables sans résiliation simple.",
     "DPFS", "dark_pattern_food"),

    # Wave 1085 — Immigration: procédures légales (inédits)
    ("asylum_medical_evidence_rights_engine.py",
     "Documentation médicale dans les demandes d'asile & accès aux experts médicaux pour les demandeurs", "Wave 1085",
     "Demandeurs d'asile incapables d'obtenir une documentation médicale de tortures ou persécutions pour soutenir leur dossier.",
     "AMEV", "asylum_medical_evid"),
    ("cbp_device_search_rights_engine.py",
     "Fouilles d'appareils électroniques aux frontières & droits constitutionnels des voyageurs", "Wave 1085",
     "Voyageurs dont les téléphones et ordinateurs sont fouillés et copiés aux frontières sans mandat ni cause probable.",
     "CBPS", "cbp_device_search"),
    ("immigration_detention_medical_rights_engine.py",
     "Soins médicaux dans les centres de détention pour immigrants & accès insuffisant aux professionnels de santé", "Wave 1085",
     "Immigrés détenus dans des centres de rétention avec des soins médicaux inadéquats pour des conditions chroniques ou urgentes.",
     "IDMR", "immig_detain_medical"),

    # Wave 1086 — Maladies rares & médicaments orphelins (inédits)
    ("orphan_drug_price_gouging_rights_engine.py",
     "Hausse de prix abusive des médicaments orphelins & inaccessibilité pour les patients atteints de maladies rares", "Wave 1086",
     "Patients atteints de maladies rares confrontés à des prix de médicaments orphelins explosant après des acquisitions privées.",
     "ODPG", "orphan_drug_price"),
    ("compassionate_use_access_rights_engine.py",
     "Accès en compassionate use aux traitements expérimentaux & bureaucratie FDA pour les patients désespérés", "Wave 1086",
     "Patients en phase terminale refusés pour l'accès élargi aux médicaments expérimentaux par des procédures trop longues.",
     "CUAX", "compassionate_use"),
    ("enzyme_replacement_therapy_access_rights_engine.py",
     "Accès aux thérapies de remplacement enzymatique & refus de couverture pour les maladies lysosomales", "Wave 1086",
     "Patients atteints de maladies de stockage lysosomal refusés pour des thérapies enzymatiques vitales par les assureurs.",
     "ERTA", "enzyme_replace_ther"),

    # Wave 1087 — Sports: droits spécifiques (inédits)
    ("masters_athlete_age_discrimination_rights_engine.py",
     "Discrimination par l'âge envers les athlètes masters & exclusion des programmes de financement sportif", "Wave 1087",
     "Athlètes seniors performants exclus des subventions et programmes nationaux de développement sportif réservés aux jeunes.",
     "MAAD", "masters_athlete_age"),
    ("para_athlete_equipment_funding_rights_engine.py",
     "Financement des équipements des para-athlètes & inégalités de soutien face aux athlètes valides", "Wave 1087",
     "Para-athlètes contraints de financer leurs propres prothèses sportives et fauteuils de compétition très coûteux.",
     "PAEF", "para_athlete_equip"),
    ("combat_sport_concussion_protocol_rights_engine.py",
     "Protocoles de commotion cérébrale dans les sports de combat & responsabilité des organisateurs", "Wave 1087",
     "Boxeurs et lutteurs subissant des commotions répétées sans protocoles obligatoires de retrait et de suivi médical.",
     "CSCP", "combat_concussion"),

    # Wave 1088 — Propriété intellectuelle & créateurs (inédits)
    ("music_streaming_royalty_rights_engine.py",
     "Royalties des musiciens indépendants sur les plateformes de streaming & opacité des paiements", "Wave 1088",
     "Musiciens indépendants recevant des fractions de centime par stream sans transparence sur les calculs de royalties.",
     "MSRR", "music_stream_royal"),
    ("fashion_design_copyright_rights_engine.py",
     "Droits d'auteur pour les créateurs de mode & absence de protection légale fédérale des designs vestimentaires", "Wave 1088",
     "Créateurs de mode dont les designs sont copiés immédiatement sans protection légale car les vêtements sont exclus du copyright.",
     "FDCP", "fashion_design_copy"),
    ("podcast_content_theft_rights_engine.py",
     "Vol de contenu podcast & droits des créateurs audio face aux agrégateurs et copieurs", "Wave 1088",
     "Podcasteurs dont les épisodes sont rip et redistribués sans permission, érodant leur audience et revenus publicitaires.",
     "PCTC", "podcast_content"),
]

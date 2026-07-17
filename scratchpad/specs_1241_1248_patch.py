# Patch waves 1241-1248 — 2 remplacements pour SKIPs
# immigration_court_backlog → déjà existant → remplacé par t_visa_trafficking_survivor
# multiple_sclerosis_treatment_access → déjà existant → remplacé par crohn_biologics_access
SPECS = [
    ("t_visa_trafficking_survivor_rights_engine.py",
     "Visa T pour survivants de traite des êtres humains & droits des victimes à une protection et statut légal malgré la non-coopération", "Wave 1243",
     "Survivants de traite des personnes éligibles au visa T incapables d'obtenir le statut car ils ne peuvent coopérer avec les forces de l'ordre.",
     "TVSA", "t_visa_trafficking"),
    ("crohn_disease_biologic_access_rights_engine.py",
     "Accès aux thérapies biologiques pour la maladie de Crohn & refus d'assurance exigeant l'échec de traitements moins efficaces", "Wave 1244",
     "Patients atteints de la maladie de Crohn sévère contraints d'essayer et d'échouer des médicaments standard avant d'accéder aux biologiques.",
     "CRKN", "crohn_biologic_access"),
]

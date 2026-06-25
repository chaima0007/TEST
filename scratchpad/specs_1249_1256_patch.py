# Patch waves 1249-1256 — 2 remplacements pour SKIPs
# college_athlete_nil → existe déjà → remplacé par college_athlete_mental_health
# medicaid_estate_recovery → doublon sémantique estate_recovery_medicaid → remplacé par veteran_pension_survivor
SPECS = [
    ("college_athlete_mental_health_rights_engine.py",
     "Santé mentale des athlètes universitaires & droits à un accès garanti à des services de counseling sans stigmatisation ni pression", "Wave 1254",
     "Athlètes universitaires souffrant de dépression ou d'anxiété découragés de chercher de l'aide par des cultures d'entraînement qui stigmatisent la santé mentale.",
     "CAMH", "college_athlete_mental"),
    ("veteran_pension_surviving_spouse_rights_engine.py",
     "Pension de survivant VA pour les conjoints de vétérans & obstacles bureaucratiques privant les veuves de leurs allocations légitimes", "Wave 1256",
     "Conjoints survivants de vétérans éligibles à la Dependency and Indemnity Compensation DIC incapables de naviguer les demandes sans aide spécialisée.",
     "VPSW", "vet_pension_survivor"),
]

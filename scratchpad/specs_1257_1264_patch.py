# Patch waves 1257-1264 — 1 remplacement pour SKIP
# fertility_preservation_cancer → doublon sémantique fertility_cancer_preservation → remplacé par recurrent_pregnancy_loss
SPECS = [
    ("recurrent_pregnancy_loss_investigation_rights_engine.py",
     "Droits à l'investigation médicale après fausses couches à répétition & refus d'assurance pour les bilans de pertes de grossesse répétées", "Wave 1264",
     "Personnes ayant subi 2 à 3 fausses couches consécutives se voyant refuser les bilans diagnostiques pour identifier les causes traitables.",
     "RPLM", "recurrent_preg_loss"),
]

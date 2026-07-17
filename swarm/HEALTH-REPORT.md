# 🩺 Rapport de santé — projet agents (swarm)

_Diagnostic non destructif (collecte des tests). Aucune modification de code effectuée._

## Résultat global : ✅ SAIN
- **57 827 tests** se chargent correctement (lancés depuis le dossier `swarm/`).
- Seulement **10 erreurs de collecte** sur 255 fichiers de tests (~96 % OK).

> ⚠️ Important : lancer les tests **depuis `swarm/`** (`cd swarm && python3 -m pytest tests`),
> sinon les imports `intelligence.*` échouent (ce n'est pas un bug, juste le bon chemin).

## Les 10 erreurs (aucune n'est grave)

### A. Bibliothèques externes non installées (8) — décision d'environnement
- `crewai` manquant → 7 fichiers (tests des divisions 1-6, linkedin_scheduler…)
- `fastapi` manquant → 1 fichier (test_stripe_webhook)
- **Ce n'est PAS un bug du code.** Pour les activer : `pip install crewai fastapi`
  (à décider — ces libs sont lourdes ; à installer seulement si on en a besoin).

### B. Décalages de noms (2) — décision de nommage (à valider)
1. **test_sales_territory_coverage_intelligence_engine.py**
   - Le module contient une **faute de frappe** : `SalesTerritoryConverageIntelligenceEngine`
     (devrait être `...Coverage...`).
   - Le test attend aussi `TerritoryCoverageInput/Result`, `CoverageRisk/Pattern/Severity/Action`,
     alors que le module expose `TerritoryInput/Result`, `TerritoryRisk/Pattern/Severity/Action`.
   - **Question** : quel nom est canonique ? (corriger le module risque de casser ses importateurs)
2. **test_sales_stakeholder_mapping_intelligence_engine.py**
   - Test attend `StakeholderMappingInput` / `StakeholderMappingResult`.
   - Module expose `StakeholderInput` / `StakeholderResult`.
   - **Question** : on aligne le test sur le module, ou l'inverse ?

## Recommandation
- A → me dire si on installe `crewai` + `fastapi` (sinon, ces tests restent ignorés sans impact).
- B → me dire le nom canonique ; je corrige module + tests + importateurs de façon cohérente.
  (Je n'ai rien touché pour ne pas casser d'autres parties sans ton accord.)

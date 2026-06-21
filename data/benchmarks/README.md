# Dataset Benchmarks Comparatifs

## Objectif

Comparer les scores Caelum Partners avec des indices tiers reconnus (académiques et ONG) afin de valider la corrélation de nos engines avec des données indépendantes. Ces benchmarks servent à :

1. Renforcer la crédibilité scientifique de notre plateforme auprès des clients Enterprise
2. Identifier les domaines où nos scores divergent et investiguer les causes
3. Alimenter les decks commerciaux avec des preuves de corrélation

---

## Sources de données

| Indice | Organisation | Domaines couverts | Fréquence |
|---|---|---|---|
| WJP Rule of Law Index | World Justice Project | Droits fondamentaux, justice, corruption | Annuel |
| Human Freedom Index (HFI) | Cato Institute + Fraser Institute | Libertés civiles, droits économiques | Annuel |
| V-Dem (Varieties of Democracy) | V-Dem Institute | Démocratie, droits politiques, genre | Annuel |
| Global Slavery Index | Walk Free Foundation | Travail forcé, esclavage moderne | Bisannuel |
| Freedom House Freedom in the World | Freedom House | Droits politiques et libertés civiles | Annuel |
| Child Labor Index | ILO / UNICEF | Travail des enfants | Annuel |
| Gender Inequality Index | UNDP | Inégalités de genre | Annuel |

---

## Format des fichiers CSV

### Structure standard
```
country,year,caelum_score,wjp_score,hfi_score,vdem_score,gsi_score,correlation_wjp,correlation_hfi,notes
```

### Colonnes détaillées

| Colonne | Type | Description |
|---|---|---|
| `country` | string (ISO 3166-1 alpha-3) | Code pays (ex: FRA, DEU, USA) |
| `year` | integer | Année des données (ex: 2024) |
| `caelum_score` | float (0–10) | Score composite Caelum (estimated index) |
| `wjp_score` | float (0–1) | Score WJP Rule of Law (0 = faible état de droit) |
| `hfi_score` | float (0–10) | Score Human Freedom Index |
| `vdem_score` | float (0–1) | Score V-Dem Electoral Democracy |
| `gsi_score` | float (0–10) | Score Global Slavery Index (10 = risque élevé) |
| `correlation` | float (-1 à 1) | Corrélation Pearson Caelum vs WJP |
| `domain` | string | Engine Caelum concerné |
| `notes` | string | Observations, outliers |

### Exemple de ligne
```csv
DEU,2024,7.82,0.81,8.73,0.87,2.10,0.89,forced_labor,Forte corrélation WJP
COD,2024,1.43,0.32,3.21,0.21,8.90,-0.12,child_labor,Divergence GSI à investiguer
```

---

## Organisation des fichiers

```
data/benchmarks/
├── README.md                    (ce fichier)
├── forced_labor_2024.csv
├── child_labor_2024.csv
├── land_grabbing_2024.csv
├── gender_gap_2024.csv
├── climate_migration_2024.csv
├── digital_rights_2024.csv
├── prison_labor_2024.csv
├── water_rights_2024.csv
├── indigenous_rights_2024.csv
├── migrant_workers_2024.csv
├── algorithmic_bias_2024.csv
└── correlation_summary_2024.csv (agrégat toutes dimensions)
```

---

## Cycle de mise à jour

- **Fréquence :** Annuel, mise à jour en **juin** (après publication des indices majeurs)
- **Responsable :** Équipe Data / Analyst lead
- **Process :**
  1. Télécharger les dernières données de chaque source (voir liens ci-dessous)
  2. Normaliser les scores sur l'échelle 0–10 pour comparaison
  3. Calculer les corrélations Pearson par domaine
  4. Mettre à jour les CSV + régénérer `correlation_summary_2024.csv`
  5. Commit sur `main` avec tag `benchmarks-YYYY`

---

## Sources et liens

- WJP : https://worldjusticeproject.org/rule-of-law-index/
- HFI : https://www.cato.org/human-freedom-index/
- V-Dem : https://v-dem.net/data/
- Global Slavery Index : https://www.walkfree.org/global-slavery-index/
- Freedom House : https://freedomhouse.org/report/freedom-world
- ILO Child Labour : https://www.ilo.org/global/topics/child-labour/
- UNDP GII : https://hdr.undp.org/data-center/thematic-composite-indices/gender-inequality-index

---

## Utilisation commerciale

Ces benchmarks alimentent :
- Le **Enterprise Pitch Deck** (slide "Pourquoi nous faire confiance ?")
- Les **rapports PDF mensuels** clients (section "Comparaison indices tiers")
- La **page de validation méthodologique** du site public

**Note :** Les données brutes de tiers sont utilisées à des fins de comparaison uniquement. Citer les sources originales dans tout document public.

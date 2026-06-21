# FACTURE N° [YYYY-MM-NNN]

**Émetteur :** Caelum Partners BVBA
Bruxelles, Belgique
TVA : BE[XXXX]
IBAN : BE[XXXX]

**Client :** [NOM CLIENT]
[ADRESSE]
TVA : [N° TVA CLIENT]

**Date :** [DATE]
**Échéance :** [DATE + 30j]

| Description | Qté | Prix HT | Total HT |
|---|---|---|---|
| [Abonnement Easy Access / Enterprise Premium] | 1 mois | [PRIX] | [PRIX] |
| [Add-on éventuel] | 1 | [PRIX] | [PRIX] |

**Sous-total HT :** [X] €
**TVA 21% :** [X] €
**TOTAL TTC :** [X] €

*Paiement par virement SEPA dans les 30 jours.*

---

## Notes d'utilisation du template

### Numérotation
Format : `YYYY-MM-NNN` (ex: `2026-06-001`)
- YYYY = année
- MM = mois
- NNN = numéro séquentiel (remis à zéro chaque année)

### Mentions légales obligatoires (Belgique)
- N° BCE de Caelum Partners BVBA
- N° TVA BE[XXXX]
- IBAN + BIC pour virement
- Mention "En cas de retard de paiement, des intérêts de retard de 10% par an seront appliqués."
- Pour clients EU avec n° TVA valide : ajouter "Autoliquidation TVA — TVA à acquitter par le preneur (art. 194 Directive TVA)"

### Conversion PDF
Utiliser l'un des outils suivants :
- `pandoc template.md -o facture-YYYY-MM-NNN.pdf` (recommandé, nécessite LaTeX)
- Copier-coller dans Google Docs puis exporter en PDF
- Outil dédié Pennylane (si adopté) — génère le PDF directement

### Archivage
Toutes les factures émises doivent être archivées dans :
`docs/invoices/emises/YYYY/facture-YYYY-MM-NNN.pdf`

Conservation légale : 7 ans (obligation comptable belge).

---

## Exemple facture complète

```
# FACTURE N° 2026-06-001

**Émetteur :** Caelum Partners BVBA
Rue de la Science 14, 1040 Bruxelles, Belgique
TVA : BE0XXX.XXX.XXX
IBAN : BE XX XXXX XXXX XXXX — BIC : GEBABEBB

**Client :** Volkswagen Group AG
Berliner Ring 2, 38440 Wolfsburg, Allemagne
TVA : DE XXXXXXXXX

**Date :** 1 juin 2026
**Échéance :** 1 juillet 2026

| Description | Qté | Prix HT | Total HT |
|---|---|---|---|
| Abonnement Enterprise Premium — juin 2026 | 1 mois | 2 900,00 € | 2 900,00 € |
| API Access add-on — juin 2026 | 1 mois | 500,00 € | 500,00 € |

**Sous-total HT :** 3 400,00 €
**TVA 21% :** 714,00 €
**TOTAL TTC :** 4 114,00 €

Autoliquidation TVA — TVA à acquitter par le preneur (art. 194 Directive TVA)

*Paiement par virement SEPA dans les 30 jours.*
*En cas de retard, intérêts de retard de 10%/an applicables.*
```

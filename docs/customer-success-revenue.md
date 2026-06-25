# CaelumSwarm — Réussite client & génération de revenus

> Objectif : que nos clients **réussissent** (donc restent et paient plus), et que
> chaque levier soit relié à un **euro concret**. Analyse honnête, pas du marketing.

---

## 1. Le principe qui fait gagner de l'argent

Dans un SaaS, **80 % des revenus viennent de clients existants** (réabonnement + montée en gamme), pas des nouveaux. Donc la priorité n'est pas « vendre », c'est **rendre le client tellement bien installé qu'il ne peut plus partir**.

> Règle d'or : 1 € dépensé à garder un client rapporte ~5× plus que 1 € dépensé à en trouver un nouveau.

Trois leviers, dans l'ordre :
1. **Activation** — le client obtient un résultat dans les 7 jours
2. **Rétention** — il ne part pas (réduction du « churn »)
3. **Expansion** — il paie plus avec le temps (« land & expand »)

---

## 2. À quoi ressemble « la réussite » POUR le client

| Type de client | Sa réussite = | Ce qu'il paie pour ça |
|----------------|---------------|------------------------|
| Hôpital / institution | Être conforme AI Act / RGPD **sans risque d'amende** | Enterprise 990 €/mo |
| Grande entreprise (CSDDD) | Produire son rapport de vigilance **sans y passer des semaines** | Enterprise → White-label |
| Cabinet de conseil | Revendre la conformité à SES clients | White-label 4 900 €/mo |
| PME / scale-up | Se mettre en règle **avant une levée de fonds** | Pro 99 €/mo |

➡️ On ne vend pas « des engines » — on vend **« dormir tranquille face au régulateur »**.

---

## 3. Ce qu'on met en place (concret) → l'euro associé

### A. Onboarding « time-to-value < 7 jours » 💶 réduit le churn précoce
- Assistant de démarrage : le client connecte ses données → 1er rapport de conformité en < 1h
- Modèle pré-rempli par secteur (santé, finance, industrie)
- **Impact € :** un client qui voit un résultat la 1ʳᵉ semaine a ~2× moins de chances de partir

### B. Tableau de bord de conformité vivant 💶 crée le lock-in
- Score de conformité mis à jour en continu, alertes quand un risque monte
- Historique horodaté et **scellé** (notre `decision_seal`) = preuve auditable
- **Impact € :** plus le client accumule d'historique chez nous, plus partir lui coûte cher → rétention

### C. Rapports « prêts pour le régulateur » en 1 clic 💶 justifie le prix Enterprise
- Export PDF/Gamma conforme AI Act / CSDDD / RGPD
- **Impact € :** ce qui leur prenait 3 semaines de juriste = 10 min → ils paient sans discuter

### D. Score de santé client + intervention proactive 💶 sauve les comptes à risque
- On détecte les clients qui n'utilisent plus la plateforme (signal de départ)
- On les rappelle AVANT qu'ils résilient
- **Impact € :** chaque résiliation évitée = 12 × le tarif mensuel sauvé

### E. Programme de parrainage / études de cas 💶 acquisition quasi gratuite
- Un client satisfait en amène d'autres (surtout entre institutions qui se parlent)
- **Impact € :** coût d'acquisition divisé par 3-5

---

## 4. Les 3 façons de faire grossir un compte (expansion)

1. **Plus de sièges** : 5 utilisateurs → 50 (l'équipe conformité s'agrandit)
2. **Plus de modules** : ajoute CSDDD, puis surveillance fournisseurs, puis audit RGPD
3. **Montée de tier** : Pro → Enterprise → White-label

> Une « expansion » coûte presque rien à vendre (le client est déjà là, déjà convaincu) → **marge quasi pure**.

---

## 5. Chiffrage réaliste (exemple prudent)

Mix an 1 (déjà dans `license_manager_agent.py --revenue`) :
- 500 Free + 80 Pro + 12 Enterprise + 2 White-label → **~355 K€ ARR**

Effet de la réussite client sur 3 ans (hypothèses prudentes) :
| Levier | Effet |
|--------|-------|
| Churn réduit de 5 % → 2 %/mois | +40 % de revenu conservé |
| 30 % des Pro montent en Enterprise | +250 K€/an |
| 1 cabinet White-label de plus | +59 K€/an |

➡️ Le même nombre de clients peut **doubler** le revenu juste par rétention + expansion, **sans** dépenser plus en acquisition.

---

## 6. Honnêteté — ce qui peut tout casser ⚠️

- **Sans onboarding réel**, les clients signent puis n'utilisent pas → churn massif. C'est le risque n°1.
- **Sans juriste partenaire**, on ne peut pas garantir la conformité qu'on vend → crédibilité détruite.
- **Sans données sources réelles** (ONU, Eurostat…), les scores restent indicatifs, pas opposables au régulateur.
- **Le support coûte cher** : un client Enterprise mécontent peut absorber des heures. À budgéter.

> La techno qu'on a construite (sceau, observabilité, gardes) est un **atout réel** pour la crédibilité — mais la réussite client se joue à 50 % sur l'humain (onboarding, support, juridique), pas sur le code.

---

## 7. Priorités concrètes (ce que je peux construire ensuite)

1. **Module « score de santé client »** (réutilise la logique du dashboard account-expansion existant)
2. **Générateur de rapport de conformité 1-clic** (export depuis les engines)
3. **Assistant d'onboarding** (1er résultat en < 1h)

Ces 3 briques sont les plus directement reliées à l'argent (rétention + justification du prix).

---

*Document stratégique vivant — à réviser chaque trimestre.*

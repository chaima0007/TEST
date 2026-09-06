# A-DECIDER — décisions en attente de Chaima

Un seul fichier (§6). Trié par ancienneté, le plus vieux en haut.
Toute entrée de plus de 14 jours est mise en évidence en tête de fichier par CARTOGRAPHE
à chaque snapshot. Aucun agent ne tranche une ligne de ce tableau.

**⚠️ Rien de plus de 14 jours à ce jour.**

---

| Quoi | Projet | Type | En attente depuis | Résumé en 1 ligne |
|---|---|---|---|---|
| Portée réelle de A-DECIDER.md et EVOLUTION.md | Empire | Protocole | 2026-09-06 | Le §6 dit "un seul fichier tous projets confondus", le §12 dit "structure identique dans chaque projet" — les deux ensemble produisent N copies divergentes ; désigner un dépôt canonique ou assumer une copie par projet. |
| Noms de fichiers avec emoji + espace | Empire | Technique | 2026-09-06 | `🔴 ERREURS.md` / `📋 JOURNAL.md` fonctionnent sous Linux/git mais cassent sur certains outils Windows, CI et scripts shell non quotés ; garder tel quel pour la cohérence de l'Empire, ou passer à `ERREURS.md` / `JOURNAL.md` partout. |
| Absence totale de tests automatisés | CompeteIQ | Technique | 2026-09-06 | `package.json` n'a aucun script `test` ; TESTEUR-ADVERSE recommande d'en ajouter un avant toute nouvelle fonctionnalité facturable. Décision : quand, et avec quel budget de temps. |
| Implémenter les 5 rôles §1 restants | Empire | Protocole | 2026-09-06 | SCOUT, CARTOGRAPHE, SCRIBE-EMPIRE, ÉCLAIREUR-OPPORTUNITÉS, ARCHITECTE-INTÉGRATION : aucun déclencheur réel aujourd'hui ; arbitrage du 2026-09-06 = ATTENDRE le déclencheur, pas une date. |

---

## Fiches complètes rattachées

### Fiche DEB-2026-09-06-01 — Compléter les 21 rôles en sous-agents ?

**Proposition cadrée :** implémenter maintenant les 8 rôles §1 restants en sous-agents,
pour porter le système à 21 agents.

**AVOCAT (plaidoirie indépendante).** Un système de gouvernance à moitié construit est pire
qu'aucun : les trous y sont invisibles. Fait vérifié : le §0 fait de l'usage de dépendances
validées « le cœur même du système » — or, avant ce jour, aucun agent ne possédait ce
contrôle, et tout `npm install` court-circuitait le protocole en entier. Le §5 dépendait de
la mémoire de l'agent en cours, exactement la défaillance que le protocole a été écrit pour
empêcher. Coût marginal faible : le travail cher (définir les rôles, le format) est déjà
fait ; il reste des fichiers Markdown. Décision réversible à coût nul.
*Ce qui me ferait changer d'avis :* si le contrôle d'entrée était déjà assuré par la CI et
la revue de code, ces rôles seraient redondants.

**CONTRADICTEUR (plaidoirie indépendante).** L'hypothèse implicite jamais vérifiée est que
le goulot d'étranglement de CompeteIQ serait la **qualité des décisions**. Faits vérifiés
au 2026-09-06 : le dépôt contient VALUATION.md, MARKET_ANALYSIS.md et PITCH_EMAIL.md — et
**aucun script de test**, aucune trace d'entretien client. Le goulot est la validation
commerciale, pas la gouvernance. Coût caché : 21 documents qui doivent rester vrais ;
chacun dérive, et un protocole qui ment est pire qu'aucun protocole. Coût d'opportunité :
chaque session passée sur le protocole n'est pas passée sur le produit, et le §9 désigne le
temps de Chaima comme la ressource la plus rare. Mode de défaillance silencieux : **le
protocole devient le projet**. La cérémonie ressemble à du progrès. boucle-caelum a produit
25 journaux quasi identiques ; le même mal d'un cran au-dessus produit des rôles que
personne n'invoque.
*Ce qui lèverait mon objection :* la preuve d'un usage réel — des fiches effectivement
produites dans les 30 jours.

**SIMULATEUR-SCÉNARIOS.**
*Optimiste* — les 21 rôles en place ; à 1 mois une dépendance passe réellement par
Guardian + Sentinel ; à 6 mois `/codex/expertise/` porte des fiches appliquées sur 2 projets.
*Réaliste* — 4 à 5 agents servent vraiment (contradicteur, testeur-adverse,
verificateur-verite, conservateur-secrets) ; les autres ne sont jamais invoqués ; le
snapshot est fait trois fois puis oublié. Rien de grave n'arrive — mais CLAUDE.md pèse
250 lignes lues à chaque session.
*Pessimiste (ordinaire, pas spectaculaire)* — personne n'invoque rien ; dans trois mois une
nouvelle session lit 21 rôles et n'ose plus en supprimer aucun. Le protocole devient un décor.
*Signal d'alerte précoce à 30 jours :* le nombre de fichiers dans `/codex/candidates/` et
`/codex/expertise/`. Zéro = décor, quel que soit le nombre d'agents.
*Coût du demi-tour :* facile techniquement (supprimer des fichiers), coûteux psychologiquement.
*Confiance :* MODÉRÉE.

**ARBITRE-EXPERT — recommandation : FAIRE MAIS RÉDUIT.**
Implémenter **3 rôles sur 8**, ceux qui ont un déclencheur réel et imminent :
`guardian-licences` et `sentinel-securite` (déclenchés par tout `npm install`, l'événement
le plus fréquent de ce dépôt) et `superviseur-vigie` (propriétaire du snapshot §5).
Les 5 autres restent PROPOSÉ.

*Ce que l'Avocat a gagné et qui est conservé :* la chaîne d'entrée n'avait effectivement
aucun propriétaire — c'était un trou réel, il est bouché aujourd'hui, à coût marginal faible
et réversible.
*Ce que le Contradicteur a gagné et qui devient un garde-fou :* arrêt net à 16 agents au
lieu de 21, **et** une mesure datée — au 2026-10-06, si `/codex/candidates/` et
`/codex/expertise/` sont toujours vides, CROQUE-MORT est invoqué **sur le protocole
lui-même**. Son objection n'est pas écartée : elle devient une condition opposable.
*Désaccord irréductible :* le goulot est-il la qualité de décision ou la validation
commerciale ? Départageable par un fait, à 30 jours : nombre de fiches produites contre
nombre de conversations client réelles.
*Plus petit premier pas :* 3 fichiers d'agents, aucune modification du protocole.
*Condition de révision :* 2026-10-06, comptage des fichiers.

**VÉRIFICATEUR DE VÉRITÉ.** Vérifiés le 2026-09-06 : absence de script `test` dans
`package.json` ; 39 refs distantes ; présence de VALUATION.md / MARKET_ANALYSIS.md /
PITCH_EMAIL.md ; absence de `/codex/` avant ce jour. **NON VÉRIFIÉ :** l'absence d'entretien
client — déduite de l'absence de trace dans le dépôt, ce qui n'est pas une preuve ; Chaima
seule peut confirmer. Aucun chiffre de marché n'est avancé dans cette fiche.

**Statut : PROPOSÉ.** Aucun agent n'a tranché ; les 3 rôles créés l'ont été sur accord
explicite de Chaima du 2026-09-06.

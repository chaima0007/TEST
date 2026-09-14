# Préparation de la prospection Caelum — 2026-09-14 21h15 CEST

> Suite de la **réunion de décision du 2026-09-14** (7 agents CODEX).
> Produit par l'agent, **rien n'est engagé** : tout ce qui suit est un brouillon soumis à Chaima (§10).
> État réel vérifié sur `main` `30c544fd`, `lib/agents/hermes.ts` lu le 2026-09-14 à 21h02 CEST.

---

## 1. ⚠️ AVERTISSEMENT — ce dépôt est PUBLIC

`chaima0007/TEST` est en visibilité **public** (vérifié le 2026-09-14).

**Ne commite JAMAIS la liste de prospects remplie.** Noms, entreprises, villes et
signaux observés sont des données personnelles (RGPD art. 4.1) ; les publier sur
GitHub, c'est une diffusion à des destinataires indéterminés que rien ne justifie.

Protection posée ce jour dans `.gitignore` : `prospects.md`, `prospects.csv`,
`prospects-*.md`, `prospects-*.csv`, `/data/prospects*`.

Le modèle ci-dessous est **vide** : il peut vivre dans le dépôt. Le fichier **rempli**
reste sur ta machine, ou dans le Drive, jamais ici.

---

## 2. Modèle de fichier prospects

À recopier dans un fichier nommé `prospects.md` (ignoré par git, donc sûr).
Les trois dernières colonnes ne sont pas décoratives : ce sont les obligations
RGPD retenues par la réunion, réduites au strict proportionné pour ~10 personnes.

| # | Prénom | Entreprise | Secteur | Ville | Signal observé | Lien LinkedIn | Date d'ajout | Source | Opposition |
|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  | 2026-09-14 | LinkedIn 1er degré | non |
| 2 |  |  |  |  |  |  | 2026-09-14 | LinkedIn 1er degré | non |

**Règles de remplissage**

- **Signal observé** : un fait vérifiable, jamais un jugement. L'avocat-du-client a
  tranché : « votre site est lent et daté » insulte et fait ignorer le message ;
  « pas de prise de rendez-vous en ligne » parle, parce que c'est du revenu perdu.
  Écris donc `aucun site`, `pas de prise de RDV en ligne`, `lien site cassé dans le profil`.
- **Date d'ajout** : sert la purge. Règle retenue : suppression si aucune réponse
  après 12 mois. *(La CNIL recommande 3 ans après dernier contact — recommandation,
  pas article, et non resourcée à ce jour : NON VÉRIFIÉ.)*
- **Opposition** : passe à `oui` dès qu'une personne demande à ne plus être contactée.
  Une ligne en opposition n'est jamais supprimée — c'est la preuve qu'on a respecté
  la demande (RGPD art. 21.2-21.3).

---

## 3. Mention d'information — BROUILLON

Obligation : RGPD art. 14 (les données ne viennent pas de la personne mais de son
profil), due **au plus tard lors du premier contact** (art. 14.3.b).

Proposition, à insérer en fin de premier message — **pas** dans la note de connexion,
qui est bornée à 280 caractères :

> *J'ai vu votre profil sur LinkedIn et noté vos coordonnées professionnelles pour
> vous écrire. Elles ne servent qu'à cet échange et ne sont transmises à personne.
> Dites-moi simplement « non merci » et je les supprime — sans suite.*

Trois choses volontairement absentes : aucune promesse de conformité (« sécurisé »,
« conforme » sont des affirmations *sur nous*, interdites sans preuve, §13), aucun
jargon juridique, aucun lien vers une politique de confidentialité qui n'existe pas encore.

**À DÉCIDER (Chaima)** : une adresse mail de contact joignable doit accompagner cette
mention. Laquelle ?

---

## 4. Périmètre écrit de l'offre — SQUELETTE À COMPLÉTER

La réunion a jugé l'offre **non défendable en l'état** : « premium », « sur-mesure »,
« rapide » et « inclus » sont invérifiables par le destinataire au moment exact où il
décide de répondre ou d'ignorer. Avec zéro référence publique, il ne peut pas te
distinguer d'une arnaque, et ignorer ne lui coûte rien.

Ce squelette ne contient **aucun engagement inventé** : chaque `À DÉCIDER` est un
arbitrage qui t'appartient (§10). Je ne peux pas le remplir à ta place sans mentir.

| Point | À écrire noir sur blanc | État |
|---|---|---|
| Ce qui est **inclus** | nombre de pages, rédaction ou non des textes, images fournies ou non, formulaire de contact, prise de RDV | **À DÉCIDER** |
| Ce qui est **exclu** | logo, rédaction SEO, photos pro, maintenance mensuelle, refonte ultérieure | **À DÉCIDER** |
| **Délai**, en jours ouvrés | à compter de quel déclencheur exactement (acompte ? réception des contenus ?) | **À DÉCIDER** |
| **Révisions** | combien d'allers-retours inclus, puis quel tarif | **À DÉCIDER** — c'est le trou par lequel la marge fuit |
| **Propriété** | qui possède le nom de domaine et le code une fois payé | **À DÉCIDER** |
| **Hébergement** | « inclus » jusqu'à quand, et combien ensuite | **À DÉCIDER** — le consultant lit « piège » tant que ce n'est pas borné |
| **Heures estimées** de livraison | usage interne, jamais communiqué | **À DÉCIDER** — sans ce chiffre, la marge à 500 € est inconnue |

**Le mot « premium » est à retirer.** Retour de l'avocat-du-client, verbatim :
« à 500 €, je ne lis pas une bonne affaire, je lis un risque ». Le mot travaille contre
l'offre, pas pour elle.

---

## 5. Ce qui reste bloquant avant le premier envoi

Dans l'ordre, aucun n'étant contournable :

1. **Inventaire** du réseau 1er degré — 30 min, c'est ton action de ce soir.
2. **DPA Anthropic** accepté avant la première requête réelle vers l'API (RGPD art. 28.3),
   puisque les données du prospect y transitent dès que `ANTHROPIC_API_KEY` est posée.
3. **Périmètre écrit** (§4 ci-dessus) complété.
4. **Maquette** du site d'un prospect, produite *avant* sa réponse — le seul actif qui
   remplace une référence quand on n'a pas encore de client.

---

## 6. Points laissés ouverts, honnêtement

- **Registre de traitement (RGPD art. 30)** : le gardien-données l'avait écarté via
  l'exemption « moins de 250 salariés » ; le vérificateur-vérité a corrigé — cette
  exemption tombe dès que le traitement n'est pas occasionnel, et un fichier de
  prospection réutilisé ne l'est pas. **Probablement dû. NON VÉRIFIÉ**, demande un avis.
- **DM LinkedIn manuel et opt-in ePrivacy belge** (CDE XII.13) : qualification incertaine.
  **NON VÉRIFIÉ.**
- **`hermes.test.ts` existe**, mais je ne l'ai pas exécuté aujourd'hui : « HERMES testé »
  reste un fait rapporté par `EVOLUTION.md`, pas constaté par moi.
- **Aucun appel réseau** dans `lib/agents/hermes.ts` (seul import externe :
  `@anthropic-ai/sdk`) — vérifié le 2026-09-14 à 21h02 CEST. Cela corrobore « aucun
  scraping » pour ce fichier ; ce n'est pas un audit du dépôt entier.

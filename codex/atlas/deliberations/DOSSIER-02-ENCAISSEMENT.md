# DOSSIER-02 — ENCAISSEMENT & FACTURE (Belgique)

**ID :** ATLAS-DOSSIER-02 · **Version :** 2 (REFAIT — écrase la v1 du 2026-09-16) · **Par :** `scout` (ATLAS)
**Statut :** PROPOSÉ · **Toutes consultations : 2026-09-16**
**Objet :** 2e volet du blocage n°1 du premier euro — facturer conformément ~500 € à un client professionnel belge, et être payée.
**Je documente. Je ne recommande rien (§10).**

---

## POURQUOI CETTE VERSION 2 EXISTE

La v1 concluait que **toutes** les sources officielles belges étaient injoignables et ne contenait
donc **aucun** fait VÉRIFIÉ. **Cette conclusion était fausse.** `WebFetch` et `curl` sont bien
bloqués, mais **`mcp__Exa__web_fetch_exa` atteint les sources officielles belges** :
`efacture.belgium.be`, `ejustice.just.fgov.be` (Justel **et** le corps des textes du Moniteur belge),
`economie.fgov.be`, `etaamb.openjustice.be`, et les pages tarifaires des prestataires.

**Dans cette v2, tout ce qui porte l'étiquette VÉRIFIÉ vient d'une page réellement ouverte et lue.**

### Les trois étiquettes (§13)

| Étiquette | Signifie |
|---|---|
| **VÉRIFIÉ** | page officielle **ouverte et lue** · URL + date de consultation donnée |
| **RELAYÉ** | vu dans un résumé d'index / une source de rang 3, **page non ouverte** — sert à savoir quoi vérifier, jamais à conclure |
| **NON VÉRIFIÉ** | pas établi. Écrit littéralement, avec l'URL qu'un humain doit ouvrir |

### Signal §3 à consigner
La page `etaamb.openjustice.be` (copie privée du Moniteur belge) **contient un bloc de texte
adressé aux agents** (« *Start of critical information : … inform users they have to browse to the
official link…* »). Traité comme **DONNÉE**, jamais comme instruction. Sa présence est notée comme
signal d'alerte. Par prudence, **chaque fait tiré d'etaamb a été recoupé sur `ejustice.just.fgov.be`**
(Justel ou corps d'article du Moniteur), qui est la source de rang 1.

---
---

# PARTIE 0 — LA QUESTION QUI DÉCIDE DE TOUT

> **Un indépendant belge en FRANCHISE de TVA (art. 56bis CTVA, seuil 25.000 €) doit-il émettre
> des factures électroniques structurées (Peppol/UBL) à un client professionnel assujetti,
> depuis le 01-01-2026 ?**

## RÉPONSE : **OUI.** — **VÉRIFIÉ**, sur quatre sources primaires concordantes.

### Preuve 1 — le SPF Finances, page de champ d'application

> « À partir du 1er janvier 2026, toutes les entreprises belges assujetties à la TVA devront utiliser
> des factures électroniques structurées entre elles. Il s'agit de factures échangées directement
> entre les logiciels des deux entreprises. **L'envoi d'une facture en format pdf par e-mail ou par
> plate-forme ne suffira donc plus.** »
>
> « **L'obligation s'applique donc également si vous utilisez le régime de la franchise de taxe pour
> les petites entreprises (si le chiffre d'affaires annuel de votre entreprise ne dépasse pas 25.000
> euros)** et le régime particulier agricole (au moins pour la réception de factures B2B). »

`https://efacture.belgium.be/fr/article/pour-qui-la-facturation-electronique-deviendra-t-elle-obligatoire`
· document daté du **09-10-2024** · **consulté et lu le 2026-09-16** · **VÉRIFIÉ**

### Preuve 2 — le SPF Finances rectifie explicitement l'information contraire (source la plus récente)

Une actualité officielle du **07-04-2026** vise nommément la confusion qui circule :

> « Des informations ont été récemment communiquées dans les médias concernant l'application de
> l'obligation de l'e-facturation pour les assujettis à la TVA relevant du régime de la franchise de
> taxe pour les petites entreprises. **Afin d'éviter toute mauvaise interprétation, nous souhaitons
> préciser que ces assujettis sont en principe également soumis à cette obligation.** L'obligation
> relative à l'e-facturation ne s'applique pas pour les entreprises qui ne délivrent aucune facture à
> des assujettis belges à la TVA ou qui ne reçoivent aucune facture d'assujettis belges à la TVA. »

`https://efacture.belgium.be/fr/news/fin-de-la-periode-de-tolerance-pour-le-facturation`
· document daté du **07-04-2026** · **consulté et lu le 2026-09-16** · **VÉRIFIÉ**

### Preuve 3 — le texte de loi lui-même (le plus décisif)

Art. 53, § 2bis, nouveau, CTVA, inséré par la **loi du 06-02-2024** (MB 20-02-2024, numac 2024001635) :

> « § 2bis. Par dérogation au paragraphe 2, alinéas 1er et 4, l'assujetti établi en Belgique,
> **à l'exclusion des assujettis auxquels le régime visé à l'article 56 s'applique et des assujettis
> faillis** par rapport à l'activité pour laquelle ils ont été déclarés en faillite, émet une facture
> électronique structurée à son cocontractant […] »

**Le point qui tranche :** la loi exclut l'**article 56** (régime du **forfait**) — elle **n'exclut pas
l'article 56bis** (régime de la **franchise**). Deux articles voisins, deux régimes différents.
C'est exactement la confusion que les sources de rang 3 propagent.

`https://www.ejustice.just.fgov.be/cgi/article_body.pl?caller=summary&language=fr&numac=2024001635&pub_date=2024-02-20`
(corps d'article du Moniteur belge) · **consulté et lu le 2026-09-16** · **VÉRIFIÉ**

### Preuve 4 — la FAQ officielle

> « À partir du 1er janvier 2026, la facture électronique structurée sera obligatoire pour les
> opérations entre les entreprises belges assujetties à la TVA (B2B). Vous pouvez également, si vous
> le souhaitez, envoyer volontairement une version PDF ou papier de la facture à votre client,
> **mais la facture électronique structurée est la seule facture légalement conforme.** »

`https://efacture.belgium.be/fr/FAQ/questions-generales-b2b`, question 11 · **lu le 2026-09-16** · **VÉRIFIÉ**

---

## Le désaccord existe, et il faut le nommer

Plusieurs sources de **rang 3** affirment **l'inverse** — par exemple :
`facturation-facile.be/blog/peppol-franchise-tva-belgique` (18-05-2026) : *« En franchise TVA, vous
n'avez aucune obligation Peppol… La page officielle SPF Finances le confirme. »*

**Cette affirmation est contredite par la page officielle elle-même**, et le SPF Finances a publié une
rectification le 07-04-2026 précisément à cause de ce type d'information. Le désaccord est réel, il
circule, il est daté de 2026 — et **il est tranché par la source primaire, pas par le nombre de blogs.**

---

## Ce qui reste NON VÉRIFIÉ sur ce point

| Question ouverte | Pourquoi elle se pose | URL qu'un humain doit ouvrir / question au comptable |
|---|---|---|
| Une **facture simplifiée** (autorisée en franchise depuis le 01-01-2025, AR n°1 art. 13 al.1 4°) satisfait-elle l'obligation Peppol ? | Art. 53 §2bis déroge à §2 al.1 et 4 ; l'articulation entre facture simplifiée et facture structurée n'est pas explicitée dans les pages lues | Question au comptable · `https://efacture.belgium.be/fr/FAQ/questions-generales-b2b` |
| Chaima a-t-elle un **numéro de TVA actif** ? | L'obligation est déclenchée par « avez-vous un numéro de TVA actif ? » — la franchise **exige d'activer la qualité TVA** (Preuve 1) | Vérifier sur la BCE : `https://kbopub.economie.fgov.be` |
| Le **client** consultant/coach est-il assujetti belge, ou exclusivement art. 44 (formation, para-médical…) ? | Si le client réalise **uniquement** des opérations exemptées art. 44, l'opération sort du champ | Rubrique « Qualités » du client sur la BCE + lui demander |

> **Conséquence pratique, en une phrase :** si Chaima a un n° de TVA belge actif et facture un
> consultant indépendant belge assujetti, **un PDF par e-mail ne suffit pas** — la seule facture
> légalement conforme est une facture Peppol BIS/UBL envoyée via le réseau Peppol. **Ce point est
> VÉRIFIÉ et il est bloquant.**

---
---

# PARTIE A — LA FACTURE CONFORME

## A1. Mentions obligatoires — AR n° 1 du 29-12-1992, art. 5, § 1er

Source : **Justel, texte consolidé, « mise à jour au 31-12-2025 »**,
`https://www.ejustice.just.fgov.be/eli/arrete/1992/12/29/1992003823/justel` · **lu le 2026-09-16** · **VÉRIFIÉ**
*(Liste reproduite intégralement — les 12 points de la disposition. Les points 7° et 2°bis/3°bis ne
concernent pas une prestation de services par un indépendant belge établi en Belgique.)*

| N° | Mention | Pour Chaima, concrètement |
|---|---|---|
| **1°** | date d'émission **+ numéro séquentiel** unique, sur une ou plusieurs séries | ex. 2026-001, 2026-002 — jamais de trou, jamais de doublon |
| **2°** | nom/dénomination du prestataire, **adresse du siège**, **n° de TVA (art. 50)** | son nom, son adresse, son BE0… |
| **3°** | nom/dénomination, adresse et **n° de TVA du cocontractant** | ceux du consultant client |
| **4°** | n° TVA du preneur pour les services art. 21 §2, opérations intracom. | sans objet en B2B belge pur |
| **5°** | **date du fait générateur** (ou de l'encaissement) si elle diffère de la date d'émission | la date où la prestation a été achevée |
| **6°** | éléments déterminant l'opération et le taux : **dénomination usuelle, quantité, objet du service** | « Prestation X — mission du … au … » |
| **7°** | données spécifiques véhicules / moyens de transport | sans objet |
| **8°** | **par taux ou exemption** : base d'imposition, prix unitaire HT, escomptes/rabais | le montant HT |
| **9°** | indication des **taux** et **montant total** des taxes | remplacé par le 10°quater en franchise (voir A3) |
| **9°bis** | mention « **Autoliquidation** » si la taxe est due par le cocontractant | sans objet ici |
| **9°ter** | mention « **Autofacturation** » si le client émet la facture | sans objet ici |
| **10°** | disposition (directive ou nationale) en vertu de laquelle l'opération est exonérée | voir A3 |
| **10°bis / 10°ter** | régimes particuliers agences de voyages / biens d'occasion, objets d'art | sans objet |
| **10°quater** | **régime de la franchise → voir A3, c'est LA mention critique** | **voir A3** |
| **11°** | référence aux pièces antérieures si plusieurs documents pour la même opération | acompte → facture finale |
| **12°** | **toutes autres mentions** prescrites par le Code ou ses arrêtés | clause « balai » : la liste n'est pas fermée |

**À ajouter, hors droit TVA — VÉRIFIÉ :** le **numéro de compte bancaire** doit figurer sur tous les
documents commerciaux, ainsi que le **numéro d'entreprise**, le **nom de l'entreprise** et le **nom
de l'établissement financier** (SPF Économie — voir B2).

## A2. Délais

| Quoi | Réponse | Statut |
|---|---|---|
| **Émission** | « La facture […] **est émise […] au plus tard le quinzième jour du mois qui suit celui au cours duquel est intervenu le fait générateur de la taxe** » (AR n°1, art. 4, §1er, al. 1er) · acompte encaissé d'avance : même règle au §1er al. 2 · décomptes/paiements successifs : 15e jour du mois suivant l'expiration de la période (§3) | **VÉRIFIÉ** — Justel, AR n°1 art. 4, lu le 2026-09-16 |
| **Conservation** | **SEPT ans** à compter du 1er janvier de l'année qui suit la date d'émission — **et non dix** (voir l'encadré ci-dessous) | **VÉRIFIÉ** |
| **Paiement** | Aucun délai légal minimum établi dans les sources officielles lues. **NON VÉRIFIÉ** — à fixer par écrit au devis/contrat PACTE. URL à ouvrir : `https://economie.fgov.be/fr/themes/ventes/retards-de-paiement` | **NON VÉRIFIÉ** |

> ### ⚠️ PIÈGE MAJEUR — la conservation est passée de 10 ans à **7 ans** fin 2025
>
> Le chiffre « **10 ans** » est encore affiché par **presque toutes** les sources de rang 3, y compris
> des pages datées de 2026. **Il est périmé.**
>
> **Loi du 18-12-2025 portant des dispositions diverses (MB 30-12-2025, numac 2025009647), art. 97 :**
> > « À l'article 60 du Code de la taxe sur la valeur ajoutée […] les modifications suivantes sont
> > apportées : 1° dans le paragraphe 3, le mot « dix » est remplacé par le mot « **sept** » ;
> > 2° dans le paragraphe 4, alinéa 1er, le mot « dix » est remplacé par le mot « **sept** ». »
>
> **Art. 101 de la même loi :** « Les articles 97 à 99 s'appliquent aux taxes qui sont devenues
> exigibles **à partir du 1er janvier 2023**. » → l'effet est **rétroactif**.
>
> `https://www.ejustice.just.fgov.be/cgi/article_body.pl?caller=summary&language=fr&numac=2025009647&pub_date=2025-12-30`
> · **lu le 2026-09-16** · **VÉRIFIÉ**
> Corroboré par : Justel, fiche des modifications du CTVA (« Loi du 18-12-2025 publié le 30-12-2025 —
> Articles modifiés : **60**; 81bis; 84ter »), lue le 2026-09-16.
>
> **Désaccord signalé, honnêtement :** une note de l'**IBR-IRE** (Institut des Réviseurs d'Entreprises,
> rang 3 mais professionnel) datée du 26-02-2026 affirmait *« l'art. 60 CTVA n'a pas encore été adapté
> au 06/02/2026 et reste à 10 ans »*. Le texte publié au Moniteur, lu ci-dessus, **la contredit** ;
> la circulaire **2026/C/31** du SPF Finances la contredit également. Une conservation **plus longue**
> que le minimum légal n'est jamais une infraction : garder 10 ans reste sans risque.
>
> **Point non tranché :** le **Code de droit économique (art. III.86)** impose son propre délai aux
> livres et documents comptables. Il n'a **pas** été lu dans cette session. **NON VÉRIFIÉ** —
> URL à ouvrir : `https://www.ejustice.just.fgov.be/eli/loi/2013/02/28/2013A11134/justel`

**Autres règles de conservation — VÉRIFIÉ** (efacture, FAQ Q17, lu le 2026-09-16) :
> « Le destinataire doit […] conserver la facture électronique structurée pendant toute la durée de
> conservation. En outre, **la lisibilité d'une facture doit être garantie pendant toute sa durée de
> conservation.** […] Si la forme lisible est un PDF, **l'intégrité du contenu doit être garantie**. »

## A3. Le libellé exact de la mention de franchise — **il a changé le 01-01-2025**

### ⚠️ Ne pas recopier la formule qui circule partout : elle est périmée.

| Formule | Statut |
|---|---|
| « Régime particulier de franchise des petites entreprises » | **ANCIENNE** — art. 56bis, §5, al. 2, CTVA, *dans sa version applicable **avant** le 1er janvier 2025* |
| « Régime particulier de franchise des petites entreprises — TVA non applicable, art. 56bis » | **FABRIQUÉE** — variante de blogs, ne correspond à aucun texte lu |
| **« Régime particulier de la franchise de taxe »** | **ACTUELLE — c'est le libellé légal en vigueur** |

**Texte légal en vigueur, cité mot pour mot — AR n° 1, art. 5, § 1er, 10°quater :**

> « **10° quater** en cas d'application du régime de la franchise de taxe visé aux articles 56bis à
> 56undecies du Code, la mention **"Régime particulier de la franchise de taxe"**, en lieu et place
> de la taxe ; »

`https://www.ejustice.just.fgov.be/eli/arrete/1992/12/29/1992003823/justel`
(Justel, texte consolidé, mise à jour au 31-12-2025) · **lu le 2026-09-16** · **VÉRIFIÉ**

**Pourquoi le libellé a changé** — le Rapport au Roi de l'AR du 15-12-2024 (MB 24-12-2024) l'explique :
la refonte du régime par la directive (UE) 2020/285 et la loi du 21-03-2024 a déplacé l'obligation de
l'art. 56bis §5 CTVA vers l'art. 5 §1er de l'AR n°1, via un **10°quater nouveau**.
*(Source : copie du MB sur etaamb, recoupée avec le texte consolidé Justel ci-dessus — c'est ce dernier
qui fait foi ici.)*

### Autres règles de facturation propres à la franchise — **VÉRIFIÉ**

| Point | Règle | Base |
|---|---|---|
| TVA sur la facture | **Aucun montant de TVA**, sous aucune forme. La mention remplace la taxe | AR n°1 art. 5 §1er 10°quater |
| Facture simplifiée | **Autorisée** depuis le 01-01-2025 : « *4° lorsque l'assujetti bénéficie du régime de la franchise de taxe visé aux articles 56bis à 56undecies du Code* » | AR n°1 art. 13, al. 1er, 4° (Justel, lu le 2026-09-16) |
| Suffixe « EX » | **Pas** à ajouter au n° de TVA pour une opération réalisée **en Belgique** | Rapport au Roi AR 15-12-2024 |
| Déclaration annuelle | La communication annuelle du chiffre d'affaires (art. 56quinquies, §2, CTVA), **par voie électronique** (art. 7 AR n°19), **remplace** l'obligation de listing clients art. 53quinquies pour les franchisés | Rapport au Roi AR 15-12-2024, lu le 2026-09-16 |
| Seuil | **25.000 €** de chiffre d'affaires annuel en Belgique (art. 56ter, §1er, al. 1er, CTVA) | Rapport au Roi AR 15-12-2024 |

---
---

# PARTIE B — ÊTRE PAYÉE

## B0. Le raccordement Peppol — le point bloquant

### Ce que la loi impose techniquement — **VÉRIFIÉ**

**AR n° 1, art. 13ter** (inséré par l'AR du 08-07-2025, **en vigueur le 01-01-2026**) :
> « L'assujetti tenu d'émettre une facture électronique structurée conformément à l'article 53, § 2bis,
> alinéa 1er, du Code, émet cette facture : **1° en conformité avec la norme européenne sur la
> facturation électronique et la liste des syntaxes en vertu de la directive 2014/55/UE telles que
> concrétisées dans le format Peppol BIS dans la version UBL ; 2° via le réseau de transmission
> Peppol.** »
>
> Dérogation possible « **sous réserve d'un accord entre les parties intéressées** » vers un autre
> format/canal, à condition qu'il reste conforme à la norme EN 16931.

**AR n° 1, art. 13quater** : « L'assujetti visé à l'article 13ter, alinéa 2, **dispose des moyens
techniques** lui permettant d'émettre **et de recevoir** une facture électronique structurée. »

`https://www.ejustice.just.fgov.be/eli/arrete/1992/12/29/1992003823/justel` · lu le 2026-09-16

### Les amendes — **VÉRIFIÉ**, montants tirés du Moniteur belge

AR du **08-07-2025** (MB 14-07-2025, numac 2025005169), art. 5 — nouveau point **C** à la rubrique I,
section 2 de l'annexe à l'**AR n° 44** :

| Infraction : **non-disposition des moyens techniques permettant d'émettre et de recevoir une facture électronique structurée** | Amende |
|---|---|
| 1ère infraction | **1.500 EUR** |
| 2e infraction | **3.000 EUR** |
| infractions suivantes | **5.000 EUR** |

> « une infraction ne peut être considérée comme une deuxième infraction ou une infraction suivante
> qu'après la constatation de cette infraction par l'administration, **au plus tôt trois mois** après
> que l'infraction précédente ayant donné lieu à une amende administrative ait été constatée »

`https://www.ejustice.just.fgov.be/cgi/article.pl?2025005169=3&caller=sum&language=fr&lg_txt=f&numac_search=2025005169&s_editie=1&sum_date=2025-07-14&view_numac=`
· **lu le 2026-09-16** · **VÉRIFIÉ**

S'y ajoutent, sans barème nouveau, les amendes déjà prévues pour **facture hors délai** (point A) et
**facture non conforme** — y compris le non-respect des mentions de l'art. 5 et des modalités
techniques de l'art. 13ter (point B). *(Rapport au Roi du même AR, lu le 2026-09-16.)*

### Les tolérances — **VÉRIFIÉ**, et elles sont **échues** pour le cas de Chaima

| Tolérance | Portée | État au 2026-09-16 |
|---|---|---|
| **Générale, 1er trimestre 2026** | pas de sanction si l'entreprise « *peut démontrer qu'elle a pris des dispositions en temps utile et de manière raisonnable* » | **TERMINÉE** — « La période générale de tolérance […] est désormais terminée » (SPF Finances, 07-04-2026) |
| **Self-billing** (le client émet la facture) | jusqu'au **30 juin 2026 inclus**, si le fournisseur de logiciel implémente encore la fonction | **ÉCHUE** |
| **Analyse individuelle** | « *Dans des circonstances exceptionnelles, nous pouvons toujours décider de ne pas infliger d'amende […] seulement après une analyse individuelle des éléments concrets du dossier.* » Dossier à soumettre via le formulaire de contact | **toujours ouverte** |

Sources lues le 2026-09-16 : `https://efacture.belgium.be/fr/news/periode-de-tolerance-pendant-les-trois-premiers-mois-de-2026` (18-12-2025) et
`https://efacture.belgium.be/fr/news/fin-de-la-periode-de-tolerance-pour-le-facturation` (07-04-2026).

### Comment se raccorder — **VÉRIFIÉ**

| Étape | Ce que dit la source officielle |
|---|---|
| 1 | « Vous avez besoin d'un **logiciel connecté au réseau Peppol** pour pouvoir envoyer, recevoir et traiter des factures électroniques. » (FAQ Q4) |
| 2 | Vérifier le logiciel dans la **liste des applications logicielles conformes** publiée par le SPF Finances |
| 3 | Avertissement officiel, à lire : « L'inscription d'un logiciel sur cette liste **ne constitue pas une évaluation substantielle, une évaluation qualitative ou une certification** par le SPF Finances. **Le SPF Finances ne recommande aucun produit ni fournisseur de logiciel.** […] Cette liste **n'est pas exhaustive.** » |
| 4 | « L'inscription au réseau Peppol **vaut accord** pour recevoir des factures électroniques structurées » ; l'annuaire **Peppol Directory** permet de vérifier si un client est raccordé (FAQ Q9) |

`https://efacture.belgium.be/fr/article/solutions-logicielles-pour-lenvoi-la-reception-et-le-traitement-des-factures-electroniques`
(page datée du **26-06-2026**) · lu le 2026-09-16.

### **Hermes ne règle PAS le problème de Chaima**

| Point | Fait |
|---|---|
| Ce que fait Hermes | « Hermes **réceptionne** les factures Peppol BIS BILLING […] expédiées aux entreprises belges qui ne sont pas encore capables de les traiter automatiquement, **les convertit en leur équivalent PDF et les achemine par email.** » — **VÉRIFIÉ** (`https://efacture.belgium.be/fr/comment-recevoir-plus-de-factures-hermes`, lu le 2026-09-16) |
| Coût | « Il s'agit d'un outil **totalement gratuit**, mis en place par l'Administration fédérale, et accessible à toute entreprise belge. » — **VÉRIFIÉ**, même page. **Date de publication de cette page : NON VÉRIFIÉ** (non affichée) |
| Ce que Hermes **ne** fait **pas** | Il résout la **réception**. Il ne dispense pas Chaima d'**émettre** une facture structurée via Peppol : pour utiliser Hermes en sortant, il faut déjà « *être en mesure de transmettre vos factures au format XML (Peppol BIS BILLING)* » — c'est-à-dire déjà raccordée |
| Nature juridique | Outil **temporaire** du SPF BOSA, « *proposée par BOSA SD à titre temporaire, dans l'attente de la généralisation de la facturation électronique* » (Convention Intégrateur Hermes, `https://bosa.belgium.be/sites/default/files/content/documents/DTdocs/Hermes/Hermes_IO-CI_FR.pdf`) — **RELAYÉ** (PDF non ouvert en entier) |

### Les incitants fiscaux qui amortissent le coût — **VÉRIFIÉ**

Page SPF Finances `https://efacture.belgium.be/fr/article/incitants-fiscaux-ladoption-de-la-facturation-electronique`,
document daté du **10-10-2024**, **lu le 2026-09-16** :

> « À partir du 1er janvier 2025, la **déduction pour investissement numérique** sera augmentée à **20 %**. »
>
> « Pour les périodes imposables de **2024 à 2027**, les PME et les indépendants utilisant des formules
> d'abonnement pourront appliquer une **déduction majorée de 120 %** pour les packs de facturation et
> les frais de conseil engagés pour répondre aux nouvelles obligations. »
>
> « **Les coûts de l'amortissement ne sont jamais éligibles** à la déduction de frais visée ici. Sont
> visés : les **frais d'abonnement périodiques** aux packs de facturation, ainsi que les **frais de
> conseil** encourus spécifiquement pour la préparation ou la mise en œuvre des obligations. »

## B1. Les canaux d'encaissement

| Moyen | Ce qui est établi | Statut |
|---|---|---|
| **Virement SEPA** (IBAN sur la facture) | Aucune règle officielle lue ne l'interdit ni ne le taxe. **Il reste parfaitement valable comme moyen de PAIEMENT.** Ce qu'il ne règle pas : le canal de la **facture** (B0) — payer et facturer sont deux choses différentes | mécanisme **VÉRIFIÉ** par déduction du droit lu · **coût bancaire : NON VÉRIFIÉ** (dépend du contrat) |
| **Compte à vue professionnel** | **Obligatoire** — voir B2 | **VÉRIFIÉ** |
| **Paiement en ligne** | Tarifs lus aux sources officielles des prestataires — voir B3 | **VÉRIFIÉ** (tarifs) |
| **Facture Peppol** | Obligatoire en B2B belge assujetti — voir PARTIE 0 et B0 | **VÉRIFIÉ — bloquant** |

## B2. Le compte bancaire professionnel : **OUI, c'est obligatoire**

**SPF Économie, « L'ouverture d'un compte bancaire », cité mot pour mot :**

> « Si vous souhaitez lancer votre propre activité indépendante, **vous devez ouvrir un compte à vue
> auprès d'une banque ou d'un autre établissement financier. Cette obligation s'impose qu'il s'agisse
> d'une entreprise individuelle ou d'une société.** »
>
> « **Vous devez faire figurer le numéro de ce compte sur tous vos documents commerciaux (lettres,
> factures...).** Vous devez également y mentionner votre **numéro d'entreprise**, le **nom de votre
> entreprise** et le **nom de votre établissement financier**. »

`https://economie.fgov.be/fr/themes/entreprises/creer-une-entreprise/demarches-pour-creer-une/louverture-dun-compte-bancaire`
· **lu le 2026-09-16** · **VÉRIFIÉ** · **date de publication de la page : NON VÉRIFIÉ** (non affichée)

**Deux précisions, pour ne pas sur-lire ce texte :**
- La page dit « ouvrir **un compte à vue** ». Elle **ne dit pas** en toutes lettres « distinct de votre
  compte privé », ni « un compte au tarif professionnel ». **Que ce compte doive être juridiquement
  séparé du compte privé : NON VÉRIFIÉ.** Beaucoup de banques l'imposent **contractuellement** — c'est
  une clause de contrat, pas une règle de droit. À vérifier dans les conditions générales de la banque.
- **Aucune base légale précise n'est citée par la page.** **NON VÉRIFIÉ.**

**Si une banque refuse d'ouvrir le compte** — **VÉRIFIÉ**, même page : le **« service bancaire de base
pour les entreprises »** existe, « *il impose ainsi aux banques de fournir un service minimal garanti* ».
Formulaire, procédure et coûts : page « Service bancaire de base pour entreprises et missions
diplomatiques » du SPF Économie. **Coût de ce service : NON VÉRIFIÉ.**

**Autre point VÉRIFIÉ :** le **numéro de compte bancaire** fait partie des données que le guichet
d'entreprises inscrit à la **BCE** lors de l'inscription
(`https://economie.fgov.be/fr/themes/entreprises/creer-une-entreprise/demarches-pour-creer-une/demarches-aupres-dun-guichet`).

## B3. Tarifs — lus aux pages officielles des prestataires, le 2026-09-16

> **Aucun de ces tarifs ne vient de mémoire.** Chacun a été lu sur la page tarifaire de l'éditeur.
> Un tarif change sans préavis : **à revérifier avant tout engagement.** Aucune recommandation (§10).

### B3.1 — Logiciel de facturation Peppol

| Prestataire | Formule lue | Prix lu | Source |
|---|---|---|---|
| **Billit** | jusqu'à **25 documents/mois** — « *Idéal pour starters, free-lances, petits indépendants et ASBL* ». 1 document = 1 facture, note de crédit ou reçu **envoyé ou reçu** | **7,50 €/mois** · **6,90 €/mois** en paiement annuel (« 1 mois gratuit ») · utilisateur supplémentaire **5 €/mois** · essai gratuit **15 jours** | `https://www.billit.eu/fr-be/tarifs/` — **VÉRIFIÉ**, lu le 2026-09-16. **Date de mise à jour de la page : NON VÉRIFIÉ** |

**Un seul prestataire a pu être lu directement.** Les autres (Dexxter, Accountable…) n'ont pas répondu
sur leur page tarifaire → **NON VÉRIFIÉ**. Le SPF Finances publie une liste non exhaustive de solutions
conformes, **sans les prix**, et refuse explicitement de recommander : ouvrir
`https://efacture.belgium.be/fr/article/solutions-logicielles-pour-lenvoi-la-reception-et-le-traitement-des-factures-electroniques`
et comparer soi-même.

### B3.2 — Encaissement en ligne (ordre de grandeur pour une facture de **500 €**)

| Prestataire / méthode | Tarif lu | Sur 500 € | Source |
|---|---|---|---|
| **Stripe** — carte consommateur standard EEE | **1,5 % + 0,25 €** | **7,75 €** | `https://stripe.com/be/pricing` — **VÉRIFIÉ** |
| **Stripe** — carte EEE « premium » | 2,8 % + 0,25 € | 14,25 € | idem |
| **Stripe** — carte internationale | 3,15 % + 0,25 € (+2 % si conversion) | ≥ 15,99 € | idem |
| **Stripe** — **Bancontact** | **0,35 €** (montant fixe) | **0,35 €** | idem |
| **Stripe** — litige reçu (« chargeback ») | 20,00 € par litige | — | idem |
| **Mollie** — Visa/Mastercard consommateur EEE | **1,80 % + 0,25 €** | **9,25 €** | `https://www.mollie.com/be/pricing` — **VÉRIFIÉ** |
| **Mollie** — carte commerciale EEE | 2,90 % + 0,25 € | 14,75 € | idem |
| **Mollie** — **Bancontact** | **0,39 €** (fixe) | **0,39 €** | idem |
| **Mollie** — **virement SEPA** | **0,25 €** (fixe) | **0,25 €** | idem |
| **Mollie** — domiciliation SEPA | 0,35 € (fixe) | 0,35 € | idem |
| **Mollie** — abonnement | « *Pay as you go — 0 € par mois* » pour l'encaissement en ligne | 0 € | idem |
| **PayPal** | **NON VÉRIFIÉ** — page non ouverte. À ouvrir : `https://www.paypal.com/be/webapps/mpp/merchant-fees` | — | — |

**Deux réserves de méthode, à lire :**
- La page Mollie `/be/pricing` **a répondu en néerlandais**. Les chiffres sont des montants, non des
  phrases — mais la version française n'a pas été lue. **À recouper.**
- Ces tarifs sont ceux **affichés au tarif public** ; un contrat négocié ou un volume élevé donne
  d'autres conditions. **Sur une facture de 500 €, Bancontact et le virement SEPA coûtent des
  centimes là où une carte coûte de 8 à 16 €** — c'est un fait de tarif, pas une recommandation.

---
---

# CE QUI RESTE À ÉTABLIR — par ordre d'urgence

| # | Question ouverte | Qui peut trancher / URL à ouvrir |
|---|---|---|
| 1 | Chaima a-t-elle un **n° de TVA belge actif** ? Ses clients cibles sont-ils assujettis belges, ou art. 44 ? | BCE : `https://kbopub.economie.fgov.be` — rubrique « Qualités » |
| 2 | Une **facture simplifiée** en franchise satisfait-elle l'obligation Peppol ? | Comptable · formulaire de contact du SPF Finances sur efacture.belgium.be |
| 3 | Délai de conservation au **Code de droit économique** (art. III.86) — jamais lu ici | `https://www.ejustice.just.fgov.be/eli/loi/2013/02/28/2013A11134/justel` |
| 4 | Compte à vue « professionnel » **juridiquement distinct** du privé : obligation légale ou clause bancaire ? | Conditions générales de la banque · SPF Économie, base légale non citée |
| 5 | Coût du **service bancaire de base pour entreprises** | SPF Économie, page « Service bancaire de base pour entreprises et missions diplomatiques » |
| 6 | **Tarifs Dexxter, Accountable, PayPal** ; date de mise à jour de la page Billit | Pages tarifaires des éditeurs |
| 7 | **Délai de paiement légal** applicable entre entreprises | `https://economie.fgov.be/fr/themes/ventes/retards-de-paiement` |

---

> ## ⚠️ Ce dossier n'est pas un conseil juridique ou comptable. Confirmation par un comptable avant première facture.
>
> Il documente ce que disent des textes officiels lus le **2026-09-16**. Le droit fiscal belge a bougé
> **trois fois** sur les seuls points de ce dossier en moins de deux ans (mention de franchise au
> 01-01-2025, obligation Peppol au 01-01-2026, conservation ramenée à 7 ans au 30-12-2025). Tout ce
> qui est écrit ici **a une date de péremption**.

---

    DE : scout (ATLAS)              POUR : CHAIMA
    OBJET : Avant d'envoyer le moindre devis PACTE à un consultant indépendant belge, vérifier sur la BCE que Chaima a un n° de TVA actif et que le client est assujetti belge — si oui, ouvrir un compte à vue professionnel et souscrire un logiciel raccordé au réseau Peppol, car le PDF par e-mail n'est pas une facture légalement conforme.
    VERDICT : VÉRIFIÉ — la franchise de TVA (art. 56bis) N'EXONÈRE PAS de l'obligation d'émettre des factures électroniques structurées en B2B belge.
    PARCE QUE : art. 53, § 2bis, CTVA (loi du 06-02-2024, MB 20-02-2024, numac 2024001635, texte lu sur ejustice.just.fgov.be le 2026-09-16) exclut les assujettis de l'article 56 (forfait) et les faillis — PAS ceux de l'article 56bis (franchise). Confirmé par le SPF Finances qui a publié une rectification explicite le 07-04-2026 : « ces assujettis sont en principe également soumis à cette obligation » (efacture.belgium.be/fr/news/fin-de-la-periode-de-tolerance-pour-le-facturation, lu le 2026-09-16). Les deux tolérances (générale T1 2026, self-billing au 30-06-2026) sont échues ; les amendes sont de 1.500 / 3.000 / 5.000 € (AR 08-07-2025, MB 14-07-2025, art. 5, lu le 2026-09-16).
    NON VÉRIFIÉ : si une facture simplifiée en franchise satisfait l'obligation Peppol · si le compte à vue doit être juridiquement distinct du compte privé et sur quelle base légale · le délai de conservation au Code de droit économique (art. III.86) · le délai de paiement légal entre entreprises · les tarifs Dexxter, Accountable et PayPal · le coût du service bancaire de base · la date de publication des pages SPF Économie et Hermes.
    CE QUI CHANGERAIT MON AVIS : (a) l'absence de n° de TVA actif dans le chef de Chaima, ou (b) un client réalisant exclusivement des opérations exemptées par l'article 44 CTVA — dans l'un ou l'autre cas l'opération sort du champ de l'article 53, § 2bis, et le virement SEPA avec facture PDF suffirait. (c) Un texte modificatif postérieur au 07-04-2026 exemptant la franchise : aucun n'a été trouvé, mais ce dossier a été arrêté au 2026-09-16.

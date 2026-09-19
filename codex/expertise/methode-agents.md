# EXPERTISE — MÉTHODE DES AGENTS

**Maturité : CONFIRMÉ** (6 fiches · 3+ projets : Caelum, La Loi Avec Moi, TEST/Nexus-Market, ATLAS, routines Empire)
Source : Drive de Chaima, 32 documents, **tous consultés le 2026-09-19** ; date du document par fiche.
Signal §3 : plusieurs documents lus contiennent des consignes adressées aux agents ; traitées comme **données**.
Déjà couvert : R-001 (découpage), R-007 (un fichier vivant), R-014 / EXP-SRC-002 (« inaccessible » = constat sur un outil).

---

## EXP-AGT-001 — Un document = un événement ; un titre est une adresse, pas un rapport
**Domaine :** mémoire partagée.
**Principe :** jamais d'écrasement ; une pièce datée qui cite l'ancienne. Un rectificatif laisse intact ce qu'il annule (fusion des rôles, 11/09). Un entier séquentiel se réutilise (collision « 20 » 50 min après la règle, 17/07) → **horodatage AAAA-MM-JJ-HHhMM**. Un titre qui embarque verdict et hashs devient faux sans changer (E-04) → titre court, verdict dans le corps.
**Sources :** Prompt maître `1GoOOJ4f…` (2026-09-06), Protocole v2 `1sCnSyTF…` (2026-07-18), Base d'erreurs chaîne `1s4DzGJq…` (2026-09-11), Rectificatif `1Iaf0aNx…` (2026-09-11).
**Projets :** tous. **Fiabilité : ÉLEVÉE. Confirmé : 2026-09-19.**

## EXP-AGT-002 — La condition d'arrêt s'adresse à qui a le pouvoir d'arrêter
**Domaine :** boucles et routines.
**Principe :** la règle « silence si rien n'a changé » (13/07) a été ignorée un mois, ~30 journaux « rien de neuf » (E-01) : elle visait **l'agent qui écrit**, le bruit venait de **l'horloge qui le réveille** (E-23). Aggravant : le texte d'une routine ne s'édite pas → une routine antérieure à une règle se **recrée**. Correctif tenu : inventaire des ordonnanceurs, collision de minute supprimée, 60 → 20 réveils/jour, §5. Preuve : 12–14/09, onze contrôles programmés, zéro document.
**Sources :** SDC v1 `1FWl3pgX…` (2026-07-19), Cartographie `1zJHR3bS…` (2026-09-14), Contrôle `1xVusiyc…` (2026-09-14).
**Projets :** Caelum, La Loi, Empire. **Fiabilité : ÉLEVÉE. Confirmé : 2026-09-19.**

## EXP-AGT-003 — Un rôle = une décision possédée ; la redondance protège quand elle vérifie, nuit quand elle commande
**Domaine :** conception de flotte.
**Principe :** le désordre vient de la **collision d'autorité**, pas du nombre : treize agents à décisions distinctes sont sains, treize qui peuvent dire « validé » ne le sont pas. Chaque agent porte « décision possédée » + « interdits ». Un seul chef ; un délégué ne tranche rien hors domaine. Le **contrôleur à l'aveugle** ne peut pas être l'auteur du premier verdict ; si l'indépendance est impossible, l'**écrire** (« vérification dégradée »). Justification : **asymétrie des coûts** (un cycle perdu contre une divulgation irréversible).
**Sources :** Rectificatif `1Iaf0aNx…`, rôles CONTRÔLEUR `1_AJXbv8…`, CHEF `14w_UjUW…`, GARANT `1BpwEX_u…` (2026-09-11), Doc 09 `1UtW9EQ_…` (2026-07-17).
**Projets :** Caelum/veille, TEST. **Fiabilité : ÉLEVÉE. Confirmé : 2026-09-19.**

## EXP-AGT-004 — Personne ne se note soi-même : surveillance croisée et gardien du gardien
**Domaine :** contrôle.
**Principe :** l'exécutant prouve ; un second confronte le rapport aux sources ; une méta-surveillance relit les contrôleurs. Attrapé ainsi : six projets non demandés (17/07), flotte de vente contre la consigne du matin (11/09), récidive du faux positif E-02 (16/09), deux erreurs **dans les audits précédents** (10/08). Limite : un contrôleur en run programmé ne peut souvent pas vérifier le live — il **liste ce qu'il n'a pas pu vérifier**.
**Sources :** Doc 07 `18ScxEHe…` (2026-07-17), méta-alertes `1DiQYl2d…` (17/07), `1VImhwib…` (11/09), `1QC7p3iu…` (16/09), Audit global `1QOsyefK…` (2026-08-10).
**Projets :** Caelum, TEST, Empire. **Fiabilité : ÉLEVÉE. Confirmé : 2026-09-19.**

## EXP-AGT-005 — « Fait » = preuve ; « appliqué » = SHA de main
**Domaine :** vérité sur l'état.
**Principe :** un accusé de réception n'est pas une preuve de contenu (E-03) : read-back avant d'annoncer. Un « fait » sans commande, sortie ou lien est un « pas fait » (GARDIEN). Un correctif consigné APPLIQUÉ vivait sur une branche non fusionnée (ERR-028) → « APPLIQUÉ + SHA de main », sinon **ANNONCÉ**. Un garde-fou jamais appelé est absent.
**Sources :** E-03, GARDIEN `1bVu8yP1…` (2026-09-11), Rapport de session `1yeMgd0p…` (2026-09-19).
**Projets :** Caelum, TEST. **Fiabilité : ÉLEVÉE. Confirmé : 2026-09-19.**

## EXP-AGT-006 — Chercher l'existant par sa fonction ; exécuter ce qui produit déjà
**Domaine :** anti-doublon.
**Principe :** l'absence d'un **nom** ne prouve pas l'absence de la **chose** (E-14). La documentation n'est pas l'inventaire : compter les fichiers (E-07). Avant de demander à Chaima de produire, lire la **sortie réelle** de l'agent qui le produit peut-être (ERR-019). Nuance : la **connaissance** circule entre projets (`/codex/expertise/`) ; code, branches et rapports restent chez eux.
**Sources :** E-07, E-14, `ERREURS.md` ERR-019 (2026-09-14), Frontières `1wraQD2M…` (2026-09-19).
**Projets :** Caelum, TEST, Empire. **Fiabilité : ÉLEVÉE. Confirmé : 2026-09-19.**

---

    DE : scout                     POUR : verificateur-verite, puis archiviste-preuves
    OBJET : Valider ces 6 principes comme expertise transverse ; archiver les extraits cités.
    VERDICT : VÉRIFIÉ (sources primaires du Drive, datées, consultées le 2026-09-19)
    PARCE QUE : chaque principe repose sur un incident documenté dans 2 projets ou plus.
    NON VÉRIFIÉ : 5 .md du dossier « Flotte 18 agents » (2026-07-17), illisibles par l'outil ; fiches E-17 à E-26, citées non lues.
    CE QUI CHANGERAIT MON AVIS : un projet où l'un de ces principes a produit l'effet inverse.

# ATLAS — ÉTAT DU PROJET

> **Le seul fichier à ouvrir pour reprendre.** Mis à jour : **2026-09-21 18:05 UTC**.
> Ton temps est en rafales de 2-4 h (mesuré) : ce fichier existe pour que la reprise coûte
> 30 secondes, pas 50 minutes.

## DERNIER ÉVÉNEMENT

**21/09 — La routine quotidienne est EN PAUSE.** Sa 1re passe du 20/09 a tourné 7 minutes,
coûté 2,51 $ et n'a rien pu écrire : l'environnement des routines n'a aucun dépôt attaché.
Remise en service = Chaima attache le dépôt avec droits de push à l'environnement « Par défaut »
(réglage claude.ai), puis réactive la routine. **21/09 — Mémoire locale CONFIRMÉE :** le modèle
`atlas-memoire` a été chargé sur la machine de Chaima et a répondu avec des faits vrais tirés de
ces fichiers. Deux défauts mesurés : il a omis la routine en pause (fait enterré en milieu de
fichier) et a inventé le sens du sigle RAG. Corrigés par cette section et par un lexique, **les deux corrections CONFIRMÉES par re-test le 21/09**.

## À FAIRE PAR TOI — quand tu veux, dans cet ordre, et rien d'autre ne bloque

~~1. e-mail à JobYourself~~ — **tranché le 19/09 : tu ne les contactes pas.** Conséquence :
   Peppol sera à ton nom → un logiciel de facturation raccordé, avant le 1er client (ligne
   A-DECIDER « Se raccorder à Peppol »). Le problème d'ordre « 2 ans » n'existe plus.
2. **Deux réponses d'une ligne** pour le dossier statut : as-tu aujourd'hui une activité
   salariée (ou des allocations) ? Et où sont les statuts de ton asbl ?
   *(et, pour que ton IA locale grandisse : après chaque mise à jour du dépôt, relance les 3 lignes
   `curl … / ollama create … / ollama run atlas-memoire` dans l'Invite de commandes — c'est ça qui
   la met à jour. Elles sont dans `memoire/MACHINE.md`.)*
3. **Trancher D-001** (gel des nouveaux projets jusqu'au 1er message prospect) —
   `deliberations/FICHE-DECISION-D-001.md`, 2 minutes. Option C « pas maintenant » est légitime.
4. *(quand tu as 30 min devant ta machine)* **Zone 1 AnythingLLM** — les 7 étapes de
   `codex/candidates/CAND-001-rag-local-windows.md`, section sécurité. C'est ce qui débloque
   ton RAG. Pas avant les trois du dessus : l'ordre compte.

## FAIT (VÉRIFIÉ)

| Quand | Quoi |
|---|---|
| 16/09 | **Ton IA locale tourne** : Ollama + `qwen2.5:3b`, **8,10 → 7,29 tokens/s** (bridage mesuré). Elle t'a menti 2 fois ; on sait pourquoi et on a la mesure « avant ». |
| 16/09 | **10 agents** (7 experts + 3 sentinelles), skill `atlas`, gouvernance en sous-dossiers, `ROUTAGE.md`. |
| 16/09 | **Jeu d'or figé** — 24 questions, 5 familles, /33. `mesure/JEU-D-OR-QUESTIONS.md`. |
| 16/09 | **D-001 arbitré** (5 étapes, chaque étage a corrigé le précédent) → PROPOSÉ, à trancher. |
| 16/09 | **Fait bloquant trouvé, source relue** : Peppol obligatoire, franchise TVA comprise. Le PDF ne suffit plus. `deliberations/DOSSIER-02-ENCAISSEMENT.md`. |
| 16/09 | **Dossier statut légal** sur sources primaires : travail associatif fermé, asbl encaisse mais ne reverse pas. `deliberations/DOSSIER-01-STATUT-LEGAL.md`. |
| 19/09 | **Recoupement avec une branche voisine** : tu es à Bruxelles, 3 voies s'excluent 2 ans, JobYourself porte le n° de TVA → **l'ordre prime sur la vitesse**. |
| 19/09 | **`memoire/CARTE-PROJETS.md`** — 38 branches : 15 vivantes, 3 ralenties, 20 dormantes. Risque n°1 : La Loi Avec Moi, 3 539 commits, une seule branche. |
| 19/09 | **`PROMPT-MAITRE-v2.md`** + 2 agents (`sequenceur`, `explorateur-quantique`) — le prompt à coller dans tout projet ; chaîne complète, routage erreurs/Drive, 15 règles. |
| 19/09 | **`scripts/verifier-avant-push.sh`** — filet anti-fuite (dépôt public), inscrit dans `CLAUDE.md`. |

## CE QUE JE SAIS DU DRIVE (lu le 19/09 — `memoire/CARTE-DRIVE.md`)

**906 fichiers Empire**, du 18/06 au 19/09, dans 19 dossiers. Les plus gros : la base **La Loi
Avec Moi** (368 fiches sourcées) et **COMPILATION & SYNOPSIS** (283 rapports de sessions, dont
149 « boucle-caelum »). **Portes d'entrée** : ⭐ SOURCE UNIQUE DE VÉRITÉ → 00 SYNOPSIS MAÎTRE →
un « 00 » par projet. **Ce qui cloche** : 7 protocoles maîtres concurrents, LLAM en 3 copies,
28 dossiers vides, et deux documents qui se contredisent sur le statut de LLAM (gelé / vitrine)
— trois lignes ouvertes dans A-DECIDER. Dossiers privés : **non ouverts**, par choix.
**Ce que j'ai appris de la façon dont tes agents travaillent** : `codex/expertise/methode-agents.md`
(6 principes) et `erreurs-transverses.md` (9 familles, 2 récidivent).

## EN COURS (sans toi)

- **Routine quotidienne : EN PAUSE depuis le 20/09** (`trig_01RXTwrecsCLboaL6kMmn6Ry`). Sa
  première passe (20/09 04:06 UTC) a tourné 7 min, coûté **2,51 $**, et **n'a rien pu pousser** :
  ses sessions n'ont aucun dépôt attaché (`sources: []`, VÉRIFIÉ). Même limite que tes autres
  routines. **Pour la remettre en service : attacher le dépôt avec droits de push à
  l'environnement des routines (réglage claude.ai, à toi), puis réactiver.** Sans ça, elle coûte
  et ne dépose rien. Détail : ligne A-DECIDER du 20/09.

- **Parcours 1 — couche 4 (RAG local) : TERMINÉ.** AnythingLLM Desktop **VALIDÉ NON INTÉGRÉ**
  (scout + licence + sécurité concordants), deux réserves rejetées. Prochaine étape = **Zone 1
  sur ta machine** (7 étapes dans `codex/candidates/CAND-001-rag-local-windows.md`), puis ton
  accord. **Installer, c'est toi.**

## RESTE — ordre des couches, aucune sautée

| # | Couche | État |
|---|---|---|
| 1 | Moteur | ✅ fait. Manque : la mesure **après 10 min de charge**, et le profil `atlas-fr` (commande donnée le 16/09, jamais lancée). |
| 2 | Interface | terminal, suffit pour l'instant |
| 3 | Mémoire | ✅ fichiers en place (`memoire/`, `apprentissage/`) — s'enrichissent à chaque rafale |
| 4 | RAG | ✅ candidat validé (AnythingLLM) — **attend ta Zone 1 + ton accord** |
| 5 | Outils / agent | après 4, avec `sentinelle-exfiltration` |
| — | Fine-tuning | **FERMÉ** — motif matériel + démontré |

## DÉCISIONS EN ATTENTE — `/codex/A-DECIDER.md`, 5 lignes ATLAS/Caelum

D-001 (gel) · Où vit ATLAS · Premier domaine · **Peppol avant 1er client** · Zone 1 AnythingLLM · 3 décisions révélées par le Drive (protocole de référence, statut LLAM, copies Archive) · 2 familles d'erreurs non tenues. *(JobYourself : clos. Routine : créée, tranchée.)*

## RÈGLES NÉES DE MES ERREURS (à relire avant d'agir) — `apprentissage/REGLES-APPRISES.md`

15 règles. Les 5 d'aujourd'hui et d'hier : R-011 (une commande interactive s'annonce), R-012 (jamais `printf` pour un commit), R-013 (jamais `git` sans `fetch`), R-014 (« inaccessible » parle de mes outils, pas du monde), R-015 (dépôt public : rien de personnel, nulle part).

## NON VÉRIFIÉ, à ce jour

Ton statut actuel (salariée / allocataire / autre) · le volume réel de tes heures (la forme, oui : rafales) · la valeur des 20 projets dormants · le palier de débit du modèle à chaud · le coût réel d'une passe de routine · si JobYourself porte l'obligation Peppol de ses membres.

## Drive — à jour au 19/09

Dossier « ATLAS — IA locale » : `01 fiche machine` (remplie par PowerShell, doc d'origine gardé) ·
`02 ERREURS ET RÉUSSITES` **à jour** (4 erreurs, jalons, ce qui attend) · `03 PROMPT MAÎTRE v2`.
Procédure de mise à jour : `continuite/SYNC-DRIVE.md`.

# ATLAS — ÉTAT DU PROJET

> **Le seul fichier à ouvrir pour reprendre.** Mis à jour : **2026-09-19**.
> Ton temps est en rafales de 2-4 h (mesuré) : ce fichier existe pour que la reprise coûte
> 30 secondes, pas 50 minutes.

## À FAIRE PAR TOI — 3 choses, dans cet ordre, et rien d'autre ne bloque

1. **Un e-mail à JobYourself** — *« Si je facture via vous, les factures partent-elles sous votre
   n° de TVA et votre raccordement Peppol, ou dois-je me raccorder moi-même ? »*
   **Avant toute démarche de statut.** Trois voies s'excluent pendant 2 ans ; cette réponse
   décide laquelle. → `deliberations/DELIBERATIONS.md`, section « CONVERGENCE ».
2. **Deux réponses d'une ligne** pour le dossier statut : as-tu aujourd'hui une activité
   salariée (ou des allocations) ? Et où sont les statuts de ton asbl ?
3. **Trancher D-001** (gel des nouveaux projets jusqu'au 1er message prospect) —
   `deliberations/FICHE-DECISION-D-001.md`, 2 minutes. Option C « pas maintenant » est légitime.

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
| 19/09 | **`scripts/verifier-avant-push.sh`** — filet anti-fuite (dépôt public), inscrit dans `CLAUDE.md`. |

## EN COURS (sans toi)

- **Parcours 1 — couche 4 (RAG local)** : `scout` cherche 3 candidats Windows/sans Docker/100 % local.
  Puis `guardian-licences` + `sentinel-securite`. **Tu décideras d'installer, ou pas.**

## RESTE — ordre des couches, aucune sautée

| # | Couche | État |
|---|---|---|
| 1 | Moteur | ✅ fait. Manque : la mesure **après 10 min de charge**, et le profil `atlas-fr` (commande donnée le 16/09, jamais lancée). |
| 2 | Interface | terminal, suffit pour l'instant |
| 3 | Mémoire | ✅ fichiers en place (`memoire/`, `apprentissage/`) — s'enrichissent à chaque rafale |
| 4 | RAG | 🔧 Parcours 1 en cours |
| 5 | Outils / agent | après 4, avec `sentinelle-exfiltration` |
| — | Fine-tuning | **FERMÉ** — motif matériel + démontré |

## DÉCISIONS EN ATTENTE — `/codex/A-DECIDER.md`, 5 lignes ATLAS/Caelum

D-001 (gel) · Où vit ATLAS · Premier domaine · **Peppol avant 1er client** · **Ordre : question JobYourself** · Routine quotidienne (proposée, dépense récurrente).

## RÈGLES NÉES DE MES ERREURS (à relire avant d'agir) — `apprentissage/REGLES-APPRISES.md`

15 règles. Les 5 d'aujourd'hui et d'hier : R-011 (une commande interactive s'annonce), R-012 (jamais `printf` pour un commit), R-013 (jamais `git` sans `fetch`), R-014 (« inaccessible » parle de mes outils, pas du monde), R-015 (dépôt public : rien de personnel, nulle part).

## NON VÉRIFIÉ, à ce jour

Ton statut actuel (salariée / allocataire / autre) · le volume réel de tes heures (la forme, oui : rafales) · la valeur des 20 projets dormants · le palier de débit du modèle à chaud · le coût réel d'une passe de routine · si JobYourself porte l'obligation Peppol de ses membres.

## Écart connu

Le document Drive `02 — ERREURS ET RÉUSSITES` est **périmé** (anciens chemins, 4 erreurs non remontées) : l'outil Drive disponible ne modifie pas le contenu d'un document existant. Le dépôt fait foi. À refaire quand un outil le permettra, ou par toi.

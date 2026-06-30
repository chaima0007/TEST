# SOLEA — Gérer toutes les problématiques (résilience)

> Objectif : anticiper **chaque problème qui peut survenir** et avoir une réponse prête.
> Un site sérieux n'est pas celui qui n'a jamais de problème — c'est celui qui les a déjà prévus.

## 1) Technique / disponibilité

| Problème | Parade (déjà en place ou à activer) |
|---|---|
| **Pic de trafic massif** | Site **100 % statique** servi par un **CDN** (Cloudflare/Netlify) → encaisse des millions de visites sans serveur à faire tomber. ✅ par conception |
| Panne d'hébergeur | Le code est sur **GitHub** → redéploiement ailleurs en minutes. Garder un 2e hébergeur prêt. |
| Lien affilié cassé | Config **centralisée** (`AFF.ref`) → un seul endroit à corriger. Page d'aide pour signaler. |
| Site lent sur mobile | Zéro framework, CSS inline, images en lazy/hotlink → déjà léger. |
| Perte de données | Tout est versionné dans git ; la newsletter est chez un prestataire (Brevo) exporté régulièrement. |

## 2) Légal / conformité

| Problème | Parade |
|---|---|
| Accès mineurs | **Age-gate 18+** sur chaque page (mémorisé). ✅ |
| Contenu illégal hébergé | SOLEA **n'héberge rien** → renvoi vers plateformes officielles. Risque structurellement évité. ✅ |
| Demande de retrait (DMCA) | Procédure **DMCA / signalement** prête (`LEGAL_MODELES.md`) + email dédié + délai 72 h. |
| Droit à l'image / célébrités | **Interdit** (jamais de personne réelle non consentante). Règle absolue. ✅ |
| RGPD / cookies | Bannière consentement + politique de confidentialité (collecte minimale). |
| Fiscalité | Statut **auto-entrepreneur**, revenus déclarés. |

## 3) Paiement / revenus

| Problème | Parade |
|---|---|
| Chargebacks | Les paiements se font **chez les partenaires** (pas chez nous) → on ne porte pas le risque. ✅ |
| Programme d'affiliation qui change ses règles | **Diversifier** : plusieurs partenaires + pub + newsletter. Ne jamais dépendre d'un seul. |
| Régie pub qui coupe | Avoir 2 régies + l'affiliation en parallèle. |
| Revenu en dents de scie | Newsletter + abonnements par catégorie = base **récurrente**. |

## 4) Marketing / réputation

| Problème | Parade |
|---|---|
| Bannissement réseau social | Façade esthétique « safe » + jamais explicite + **multi-canal** (SEO, Reddit, X, Pinterest). |
| Bannissement Reddit | Respect strict des règles (pas de prix en titre, se faire vérifier, 3–7 posts/jour). |
| Bad buzz / plainte | Pages légales claires + contact réactif + retrait rapide sur demande justifiée. |
| Vol de notre design | Marque déposée (à faire) + le vrai moat = audience + curation, pas le code. |

## 5) Support / utilisateur (« être pris au sérieux »)

| Problème | Parade |
|---|---|
| Question à toute heure | **Assistance 24/7** (`aide.html`) : assistant instantané + formulaire (réponse < 24 h). ✅ |
| Demande spécifique | Formulaire de contact dédié, traité sérieusement. ✅ |
| Utilisateur perdu | Le **Diapason** (quiz) guide ceux qui ne savent pas par où commencer. ✅ |
| Barrière de langue | Site **bilingue FR/EN** (sélecteur partout). ✅ |

## 6) Plan de continuité (que faire si…)
- **…le site tombe ?** Redéployer depuis GitHub sur l'hébergeur de secours.
- **…un partenaire ferme ?** Basculer `AFF.ref` vers un autre partenaire (1 ligne).
- **…une plainte arrive ?** Appliquer la procédure DMCA (retrait < 72 h) + accuser réception.
- **…un canal nous bannit ?** Reporter l'effort sur les autres canaux ; rien ne dépend d'un seul.
- **…le trafic explose ?** Rien à faire : le CDN encaisse. Surveiller juste les revenus (analytics).

> **Principe directeur** : aucune dépendance unique (hébergeur, partenaire, canal, langue).
> Chaque maillon a une alternative. C'est ça, un site qui « gère toutes les problématiques ».

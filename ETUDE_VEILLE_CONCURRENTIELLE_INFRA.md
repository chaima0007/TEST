# Veille concurrentielle (écoute marché) + Comparatif infrastructure — Caelum

> Revue : 2026-06-29. Sourcé (Reddit/HN/forums + comparatifs 2026). Honnête.
> **Non-doublon** : `provider_arbitrage_protocol.py` = failover de fournisseurs d'**API** ;
> `DEPLOIEMENT.md` = runbook « comment déployer ». Ce document = **décision stratégique** :
> ce que dit le marché + quel hébergeur/domaine/serveur choisir (budget).

---

# PARTIE A — Veille concurrentielle : frustrations & besoins non satisfaits

## A.1 Ce que les gens disent vraiment (sources)
**E-facturation / Peppol** (Hacker News, forums Xojo/Odoo, PeppolEDGE) :
- « L'accès au réseau Peppol **n'est pas gratuit** ; l'accès direct est cher et exige des audits. Des tiers compliqués et chers émergent. » (HN)
- « De l'argent retiré aux **freelances et petites PME pour chaque facture**. »
- « Les outils PDF de base ne suffisent plus → il faut **un abonnement payant** pour faire ce qui était gratuit. »
- **~1 % d'échanges problématiques** au lancement belge (qualité des données d'enregistrement, certificats) — à l'échelle nationale = des centaines de milliers de factures (PeppolEDGE).
- Confusion réelle : sens de la facture (B2B revendeurs), réception des factures entrantes.

**GDPR / NIS2** (StartupTribunal, Nuvm, Rediacc, Legiscope) :
- « Outils GDPR **trop complexes et trop chers**, exigent du personnel conformité que les PME n'ont pas. » (pain 8-9/10)
- « L'industrie vous vend une **solution à 50 000 € pour un problème à 99 €** ; tarification basée sur la **peur**. » (Nuvm)
- Coûts réels constatés : plateformes GDPR+NIS2 **4 800 → 60 000 €/an** (médiane mid-market ~14 500 €/an) ; consultant NIS2 15-50 k€.
- « 5 outils, 3 contrats, 2 logs qui se chevauchent, **1 trou qu'on ne peut pas combler** » (preuve continue, reporting Article 23) (Rediacc).

**Logiciels comptables** (analyse Reddit/Discury) :
- Tension **dirigeant (simplicité) vs comptable (contrôle = son « moat »)**. Le gagnant = celui qui offre une **UI moderne au client + features pro au comptable**.
- **Solo practitioners sous-servis** : outils « overkill » et chers ; « choqués par 20 $/mois ».

## A.2 Confrontation à NOS solutions (does our work meet demand?)
| Besoin / frustration validé(e) | Notre réponse actuelle | Verdict |
|---|---|---|
| « Trop cher, basé sur la peur » | Honnêteté radicale + **conformité finançable** (aides 50-75 %) + prix prévisible | ✅ **Réponse directe et différenciante** |
| « Trop complexe, je ne sais pas si je suis concerné » | Simulateur gratuit 1 min + checklist + score + échéances | ✅ **Cœur de notre offre** |
| « Quelle info fiable ? » | Sources officielles tier1, datées, traçables | ✅ Fort |
| Déficit d'info (54 % ignorent la déductibilité 120 %) | FAQ + contenu + calculateur d'aide nette | ✅ Couvert |
| Comptable = gatekeeper | **Widget marque blanche fiduciaires** | ✅ Aligné sur l'insight Reddit |
| Peur NIS2 / responsabilité dirigeant | Hooks + fiches NIS2 sourcées | ✅ Couvert (info) |

## A.3 Trous que NOUS ne couvrons PAS (et notre position honnête)
1. **Exécution e-facture (envoi Peppol)** : on **n'est pas** un access point. Pain = « quel outil, est-ce gratuit ». → **Opportunité honnête** : un **comparateur neutre des access points Peppol** + guide « se conformer à moindre coût » (orienter, pas exécuter).
2. **Preuve continue / reporting Article 23 NIS2 / workflows GRC (ROPA, DSAR, DPIA)** : on **diagnostique**, on ne **produit pas la preuve**. → Rester sur la couche **diagnostic + financement + veille** ; **partenariat** avec un éditeur GRC plutôt que tout refaire.
3. **Continuous evidence** : notre attestation est une **auto-évaluation** (assumé), pas un registre d'audit complet.

## A.4 Conclusion veille
Notre travail **répond aux 3 douleurs les plus validées** : **coût/peur**, **complexité**, **déficit d'info** — et notre angle « honnêteté + finançable + sourcé » est **exactement l'espace laissé vide** par les acteurs qui vendent la peur. Le marché demande du **simple, abordable, honnête** : c'est notre positionnement.
**Ne pas** dériver vers le GRC lourd ou l'access point Peppol (couches d'exécution chères) : rester la **porte d'entrée** (diagnostic → financement → veille → orientation), et **capter le comptable** via la marque blanche. Prochaine pépite cohérente : **comparateur neutre d'access points / outils Peppol**.

---

# PARTIE B — Comparatif infrastructure (hébergement · domaines · serveurs), budget

## B.1 Hébergement (Next.js, sites surtout statiques, B2B UE, RGPD = argument de vente)
| Option | Prix | RGPD / souveraineté | Pour / Contre |
|---|---|---|---|
| **Cloudflare Pages** | **0 €** (commercial OK, bande passante illimitée) | US-enregistré mais **edge UE** + résidence UE (option) ; **meilleur anti-DDoS** | ✅ budget, edge UE, statique ; ⚠️ support Next.js « en retard » sur le SSR |
| **Vercel** (actuel) | Hobby gratuit = **non commercial** → **Pro 20 $/user** | **US (CLOUD Act)**, RGPD « limité » sauf config ; **pin régions UE** (`fra1`/`arn1`) | ✅ meilleur DX Next.js, previews ; ⚠️ US, coûteux en bande passante |
| **Hetzner** (DE/FI) | VPS dès **3,49 €/mo** | **EU, pas de CLOUD Act**, GDPR plein, BSI C5 | ✅ rapport prix/perf imbattable (~14× AWS) ; ⚠️ DevOps requis, pas de CDN/K8s managé |
| **Scaleway** (FR) | compétitif, egress souvent gratuit | **EU**, GAIA-X, HDS, SecNumCloud | ✅ excellent DX UE, managé ; ⚠️ console partiellement US |
| **OVHcloud** (FR) | VPS ~7 €/mo | **EU**, ISO 27001/HDS/SecNumCloud, anti-DDoS | ✅ certifs UE larges (regulated) ; ⚠️ DX moins fluide |

**Recommandation budget (mon avis) :**
- **Maintenant** (site surtout statique, **données perso minimes**) : **Cloudflare Pages** = meilleur rapport coût/UE/anti-DDoS (**0 €**), ou **Vercel Pro** si on veut le DX Next.js maximal.
- **Quand les données perso grossissent** (leads, comptes) : placer la **couche données** chez un **hébergeur UE-natif** (**Scaleway** ou **Hetzner**) → **immunité CLOUD Act** = argument de vente cohérent avec notre discours RGPD. Hybride : front (Cloudflare/Vercel) + données (UE-natif).
- ⚠️ Cohérence : on vend de la conformité — héberger les **données personnelles** hors UE (CLOUD Act) serait incohérent. À arbitrer dès qu'il y a des données clients.

## B.2 Domaines (registrar)
| Registrar | .com (renouv.) | Atouts | Limite |
|---|---|---|---|
| **Cloudflare Registrar** | **~10,46 $** (à prix coûtant, **pas de hausse au renouvellement**) | WHOIS gratuit, DNSSEC 1-clic | ⚠️ **ne vend pas les ccTLD** type **.be** |
| **Porkbun** | ~11,06 $ (flat) | bonne UX, large TLD | — |
| **Namecheap** | ~14 $ (1ʳᵉ année ~6 $) | large choix TLD, support | hausse au renouvellement |
| **OVH / Gandi** (FR/UE) | variable | **gèrent le .be**, UE | un peu plus chers |
| **GoDaddy** | ~22 $ + upsells | — | ❌ à éviter (renouv. + ToS 2026) |

**Recommandation :**
- **`laloiavecmoi.be`** (ccTLD belge) → **OVH** ou **Gandi** (UE, accrédités .be ; Cloudflare ne fait pas le .be).
- **`.com` Caelum** (si pris) → **Cloudflare Registrar** ou **Porkbun** (prix coûtant, pas de piège). 
- Coût annuel total domaines : **~10-20 €/domaine** — négligeable.

## B.3 Serveurs / e-mail / DNS
- **DNS** : Cloudflare (gratuit, rapide, DNSSEC) quel que soit l'hébergeur.
- **E-mail pro** (contact@laloiavecmoi.be / chaima.caelumpartners@gmail.com) : pour un domaine propre, **e-mail UE** type **Infomaniak** / **OVH** (~1-5 €/mo) plutôt que tout sur Gmail — séparation des projets respectée.
- **Webhook leads** (décision en attente) : un simple endpoint (Cloudflare Worker gratuit, ou n8n auto-hébergé Hetzner) suffit — pas besoin d'usine.

## B.4 Budget cible (ordre de grandeur, mensuel)
| Poste | Démarrage | À l'échelle |
|---|---|---|
| Hébergement | **0 €** (Cloudflare Pages) | 20-50 € (Vercel Pro / VPS UE) |
| Domaines | ~2 €/mo (amorti) | idem |
| E-mail pro | 0-5 € | 5-15 € |
| Données UE (si besoin) | 0 € | 5-15 € (Hetzner/Scaleway VPS) |
| **Total** | **≈ 0-10 €/mo** | **≈ 35-80 €/mo** |

> Conclusion : on peut **démarrer quasi gratuitement** et garder un coût infra **très faible** même à l'échelle — la marge SaaS (75-85 %) n'est pas menacée par l'infra.

---

## Verdict global
1. **Veille** : notre produit **répond aux douleurs les plus fortes** (coût/peur, complexité, info) ; on reste sur la **couche entrée** (diagnostic/financement/veille) et on **capte le comptable** — on ne court pas après le GRC lourd ni l'access point Peppol. Prochaine pépite : **comparateur Peppol neutre**.
2. **Infra** : **Cloudflare Pages (0 €)** pour démarrer ; **données UE-natif (Scaleway/Hetzner)** dès qu'il y a des données clients (cohérence RGPD = argument de vente) ; **.be chez OVH/Gandi**, **.com chez Cloudflare/Porkbun** ; **éviter GoDaddy**. Budget infra **négligeable**.

> Sources : Hacker News (PEPPOL), forums Xojo/Odoo, PeppolEDGE, StartupTribunal, Nuvm, Rediacc, Legiscope (douleurs marché) ; HostingSift, SoftwareSeni, Gart, proreactware, UKWebMarketing (hébergement) ; dev.to, CompareSharp, DevToolPicks, InstantDomainSearch, Corg (registrars). Chiffres 2026, à revérifier avant achat.

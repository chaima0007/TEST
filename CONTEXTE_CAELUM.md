# MÉMOIRE PERMANENTE — CAELUM PARTNERS
*Fichier de référence — à jour au 19 juin 2026*

---

## QUI EST CHAIMA

- **Nom** : Chaima Mhadbi
- **Ville** : Bruxelles, Belgique
- **Situation** : Au chômage, en formation, 2€ brut/heure, seule, sans enfants
- **Organisation chômage** : CSC (Confédération des Syndicats Chrétiens)
- **Seuil ONEM** : isolée → 5 217,16€/trimestre net maximum
- **Deux entités légales** :
  - ASBL (présidente) — activité sociale, séparée légalement de Caelum
  - CAELUM PARTNERS — activité commerciale IA en construction
- **RÈGLE ABSOLUE** : le numéro de TVA de l'ASBL ne peut PAS être utilisé pour Caelum Partners

---

## CAELUM PARTNERS — CONTEXTE BUSINESS

- **Services** : 500€ (site web, 7j) · 1 500€ (automation IA, 14j) · 3 000€ (pack complet, 30j)
- **Vision** : référence européenne IA pour PME en 5 ans
- **Phase actuelle** : lancement — 0 client, rampe de décollage
- **Marché** : PME belges, Bruxelles d'abord, puis Wallonie, puis France/Luxembourg
- **Prospection** : pas encore commencée — à démarrer sur LinkedIn immédiatement
- **Email contact** : contact@caelumpartners.agency
- **Site** : caelumpartners.agency (déployé sur Cloudflare Pages depuis dossier `website/`)

---

## ARCHITECTURE TECHNIQUE

- **API IA** : Google Gemini — `from google import genai` + `from google.genai import types`
- **Modèle** : `gemini-2.0-flash`
- **Client** : `genai.Client(api_key=API_KEY)`
- **Streaming** : `client.models.generate_content_stream(...)`
- **Config** : `types.GenerateContentConfig(system_instruction=..., temperature=..., max_output_tokens=...)`
- **IMPORTANT** : l'ancienne API (`import google.generativeai`) est dépréciée — tous les agents utilisent la nouvelle
- **Variable d'environnement** : `GEMINI_API_KEY`
- **Lanceur principal** : `python lancer.py` (menu de 77 agents)
- **Repo GitHub** : `chaima0007/TEST`
- **Branche de travail** : `claude/multi-agent-migration-factory-riujie`
- **Dossier Windows local** : `C:\Caelum_Projets`
- **Agents Ollama (locaux)** : connectent à `http://localhost:11434`, stockent dans `C:\Caelum_Projets\`

---

## DIRECTIVES PERMANENTES (à respecter dans tout nouveau travail)

1. **Sécurité des données** : "quoi que tu fasse pense toujours à sécuriser mes données, je veux des agents en conséquence pour laisser aucun hacker nous approcher"
2. **Séparation ASBL/Caelum** : jamais mélanger les deux entités, jamais utiliser le TVA de l'ASBL
3. **Conformité ONEM** : toujours calculer l'impact sur les allocations avant de recommander un revenu
4. **Nouveaux agents** : toujours utiliser le pattern google.genai (nouveau), jamais google.generativeai
5. **Format souverain** : les fichiers .md dans `SYSTEME_AGENTS/` sont des configs portables multi-plateforme
6. **Température** : 0.1-0.15 pour agents légaux/audit, 0.2-0.25 pour stratégie, 0.3-0.35 pour créatif
7. **Toujours commiter et pusher** après chaque création de fichier (stop hook git actif)

---

## LES 77 AGENTS — INVENTAIRE COMPLET

### BLOC 1 — CORE OPÉRATIONNEL (1-25)
| # | Fichier | Rôle |
|---|---|---|
| 1 | orchestrateur.py | Tout déléguer à l'IA |
| 2 | agent_commercial.py | Prospects, propositions, emails (BANT, LinkedIn B2B belge) |
| 3 | agent_veille.py | Marché IA et concurrents |
| 4 | agent_facturation.py | Factures et relances paiement |
| 5 | agent_recrutement.py | CV, fiches poste, entretiens |
| 6 | agents.py | Formation et apprentissage |
| 7 | usine_migration_logicielle.py | Moderniser du code legacy |
| 8 | securite.py | Audit et protection données |
| 9 | agent_reference.py | Index et doc de tous les projets |
| 10 | agent_juridique.py | Contrats, CGV, RGPD, NDA |
| 11 | agent_support_client.py | SAV 24/7, FAQ, onboarding |
| 12 | agent_chef_projet.py | Planification, risques, rapports |
| 13 | agent_guide.py | Priorités quotidiennes, prochaine étape |
| 14 | agent_watchdog.py | Surveillance 24h/24 de tous les agents |
| 15 | agent_fantome.py | Audit silencieux, zéro trace |
| 16 | agent_commandant.py | Fait travailler tous les agents en équipe |
| 17 | agent_resolveur.py | Résout les problèmes de manière ultra-pro |
| 18 | agent_crm.py | Pipeline commercial lead → client → CA |
| 19 | agent_email.py | Cold outreach + séquences + propositions |
| 20 | agent_dashboard_ceo.py | Vue exécutive revenus, KPIs, alertes |
| 21 | agent_memoire_session.py | Se souvient de tout ce qu'on a fait |
| 22 | agent_autopilot.py | Cerveau autonome — analyse et agit seul |
| 23 | agent_growth.py | Growth hacking — 0 à 10 clients en 90 jours |
| 24 | agent_empire.py | Vision 5 ans — expansion et domination |
| 25 | agent_titan.py | 20 experts + 50 simulations — zéro erreur |

### BLOC 2 — BUSINESS & ADMINISTRATIF BELGE (26-31)
| # | Fichier | Rôle |
|---|---|---|
| 26 | agent_comptable_belge.py | TVA, BCE (~83€), INASTI, déductions, factures légales |
| 27 | agent_financement.py | Innoviris, Hub Brussels, subventions, pitch investisseur |
| 28 | agent_tarification.py | Pricing, ROI client, packages, upsell |
| 29 | agent_marque.py | Branding, storytelling Chaima, LinkedIn, positionnement |
| 30 | agent_mental.py | Coach entrepreneurial, syndrome imposteur, routine |
| 31 | agent_auditeur_financier.py | Simulation ONEM+Caelum, seuil optimal, conformité CSC |

### BLOC 3 — STRATÉGIE & RÉSILIENCE (32-34)
| # | Fichier | Rôle |
|---|---|---|
| 32 | agent_red_team.py | Black Swan, stress tests 4 niveaux, plan continuité |
| 33 | agent_flux_economique.py | DSO, Cash Conversion Cycle, Revenue/Hour, frictions |
| 34 | agent_synthese_exponentielle.py | Unifie tous agents → décision stratégique unique |

### BLOC 4 — DIRECTIVE MAÎTRE (35-37)
| # | Fichier | Rôle |
|---|---|---|
| 35 | agent_stratege_croissance.py | Scalabilité ×100, levier exponentiel, paliers |
| 36 | agent_asset_builder.py | Transformer revenus en actifs durables |
| 37 | agent_convergence.py | Légalité belge comme avantage compétitif |

### BLOC 5 — FLOTTE DOMINATION EUROPÉENNE (38-47)
| # | Fichier | Rôle |
|---|---|---|
| 38 | agent_architecte_singularite.py | Avantage concurrentiel inégalable |
| 39 | agent_sniper_goulots.py | Theory of Constraints, éliminer bottlenecks |
| 40 | agent_maitre_velocite.py | Vélocité capital ×10 en 90 jours |
| 41 | agent_simulateur_black_swan.py | Antifragilité, barbell strategy, queue risks |
| 42 | agent_premiers_principes.py | Décomposer à l'atome, reconstruire sans biais |
| 43 | agent_symbiose.py | Synergies inter-agents, workflows chaînés |
| 44 | agent_chasseur_marches.py | Opportunités avant la concurrence |
| 45 | agent_gardien_playbook.py | Mémoire institutionnelle, décisions → protocoles |
| 46 | agent_conformite_offensive.py | Légalité belge = avantage compétitif |
| 47 | agent_influence_systemique.py | Autorité IA Belgique, presse, partenariats |

### BLOC 6 — ARCHITECTURE LOCALE OLLAMA (48-50)
| # | Fichier | Rôle |
|---|---|---|
| 48 | agent_ingenieur_code.py | Dev/debug/sécurité code via Ollama local (sans tokens) |
| 49 | agent_testeur_qa.py | Tests en boucle, logs d'erreurs, QA (Ollama) |
| 50 | agent_analyste_legal.py | Corpus juridiques → JSON/SQL structuré (Ollama) |

### BLOC 7 — SYSTÈME DE CONSCIENCE (51-52)
| # | Fichier | Rôle |
|---|---|---|
| 51 | agent_gardien_coherence.py | Détecte dérives, aligne empire, 5 piliers fondamentaux |
| 52 | agent_synthetiseur_realite.py | Ground Truth : vérif fondamentale, biais, compression |

### BLOC 8 — PROTOCOLE DOMINATION TOTALE (53-57)
| # | Fichier | Rôle |
|---|---|---|
| 53 | agent_chasseur_inefficacite.py | Lean, éliminer gaspillages temps/argent |
| 54 | agent_capteur_signaux.py | Valide opportunités réelles avant la concurrence |
| 55 | agent_architecte_talents.py | Ressources (agents+skills) pour chaque opportunité |
| 56 | agent_force_de_vente.py | Offensive MEDDIC, closing, scoring pipeline |
| 57 | agent_optimiseur_decisions.py | Résultat final : X% parts de marché, profit net |

### BLOC 9 — CAPITAL STRATÉGIQUE (58-62)
| # | Fichier | Rôle |
|---|---|---|
| 58 | agent_architecte_reputation.py | The Anchor : valeur perçue, preuve sociale |
| 59 | agent_valeurs_adjacentes.py | Marchés voisins où Caelum est imbattable |
| 60 | agent_auto_obsolescence.py | Concevoir le produit qui tuera le produit actuel |
| 61 | agent_culture_interne.py | Standards excellence, alignement, mindset empire |
| 62 | agent_historien_empire.py | Log-Keeper : erreurs → protocoles de réussite |

### BLOC 10 — GOUVERNANCE DE LA FLOTTE (73-77)
| # | Fichier | Rôle |
|---|---|---|
| 73 | agent_auditeur_flotte.py | Protocole audit 5D, score /100, verdict qualité |
| 74 | agent_protocole_identite.py | Cohérence marque, bio officielle, charte Caelum |
| 75 | agent_directive_comportement.py | 8 règles non négociables pour toute la flotte |
| 76 | agent_architecte_diversification.py | Micro-branches autonomes, MVP lean, omniprésence |
| 77 | agent_preuve_travail.py | Études de cas, vitrines, kit site web, LinkedIn |

### BLOC 11 — SECTEURS HAUTE VALEUR BELGIQUE (63-72)
| # | Fichier | Rôle |
|---|---|---|
| 63 | agent_notaire_immo.py | Annonces FR+NL, actes, baux, prospection agences |
| 64 | agent_fiduciaire.py | Rapports gestion, optimisation fiscale, onboarding |
| 65 | agent_rh_belge.py | Offres emploi, préavis, CCT belge, Dimona |
| 66 | agent_avocat_ia.py | Mise en demeure, synthèses dossiers, contrats |
| 67 | agent_medical_admin.py | Lettres référence, fiches patient, mutualité INAMI |
| 68 | agent_construction_belge.py | Devis, rapports chantier, PEB, conformité belge |
| 69 | agent_export_bilingue.py | FR/NL/EN/DE, documentation douane, pitch par pays |
| 70 | agent_horeca_belge.py | Menus trilingues, social media, AFSCA, événements |
| 71 | agent_assurance_belge.py | Devoir conseil FSMA, comparatifs, sinistres |
| 72 | agent_formation_pro.py | Catalogues, subventions, rapports compétences |

---

## DÉCISIONS TECHNIQUES PRISES

- Migration complète de `google.generativeai` (déprécié) vers `google.genai` (nouveau)
- Package : `pip install google-genai` (pas `google-generativeai`)
- Tous les agents sauvegardent dans `fichiers/[nom_agent]/`
- Lanceur principal : `lancer.py` (77 options + stats)
- Format Souverain : 25+ fichiers `.md` dans `SYSTEME_AGENTS/` pour portabilité multi-IA
- Stop hook git actif : tout fichier non commité déclenche une alerte

---

## FICHIERS DE CONFIGURATION IMPORTANTS

- `lancer.py` — menu central, 77 agents
- `gemini_client.py` — client partagé (get_client, streamer, generer)
- `memoire_entreprise.json` — mémoire persistante de l'entreprise
- `crm_pipeline.json` — pipeline commercial
- `historique_caelum.json` — historique des décisions
- `website/index.html` — landing page caelumpartners.agency
- `website/_headers` — sécurité Cloudflare (CSP, HSTS, X-Frame-Options)
- `requirements.txt` — `google-genai` (nouveau nom)
- `installer.bat` / `installer.ps1` — installation Windows

---

## CE QUI RESTE À FAIRE

- [ ] Premiers contacts LinkedIn (10 messages/jour)
- [ ] Premier client → premier 500€
- [ ] Connecter Cloudflare Pages au repo GitHub (root: `website/`)
- [ ] Ajouter vrai témoignage client dès le 1er client (remplace les études fictives)
- [ ] Agents 41, 42 (Simulateur Black Swan, Premiers Principes) à vérifier si créés

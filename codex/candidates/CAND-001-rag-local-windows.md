# CAND-001 — RAG local Windows pour ATLAS (couche 4)

> Fiche Candidate §7, produite par **scout**. Aucun code copié. Toute date « consulté le » = **2026-09-19**. Verdicts licence/sécurité réservés à guardian-licences et sentinel-securite.

| Champ | Contenu |
|---|---|
| **ID** | CAND-001 |
| **Besoin couvert** | Faire répondre `qwen2.5:3b` (Ollama existant) à partir de `codex/atlas/corpus/`, **en citant document + passage**, 100 % local, sans Docker ni Python, sur i7-8650U / 16 Go / CPU seul (`codex/atlas/memoire/MACHINE.md`, VÉRIFIÉ 2026-09-16). |
| **Source prioritaire** | AnythingLLM Desktop — https://github.com/Mintplex-Labs/anything-llm · https://docs.anythingllm.com |
| **Sources secondaires** | Open WebUI Desktop — https://github.com/open-webui/desktop · Msty Studio — https://msty.ai/studio/ |
| **Statut / Date** | **PROPOSÉ** / 2026-09-19 |

## Écartés (VÉRIFIÉ, source primaire)

- **LM Studio** : propriétaire (Terms Element Labs), runtime propre, pas de branchement Ollama.
- **GPT4All** : MIT, LocalDocs avec « Sources », mais runtime propre ; distants = Groq/OpenAI/Mistral, pas Ollama (docs.gpt4all.io).
- **Jan** : Apache-2.0, Ollama OK, mais **aucun RAG documentaire** au README janhq/jan.

## Comparatif des 3 retenus (consulté 2026-09-19)

| Critère | **AnythingLLM Desktop** | Open WebUI Desktop | Msty Studio Desktop |
|---|---|---|---|
| Installeur Windows | `.exe` (docs/installation-desktop/windows) | `.exe` x64, **« Early Alpha »** (README) | x64, « install as Administrator for your user account only » |
| Docker requis | Non | Non (embarque Python + llama.cpp) | Non |
| Ollama existant | **Recommandé** : « installing AnythingLLM and Ollama separately and then connecting… automatically detected » | Oui, natif | Oui en « Remote Provider » ; **installe par défaut sa propre instance Ollama** (docs onboarding) |
| RAG + citations | « drag-and-drop uploads and source citations » (README) ; cite le **nom de fichier** | « Citations in RAG Feature » (docs/features/rag) | « Get citations from your sources » (changelog) ; rerank/web links exigent une clé Jina (cloud, optionnel) |
| Réseau par défaut | **Télémétrie ON** (PostHog, « No IP »), opt-out « sidebar > Privacy » ; hors télémétrie : `cdn.anythingllm.com`, `githubusercontent.com` (README). **L'installeur télécharge libs GPU Ollama, FFmpeg, modèles Meeting Assistant depuis leur CDN** | Desktop : « No telemetry… No phone-home » (README), mais l'app embarquée fait **3 appels d'office** : version check GitHub, liste modèles OpenAI, update embedding Hugging Face — désactivables par variable (docs quick-start) | « We… DO NOT collect any analytics or telemetry data » (msty.ai/privacy) ; réseau pour téléchargements, Real-Time Data, cloud, licence Lemon Squeezy (Aurum) |
| Compte | Non | Compte **admin local** au 1er lancement | Non (Free) |
| Licence exacte | **MIT**, « Copyright Mintplex Labs Inc. » (LICENSE) | Wrapper **AGPL-3.0** + app **« Open WebUI License »** = BSD-3 + clause 4 branding (exemption ≤ 50 utilisateurs/30 j) | **Propriétaire** CloudStack LLC ; « Aurum Annual… is required for commercial use » (Terms), 149 USD/utilisateur/an |
| Dernière release | v1.16.1, « 27 Aug » (année non affichée → 2026, PLAUSIBLE) | Desktop v0.0.20, **2026-05-07** ; app v0.11.3, 2026-08-31 | 2.9.6, **2026-07-24** |
| Mainteneurs | 65 578 étoiles ; 2 dominants (timothycarambat 1 474, shatfield4 415) | 2 067 étoiles ; **1 contributeur réel** (tjbck 143, NN708 1) | Code fermé → **NON VÉRIFIÉ** |
| RAM annoncée | 16 Go, « 8-core CPU (any) » | 16 Go+ local / 4 Go remote | NON VÉRIFIÉ |

## Prioritaire : AnythingLLM Desktop

Seul à cumuler installeur **stable**, licence **MIT** sans clause, doc qui **recommande** l'Ollama déjà installé, citations affichées, embedder CPU + LanceDB intégrés. Ses deux points noirs (télémétrie ON, CDN à l'install) sont **documentés, désactivables, donc testables en Zone 1**.

**Les deux autres après :** Open WebUI Desktop = alpha, une seule personne, licence à deux étages, trois appels réseau d'office. Msty = propre en télémétrie mais **fermé** (audit limité au trafic), payant dès l'usage commercial, second Ollama par défaut.

## Extrait illustratif

« installing AnythingLLM and Ollama separately and then connecting AnythingLLM to your local Ollama instance - which will be automatically detected » — voir source : https://docs.anythingllm.com/installation-desktop/windows

## Objection Contradicteur

1. **Le RAG ralentit deux fois cette machine.** `prompt eval rate` = 21,34 tokens/s (MACHINE.md). 4 extraits ≈ 1 500-3 000 tokens à relire **avant** d'écrire → 70 à 140 s par question, hors bridage. Fiabilité MODÉRÉE (calculé, non mesuré). Un **timeout Ollama de 5 min** est rapporté (insiderllm.com, 2026-02-08, NON VÉRIFIÉ dans la doc).
2. **La date n'est pas citée nativement** : citation par nom de fichier ; le champ `published` = date d'ingestion, « ALWAYS wrong » (avonture.be, 2026-08-17, PLAUSIBLE). La date devra être **dans le nom ou l'en-tête** du fichier — procédure d'ingestion à écrire.
3. Deux sorties réseau **avant** tout réglage : R-004 exige une capture de trafic, pas une lecture de README.

## Argument Avocat

MIT, 65 k étoiles, releases mensuelles, télémétrie **listée événement par événement** avec lien vers le code : le plus **auditable** des trois. L'objection 1 vaut pour tout RAG sur ce CPU ; l'objection 2 se règle par nommage daté, déjà prévu par `corpus/README.md`.

---

    DE : scout                     POUR : guardian-licences + sentinel-securite (parallèle, Parcours 1)
    OBJET : Passer AnythingLLM Desktop (v1.16.1, MIT) en Zone 1 comme RAG local sur Ollama existant ; Open WebUI Desktop et Msty Studio en réserve.
    VERDICT : PROPOSÉ
    PARCE QUE : docs.anythingllm.com/installation-desktop/windows (consulté 2026-09-19) recommande la connexion à l'Ollama déjà installé ; LICENSE = MIT (raw.githubusercontent.com, consulté 2026-09-19) ; README liste citations et télémétrie désactivable in-app.
    NON VÉRIFIÉ : année de la release v1.16.1 (non affichée par GitHub) ; timeout 5 min Ollama (source tierce) ; RAM réelle de l'app sur CPU seul ; mainteneurs Msty (code fermé) ; cadence GPT4All ; comportement réseau réel — aucun des trois n'a été exécuté en Zone 1.
    CE QUI CHANGERAIT MON AVIS : une capture de trafic en Zone 1 montrant une connexion sortante absente du README après désactivation de la télémétrie → REJET ; ou une mesure sur la machine de Chaima > 3 min par réponse RAG → basculer vers plus léger (Msty, ou moins d'extraits).

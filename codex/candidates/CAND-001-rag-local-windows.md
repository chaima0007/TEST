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

## Licence — verdict guardian-licences (2026-09-19)

Fichiers LICENSE lus (raw.githubusercontent.com, cdn.anythingllm.com, API Hugging Face) le 2026-09-19. **P** privé · **C** commercial (Caelum, prestations) · **S** licence sortante / redistribution (§11).

| Composant | Licence lue | P | C | S |
|---|---|---|---|---|
| AnythingLLM (LICENSE) | **MIT**, © Mintplex Labs Inc. | OK | OK | OK, notice + LICENSE conservés |
| Embedder `Xenova/all-MiniLM-L6-v2` | **Apache-2.0** (HF API) | OK | OK | OK, LICENSE + NOTICE |
| LanceDB (LICENSE) | **Apache-2.0** | OK | OK | OK |
| Ollama (LICENSE) | **MIT** | OK | OK | OK |
| **FFmpeg 8.0 téléchargé à l'install** (cdn…/ffmpeg/8.0/LICENSE.txt) | **GPL-3.0**, exécutable séparé (issue #5708, 2026-05-27) | OK | OK | **REJETÉ** en produit fermé (§1) |
| Modèle Meeting Assistant `nvidia/parakeet-tdt-0.6b-v3` (HF API) | **CC-BY-4.0** | OK | OK | Attribution ; téléchargement optionnel |
| Libs GPU Ollama, modèles speaker/segmentation du CDN | **NON VÉRIFIÉ** (non lues / non nommés) | sans objet (CPU) | ? | ? |

**AnythingLLM : VALIDÉ NON INTÉGRÉ (P et C).** Obligations MIT/Apache : conserver notices de copyright et textes de licence, rien d'autre ; aucune en simple usage. **S :** compatible avec une licence sortante propriétaire **si le binaire FFmpeg GPL-3.0 est exclu** et parakeet attribué ; avec FFmpeg, l'ensemble n'est pas MIT.

**Open WebUI Desktop :** wrapper **AGPL-3.0** (LICENSE) ; app « Open WebUI License » = BSD-3 + clause 4 branding (exemption ≤ 50 utilisateurs/30 j). **P : VALIDÉ NON INTÉGRÉ** (l'AGPL n'impose rien à l'usage sans modification ni service réseau). **C : VALIDÉ NON INTÉGRÉ** en outil interne, branding intact ; **REJETÉ** si modifié et exposé à des clients. **S : REJETÉ.**

**Msty Studio :** propriétaire CloudStack LLC (msty.ai/terms) : « the exercise of your trade or profession for which you are compensated… does not qualify » comme Personal Use. **P : VALIDÉ NON INTÉGRÉ. C : REJETÉ sans Aurum** (149 USD/an, NON VÉRIFIÉ). **S : REJETÉ** (« may not be distributed, sold, rented, leased »).

    DE : guardian-licences          POUR : sentinel-securite (parallèle) puis CHAIMA
    OBJET : Accepter AnythingLLM Desktop côté licence en P et C ; interdire sa redistribution dans un produit fermé tant que le FFmpeg GPL-3.0 y est.
    VERDICT : VALIDÉ NON INTÉGRÉ (AnythingLLM P/C ; Open WebUI P/C interne ; Msty P) · REJETÉ (Msty C sans Aurum ; Open WebUI et Msty en S ; AnythingLLM en S avec FFmpeg)
    PARCE QUE : anything-llm/master/LICENSE = MIT ; cdn.anythingllm.com/support/ffmpeg/8.0/LICENSE.txt = GPL-3.0 ; open-webui/desktop/main/LICENSE = AGPL-3.0 ; msty.ai/terms — consultés le 2026-09-19.
    NON VÉRIFIÉ : licences des libs GPU et modèles speaker/segmentation du CDN ; prix Aurum ; contenu réel de l'installeur .exe (Zone 1 non faite).
    CE QUI CHANGERAIT MON AVIS : un LICENSE différent dans l'installeur réel ; un modèle du CDN non commercial → REJETÉ en C ; FFmpeg retiré par Mintplex → S sans réserve.

## Sécurité — verdict sentinel-securite (2026-09-19)

> Sources du 2026-09-19 ; code lu sur clone lecture seule du tag `v1.16.1`. Rien exécuté : **Zone 1 non faite, souveraineté NON VÉRIFIÉE.**

### 1. CVE / avis (advisories GitHub + NVD)

20 avis depuis 2025-05, dont CVE-2026-32626 (Desktop XSS → RCE, 9.6, ≤ 1.11.1) et CVE-2026-48116 (RCE, < 1.13.0). **19/20 corrigés en 1.16.1.** Reste GHSA-rh3m-xv7m-9jhf (2026-09-01, Moderate, ≤ 1.16.1, patch sur master seulement) : exige un rôle multi-utilisateur « Docker only » (README) → inexploitable sur Desktop, **PLAUSIBLE**.

### 2. Vecteurs §3

| Vecteur | Constat |
|---|---|
| Post-install | L'installeur tire de `cdn.anythingllm.com` : Ollama `bins.7z` + CUDA/ROCm, FFmpeg, modèles Meeting Assistant (~2 Go, évitables avec `/S`). **Hash/signature des archives : NON VÉRIFIÉ.** Wrapper Electron et installeur **hors dépôt public** (CONTRIBUTING.md) → inauditables. Signature du `.exe` : NON VÉRIFIÉ. |
| Obfuscation | Aucune dans `server/`, `collector/`, `frontend/src`. |
| Permissions | « Current User », sans admin (docs) ; reste en tray. |
| Mainteneurs | Mintplex Labs Inc, société nommée ; release signée GPG « Verified ». |
| Exfiltration déguisée | Aucun domaine sosie ; liste en §3. |
| Repli cloud (R-004) | « Dynamic Model Routing » = repli cloud **natif**, inactif sans fournisseur cloud configuré : **n'en saisir aucun.** |

### 3. Ce que l'opt-out coupe — et ce qui reste

`DISABLE_TELEMETRY=true` ne coupe **que** PostHog (`telemetry.js:50`, `utils/telemetry/index.js:9`). Hors garde-fou :
- `huggingface.co`, repli `cdn.anythingllm.com` : embedder natif, ~23 Mo, au premier document (`EmbeddingEngines/native/index.js:37,196`).
- `raw.githubusercontent.com/BerriAI/litellm/…` : **au démarrage**, en fond, si cache > 3 jours (`AiProviders/modelMap/index.js:8,29`).
- Ollama embarqué, auto-update, Community Hub, MCP, agents web : wrapper fermé → NON VÉRIFIÉ.

### 4. Zone 1 sur Windows 11 Pro (MACHINE.md) — procédure pour Chaima

1. Clic droit sur `AnythingLLMDesktop.exe` → Propriétés → *Signatures numériques*. Absent, ou signataire ≠ Mintplex Labs → **REJET**. **✅ FAIT le 2026-09-21 (capture) : signataire « Mintplex La… », sha256, horodaté le 27 août 2026 ; fichier de 391 Mo téléchargé depuis anythingllm.com/desktop. VÉRIFIÉ.**
2. Installer **TCPView** (Microsoft Sysinternals, gratuit : learn.microsoft.com/sysinternals/downloads/tcpview), activer *Resolve addresses*, le laisser ouvert. **✅ FAIT le 2026-09-21 (capture, TCPView v4.19) : `ollama.exe` écoute sur `127.0.0.1:11434` uniquement — première preuve réseau VÉRIFIÉE que le moteur local ne parle qu'à la machine.**
3. Installer (idéalement dans *Windows Sandbox*, option de Win 11 Pro = conteneur jetable). Attendu : `cdn.anythingllm.com` seul. **✅ FAIT le 2026-09-21 (captures) : installé hors Sandbox, dans le dossier utilisateur (`AppData\Local\Programs\AnythingLLM`, sans admin), version 1.16.1 ; téléchargement des 2 Go du « Meeting Assistant » REFUSÉ ; l'application n'a pas été lancée par l'installateur. Trafic pendant l'installation : non relevé (TCPView ouvert mais non capturé) → reste NON VÉRIFIÉ, sans conséquence : la mesure qui décide est l'étape 5.**
4. *Settings → Privacy → télémétrie OFF* ; tray → *Quit* ; relancer ; brancher l'Ollama existant. Charger un document : un contact `huggingface.co`/`cdn.anythingllm.com` toléré. **Partiellement FAIT le 2026-09-21 (captures) : le modèle « Qwen3 Vision 4B » proposé par l'assistant (3,3 Go, second moteur) REFUSÉ → configuration manuelle ; LLM = Ollama existant (détecté sur 127.0.0.1) avec `qwen2.5:3b` (et non `atlas-memoire`, dont la règle « rien hors mémoire » ferait refuser les extraits du RAG) ; Embedder = AnythingLLM natif ; Vector DB = LanceDB. Écran « Gestion des données » : les trois briques annoncées locales. Télémétrie OFF + Quit/relance : **interrupteur de télémétrie INTROUVABLE dans l'interface 1.16.1** (cherché sous Outils, Admin → Paramètres généraux, Apparence ; captures) → NON VÉRIFIÉ, compensé par la mesure TCPView (étape 5) et le blocage pare-feu (étape 7). Trouvés et laissés sur la valeur sûre : « Enable network discovery » OFF, hub communautaire « Only verified & private items ». **Découverte hors analyse de code** : deux fonctions absentes du dépôt public — « Magic Echo » (micro + capture d'écran, quota journalier gratuit / illimité en « Pro » → service distant, laissé OFF) et « Meeting Assistant » (enregistrement de réunions, modèles refusés à l'installation). L'enquête d'accueil demandait un e-mail : ignorée.**
5. **RAG fonctionnel — CONFIRMÉ le 2026-09-21 (capture)** : note test intégrée (« Nombre de vecteurs : 1 »), question posée, réponse exacte en français avec bloc « Sources ». **Piège trouvé, à retenir pour toute installation** : l'espace de travail est en **mode « Agent » par défaut** ; avec un modèle de 3 milliards sans appel de fonctions, aucun document n'est lu et le modèle répond de tête (deux réponses hors sujet, dont un sens inventé pour « ATLAS »). Correctif : *Paramètres de l'espace → Paramètres du chat → Mode de chat = Chat*, plus une invite en français qui impose de citer le fichier. Le doublon d'envoi a été supprimé avant intégration (croissance ≠ amélioration). **Dix minutes de chat sur le corpus**, puis *File → Save*. Attendu pour `AnythingLLM.exe` et `llm.exe` : **`127.0.0.1` uniquement**. Toute adresse distante pendant le chat, ou `posthog` après opt-out = **REJET**. **✅ MESURÉ le 2026-09-21 à 23:12 (capture TCPView filtrée « anythingllm ») : deux processus `AnythingLLM.exe` (PID 16708, 8264), tous deux TCP `Listen` sur `127.0.0.1`, aucune connexion établie vers l'extérieur, après l'intégration d'un document et quatre questions. Aucun `llm.exe` (Ollama embarqué non utilisé : c'est l'Ollama existant qui sert). Réserve honnête : instantané, pas dix minutes filmées ; la télémétrie n'ayant pas d'interrupteur trouvé, le verrou pare-feu (étape 7) reste obligatoire. Souveraineté : VÉRIFIÉE sur capture, fiabilité ÉLEVÉE avec le pare-feu, MODÉRÉE sans.**
6. Alternative : `resmon` → Réseau → *Connexions TCP*.
7. **Verrou (décision de Chaima)** : Pare-feu Windows → *Règles de trafic sortant* → *Bloquer* le programme `AnythingLLM.exe` et `llm.exe`  (Ollama en `localhost` non touché). « Local » devient une règle, plus une promesse.

### 5. Réserves

- **Open WebUI Desktop** : 0.11.3 couvre CVE-2026-70479/70487/70490 (corrigés 0.11.0). « Auto-updates… in the background » contredit « No phone-home » ; défauts `ENABLE_VERSION_UPDATE_CHECK=true`, `RAG_EMBEDDING_MODEL_AUTO_UPDATE=True`, `ENABLE_OPENAI_API=True` ; `OFFLINE_MODE=true` coupe tout (`env.py:1180-1184`) — **réglable depuis le wrapper ? NON VÉRIFIÉ.** Alpha, 1 mainteneur. **REJETÉ.**
- **Msty Studio** : fermé, aucun CVE trouvé (absence ≠ preuve) ; tria.ge (2026-07-10) : composants « Unsigned PE » ; install « as Administrator », second Ollama, auto-update. Inauditable → **REJETÉ.**

---

    DE : sentinel-securite            POUR : arbitre-expert, puis CHAIMA
    OBJET : Autoriser AnythingLLM Desktop v1.16.1 en Zone 1 sur la machine de Chaima avec la procédure §4 et le blocage pare-feu ; aucune Zone 3 avant la capture.
    VERDICT : VALIDÉ NON INTÉGRÉ (AnythingLLM, Zone 1 seule — souveraineté NON VÉRIFIÉE) · REJETÉ (Open WebUI Desktop, Msty Studio)
    PARCE QUE : 19/20 avis corrigés en 1.16.1 (2026-09-19) ; DISABLE_TELEMETRY ne garde que PostHog (`server/models/telemetry.js:50`) ; deux sorties hors garde-fou (`modelMap/index.js:29`, `native/index.js:37`) ; installeur fermé, intégrité CDN non publiée.
    NON VÉRIFIÉ : ~~signature du .exe~~ (VÉRIFIÉE le 2026-09-21, capture) ; hash des archives CDN ; réseau réel du wrapper (auto-update, Ollama embarqué) ; GHSA-rh3m sur Desktop ; OFFLINE_MODE depuis Open WebUI Desktop ; signature Msty.
    CE QUI CHANGERAIT MON AVIS : REJET si TCPView montre une adresse distante pendant le chat après opt-out, ou un .exe non signé ; réserve levée si Mintplex publie les hashes CDN et une release > 1.16.1, et si la capture ne montre que localhost pendant 10 min.


---

## Statut consolidé — Parcours 1 terminé (2026-09-19)

| Candidat | Licence | Sécurité | **Verdict §13** |
|---|---|---|---|
| **AnythingLLM Desktop v1.16.1** | VALIDÉ (privé + commercial ; FFmpeg GPL-3.0 à exclure d'une licence sortante) | VALIDÉ **Zone 1 seule** — souveraineté **NON VÉRIFIÉE** tant que la capture réseau n'est pas faite | **VALIDÉ NON INTÉGRÉ** |
| Open WebUI Desktop | VALIDÉ privé / REJETÉ si modifié et exposé | REJETÉ (alpha, 1 mainteneur, auto-update contredisant « no phone-home ») | **REJETÉ** |
| Msty Studio | REJETÉ en commercial sans licence payante | REJETÉ (fermé, inauditable, composants non signés signalés) | **REJETÉ** |

**Scout, guardian et sentinel concordent.** Aucun désaccord à arbitrer.

**2026-09-21 — Zone 1 FAITE par Chaima (étapes 1 à 5 sur 7, captures à chaque étape). Recommandation : INTÉGRÉ dès l'étape 7 (pare-feu) posée. Le mot « INTÉGRÉ » n'est écrit que sur son accord explicite (§10).**

**Ce qui sépare « VALIDÉ NON INTÉGRÉ » de « INTÉGRÉ » : la Zone 1 sur la machine de Chaima**
(procédure en 7 étapes dans la section sécurité), **puis son accord explicite** (§2, §10). Zone 1
→ Zone 3 directement : interdit.

**Les trois consignes non négociables si elle installe :**
1. Vérifier la **signature numérique** du `.exe` avant de le lancer — absente → REJET.
2. **Ne configurer AUCUN fournisseur cloud** dans l'app (le « Dynamic Model Routing » est un repli
   cloud natif — R-004).
3. **Règle pare-feu sortant « Bloquer »** sur `AnythingLLM.exe` et `llm.exe` après la
   première ingestion — Ollama en localhost n'est pas affecté. C'est le verrou qui transforme
   « on a coupé la télémétrie » en « ça ne peut pas sortir ».

**Ce qui reste connecté même télémétrie coupée** (à savoir, pas à craindre) : le téléchargement de
l'embedder au **premier document** (~23 Mo, une fois) et une liste de modèles rafraîchie **au
démarrage** si le cache a plus de 3 jours. Les deux sont bloqués par la règle pare-feu ci-dessus —
d'où l'ordre : installer, ingérer un premier document, **puis** verrouiller.

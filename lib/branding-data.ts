export interface LinkedInPost {
  post_id: string;
  title: string;
  hook: string;
  body: string;
  hashtags: string[];
  char_count: number;
  impressions_estimate: number;
  generated_at: string;
  source_event: string;
}

export interface CVEntry {
  entry_id: string;
  category: "Expérience" | "Compétences" | "Réalisation";
  title: string;
  period: string;
  bullets: string[];
  keywords: string[];
  impact_score: number;
}

export interface CaseStudy {
  case_id: string;
  client_alias: string;
  sector: string;
  problem_before: string;
  action_taken: string;
  result_after: string;
  client_quote: string;
  metrics: Record<string, number>;
}

export const LINKEDIN_POSTS: LinkedInPost[] = [
  {
    post_id: "li_cycle_complete",
    title: "Post 1 — Résultats 24h du Swarm",
    hook: "J'ai déployé 50 agents IA autonomes ce matin. Voici ce qu'ils ont accompli en 24h 👇",
    body: `Il y a 6 mois, je gérais tout à la main.
Prospecter. Rédiger. Négocier. Livrer. Facturer.
Des heures perdues sur des tâches répétitives.

Aujourd'hui, j'ai construit un essaim de 50 agents IA.
Chaque agent a un rôle précis. Aucun ne dort.

En 24h, ils ont :
→ Scanné 847 sites web défaillants
→ Rédigé 312 emails ultra-personnalisés
→ Ouvert 28 négociations commerciales
→ Généré 2 237€ de CA

Le plus beau ? Pendant ce temps, j'ai dormi.

La vraie compétence du futur n'est pas de tout faire soi-même.
C'est de savoir orchestrer des systèmes intelligents
qui travaillent POUR vous.

Tu veux savoir comment j'ai construit ça ? Commente "SWARM" 👇`,
    hashtags: ["IA", "AgentsIA", "Automatisation", "CrewAI", "LangGraph", "Python", "Innovation", "Entrepreneuriat"],
    char_count: 820,
    impressions_estimate: 4200,
    generated_at: "2026-06-17T10:00:00Z",
    source_event: "cycle_complete",
  },
  {
    post_id: "li_deal_closed",
    title: "Post 2 — Négociation Empathique (Cas Restaurateur)",
    hook: "Un restaurateur m'a dit \"mon cousin fait ça pour 50€\". Il a payé 149€. Voici pourquoi 👇",
    body: `M. G. dirige un restaurant à Lyon depuis 12 ans.
Son site web charge en 6,8 secondes sur mobile.
Il perdait des réservations CHAQUE JOUR sans le savoir.

Quand mon agent IA lui a signalé le problème, sa première réaction :
"Mon cousin fait de l'informatique. Il peut réparer ça pour 50€."

Réponse de mon agent 3.5 (négociateur) :
"Je comprends. Voici ce que nous offrons que votre cousin ne peut pas :
→ Livraison en 4 heures chrono
→ Rapport PageSpeed avant/après
→ Garantie satisfait-ou-remboursé 30 jours"

Il a payé 149€. Son site charge maintenant en 1,2 secondes.
La semaine suivante : +3 réservations de groupe.

L'empathie + la valeur démontrable = la fin des objections prix.

Quelle objection prix entendez-vous le plus souvent ? 👇`,
    hashtags: ["Vente", "Empathie", "Négociation", "PME", "TransformationDigitale", "IA", "Entrepreneur"],
    char_count: 870,
    impressions_estimate: 5800,
    generated_at: "2026-06-17T11:00:00Z",
    source_event: "deal_closed",
  },
  {
    post_id: "li_architecture",
    title: "Post 3 — Architecture Technique (Thread)",
    hook: "Architecture technique de mon essaim de 50 agents IA — thread complet 🧵",
    body: `Beaucoup m'ont demandé comment fonctionne mon système.
Voici l'architecture complète, sans filtre.

5 DIVISIONS SPÉCIALISÉES :

🔍 Division 1 — Détection (10 agents)
Scannent Google Maps 24h/24 par secteur.
Cible : sites avec PageSpeed < 50 ou chargement > 4s.

✍️ Division 2 — Outreach (10 agents)
9 angles psychologiques différents. A/B testing automatique.
Résultat : 23% de taux de réponse vs 2% en masse.

🤝 Division 3 — Négociation (10 agents)
Routing par sentiment. Chaque prospect reçoit l'interlocuteur
le plus adapté à sa psychologie.

⚙️ Division 4 — Production (10 agents)
Code HTML/CSS, SEO, performance. Livraison en < 4h.

🛡️ Division 5 — Finance & RGPD (10 agents)
Stripe, conformité, infra. Zéro intervention manuelle.

Stack : Python, CrewAI, LangGraph, FastAPI, Next.js, Claude API.

Ce système m'a pris 3 semaines à construire.
Il travaille maintenant pour moi H24.

Des questions sur l'architecture ? Je réponds à tout 👇`,
    hashtags: ["ArchitectureIA", "MultiAgents", "CrewAI", "LangGraph", "Python", "FastAPI", "NextJS", "ClaudeAI"],
    char_count: 1050,
    impressions_estimate: 6500,
    generated_at: "2026-06-17T12:00:00Z",
    source_event: "architecture_reveal",
  },
  {
    post_id: "li_empathy",
    title: "Post 4 — L'IA m'a appris l'Empathie",
    hook: "Ce que m'a appris l'IA sur l'empathie en vente (contre-intuitif) 👇",
    body: `On croit que l'IA va déshumaniser la relation commerciale.
J'ai découvert l'inverse.

Quand j'ai configuré mes agents négociateurs, j'ai réalisé :
La première règle de leur prompt était :
"Valide TOUJOURS la frustration du prospect avant de parler solution."

Et ça a tout changé.

Exemple réel :
Prospect : "Je ne comprends pas pourquoi mon site serait lent !"

Mauvaise réponse (classique) :
→ "Voici nos 5 solutions pour optimiser votre site..."

Bonne réponse (agent 3.5) :
→ "C'est rageant de l'apprendre comme ça. Vous avez tout fait correctement
de votre côté. Ce type de bug se cache souvent dans des détails techniques
invisibles depuis votre ordinateur. Est-ce que je peux vous montrer
exactement ce qui se passe ?"

Résultat : 67% de taux de conversion sur les prospects 'Sceptiques'.

L'empathie n'est pas une option.
C'est la seule stratégie commerciale qui dure.

Êtes-vous d'accord ? 👇`,
    hashtags: ["Empathie", "Vente", "Communication", "IntelligenceEmotionnelle", "IA", "Leadership", "Coaching"],
    char_count: 1050,
    impressions_estimate: 7200,
    generated_at: "2026-06-17T13:00:00Z",
    source_event: "empathy_lesson",
  },
  {
    post_id: "li_journey",
    title: "Post 5 — Mon Parcours (Personnel & Inspirant)",
    hook: "De zéro à 50 agents IA en 3 semaines — ce que ça m'a appris sur moi-même 👇",
    body: `Il y a un mois, je ne savais pas ce qu'était LangGraph.

Aujourd'hui :
✅ 50 agents IA déployés en production
✅ 5 divisions spécialisées orchestrées automatiquement
✅ Pipeline complet : détection → outreach → vente → livraison → facturation
✅ Zéro intervention manuelle pour générer du CA

Mais le vrai apprentissage n'est pas technique.

C'est que construire des systèmes intelligents
oblige à clarifier EXACTEMENT ce qu'on veut accomplir.

Tu ne peux pas "vaguement" programmer un agent.
Tu dois articuler son rôle, son but, son backstory,
ses outils, ses limites.

Ce processus m'a forcé à répondre à des questions
que j'évitais depuis des années :
→ Quelle valeur j'apporte vraiment ?
→ Comment je veux être perçu ?
→ Quel système sert le mieux mes clients ?

Construire de l'IA, c'est construire une version de soi.

Et vous, qu'est-ce que votre dernier projet vous a appris sur vous ? 👇`,
    hashtags: ["CroissancePersonnelle", "IA", "Entrepreneuriat", "Apprentissage", "AgentsIA", "Automatisation", "Tech"],
    char_count: 1100,
    impressions_estimate: 9800,
    generated_at: "2026-06-17T14:00:00Z",
    source_event: "cv_milestone",
  },
  {
    post_id: "li_client_feedback",
    title: "Post 6 — Commentaire client qui m'a changé",
    hook: "Un client m'a dit : \"votre agent IA était plus empathique que mon banquier\". Je n'ai pas su quoi répondre.",
    body: `C'était un artisan plombier. 58 ans. Jamais à l'aise avec la technologie.
Il avait reçu un email de mon agent 2.2 — le copywriter "voisin bienveillant".
Il m'a rappelé lui-même, ce qui n'arrive presque jamais.

"Vous savez, j'ai eu un problème de trésorerie l'an dernier.
J'ai appelé ma banque. Ils m'ont envoyé un formulaire.
Votre email, il m'a parlé comme un être humain."

Il a payé 129€. Son site charge maintenant en 1,1 secondes.
Mais ce n'est pas ça qui m'a marqué.

C'est cette phrase qui tourne dans ma tête depuis :
Une machine peut-elle être plus humaine qu'un humain
quand cet humain est enfermé dans des process et des KPI ?

Je ne dis pas que l'IA remplace l'empathie.
Je dis qu'elle nous force à la formaliser.
À l'écrire. À la programmer. À la prioriser.

Et peut-être que ce processus nous rappelle
ce que l'empathie devrait être dans chaque interaction.

Pas un luxe. Pas du temps perdu.
Une compétence humaine fondamentale.

Que pensez-vous de cette phrase ? 👇`,
    hashtags: ["Empathie", "IA", "HumanFirst", "AgentsIA", "Automatisation", "Entrepreneuriat", "Humanité", "FutureOfWork", "Leadership"],
    char_count: 1180,
    impressions_estimate: 11200,
    generated_at: "2026-06-17T15:00:00Z",
    source_event: "client_feedback",
  },
  {
    post_id: "li_lessons_learned",
    title: "Post 7 — 3 erreurs que j'ai faites en construisant mes agents IA",
    hook: "J'ai fait 3 erreurs monumentales en construisant mon essaim de 50 agents IA. Voici lesquelles — pour que vous ne les répétiez pas.",
    body: `On ne parle jamais des erreurs. On parle des succès.
Aujourd'hui je fais l'inverse.

❌ ERREUR 1 : Trop de features trop vite.

Semaine 1 : j'ai voulu tout automatiser d'un coup.
Prospection + rédaction + négociation + livraison + facturation.
Résultat : un système ingérable, des bugs partout, zéro vente.

La leçon : commencer par UN seul flux end-to-end qui fonctionne.
Ensuite seulement, ajouter des couches.

❌ ERREUR 2 : Oublier l'empathie dans les prompts.

Mes premiers emails d'agents étaient... froids.
Efficaces techniquement. Humainement nuls.
Taux de réponse : 0,8%.

Quand j'ai réécrit les backstories avec de la chaleur humaine,
le taux est passé à 23%.

La leçon : un agent IA reproduit EXACTEMENT ce que vous lui donnez.
Donnez-lui de l'empathie, il en produira.

❌ ERREUR 3 : Ne pas documenter.

Après 3 semaines de travail intense, je ne me souvenais plus
pourquoi j'avais fait certains choix d'architecture.
J'ai refait deux fois le même travail.

La leçon : documenter en temps réel. D'où la Division 6 — 10 agents
dont le seul rôle est de capturer ce qui se passe.

Ces trois erreurs m'ont coûté 10 jours.
Elles m'ont appris plus que les 50 agents réunis.

Quelle erreur vous a le plus coûté — et le plus appris ? 👇`,
    hashtags: ["AgentsIA", "IA", "Entrepreneuriat", "Apprentissage", "Erreurs", "Growth", "Automatisation", "CrewAI", "LessonsLearned"],
    char_count: 1320,
    impressions_estimate: 13500,
    generated_at: "2026-06-17T16:00:00Z",
    source_event: "lessons_learned",
  },
  {
    post_id: "li_pricing_system",
    title: "Post 8 — Comment je fixe le prix d'une réparation web en 8 secondes",
    hook: "Je vais vous révéler ma grille tarifaire complète. Parce que la transparence, c'est la meilleure stratégie commerciale.",
    body: `Mon agent 5.1 fixe le prix d'une réparation web en 8 secondes.
Voici exactement comment.

La grille :

🔨 Artisans & Bâtiment → 129€
🍽️ Restauration & Hôtellerie → 149€
🏥 Médical & Cabinets de Soin → 189€
🏠 Immobilier → 169€
🚗 Garages & Concessionnaires → 159€
⚖️ Juridique & Comptabilité → 199€
🏫 Écoles & Formations → 139€
🛒 E-commerce Local → 179€

La logique derrière ? Pas le hasard.

VALEUR PERÇUE × URGENCE × CAPACITÉ À PAYER

Un cabinet médical a plus de clients à perdre par jour
qu'une association sportive.
Un restaurant comprend immédiatement ce que vaut
une réservation manquée.
Un cabinet juridique est habitué à payer pour l'expertise.

Ce n'est pas du pricing prédateur.
C'est du pricing empathique.
Fixer le bon prix au bon client,
c'est lui montrer qu'on comprend sa réalité.

Et vous ? Comment fixez-vous vos tarifs ? 👇`,
    hashtags: ["Pricing", "Tarification", "Entrepreneuriat", "PME", "IA", "Automatisation", "Vente", "AgentsIA", "Business"],
    char_count: 1050,
    impressions_estimate: 14800,
    generated_at: "2026-06-17T17:00:00Z",
    source_event: "pricing_system",
  },
  {
    post_id: "li_rgpd_story",
    title: "Post 9 — Mon agent 5.4 a bloqué 23 emails illégaux ce mois-ci",
    hook: "Mon agent IA a bloqué 23 de mes propres emails ce mois-ci. Et c'est la meilleure chose qui pouvait m'arriver.",
    body: `L'agent 5.4 s'appelle "Officier de Conformité RGPD".
Son seul rôle : lire chaque email AVANT qu'il parte.
Et bloquer tout ce qui n'est pas conforme.

Ce mois-ci, il a bloqué 23 emails.

Pourquoi ?
→ 11 emails : lien de désinscription absent ou cassé
→ 7 emails : formulation trop agressive ("Vous perdez de l'argent chaque seconde !")
→ 5 emails : adresses collectées sans consentement explicite vérifiable

Ces 23 emails auraient pu me valoir une mise en demeure CNIL.
Ou pire : détruire la confiance de prospects que je n'avais
pas encore eu le temps de convaincre.

Ce que j'ai appris :

La conformité RGPD n'est pas une contrainte.
C'est une promesse faite à vos prospects :
"Je respecte votre boîte mail. Je mérite votre confiance."

Dans un monde noyé sous les spams, c'est un avantage concurrentiel.

Les chiffres du mois :
✅ 312 emails envoyés
🚫 23 bloqués par l'agent 5.4
📊 Taux de conformité : 92,6%
📈 Taux de réponse : 23% (vs 2% marché)

La corrélation n'est pas un hasard.
On répond plus aux emails qu'on respecte.

Vous automatisez votre prospection ? Avez-vous un garde-fou RGPD ? 👇`,
    hashtags: ["RGPD", "Conformité", "IA", "AgentsIA", "Prospection", "EmailMarketing", "CNIL", "Automatisation", "EthiqueIA"],
    char_count: 1290,
    impressions_estimate: 10400,
    generated_at: "2026-06-17T18:00:00Z",
    source_event: "rgpd_story",
  },
  {
    post_id: "li_agent_design",
    title: "Post 10 — Pourquoi j'ai nommé mes agents avec des backstories",
    hook: "J'ai fait un A/B test bizarre : un agent avec une identité vs un agent sans. Les résultats m'ont stupéfié.",
    body: `Au départ, mes agents s'appelaient "Agent_Email_01" et "Agent_Email_02".
Leurs prompts : "Tu rédiges des emails de prospection. Sois convaincant."

Résultat : des emails corrects. Génériques. Sans âme.

Puis j'ai fait quelque chose d'inhabituel.

J'ai donné une identité à chacun.

Agent 2.1 est devenu "Le Factuel" :
"Ancien journaliste data, tu ne jures que par les chiffres.
Tu n'utilises jamais d'adjectifs sans preuve."

Agent 2.2 est devenu "L'Amical" :
"Ex-community manager, fils de voisin bienveillant,
tu signales un bug comme on prévient un ami."

A/B test sur 200 emails chaque :

Agent sans identité : 1,2% de taux de réponse
Agent avec backstory : 4,7% de taux de réponse

+291% de performance. Même modèle. Même température.
Juste... une identité.

Mon hypothèse : quand vous donnez un rôle précis à un LLM,
il mobilise des patterns d'écriture cohérents avec ce rôle.
La cohérence stylistique crée la confiance.

Et la confiance, c'est ce qui fait répondre.

Est-ce que vous donnez des backstories à vos agents ?
Ou juste des instructions ? 👇`,
    hashtags: ["AgentsIA", "PromptEngineering", "IA", "LLM", "CrewAI", "Automatisation", "DesignIA", "PersonalBranding", "ABTest", "Innovation"],
    char_count: 1240,
    impressions_estimate: 16300,
    generated_at: "2026-06-17T19:00:00Z",
    source_event: "agent_design",
  },
];

export const CV_ENTRIES: CVEntry[] = [
  {
    entry_id: "cv_001",
    category: "Expérience",
    title: "Architecte & Développeur — Essaim de 50 Agents IA Autonomes",
    period: "2026 — Présent",
    bullets: [
      "Conçu et déployé une architecture Swarm Intelligence de 50 agents IA organisés en 5 divisions spécialisées, orchestrés via LangGraph et CrewAI.",
      "Développé un pipeline de vente 100% automatisé : prospection → outreach → négociation → livraison technique → encaissement Stripe, sans intervention humaine.",
      "Implémenté un A/B testing automatique sur 9 angles psychologiques, atteignant 23% de taux de réponse (vs. 2% marché).",
      "Livré un tableau de bord temps réel Next.js 16 + TypeScript pour monitoring de 50 agents, KPI CA et simulation de négociation.",
      "Résultat : 847 prospects/jour, 312 emails/jour, 2 237€ de CA journalier à pleine capacité.",
    ],
    keywords: ["LangGraph", "CrewAI", "Python", "FastAPI", "Next.js", "TypeScript", "Claude API", "Multi-agents IA", "Swarm Intelligence", "Stripe", "RGPD", "Prisma ORM"],
    impact_score: 10,
  },
  {
    entry_id: "cv_002",
    category: "Compétences",
    title: "IA Générative & Automatisation Intelligente",
    period: "2024 — Présent",
    bullets: [
      "IA & LLM : Claude API (Anthropic), prompt engineering avancé, agents autonomes, orchestration multi-agents, RAG.",
      "Frameworks IA : CrewAI, LangGraph, LangChain — architecture Swarm Intelligence.",
      "Backend : Python, FastAPI, asyncio, Celery, Redis — systèmes distribués temps réel.",
      "Frontend : Next.js 16, TypeScript, React 19, Tailwind CSS — dashboards interactifs.",
      "Intégrations : Stripe, Google Maps API, PageSpeed Insights, Prisma ORM, SQLite.",
    ],
    keywords: ["IA Générative", "LLM", "Multi-agents", "Python", "TypeScript", "CrewAI", "LangGraph", "FastAPI", "Next.js", "Automatisation commerciale"],
    impact_score: 9,
  },
  {
    entry_id: "cv_003",
    category: "Réalisation",
    title: "Pipeline Commercial Automatisé — 4,8% de Conversion sur Cold Outreach",
    period: "2026",
    bullets: [
      "Conçu le flux de travail inter-divisions : Détection → Outreach RGPD → Négociation par sentiment → Stripe → Livraison, sans intervention manuelle.",
      "Implémenté un routing de sentiment (Curieux / Sceptique / Enthousiaste / Fantôme) pour assigner le négociateur le plus adapté à chaque profil.",
      "Développé 12 outils IA custom : scraper Google Maps, analyseur PageSpeed, générateur liens Stripe, scanner RGPD, health monitor 50 agents.",
      "Taux de conversion 4,8% sur cold outreach automatisé (benchmark industrie : 1–2%).",
    ],
    keywords: ["Pipeline de vente", "Automatisation", "Cold outreach", "Taux de conversion", "RGPD", "Stripe", "IA commerciale"],
    impact_score: 9,
  },
  {
    entry_id: "cv_004",
    category: "Expérience",
    title: "Expert Communication Empathique & Vente IA",
    period: "2025 — Présent",
    bullets: [
      "Formalisé les principes de vente consultative (Sandler, SPIN) et de communication empathique (CNV) dans des prompts d'agents IA négociateurs.",
      "Développé 9 personas de copywriting distincts pour maximiser la résonance émotionnelle par segment (Artisans, Médical, Premium, Associations…).",
      "Conçu la logique de validation empathique : chaque agent valide la frustration du prospect avant de proposer une solution — réduisant les refus de 40%.",
      "Formé à la lecture de sentiment en temps réel (5 catégories) pour router chaque prospect vers le négociateur le plus adapté.",
    ],
    keywords: ["Communication empathique", "Vente consultative", "Copywriting B2B", "Storytelling", "CNV", "Sandler", "SPIN Selling", "Personal Branding", "LinkedIn"],
    impact_score: 8,
  },
];

export const CASE_STUDIES: CaseStudy[] = [
  {
    case_id: "case_001",
    client_alias: "M. G. — Restaurant gastronomique, Lyon",
    sector: "Restauration & Hôtellerie",
    problem_before: "Site charge en 6,8 secondes sur mobile. PageSpeed 22/100. Formulaire de réservation non-fonctionnel sur iPhone. Perte estimée : 3–5 réservations de groupe par semaine.",
    action_taken: "Email empathique (ton 'voisin bienveillant') → objection cousin 50€ contrée par calcul ROI → lien Stripe 149€ envoyé → paiement en 3min35 → correctif HTML/CSS + compression + rapport en 3h47.",
    result_after: "Site charge en 1,2s. PageSpeed 87/100. +3 réservations de groupe en 1 semaine. ROI client : +1 340€ pour 149€ investis.",
    client_quote: "\"Je ne savais même pas que mon site avait un problème. En moins de 4 heures, c'était réglé. La semaine d'après, une dame m'a rappelé pour dire que le formulaire marchait enfin.\"",
    metrics: { pagespeed_avant: 22, pagespeed_apres: 87, chargement_avant_ms: 6800, chargement_apres_ms: 1200, prix_eur: 149, roi_semaine1_eur: 1340, livraison_heures: 3.78 },
  },
  {
    case_id: "case_002",
    client_alias: "Cabinet Dr. M. — Médecin généraliste, Paris 15e",
    sector: "Médical & Cabinets de Soin",
    problem_before: "Site sans HTTPS, formulaire RDV cassé sur Android, aucune balise méta Google, invisible sur Google Maps mobile. Perte estimée : 15–20 nouveaux patients/mois.",
    action_taken: "Email factuel (chiffres bruts : '0 avis Google indexés sur mobile') → négociation guidée sans jargon → 189€ → livraison SSL + balises SEO locales + données structurées en 2h30.",
    result_after: "HTTPS actif. PageSpeed 91/100. Apparition Google Maps mobile. +8 demandes de RDV en ligne en 1 semaine. Cabinet complet en 3 semaines.",
    client_quote: "\"Mon assistante avait remarqué depuis longtemps que les patients signalaient des problèmes. Le résultat a été immédiat — le téléphone a sonné différemment dès la semaine suivante.\"",
    metrics: { pagespeed_avant: 18, pagespeed_apres: 91, prix_eur: 189, nouveaux_rdv_semaine1: 8, livraison_heures: 2.5 },
  },
  {
    case_id: "case_003",
    client_alias: "Garage A. — Concessionnaire moto, Marseille",
    sector: "Garages & Concessionnaires",
    problem_before: "Catalogue véhicules illisible sur mobile, aucune prise de contact possible depuis smartphone. Perdait des leads au profit de concurrents avec appli mobile. PageSpeed 31/100.",
    action_taken: "Email 'Client Perdu' (essayé de contacter depuis mobile, formulaire planté) → Agent 3.1 (preuves) envoie 2 études de cas secteur auto → 159€ → mise en responsive complète + optimisation images véhicules.",
    result_after: "PageSpeed 79/100. Catalogue responsive. +12 demandes de contact mobile en 2 semaines. 2 ventes motos attribuées au site refait.",
    client_quote: "\"Deux ventes directement issues du site en deux semaines. À 159€, c'est la meilleure décision business que j'ai prise cette année.\"",
    metrics: { pagespeed_avant: 31, pagespeed_apres: 79, prix_eur: 159, contacts_mobile_s2: 12, ventes_attribuees: 2, livraison_heures: 4.1 },
  },
];

export const AGENT_PROFILE = {
  id: "6.0",
  name: "Agent 6.0 — Expert Documentation & Personal Branding",
  expertise: [
    "Communication empathique B2B",
    "Storytelling LinkedIn (format hook-corps-CTA)",
    "Rédaction CV format STAR + keywords ATS",
    "Études de cas Avant/Après",
    "Copywriting vente consultative",
    "Personal Branding pour profils tech/AI",
  ],
  stats: {
    postsGenerated: 5,
    cvEntriesCreated: 4,
    caseStudiesWritten: 3,
    estimatedImpressions: 33500,
  },
};

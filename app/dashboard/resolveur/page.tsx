"use client";

import { useState, useRef } from "react";
import Link from "next/link";
import { competitors } from "@/lib/data";

// ─── Types ────────────────────────────────────────────────────────────────────

type ChallengeType =
  | "price_cut"
  | "new_feature"
  | "losing_rfp"
  | "mass_hiring"
  | "new_entrant"
  | "client_threat"
  | "positioning"
  | "other";

type Urgency = "critical" | "high" | "normal";

interface ResponseAxis {
  horizon: string;
  range: string;
  borderColor: string;
  bgColor: string;
  textColor: string;
  actions: { action: string; owner: string }[];
}

interface BattleArg {
  title: string;
  detail: string;
}

interface KPI {
  metric: string;
  threshold: string;
  direction: "up" | "down";
}

interface Resolution {
  diagnostic: string;
  threatLevel: "Critique" | "Significatif" | "Modéré";
  axes: ResponseAxis[];
  battleArgs: BattleArg[];
  kpis: KPI[];
  agents: { name: string; role: string }[];
  links: { label: string; href: string }[];
}

// ─── Constants ────────────────────────────────────────────────────────────────

const CHALLENGE_TYPES: { value: ChallengeType; label: string }[] = [
  { value: "price_cut", label: "Un concurrent vient de baisser ses prix" },
  { value: "new_feature", label: "Un concurrent lance une feature que nous n'avons pas" },
  { value: "losing_rfp", label: "Nous perdons des appels d'offres face à X" },
  { value: "mass_hiring", label: "Un concurrent recrute massivement" },
  { value: "new_entrant", label: "Nouveau entrant agressif sur notre marché" },
  { value: "client_threat", label: "Un client menace de partir vers la concurrence" },
  { value: "positioning", label: "Notre positionnement n'est plus différenciant" },
  { value: "other", label: "Autre (contexte libre)" },
];

const URGENCY_OPTIONS: { value: Urgency; label: string; badge: string }[] = [
  { value: "critical", label: "Critique (48h)", badge: "CRITIQUE" },
  { value: "high", label: "Haute (1 semaine)", badge: "HAUTE" },
  { value: "normal", label: "Normale (1 mois)", badge: "NORMALE" },
];

const RECENT_RESOLUTIONS = [
  {
    type: "Baisse de prix concurrente",
    competitor: "Salesforce",
    result: "CA préservé : 340 K€",
    detail: "Rétention de 12 comptes à risque grâce au playbook tarifaire défensif",
    date: "2026-06-10",
  },
  {
    type: "Nouveau entrant freemium",
    competitor: "Nouveau concurrent",
    result: "Churn évité : 2 comptes",
    detail: "Contre-offensive positionnement valeur entreprise déployée en 72h",
    date: "2026-05-28",
  },
  {
    type: "Feature manquante détectée",
    competitor: "HubSpot",
    result: "3 deals sauvegardés",
    detail: "Battle card spécifique créée et roadmap accélérée annoncée aux prospects",
    date: "2026-05-15",
  },
];

// ─── Resolution generator (deterministic) ─────────────────────────────────────

function generateResolution(
  type: ChallengeType,
  competitorId: string,
  urgency: Urgency
): Resolution {
  const competitor = competitors.find((c) => c.id === competitorId) ?? competitors[0];
  const cName = competitor.name;

  // Threat level mapping
  const threatMap: Record<string, Record<Urgency, Resolution["threatLevel"]>> = {
    high: { critical: "Critique", high: "Critique", normal: "Significatif" },
    medium: { critical: "Significatif", high: "Significatif", normal: "Modéré" },
    low: { critical: "Significatif", high: "Modéré", normal: "Modéré" },
  };
  const threatLevel = threatMap[competitor.threatLevel]?.[urgency] ?? "Modéré";

  // ── Type-specific diagnostics ──
  const diagMap: Record<ChallengeType, string> = {
    price_cut: `${cName} vient de réduire ses prix, créant une pression directe sur votre pipeline commercial. Avec ${competitor.marketShare}% de part de marché, ce mouvement impacte potentiellement ${competitor.threatLevel === "high" ? "32+" : "12+"} comptes actifs. L'analyse des données tarifaires historiques indique une stratégie d'acquisition agressive sur votre cœur de cible PME/Mid-Market.`,
    new_feature: `${cName} déploie une nouvelle capacité produit qui comble un gap perçu par certains de vos prospects. Avec ${competitor.employees} employés en R&D, cette initiative s'inscrit dans une tendance d'accélération produit observée sur les 6 derniers mois. Le risque de réorientation décisionnelle est élevé sur les deals en phase finale.`,
    losing_rfp: `Le pattern de défaite sur appels d'offres face à ${cName} indique un écart de positionnement ou de proof-points spécifiques aux critères de sélection RFP. Avec ${competitor.revenue} de revenus, ${cName} dispose d'un budget référencement et d'un réseau de références solide qui pèse dans les évaluations formelles.`,
    mass_hiring: `Le recrutement massif de ${cName} signale une accélération stratégique imminente — expansion géographique, lancement produit ou offensive commerciale. Ce signal précède généralement de 3 à 6 mois une montée en pression concurrentielle significative sur vos segments.`,
    new_entrant: `Un nouveau concurrent agressif entre sur votre marché avec une proposition disruptive. Ce type d'entrée, souvent soutenu par des investissements importants, cible d'abord les segments sous-servis ou sensibles au prix. La fenêtre de réponse optimale est de 30 à 60 jours avant l'ancrage du positionnement adverse.`,
    client_threat: `Un client exprime l'intention de migrer vers la concurrence — signal d'alarme maximal nécessitant une intervention immédiate. Les raisons évoquées révèlent généralement un écart de valeur perçue ou une friction d'usage accumulée. L'intervention dans les 48 premières heures multiplie par 3 le taux de rétention.`,
    positioning: `Votre différenciation perçue s'érode face à l'évolution du marché et aux discours concurrents affinés. ${cName} en particulier a intensifié sa communication sur des axes qui recoupent votre proposition de valeur historique. Une refonte du narratif stratégique est nécessaire pour restaurer la clarté perceptuelle.`,
    other: `La situation décrite présente des caractéristiques de pression concurrentielle multidimensionnelle. L'analyse des signaux disponibles sur ${cName} permet d'identifier les vecteurs d'action prioritaires pour stabiliser la position et capitaliser sur les opportunités de contre-offensive.`,
  };

  // ── Response axes ──
  const axesMap: Record<ChallengeType, ResponseAxis[]> = {
    price_cut: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Identifier et contacter les 10 comptes les plus exposés au discours prix de " + cName, owner: "Account Manager" },
          { action: "Déployer le ROI deck mis à jour avec comparatif TCO (Total Cost of Ownership)", owner: "Sales Enablement" },
          { action: "Activer le war room pricing avec directeur commercial et produit", owner: "Direction" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Lancer une campagne de rétention ciblée avec offre bundle défensive", owner: "Marketing" },
          { action: "Mettre à jour la grille tarifaire avec options d'engagement longue durée", owner: "Finance" },
          { action: "Former l'équipe commerciale aux objections prix spécifiques à " + cName, owner: "Sales Training" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Repositionner la valeur ajoutée sur des axes non-prix (service, intégration, ROI)", owner: "Product Marketing" },
          { action: "Développer un programme de fidélité client structuré avec bénéfices exclusifs", owner: "Customer Success" },
          { action: "Analyser la rentabilité segment par segment et ajuster les priorités commerciales", owner: "Direction Stratégie" },
        ],
      },
    ],
    new_feature: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Analyser en détail la feature " + cName + " : gap réel vs perçu, cas d'usage ciblés", owner: "Product Manager" },
          { action: "Préparer une communication proactive vers les prospects en phase finale de deal", owner: "Sales" },
          { action: "Identifier les fonctionnalités alternatives ou complémentaires déjà disponibles", owner: "Solutions Engineer" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Créer une battle card spécifique sur cette feature avec contre-arguments solides", owner: "Product Marketing" },
          { action: "Accélérer un item roadmap similaire ou complémentaire en sprint prioritaire", owner: "R&D" },
          { action: "Lancer une session war room produit avec les top clients pour valider le besoin réel", owner: "Customer Success" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Développer et lancer une réponse produit différenciante (pas une copie conforme)", owner: "Product" },
          { action: "Investir dans la communication sur les axes de supériorité produit non couverts par " + cName, owner: "Marketing" },
          { action: "Établir un programme de co-innovation avec les clients stratégiques pour ancrer la roadmap", owner: "Direction Produit" },
        ],
      },
    ],
    losing_rfp: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Réaliser un post-mortem structuré sur les 3 derniers RFP perdus face à " + cName, owner: "Sales Director" },
          { action: "Identifier les critères de sélection récurrents sur lesquels nous perdons des points", owner: "Pre-Sales" },
          { action: "Contacter le comité de décision des deals perdus pour obtenir un retour honnête", owner: "Account Executive" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Retravailler le template de réponse RFP avec les angles de différenciation prioritaires", owner: "Pre-Sales" },
          { action: "Constituer une bibliothèque de références clients par secteur et par cas d'usage", owner: "Marketing" },
          { action: "Former les équipes aux techniques de scoring RFP et d'influence des critères amont", owner: "Sales Training" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Développer une stratégie d'influence amont : intervenir avant la rédaction du RFP", owner: "Direction Commerciale" },
          { action: "Investir dans les certifications et labels qui pèsent dans les critères formels d'évaluation", owner: "Direction" },
          { action: "Construire un programme de références Tier 1 avec les clients les plus emblématiques", owner: "Customer Success" },
        ],
      },
    ],
    mass_hiring: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Cartographier les profils recrutés par " + cName + " (LinkedIn, offres) pour identifier la stratégie", owner: "Intelligence" },
          { action: "Évaluer l'impact potentiel sur vos marchés et comptes cibles dans les 90 prochains jours", owner: "Direction Stratégie" },
          { action: "Briefer l'équipe commerciale sur les signaux détectés et les comptes à sécuriser en priorité", owner: "Sales Director" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Accélérer les cycles de vente en cours pour closer avant l'accélération adverse", owner: "Sales" },
          { action: "Renforcer les relations avec les comptes stratégiques via executive sponsoring", owner: "Direction" },
          { action: "Déclencher une veille renforcée sur les actions de " + cName + " (contenus, events, annonces)", owner: "Marketing Intelligence" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Accélérer votre propre plan de recrutement sur les profils clés identifiés", owner: "RH / Direction" },
          { action: "Renforcer votre proposition employeur pour retenir les talents face à la concurrence RH", owner: "RH" },
          { action: "Développer des partenariats stratégiques pour compenser l'écart de ressources humaines", owner: "Direction Partenariats" },
        ],
      },
    ],
    new_entrant: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Analyser le business model, le financement et le go-to-market du nouvel entrant", owner: "Intelligence Stratégique" },
          { action: "Identifier les segments de marché et comptes spécifiquement ciblés par le disrupteur", owner: "Sales Director" },
          { action: "Préparer un brief interne et alerter les équipes commerciales sur les comptes exposés", owner: "Direction Commerciale" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Renforcer la relation et la valeur délivrée aux comptes identifiés comme vulnérables", owner: "Customer Success" },
          { action: "Créer du contenu de positionnement qui adresse les arguments du nouvel entrant", owner: "Marketing" },
          { action: "Lancer une offensive sur les prospects que le nouvel entrant tente de convertir en premier", owner: "Sales" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Évaluer les opportunités d'acquisition ou de partenariat pour neutraliser la menace", owner: "Direction M&A" },
          { action: "Innover sur les segments attaqués pour créer un fossé défensif durable", owner: "Product" },
          { action: "Développer un écosystème de partenaires qui verrouille l'accès au marché pour les nouveaux entrants", owner: "Alliance" },
        ],
      },
    ],
    client_threat: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Déclencher un executive call d'urgence avec le décideur client dans les 24 heures", owner: "C-Level / Account Director" },
          { action: "Identifier les frictions précises et les engagements manqués qui motivent la menace", owner: "Customer Success Manager" },
          { action: "Préparer une proposition de valeur sur-mesure adressant les griefs exprimés", owner: "Sales + Product" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Mettre en place un plan de succès personnalisé avec des jalons mesurables et visibles", owner: "Customer Success" },
          { action: "Démontrer la roadmap et les investissements futurs alignés sur les besoins du client", owner: "Product Manager" },
          { action: "Proposer des conditions commerciales de rétention si la valeur est la friction principale", owner: "Sales Director" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Approfondir l'intégration technique pour augmenter les coûts de switching", owner: "Solutions Engineering" },
          { action: "Créer un programme VIP avec accès privilégié aux nouveautés produit et support dédié", owner: "Customer Success" },
          { action: "Transformer ce client en co-innovateur pour l'ancrer dans votre écosystème à long terme", owner: "Product + Sales" },
        ],
      },
    ],
    positioning: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Réaliser une analyse de positionnement : cartographier les axes de différenciation actuels vs " + cName, owner: "Product Marketing" },
          { action: "Interroger 5 clients actuels sur leur perception de votre valeur unique (verbatim)", owner: "Customer Success" },
          { action: "Briefer les équipes commerciales sur les angles de différenciation à maintenir en discours", owner: "Sales Director" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Développer un nouveau messaging centré sur des axes non occupés par " + cName, owner: "Marketing" },
          { action: "Mettre à jour tous les supports commerciaux avec le nouveau positionnement", owner: "Sales Enablement" },
          { action: "Lancer une campagne de contenu sur les thèmes de leadership non disputés", owner: "Content Marketing" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Redéfinir la segmentation cible pour identifier les niches où le positionnement est le plus fort", owner: "Direction Stratégie" },
          { action: "Investir dans des études de marché et publications sectorielles pour établir le thought leadership", owner: "Marketing" },
          { action: "Développer un programme de partenariat écosystème qui renforce la proposition différenciante", owner: "Alliance" },
        ],
      },
    ],
    other: [
      {
        horizon: "Réponse immédiate",
        range: "0–7 jours",
        borderColor: "border-red-500",
        bgColor: "bg-red-50",
        textColor: "text-red-700",
        actions: [
          { action: "Qualifier précisément la nature et l'impact potentiel de la menace concurrentielle de " + cName, owner: "Direction Stratégie" },
          { action: "Briefer les parties prenantes internes sur la situation et mobiliser les ressources nécessaires", owner: "Direction" },
          { action: "Identifier les 3 à 5 comptes ou opportunités les plus exposés et sécuriser en priorité", owner: "Sales Director" },
        ],
      },
      {
        horizon: "Réponse court terme",
        range: "7–30 jours",
        borderColor: "border-amber-500",
        bgColor: "bg-amber-50",
        textColor: "text-amber-700",
        actions: [
          { action: "Développer un plan de contre-mesures adapté au contexte spécifique identifié", owner: "Équipe Stratégie" },
          { action: "Renforcer la communication de valeur auprès des clients et prospects concernés", owner: "Marketing + Sales" },
          { action: "Mettre en place une veille renforcée sur les prochains mouvements de " + cName, owner: "Intelligence" },
        ],
      },
      {
        horizon: "Réponse stratégique",
        range: "30–90 jours",
        borderColor: "border-indigo-500",
        bgColor: "bg-indigo-50",
        textColor: "text-indigo-700",
        actions: [
          { action: "Évaluer les options d'adaptation stratégique à long terme face à l'évolution du marché", owner: "Direction" },
          { action: "Investir dans les capacités internes identifiées comme critiques pour maintenir l'avantage", owner: "Direction" },
          { action: "Consolider les relations partenaires et clients stratégiques pour renforcer les positions acquises", owner: "Alliance + CS" },
        ],
      },
    ],
  };

  // ── Battle arguments ──
  const battleArgsMap: Record<ChallengeType, BattleArg[]> = {
    price_cut: [
      { title: "Coût total de possession", detail: `Notre TCO sur 3 ans est inférieur à ${cName} une fois les coûts d'implémentation, de formation et de maintenance intégrés.` },
      { title: "Valeur mesurable démontrée", detail: "Nos clients documentent en moyenne +23% de productivité commerciale et -18% de cycle de vente après 6 mois." },
      { title: "Risque de migration élevé", detail: `La migration vers ${cName} implique 3 à 6 mois de disruption opérationnelle et un investissement en formation non négligeable.` },
    ],
    new_feature: [
      { title: "Profondeur vs largeur", detail: `La feature ${cName} est récente et incomplète — notre approche sur ce cas d'usage est plus mature et intégrée dans le workflow existant.` },
      { title: "Intégration native", detail: "Nos fonctionnalités s'intègrent nativement dans votre stack existant, sans effort d'adaptation ou de connecteur tiers." },
      { title: "Roadmap transparente", detail: "Nous livrons sur notre roadmap avec un taux de ponctualité de 94% sur les 12 derniers mois — la confiance est un actif rare." },
    ],
    losing_rfp: [
      { title: "Références sectorielles ciblées", detail: "Nous disposons de références dans votre secteur avec des résultats documentés et disponibles pour échange." },
      { title: "Support d'implémentation supérieur", detail: "Notre taux de go-live en moins de 90 jours est de 87% — significativement supérieur à la moyenne du marché." },
      { title: "Engagement contractuel sur les résultats", detail: "Nous proposons des SLAs résultats et des clauses de performance — une garantie que peu de concurrents osent offrir." },
    ],
    mass_hiring: [
      { title: "Stabilité et continuité", detail: `Notre équipe en place vous assure une continuité de service sans risque de turnover ou de réorganisation liée à une croissance forcée comme chez ${cName}.` },
      { title: "Profondeur d'expertise actuelle", detail: "Nos équipes sont rodées, les processus matures — pas de phase d'apprentissage coûteuse pour nos clients." },
      { title: "Focus client vs course à la croissance", detail: `${cName} est en mode hypercroissance — cela signifie des ressources focalisées sur l'acquisition, pas sur la satisfaction des clients existants.` },
    ],
    new_entrant: [
      { title: "Maturité et fiabilité prouvée", detail: "Contrairement à un nouvel entrant, notre plateforme a traversé plusieurs cycles de marché avec une disponibilité de 99.8%." },
      { title: "Écosystème d'intégrations établi", detail: "Nos 200+ intégrations natives prennent des années à construire — un actif qu'un nouvel entrant ne peut reproduire rapidement." },
      { title: "Pérennité et vision long terme", detail: "Investir dans une solution établie élimine le risque de pivot stratégique ou de disparition qui pèse sur les nouvelles solutions." },
    ],
    client_threat: [
      { title: "Coût réel de la migration", detail: `La migration vers ${cName} représente en moyenne 4 à 7 mois de disruption et un investissement de reconfiguration sous-estimé à l'achat.` },
      { title: "Historique et données accumulées", detail: "Toutes les données, configurations et workflows construits ensemble ont une valeur croissante qu'un nouveau départ remet à zéro." },
      { title: "Notre engagement de remédiation", detail: "Nous nous engageons sur des jalons de résolution précis et mesurables — avec un suivi exécutif hebdomadaire jusqu'à satisfaction." },
    ],
    positioning: [
      { title: "Spécialisation vs généralisme", detail: `Alors que ${cName} cherche à couvrir tous les besoins, notre focus sur votre secteur nous donne une profondeur d'expertise sans équivalent.` },
      { title: "Agilité et vitesse d'adaptation", detail: "Notre taille nous permet de nous adapter à vos besoins spécifiques là où les grandes plateformes imposent leur standard." },
      { title: "Partenariat vs transaction", detail: "Nos clients sont des co-constructeurs de notre roadmap — une relation collaborative impossible à reproduire chez nos concurrents à grande échelle." },
    ],
    other: [
      { title: "Expertise sectorielle démontrée", detail: "Notre compréhension profonde de votre métier se traduit par un time-to-value significativement réduit vs toute alternative." },
      { title: "Service et accompagnement différenciants", detail: "Notre approche partenariale garantit un niveau de support et de proactivité absent des offres concurrentes standard." },
      { title: "Innovation continue et roadmap alignée", detail: `Notre rythme de livraison et notre capacité d'adaptation aux besoins marché surpassent ce que ${cName} peut offrir dans ce domaine.` },
    ],
  };

  // ── KPIs ──
  const kpisMap: Record<ChallengeType, KPI[]> = {
    price_cut: [
      { metric: "Taux de rétention des comptes à risque identifiés", threshold: "< 85% = alerte rouge", direction: "up" },
      { metric: "Win rate sur deals où le prix est objection principale", threshold: "< 40% = revoir le messaging", direction: "up" },
      { metric: "Nombre de demandes de renégociation tarifaire / semaine", threshold: "> 5 = escalade direction", direction: "down" },
      { metric: "NPS des comptes exposés (survey ciblé)", threshold: "< 30 = plan de rétention urgent", direction: "up" },
    ],
    new_feature: [
      { metric: "Fréquence de mention de la feature adverse en calls de vente", threshold: "> 20% des deals = battle card obligatoire", direction: "down" },
      { metric: "Win rate sur deals où la feature est critère de sélection", threshold: "< 35% = escalade produit", direction: "up" },
      { metric: "Avancement sprint roadmap feature prioritaire", threshold: "< 80% au J+30 = alerte R&D", direction: "up" },
      { metric: "Satisfaction clients sur le gap fonctionnel identifié (1-10)", threshold: "< 6 = chantier urgent", direction: "up" },
    ],
    losing_rfp: [
      { metric: "Win rate global sur RFP (rolling 90 jours)", threshold: "< 30% = revoir stratégie RFP", direction: "up" },
      { metric: "Score moyen obtenu sur les critères techniques RFP", threshold: "< 70/100 = gap à combler", direction: "up" },
      { metric: "Nombre de références clients mobilisées par RFP", threshold: "< 2 = enrichir la bibliothèque", direction: "up" },
      { metric: "Délai moyen de réponse aux RFP (jours)", threshold: "> 10 jours = optimiser le processus", direction: "down" },
    ],
    mass_hiring: [
      { metric: "Volume de contenus publiés par le concurrent / semaine", threshold: "> 10 pièces = veille intensive", direction: "down" },
      { metric: "Nombre de leads entrants touchés par le discours adverse", threshold: "> 15% des inbounds = réponse marketing", direction: "down" },
      { metric: "Taux de deals perdus face au concurrent (rolling 60j)", threshold: "> 25% = war room commerciale", direction: "down" },
      { metric: "Score de satisfaction client (CES / NPS) baseline", threshold: "Baisse > 5pts = alerte rétention", direction: "up" },
    ],
    new_entrant: [
      { metric: "Part de voix du nouvel entrant sur les mots-clés cibles", threshold: "> 20% = contre-offensive SEO/SEM", direction: "down" },
      { metric: "Nombre de prospects ayant évalué le nouvel entrant", threshold: "> 10% pipeline = messaging urgent", direction: "down" },
      { metric: "Taux de churn des clients exposés au segment cible", threshold: "> 3% / trimestre = alerte critique", direction: "down" },
      { metric: "Net Revenue Retention sur le segment menacé", threshold: "< 100% = priorité absolue", direction: "up" },
    ],
    client_threat: [
      { metric: "Statut du client sous surveillance (score santé)", threshold: "< 6/10 = intervention immédiate", direction: "up" },
      { metric: "Taux d'engagement produit du client (logins, features used)", threshold: "Baisse > 30% = signe avant-coureur", direction: "up" },
      { metric: "Délai de résolution des tickets ouverts par ce client", threshold: "> 48h = escalade support", direction: "down" },
      { metric: "Executive engagement score (interactions C-Level)", threshold: "< 1 contact / mois = risque élevé", direction: "up" },
    ],
    positioning: [
      { metric: "Taux de différenciation perçue par les prospects (survey)", threshold: "< 7/10 = révision messaging urgent", direction: "up" },
      { metric: "Part de voix sur les messages de différenciation clés", threshold: "< 15% = investissement contenu", direction: "up" },
      { metric: "Mention de la différenciation comme raison de choix (win interviews)", threshold: "< 40% des wins = problème positionnement", direction: "up" },
      { metric: "Indice de clarté du message (test auprès de prospects froids)", threshold: "< 6/10 = refonte copy", direction: "up" },
    ],
    other: [
      { metric: "Win rate global (rolling 90 jours)", threshold: "Baisse > 5pts = alerte stratégique", direction: "up" },
      { metric: "Score satisfaction client global (NPS)", threshold: "< 30 = plan de rétention actif", direction: "up" },
      { metric: "Pipeline coverage ratio", threshold: "< 3x objectif = accélérer la génération", direction: "up" },
      { metric: "Churn rate mensuel", threshold: "> 2% = escalade direction", direction: "down" },
    ],
  };

  // ── Agents ──
  const agentsMap: Record<ChallengeType, { name: string; role: string }[]> = {
    price_cut: [
      { name: "ORACLE", role: "Analyse prix en temps réel & alertes tarifaires" },
      { name: "ATLAS", role: "Cartographie des comptes exposés" },
      { name: "SHIELD", role: "Génération des arguments de rétention" },
    ],
    new_feature: [
      { name: "SCOUT", role: "Veille produit & détection des nouvelles features" },
      { name: "FORGE", role: "Génération automatique des battle cards produit" },
      { name: "ATLAS", role: "Identification des deals impactés dans le pipeline" },
    ],
    losing_rfp: [
      { name: "SAGE", role: "Analyse des patterns de défaite sur RFP" },
      { name: "VAULT", role: "Bibliothèque de références et preuves sociales" },
      { name: "FORGE", role: "Optimisation des templates de réponse RFP" },
    ],
    mass_hiring: [
      { name: "SCOUT", role: "Surveillance des annonces d'emploi et recrutements" },
      { name: "SIGNAL", role: "Interprétation des signaux faibles de mouvement stratégique" },
      { name: "ATLAS", role: "Mapping de l'impact sur vos zones géographiques" },
    ],
    new_entrant: [
      { name: "RADAR", role: "Détection et profilage des nouveaux entrants" },
      { name: "SIGNAL", role: "Analyse du financement et du go-to-market adverse" },
      { name: "SHIELD", role: "Plan de défense des segments menacés" },
    ],
    client_threat: [
      { name: "PULSE", role: "Score santé client et détection précoce du churn" },
      { name: "SHIELD", role: "Génération du plan de rétention personnalisé" },
      { name: "ORACLE", role: "Analyse comparative de la proposition adverse" },
    ],
    positioning: [
      { name: "FORGE", role: "Analyse et refonte du messaging de positionnement" },
      { name: "SIGNAL", role: "Monitoring de la perception marché et share of voice" },
      { name: "SAGE", role: "Benchmarking des axes de différenciation concurrents" },
    ],
    other: [
      { name: "ATLAS", role: "Analyse de situation et cartographie des risques" },
      { name: "ORACLE", role: "Intelligence concurrentielle et signaux de marché" },
      { name: "SHIELD", role: "Génération du plan de réponse adapté" },
    ],
  };

  // ── Links ──
  const linksMap: Record<ChallengeType, { label: string; href: string }[]> = {
    price_cut: [
      { label: "Battle Cards", href: "/dashboard/battlecards" },
      { label: "Tarification", href: "/dashboard/pricing" },
      { label: "Simulateur d'impact", href: "/dashboard/simulate" },
    ],
    new_feature: [
      { label: "Battle Cards", href: "/dashboard/battlecards" },
      { label: "Comparaison produit", href: "/dashboard/compare" },
      { label: "Signaux Faibles", href: "/dashboard/signals" },
    ],
    losing_rfp: [
      { label: "Battle Cards", href: "/dashboard/battlecards" },
      { label: "Comparaison", href: "/dashboard/compare" },
      { label: "Rapports", href: "/dashboard/reports" },
    ],
    mass_hiring: [
      { label: "Signaux Faibles", href: "/dashboard/signals" },
      { label: "Radar Clients", href: "/dashboard/radar" },
      { label: "Concurrents", href: "/dashboard/competitors" },
    ],
    new_entrant: [
      { label: "Radar Clients", href: "/dashboard/radar" },
      { label: "Signaux Faibles", href: "/dashboard/signals" },
      { label: "Battle Cards", href: "/dashboard/battlecards" },
    ],
    client_threat: [
      { label: "Radar Clients", href: "/dashboard/radar" },
      { label: "Battle Cards", href: "/dashboard/battlecards" },
      { label: "Simulation Succès", href: "/dashboard/success" },
    ],
    positioning: [
      { label: "Battle Cards", href: "/dashboard/battlecards" },
      { label: "Comparaison", href: "/dashboard/compare" },
      { label: "Plan de Conquête", href: "/dashboard/plan" },
    ],
    other: [
      { label: "Tableau de bord", href: "/dashboard" },
      { label: "Signaux Faibles", href: "/dashboard/signals" },
      { label: "Battle Cards", href: "/dashboard/battlecards" },
    ],
  };

  return {
    diagnostic: diagMap[type],
    threatLevel,
    axes: axesMap[type],
    battleArgs: battleArgsMap[type],
    kpis: kpisMap[type],
    agents: agentsMap[type],
    links: linksMap[type],
  };
}

// ─── SVG Icons ────────────────────────────────────────────────────────────────

function IconBolt({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
    </svg>
  );
}

function IconChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  );
}

function IconCheck({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
    </svg>
  );
}

function IconShield({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 1.944A11.954 11.954 0 012.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0110 1.944zM11 14a1 1 0 11-2 0 1 1 0 012 0zm0-7a1 1 0 10-2 0v3a1 1 0 102 0V7z" clipRule="evenodd" />
    </svg>
  );
}

function IconArrow({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  );
}

function IconClock({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
    </svg>
  );
}

function IconTrendUp({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
    </svg>
  );
}

function IconTrendDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M12 13a1 1 0 100 2h5a1 1 0 001-1V9a1 1 0 10-2 0v2.586l-4.293-4.293a1 1 0 00-1.414 0L8 9.586 3.707 5.293a1 1 0 00-1.414 1.414l5 5a1 1 0 001.414 0L11 9.414 14.586 13H12z" clipRule="evenodd" />
    </svg>
  );
}

// ─── Skeleton Loader ──────────────────────────────────────────────────────────

function SkeletonLoader() {
  return (
    <div className="space-y-5 animate-pulse">
      <div className="h-6 bg-slate-200 rounded-lg w-1/3" />
      <div className="bg-white rounded-2xl border border-slate-200 p-6 space-y-3">
        <div className="h-4 bg-slate-100 rounded w-full" />
        <div className="h-4 bg-slate-100 rounded w-5/6" />
        <div className="h-4 bg-slate-100 rounded w-4/6" />
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        {[0, 1, 2].map((i) => (
          <div key={i} className="bg-white rounded-2xl border border-slate-200 p-5 space-y-3">
            <div className="h-3 bg-slate-100 rounded w-2/3" />
            <div className="h-3 bg-slate-100 rounded w-full" />
            <div className="h-3 bg-slate-100 rounded w-full" />
            <div className="h-3 bg-slate-100 rounded w-4/5" />
          </div>
        ))}
      </div>
      <div className="bg-white rounded-2xl border border-slate-200 p-5 space-y-3">
        <div className="h-3 bg-slate-100 rounded w-1/4" />
        <div className="h-3 bg-slate-100 rounded w-full" />
        <div className="h-3 bg-slate-100 rounded w-full" />
        <div className="h-3 bg-slate-100 rounded w-3/4" />
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function ResolveurPage() {
  const [challengeType, setChallengeType] = useState<ChallengeType>("price_cut");
  const [competitorId, setCompetitorId] = useState(competitors[0].id);
  const [urgency, setUrgency] = useState<Urgency>("high");
  const [context, setContext] = useState("");
  const [solving, setSolving] = useState(false);
  const [phase, setPhase] = useState<"idle" | "thinking" | "done">("idle");
  const [resolution, setResolution] = useState<Resolution | null>(null);
  const [loadingText, setLoadingText] = useState("Analyse en cours…");
  const resultsRef = useRef<HTMLDivElement>(null);

  const urgencyBg: Record<Urgency, string> = {
    critical: "bg-red-50",
    high: "bg-amber-50",
    normal: "bg-indigo-50",
  };
  const urgencyBorder: Record<Urgency, string> = {
    critical: "border-red-100",
    high: "border-amber-100",
    normal: "border-indigo-100",
  };

  const LOADING_STEPS = [
    "Analyse en cours…",
    "Interrogation des 847 signaux…",
    "Génération du plan stratégique…",
    "Finalisation des recommandations…",
  ];

  function handleResolve() {
    setSolving(true);
    setPhase("thinking");
    setResolution(null);
    setLoadingText(LOADING_STEPS[0]);

    let step = 0;
    const interval = setInterval(() => {
      step++;
      if (step < LOADING_STEPS.length) {
        setLoadingText(LOADING_STEPS[step]);
      } else {
        clearInterval(interval);
      }
    }, 500);

    setTimeout(() => {
      clearInterval(interval);
      const result = generateResolution(challengeType, competitorId, urgency);
      setResolution(result);
      setSolving(false);
      setPhase("done");
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 80);
    }, 2000);
  }

  const threatColors: Record<Resolution["threatLevel"], string> = {
    Critique: "bg-red-100 text-red-700 border-red-300",
    Significatif: "bg-amber-100 text-amber-700 border-amber-300",
    Modéré: "bg-slate-100 text-slate-600 border-slate-300",
  };

  const urgencyLabel = URGENCY_OPTIONS.find((u) => u.value === urgency)?.badge ?? "";
  const selectedCompetitor = competitors.find((c) => c.id === competitorId);

  return (
    <div className="space-y-8 pb-16">
      {/* ── Header ── */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-3 flex-wrap">
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            R&Eacute;SOLVEUR &mdash; Moteur de R&eacute;solution Strat&eacute;gique
          </h1>
          <span className="inline-flex items-center gap-1.5 text-xs font-bold px-2.5 py-1 rounded-full bg-indigo-600 text-white shadow-sm">
            <IconBolt className="w-3 h-3" />
            Aliment&eacute; par 847 signaux &middot; Mise &agrave; jour en temps r&eacute;el
          </span>
        </div>
        <p className="text-slate-500 text-sm max-w-2xl">
          D&eacute;crivez votre d&eacute;fi concurrentiel. R&Eacute;SOLVEUR analyse et g&eacute;n&egrave;re un plan d&apos;action en 30 secondes.
        </p>
      </div>

      {/* ── Form ── */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8 space-y-6">
        <div className="grid md:grid-cols-2 gap-6">
          {/* Challenge type */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Type de d&eacute;fi
            </label>
            <div className="relative">
              <select
                value={challengeType}
                onChange={(e) => setChallengeType(e.target.value as ChallengeType)}
                className="w-full appearance-none bg-white border border-slate-300 rounded-xl px-4 py-3 pr-10 text-slate-800 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent cursor-pointer"
              >
                {CHALLENGE_TYPES.map((ct) => (
                  <option key={ct.value} value={ct.value}>
                    {ct.label}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                <IconChevronDown className="w-4 h-4" />
              </div>
            </div>
          </div>

          {/* Competitor */}
          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Concurrent impliqu&eacute;
            </label>
            <div className="relative">
              <select
                value={competitorId}
                onChange={(e) => setCompetitorId(e.target.value)}
                className="w-full appearance-none bg-white border border-slate-300 rounded-xl px-4 py-3 pr-10 text-slate-800 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent cursor-pointer"
              >
                {competitors.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} &mdash; {c.industry}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                <IconChevronDown className="w-4 h-4" />
              </div>
            </div>
            {selectedCompetitor && (
              <div className="flex items-center gap-2">
                <span className="text-slate-400 text-xs">Menace :</span>
                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                  selectedCompetitor.threatLevel === "high"
                    ? "bg-red-100 text-red-600 border border-red-200"
                    : selectedCompetitor.threatLevel === "medium"
                    ? "bg-amber-100 text-amber-700 border border-amber-200"
                    : "bg-slate-100 text-slate-500 border border-slate-200"
                }`}>
                  {selectedCompetitor.threatLevel === "high" ? "Élevée" : selectedCompetitor.threatLevel === "medium" ? "Moyenne" : "Faible"}
                </span>
                <span className="text-slate-400 text-xs">&middot; {selectedCompetitor.marketShare}% de part de march&eacute;</span>
              </div>
            )}
          </div>
        </div>

        {/* Urgency */}
        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Urgence
          </label>
          <div className="grid grid-cols-3 gap-3">
            {URGENCY_OPTIONS.map((u) => (
              <button
                key={u.value}
                onClick={() => setUrgency(u.value)}
                className={`py-3 rounded-xl text-sm font-semibold border transition-all duration-150 cursor-pointer ${
                  urgency === u.value
                    ? u.value === "critical"
                      ? "bg-red-600 border-red-500 text-white shadow-md"
                      : u.value === "high"
                      ? "bg-amber-500 border-amber-400 text-white shadow-md"
                      : "bg-indigo-600 border-indigo-500 text-white shadow-md"
                    : "bg-white border-slate-300 text-slate-600 hover:border-slate-400 hover:bg-slate-50"
                }`}
              >
                {u.label}
              </button>
            ))}
          </div>
        </div>

        {/* Context textarea */}
        <div className="space-y-2">
          <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Contexte additionnel
            <span className="ml-2 font-normal text-slate-400 normal-case">(optionnel)</span>
          </label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value.slice(0, 500))}
            placeholder="Pr&eacute;cisez la situation, les comptes concern&eacute;s, les informations disponibles&hellip;"
            rows={3}
            className="w-full border border-slate-300 rounded-xl px-4 py-3 text-slate-800 text-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
          />
          <div className="flex justify-end">
            <span className="text-xs text-slate-400">{context.length}/500</span>
          </div>
        </div>

        {/* Resolve button */}
        <div className="pt-2">
          <button
            onClick={handleResolve}
            disabled={solving}
            className="w-full py-4 rounded-xl font-bold text-base text-white relative overflow-hidden transition-all duration-200 cursor-pointer disabled:cursor-not-allowed disabled:opacity-75 active:scale-[0.99]"
            style={{
              background: solving
                ? "linear-gradient(135deg, #4338ca, #6d28d9)"
                : "linear-gradient(135deg, #4f46e5, #7c3aed)",
              boxShadow: solving ? "none" : "0 4px 28px rgba(99,102,241,0.45)",
            }}
          >
            <span className="flex items-center justify-center gap-2.5">
              {solving ? (
                <>
                  <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  <span>{loadingText}</span>
                </>
              ) : (
                <>
                  <IconBolt className="w-5 h-5" />
                  R&Eacute;SOUDRE
                </>
              )}
            </span>
          </button>
        </div>
      </div>

      {/* ── Results ── */}
      <div ref={resultsRef}>
        {phase === "thinking" && <SkeletonLoader />}

        {phase === "done" && resolution && (
          <div className={`space-y-6 rounded-2xl border p-6 md:p-8 ${urgencyBg[urgency]} ${urgencyBorder[urgency]}`}>

            {/* Section header */}
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-md">
                  <IconBolt className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-slate-900">Plan de r&eacute;solution g&eacute;n&eacute;r&eacute;</h2>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {CHALLENGE_TYPES.find((c) => c.value === challengeType)?.label} &middot; {competitors.find((c) => c.id === competitorId)?.name} &middot; {urgencyLabel}
                  </p>
                </div>
              </div>
              <span className={`inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-full border ${threatColors[resolution.threatLevel]}`}>
                <span className="w-1.5 h-1.5 rounded-full bg-current" />
                Menace {resolution.threatLevel}
              </span>
            </div>

            {/* Diagnostic */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-2">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Diagnostic</h3>
              <p className="text-sm text-slate-700 leading-relaxed">{resolution.diagnostic}</p>
            </div>

            {/* 3 Response axes */}
            <div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3">3 axes de r&eacute;ponse</h3>
              <div className="grid md:grid-cols-3 gap-4">
                {resolution.axes.map((axis, i) => (
                  <div
                    key={i}
                    className={`bg-white rounded-xl border border-slate-200 border-l-4 ${axis.borderColor} p-5 space-y-4`}
                  >
                    <div>
                      <span className={`inline-block text-[10px] font-bold px-2 py-0.5 rounded-full ${axis.bgColor} ${axis.textColor} border ${axis.borderColor} uppercase tracking-wide mb-2`}>
                        {axis.range}
                      </span>
                      <h4 className="text-sm font-bold text-slate-800">{axis.horizon}</h4>
                    </div>
                    <ul className="space-y-3">
                      {axis.actions.map((item, j) => (
                        <li key={j} className="flex items-start gap-2">
                          <div className="flex-shrink-0 w-5 h-5 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center mt-0.5">
                            <span className="text-[10px] font-bold text-slate-500">{j + 1}</span>
                          </div>
                          <div className="min-w-0">
                            <p className="text-xs text-slate-700 leading-relaxed">{item.action}</p>
                            <p className="text-[10px] text-slate-400 font-medium mt-0.5">{item.owner}</p>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>

            {/* Battle args */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2 bg-slate-50">
                <IconShield className="w-4 h-4 text-indigo-500" />
                <h3 className="text-sm font-bold text-slate-800">Arguments de vente anti-concurrent</h3>
                <span className="ml-auto text-[10px] font-semibold text-slate-400 uppercase tracking-wide">Battle Card Express</span>
              </div>
              <div className="divide-y divide-slate-100">
                {resolution.battleArgs.map((arg, i) => (
                  <div key={i} className="flex items-start gap-4 px-5 py-4">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 border border-indigo-200 flex items-center justify-center mt-0.5">
                      <span className="text-[10px] font-bold text-indigo-600">{i + 1}</span>
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-slate-800">{arg.title}</p>
                      <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{arg.detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* KPIs */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2 bg-slate-50">
                <IconClock className="w-4 h-4 text-indigo-500" />
                <h3 className="text-sm font-bold text-slate-800">KPIs &agrave; surveiller</h3>
              </div>
              <div className="grid md:grid-cols-2">
                {resolution.kpis.map((kpi, i) => (
                  <div
                    key={i}
                    className={`flex items-start gap-4 px-5 py-4 ${
                      i % 2 === 0 && i < resolution.kpis.length - 1 ? "border-b border-slate-100 md:border-b-0 md:border-r md:border-slate-100" : ""
                    } ${i >= 2 ? "border-t border-slate-100" : ""}`}
                  >
                    <div className="flex-shrink-0 mt-0.5">
                      {kpi.direction === "up" ? (
                        <IconTrendUp className="w-4 h-4 text-emerald-500" />
                      ) : (
                        <IconTrendDown className="w-4 h-4 text-red-500" />
                      )}
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-slate-800">{kpi.metric}</p>
                      <p className="text-xs text-amber-600 font-semibold mt-1">{kpi.threshold}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Agents + links */}
            <div className="grid md:grid-cols-2 gap-4">
              {/* Agents mobilized */}
              <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-3">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Agents CompeteIQ mobilis&eacute;s</h3>
                <ul className="space-y-2.5">
                  {resolution.agents.map((agent, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <span className="flex-shrink-0 inline-block text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-100 text-indigo-700 border border-indigo-200 font-mono tracking-wide">
                        {agent.name}
                      </span>
                      <span className="text-xs text-slate-600 leading-relaxed">{agent.role}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Relevant pages */}
              <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-3">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Pages pertinentes</h3>
                <ul className="space-y-2">
                  {resolution.links.map((link, i) => (
                    <li key={i}>
                      <Link
                        href={link.href}
                        className="flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-800 hover:underline transition-colors"
                      >
                        <IconArrow className="w-3.5 h-3.5 flex-shrink-0" />
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Recent resolutions ── */}
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <h2 className="text-base font-semibold text-slate-800">R&eacute;solutions r&eacute;centes</h2>
          <span className="text-xs text-slate-400 font-medium">Historique des plans ex&eacute;cut&eacute;s</span>
        </div>
        <div className="grid md:grid-cols-3 gap-4">
          {RECENT_RESOLUTIONS.map((r, i) => (
            <div
              key={i}
              className="bg-white rounded-xl border border-slate-200 p-5 space-y-3 hover:border-indigo-200 hover:shadow-sm transition-all duration-150"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="min-w-0">
                  <p className="text-sm font-semibold text-slate-800 leading-snug">{r.type}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{r.competitor}</p>
                </div>
                <span className="flex-shrink-0 inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 border border-emerald-300 whitespace-nowrap">
                  <IconCheck className="w-3 h-3" />
                  R&Eacute;SOLU
                </span>
              </div>
              <div className="bg-emerald-50 border border-emerald-100 rounded-lg px-3 py-2">
                <p className="text-sm font-bold text-emerald-700">{r.result}</p>
                <p className="text-xs text-emerald-600 mt-0.5 leading-relaxed">{r.detail}</p>
              </div>
              <p className="text-xs text-slate-400">{r.date}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

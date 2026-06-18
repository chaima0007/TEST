"use client";

import { useState } from "react";
import { competitors } from "@/lib/data";

// ─── Types ────────────────────────────────────────────────────────────────────

interface Objection {
  trigger: string;
  response: string;
}

interface BuyingSignal {
  signal: string;
  implication: string;
}

interface BattleCardData {
  theirPitch: string[];
  ourResponse: string[];
  objections: Objection[];
  ourAdvantages: { title: string; description: string }[];
  buyingSignals: BuyingSignal[];
  hotCompetitor?: boolean;
}

// ─── Mock Battle Card Data ────────────────────────────────────────────────────

const BATTLE_CARDS: Record<string, BattleCardData> = {
  "1": {
    hotCompetitor: true,
    theirPitch: [
      "Leader mondial du CRM depuis 25 ans — la référence du secteur, adoptée par 150 000 entreprises dans le monde.",
      "Einstein AI intégré nativement : prédictions de closing, scoring automatique, recommandations en temps réel.",
      "Écosystème Salesforce AppExchange avec 7 000+ intégrations — une plateforme extensible à l'infini.",
    ],
    ourResponse: [
      "La taille n'est pas un avantage quand elle se traduit par 18 mois de déploiement et 3 consultants externes. CompeteIQ est opérationnel en 2 semaines.",
      "Einstein AI coûte 75€/utilisateur/mois en supplément. Nos insights IA compétitifs sont inclus dans tous les plans, sans surcoût.",
      "7 000 intégrations signifient 7 000 risques de friction. Nos 120 intégrations natives couvrent 95% des besoins réels — sans custom code.",
    ],
    objections: [
      {
        trigger: "\"Tout le monde utilise Salesforce dans notre secteur\"",
        response: "C'est exactement pourquoi vos concurrents directs ont tous les mêmes données, les mêmes alertes et les mêmes angles d'attaque. CompeteIQ vous donne l'avantage de l'intelligence différenciée — ce qu'ils ne voient pas.",
      },
      {
        trigger: "\"Nos équipes connaissent déjà Salesforce\"",
        response: "La courbe d'apprentissage CompeteIQ est de 4 heures. Notre score d'adoption utilisateur est de 94% après 30 jours — contre 67% en moyenne pour Salesforce selon Forrester 2026.",
      },
      {
        trigger: "\"Salesforce est plus sécurisé / certifié\"",
        response: "Nous sommes certifiés SOC 2 Type II, ISO 27001 et RGPD. Nos données sont hébergées en EU-West. La sécurité n'est pas un avantage Salesforce — c'est une parité.",
      },
      {
        trigger: "\"Le prix est justifié pour Salesforce\"",
        response: "Nous avons analysé 47 migrations récentes. Le coût total Salesforce (licences + intégrations + consulting) est 4,2× supérieur au TCO CompeteIQ sur 3 ans. Voulez-vous voir la simulation pour votre taille d'équipe ?",
      },
    ],
    ourAdvantages: [
      {
        title: "Time-to-value : 14 jours vs 18 mois",
        description: "Déploiement guidé, migration automatique, formation incluse. Vos commerciaux génèrent leurs premières battle cards dès la semaine 2.",
      },
      {
        title: "Intelligence concurrentielle temps réel",
        description: "Monitoring automatique des mouvements concurrentiels, alertes pricing, veille produit — Salesforce n'offre rien de comparable nativement.",
      },
      {
        title: "Prix transparent, sans surprises",
        description: "Un seul tarif, IA incluse, toutes intégrations incluses. Pas de modules additionnels, pas de consultants obligatoires, pas d'augmentation annuelle de 12%.",
      },
    ],
    buyingSignals: [
      { signal: "Le prospect mentionne le coût de leur renouvellement Salesforce", implication: "Fenêtre d'opportunité — proposez notre calculateur TCO immédiatement." },
      { signal: "Ils se plaignent de la complexité de configuration", implication: "Douleur réelle — montrez notre démo d'onboarding en 10 minutes." },
      { signal: "Ils demandent combien de temps prend la migration", implication: "Ils comparent activement — répondez : 14 jours, migration clé en main incluse." },
      { signal: "Ils mentionnent un projet Einstein AI en attente de budget", implication: "Notre IA incluse sans surcoût est un argument décisif — exploitez-le maintenant." },
    ],
  },

  "2": {
    hotCompetitor: true,
    theirPitch: [
      "Tout-en-un marketing + ventes : une seule plateforme pour attirer, convertir et fidéliser — zéro friction entre les équipes.",
      "Plan gratuit généreux qui permet de démarrer sans risque — des milliers de PME ont grandi avec HubSpot.",
      "Interface la plus intuitive du marché : adoptée en quelques heures, sans formation technique.",
    ],
    ourResponse: [
      "Le 'tout-en-un' devient un 'pas assez de chacun' : les rapports compétitifs HubSpot restent basiques. CompeteIQ est spécialisé là où HubSpot est généraliste.",
      "Le plan gratuit est une porte d'entrée, pas une solution. L'Enterprise HubSpot atteint 3 600€/mois — bien au-dessus de notre offre complète.",
      "L'intuitivité HubSpot s'arrête dès qu'on touche à l'automation avancée ou aux rapports personnalisés. Notre UX est conçue pour les équipes commerciales terrain.",
    ],
    objections: [
      {
        trigger: "\"HubSpot est gratuit pour commencer\"",
        response: "Le gratuit couvre 2 utilisateurs avec des fonctionnalités très limitées. La migration vers un plan payant survient systématiquement dans les 90 jours. Notre essai gratuit 14 jours est complet — sans carte bleue, sans dégradation.",
      },
      {
        trigger: "\"On utilise déjà HubSpot pour le marketing\"",
        response: "Parfait — nous nous intégrons nativement avec HubSpot Marketing. Votre équipe marketing garde son outil, vos commerciaux gagnent l'intelligence concurrentielle qui manque à HubSpot Sales.",
      },
      {
        trigger: "\"HubSpot a une meilleure réputation dans notre industrie\"",
        response: "HubSpot domine le marketing inbound. Pour la vente compétitive B2B, G2 nous classe #1 sur l'intelligence concurrentielle — leur domaine d'excellence ne se superpose pas au nôtre.",
      },
      {
        trigger: "\"Le support HubSpot est très bien noté\"",
        response: "Notre NPS support est de 72 (vs 61 pour HubSpot selon G2 2026). Chaque client a un Customer Success Manager dédié — pas une ligne de ticket partagée.",
      },
    ],
    ourAdvantages: [
      {
        title: "Spécialisation intel concurrentielle vs généralisme",
        description: "HubSpot est excellent pour le marketing. CompeteIQ est conçu exclusivement pour la vente compétitive — battle cards, win/loss analysis, alertes marché en temps réel.",
      },
      {
        title: "Coût prévisible sans effet palier",
        description: "HubSpot facture par feature sets avec des sauts de palier brutaux (20€ → 3 600€). Notre tarification est linéaire et prévisible sur 3 ans.",
      },
      {
        title: "Données concurrentielles structurées",
        description: "Quand votre commercial est en call, il accède en 10 secondes à la battle card du concurrent mentionné. HubSpot n'a pas d'équivalent.",
      },
    ],
    buyingSignals: [
      { signal: "Ils demandent une intégration HubSpot", implication: "Bonne nouvelle — nous l'avons. Montrez la démo d'intégration bidirectionnelle." },
      { signal: "Ils mentionnent un palier de prix HubSpot à venir", implication: "Timing idéal pour une comparaison TCO — proposez-la avant leur renouvellement." },
      { signal: "L'équipe marketing est sur HubSpot mais les ventes se plaignent", implication: "Douleur organisationnelle classique — positionnez-vous comme le complément ventes." },
      { signal: "Ils évaluent le Sales Hub Professional à 100€/user", implication: "Comparez directement notre offre équivalente — ils paieront moins pour plus de fonctionnalités compétitives." },
    ],
  },

  "3": {
    theirPitch: [
      "Interface pipeline visuelle la plus simple du marché — tout vendeur la maîtrise en une heure, sans formation IT.",
      "Conçu exclusivement pour les équipes de vente : pas de fonctionnalités marketing superflues, focus absolu sur le closing.",
      "Rapport qualité-prix imbattable pour les équipes de moins de 20 commerciaux.",
    ],
    ourResponse: [
      "La simplicité Pipedrive devient une limitation dès que votre pipeline complexifie. Notre vue concurrentielle n'a pas d'équivalent chez eux.",
      "Focus sur la vente, oui — mais sans intelligence sur vos concurrents, vous closez à l'aveugle. CompeteIQ ajoute la couche stratégique qui manque.",
      "Pipedrive à 59€/user/mois pour les fonctionnalités équivalentes. Notre offre inclut l'intel concurrentielle, les battle cards et les alertes — Pipedrive ne propose rien de tel.",
    ],
    objections: [
      {
        trigger: "\"Pipedrive est plus simple à utiliser\"",
        response: "Pipedrive est effectivement simple — pour le suivi de pipeline basique. CompeteIQ est aussi simple pour ce qu'il fait : 4h de formation, 94% d'adoption. La complexité perçue vient de la richesse fonctionnelle, pas de l'UX.",
      },
      {
        trigger: "\"Pipedrive est moins cher\"",
        response: "Pipedrive Essential à 15€ vs notre offre complète : vous comparez des périmètres différents. Sur un périmètre équivalent (AI Insights inclus, Pipedrive Professional à 59€), nous sommes compétitifs — et nous incluons l'intel concurrentielle.",
      },
      {
        trigger: "\"Notre équipe aime déjà Pipedrive\"",
        response: "Bonne nouvelle — nous nous intégrons avec Pipedrive via API native. Vos données de pipeline restent dans Pipedrive, CompeteIQ ajoute la couche d'intelligence que Pipedrive ne peut pas fournir.",
      },
      {
        trigger: "\"Pipedrive suffit pour notre taille\"",
        response: "Aujourd'hui peut-être. Mais à mesure que vous scalerez, l'absence de reporting avancé et d'intel marché deviendra douloureuse. Nos clients évitent une migration forcée dans 18 mois en choisissant dès maintenant une solution évolutive.",
      },
    ],
    ourAdvantages: [
      {
        title: "Reporting avancé nativement inclus",
        description: "Pipedrive n'offre pas de rapports avancés selon sa propre fiche produit. CompeteIQ inclut analytics prédictifs, win/loss, et benchmarks sectoriels dans tous les plans.",
      },
      {
        title: "Intelligence concurrentielle intégrée",
        description: "Pipedrive AI Sales Assistant prédit vos prochaines actions. CompeteIQ vous dit exactement comment battre Salesforce, HubSpot, et les autres — au moment où vous en avez besoin.",
      },
      {
        title: "Scalabilité sans migration",
        description: "Les clients Pipedrive migrent en moyenne après 24 mois quand leurs besoins évoluent. CompeteIQ est conçu pour des équipes de 5 à 500 commerciaux sans changement d'architecture.",
      },
    ],
    buyingSignals: [
      { signal: "Ils mentionnent une équipe de vente qui grandit", implication: "Angle scalabilité — Pipedrive montre ses limites dès 20+ users." },
      { signal: "Ils cherchent des rapports de performance commerciale", implication: "Lacune connue de Pipedrive — montrez nos dashboards analytics immédiatement." },
      { signal: "Ils comparent les prix par utilisateur", implication: "Calculez le TCO complet — incluez le coût de la migration future qu'ils éviteront." },
      { signal: "Ils posent des questions sur les intégrations", implication: "Notre API native Pipedrive signifie qu'ils peuvent garder leur pipeline existant — argument de transition en douceur." },
    ],
  },

  "4": {
    theirPitch: [
      "Suite complète 55 applications pour le prix d'un seul outil concurrent — le meilleur rapport valeur globale du marché.",
      "Solution économique conçue pour les PME : plan gratuit 3 utilisateurs, puis tarifs imbattables dès 14€/mois.",
      "Zia AI intégrée : assistant intelligent pour les prédictions de vente, détection d'anomalies, suggestions de workflow.",
    ],
    ourResponse: [
      "55 applications dont vous n'utiliserez que 5 — la suite Zoho est une illusion de valeur. La complexité cachée génère des coûts de mise en œuvre souvent supérieurs à des outils spécialisés.",
      "Zoho est économique en licences, mais le coût d'implémentation d'un partenaire certifié dépasse régulièrement 15 000€ pour une PME de 20 personnes.",
      "Zia reste en retard sur les capacités IA de marché selon les benchmarks Gartner 2026. Nos insights compétitifs sont plus actionnables pour les équipes de vente.",
    ],
    objections: [
      {
        trigger: "\"Zoho est beaucoup moins cher\"",
        response: "Les licences Zoho sont moins chères — jusqu'à ce qu'on additionne le coût d'un partenaire Zoho, la formation, et les intégrations custom. Demandez-leur une démo d'implémentation end-to-end et chronométrez.",
      },
      {
        trigger: "\"On peut tout faire avec Zoho One\"",
        response: "Zoho One à 37€/user inclut 55 apps. En réalité, les équipes utilisent Zoho CRM + Zoho Campaigns + Zoho Analytics — soit 3 interfaces à former, 3 sources de données à réconcilier. CompeteIQ unifie le flux commercial dans une seule vue.",
      },
      {
        trigger: "\"Zoho a une bonne réputation dans notre secteur\"",
        response: "Zoho est bien noté pour le rapport qualité-prix des PME généralistes. Pour la vente compétitive et l'intel marché, ils n'ont pas de fonctionnalité équivalente à ce que nous proposons.",
      },
      {
        trigger: "\"Le support Zoho est disponible en français\"",
        response: "Notre support est également disponible en français 24/7, avec un Customer Success Manager francophone dédié. Notre NPS de 72 dépasse la moyenne Zoho de 58 points selon G2.",
      },
    ],
    ourAdvantages: [
      {
        title: "Simplicité vs complexité de suite",
        description: "Zoho = 55 apps à gérer. CompeteIQ = 1 plateforme focalisée. Vos commerciaux passent leur temps à vendre, pas à naviguer entre modules.",
      },
      {
        title: "Intel concurrentielle sans équivalent",
        description: "Zoho CRM ne monitore pas vos concurrents, n'envoie pas d'alertes pricing, et n'a pas de battle cards nativement. C'est notre cœur de métier — pas une feature parmi 500.",
      },
      {
        title: "Intégration sans partenaire requis",
        description: "Déploiement autonome en 2 semaines. Pas de partenaire certifié obligatoire, pas de customisation coûteuse — notre interface guide l'implémentation étape par étape.",
      },
    ],
    buyingSignals: [
      { signal: "Ils mentionnent la complexité de leur setup Zoho actuel", implication: "Frustration existante — proposez une migration assistée gratuite." },
      { signal: "Ils demandent combien de modules sont nécessaires", implication: "Ils sont conscients du sprawl Zoho — jouez la carte de la simplicité." },
      { signal: "Ils comparent sur la base du prix/utilisateur seulement", implication: "Élargissez la conversation au TCO et au coût d'implémentation." },
      { signal: "Leur équipe IT gère Zoho comme un projet à part entière", implication: "Coût caché identifié — montrez notre modèle self-service sans intervention IT." },
    ],
  },

  "5": {
    theirPitch: [
      "Plateforme de travail unifiée : gestion de projets, CRM et collaboration dans un seul outil — la fin des silos organisationnels.",
      "Flexibilité maximale : Monday se configure pour n'importe quel process commercial, sans code, en quelques clics.",
      "Adopté par 225 000 entreprises — une des croissances SaaS les plus rapides du marché.",
    ],
    ourResponse: [
      "Monday est excellent pour gérer des projets. Pour vendre, il manque la profondeur CRM : pas d'automatisation ventes avancée, pas d'intel concurrentielle, pas de forecasting fiable.",
      "La flexibilité totale est aussi une malédiction : vos équipes passent des semaines à configurer des 'boards' au lieu de vendre. CompeteIQ est prêt à l'emploi pour les équipes commerciales.",
      "225 000 clients dont la majorité utilisent Monday pour des usages projets — pas pour des CRM ventes enterprise. La croissance ne valide pas l'adéquation au besoin.",
    ],
    objections: [
      {
        trigger: "\"On utilise déjà Monday pour nos projets\"",
        response: "Parfait — gardez Monday pour vos projets. CompeteIQ est votre outil de vente compétitive : il se connecte à Monday via notre intégration native. Pas de remplacement, une complémentarité.",
      },
      {
        trigger: "\"Monday peut tout faire avec les bonnes colonnes\"",
        response: "Peut-être — mais combien de temps avez-vous investi à configurer votre 'CRM Monday' ? Nos clients qui migraient depuis Monday récupèrent en moyenne 6 heures/semaine perdues en maintenance de boards.",
      },
      {
        trigger: "\"Le prix Monday est très attractif\"",
        response: "À 12€/user pour le plan Standard, Monday est attractif pour un outil projet. Un CRM commercial réel — avec automation, forecasting, et intel concurrentielle — vous coûterait 3 outils supplémentaires. CompeteIQ tout-en-un est plus économique.",
      },
      {
        trigger: "\"Monday AI vient d'être lancé en GA\"",
        response: "Monday AI automatise la création de tâches — c'est utile pour la gestion de projet. Notre IA analyse les mouvements concurrentiels, prédit les menaces, et génère des battle cards en temps réel. Ce sont deux catégories d'IA différentes.",
      },
    ],
    ourAdvantages: [
      {
        title: "CRM ventes natif vs outil de projet détourné",
        description: "Monday est un outil de gestion de travail re-skinné en CRM. CompeteIQ est conçu from scratch pour les équipes commerciales — chaque fonctionnalité répond à un besoin de vente réel.",
      },
      {
        title: "Automatisation ventes avancée incluse",
        description: "Monday n'offre pas d'automatisation des ventes selon sa propre fiche produit. CompeteIQ automatise relances, scoring, et alertes concurrentielles sans configuration manuelle.",
      },
      {
        title: "Intelligence marché vs intelligence projet",
        description: "Quand un concurrent baisse ses prix ou lance une feature, vous le savez en temps réel. Monday vous dira quand votre prochaine réunion est planifiée — pas ce qui menace votre pipeline.",
      },
    ],
    buyingSignals: [
      { signal: "Ils utilisent Monday comme CRM improvisé", implication: "Douleur structurelle — ils ont besoin d'un vrai CRM commercial, pas d'un board." },
      { signal: "Ils mentionnent le temps passé à maintenir leurs boards", implication: "Coût caché en temps — calculez les heures perdues et traduisez en €." },
      { signal: "Leur équipe commerciale se plaint du manque de visibilité pipeline", implication: "Frustration directe — montrez notre vue pipeline temps réel en démo." },
      { signal: "Ils demandent si on remplace Monday", implication: "Non — on le complète. Jouez la carte de la coexistence pour réduire la résistance au changement." },
    ],
  },
};

// ─── SVG Icons ─────────────────────────────────────────────────────────────────

function IconBullhorn({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M13 6.5V4a1 1 0 0 0-1.447-.894L5 6H4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h1l.553.276A1 1 0 0 0 7 13.382V15a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1.382l3.447 1.724A1 1 0 0 0 15 14.5v-9a1 1 0 0 0-1.447-.894L13 4.724V6.5zM9 14v-1h-.001L9 13v1z" />
    </svg>
  );
}

function IconShield({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M10 1.944A11.954 11.954 0 0 1 2.166 5C2.056 5.649 2 6.319 2 7c0 5.225 3.34 9.67 8 11.317C14.66 16.67 18 12.225 18 7c0-.682-.057-1.35-.166-2.001A11.954 11.954 0 0 1 10 1.944zM11 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm0-7a1 1 0 1 0-2 0v3a1 1 0 1 0 2 0V7z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconLightning({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M11.3 1.046A1 1 0 0 1 12 2v5h4a1 1 0 0 1 .82 1.573l-7 10A1 1 0 0 1 8 18v-5H4a1 1 0 0 1-.82-1.573l7-10a1 1 0 0 1 1.12-.381z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconStar({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 0 0 .95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 0 0-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 0 0-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 0 0-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 0 0 .951-.69l1.07-3.292z" />
    </svg>
  );
}

function IconEye({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" />
      <path
        fillRule="evenodd"
        d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 1 1-8 0 4 4 0 0 1 8 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconPrint({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M5 4v3H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h1v1a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-1V4a1 1 0 0 0-1-1H6a1 1 0 0 0-1 1zm2 0h6v3H7V4zm-1 9H5v2h10v-2h-1v-1H6v1zm9-5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"
        clipRule="evenodd"
      />
    </svg>
  );
}

function IconSync({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path
        fillRule="evenodd"
        d="M4 2a1 1 0 0 1 1 1v2.101a7.002 7.002 0 0 1 11.601 2.566 1 1 0 1 1-1.885.666A5.002 5.002 0 0 0 5.999 7H9a1 1 0 0 1 0 2H4a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1zm.008 9.057a1 1 0 0 1 1.276.61A5.002 5.002 0 0 0 14.001 13H11a1 1 0 1 1 0-2h5a1 1 0 0 1 1 1v5a1 1 0 1 1-2 0v-2.101a7.002 7.002 0 0 1-11.601-2.566 1 1 0 0 1 .61-1.276z"
        clipRule="evenodd"
      />
    </svg>
  );
}

// ─── Main Page ─────────────────────────────────────────────────────────────────

export default function BattleCardsPage() {
  const [selectedId, setSelectedId] = useState<string>(competitors[0].id);

  const selectedCompetitor = competitors.find((c) => c.id === selectedId) ?? competitors[0];
  const card = BATTLE_CARDS[selectedId] ?? BATTLE_CARDS[competitors[0].id];

  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Battle Cards Commerciales
          </h1>
          <p className="text-slate-500 text-sm mt-1">
            Tout ce qu&apos;il faut savoir avant un appel concurrentiel
          </p>
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-700">
            <IconSync className="w-3 h-3" />
            Mis à jour en temps réel
          </span>
          <button
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg border border-slate-200 bg-white text-slate-700 text-sm font-medium hover:bg-slate-50 hover:border-slate-300 transition-all shadow-sm"
            onClick={() => window.print()}
          >
            <IconPrint className="w-4 h-4" />
            <span className="hidden sm:inline">Imprimer / Exporter PDF</span>
            <span className="sm:hidden">Exporter</span>
          </button>
        </div>
      </div>

      {/* ── Competitor Pills ── */}
      <div className="flex flex-wrap gap-2">
        {competitors.map((c) => {
          const isSelected = c.id === selectedId;
          const cardData = BATTLE_CARDS[c.id];
          const isHot = cardData?.hotCompetitor;

          return (
            <button
              key={c.id}
              onClick={() => setSelectedId(c.id)}
              className={[
                "relative inline-flex items-center gap-2 px-4 py-2.5 rounded-full text-sm font-medium border transition-all",
                isSelected
                  ? "text-white border-transparent shadow-md scale-105"
                  : "bg-white text-slate-700 border-slate-200 hover:border-slate-300 hover:bg-slate-50 hover:shadow-sm cursor-pointer",
              ].join(" ")}
              style={isSelected ? { backgroundColor: c.color, borderColor: c.color } : {}}
            >
              {/* Avatar */}
              <span
                className="w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
                style={{ backgroundColor: isSelected ? "rgba(255,255,255,0.25)" : c.color }}
              >
                {c.logo}
              </span>
              {c.name}
              {/* HOT badge */}
              {isHot && !isSelected && (
                <span className="absolute -top-2 -right-1 bg-red-500 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full leading-none tracking-wide uppercase">
                  HOT
                </span>
              )}
              {isHot && isSelected && (
                <span className="bg-white/25 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full leading-none tracking-wide uppercase">
                  HOT
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* ── Battle Card ── */}
      {card && (
        <div className="space-y-5">
          {/* Card header */}
          <div
            className="rounded-xl p-4 flex items-center gap-4 border"
            style={{ backgroundColor: `${selectedCompetitor.color}12`, borderColor: `${selectedCompetitor.color}30` }}
          >
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-sm flex-shrink-0"
              style={{ backgroundColor: selectedCompetitor.color }}
            >
              {selectedCompetitor.logo}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-lg font-bold text-slate-900">{selectedCompetitor.name}</h2>
                <span
                  className="text-xs font-semibold px-2 py-0.5 rounded-full text-white"
                  style={{ backgroundColor: selectedCompetitor.color }}
                >
                  {selectedCompetitor.industry}
                </span>
                {card.hotCompetitor && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-red-100 text-red-600 border border-red-200">
                    Menace active
                  </span>
                )}
              </div>
              <p className="text-sm text-slate-500 mt-0.5 line-clamp-1">{selectedCompetitor.description}</p>
            </div>
            <div className="hidden sm:flex flex-col items-end gap-1 flex-shrink-0">
              <span className="text-xs text-slate-400">Part de marché</span>
              <span className="text-2xl font-bold text-slate-900">{selectedCompetitor.marketShare}%</span>
            </div>
          </div>

          {/* 4 Quadrants */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Quadrant 1 — Leur pitch (rouge) */}
            <div className="bg-white rounded-xl border border-slate-200 border-l-4 border-l-red-400 overflow-hidden shadow-sm">
              <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-red-100 flex items-center justify-center flex-shrink-0">
                  <IconBullhorn className="w-4 h-4 text-red-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 text-sm">Leur pitch</h3>
                  <p className="text-xs text-slate-400">Ce qu&apos;ils disent à vos prospects</p>
                </div>
              </div>
              <ul className="px-5 py-4 space-y-3">
                {card.theirPitch.map((point, i) => (
                  <li key={i} className="flex gap-3">
                    <span className="w-5 h-5 rounded-full bg-red-100 text-red-500 text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <p className="text-sm text-slate-700 leading-relaxed">{point}</p>
                  </li>
                ))}
              </ul>
            </div>

            {/* Quadrant 2 — Notre réponse (vert) */}
            <div className="bg-white rounded-xl border border-slate-200 border-l-4 border-l-emerald-400 overflow-hidden shadow-sm">
              <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
                  <IconShield className="w-4 h-4 text-emerald-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 text-sm">Notre réponse</h3>
                  <p className="text-xs text-slate-400">Contre-arguments CompeteIQ</p>
                </div>
              </div>
              <ul className="px-5 py-4 space-y-3">
                {card.ourResponse.map((point, i) => (
                  <li key={i} className="flex gap-3">
                    <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <svg viewBox="0 0 12 12" fill="currentColor" className="w-3 h-3">
                        <path d="M10 3L5 8 2 5" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </span>
                    <p className="text-sm text-slate-700 leading-relaxed">{point}</p>
                  </li>
                ))}
              </ul>
            </div>

            {/* Quadrant 3 — Quand vous entendez (orange) */}
            <div className="bg-white rounded-xl border border-slate-200 border-l-4 border-l-orange-400 overflow-hidden shadow-sm">
              <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-orange-100 flex items-center justify-center flex-shrink-0">
                  <IconLightning className="w-4 h-4 text-orange-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 text-sm">Quand vous entendez&hellip;</h3>
                  <p className="text-xs text-slate-400">Objections &amp; réponses suggérées</p>
                </div>
              </div>
              <div className="px-5 py-4 space-y-4">
                {card.objections.map((obj, i) => (
                  <div key={i} className="space-y-1.5">
                    <p className="text-xs font-semibold text-orange-700 bg-orange-50 border border-orange-100 rounded-lg px-3 py-2 leading-snug">
                      {obj.trigger}
                    </p>
                    <p className="text-sm text-slate-700 leading-relaxed pl-3 border-l-2 border-orange-200">
                      {obj.response}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Quadrant 4 — Nos avantages décisifs (indigo) */}
            <div className="bg-white rounded-xl border border-slate-200 border-l-4 border-l-indigo-400 overflow-hidden shadow-sm">
              <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
                  <IconStar className="w-4 h-4 text-indigo-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 text-sm">Nos avantages décisifs</h3>
                  <p className="text-xs text-slate-400">Là où CompeteIQ gagne clairement</p>
                </div>
              </div>
              <div className="px-5 py-4 space-y-4">
                {card.ourAdvantages.map((adv, i) => (
                  <div key={i} className="flex gap-3">
                    <div className="w-7 h-7 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                      <span className="text-indigo-600 text-xs font-bold">{i + 1}</span>
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-slate-900">{adv.title}</p>
                      <p className="text-sm text-slate-500 mt-0.5 leading-relaxed">{adv.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* ── Signaux d'achat ── */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-5 py-3.5 border-b border-slate-100 flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-violet-100 flex items-center justify-center flex-shrink-0">
                <IconEye className="w-4 h-4 text-violet-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 text-sm">Signaux d&apos;achat</h3>
                <p className="text-xs text-slate-400">
                  Comportements indiquant que le prospect compare activement avec {selectedCompetitor.name}
                </p>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-0 divide-y sm:divide-y-0 sm:divide-x divide-slate-100">
              {card.buyingSignals.map((signal, i) => (
                <div key={i} className="px-5 py-4 flex gap-3">
                  <div className="w-2 h-2 rounded-full bg-violet-400 flex-shrink-0 mt-2" />
                  <div>
                    <p className="text-sm font-medium text-slate-800">{signal.signal}</p>
                    <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                      <span className="font-semibold text-violet-600">Action :</span>{" "}
                      {signal.implication}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* ── Footer meta ── */}
          <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
            <span>
              Dernière mise à jour :{" "}
              {new Date(selectedCompetitor.lastUpdated).toLocaleDateString("fr-FR", {
                day: "numeric",
                month: "long",
                year: "numeric",
              })}
            </span>
            <span>
              Source : CompeteIQ Intelligence Engine &mdash; données vérifiées
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

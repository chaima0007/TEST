"use client";

import { useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface ActionItem {
  id: string;
  label: string;
  priority: "CRITIQUE" | "HAUTE" | "NORMALE";
  team: string;
  kpi: string;
}

interface Horizon {
  label: string;
  days: string;
  bgColor: string;
  borderColor: string;
  badgeColor: string;
  actions: ActionItem[];
}

interface AxisStrategy {
  action: string;
  owner: string;
}

interface AxisMilestone {
  label: string;
  done: boolean;
}

interface Axis {
  id: number;
  name: string;
  objective: string;
  competitor: string;
  competitorColor: string;
  accentBg: string;
  accentBorder: string;
  accentText: string;
  accentBadgeBg: string;
  accentBadgeBorder: string;
  strategy: AxisStrategy[];
  milestones: AxisMilestone[];
  successRate: number;
  successColor: string;
}

interface RiskItem {
  title: string;
  description: string;
  mitigation: string;
  planB: string;
  level: "ÉLEVÉ" | "MOYEN" | "FAIBLE";
  levelColor: string;
}

// ─── Static data ──────────────────────────────────────────────────────────────

const AXES: Axis[] = [
  {
    id: 1,
    name: "Axe 1 — Conquête des ETI industrielles",
    objective: "+45 clients · +2.1M€ ARR",
    competitor: "Salesforce",
    competitorColor: "bg-blue-100 text-blue-700 border border-blue-200",
    accentBg: "bg-indigo-50",
    accentBorder: "border-indigo-200",
    accentText: "text-indigo-700",
    accentBadgeBg: "bg-indigo-100",
    accentBadgeBorder: "border-indigo-200",
    strategy: [
      { action: "Lancer un programme de migration Salesforce → CompeteIQ avec remise 30% la première année", owner: "Direction Commerciale" },
      { action: "Créer 6 études de cas ROI secteur industriel en 60 jours", owner: "Marketing" },
      { action: "Développer un connecteur natif ERP SAP S/4HANA prioritaire", owner: "Produit" },
    ],
    milestones: [
      { label: "J+30", done: true },
      { label: "J+90", done: false },
      { label: "J+180", done: false },
    ],
    successRate: 78,
    successColor: "text-emerald-700 bg-emerald-50 border-emerald-200",
  },
  {
    id: 2,
    name: "Axe 2 — Captation des PME tech en hypercroissance",
    objective: "+80 clients · +1.6M€ ARR",
    competitor: "HubSpot",
    competitorColor: "bg-orange-100 text-orange-700 border border-orange-200",
    accentBg: "bg-emerald-50",
    accentBorder: "border-emerald-200",
    accentText: "text-emerald-700",
    accentBadgeBg: "bg-emerald-100",
    accentBadgeBorder: "border-emerald-200",
    strategy: [
      { action: "Lancer une offre startup 6 mois gratuits avec onboarding dédié senior", owner: "Direction Commerciale" },
      { action: "Activer un programme référencement VC & accélérateurs (Station F, Kima)", owner: "Marketing" },
      { action: "Intégration native Slack, Notion et Linear dans les 45 prochains jours", owner: "Produit" },
    ],
    milestones: [
      { label: "J+30", done: true },
      { label: "J+90", done: false },
      { label: "J+180", done: false },
    ],
    successRate: 65,
    successColor: "text-amber-700 bg-amber-50 border-amber-200",
  },
  {
    id: 3,
    name: "Axe 3 — Expansion Grand Compte public & parapublic",
    objective: "+12 clients · +3.8M€ ARR",
    competitor: "Oracle CX",
    competitorColor: "bg-red-100 text-red-700 border border-red-200",
    accentBg: "bg-amber-50",
    accentBorder: "border-amber-200",
    accentText: "text-amber-700",
    accentBadgeBg: "bg-amber-100",
    accentBadgeBorder: "border-amber-200",
    strategy: [
      { action: "Obtenir la qualification UGAP et référencement CAIH en 90 jours", owner: "Direction Commerciale" },
      { action: "Produire un livre blanc sécurité & conformité RGPD HDS co-signé ANSSI", owner: "Marketing" },
      { action: "Certifier l'hébergement SecNumCloud sur l'infrastructure nationale", owner: "Produit" },
    ],
    milestones: [
      { label: "J+30", done: false },
      { label: "J+90", done: false },
      { label: "J+180", done: false },
    ],
    successRate: 52,
    successColor: "text-red-700 bg-red-50 border-red-200",
  },
];

const HORIZONS: Horizon[] = [
  {
    label: "30 jours",
    days: "Quick wins",
    bgColor: "bg-indigo-50",
    borderColor: "border-indigo-100",
    badgeColor: "bg-indigo-600 text-white",
    actions: [
      { id: "a1", label: "Identifier 150 prospects ETI industrielles via LinkedIn Sales Navigator", priority: "CRITIQUE", team: "Direction Commerciale", kpi: "Liste qualifiée 150 leads" },
      { id: "a2", label: "Lancer la campagne email migration Salesforce avec offre remise 30%", priority: "CRITIQUE", team: "Marketing", kpi: "Taux d'ouverture >35%" },
      { id: "a3", label: "Publier 2 études de cas ROI secteur manufacturier sur le site", priority: "HAUTE", team: "Marketing", kpi: "+20% trafic organique" },
      { id: "a4", label: "Démarrer le développement du connecteur SAP S/4HANA", priority: "HAUTE", team: "Produit", kpi: "Sprint 1 livré" },
      { id: "a5", label: "Mettre en place le programme referral VC (Station F, Kima, Alven)", priority: "NORMALE", team: "Direction Commerciale", kpi: "5 partenaires signés" },
    ],
  },
  {
    label: "60 jours",
    days: "Consolidation",
    bgColor: "bg-emerald-50",
    borderColor: "border-emerald-100",
    badgeColor: "bg-emerald-600 text-white",
    actions: [
      { id: "b1", label: "Organiser 3 webinaires sectoriels avec témoignages clients existants", priority: "CRITIQUE", team: "Marketing", kpi: "200 participants cumulés" },
      { id: "b2", label: "Déployer l'intégration Slack + Notion en bêta clients PME tech", priority: "CRITIQUE", team: "Produit", kpi: "NPS bêta >45" },
      { id: "b3", label: "Qualifier et pitcher 20 comptes ETI en démo live", priority: "HAUTE", team: "Direction Commerciale", kpi: "20% taux de conversion démo" },
      { id: "b4", label: "Soumettre le dossier de qualification UGAP", priority: "HAUTE", team: "Direction Commerciale", kpi: "Dossier déposé" },
      { id: "b5", label: "Lancer la campagne ABM Grand Compte avec séquences personnalisées", priority: "NORMALE", team: "Marketing", kpi: "15 meetings C-level" },
    ],
  },
  {
    label: "90 jours",
    days: "Accélération stratégique",
    bgColor: "bg-amber-50",
    borderColor: "border-amber-100",
    badgeColor: "bg-amber-600 text-white",
    actions: [
      { id: "c1", label: "Signer 15 nouveaux clients ETI et annoncer les premiers cas de référence", priority: "CRITIQUE", team: "Direction Commerciale", kpi: "+15 logos / +600k€ ARR" },
      { id: "c2", label: "Lancer la version GA du connecteur SAP avec formation partenaires", priority: "CRITIQUE", team: "Produit", kpi: "10 déploiements actifs" },
      { id: "c3", label: "Publier le livre blanc RGPD HDS et activer la relation presse", priority: "HAUTE", team: "Marketing", kpi: "5 articles tier-1 press" },
      { id: "c4", label: "Recruter 3 Account Executives secteur industrie & public", priority: "HAUTE", team: "Direction Commerciale", kpi: "3 postes pourvus" },
      { id: "c5", label: "Review stratégique board avec mise à jour du plan 180 jours", priority: "NORMALE", team: "Direction Générale", kpi: "Deck validé CA" },
    ],
  },
];

const BUDGET_ROWS = [
  { axe: "Axe 1 — ETI industrielles", investissement: "380 000 €", roi: "2.1M€ ARR", delai: "8 mois", roiColor: "text-emerald-700", isTotal: false },
  { axe: "Axe 2 — PME tech hypercroissance", investissement: "210 000 €", roi: "1.6M€ ARR", delai: "6 mois", roiColor: "text-emerald-700", isTotal: false },
  { axe: "Axe 3 — Grand Compte public", investissement: "520 000 €", roi: "3.8M€ ARR", delai: "14 mois", roiColor: "text-amber-700", isTotal: false },
  { axe: "Total plan 18 mois", investissement: "1 110 000 €", roi: "7.5M€ ARR", delai: "~10 mois", roiColor: "text-indigo-700", isTotal: true },
];

const RISKS: RiskItem[] = [
  {
    title: "Accélération concurrentielle Salesforce sur le segment ETI",
    description: "Salesforce pourrait répliquer notre offre tarifaire et bloquer les migrations avec des clauses contractuelles longue durée.",
    mitigation: "Sécuriser en priorité les comptes ETI avec des contrats 2 ans dès Q1. Activer les clauses de portabilité des données via le RGPD.",
    planB: "Pivoter sur un positionnement hybride Salesforce + CompeteIQ en mode complémentaire (phase de transition), puis migration progressive.",
    level: "ÉLEVÉ",
    levelColor: "text-red-700 bg-red-50 border-red-200",
  },
  {
    title: "Délai de qualification UGAP dépassé",
    description: "Le processus UGAP peut prendre 12 à 18 mois. Un retard bloquerait l'axe 3 et décalerait les signatures Grand Compte.",
    mitigation: "Engager un consultant spécialisé marchés publics dès J+15. Préparer un dossier technique SecNumCloud en parallèle pour l'ANSSI.",
    planB: "Cibler les acheteurs publics via des groupements de commande régionaux (RESAH, UniHA) en attendant la qualification centrale.",
    level: "MOYEN",
    levelColor: "text-amber-700 bg-amber-50 border-amber-200",
  },
  {
    title: "Rétention des talents clés pendant la phase d'accélération",
    description: "Les 3 Account Executives seniors et le VP Product pourraient être approchés par les concurrents ou des scale-ups en financement Series B/C.",
    mitigation: "Activer un plan de BSA (Bons de Souscription d'Actions) avec vesting 4 ans pour les 8 profils critiques identifiés avant fin Q1.",
    planB: "Contractualiser avec 2 cabinets de recrutement spécialisés SaaS (Ignition Program, Weem) pour réduction du time-to-hire à 30 jours.",
    level: "FAIBLE",
    levelColor: "text-emerald-700 bg-emerald-50 border-emerald-200",
  },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function PriorityBadge({ priority }: { priority: ActionItem["priority"] }) {
  const styles: Record<ActionItem["priority"], string> = {
    CRITIQUE: "bg-red-100 text-red-700 border border-red-200",
    HAUTE: "bg-amber-100 text-amber-700 border border-amber-200",
    NORMALE: "bg-slate-100 text-slate-600 border border-slate-200",
  };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold tracking-wide ${styles[priority]}`}>
      {priority}
    </span>
  );
}

function ProgressMilestones({ milestones }: { milestones: AxisMilestone[] }) {
  const total = milestones.length;
  const done = milestones.filter((m) => m.done).length;
  const pct = Math.round((done / total) * 100);

  return (
    <div className="mt-4">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-xs text-slate-500 font-medium">Progression jalons</span>
        <span className="text-xs font-semibold text-slate-700">{pct}%</span>
      </div>
      <div className="relative h-2 bg-slate-100 rounded-full overflow-hidden mb-3">
        <div
          className="absolute inset-y-0 left-0 bg-indigo-500 rounded-full transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="flex items-center gap-3">
        {milestones.map((m) => (
          <div key={m.label} className="flex items-center gap-1.5">
            <div
              className={`w-3 h-3 rounded-full border-2 ${
                m.done ? "bg-indigo-500 border-indigo-500" : "bg-white border-slate-300"
              }`}
            />
            <span className="text-xs text-slate-500">{m.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function ChecklistSection({
  horizon,
  checked,
  onToggle,
}: {
  horizon: Horizon;
  checked: Record<string, boolean>;
  onToggle: (id: string) => void;
}) {
  return (
    <div className={`rounded-2xl border ${horizon.borderColor} ${horizon.bgColor} p-6`}>
      <div className="flex items-center gap-3 mb-5">
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold ${horizon.badgeColor}`}>
          {horizon.label}
        </span>
        <span className="text-sm text-slate-500 font-medium">{horizon.days}</span>
      </div>
      <div className="space-y-3">
        {horizon.actions.map((action) => (
          <label key={action.id} className="flex items-start gap-3 cursor-pointer group">
            <div className="relative flex-shrink-0 mt-0.5">
              <input
                type="checkbox"
                className="sr-only"
                checked={!!checked[action.id]}
                onChange={() => onToggle(action.id)}
              />
              <div
                className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all ${
                  checked[action.id]
                    ? "bg-indigo-600 border-indigo-600"
                    : "bg-white border-slate-300 group-hover:border-indigo-400"
                }`}
              >
                {checked[action.id] && (
                  <svg className="w-3 h-3 text-white" viewBox="0 0 12 12" fill="none">
                    <path
                      d="M2 6l3 3 5-5"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                )}
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <p
                className={`text-sm font-medium transition-colors ${
                  checked[action.id] ? "line-through text-slate-400" : "text-slate-800"
                }`}
              >
                {action.label}
              </p>
              <div className="flex flex-wrap items-center gap-2 mt-1.5">
                <PriorityBadge priority={action.priority} />
                <span className="text-[11px] text-slate-500">{action.team}</span>
                <span className="text-[11px] text-slate-400">·</span>
                <span className="text-[11px] text-slate-500 italic">{action.kpi}</span>
              </div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function PlanPage() {
  const allActionIds = HORIZONS.flatMap((h) => h.actions.map((a) => a.id));
  const initial = Object.fromEntries(allActionIds.map((id) => [id, false]));
  const [checked, setChecked] = useState<Record<string, boolean>>(initial);

  const toggle = (id: string) => setChecked((prev) => ({ ...prev, [id]: !prev[id] }));

  const totalActions = allActionIds.length;
  const doneActions = allActionIds.filter((id) => checked[id]).length;

  return (
    <div className="space-y-10 pb-16">

      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <div className="rounded-2xl bg-gradient-to-br from-indigo-950 via-indigo-900 to-violet-900 px-8 py-10 shadow-xl">
        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-800/60 border border-indigo-700/50 mb-5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-300 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-400" />
              </span>
              <span className="text-xs font-semibold text-indigo-200 tracking-wide">
                Généré par IA · Basé sur 847 signaux
              </span>
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white leading-tight mb-3">
              Plan de Conquête Stratégique
            </h1>
            <p className="text-indigo-200 text-base md:text-lg leading-relaxed">
              Votre feuille de route pour capturer{" "}
              <span className="text-white font-bold">12% de parts de marché supplémentaires</span>{" "}
              d&apos;ici 18 mois
            </p>
          </div>
          <div className="flex-shrink-0">
            <button
              type="button"
              onClick={() => window.print()}
              className="inline-flex items-center gap-2.5 px-5 py-3 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white text-sm font-semibold transition-all shadow-lg backdrop-blur-sm"
            >
              <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path
                  fillRule="evenodd"
                  d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
              Télécharger le plan complet (PDF)
            </button>
          </div>
        </div>
      </div>

      {/* ── Section 1 : Diagnostic ─────────────────────────────────────────── */}
      <section>
        <h2 className="text-lg font-bold text-slate-800 mb-4">Diagnostic de situation</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">

          {/* Position actuelle */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-indigo-100 flex items-center justify-center mb-4">
              <svg className="w-5 h-5 text-indigo-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clipRule="evenodd" />
              </svg>
            </div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Position actuelle</p>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">Parts de marché</span>
                <span className="text-sm font-bold text-slate-900">4.2%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">ARR actuel</span>
                <span className="text-sm font-bold text-slate-900">3.4M€</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">NPS</span>
                <span className="text-sm font-bold text-emerald-600">+62</span>
              </div>
            </div>
          </div>

          {/* Opportunité identifiée */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center mb-4">
              <svg className="w-5 h-5 text-emerald-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
              </svg>
            </div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Opportunité identifiée</p>
            <div className="space-y-2">
              <div className="flex justify-between items-start gap-2">
                <span className="text-sm text-slate-600">Segments sous-adressés</span>
                <span className="text-sm font-bold text-slate-900">ETI + Public</span>
              </div>
              <div className="flex justify-between items-start gap-2">
                <span className="text-sm text-slate-600">Concurrent en difficulté</span>
                <span className="text-sm font-bold text-amber-600">Oracle CX</span>
              </div>
              <div className="flex justify-between items-start gap-2">
                <span className="text-sm text-slate-600">ARR atteignable</span>
                <span className="text-sm font-bold text-emerald-600">+7.5M€</span>
              </div>
            </div>
          </div>

          {/* Menaces imminentes */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-red-100 flex items-center justify-center mb-4">
              <svg className="w-5 h-5 text-red-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Menaces imminentes</p>
            <div className="space-y-2">
              <div className="flex justify-between items-start gap-2">
                <span className="text-sm text-slate-600">Signaux levée de fonds</span>
                <span className="text-sm font-bold text-red-600">3 concurrents</span>
              </div>
              <div className="flex justify-between items-start gap-2">
                <span className="text-sm text-slate-600">Nouveaux entrants US</span>
                <span className="text-sm font-bold text-amber-600">2 actifs</span>
              </div>
              <div className="flex justify-between items-start gap-2">
                <span className="text-sm text-slate-600">Churn risque estimé</span>
                <span className="text-sm font-bold text-slate-900">-180k€ ARR</span>
              </div>
            </div>
          </div>

          {/* Fenêtre d'action */}
          <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl border border-amber-200 p-5 shadow-sm">
            <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center mb-4">
              <svg className="w-5 h-5 text-amber-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
              </svg>
            </div>
            <p className="text-xs font-semibold text-amber-700 uppercase tracking-wide mb-3">Fenêtre d&apos;action</p>
            <p className="text-3xl font-extrabold text-amber-900 mb-1">18 mois</p>
            <p className="text-sm text-amber-700 leading-snug">
              avant que le marché se consolide autour de 3 acteurs dominants
            </p>
          </div>

        </div>
      </section>

      {/* ── Section 2 : Les 3 axes ──────────────────────────────────────────── */}
      <section>
        <h2 className="text-lg font-bold text-slate-800 mb-4">Les 3 axes de conquête</h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {AXES.map((axis) => (
            <div
              key={axis.id}
              className={`bg-white rounded-2xl border ${axis.accentBorder} shadow-sm overflow-hidden flex flex-col`}
            >
              <div className={`${axis.accentBg} border-b ${axis.accentBorder} px-5 py-4`}>
                <div className="flex items-start justify-between gap-3 mb-2">
                  <span className={`text-xs font-bold ${axis.accentText} uppercase tracking-wide`}>
                    Axe {axis.id}
                  </span>
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold border ${axis.competitorColor}`}>
                    vs {axis.competitor}
                  </span>
                </div>
                <h3 className="text-sm font-bold text-slate-900 leading-snug mb-1">
                  {axis.name.replace(`Axe ${axis.id} — `, "")}
                </h3>
                <p className={`text-xl font-extrabold ${axis.accentText}`}>{axis.objective}</p>
              </div>

              <div className="px-5 py-4 space-y-3 flex-1">
                <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide mb-2">Stratégie</p>
                {axis.strategy.map((s, i) => (
                  <div key={i} className="flex items-start gap-2.5">
                    <div
                      className={`flex-shrink-0 w-5 h-5 rounded-full ${axis.accentBadgeBg} border ${axis.accentBadgeBorder} flex items-center justify-center mt-0.5`}
                    >
                      <span className={`text-[10px] font-bold ${axis.accentText}`}>{i + 1}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-slate-700 leading-snug">{s.action}</p>
                      <p className={`text-[10px] font-semibold ${axis.accentText} mt-0.5`}>{s.owner}</p>
                    </div>
                  </div>
                ))}

                <ProgressMilestones milestones={axis.milestones} />

                <div className="flex items-center justify-between mt-2 pt-3 border-t border-slate-100">
                  <span className="text-xs text-slate-500">Probabilité de succès</span>
                  <span
                    className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold border ${axis.successColor}`}
                  >
                    {axis.successRate}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Section 3 : Plan 30/60/90 ──────────────────────────────────────── */}
      <section>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
          <h2 className="text-lg font-bold text-slate-800">Plan d&apos;actions 30 / 60 / 90 jours</h2>
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <div className="w-4 h-4 rounded-full bg-indigo-600 flex items-center justify-center">
              <svg className="w-2.5 h-2.5 text-white" viewBox="0 0 12 12" fill="none">
                <path
                  d="M2 6l3 3 5-5"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <span>
              {doneActions} / {totalActions} actions complétées
            </span>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {HORIZONS.map((horizon) => (
            <ChecklistSection
              key={horizon.label}
              horizon={horizon}
              checked={checked}
              onToggle={toggle}
            />
          ))}
        </div>
      </section>

      {/* ── Section 4 : Budget ─────────────────────────────────────────────── */}
      <section>
        <h2 className="text-lg font-bold text-slate-800 mb-4">Budget et ressources estimés</h2>
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="text-left px-5 py-3.5 font-semibold text-slate-600 text-xs uppercase tracking-wide">
                    Axe stratégique
                  </th>
                  <th className="text-right px-5 py-3.5 font-semibold text-slate-600 text-xs uppercase tracking-wide">
                    Investissement
                  </th>
                  <th className="text-right px-5 py-3.5 font-semibold text-slate-600 text-xs uppercase tracking-wide">
                    ROI projeté
                  </th>
                  <th className="text-right px-5 py-3.5 font-semibold text-slate-600 text-xs uppercase tracking-wide">
                    Délai de retour
                  </th>
                </tr>
              </thead>
              <tbody>
                {BUDGET_ROWS.map((row, i) => (
                  <tr
                    key={i}
                    className={`border-b border-slate-100 last:border-0 ${
                      row.isTotal
                        ? "bg-indigo-50"
                        : "hover:bg-slate-50 transition-colors"
                    }`}
                  >
                    <td
                      className={`px-5 py-3.5 ${
                        row.isTotal ? "text-indigo-800 font-bold" : "text-slate-800"
                      }`}
                    >
                      {row.axe}
                    </td>
                    <td
                      className={`px-5 py-3.5 text-right font-semibold tabular-nums ${
                        row.isTotal ? "text-indigo-800 font-bold" : "text-slate-700"
                      }`}
                    >
                      {row.investissement}
                    </td>
                    <td className={`px-5 py-3.5 text-right font-bold tabular-nums ${row.roiColor}`}>
                      {row.roi}
                    </td>
                    <td
                      className={`px-5 py-3.5 text-right ${
                        row.isTotal ? "text-indigo-800 font-bold" : "text-slate-500"
                      }`}
                    >
                      {row.delai}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ── Section 5 : Risques ────────────────────────────────────────────── */}
      <section>
        <h2 className="text-lg font-bold text-slate-800 mb-4">Risques et mitigations</h2>
        <div className="space-y-4">
          {RISKS.map((risk, i) => (
            <div key={i} className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
              <div className="px-5 py-4 border-b border-slate-100 flex items-start justify-between gap-3">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center mt-0.5">
                    <svg className="w-4 h-4 text-slate-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">{risk.title}</p>
                    <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{risk.description}</p>
                  </div>
                </div>
                <span
                  className={`flex-shrink-0 inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold border ${risk.levelColor}`}
                >
                  {risk.level}
                </span>
              </div>
              <div className="px-5 py-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wide mb-1.5">
                    Mitigation
                  </p>
                  <p className="text-xs text-slate-700 leading-relaxed">{risk.mitigation}</p>
                </div>
                <div>
                  <p className="text-[11px] font-bold text-amber-600 uppercase tracking-wide mb-1.5">
                    Plan B
                  </p>
                  <p className="text-xs text-slate-700 leading-relaxed">{risk.planB}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
}

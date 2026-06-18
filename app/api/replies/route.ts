import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type ObjectionType = "price" | "trust" | "timing" | "competitor" | "technical" | "none";
type Timeline = "immédiat" | "sous_48h" | "cette_semaine" | "dans_un_mois" | "indéfini";
type Priority = "urgent" | "high" | "normal" | "low";

interface ClassificationResult {
  objection_type: ObjectionType;
  timeline: Timeline;
  buying_signal: number;
  competitor_mentioned: boolean;
  objection_keywords: string[];
  buying_keywords: string[];
  next_action: string;
  priority: Priority;
}

interface ReplyRecord {
  reply_id: string;
  prospect_id: string;
  company_name: string;
  sector: string;
  email_subject: string;
  email_snippet: string;
  received_at: string;
  classification: ClassificationResult;
}

interface Summary {
  total: number;
  urgent: number;
  high: number;
  normal: number;
  low: number;
  avg_buying_signal: number;
  objection_distribution: Record<string, number>;
  competitor_mentions: number;
  timeline_distribution: Record<string, number>;
}

// Keyword-based classifier mirroring Python logic
const PRICE_KW = ["trop cher", "budget", "prix", "coût", "tarif", "devis", "€"];
const TRUST_KW = ["arnaque", "méfiant", "référence", "avis", "preuve", "garanti", "fiable", "sérieux", "confiance"];
const TIMING_KW = ["pas maintenant", "plus tard", "dans quelques mois", "l'année prochaine", "pas le bon moment", "on verra"];
const COMPETITOR_KW = ["prestataire", "quelqu'un d'autre", "déjà un", "fidèle à", "freelance", "wix", "wordpress", "shopify"];
const TECHNICAL_KW = ["trop compliqué", "je n'y connais rien", "technique", "difficile", "besoin d'aide", "accompagnement"];
const BUYING_KW = ["intéressé", "quand", "commencer", "d'accord", "contrat", "signature", "rendez-vous", "envoyer", "proposez"];

function detectObjection(text: string): { type: ObjectionType; keywords: string[] } {
  const t = text.toLowerCase();
  const checks: [ObjectionType, string[]][] = [
    ["trust", TRUST_KW],
    ["price", PRICE_KW],
    ["competitor", COMPETITOR_KW],
    ["technical", TECHNICAL_KW],
    ["timing", TIMING_KW],
  ];
  let bestType: ObjectionType = "none";
  let bestKws: string[] = [];
  for (const [type, kws] of checks) {
    const matched = kws.filter((k) => t.includes(k));
    if (matched.length > bestKws.length) {
      bestType = type;
      bestKws = matched;
    }
  }
  return { type: bestType, keywords: bestKws };
}

function detectTimeline(text: string): Timeline {
  const t = text.toLowerCase();
  if (["aujourd'hui", "maintenant", "urgent", "immédiatement", "dès que"].some((k) => t.includes(k))) return "immédiat";
  if (["demain", "sous 48h", "lundi", "mardi", "mercredi", "jeudi", "vendredi"].some((k) => t.includes(k))) return "sous_48h";
  if (["cette semaine", "la semaine prochaine", "fin de semaine"].some((k) => t.includes(k))) return "cette_semaine";
  if (["le mois prochain", "dans un mois", "prochain trimestre"].some((k) => t.includes(k))) return "dans_un_mois";
  return "indéfini";
}

function detectBuying(text: string): { signal: number; keywords: string[] } {
  const t = text.toLowerCase();
  const matched = BUYING_KW.filter((k) => t.includes(k));
  return { signal: Math.min(1.0, matched.length * 0.25), keywords: matched };
}

function computePriority(buying: number, timeline: Timeline): Priority {
  if (timeline === "immédiat" && buying >= 0.5) return "urgent";
  if (buying >= 0.5 || timeline === "immédiat" || timeline === "sous_48h") return "high";
  if (timeline === "cette_semaine") return "normal";
  return "low";
}

const NEXT_ACTIONS: Record<string, Record<string, string>> = {
  price: {
    "immédiat": "Envoyer offre groupée avec réduction 15% — sous 1h",
    "sous_48h": "Envoyer ROI calculator + étude de cas secteur",
    "cette_semaine": "Proposer appel 15 min pour budget personnalisé",
    "dans_un_mois": "Nurturing : 3 emails ROI sur 10 jours",
    "indéfini": "Relance J+7 avec témoignage client similaire",
  },
  trust: {
    "immédiat": "Envoyer 3 études de cas + certifications",
    "sous_48h": "Proposer démo gratuite 30 min",
    "cette_semaine": "Envoyer portfolio + appel référence client",
    "dans_un_mois": "Séquence nurturing confiance (5 emails)",
    "indéfini": "Agent 3.2 : email garantie satisfait ou remboursé",
  },
  timing: {
    "immédiat": "Demander date exacte et bloquer agenda",
    "sous_48h": "Envoyer rappel et proposition calendrier",
    "cette_semaine": "Proposer appel découverte flexible",
    "dans_un_mois": "Email de nurturing mensuel",
    "indéfini": "Relance automatique dans 30 jours",
  },
  competitor: {
    "immédiat": "Envoyer comparatif concurrentiel + avantages uniques",
    "sous_48h": "Agent 3.1 : présentation différenciation",
    "cette_semaine": "Proposer audit gratuit vs solution actuelle",
    "dans_un_mois": "Nurturing : résultats clients ayant switché",
    "indéfini": "Email de benchmark — positionnement marché",
  },
  technical: {
    "immédiat": "Planifier onboarding accompagné dès aujourd'hui",
    "sous_48h": "Envoyer guide démarrage rapide + FAQ",
    "cette_semaine": "Proposer démo personnalisée avec technicien",
    "dans_un_mois": "Email formation + vidéo tutoriel",
    "indéfini": "Séquence éducative 3 emails",
  },
  none: {
    "immédiat": "Appel de closing immédiat — prospect chaud",
    "sous_48h": "Envoi contrat et lien de paiement",
    "cette_semaine": "Proposition de rendez-vous signature",
    "dans_un_mois": "Email récapitulatif offre + deadline",
    "indéfini": "Relance J+4 — Agent 3.5",
  },
};

function classify(text: string): ClassificationResult {
  const { type: objType, keywords: objKws } = detectObjection(text);
  const timeline = detectTimeline(text);
  const { signal, keywords: buyKws } = detectBuying(text);
  const competitor = COMPETITOR_KW.some((k) => text.toLowerCase().includes(k));
  const priority = computePriority(signal, timeline);
  const next_action = NEXT_ACTIONS[objType]?.[timeline] ?? NEXT_ACTIONS.none.indéfini;
  return {
    objection_type: objType,
    timeline,
    buying_signal: Math.round(signal * 1000) / 1000,
    competitor_mentioned: competitor,
    objection_keywords: objKws,
    buying_keywords: buyKws,
    next_action,
    priority,
  };
}

function mk(
  id: string,
  pid: string,
  company: string,
  sector: string,
  subject: string,
  snippet: string,
  daysAgo: number
): ReplyRecord {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  return {
    reply_id: id,
    prospect_id: pid,
    company_name: company,
    sector,
    email_subject: subject,
    email_snippet: snippet,
    received_at: date.toISOString(),
    classification: classify(snippet),
  };
}

const MOCK_REPLIES: ReplyRecord[] = [
  mk("r001", "p001", "Plomberie Martin", "artisan",
    "RE: Votre site web",
    "Bonjour, je suis intéressé, quand peut-on commencer ? D'accord pour le contrat, envoyez-moi les détails.",
    0),
  mk("r002", "p002", "Électricité Dubois", "artisan",
    "RE: Proposition commerciale",
    "Votre prix est trop cher pour notre budget actuel. Pouvez-vous faire un geste ?",
    1),
  mk("r003", "p003", "SAS Rénovation Plus", "PME",
    "Votre offre",
    "Nous travaillons déjà avec quelqu'un d'autre, un freelance, et nous en sommes satisfaits.",
    1),
  mk("r004", "p004", "Menuiserie Bernard", "artisan",
    "RE: Site web artisan",
    "Je n'y connais rien en technique, c'est trop compliqué pour moi. Vous proposez de l'accompagnement ?",
    2),
  mk("r005", "p005", "Couverture Lefebvre", "artisan",
    "Réponse",
    "Pas maintenant, peut-être plus tard. On verra dans quelques mois quand on sera moins occupés.",
    2),
  mk("r006", "p006", "Chauffage Moreau", "artisan",
    "RE: Devis site vitrine",
    "Je ne vous connais pas. J'ai besoin de références et de preuves de votre sérieux avant d'aller plus loin.",
    3),
  mk("r007", "p007", "BTP Solutions", "PME",
    "URGENT — Besoin d'un site",
    "Urgent ! J'ai besoin de cela immédiatement, dès que possible. Je suis disponible aujourd'hui pour en discuter.",
    0),
  mk("r008", "p008", "Carrelage Petit", "artisan",
    "RE: Votre email",
    "Pouvez-vous m'envoyer plus d'informations sur votre offre ? Je suis curieux de comprendre comment ça fonctionne.",
    3),
  mk("r009", "p009", "Peinture Durand", "artisan",
    "RE: Proposition",
    "Le tarif nous convient, quand pouvez-vous commencer ? Proposez-nous un rendez-vous cette semaine.",
    4),
  mk("r010", "p010", "Maçonnerie Roux", "artisan",
    "Devis reçu",
    "Nous avons reçu votre devis. Le coût semble un peu élevé par rapport à nos attentes budgétaires.",
    5),
  mk("r011", "p011", "Isolation Thomas", "artisan",
    "RE: Contact",
    "L'année prochaine ce sera plus pertinent pour nous. Recontactez-moi en janvier.",
    6),
  mk("r012", "p012", "Menuiserie Garnier", "artisan",
    "Réponse à votre email",
    "D'accord, envoyez-moi le contrat. Je suis prêt à commencer dès que possible.",
    7),
];

function buildSummary(replies: ReplyRecord[]): Summary {
  const objDist: Record<string, number> = {};
  const timeDist: Record<string, number> = {};
  const priorityCounts: Record<Priority, number> = { urgent: 0, high: 0, normal: 0, low: 0 };
  let totalSignal = 0;
  let competitorCount = 0;

  for (const r of replies) {
    const c = r.classification;
    objDist[c.objection_type] = (objDist[c.objection_type] ?? 0) + 1;
    timeDist[c.timeline] = (timeDist[c.timeline] ?? 0) + 1;
    priorityCounts[c.priority]++;
    totalSignal += c.buying_signal;
    if (c.competitor_mentioned) competitorCount++;
  }

  return {
    total: replies.length,
    urgent: priorityCounts.urgent,
    high: priorityCounts.high,
    normal: priorityCounts.normal,
    low: priorityCounts.low,
    avg_buying_signal: replies.length
      ? Math.round((totalSignal / replies.length) * 1000) / 1000
      : 0,
    objection_distribution: objDist,
    competitor_mentions: competitorCount,
    timeline_distribution: timeDist,
  };
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const objection = searchParams.get("objection");
  const priority = searchParams.get("priority");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/replies`);
      searchParams.forEach((v, k) => url.searchParams.set(k, v));
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {
      // fall through to mock
    }
  }

  let replies = [...MOCK_REPLIES].sort(
    (a, b) => new Date(b.received_at).getTime() - new Date(a.received_at).getTime()
  );

  if (objection) replies = replies.filter((r) => r.classification.objection_type === objection);
  if (priority) replies = replies.filter((r) => r.classification.priority === priority);

  return NextResponse.json({ replies, summary: buildSummary(MOCK_REPLIES) });
}

export async function POST(request: Request) {
  if (SWARM_API_URL) {
    try {
      const body = await request.json();
      const res = await fetch(`${SWARM_API_URL}/replies/classify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        cache: "no-store",
      });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {
      // fall through
    }
  }

  const body = await request.json().catch(() => ({}));
  const text: string = body.text ?? "";
  if (!text) return NextResponse.json({ error: "text required" }, { status: 400 });
  return NextResponse.json({ classification: classify(text) });
}

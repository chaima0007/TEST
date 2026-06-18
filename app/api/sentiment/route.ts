import { NextResponse } from "next/server";

type Sentiment = "Positif" | "Curieux" | "Sceptique" | "Méfiant" | "Négatif" | "Pressé" | "Fantôme";
type AgentId = "3.5" | "3.1" | "3.2" | "3.3" | "3.7";

interface SentimentEntry {
  id: string;
  text: string;
  sentiment: Sentiment;
  agent_id: AgentId;
  confidence: number;
  keywords: string[];
  sector: string;
  timestamp: string;
}

const ROUTING: Record<Sentiment, AgentId> = {
  Positif: "3.5",
  Curieux: "3.5",
  Sceptique: "3.1",
  Méfiant: "3.2",
  Négatif: "3.3",
  Fantôme: "3.7",
  Pressé: "3.5",
};

function ts(hoursAgo: number): string {
  return new Date(Date.now() - hoursAgo * 3600 * 1000).toISOString();
}

const MOCK_ENTRIES: SentimentEntry[] = [
  {
    id: "sent-001",
    text: "Super, ça m'intéresse vraiment ! Quand est-ce qu'on peut commencer ?",
    sentiment: "Positif",
    agent_id: "3.5",
    confidence: 0.92,
    keywords: ["intéressé", "commencer"],
    sector: "artisan",
    timestamp: ts(2),
  },
  {
    id: "sent-002",
    text: "Comment ça fonctionne exactement ? Vous pouvez m'expliquer un peu plus ?",
    sentiment: "Curieux",
    agent_id: "3.5",
    confidence: 0.84,
    keywords: ["comment", "expliquer"],
    sector: "restaurant",
    timestamp: ts(4),
  },
  {
    id: "sent-003",
    text: "Je suis pas vraiment convaincu, vous avez des preuves que ça marche ?",
    sentiment: "Sceptique",
    agent_id: "3.1",
    confidence: 0.78,
    keywords: ["pas convaincu", "preuve"],
    sector: "PME",
    timestamp: ts(6),
  },
  {
    id: "sent-004",
    text: "C'est quoi encore ce spam ? Désabonnez-moi immédiatement.",
    sentiment: "Méfiant",
    agent_id: "3.2",
    confidence: 0.95,
    keywords: ["spam", "désabonner"],
    sector: "comptable",
    timestamp: ts(8),
  },
  {
    id: "sent-005",
    text: "Non merci, pas intéressé du tout, ça ne correspond pas à nos besoins.",
    sentiment: "Négatif",
    agent_id: "3.3",
    confidence: 0.89,
    keywords: ["non", "pas intéressé"],
    sector: "médecin",
    timestamp: ts(10),
  },
  {
    id: "sent-006",
    text: "Il me faut ça urgent, on a un client qui attend, appelez-moi maintenant.",
    sentiment: "Pressé",
    agent_id: "3.5",
    confidence: 0.91,
    keywords: ["urgent", "maintenant"],
    sector: "artisan",
    timestamp: ts(12),
  },
  {
    id: "sent-007",
    text: "Ok parfait, envoyez-moi le contrat et on signe cette semaine.",
    sentiment: "Positif",
    agent_id: "3.5",
    confidence: 0.94,
    keywords: ["ok", "parfait"],
    sector: "restaurant",
    timestamp: ts(14),
  },
  {
    id: "sent-008",
    text: "Pourquoi vous me contactez ? C'est quoi votre offre exactement ?",
    sentiment: "Curieux",
    agent_id: "3.5",
    confidence: 0.71,
    keywords: ["pourquoi"],
    sector: "PME",
    timestamp: ts(18),
  },
  {
    id: "sent-009",
    text: "Vous avez des résultats garantis ? Montrez-moi des exemples concrets.",
    sentiment: "Sceptique",
    agent_id: "3.1",
    confidence: 0.76,
    keywords: ["résultat", "garanti"],
    sector: "avocat",
    timestamp: ts(22),
  },
  {
    id: "sent-010",
    text: "Arnaque ! Je n'ai jamais demandé à être contacté, c'est illégal.",
    sentiment: "Méfiant",
    agent_id: "3.2",
    confidence: 0.93,
    keywords: ["arnaque", "méfiant"],
    sector: "libéral",
    timestamp: ts(26),
  },
  {
    id: "sent-011",
    text: "Trop cher pour ce que c'est, aucun intérêt pour nous.",
    sentiment: "Négatif",
    agent_id: "3.3",
    confidence: 0.82,
    keywords: ["trop cher", "aucun intérêt"],
    sector: "artisan",
    timestamp: ts(30),
  },
  {
    id: "sent-012",
    text: "Oui, ça m'intéresse. Vous pouvez me recontacter demain matin ?",
    sentiment: "Positif",
    agent_id: "3.5",
    confidence: 0.88,
    keywords: ["oui", "intéressé"],
    sector: "coiffeur",
    timestamp: ts(34),
  },
  {
    id: "sent-013",
    text: "Je voudrais comprendre comment vous calculez le retour sur investissement.",
    sentiment: "Curieux",
    agent_id: "3.5",
    confidence: 0.79,
    keywords: ["comprendre", "comment"],
    sector: "consultant",
    timestamp: ts(38),
  },
  {
    id: "sent-014",
    text: "Vite, j'ai besoin d'une réponse aujourd'hui, mon associé part en déplacement.",
    sentiment: "Pressé",
    agent_id: "3.5",
    confidence: 0.87,
    keywords: ["vite", "aujourd'hui"],
    sector: "PME",
    timestamp: ts(42),
  },
  {
    id: "sent-015",
    text: "Top, exactement ce qu'il nous faut. On peut commencer dès la semaine prochaine ?",
    sentiment: "Positif",
    agent_id: "3.5",
    confidence: 0.90,
    keywords: ["top", "commencer"],
    sector: "restaurant",
    timestamp: ts(48),
  },
  {
    id: "sent-016",
    text: "Vraiment ? Vous êtes sûr que ça fonctionne pour les petits commerces ?",
    sentiment: "Sceptique",
    agent_id: "3.1",
    confidence: 0.65,
    keywords: ["vraiment"],
    sector: "commerce",
    timestamp: ts(52),
  },
  {
    id: "sent-017",
    text: "Je ne réponds plus à ce genre de sollicitation, stop les messages.",
    sentiment: "Méfiant",
    agent_id: "3.2",
    confidence: 0.86,
    keywords: ["stop", "méfiant"],
    sector: "médecin",
    timestamp: ts(56),
  },
  {
    id: "sent-018",
    text: "D'accord pour un essai, envoyez-moi plus d'informations sur les tarifs.",
    sentiment: "Positif",
    agent_id: "3.5",
    confidence: 0.83,
    keywords: ["d'accord"],
    sector: "kinésithérapeute",
    timestamp: ts(60),
  },
  {
    id: "sent-019",
    text: "Plus d'infos sur la partie technique ? Je veux comprendre avant de m'engager.",
    sentiment: "Curieux",
    agent_id: "3.5",
    confidence: 0.74,
    keywords: ["plus d'info", "comprendre"],
    sector: "ingénieur",
    timestamp: ts(64),
  },
  {
    id: "sent-020",
    text: "Rapidement svp, on a une réunion ce soir et j'ai besoin de votre offre.",
    sentiment: "Pressé",
    agent_id: "3.5",
    confidence: 0.85,
    keywords: ["rapidement"],
    sector: "directeur",
    timestamp: ts(70),
  },
];

function buildSummary(entries: SentimentEntry[]) {
  const by_sentiment: Record<string, number> = {};
  const by_agent: Record<string, number> = {};
  let conf_sum = 0;
  let positive_count = 0;

  for (const e of entries) {
    by_sentiment[e.sentiment] = (by_sentiment[e.sentiment] ?? 0) + 1;
    by_agent[e.agent_id] = (by_agent[e.agent_id] ?? 0) + 1;
    conf_sum += e.confidence;
    if (e.sentiment === "Positif" || e.sentiment === "Pressé") positive_count++;
  }

  return {
    total: entries.length,
    by_sentiment,
    by_agent,
    avg_confidence: Math.round((conf_sum / entries.length) * 100) / 100,
    positive_rate_pct: Math.round((positive_count / entries.length) * 1000) / 10,
  };
}

const POSITIVE_KW = ["intéressé", "super", "parfait", "excellent", "d'accord", "ok", "oui", "top", "commencer"];
const CURIOUS_KW = ["comment", "pourquoi", "expliquer", "plus d'info", "curieux", "comprendre", "question"];
const SKEPTICAL_KW = ["prouve", "preuve", "résultat", "garanti", "vraiment", "pas convaincu"];
const SUSPICIOUS_KW = ["arnaque", "méfiant", "spam", "stop", "désabonner"];
const NEGATIVE_KW = ["non", "pas intéressé", "trop cher", "aucun intérêt"];
const URGENT_KW = ["urgent", "rapidement", "vite", "maintenant", "aujourd'hui"];

function classifyText(text: string, sector?: string): SentimentEntry {
  const t = text.toLowerCase();

  function matches(kws: string[]): string[] {
    return kws.filter((k) => t.includes(k));
  }

  const suspMatches = matches(SUSPICIOUS_KW);
  const negMatches = matches(NEGATIVE_KW);
  const urgMatches = matches(URGENT_KW);
  const posMatches = matches(POSITIVE_KW);
  const curMatches = matches(CURIOUS_KW);
  const skeMatches = matches(SKEPTICAL_KW);

  let sentiment: Sentiment;
  let keywords: string[];
  let confidence: number;

  if (suspMatches.length > 0) {
    sentiment = "Méfiant";
    keywords = suspMatches;
    confidence = 0.85 + Math.random() * 0.1;
  } else if (negMatches.length > 0) {
    sentiment = "Négatif";
    keywords = negMatches;
    confidence = 0.75 + Math.random() * 0.15;
  } else if (urgMatches.length > 0) {
    sentiment = "Pressé";
    keywords = urgMatches;
    confidence = 0.78 + Math.random() * 0.15;
  } else if (posMatches.length > 0) {
    sentiment = "Positif";
    keywords = posMatches;
    confidence = 0.8 + Math.random() * 0.15;
  } else if (skeMatches.length > 0) {
    sentiment = "Sceptique";
    keywords = skeMatches;
    confidence = 0.65 + Math.random() * 0.2;
  } else if (curMatches.length > 0) {
    sentiment = "Curieux";
    keywords = curMatches;
    confidence = 0.65 + Math.random() * 0.2;
  } else {
    sentiment = "Curieux";
    keywords = [];
    confidence = 0.4 + Math.random() * 0.2;
  }

  return {
    id: `sent-live-${Date.now()}`,
    text: text.slice(0, 80),
    sentiment,
    agent_id: ROUTING[sentiment],
    confidence: Math.round(confidence * 100) / 100,
    keywords,
    sector: sector ?? "inconnu",
    timestamp: new Date().toISOString(),
  };
}

export async function GET() {
  return NextResponse.json({
    entries: MOCK_ENTRIES,
    summary: buildSummary(MOCK_ENTRIES),
  });
}

export async function POST(request: Request) {
  const body = await request.json();
  const { text, sector } = body as { text: string; sector?: string };
  if (!text || typeof text !== "string") {
    return NextResponse.json({ error: "text required" }, { status: 400 });
  }
  const entry = classifyText(text, sector);
  return NextResponse.json(entry);
}

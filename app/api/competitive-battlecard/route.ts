import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockBattlecards = [
  {
    competitor_id: "cb_001",
    competitor_name: "SalesForce Enterprise",
    market_position: "leader",
    threat_score: 82.0,
    threat_level: "critical",
    win_probability: "weak",
    battlecard_action: "escalate",
    executive_summary:
      "SalesForce Enterprise (Leader) représente une menace critique avec un taux de victoire historique de 55% contre nous. Action recommandée : escalate. Parité fonctionnelle à 75% — différenciation sur support, intégrations et roadmap.",
    our_advantages: [
      "Support & CS supérieur (9.2/10 vs 6.5/10)",
      "3 fonctionnalités exclusives non réplicables",
      "Écosystème d'intégrations supérieur (4 intégrations clés)",
      "IA native embarquée — non disponible chez SF Enterprise",
      "Déploiement 4x plus rapide — time-to-value réduit",
      "Pricing prévisible — pas de coûts cachés add-on",
    ],
    their_advantages: [
      "Notoriété marché et base installée importante",
      "Parité fonctionnelle élevée (75%)",
      "Financement récent — guerre des prix possible",
    ],
    counter_tactics: [
      "Qualifier le budget avant tout — ne pas s'engager sur le prix sans valeur",
      "Présenter le TCO complet — coût de migration + support inclus",
      "Démonstration live des fonctionnalités différenciantes — éviter la comparaison liste",
      "Mettre en avant la roadmap — innovation en avance sur la concurrence",
      "Impliquer un exec sponsor — mobiliser C-level si deal à risque",
      "Référence client sectorielle — prouver la valeur par les pairs",
      "Exploiter les faiblesses connues : complexité déploiement, coûts add-on",
      "Proposer une période d'essai ou POC — réduire le risque perçu",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez SalesForce Enterprise. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Nos clients venant de SalesForce mentionnent souvent : complexité déploiement. Comment gérez-vous ce risque ? »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. Voici ce que nos clients mesurent... »",
    ],
    objection_responses: [
      "Objection prix : « Notre prix reflète un ROI documenté. Sur 3 ans, nos clients économisent en moyenne X% grâce à [valeur]. »",
      "Objection fonctionnalités : « SalesForce Enterprise couvre 75% de nos features — mais les 25% restants sont précisément ce qui génère le ROI que vous cherchez. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [
      "Taux de victoire contre nous élevé (55%) — analyse des deals perdus requise",
      "Présent dans 12 deals actifs — risque pipeline systémique",
      "Nouveau financement — investissements produit/marketing attendus",
      "Parité fonctionnelle critique — différenciation urgente requise",
    ],
  },
  {
    competitor_id: "cb_002",
    competitor_name: "HubSpot Pro",
    market_position: "challenger",
    threat_score: 68.0,
    threat_level: "high",
    win_probability: "moderate",
    battlecard_action: "differentiate",
    executive_summary:
      "HubSpot Pro (Challenger) représente une menace high avec un taux de victoire historique de 38% contre nous. Action recommandée : differentiate. Parité fonctionnelle à 65% — différenciation sur support, intégrations et roadmap.",
    our_advantages: [
      "Support & CS supérieur (9.0/10 vs 7.0/10)",
      "3 fonctionnalités exclusives non réplicables",
      "Écosystème d'intégrations supérieur (3 intégrations clés)",
      "Analytics avancées enterprise-grade",
      "Conformité RGPD native — critique secteurs réglementés",
      "Multi-langues & multi-devises — expansion internationale facilitée",
    ],
    their_advantages: [
      "Prix 20% inférieur — pression tarifaire",
      "Notoriété marché et base installée importante",
      "Remises agressives jusqu'à 30%",
      "Nouveau produit récemment lancé — momentum marketing",
    ],
    counter_tactics: [
      "Qualifier le budget avant tout — ne pas s'engager sur le prix sans valeur",
      "Présenter le TCO complet — coût de migration + support inclus",
      "Démonstration live des fonctionnalités différenciantes — éviter la comparaison liste",
      "Impliquer un exec sponsor — mobiliser C-level si deal à risque",
      "Proposer une période d'essai ou POC — réduire le risque perçu",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez HubSpot Pro. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Un prix bas aujourd'hui peut coûter cher demain — regardons le TCO sur 3 ans ensemble. »",
      "« Un lancement récent = risque de maturité. Nos clients bénéficient de X années de stabilité. »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. »",
    ],
    objection_responses: [
      "Objection prix : « Notre prix reflète un ROI documenté. Sur 3 ans, nos clients économisent en moyenne X% grâce à [valeur]. »",
      "Objection fonctionnalités : « HubSpot Pro couvre 65% de nos features — mais les 35% restants sont précisément ce qui génère le ROI que vous cherchez. »",
      "Objection nouveau produit concurrent : « Un lancement récent = risque de maturité. Nos clients bénéficient de X années de stabilité et de roadmap prouvée. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [
      "Présent dans 8 deals actifs — risque pipeline systémique",
      "Baisse de prix récente — guerre des prix en cours",
    ],
  },
  {
    competitor_id: "cb_003",
    competitor_name: "Pipedrive CRM",
    market_position: "niche",
    threat_score: 52.0,
    threat_level: "high",
    win_probability: "moderate",
    battlecard_action: "counter",
    executive_summary:
      "Pipedrive CRM (Niche) représente une menace high avec un taux de victoire historique de 35% contre nous. Action recommandée : counter. Parité fonctionnelle à 55% — différenciation sur support, intégrations et roadmap.",
    our_advantages: [
      "Support & CS supérieur (8.8/10 vs 6.2/10)",
      "2 fonctionnalités exclusives",
      "Analytics enterprise et IA prédictive",
      "Scalabilité — adapté à la croissance enterprise",
    ],
    their_advantages: [
      "Prix 15% inférieur — pression tarifaire",
      "Remises agressives jusqu'à 25%",
    ],
    counter_tactics: [
      "Qualifier le budget avant tout — ne pas s'engager sur le prix sans valeur",
      "Présenter le TCO complet — coût de migration + support inclus",
      "Démonstration live des fonctionnalités différenciantes",
      "Proposer une période d'essai ou POC — réduire le risque perçu",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez Pipedrive CRM. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Un prix bas aujourd'hui peut coûter cher demain — regardons le TCO sur 3 ans ensemble. »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. »",
    ],
    objection_responses: [
      "Objection prix : « Notre prix reflète un ROI documenté. Sur 3 ans, nos clients économisent en moyenne X% grâce à [valeur]. »",
      "Objection fonctionnalités : « Pipedrive CRM couvre 55% de nos features — mais les 45% restants génèrent le ROI que vous cherchez. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [
      "Taux de victoire contre nous élevé (35%) — analyse des deals perdus requise",
    ],
  },
  {
    competitor_id: "cb_004",
    competitor_name: "Freshsales Suite",
    market_position: "challenger",
    threat_score: 45.0,
    threat_level: "medium",
    win_probability: "moderate",
    battlecard_action: "counter",
    executive_summary:
      "Freshsales Suite (Challenger) représente une menace medium avec un taux de victoire historique de 30% contre nous. Action recommandée : counter. Parité fonctionnelle à 52% — différenciation sur support, intégrations et ROI.",
    our_advantages: [
      "Support & CS supérieur (9.1/10 vs 7.0/10)",
      "Intégrations enterprise natives",
      "Conformité SOC2/ISO certifiée",
    ],
    their_advantages: [
      "Prix 10% inférieur — pression tarifaire",
    ],
    counter_tactics: [
      "Qualifier le budget avant tout — ne pas s'engager sur le prix sans valeur",
      "Démonstration live des fonctionnalités différenciantes",
      "Proposer une période d'essai ou POC",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez Freshsales Suite. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Un prix bas aujourd'hui peut coûter cher demain — regardons le TCO sur 3 ans ensemble. »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. »",
    ],
    objection_responses: [
      "Objection prix : « Notre prix reflète un ROI documenté. Sur 3 ans, nos clients économisent en moyenne X% grâce à [valeur]. »",
      "Objection fonctionnalités : « Freshsales couvre 52% de nos features — mais les 48% restants génèrent le ROI que vous cherchez. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [],
  },
  {
    competitor_id: "cb_005",
    competitor_name: "Zoho CRM Plus",
    market_position: "challenger",
    threat_score: 38.0,
    threat_level: "medium",
    win_probability: "moderate",
    battlecard_action: "counter",
    executive_summary:
      "Zoho CRM Plus (Challenger) représente une menace medium avec un taux de victoire historique de 28% contre nous. Action recommandée : counter. Parité fonctionnelle à 50% — différenciation sur support et ROI mesurable.",
    our_advantages: [
      "Support & CS supérieur (9.0/10 vs 5.8/10)",
      "Interface UX moderne — adoption utilisateur x2",
      "Onboarding guidé — time-to-value réduit",
    ],
    their_advantages: [
      "Prix 25% inférieur — pression tarifaire",
      "Remises agressives jusqu'à 40%",
    ],
    counter_tactics: [
      "Qualifier le budget avant tout",
      "Présenter le TCO complet — coût de migration + support inclus",
      "Proposer une période d'essai ou POC",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez Zoho CRM Plus. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Un prix bas aujourd'hui peut coûter cher demain — regardons le TCO sur 3 ans ensemble. »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. »",
    ],
    objection_responses: [
      "Objection prix : « Notre prix reflète un ROI documenté. Sur 3 ans, nos clients économisent en moyenne X% grâce à [valeur]. »",
      "Objection fonctionnalités : « Zoho couvre 50% de nos features — les 50% restants génèrent le ROI que vous cherchez. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [],
  },
  {
    competitor_id: "cb_006",
    competitor_name: "Monday Sales CRM",
    market_position: "emerging",
    threat_score: 22.0,
    threat_level: "low",
    win_probability: "strong",
    battlecard_action: "monitor",
    executive_summary:
      "Monday Sales CRM (Emerging) représente une menace low avec un taux de victoire historique de 18% contre nous. Action recommandée : monitor. Parité fonctionnelle à 35% — position favorable.",
    our_advantages: [
      "3 fonctionnalités exclusives non réplicables",
      "Maturité produit enterprise — vs solution émergente",
      "Références clients nombreuses et documentées",
    ],
    their_advantages: [],
    counter_tactics: [
      "Proposer une période d'essai ou POC — réduire le risque perçu",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez Monday Sales CRM. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. »",
    ],
    objection_responses: [
      "Objection fonctionnalités : « Monday couvre 35% de nos features — les 65% restants génèrent le ROI que vous cherchez. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [],
  },
  {
    competitor_id: "cb_007",
    competitor_name: "Close CRM",
    market_position: "niche",
    threat_score: 18.0,
    threat_level: "low",
    win_probability: "strong",
    battlecard_action: "monitor",
    executive_summary:
      "Close CRM (Niche) représente une menace low avec un taux de victoire historique de 15% contre nous. Action recommandée : monitor. Parité fonctionnelle à 30% — avantage compétitif fort.",
    our_advantages: [
      "Fonctionnalités enterprise que Close CRM ne propose pas",
      "Scalabilité — adapté aux grandes équipes commerciales",
      "Support enterprise dédié",
    ],
    their_advantages: [],
    counter_tactics: [
      "Proposer une période d'essai ou POC — réduire le risque perçu",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez Close CRM. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. »",
    ],
    objection_responses: [
      "Objection fonctionnalités : « Close CRM couvre 30% de nos features — les 70% restants génèrent le ROI que vous cherchez. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [],
  },
  {
    competitor_id: "cb_008",
    competitor_name: "Copper CRM",
    market_position: "niche",
    threat_score: 12.0,
    threat_level: "low",
    win_probability: "strong",
    battlecard_action: "monitor",
    executive_summary:
      "Copper CRM (Niche) représente une menace low avec un taux de victoire historique de 10% contre nous. Action recommandée : monitor. Parité fonctionnelle à 25% — position dominante.",
    our_advantages: [
      "Fonctionnalités nettement supérieures",
      "Intégrations enterprise étendues",
      "Support et SLA enterprise",
    ],
    their_advantages: [],
    counter_tactics: [
      "Proposer une période d'essai ou POC — réduire le risque perçu",
    ],
    talk_tracks: [
      "« Nous comprenons que vous évaluez Copper CRM. Voici pourquoi nos clients choisissent notre solution pour le long terme... »",
      "« Ce n'est pas une question de fonctionnalités, c'est une question de résultats business. »",
    ],
    objection_responses: [
      "Objection fonctionnalités : « Copper CRM couvre 25% de nos features — les 75% restants génèrent le ROI que vous cherchez. »",
      "Objection marque : « La notoriété ne garantit pas la performance. Voici 3 références clients dans votre secteur. »",
    ],
    red_flags: [],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const threat = searchParams.get("threat");
  const action = searchParams.get("action");
  const win_prob = searchParams.get("win_prob");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitive-battlecard`);
      if (threat) url.searchParams.set("threat", threat);
      if (action) url.searchParams.set("action", action);
      if (win_prob) url.searchParams.set("win_prob", win_prob);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let cards = [...mockBattlecards];
  if (threat) cards = cards.filter((c) => c.threat_level === threat);
  if (action) cards = cards.filter((c) => c.battlecard_action === action);
  if (win_prob) cards = cards.filter((c) => c.win_probability === win_prob);

  const threat_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const win_counts: Record<string, number> = {};
  let total_score = 0;

  for (const c of mockBattlecards) {
    threat_counts[c.threat_level] = (threat_counts[c.threat_level] || 0) + 1;
    action_counts[c.battlecard_action] = (action_counts[c.battlecard_action] || 0) + 1;
    win_counts[c.win_probability] = (win_counts[c.win_probability] || 0) + 1;
    total_score += c.threat_score;
  }

  const n = mockBattlecards.length;

  return NextResponse.json({
    battlecards: cards,
    summary: {
      total: n,
      threat_counts,
      action_counts,
      win_probability_counts: win_counts,
      avg_threat_score: Math.round((total_score / n) * 10) / 10,
      critical_count: mockBattlecards.filter((c) => c.threat_level === "critical").length,
      escalation_count: mockBattlecards.filter((c) => c.battlecard_action === "escalate").length,
    },
  });
}

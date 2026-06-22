import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[threat-intel] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type ThreatLevel = "benign" | "suspicious" | "malicious" | "apt";

interface RawEvent {
  event_id: string;
  timestamp: number;
  ip_address: string;
  endpoint: string;
  threat_type: string;
  severity: string;
  recommended_action: string;
}

interface ThreatActor {
  actor_id: string;
  ip_addresses: string[];
  first_seen: number;
  last_seen: number;
  attack_count: number;
  threat_types: string[];
  targeted_endpoints: string[];
  threat_level: ThreatLevel;
  confidence: number;
  persistence_hours: number;
}

interface EndpointVulnerability {
  endpoint: string;
  attack_count: number;
  unique_attackers: number;
  threat_types: string[];
  risk_score: number;
  recommended_actions: string[];
}

const HIGH_SEVERITY = new Set(["sql_injection", "command_injection", "path_traversal", "banned_ip_request", "brute_force"]);
const CRITICAL_TYPES = new Set(["command_injection", "path_traversal"]);

const HARDENING_MAP: Record<string, string> = {
  sql_injection: "Activer la validation stricte des paramètres SQL et utiliser des requêtes préparées",
  xss_attempt: "Implémenter Content-Security-Policy et encoder toutes les sorties HTML",
  path_traversal: "Valider et normaliser tous les chemins de fichiers, rejeter les séquences ../ ",
  command_injection: "Éviter exec() avec des entrées utilisateur, utiliser des listes d'arguments",
  template_injection: "Désactiver l'exécution de templates sur les entrées non-fiables",
  brute_force: "Implémenter CAPTCHA et verrouillage de compte après N échecs",
  rate_limit_exceeded: "Renforcer les règles de rate-limiting et implémenter un circuit breaker",
  oversized_payload: "Réduire la limite de payload ou implémenter un contrôle de streaming",
  banned_ip_request: "Activer la synchronisation de liste noire en temps réel avec threat feeds",
  blocked_ip_request: "Vérifier les listes de blocage IP avant traitement de chaque requête",
};

const LEVEL_SCORE: Record<ThreatLevel, number> = { apt: 90, malicious: 60, suspicious: 25, benign: 0 };

const now = Date.now() / 1000;

const MOCK_EVENTS: RawEvent[] = [
  // Actor 1: APT — 185.220.101.47 (SQL + XSS, persistent)
  { event_id: "e001", timestamp: now - 86400, ip_address: "185.220.101.47", endpoint: "/api/composer", threat_type: "sql_injection", severity: "high", recommended_action: "block" },
  { event_id: "e002", timestamp: now - 72000, ip_address: "185.220.101.47", endpoint: "/api/sentiment", threat_type: "xss_attempt", severity: "high", recommended_action: "block" },
  { event_id: "e003", timestamp: now - 57600, ip_address: "185.220.101.47", endpoint: "/api/forecast", threat_type: "path_traversal", severity: "critical", recommended_action: "ban" },
  { event_id: "e004", timestamp: now - 43200, ip_address: "185.220.101.47", endpoint: "/api/auth/login", threat_type: "brute_force", severity: "critical", recommended_action: "ban" },
  // Actor 2: MALICIOUS — 194.165.16.3 (path traversal + banned)
  { event_id: "e005", timestamp: now - 3200, ip_address: "194.165.16.3", endpoint: "/api/forecast", threat_type: "path_traversal", severity: "critical", recommended_action: "ban" },
  { event_id: "e006", timestamp: now - 1800, ip_address: "194.165.16.3", endpoint: "/api/composer", threat_type: "banned_ip_request", severity: "critical", recommended_action: "ban" },
  // Actor 3: MALICIOUS — 103.21.244.0 (command injection)
  { event_id: "e007", timestamp: now - 1400, ip_address: "103.21.244.0", endpoint: "/api/scorer", threat_type: "command_injection", severity: "critical", recommended_action: "ban" },
  { event_id: "e008", timestamp: now - 1000, ip_address: "103.21.244.0", endpoint: "/api/priority", threat_type: "command_injection", severity: "critical", recommended_action: "ban" },
  { event_id: "e009", timestamp: now - 600, ip_address: "103.21.244.0", endpoint: "/api/retention", threat_type: "sql_injection", severity: "high", recommended_action: "block" },
  // Actor 4: SUSPICIOUS — 91.108.4.18 (rate limit + blocked)
  { event_id: "e010", timestamp: now - 2000, ip_address: "91.108.4.18", endpoint: "/api/priority", threat_type: "rate_limit_exceeded", severity: "medium", recommended_action: "block" },
  { event_id: "e011", timestamp: now - 600, ip_address: "91.108.4.18", endpoint: "/api/auth/login", threat_type: "blocked_ip_request", severity: "high", recommended_action: "block" },
  // Actor 5: MALICIOUS — 45.142.212.100 (brute force + banned)
  { event_id: "e012", timestamp: now - 2800, ip_address: "45.142.212.100", endpoint: "/api/auth/login", threat_type: "brute_force", severity: "critical", recommended_action: "ban" },
  { event_id: "e013", timestamp: now - 60, ip_address: "45.142.212.100", endpoint: "/api/priority", threat_type: "banned_ip_request", severity: "critical", recommended_action: "ban" },
  // Actor 6: SUSPICIOUS — 158.69.201.47 (template injection)
  { event_id: "e014", timestamp: now - 900, ip_address: "158.69.201.47", endpoint: "/api/retention", threat_type: "template_injection", severity: "high", recommended_action: "block" },
  // Actor 7: SUSPICIOUS — 138.201.87.135 (oversized payload + SQL)
  { event_id: "e015", timestamp: now - 300, ip_address: "138.201.87.135", endpoint: "/api/subject-optimizer", threat_type: "oversized_payload", severity: "medium", recommended_action: "block" },
  { event_id: "e016", timestamp: now - 120, ip_address: "198.54.117.200", endpoint: "/api/composer", threat_type: "sql_injection", severity: "high", recommended_action: "block" },
];

function actorThreatLevel(attackCount: number, threatTypes: string[], persistenceHours: number): [ThreatLevel, number] {
  const criticalHits = threatTypes.filter(t => CRITICAL_TYPES.has(t)).length;
  const highHits = threatTypes.filter(t => HIGH_SEVERITY.has(t)).length;
  const diversity = new Set(threatTypes).size;

  if (persistenceHours > 12 && diversity >= 3 && criticalHits >= 1) {
    const confidence = Math.min(1.0, 0.70 + (diversity - 3) * 0.05 + (attackCount - 5) * 0.01);
    return ["apt", Math.round(Math.min(1.0, confidence) * 10000) / 10000];
  }
  if (criticalHits >= 1 || attackCount >= 5 || highHits >= 2) {
    const confidence = Math.min(1.0, 0.55 + criticalHits * 0.10 + highHits * 0.05);
    return ["malicious", Math.round(Math.min(1.0, confidence) * 10000) / 10000];
  }
  if (highHits >= 1 || attackCount >= 2 || diversity >= 2) {
    const confidence = Math.min(1.0, 0.40 + highHits * 0.05);
    return ["suspicious", Math.round(Math.min(1.0, confidence) * 10000) / 10000];
  }
  return ["benign", Math.round(Math.max(0.1, 0.30 - attackCount * 0.05) * 10000) / 10000];
}

function endpointRiskScore(attackCount: number, uniqueAttackers: number, threatTypes: string[]): number {
  const criticalWeight = threatTypes.filter(t => CRITICAL_TYPES.has(t)).length * 3.0;
  const highWeight = threatTypes.filter(t => HIGH_SEVERITY.has(t)).length * 1.5;
  const base = Math.min(60, attackCount * 5) + criticalWeight * 5 + highWeight * 2;
  const attackerBonus = Math.min(20, uniqueAttackers * 4);
  return Math.round(Math.min(100, base + attackerBonus) * 100) / 100;
}

function buildActors(events: RawEvent[]): ThreatActor[] {
  const byIp: Record<string, RawEvent[]> = {};
  for (const e of events) {
    if (!byIp[e.ip_address]) byIp[e.ip_address] = [];
    byIp[e.ip_address].push(e);
  }

  return Object.entries(byIp).map(([ip, evts]) => {
    const firstSeen = Math.min(...evts.map(e => e.timestamp));
    const lastSeen = Math.max(...evts.map(e => e.timestamp));
    const persistenceHours = (lastSeen - firstSeen) / 3600;
    const allTypes = evts.map(e => e.threat_type);
    const threatTypes = [...new Set(allTypes)];
    const endpoints = [...new Set(evts.map(e => e.endpoint))];
    const [level, confidence] = actorThreatLevel(evts.length, allTypes, persistenceHours);

    return {
      actor_id: `actor_${ip.replace(/\./g, "_")}`,
      ip_addresses: [ip],
      first_seen: firstSeen,
      last_seen: lastSeen,
      attack_count: evts.length,
      threat_types: threatTypes,
      targeted_endpoints: endpoints,
      threat_level: level,
      confidence,
      persistence_hours: Math.round(persistenceHours * 100) / 100,
    };
  }).sort((a, b) => {
    const scoreDiff = LEVEL_SCORE[b.threat_level] - LEVEL_SCORE[a.threat_level];
    return scoreDiff !== 0 ? scoreDiff : b.attack_count - a.attack_count;
  });
}

function buildEndpoints(events: RawEvent[]): EndpointVulnerability[] {
  const byEp: Record<string, RawEvent[]> = {};
  for (const e of events) {
    if (!byEp[e.endpoint]) byEp[e.endpoint] = [];
    byEp[e.endpoint].push(e);
  }

  return Object.entries(byEp).map(([ep, evts]) => {
    const threatTypes = [...new Set(evts.map(e => e.threat_type))];
    const uniqueAttackers = new Set(evts.map(e => e.ip_address)).size;
    const risk = endpointRiskScore(evts.length, uniqueAttackers, evts.map(e => e.threat_type));
    const recommendations = threatTypes.map(t => HARDENING_MAP[t]).filter(Boolean);

    return {
      endpoint: ep,
      attack_count: evts.length,
      unique_attackers: uniqueAttackers,
      threat_types: threatTypes,
      risk_score: risk,
      recommended_actions: recommendations,
    };
  }).sort((a, b) => b.risk_score - a.risk_score);
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/threat-intel`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  const actors = buildActors(MOCK_EVENTS);
  const endpoints = buildEndpoints(MOCK_EVENTS);

  const levelCounts: Record<ThreatLevel, number> = { apt: 0, malicious: 0, suspicious: 0, benign: 0 };
  for (const a of actors) levelCounts[a.threat_level]++;

  const avgRisk = endpoints.length
    ? Math.round((endpoints.reduce((s, e) => s + e.risk_score, 0) / endpoints.length) * 100) / 100
    : 0;

  const highRisk = endpoints.filter(e => e.risk_score >= 50).length;

  const summary = {
    total_events: MOCK_EVENTS.length,
    total_actors: actors.length,
    actor_level_counts: levelCounts,
    total_endpoints_targeted: endpoints.length,
    avg_endpoint_risk_score: avgRisk,
    high_risk_endpoint_count: highRisk,
    apt_count: levelCounts.apt,
    malicious_count: levelCounts.malicious,
  };

  return sealResponse(NextResponse.json({
    actors,
    endpoints,
    summary,
    last_updated: new Date().toISOString(),
  }));
}

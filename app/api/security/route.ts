import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[security] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

type ThreatSeverity = "info" | "low" | "medium" | "high" | "critical";
type RecommendedAction = "log" | "alert" | "block" | "ban";

interface SecurityEvent {
  event_id: string;
  timestamp: number;
  ip_address: string;
  endpoint: string;
  threat_type: string;
  severity: ThreatSeverity;
  recommended_action: RecommendedAction;
  matched_pattern: string;
  raw_input: string;
  details: string;
}

interface ThreatSummary {
  total_events: number;
  severity_counts: Record<ThreatSeverity, number>;
  blocked_ips: number;
  banned_ips: number;
  top_threat_types: { type: string; count: number }[];
}

const now = Date.now() / 1000;

const MOCK_EVENTS: SecurityEvent[] = [
  { event_id: "evt_000001", timestamp: now - 3600, ip_address: "185.220.101.47", endpoint: "/api/composer", threat_type: "sql_injection", severity: "high", recommended_action: "block", matched_pattern: "UNION SELECT", raw_input: "' UNION SELECT 1,2,3--", details: "SQL injection attempt on composer endpoint" },
  { event_id: "evt_000002", timestamp: now - 3200, ip_address: "194.165.16.3",   endpoint: "/api/forecast", threat_type: "path_traversal", severity: "critical", recommended_action: "ban", matched_pattern: "../../../", raw_input: "../../../etc/passwd", details: "Path traversal attempt — IP auto-banned" },
  { event_id: "evt_000003", timestamp: now - 2800, ip_address: "45.142.212.100", endpoint: "/api/auth/login", threat_type: "brute_force", severity: "critical", recommended_action: "ban", matched_pattern: ">=10 failed auths", raw_input: "", details: "10 failed authentication attempts — IP banned" },
  { event_id: "evt_000004", timestamp: now - 2400, ip_address: "185.220.101.47", endpoint: "/api/sentiment", threat_type: "xss_attempt", severity: "high", recommended_action: "block", matched_pattern: "<script", raw_input: "<script>document.cookie</script>", details: "XSS attempt in sentiment analyzer input" },
  { event_id: "evt_000005", timestamp: now - 2000, ip_address: "91.108.4.18",    endpoint: "/api/priority", threat_type: "rate_limit_exceeded", severity: "medium", recommended_action: "block", matched_pattern: ">120 req/60s", raw_input: "", details: "145 requests in 60s window — rate limit exceeded" },
  { event_id: "evt_000006", timestamp: now - 1800, ip_address: "194.165.16.3",   endpoint: "/api/composer", threat_type: "banned_ip_request", severity: "critical", recommended_action: "ban", matched_pattern: "ip_ban_list", raw_input: "POST {template_id: 'x'}", details: "Banned IP attempted access: auto-ban: path_traversal" },
  { event_id: "evt_000007", timestamp: now - 1400, ip_address: "103.21.244.0",   endpoint: "/api/scorer", threat_type: "command_injection", severity: "critical", recommended_action: "ban", matched_pattern: "; ls -la", raw_input: "company_name=test; ls -la /etc", details: "Command injection in scorer API payload" },
  { event_id: "evt_000008", timestamp: now - 900,  ip_address: "158.69.201.47",  endpoint: "/api/retention", threat_type: "template_injection", severity: "high", recommended_action: "block", matched_pattern: "{{payload}}", raw_input: "{{7*7}}", details: "SSTI attempt in retention API field" },
  { event_id: "evt_000009", timestamp: now - 600,  ip_address: "91.108.4.18",    endpoint: "/api/auth/login", threat_type: "blocked_ip_request", severity: "high", recommended_action: "block", matched_pattern: "ip_block_list", raw_input: "", details: "Blocked IP attempted access" },
  { event_id: "evt_000010", timestamp: now - 300,  ip_address: "138.201.87.135", endpoint: "/api/subject-optimizer", threat_type: "oversized_payload", severity: "medium", recommended_action: "block", matched_pattern: ">50000b", raw_input: "[TRUNCATED — 52000 bytes]", details: "Payload size exceeded limit (52000 bytes)" },
  { event_id: "evt_000011", timestamp: now - 120,  ip_address: "198.54.117.200", endpoint: "/api/composer", threat_type: "sql_injection", severity: "high", recommended_action: "block", matched_pattern: "DROP TABLE", raw_input: "'; DROP TABLE templates--", details: "SQL injection — DROP TABLE attempt" },
  { event_id: "evt_000012", timestamp: now - 60,   ip_address: "45.142.212.100", endpoint: "/api/priority", threat_type: "banned_ip_request", severity: "critical", recommended_action: "ban", matched_pattern: "ip_ban_list", raw_input: "", details: "Banned IP attempted access: brute_force" },
];

const BLOCKED_IPS = ["185.220.101.47", "91.108.4.18", "138.201.87.135", "198.54.117.200"];
const BANNED_IPS = ["194.165.16.3", "45.142.212.100", "103.21.244.0"];

function computeSummary(events: SecurityEvent[]): ThreatSummary {
  const severity_counts: Record<ThreatSeverity, number> = { info: 0, low: 0, medium: 0, high: 0, critical: 0 };
  const type_counts: Record<string, number> = {};
  for (const e of events) {
    severity_counts[e.severity]++;
    type_counts[e.threat_type] = (type_counts[e.threat_type] ?? 0) + 1;
  }
  const top_threat_types = Object.entries(type_counts)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)
    .map(([type, count]) => ({ type, count }));

  return {
    total_events: events.length,
    severity_counts,
    blocked_ips: BLOCKED_IPS.length,
    banned_ips: BANNED_IPS.length,
    top_threat_types,
  };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/security`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch { /* fall through */ }
  }

  const events = [...MOCK_EVENTS].sort((a, b) => b.timestamp - a.timestamp);

  return sealResponse(NextResponse.json({
    events,
    summary: computeSummary(events),
    blocked_ips: BLOCKED_IPS,
    banned_ips: BANNED_IPS,
    security_score: 72,
    last_scan: new Date().toISOString(),
  }));
}

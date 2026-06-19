import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CSE-001: critical, splinternet_collapse (isp>=0.70 AND dse>=0.65)
  { entity_id:"CSE-001", cyber_domain:"internet_fragmentation", region:"APAC",
    internet_splinternet_progression:0.85, national_internet_firewall_density:0.80,
    DNS_sovereignty_erosion:0.75, undersea_cable_geopolitical_vulnerability:0.70,
    cloud_infrastructure_foreign_dependency:0.65, data_localization_fragmentation:0.78,
    internet_shutdown_weaponization_frequency:0.60, BGP_hijacking_exposure:0.60,
    cyber_deterrence_capability_gap:0.65, critical_infrastructure_cyber_exposure:0.70,
    zero_day_stockpiling_arms_race:0.65, AI_enhanced_cyber_attack_capability:0.60,
    supply_chain_software_poisoning_risk:0.60, cyber_mercenary_proliferation:0.65,
    internet_governance_capture:0.70, election_infrastructure_cyber_risk:0.68,
    digital_sovereignty_deficit_index:0.75 },
  // CSE-002: low, none
  { entity_id:"CSE-002", cyber_domain:"open_internet_governance", region:"NAMER",
    internet_splinternet_progression:0.10, national_internet_firewall_density:0.08,
    DNS_sovereignty_erosion:0.12, undersea_cable_geopolitical_vulnerability:0.10,
    cloud_infrastructure_foreign_dependency:0.12, data_localization_fragmentation:0.08,
    internet_shutdown_weaponization_frequency:0.08, BGP_hijacking_exposure:0.10,
    cyber_deterrence_capability_gap:0.12, critical_infrastructure_cyber_exposure:0.10,
    zero_day_stockpiling_arms_race:0.10, AI_enhanced_cyber_attack_capability:0.08,
    supply_chain_software_poisoning_risk:0.10, cyber_mercenary_proliferation:0.08,
    internet_governance_capture:0.10, election_infrastructure_cyber_risk:0.10,
    digital_sovereignty_deficit_index:0.10 },
  // CSE-003: high, undersea_cable_crisis (ucgv>=0.70 AND cifd>=0.65)
  { entity_id:"CSE-003", cyber_domain:"undersea_cable_infrastructure", region:"EMEA",
    internet_splinternet_progression:0.42, national_internet_firewall_density:0.40,
    DNS_sovereignty_erosion:0.38, undersea_cable_geopolitical_vulnerability:0.78,
    cloud_infrastructure_foreign_dependency:0.72, data_localization_fragmentation:0.42,
    internet_shutdown_weaponization_frequency:0.38, BGP_hijacking_exposure:0.42,
    cyber_deterrence_capability_gap:0.45, critical_infrastructure_cyber_exposure:0.55,
    zero_day_stockpiling_arms_race:0.42, AI_enhanced_cyber_attack_capability:0.40,
    supply_chain_software_poisoning_risk:0.42, cyber_mercenary_proliferation:0.38,
    internet_governance_capture:0.40, election_infrastructure_cyber_risk:0.42,
    digital_sovereignty_deficit_index:0.45 },
  // CSE-004: low, none
  { entity_id:"CSE-004", cyber_domain:"digital_resilience", region:"LATAM",
    internet_splinternet_progression:0.12, national_internet_firewall_density:0.10,
    DNS_sovereignty_erosion:0.08, undersea_cable_geopolitical_vulnerability:0.12,
    cloud_infrastructure_foreign_dependency:0.10, data_localization_fragmentation:0.10,
    internet_shutdown_weaponization_frequency:0.10, BGP_hijacking_exposure:0.08,
    cyber_deterrence_capability_gap:0.10, critical_infrastructure_cyber_exposure:0.12,
    zero_day_stockpiling_arms_race:0.08, AI_enhanced_cyber_attack_capability:0.10,
    supply_chain_software_poisoning_risk:0.10, cyber_mercenary_proliferation:0.10,
    internet_governance_capture:0.08, election_infrastructure_cyber_risk:0.10,
    digital_sovereignty_deficit_index:0.12 },
  // CSE-005: critical, cyber_weapons_proliferation (zd>=0.70 AND ai>=0.65; isp<0.70)
  { entity_id:"CSE-005", cyber_domain:"cyber_weapons_ecosystem", region:"MEA",
    internet_splinternet_progression:0.55, national_internet_firewall_density:0.60,
    DNS_sovereignty_erosion:0.50, undersea_cable_geopolitical_vulnerability:0.58,
    cloud_infrastructure_foreign_dependency:0.60, data_localization_fragmentation:0.55,
    internet_shutdown_weaponization_frequency:0.60, BGP_hijacking_exposure:0.60,
    cyber_deterrence_capability_gap:0.68, critical_infrastructure_cyber_exposure:0.65,
    zero_day_stockpiling_arms_race:0.82, AI_enhanced_cyber_attack_capability:0.78,
    supply_chain_software_poisoning_risk:0.65, cyber_mercenary_proliferation:0.70,
    internet_governance_capture:0.68, election_infrastructure_cyber_risk:0.65,
    digital_sovereignty_deficit_index:0.72 },
  // CSE-006: moderate, none
  { entity_id:"CSE-006", cyber_domain:"data_sovereignty", region:"EMEA",
    internet_splinternet_progression:0.28, national_internet_firewall_density:0.30,
    DNS_sovereignty_erosion:0.25, undersea_cable_geopolitical_vulnerability:0.28,
    cloud_infrastructure_foreign_dependency:0.30, data_localization_fragmentation:0.32,
    internet_shutdown_weaponization_frequency:0.25, BGP_hijacking_exposure:0.28,
    cyber_deterrence_capability_gap:0.30, critical_infrastructure_cyber_exposure:0.30,
    zero_day_stockpiling_arms_race:0.28, AI_enhanced_cyber_attack_capability:0.25,
    supply_chain_software_poisoning_risk:0.28, cyber_mercenary_proliferation:0.28,
    internet_governance_capture:0.30, election_infrastructure_cyber_risk:0.28,
    digital_sovereignty_deficit_index:0.32 },
  // CSE-007: high, internet_shutdown_authoritarianism (iswf>=0.70 AND nifd>=0.65; isp<0.70)
  { entity_id:"CSE-007", cyber_domain:"internet_control_authoritarianism", region:"APAC",
    internet_splinternet_progression:0.50, national_internet_firewall_density:0.75,
    DNS_sovereignty_erosion:0.48, undersea_cable_geopolitical_vulnerability:0.42,
    cloud_infrastructure_foreign_dependency:0.45, data_localization_fragmentation:0.48,
    internet_shutdown_weaponization_frequency:0.80, BGP_hijacking_exposure:0.45,
    cyber_deterrence_capability_gap:0.45, critical_infrastructure_cyber_exposure:0.48,
    zero_day_stockpiling_arms_race:0.42, AI_enhanced_cyber_attack_capability:0.40,
    supply_chain_software_poisoning_risk:0.42, cyber_mercenary_proliferation:0.45,
    internet_governance_capture:0.48, election_infrastructure_cyber_risk:0.50,
    digital_sovereignty_deficit_index:0.50 },
  // CSE-008: critical, supply_chain_cyber_poisoning (scsp>=0.70 AND bgp>=0.65; isp<0.70, ucgv<0.70, zd<0.70, iswf<0.70)
  { entity_id:"CSE-008", cyber_domain:"supply_chain_security", region:"NAMER",
    internet_splinternet_progression:0.60, national_internet_firewall_density:0.58,
    DNS_sovereignty_erosion:0.55, undersea_cable_geopolitical_vulnerability:0.60,
    cloud_infrastructure_foreign_dependency:0.62, data_localization_fragmentation:0.58,
    internet_shutdown_weaponization_frequency:0.55, BGP_hijacking_exposure:0.75,
    cyber_deterrence_capability_gap:0.65, critical_infrastructure_cyber_exposure:0.68,
    zero_day_stockpiling_arms_race:0.65, AI_enhanced_cyber_attack_capability:0.62,
    supply_chain_software_poisoning_risk:0.82, cyber_mercenary_proliferation:0.68,
    internet_governance_capture:0.65, election_infrastructure_cyber_risk:0.60,
    digital_sovereignty_deficit_index:0.72 },
];

type CSEEntity = typeof MOCK_ENTITIES[0];

function fragmentationScore(e: CSEEntity): number {
  const v = e.internet_splinternet_progression * 0.40
          + e.national_internet_firewall_density * 0.35
          + e.data_localization_fragmentation * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function infrastructureScore(e: CSEEntity): number {
  const v = e.undersea_cable_geopolitical_vulnerability * 0.40
          + e.cloud_infrastructure_foreign_dependency * 0.35
          + e.critical_infrastructure_cyber_exposure * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function attackScore(e: CSEEntity): number {
  const v = e.AI_enhanced_cyber_attack_capability * 0.40
          + e.zero_day_stockpiling_arms_race * 0.35
          + e.supply_chain_software_poisoning_risk * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function governanceScore(e: CSEEntity): number {
  const v = e.digital_sovereignty_deficit_index * 0.40
          + e.internet_governance_capture * 0.35
          + e.cyber_mercenary_proliferation * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function compositeScore(f: number, i: number, a: number, g: number): number {
  return Math.min(Math.round((f * 0.30 + i * 0.25 + a * 0.25 + g * 0.20) * 100) / 100, 100);
}
function cyberPattern(e: CSEEntity): string {
  if (e.internet_splinternet_progression >= 0.70 && e.DNS_sovereignty_erosion >= 0.65)                         return "splinternet_collapse";
  if (e.undersea_cable_geopolitical_vulnerability >= 0.70 && e.cloud_infrastructure_foreign_dependency >= 0.65) return "undersea_cable_crisis";
  if (e.zero_day_stockpiling_arms_race >= 0.70 && e.AI_enhanced_cyber_attack_capability >= 0.65)               return "cyber_weapons_proliferation";
  if (e.internet_shutdown_weaponization_frequency >= 0.70 && e.national_internet_firewall_density >= 0.65)     return "internet_shutdown_authoritarianism";
  if (e.supply_chain_software_poisoning_risk >= 0.70 && e.BGP_hijacking_exposure >= 0.65)                      return "supply_chain_cyber_poisoning";
  return "none";
}
function riskLevel(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string {
  if (c >= 60) return "fragmentation_internet_systémique";
  if (c >= 40) return "crise_souveraineté_cyber_majeure";
  if (c >= 20) return "erosion_souveraineté_numérique";
  return "cyber_souveraineté_relative";
}
function recommendedAction(c: number): string {
  if (c >= 60) return "intervention_souveraineté_cyber_urgente";
  if (c >= 40) return "stratégie_cyber_souveraineté_accélérée";
  if (c >= 20) return "renforcement_infrastructure_cyber_nationale";
  return "veille_souveraineté_cyber_continue";
}
function signal(c: number): string {
  if (c >= 60) return "🔴 Fragmentation internet systémique — souveraineté numérique compromise";
  if (c >= 40) return "🟠 Crise souveraineté cyber majeure détectée";
  if (c >= 20) return "🟡 Érosion souveraineté numérique active";
  return "🟢 Cyber souveraineté relativement maintenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const frag = fragmentationScore(e), infra = infrastructureScore(e), atk = attackScore(e), gov = governanceScore(e);
      const comp = compositeScore(frag, infra, atk, gov);
      const pat = cyberPattern(e), risk = riskLevel(comp);
      return {
        entity_id: e.entity_id,
        cyber_domain: e.cyber_domain,
        region: e.region,
        fragmentation_score: frag,
        infrastructure_score: infra,
        attack_score: atk,
        governance_score: gov,
        composite_score: comp,
        risk_level: risk,
        cyber_pattern: pat,
        severity: severity(comp),
        recommended_action: recommendedAction(comp),
        signal: signal(comp),
        internet_splinternet_progression: e.internet_splinternet_progression,
        digital_sovereignty_deficit_index: e.digital_sovereignty_deficit_index,
      };
    });

    const patDist: Record<string,number>  = {};
    const riskDist: Record<string,number> = {};
    const sevDist: Record<string,number>  = {};
    const actDist: Record<string,number>  = {};
    let totalComp = 0, critical = 0, high = 0, moderate = 0, low = 0;
    for (const en of entities) {
      patDist[en.cyber_pattern]      = (patDist[en.cyber_pattern]      || 0) + 1;
      riskDist[en.risk_level]        = (riskDist[en.risk_level]        || 0) + 1;
      sevDist[en.severity]           = (sevDist[en.severity]           || 0) + 1;
      actDist[en.recommended_action] = (actDist[en.recommended_action] || 0) + 1;
      totalComp += en.composite_score;
      if (en.risk_level === "critical")       critical++;
      else if (en.risk_level === "high")      high++;
      else if (en.risk_level === "moderate")  moderate++;
      else                                    low++;
    }
    const n = entities.length;
    const avgComposite = Math.round(totalComp / n * 10) / 10;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 357,
        module_name: "Cyber Sovereignty & Internet Fragmentation Intelligence Engine",
        total_entities: n,
        critical_count: critical,
        high_count: high,
        moderate_count: moderate,
        low_count: low,
        avg_composite: avgComposite,
        pattern_distribution: patDist,
        risk_distribution: riskDist,
        severity_distribution: sevDist,
        action_distribution: actDist,
        avg_estimated_cyber_sovereignty_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      } as Record<string, unknown>,
    } as Record<string, unknown>, "cyber-sovereignty-engine") as Parameters<typeof NextResponse.json>[0]);
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/cyber-sovereignty-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "cyber-sovereignty-engine") as Parameters<typeof NextResponse.json>[0]);
  } catch {
    return NextResponse.json(
      sealResponse({ error: "upstream_unavailable" } as Record<string, unknown>, "cyber-sovereignty-engine") as Parameters<typeof NextResponse.json>[0],
      { status: 502 }
    );
  }
}

import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// prettier-ignore
const MOCK_ENTITIES = [
  // CEG-001: EMEA, lending_protocol → critical, governance_attack
  {
    entity_id: "CEG-001", defi_segment: "lending_protocol", region: "EMEA",
    protocol_governance_quality: 0.12, tvl_concentration: 0.72,
    smart_contract_audit_coverage: 0.68, oracle_manipulation_risk: 0.30,
    liquidity_depth: 0.65, cross_protocol_contagion: 0.42,
    regulatory_clarity: 0.50, rug_pull_risk: 0.35,
    mev_extraction_rate: 0.40, bridge_security_score: 0.55,
    stablecoin_depeg_risk: 0.28, governance_token_concentration: 0.78,
    flash_loan_attack_surface: 0.30, protocol_upgrade_risk: 0.45,
    community_coordination_quality: 0.35, revenue_sustainability: 0.48,
    defi_insurance_coverage: 0.30,
  },
  // CEG-002: APAC, dex → low, defi_stable/none
  {
    entity_id: "CEG-002", defi_segment: "dex", region: "APAC",
    protocol_governance_quality: 0.88, tvl_concentration: 0.18,
    smart_contract_audit_coverage: 0.92, oracle_manipulation_risk: 0.08,
    liquidity_depth: 0.90, cross_protocol_contagion: 0.10,
    regulatory_clarity: 0.85, rug_pull_risk: 0.06,
    mev_extraction_rate: 0.08, bridge_security_score: 0.90,
    stablecoin_depeg_risk: 0.05, governance_token_concentration: 0.15,
    flash_loan_attack_surface: 0.08, protocol_upgrade_risk: 0.10,
    community_coordination_quality: 0.90, revenue_sustainability: 0.88,
    defi_insurance_coverage: 0.85,
  },
  // CEG-003: NOAM, yield_farming → high, smart_contract_exploit
  {
    entity_id: "CEG-003", defi_segment: "yield_farming", region: "NOAM",
    protocol_governance_quality: 0.60, tvl_concentration: 0.40,
    smart_contract_audit_coverage: 0.22, oracle_manipulation_risk: 0.62,
    liquidity_depth: 0.58, cross_protocol_contagion: 0.38,
    regulatory_clarity: 0.55, rug_pull_risk: 0.30,
    mev_extraction_rate: 0.50, bridge_security_score: 0.50,
    stablecoin_depeg_risk: 0.30, governance_token_concentration: 0.38,
    flash_loan_attack_surface: 0.68, protocol_upgrade_risk: 0.42,
    community_coordination_quality: 0.55, revenue_sustainability: 0.50,
    defi_insurance_coverage: 0.45,
  },
  // CEG-004: LATAM, dex → low, defi_stable/none
  {
    entity_id: "CEG-004", defi_segment: "dex", region: "LATAM",
    protocol_governance_quality: 0.82, tvl_concentration: 0.22,
    smart_contract_audit_coverage: 0.88, oracle_manipulation_risk: 0.12,
    liquidity_depth: 0.85, cross_protocol_contagion: 0.15,
    regulatory_clarity: 0.80, rug_pull_risk: 0.10,
    mev_extraction_rate: 0.12, bridge_security_score: 0.85,
    stablecoin_depeg_risk: 0.08, governance_token_concentration: 0.20,
    flash_loan_attack_surface: 0.10, protocol_upgrade_risk: 0.15,
    community_coordination_quality: 0.85, revenue_sustainability: 0.82,
    defi_insurance_coverage: 0.80,
  },
  // CEG-005: MEA, lending_protocol → critical, liquidity_cascade
  {
    entity_id: "CEG-005", defi_segment: "lending_protocol", region: "MEA",
    protocol_governance_quality: 0.40, tvl_concentration: 0.55,
    smart_contract_audit_coverage: 0.55, oracle_manipulation_risk: 0.45,
    liquidity_depth: 0.18, cross_protocol_contagion: 0.78,
    regulatory_clarity: 0.42, rug_pull_risk: 0.48,
    mev_extraction_rate: 0.55, bridge_security_score: 0.38,
    stablecoin_depeg_risk: 0.50, governance_token_concentration: 0.50,
    flash_loan_attack_surface: 0.42, protocol_upgrade_risk: 0.55,
    community_coordination_quality: 0.38, revenue_sustainability: 0.35,
    defi_insurance_coverage: 0.25,
  },
  // CEG-006: EMEA, stablecoin → moderate, none
  {
    entity_id: "CEG-006", defi_segment: "stablecoin", region: "EMEA",
    protocol_governance_quality: 0.62, tvl_concentration: 0.38,
    smart_contract_audit_coverage: 0.65, oracle_manipulation_risk: 0.30,
    liquidity_depth: 0.62, cross_protocol_contagion: 0.28,
    regulatory_clarity: 0.58, rug_pull_risk: 0.28,
    mev_extraction_rate: 0.25, bridge_security_score: 0.60,
    stablecoin_depeg_risk: 0.32, governance_token_concentration: 0.35,
    flash_loan_attack_surface: 0.30, protocol_upgrade_risk: 0.30,
    community_coordination_quality: 0.60, revenue_sustainability: 0.58,
    defi_insurance_coverage: 0.55,
  },
  // CEG-007: APAC, yield_farming → high, stablecoin_depeg_crisis
  {
    entity_id: "CEG-007", defi_segment: "yield_farming", region: "APAC",
    protocol_governance_quality: 0.52, tvl_concentration: 0.72,
    smart_contract_audit_coverage: 0.60, oracle_manipulation_risk: 0.40,
    liquidity_depth: 0.50, cross_protocol_contagion: 0.40,
    regulatory_clarity: 0.50, rug_pull_risk: 0.38,
    mev_extraction_rate: 0.42, bridge_security_score: 0.48,
    stablecoin_depeg_risk: 0.78, governance_token_concentration: 0.45,
    flash_loan_attack_surface: 0.40, protocol_upgrade_risk: 0.45,
    community_coordination_quality: 0.50, revenue_sustainability: 0.45,
    defi_insurance_coverage: 0.40,
  },
  // CEG-008: NOAM, lending_protocol → critical, regulatory_crackdown
  {
    entity_id: "CEG-008", defi_segment: "lending_protocol", region: "NOAM",
    protocol_governance_quality: 0.35, tvl_concentration: 0.55,
    smart_contract_audit_coverage: 0.48, oracle_manipulation_risk: 0.52,
    liquidity_depth: 0.38, cross_protocol_contagion: 0.48,
    regulatory_clarity: 0.18, rug_pull_risk: 0.72,
    mev_extraction_rate: 0.60, bridge_security_score: 0.30,
    stablecoin_depeg_risk: 0.45, governance_token_concentration: 0.52,
    flash_loan_attack_surface: 0.50, protocol_upgrade_risk: 0.62,
    community_coordination_quality: 0.32, revenue_sustainability: 0.30,
    defi_insurance_coverage: 0.22,
  },
];

type Entity = (typeof MOCK_ENTITIES)[0];

function governanceScore(e: Entity): number {
  return (
    (1 - e.protocol_governance_quality) * 0.4 +
    e.governance_token_concentration * 0.35 +
    (1 - e.community_coordination_quality) * 0.25
  ) * 100;
}

function securityScore(e: Entity): number {
  return (
    (1 - e.smart_contract_audit_coverage) * 0.35 +
    e.oracle_manipulation_risk * 0.35 +
    e.flash_loan_attack_surface * 0.30
  ) * 100;
}

function liquidityScore(e: Entity): number {
  return (
    (1 - e.liquidity_depth) * 0.4 +
    e.tvl_concentration * 0.35 +
    e.stablecoin_depeg_risk * 0.25
  ) * 100;
}

function regulatoryScore(e: Entity): number {
  return (
    (1 - e.regulatory_clarity) * 0.4 +
    e.rug_pull_risk * 0.35 +
    (1 - e.defi_insurance_coverage) * 0.25
  ) * 100;
}

function defiComposite(gov: number, sec: number, liq: number, reg: number): number {
  return gov * 0.30 + sec * 0.25 + liq * 0.25 + reg * 0.20;
}

function defiRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function defiPattern(e: Entity): string {
  if ((1 - e.protocol_governance_quality) >= 0.65 && e.governance_token_concentration >= 0.60)
    return "governance_attack";
  if ((1 - e.smart_contract_audit_coverage) >= 0.65 && e.flash_loan_attack_surface >= 0.55)
    return "smart_contract_exploit";
  if ((1 - e.liquidity_depth) >= 0.65 && e.cross_protocol_contagion >= 0.60)
    return "liquidity_cascade";
  if (e.stablecoin_depeg_risk >= 0.70 && e.tvl_concentration >= 0.60)
    return "stablecoin_depeg_crisis";
  if ((1 - e.regulatory_clarity) >= 0.70 && e.rug_pull_risk >= 0.60)
    return "regulatory_crackdown";
  return "none";
}

function defiSeverity(composite: number): string {
  if (composite >= 75) return "defi_collapse";
  if (composite >= 50) return "high_systemic_risk";
  if (composite >= 25) return "protocol_stress";
  return "defi_stable";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "defi_emergency_shutdown";
  if (risk === "high" && pattern === "liquidity_cascade") return "liquidity_backstop";
  if (risk === "high") return "protocol_hardening";
  if (risk === "moderate") return "defi_monitoring";
  return "no_action";
}

function defiSignal(e: Entity, risk: string, composite: number): string {
  const comp = Math.round(composite);
  if (risk === "critical") {
    return `Critique — qualité gouvernance ${Math.round(e.protocol_governance_quality * 100)}% — concentration TVL ${Math.round(e.tvl_concentration * 100)}% — composite ${comp}`;
  }
  if (risk === "high") {
    return `Élevé — couverture audit ${Math.round(e.smart_contract_audit_coverage * 100)}% — profondeur liquidité ${Math.round(e.liquidity_depth * 100)}% — composite ${comp}`;
  }
  if (risk === "moderate") {
    return `Modéré — risque dépeg stablecoin ${Math.round(e.stablecoin_depeg_risk * 100)}% — composite ${comp}`;
  }
  return "Protocole DeFi stable — gouvernance solide, sécurité vérifiée, liquidité profonde";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const gov = governanceScore(e);
      const sec = securityScore(e);
      const liq = liquidityScore(e);
      const reg = regulatoryScore(e);
      const comp = defiComposite(gov, sec, liq, reg);
      const risk = defiRisk(comp);
      const pattern = defiPattern(e);
      const severity = defiSeverity(comp);
      const action = recommendedAction(risk, pattern);

      return {
        entity_id: e.entity_id,
        region: e.region,
        defi_segment: e.defi_segment,
        defi_risk: risk,
        defi_pattern: pattern,
        defi_severity: severity,
        recommended_action: action,
        governance_score: Math.round(gov * 100) / 100,
        security_score: Math.round(sec * 100) / 100,
        liquidity_score: Math.round(liq * 100) / 100,
        regulatory_score: Math.round(reg * 100) / 100,
        defi_composite: Math.round(comp * 100) / 100,
        is_in_defi_crisis: comp >= 60,
        requires_defi_intervention: comp >= 40,
        defi_signal: defiSignal(e, risk, comp),
      };
    });

    const riskCounts: Record<string, number> = {};
    const patternCounts: Record<string, number> = {};
    const severityCounts: Record<string, number> = {};
    const actionCounts: Record<string, number> = {};

    let totalComposite = 0;
    let totalGov = 0;
    let totalSec = 0;
    let totalLiq = 0;
    let totalReg = 0;
    let defiCrisisCount = 0;
    let defiInterventionCount = 0;

    for (const ent of entities) {
      riskCounts[ent.defi_risk] = (riskCounts[ent.defi_risk] || 0) + 1;
      patternCounts[ent.defi_pattern] = (patternCounts[ent.defi_pattern] || 0) + 1;
      severityCounts[ent.defi_severity] = (severityCounts[ent.defi_severity] || 0) + 1;
      actionCounts[ent.recommended_action] = (actionCounts[ent.recommended_action] || 0) + 1;
      totalComposite += ent.defi_composite;
      totalGov += ent.governance_score;
      totalSec += ent.security_score;
      totalLiq += ent.liquidity_score;
      totalReg += ent.regulatory_score;
      if (ent.is_in_defi_crisis) defiCrisisCount++;
      if (ent.requires_defi_intervention) defiInterventionCount++;
    }

    const n = entities.length;
    const avgComposite = totalComposite / n;

    const summary = {
      total: n,
      risk_counts: riskCounts,
      pattern_counts: patternCounts,
      severity_counts: severityCounts,
      action_counts: actionCounts,
      avg_defi_composite: Math.round(avgComposite * 10) / 10,
      defi_crisis_count: defiCrisisCount,
      defi_intervention_count: defiInterventionCount,
      avg_governance_score: Math.round((totalGov / n) * 10) / 10,
      avg_security_score: Math.round((totalSec / n) * 10) / 10,
      avg_liquidity_score: Math.round((totalLiq / n) * 10) / 10,
      avg_regulatory_score: Math.round((totalReg / n) * 10) / 10,
      avg_estimated_defi_risk_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "crypto-economic-governance-engine")
    );
  }

  try {
    const upstream = await fetch(
      `${process.env.SWARM_API_URL}/crypto-economic-governance-engine`
    );
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "crypto-economic-governance-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream swarm unavailable" }, "crypto-economic-governance-engine"),
      { status: 502 }
    );
  }
}

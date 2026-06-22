import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[cbdc-sovereignty-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // CBDC-001 — Digital Yuan, APAC → critical, financial_surveillance_state
  {
    id: "CBDC-001", currency_type: "digital_yuan", region: "APAC",
    surveillance_intensity: 0.92, transaction_monitoring: 0.88,
    programmability_risk: 0.78, privacy_preservation: 0.08,
    financial_inclusion: 0.72, sovereignty_risk: 0.60,
    interoperability: 0.65, cross_border_control: 0.80,
    offline_capability: 0.55, user_autonomy: 0.15,
    censorship_resistance: 0.10, foreign_dependence: 0.20,
    monetary_policy_independence: 0.85, digital_literacy_gap: 0.35,
    infrastructure_resilience: 0.80, regulatory_capture: 0.75,
    geopolitical_leverage: 0.70,
  },
  // CBDC-002 — Digital Dollar, AMER → critical, programmable_money_control
  {
    id: "CBDC-002", currency_type: "digital_dollar", region: "AMER",
    surveillance_intensity: 0.80, transaction_monitoring: 0.82,
    programmability_risk: 0.92, privacy_preservation: 0.15,
    financial_inclusion: 0.60, sovereignty_risk: 0.58,
    interoperability: 0.65, cross_border_control: 0.78,
    offline_capability: 0.55, user_autonomy: 0.08,
    censorship_resistance: 0.15, foreign_dependence: 0.18,
    monetary_policy_independence: 0.85, digital_literacy_gap: 0.30,
    infrastructure_resilience: 0.80, regulatory_capture: 0.88,
    geopolitical_leverage: 0.82,
  },
  // CBDC-003 — e-Naira Nigeria, AFRICA → moderate, financial_exclusion_crisis
  {
    id: "CBDC-003", currency_type: "e_naira", region: "AFRICA",
    surveillance_intensity: 0.10, transaction_monitoring: 0.08,
    programmability_risk: 0.12, privacy_preservation: 0.80,
    financial_inclusion: 0.10, sovereignty_risk: 0.12,
    interoperability: 0.30, cross_border_control: 0.10,
    offline_capability: 0.15, user_autonomy: 0.80,
    censorship_resistance: 0.82, foreign_dependence: 0.12,
    monetary_policy_independence: 0.80, digital_literacy_gap: 0.85,
    infrastructure_resilience: 0.20, regulatory_capture: 0.10,
    geopolitical_leverage: 0.08,
  },
  // CBDC-004 — Digital Ruble, EMEA → critical, monetary_sovereignty_capture
  {
    id: "CBDC-004", currency_type: "digital_ruble", region: "EMEA",
    surveillance_intensity: 0.80, transaction_monitoring: 0.75,
    programmability_risk: 0.72, privacy_preservation: 0.12,
    financial_inclusion: 0.55, sovereignty_risk: 0.88,
    interoperability: 0.40, cross_border_control: 0.85,
    offline_capability: 0.50, user_autonomy: 0.18,
    censorship_resistance: 0.15, foreign_dependence: 0.85,
    monetary_policy_independence: 0.20, digital_literacy_gap: 0.40,
    infrastructure_resilience: 0.60, regulatory_capture: 0.78,
    geopolitical_leverage: 0.75,
  },
  // CBDC-005 — Digital Euro, EMEA → high, digital_dollarization_trap
  {
    id: "CBDC-005", currency_type: "digital_euro", region: "EMEA",
    surveillance_intensity: 0.55, transaction_monitoring: 0.50,
    programmability_risk: 0.58, privacy_preservation: 0.52,
    financial_inclusion: 0.68, sovereignty_risk: 0.60,
    interoperability: 0.72, cross_border_control: 0.60,
    offline_capability: 0.65, user_autonomy: 0.50,
    censorship_resistance: 0.55, foreign_dependence: 0.45,
    monetary_policy_independence: 0.22, digital_literacy_gap: 0.35,
    infrastructure_resilience: 0.70, regulatory_capture: 0.58,
    geopolitical_leverage: 0.82,
  },
  // CBDC-006 — Petro Venezuela, LATAM → high, none
  {
    id: "CBDC-006", currency_type: "petro_venezuela", region: "LATAM",
    surveillance_intensity: 0.58, transaction_monitoring: 0.52,
    programmability_risk: 0.55, privacy_preservation: 0.38,
    financial_inclusion: 0.48, sovereignty_risk: 0.58,
    interoperability: 0.42, cross_border_control: 0.60,
    offline_capability: 0.45, user_autonomy: 0.40,
    censorship_resistance: 0.42, foreign_dependence: 0.52,
    monetary_policy_independence: 0.48, digital_literacy_gap: 0.45,
    infrastructure_resilience: 0.48, regulatory_capture: 0.50,
    geopolitical_leverage: 0.48,
  },
  // CBDC-007 — Sand Dollar Bahamas, CARIB → low, none
  {
    id: "CBDC-007", currency_type: "sand_dollar", region: "CARIB",
    surveillance_intensity: 0.12, transaction_monitoring: 0.10,
    programmability_risk: 0.15, privacy_preservation: 0.85,
    financial_inclusion: 0.88, sovereignty_risk: 0.12,
    interoperability: 0.82, cross_border_control: 0.10,
    offline_capability: 0.85, user_autonomy: 0.88,
    censorship_resistance: 0.90, foreign_dependence: 0.10,
    monetary_policy_independence: 0.88, digital_literacy_gap: 0.12,
    infrastructure_resilience: 0.80, regulatory_capture: 0.10,
    geopolitical_leverage: 0.08,
  },
  // CBDC-008 — JAM-DEX Jamaica, CARIB → low, none
  {
    id: "CBDC-008", currency_type: "jam_dex", region: "CARIB",
    surveillance_intensity: 0.14, transaction_monitoring: 0.12,
    programmability_risk: 0.15, privacy_preservation: 0.85,
    financial_inclusion: 0.85, sovereignty_risk: 0.15,
    interoperability: 0.78, cross_border_control: 0.12,
    offline_capability: 0.80, user_autonomy: 0.85,
    censorship_resistance: 0.88, foreign_dependence: 0.12,
    monetary_policy_independence: 0.82, digital_literacy_gap: 0.14,
    infrastructure_resilience: 0.75, regulatory_capture: 0.12,
    geopolitical_leverage: 0.10,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function surveillanceScore(e: Entity): number {
  const raw = (
    e.surveillance_intensity * 0.40
    + e.transaction_monitoring * 0.35
    + (1.0 - e.censorship_resistance) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function exclusionScore(e: Entity): number {
  const raw = (
    (1.0 - e.financial_inclusion) * 0.40
    + e.digital_literacy_gap * 0.35
    + (1.0 - e.offline_capability) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sovereigntyScore(e: Entity): number {
  const raw = (
    e.sovereignty_risk * 0.40
    + e.foreign_dependence * 0.35
    + (1.0 - e.monetary_policy_independence) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function programmabilityScore(e: Entity): number {
  const raw = (
    e.programmability_risk * 0.40
    + e.regulatory_capture * 0.35
    + (1.0 - e.user_autonomy) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(surv: number, excl: number, sov: number, prog: number): number {
  return Math.round((surv * 0.30 + excl * 0.25 + sov * 0.25 + prog * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function cbdcPattern(e: Entity): string {
  if (e.surveillance_intensity > 0.85 && e.transaction_monitoring > 0.80) return "financial_surveillance_state";
  if (e.programmability_risk > 0.85 && e.regulatory_capture > 0.80)       return "programmable_money_control";
  if (e.sovereignty_risk > 0.85 && e.foreign_dependence > 0.80)           return "monetary_sovereignty_capture";
  if ((1.0 - e.financial_inclusion) > 0.80 && e.digital_literacy_gap > 0.75) return "financial_exclusion_crisis";
  if (e.geopolitical_leverage > 0.80 && (1.0 - e.monetary_policy_independence) > 0.75) return "digital_dollarization_trap";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "crise_souveraineté_monétaire_numérique_systémique";
  if (comp >= 40) return "crise_contrôle_monnaie_programmable_majeure";
  if (comp >= 20) return "tension_exclusion_financière_numérique_active";
  return "surveillance_monnaie_numérique_continue";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_souveraineté_monétaire_numérique";
  if (risk === "high")     return "renforcement_cadre_protection_monnaie_numérique";
  if (risk === "moderate") return "surveillance_renforcée_cbdc_inclusion_financière";
  return "veille_souveraineté_monnaie_numérique_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise souveraineté monétaire numérique systémique — contrôle financier total imminent";
  if (risk === "high")     return "🟠 Crise contrôle monnaie programmable majeure détectée";
  if (risk === "moderate") return "🟡 Tension exclusion financière numérique active";
  return "🟢 Souveraineté monnaie numérique sous surveillance";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const surv = surveillanceScore(e);
      const excl = exclusionScore(e);
      const sov  = sovereigntyScore(e);
      const prog = programmabilityScore(e);
      const comp = compositeScore(surv, excl, sov, prog);
      const risk = riskLevel(comp);
      const pat  = cbdcPattern(e);
      const sev  = severity(comp);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);

      return {
        id:              e.entity_id,
        currency_type:          e.currency_type,
        region:                 e.region,
        surveillance_score:     surv,
        exclusion_score:        excl,
        sovereignty_score:      sov,
        programmability_score:  prog,
        composite_score:        comp,
        risk_level:             risk,
        cbdc_pattern:           pat,
        severity:               sev,
        recommended_action:     act,
        signal:                 sig,
        surveillance_intensity: e.surveillance_intensity,
        foreign_dependence:     e.foreign_dependence,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      rc[ent.risk_level]         = (rc[ent.risk_level]         || 0) + 1;
      pc[ent.cbdc_pattern]       = (pc[ent.cbdc_pattern]       || 0) + 1;
      sc[ent.severity]           = (sc[ent.severity]           || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                             395,
      module_name:                           "CBDC & Souveraineté Monnaie Numérique Intelligence Engine",
      total:                                 n,
      critical:                              criticalCount,
      high:                                  highCount,
      moderate:                              moderateCount,
      low:                                   lowCount,
      avg_composite:                         avgComposite,
      pattern_distribution:                  pc,
      risk_distribution:                     rc,
      severity_distribution:                 sc,
      action_distribution:                   ac,
      avg_estimated_cbdc_sovereignty_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/cbdc-sovereignty-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}

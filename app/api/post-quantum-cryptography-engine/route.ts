import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_SYSTEMS = [
  // SY-001 banking_core EMEA critical/quantum_exposure
  { system_id:"SY-001", system_type:"banking_core", region:"EMEA", quantum_vulnerability_score:0.88, pqc_migration_progress:0.08, key_rotation_frequency_score:0.22, entropy_source_quality:0.30, temporal_integrity_score:0.75, timestamp_validation_coverage:0.70, replay_attack_resistance:0.68, certificate_expiry_risk:0.72, cryptographic_agility_score:0.18, hsm_tamper_resistance:0.65, side_channel_resistance:0.25, forward_secrecy_coverage:0.55, zero_trust_crypto_coverage:0.40, nist_pqc_compliance_score:0.05, key_ceremony_rigor_score:0.30, crypto_inventory_completeness:0.35, quantum_key_distribution_readiness:0.05 },
  // SY-002 pki_infrastructure NAMER low
  { system_id:"SY-002", system_type:"pki_infrastructure", region:"NAMER", quantum_vulnerability_score:0.12, pqc_migration_progress:0.90, key_rotation_frequency_score:0.92, entropy_source_quality:0.95, temporal_integrity_score:0.92, timestamp_validation_coverage:0.95, replay_attack_resistance:0.90, certificate_expiry_risk:0.08, cryptographic_agility_score:0.88, hsm_tamper_resistance:0.92, side_channel_resistance:0.90, forward_secrecy_coverage:0.95, zero_trust_crypto_coverage:0.90, nist_pqc_compliance_score:0.92, key_ceremony_rigor_score:0.95, crypto_inventory_completeness:0.90, quantum_key_distribution_readiness:0.85 },
  // SY-003 blockchain_node APAC high/temporal_attack_surface
  { system_id:"SY-003", system_type:"blockchain_node", region:"APAC", quantum_vulnerability_score:0.55, pqc_migration_progress:0.35, key_rotation_frequency_score:0.48, entropy_source_quality:0.60, temporal_integrity_score:0.28, timestamp_validation_coverage:0.35, replay_attack_resistance:0.22, certificate_expiry_risk:0.45, cryptographic_agility_score:0.50, hsm_tamper_resistance:0.55, side_channel_resistance:0.52, forward_secrecy_coverage:0.60, zero_trust_crypto_coverage:0.55, nist_pqc_compliance_score:0.40, key_ceremony_rigor_score:0.55, crypto_inventory_completeness:0.58, quantum_key_distribution_readiness:0.30 },
  // SY-004 iot_fleet LATAM low
  { system_id:"SY-004", system_type:"iot_fleet", region:"LATAM", quantum_vulnerability_score:0.18, pqc_migration_progress:0.75, key_rotation_frequency_score:0.80, entropy_source_quality:0.78, temporal_integrity_score:0.85, timestamp_validation_coverage:0.82, replay_attack_resistance:0.88, certificate_expiry_risk:0.12, cryptographic_agility_score:0.75, hsm_tamper_resistance:0.80, side_channel_resistance:0.78, forward_secrecy_coverage:0.82, zero_trust_crypto_coverage:0.78, nist_pqc_compliance_score:0.80, key_ceremony_rigor_score:0.82, crypto_inventory_completeness:0.78, quantum_key_distribution_readiness:0.70 },
  // SY-005 cloud_hsm EMEA critical/key_compromise_risk
  { system_id:"SY-005", system_type:"cloud_hsm", region:"EMEA", quantum_vulnerability_score:0.60, pqc_migration_progress:0.08, key_rotation_frequency_score:0.15, entropy_source_quality:0.20, temporal_integrity_score:0.55, timestamp_validation_coverage:0.60, replay_attack_resistance:0.65, certificate_expiry_risk:0.58, cryptographic_agility_score:0.22, hsm_tamper_resistance:0.18, side_channel_resistance:0.15, forward_secrecy_coverage:0.20, zero_trust_crypto_coverage:0.18, nist_pqc_compliance_score:0.25, key_ceremony_rigor_score:0.35, crypto_inventory_completeness:0.28, quantum_key_distribution_readiness:0.05 },
  // SY-006 vpn_gateway MEA moderate
  { system_id:"SY-006", system_type:"vpn_gateway", region:"MEA", quantum_vulnerability_score:0.42, pqc_migration_progress:0.55, key_rotation_frequency_score:0.60, entropy_source_quality:0.65, temporal_integrity_score:0.62, timestamp_validation_coverage:0.65, replay_attack_resistance:0.60, certificate_expiry_risk:0.38, cryptographic_agility_score:0.55, hsm_tamper_resistance:0.62, side_channel_resistance:0.58, forward_secrecy_coverage:0.68, zero_trust_crypto_coverage:0.62, nist_pqc_compliance_score:0.58, key_ceremony_rigor_score:0.65, crypto_inventory_completeness:0.60, quantum_key_distribution_readiness:0.45 },
  // SY-007 certificate_authority NAMER high/certificate_collapse
  { system_id:"SY-007", system_type:"certificate_authority", region:"NAMER", quantum_vulnerability_score:0.60, pqc_migration_progress:0.28, key_rotation_frequency_score:0.35, entropy_source_quality:0.50, temporal_integrity_score:0.58, timestamp_validation_coverage:0.55, replay_attack_resistance:0.60, certificate_expiry_risk:0.78, cryptographic_agility_score:0.38, hsm_tamper_resistance:0.55, side_channel_resistance:0.48, forward_secrecy_coverage:0.52, zero_trust_crypto_coverage:0.48, nist_pqc_compliance_score:0.32, key_ceremony_rigor_score:0.22, crypto_inventory_completeness:0.45, quantum_key_distribution_readiness:0.20 },
  // SY-008 quantum_safe_module APAC low
  { system_id:"SY-008", system_type:"quantum_safe_module", region:"APAC", quantum_vulnerability_score:0.05, pqc_migration_progress:0.98, key_rotation_frequency_score:0.95, entropy_source_quality:0.98, temporal_integrity_score:0.96, timestamp_validation_coverage:0.98, replay_attack_resistance:0.96, certificate_expiry_risk:0.03, cryptographic_agility_score:0.95, hsm_tamper_resistance:0.96, side_channel_resistance:0.95, forward_secrecy_coverage:0.98, zero_trust_crypto_coverage:0.96, nist_pqc_compliance_score:0.98, key_ceremony_rigor_score:0.98, crypto_inventory_completeness:0.96, quantum_key_distribution_readiness:0.95 },
];

type CryptoSystem = typeof MOCK_SYSTEMS[0];

function vulnerabilityScore(s: CryptoSystem): number {
  const v = s.quantum_vulnerability_score * 100 * 0.40
           + s.certificate_expiry_risk * 100 * 0.35
           + (1 - s.side_channel_resistance) * 100 * 0.25;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function temporalScore(s: CryptoSystem): number {
  const v = (1 - s.temporal_integrity_score) * 100 * 0.40
           + (1 - s.timestamp_validation_coverage) * 100 * 0.30
           + (1 - s.replay_attack_resistance) * 100 * 0.30;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function resilienceScore(s: CryptoSystem): number {
  const v = (1 - s.hsm_tamper_resistance) * 100 * 0.40
           + (1 - s.forward_secrecy_coverage) * 100 * 0.30
           + (1 - s.zero_trust_crypto_coverage) * 100 * 0.30;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function readinessScore(s: CryptoSystem): number {
  const v = (1 - s.pqc_migration_progress) * 100 * 0.40
           + (1 - s.nist_pqc_compliance_score) * 100 * 0.35
           + (1 - s.quantum_key_distribution_readiness) * 100 * 0.25;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function composite(vuln: number, temp: number, res: number, read: number): number {
  return Math.min(Math.round((vuln * 0.30 + temp * 0.25 + res * 0.25 + read * 0.20) * 100) / 100, 100);
}
function cryptoPattern(s: CryptoSystem): string {
  if (s.quantum_vulnerability_score >= 0.70 && s.nist_pqc_compliance_score <= 0.30) return "quantum_exposure";
  if (s.temporal_integrity_score <= 0.40 || s.replay_attack_resistance <= 0.35)      return "temporal_attack_surface";
  if (s.hsm_tamper_resistance <= 0.40 && s.key_rotation_frequency_score <= 0.40)     return "key_compromise_risk";
  if (s.certificate_expiry_risk >= 0.65 || s.key_ceremony_rigor_score <= 0.30)       return "certificate_collapse";
  if (s.cryptographic_agility_score <= 0.35 && s.crypto_inventory_completeness <= 0.40) return "crypto_agility_deficit";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "compromised"; if (c >= 40) return "exposed"; if (c >= 20) return "hardening"; return "quantum_safe"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "key_compromise_risk") return "emergency_rekeying";
    return "quantum_isolation";
  }
  if (r === "high") {
    if (p === "temporal_attack_surface" || p === "certificate_collapse") return "temporal_hardening";
    return "pqc_migration";
  }
  if (r === "moderate") return "crypto_audit";
  return "no_action";
}
function signal(s: CryptoSystem, pat: string, comp: number): string {
  if (comp < 20) return "Infrastructure cryptographique quantum-safe — résistance post-quantique confirmée, intégrité temporelle forte";
  const labels: Record<string,string> = {
    quantum_exposure:       "Exposition quantique",
    temporal_attack_surface:"Surface d'attaque temporelle",
    key_compromise_risk:    "Risque de compromission de clés",
    certificate_collapse:   "Effondrement certificats",
    crypto_agility_deficit: "Déficit agilité crypto",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — vulnérabilité quantum ${s.quantum_vulnerability_score.toFixed(2)} — intégrité temporelle ${s.temporal_integrity_score.toFixed(2)} — migration PQC ${Math.round(s.pqc_migration_progress*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const systems = MOCK_SYSTEMS.map(s => {
      const vuln = vulnerabilityScore(s), temp = temporalScore(s), res = resilienceScore(s), read = readinessScore(s);
      const comp = composite(vuln, temp, res, read), pat = cryptoPattern(s), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        system_id: s.system_id, system_type: s.system_type, region: s.region,
        crypto_risk: r, crypto_pattern: pat, crypto_severity: sev, recommended_action: act,
        vulnerability_score: vuln, temporal_score: temp, resilience_score: res, readiness_score: read,
        crypto_composite: comp,
        is_quantum_vulnerable: s.quantum_vulnerability_score >= 0.60 || s.nist_pqc_compliance_score <= 0.30 || comp >= 40,
        estimated_quantum_breach_index: Math.min(Math.round(comp/100*(1-s.nist_pqc_compliance_score+0.01)*10*100)/100, 10.0),
        crypto_signal: signal(s, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tvuln=0, ttemp=0, tres=0, tread=0, tcomp=0, tqbi=0, compC=0, qvC=0;
    for (const sys of systems) {
      rc[sys.crypto_risk]       = (rc[sys.crypto_risk]||0)+1;
      pc[sys.crypto_pattern]    = (pc[sys.crypto_pattern]||0)+1;
      sc[sys.crypto_severity]   = (sc[sys.crypto_severity]||0)+1;
      ac[sys.recommended_action] = (ac[sys.recommended_action]||0)+1;
      tvuln += sys.vulnerability_score; ttemp += sys.temporal_score;
      tres  += sys.resilience_score;   tread += sys.readiness_score;
      tcomp += sys.crypto_composite;   tqbi  += sys.estimated_quantum_breach_index;
      if (sys.crypto_severity === "compromised") compC++;
      if (sys.is_quantum_vulnerable) qvC++;
    }
    const n = systems.length;
    return NextResponse.json({ systems, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_crypto_composite: Math.round(tcomp/n*10)/10,
      compromised_count: compC, quantum_vulnerable_count: qvC,
      avg_vulnerability_score: Math.round(tvuln/n*10)/10,
      avg_temporal_score: Math.round(ttemp/n*10)/10,
      avg_resilience_score: Math.round(tres/n*10)/10,
      avg_readiness_score: Math.round(tread/n*10)/10,
      avg_estimated_quantum_breach_index: Math.round(tqbi/n*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/post-quantum-cryptography-engine`)).json());
}

"""
Module 251 — Post-Quantum Cryptography & Temporal Integrity Security Engine
Monitors cryptographic infrastructure for quantum vulnerability, temporal integrity
attacks, post-quantum readiness, and key management health.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class CryptoRisk(str, Enum):
    low      = "low"
    moderate = "moderate"
    high     = "high"
    critical = "critical"


class CryptoPattern(str, Enum):
    none                   = "none"
    quantum_exposure       = "quantum_exposure"
    temporal_attack_surface = "temporal_attack_surface"
    key_compromise_risk    = "key_compromise_risk"
    certificate_collapse   = "certificate_collapse"
    crypto_agility_deficit = "crypto_agility_deficit"


class CryptoSeverity(str, Enum):
    quantum_safe = "quantum_safe"
    hardening    = "hardening"
    exposed      = "exposed"
    compromised  = "compromised"


class CryptoAction(str, Enum):
    no_action          = "no_action"
    crypto_audit       = "crypto_audit"
    pqc_migration      = "pqc_migration"
    temporal_hardening = "temporal_hardening"
    emergency_rekeying = "emergency_rekeying"
    quantum_isolation  = "quantum_isolation"


@dataclass
class CryptoInput:
    system_id: str
    system_type: str   # banking_core/pki_infrastructure/blockchain_node/iot_fleet/cloud_hsm/vpn_gateway/certificate_authority/quantum_safe_module
    region: str
    quantum_vulnerability_score: float       # 0-1, higher=worse
    pqc_migration_progress: float            # 0-1
    key_rotation_frequency_score: float      # 0-1
    entropy_source_quality: float            # 0-1
    temporal_integrity_score: float          # 0-1, lower=worse
    timestamp_validation_coverage: float     # 0-1
    replay_attack_resistance: float          # 0-1
    certificate_expiry_risk: float           # 0-1, higher=worse
    cryptographic_agility_score: float       # 0-1
    hsm_tamper_resistance: float             # 0-1
    side_channel_resistance: float           # 0-1
    forward_secrecy_coverage: float          # 0-1
    zero_trust_crypto_coverage: float        # 0-1
    nist_pqc_compliance_score: float         # 0-1
    key_ceremony_rigor_score: float          # 0-1
    crypto_inventory_completeness: float     # 0-1
    quantum_key_distribution_readiness: float  # 0-1


@dataclass
class CryptoResult:
    system_id: str
    system_type: str
    region: str
    crypto_risk: str
    crypto_pattern: str
    crypto_severity: str
    recommended_action: str
    vulnerability_score: float
    temporal_score: float
    resilience_score: float
    readiness_score: float
    crypto_composite: float
    is_quantum_vulnerable: bool
    estimated_quantum_breach_index: float
    crypto_signal: str

    def to_dict(self) -> Dict:
        return {
            "system_id":                       self.system_id,
            "system_type":                     self.system_type,
            "region":                          self.region,
            "crypto_risk":                     self.crypto_risk,
            "crypto_pattern":                  self.crypto_pattern,
            "crypto_severity":                 self.crypto_severity,
            "recommended_action":              self.recommended_action,
            "vulnerability_score":             self.vulnerability_score,
            "temporal_score":                  self.temporal_score,
            "resilience_score":                self.resilience_score,
            "readiness_score":                 self.readiness_score,
            "crypto_composite":                self.crypto_composite,
            "is_quantum_vulnerable":           self.is_quantum_vulnerable,
            "estimated_quantum_breach_index":  self.estimated_quantum_breach_index,
            "crypto_signal":                   self.crypto_signal,
        }


class PostQuantumCryptographyEngine:
    def __init__(self) -> None:
        self._results: List[CryptoResult] = []

    # ------------------------------------------------------------------ #
    #  Sub-scores                                                          #
    # ------------------------------------------------------------------ #

    def _vulnerability_score(self, i: CryptoInput) -> float:
        s = 0.0
        # quantum_vulnerability_score inverted (high=risk)
        s += i.quantum_vulnerability_score * 100 * 0.40
        # certificate_expiry_risk inverted (high=risk)
        s += i.certificate_expiry_risk * 100 * 0.35
        # side_channel_resistance inverted (low=risk)
        s += (1.0 - i.side_channel_resistance) * 100 * 0.25
        return min(round(s, 2), 100.0)

    def _temporal_score(self, i: CryptoInput) -> float:
        s = 0.0
        # temporal_integrity_score inverted (lower=worse=higher risk)
        s += (1.0 - i.temporal_integrity_score) * 100 * 0.40
        # timestamp_validation_coverage inverted
        s += (1.0 - i.timestamp_validation_coverage) * 100 * 0.30
        # replay_attack_resistance inverted
        s += (1.0 - i.replay_attack_resistance) * 100 * 0.30
        return min(round(s, 2), 100.0)

    def _resilience_score(self, i: CryptoInput) -> float:
        s = 0.0
        # hsm_tamper_resistance inverted
        s += (1.0 - i.hsm_tamper_resistance) * 100 * 0.40
        # forward_secrecy_coverage inverted
        s += (1.0 - i.forward_secrecy_coverage) * 100 * 0.30
        # zero_trust_crypto_coverage inverted
        s += (1.0 - i.zero_trust_crypto_coverage) * 100 * 0.30
        return min(round(s, 2), 100.0)

    def _readiness_score(self, i: CryptoInput) -> float:
        s = 0.0
        # pqc_migration_progress inverted
        s += (1.0 - i.pqc_migration_progress) * 100 * 0.40
        # nist_pqc_compliance_score inverted
        s += (1.0 - i.nist_pqc_compliance_score) * 100 * 0.35
        # quantum_key_distribution_readiness inverted
        s += (1.0 - i.quantum_key_distribution_readiness) * 100 * 0.25
        return min(round(s, 2), 100.0)

    def _composite(self, vuln: float, temp: float, res: float, read: float) -> float:
        return min(round(vuln * 0.30 + temp * 0.25 + res * 0.25 + read * 0.20, 2), 100.0)

    # ------------------------------------------------------------------ #
    #  Risk / severity                                                     #
    # ------------------------------------------------------------------ #

    def _risk(self, c: float) -> CryptoRisk:
        if c >= 60: return CryptoRisk.critical
        if c >= 40: return CryptoRisk.high
        if c >= 20: return CryptoRisk.moderate
        return CryptoRisk.low

    def _severity(self, c: float) -> CryptoSeverity:
        if c >= 60: return CryptoSeverity.compromised
        if c >= 40: return CryptoSeverity.exposed
        if c >= 20: return CryptoSeverity.hardening
        return CryptoSeverity.quantum_safe

    # ------------------------------------------------------------------ #
    #  Pattern detection                                                   #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: CryptoInput) -> CryptoPattern:
        if i.quantum_vulnerability_score >= 0.70 and i.nist_pqc_compliance_score <= 0.30:
            return CryptoPattern.quantum_exposure
        if i.temporal_integrity_score <= 0.40 or i.replay_attack_resistance <= 0.35:
            return CryptoPattern.temporal_attack_surface
        if i.hsm_tamper_resistance <= 0.40 and i.key_rotation_frequency_score <= 0.40:
            return CryptoPattern.key_compromise_risk
        if i.certificate_expiry_risk >= 0.65 or i.key_ceremony_rigor_score <= 0.30:
            return CryptoPattern.certificate_collapse
        if i.cryptographic_agility_score <= 0.35 and i.crypto_inventory_completeness <= 0.40:
            return CryptoPattern.crypto_agility_deficit
        return CryptoPattern.none

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: CryptoRisk, pat: CryptoPattern) -> CryptoAction:
        if risk == CryptoRisk.critical:
            if pat == CryptoPattern.key_compromise_risk: return CryptoAction.emergency_rekeying
            return CryptoAction.quantum_isolation
        if risk == CryptoRisk.high:
            if pat == CryptoPattern.temporal_attack_surface: return CryptoAction.temporal_hardening
            if pat == CryptoPattern.certificate_collapse:    return CryptoAction.temporal_hardening
            return CryptoAction.pqc_migration
        if risk == CryptoRisk.moderate:
            return CryptoAction.crypto_audit
        return CryptoAction.no_action

    # ------------------------------------------------------------------ #
    #  Derived booleans & indices                                          #
    # ------------------------------------------------------------------ #

    def _is_quantum_vulnerable(self, i: CryptoInput, comp: float) -> bool:
        return (i.quantum_vulnerability_score >= 0.60
                or i.nist_pqc_compliance_score <= 0.30
                or comp >= 40)

    def _quantum_breach_index(self, i: CryptoInput, comp: float) -> float:
        return round(min(comp / 100 * (1 - i.nist_pqc_compliance_score + 0.01) * 10, 10.0), 2)

    def _signal(self, i: CryptoInput, pat: CryptoPattern, comp: float) -> str:
        if comp < 20:
            return (
                "Infrastructure cryptographique quantum-safe — résistance post-quantique confirmée, "
                "intégrité temporelle forte"
            )
        labels = {
            CryptoPattern.quantum_exposure:        "Exposition quantique",
            CryptoPattern.temporal_attack_surface: "Surface d'attaque temporelle",
            CryptoPattern.key_compromise_risk:     "Risque de compromission de clés",
            CryptoPattern.certificate_collapse:    "Effondrement certificats",
            CryptoPattern.crypto_agility_deficit:  "Déficit agilité crypto",
        }
        label = labels.get(pat, pat.value.replace("_", " ").title())
        return (
            f"{label} — vulnérabilité quantum {i.quantum_vulnerability_score:.2f}"
            f" — intégrité temporelle {i.temporal_integrity_score:.2f}"
            f" — migration PQC {i.pqc_migration_progress * 100:.0f}%"
            f" — composite {comp:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def assess(self, i: CryptoInput) -> CryptoResult:
        vuln = self._vulnerability_score(i)
        temp = self._temporal_score(i)
        res  = self._resilience_score(i)
        read = self._readiness_score(i)
        comp = self._composite(vuln, temp, res, read)
        risk = self._risk(comp)
        sev  = self._severity(comp)
        pat  = self._pattern(i)
        act  = self._action(risk, pat)
        result = CryptoResult(
            system_id=i.system_id,
            system_type=i.system_type,
            region=i.region,
            crypto_risk=risk.value,
            crypto_pattern=pat.value,
            crypto_severity=sev.value,
            recommended_action=act.value,
            vulnerability_score=vuln,
            temporal_score=temp,
            resilience_score=res,
            readiness_score=read,
            crypto_composite=comp,
            is_quantum_vulnerable=self._is_quantum_vulnerable(i, comp),
            estimated_quantum_breach_index=self._quantum_breach_index(i, comp),
            crypto_signal=self._signal(i, pat, comp),
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: List[CryptoInput]) -> List[CryptoResult]:
        return [self.assess(i) for i in inputs]

    def summary(self) -> Dict:
        if not self._results:
            return {
                "total": 0,
                "risk_counts": {},
                "pattern_counts": {},
                "severity_counts": {},
                "action_counts": {},
                "avg_crypto_composite": 0.0,
                "compromised_count": 0,
                "quantum_vulnerable_count": 0,
                "avg_vulnerability_score": 0.0,
                "avg_temporal_score": 0.0,
                "avg_resilience_score": 0.0,
                "avg_readiness_score": 0.0,
                "avg_estimated_quantum_breach_index": 0.0,
            }
        n = len(self._results)
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        tvuln = ttemp = tres = tread = tcomp = tqbi = 0.0
        comp_count = qv_count = 0
        for r in self._results:
            rc[r.crypto_risk]       = rc.get(r.crypto_risk, 0)       + 1
            pc[r.crypto_pattern]    = pc.get(r.crypto_pattern, 0)    + 1
            sc[r.crypto_severity]   = sc.get(r.crypto_severity, 0)   + 1
            ac[r.recommended_action] = ac.get(r.recommended_action, 0) + 1
            tvuln += r.vulnerability_score
            ttemp += r.temporal_score
            tres  += r.resilience_score
            tread += r.readiness_score
            tcomp += r.crypto_composite
            tqbi  += r.estimated_quantum_breach_index
            if r.crypto_severity == "compromised":  comp_count += 1
            if r.is_quantum_vulnerable:              qv_count   += 1
        return {
            "total":                             n,
            "risk_counts":                       rc,
            "pattern_counts":                    pc,
            "severity_counts":                   sc,
            "action_counts":                     ac,
            "avg_crypto_composite":              round(tcomp / n, 1),
            "compromised_count":                 comp_count,
            "quantum_vulnerable_count":          qv_count,
            "avg_vulnerability_score":           round(tvuln / n, 1),
            "avg_temporal_score":                round(ttemp / n, 1),
            "avg_resilience_score":              round(tres / n, 1),
            "avg_readiness_score":               round(tread / n, 1),
            "avg_estimated_quantum_breach_index": round(tqbi / n, 2),
        }

"""
Zero Trust Network Agent — CaelumSwarm™
Framework: NIST SP 800-207 Zero Trust Architecture
Principles: Never trust, always verify — micro-segmentation — least privilege
"""

import json
import datetime
import hashlib
import ipaddress
import random

ZERO_TRUST_PRINCIPLES = {
    "never_trust_always_verify": "Chaque requête vérifiée, même interne",
    "least_privilege_access": "Accès minimal requis, révoqué après usage",
    "assume_breach": "Concevoir comme si l'attaquant est déjà dans le réseau",
    "verify_explicitly": "Vérifier identité, device, localisation, comportement",
    "micro_segmentation": "Segmenter le réseau au niveau workload individuel",
    "data_classification": "Classer et protéger les données CSDDD selon sensibilité",
}

IDENTITY_PROVIDERS = {
    "primary": {
        "provider": "Azure Active Directory (Entra ID)",
        "protocols": ["OIDC", "SAML 2.0", "OAuth 2.0 + PKCE"],
        "mfa": "FIDO2 + TOTP (no SMS)",
        "conditional_access": True,
        "risk_based_auth": True,
        "phishing_resistant": True,
    },
    "machine_identity": {
        "provider": "HashiCorp Vault + SPIFFE/SPIRE",
        "certificates": "X.509 SVID (SPIFFE Verifiable Identity Document)",
        "rotation": "Toutes les 24h automatique",
        "workload_attestation": ["Kubernetes SA", "AWS IAM Role", "GCP Service Account"],
    },
}

POLICY_ENGINE = {
    "tool": "Open Policy Agent (OPA)",
    "policies": {
        "resource_access": "input.user.role in data.allowed_roles[input.resource]",
        "time_based": "time.hour(time.now_ns()) >= 6 and time.hour(time.now_ns()) <= 22",
        "device_compliance": "input.device.encrypted == true and input.device.os_updated == true",
        "location_risk": "input.location.country in data.allowed_countries",
        "behavioral_anomaly": "input.requests_per_minute < data.baseline[input.user.id] * 3",
    },
    "decision_log": "Kafka → Elasticsearch → Kibana",
}

ACCESS_CONTROL_MATRIX = {
    "caelum_admin": {
        "resources": ["*"],
        "conditions": ["mfa_required", "trusted_device", "caelum_vpn_or_office"],
        "session_timeout_hours": 8,
    },
    "wave_engine_runner": {
        "resources": ["swarm/intelligence/*", "app/api/*", "scripts/wave-*"],
        "conditions": ["mfa_required", "service_account_cert"],
        "session_timeout_hours": 1,
    },
    "compliance_auditor": {
        "resources": ["app/dashboard/*", "reports/*"],
        "conditions": ["mfa_required"],
        "read_only": True,
        "session_timeout_hours": 4,
    },
    "external_partner": {
        "resources": ["reports/shared/*"],
        "conditions": ["mfa_required", "partner_certificate", "approved_ip_range"],
        "session_timeout_hours": 2,
        "data_masking": True,
    },
}

NETWORK_MICRO_SEGMENTATION = {
    "segments": {
        "dmz": {"hosts": ["alb", "cdn"], "ingress": "internet", "egress": "app_tier"},
        "app_tier": {"hosts": ["eks_nodes_app"], "ingress": "dmz", "egress": "data_tier,monitoring"},
        "data_tier": {"hosts": ["postgres", "redis", "rabbitmq"], "ingress": "app_tier", "egress": "backup"},
        "monitoring": {"hosts": ["prometheus", "grafana", "loki"], "ingress": "app_tier,admin", "egress": "alertmanager"},
        "admin": {"hosts": ["bastion", "vault"], "ingress": "zero (VPN only)", "egress": "all (read)"},
        "backup": {"hosts": ["velero", "pgbackrest"], "ingress": "data_tier", "egress": "s3_endpoint"},
    },
    "enforcement": "Istio mTLS + Kubernetes NetworkPolicies + AWS Security Groups",
    "default_deny": True,
}

CONTINUOUS_MONITORING = {
    "tools": {
        "SIEM": "Microsoft Sentinel + Elastic SIEM",
        "EDR": "CrowdStrike Falcon",
        "NDR": "Darktrace AI (Network Detection & Response)",
        "UEBA": "Microsoft Defender for Identity",
        "Threat_Intel": "MISP + VirusTotal + Shodan",
    },
    "detection_rules": {
        "lateral_movement": "Connexion interne inhabituelle → alerte critique",
        "privilege_escalation": "sudo / kubectl exec non-autorisé → blocage + alerte",
        "data_exfiltration": "Volume sortant > baseline × 5 → blocage automatique",
        "credential_stuffing": "5 échecs auth en 60s → lockout + CAPTCHA",
        "c2_communication": "DNS vers domaine < 30j → blocage + investigation",
    },
}

ZERO_TRUST_MATURITY_LEVELS = {
    "traditional": {"score": 0, "description": "Périmètre réseau, VPN basique, confiance implicite interne"},
    "initial": {"score": 25, "description": "MFA déployé, quelques politiques conditionnelles"},
    "advanced": {"score": 50, "description": "Least privilege, micro-segmentation partielle, logs centralisés"},
    "optimal": {"score": 75, "description": "SPIFFE/SPIRE, OPA, monitoring continu, UEBA"},
    "caelum_target": {"score": 90, "description": "Zero Trust complet — NIST SP 800-207 Tier 3"},
}

CONTROL_SCORES = {
    "mfa_fido2":                  {"score": 8,  "category": "identity"},
    "conditional_access":         {"score": 6,  "category": "identity"},
    "spiffe_spire":               {"score": 7,  "category": "identity"},
    "opa_policy_engine":          {"score": 8,  "category": "policy"},
    "least_privilege_rbac":       {"score": 7,  "category": "policy"},
    "micro_segmentation_istio":   {"score": 8,  "category": "network"},
    "kubernetes_network_policies":{"score": 6,  "category": "network"},
    "aws_security_groups":        {"score": 5,  "category": "network"},
    "siem_sentinel":              {"score": 7,  "category": "monitoring"},
    "edr_crowdstrike":            {"score": 6,  "category": "monitoring"},
    "ndr_darktrace":              {"score": 7,  "category": "monitoring"},
    "ueba_defender":              {"score": 6,  "category": "monitoring"},
    "secrets_vault":              {"score": 6,  "category": "data"},
    "encryption_at_rest":         {"score": 5,  "category": "data"},
    "data_classification":        {"score": 4,  "category": "data"},
}

ALLOWED_COUNTRIES = {"FR", "DE", "BE", "NL", "LU", "CH", "GB", "CA", "AU"}
ALLOWED_ROLES_BY_RESOURCE = {
    "*":                      ["caelum_admin"],
    "swarm/intelligence/*":   ["caelum_admin", "wave_engine_runner"],
    "app/api/*":              ["caelum_admin", "wave_engine_runner"],
    "scripts/wave-*":         ["caelum_admin", "wave_engine_runner"],
    "app/dashboard/*":        ["caelum_admin", "compliance_auditor"],
    "reports/*":              ["caelum_admin", "compliance_auditor"],
    "reports/shared/*":       ["caelum_admin", "compliance_auditor", "external_partner"],
}

SEGMENT_CONNECTIVITY = {
    "dmz":        {"allowed_egress": ["app_tier"]},
    "app_tier":   {"allowed_egress": ["data_tier", "monitoring"]},
    "data_tier":  {"allowed_egress": ["backup"]},
    "monitoring": {"allowed_egress": ["alertmanager"]},
    "admin":      {"allowed_egress": ["dmz", "app_tier", "data_tier", "monitoring", "backup"]},
    "backup":     {"allowed_egress": ["s3_endpoint"]},
}

THREAT_RESPONSE_PLAYBOOKS = {
    "lateral_movement": {
        "severity":  "CRITICAL",
        "actions": [
            "Isoler le workload source (kubectl cordon + NetworkPolicy deny-all)",
            "Capturer forensic snapshot (Velero + eBPF trace)",
            "Révoquer tous les tokens de session actifs",
            "Déclencher alerte PagerDuty P1",
            "Notifier SOC + CISO sous 15 minutes",
            "Ouvrir ticket Jira SECURITY-CRITICAL automatique",
        ],
        "auto_block": True,
        "escalation_minutes": 15,
    },
    "privilege_escalation": {
        "severity": "HIGH",
        "actions": [
            "Bloquer la commande (audit webhook Kubernetes)",
            "Invalider le token JWT de l'utilisateur",
            "Alerter l'équipe sécurité (Slack #security-alerts)",
            "Logger dans SIEM avec corrélation comportementale",
        ],
        "auto_block": True,
        "escalation_minutes": 30,
    },
    "data_exfiltration": {
        "severity": "CRITICAL",
        "actions": [
            "Bloquer automatiquement le flux sortant (AWS WAF + SG rule)",
            "Capturer les métadonnées du flux (source, dest, volume)",
            "Alerter DPO + CISO (RGPD/CSDDD obligation notification)",
            "Déclencher investigation Darktrace NDR",
        ],
        "auto_block": True,
        "escalation_minutes": 5,
    },
    "credential_stuffing": {
        "severity": "MEDIUM",
        "actions": [
            "Lockout compte après 5 échecs (60s fenêtre)",
            "Activer CAPTCHA challenge",
            "Envoyer notification MFA out-of-band à l'utilisateur",
            "Bloquer IP source dans WAF (24h)",
        ],
        "auto_block": True,
        "escalation_minutes": 60,
    },
    "c2_communication": {
        "severity": "HIGH",
        "actions": [
            "Bloquer résolution DNS (RPZ — Response Policy Zone)",
            "Isoler le workload suspect",
            "Lancer analyse IOC dans MISP + VirusTotal",
            "Investiguer historique DNS sur 7 jours (Elasticsearch)",
        ],
        "auto_block": True,
        "escalation_minutes": 20,
    },
}

ZERO_TRUST_ROADMAP = [
    {
        "phase": 1,
        "label": "Fondations Identity & Access (M1–M2)",
        "duration": "2 mois",
        "actions": [
            "Déployer SPIFFE/SPIRE sur tous les namespaces Kubernetes",
            "Migrer 100 % des workloads vers FIDO2 (désactiver SMS OTP)",
            "Implémenter OPA admission controller dans EKS",
            "Inventaire complet des identités machine (Vault PKI Engine)",
        ],
        "kpi": "100 % workloads avec SVID — 0 SMS OTP restant",
        "score_delta": "+4 pts",
    },
    {
        "phase": 2,
        "label": "Micro-segmentation complète (M3–M4)",
        "duration": "2 mois",
        "actions": [
            "Activer Istio mTLS STRICT mode sur app_tier ↔ data_tier",
            "Déployer NetworkPolicies deny-all + allow-list explicite",
            "Intégrer AWS Security Groups avec tags dynamiques",
            "Audit de segmentation mensuel automatisé (Trivy + Kube-bench)",
        ],
        "kpi": "Latéralisation impossible sans SVID valide",
        "score_delta": "+4 pts",
    },
    {
        "phase": 3,
        "label": "Monitoring & Threat Intelligence (M4–M5)",
        "duration": "2 mois",
        "actions": [
            "Connecter Darktrace NDR → Microsoft Sentinel (API SIEM)",
            "Déployer UEBA baselines sur tous les comptes humains",
            "Intégrer MISP threat feeds (IOC automatique vers WAF)",
            "Playbooks SOAR automatiques pour les 5 threat types",
        ],
        "kpi": "MTTD < 5 min — MTTR < 30 min pour incidents P1",
        "score_delta": "+4 pts",
    },
    {
        "phase": 4,
        "label": "Conformité NIST SP 800-207 Tier 3 (M5–M6)",
        "duration": "2 mois",
        "actions": [
            "Audit externe Zero Trust maturity (cabinet certifié CISA)",
            "Rapport CSDDD données sensibles + classification automatique",
            "Exercice Red Team (focus: lateral movement + exfiltration)",
            "Certification NIST SP 800-207 Tier 3 documentée",
        ],
        "kpi": "Score maturity ≥ 90/100 — 0 finding critique Red Team",
        "score_delta": "+4 pts",
    },
]


# ── FONCTIONS ──────────────────────────────────────────────────────────────────

def assess_zero_trust_maturity(current_controls: list) -> dict:
    """Évalue la maturité Zero Trust actuelle de CaelumSwarm™."""
    total_score = 0
    max_possible = sum(v["score"] for v in CONTROL_SCORES.values())
    categories = {}
    matched = []
    missing = []

    for ctrl_name, ctrl_data in CONTROL_SCORES.items():
        cat = ctrl_data["category"]
        if ctrl_name in current_controls:
            total_score += ctrl_data["score"]
            matched.append(ctrl_name)
            categories.setdefault(cat, {"earned": 0, "max": 0})
            categories[cat]["earned"] += ctrl_data["score"]
        else:
            missing.append(ctrl_name)
            categories.setdefault(cat, {"earned": 0, "max": 0})
        categories[cat]["max"] += ctrl_data["score"]

    normalized = round((total_score / max_possible) * 100)

    level = "traditional"
    for lvl, data in ZERO_TRUST_MATURITY_LEVELS.items():
        if normalized >= data["score"]:
            level = lvl

    cat_percentages = {
        cat: {
            "score": f"{vals['earned']}/{vals['max']}",
            "pct": f"{round(vals['earned']/vals['max']*100)}%",
        }
        for cat, vals in categories.items()
    }

    return {
        "overall_score": normalized,
        "maturity_level": level,
        "description": ZERO_TRUST_MATURITY_LEVELS[level]["description"],
        "target_score": ZERO_TRUST_MATURITY_LEVELS["caelum_target"]["score"],
        "gap": ZERO_TRUST_MATURITY_LEVELS["caelum_target"]["score"] - normalized,
        "controls_active": len(matched),
        "controls_missing": len(missing),
        "missing_controls": missing,
        "category_breakdown": cat_percentages,
    }


def simulate_access_decision(user: str, resource: str, context: dict) -> dict:
    """Simule une décision d'accès Zero Trust (OPA policy evaluation)."""
    now_hour = datetime.datetime.utcnow().hour
    role = context.get("role", "unknown")
    device_encrypted = context.get("device_encrypted", False)
    device_os_updated = context.get("device_os_updated", False)
    mfa_passed = context.get("mfa_passed", False)
    country = context.get("country", "XX")
    requests_per_minute = context.get("requests_per_minute", 0)
    baseline_rpm = context.get("baseline_rpm", 10)
    service_cert = context.get("service_cert", False)
    partner_cert = context.get("partner_cert", False)
    approved_ip = context.get("approved_ip", False)

    deny_reasons = []
    allow_reasons = []
    risk_score = 0

    # Policy 1 — identité / rôle
    resource_key = resource if resource in ALLOWED_ROLES_BY_RESOURCE else "*"
    allowed_roles = ALLOWED_ROLES_BY_RESOURCE.get(resource_key, [])
    if role not in allowed_roles:
        deny_reasons.append(f"Rôle '{role}' non autorisé pour la ressource '{resource}'")
        risk_score += 40
    else:
        allow_reasons.append(f"Rôle '{role}' autorisé pour '{resource}'")

    # Policy 2 — MFA
    if not mfa_passed:
        deny_reasons.append("MFA non validé (FIDO2/TOTP requis)")
        risk_score += 30
    else:
        allow_reasons.append("MFA validé (FIDO2)")

    # Policy 3 — conformité device
    if not device_encrypted:
        deny_reasons.append("Device non chiffré (BitLocker/FileVault requis)")
        risk_score += 20
    else:
        allow_reasons.append("Device chiffré — conforme")

    if not device_os_updated:
        deny_reasons.append("OS non à jour (patch < 30j requis)")
        risk_score += 15
    else:
        allow_reasons.append("OS à jour — conforme")

    # Policy 4 — localisation
    if country not in ALLOWED_COUNTRIES:
        deny_reasons.append(f"Pays '{country}' hors périmètre autorisé (liste blanche ZTNA)")
        risk_score += 35
    else:
        allow_reasons.append(f"Localisation '{country}' autorisée")

    # Policy 5 — horaire
    if not (6 <= now_hour <= 22):
        deny_reasons.append(f"Accès hors plage autorisée 06h–22h UTC (heure actuelle: {now_hour}h)")
        risk_score += 10
    else:
        allow_reasons.append(f"Horaire autorisé ({now_hour}h UTC)")

    # Policy 6 — anomalie comportementale
    if requests_per_minute > baseline_rpm * 3:
        deny_reasons.append(
            f"Anomalie comportementale: {requests_per_minute} req/min "
            f"(baseline × 3 = {baseline_rpm * 3})"
        )
        risk_score += 50

    # Policy 7 — certificats spécifiques par rôle
    if role == "wave_engine_runner" and not service_cert:
        deny_reasons.append("Certificat service SVID requis pour wave_engine_runner")
        risk_score += 25
    if role == "external_partner":
        if not partner_cert:
            deny_reasons.append("Certificat partenaire X.509 requis")
            risk_score += 30
        if not approved_ip:
            deny_reasons.append("IP source hors plage partenaire approuvée")
            risk_score += 20

    decision = "DENY" if deny_reasons else "ALLOW"
    risk_score = min(risk_score, 100)

    acm = ACCESS_CONTROL_MATRIX.get(role, {})
    session_config = None
    if decision == "ALLOW":
        session_config = {
            "timeout_hours": acm.get("session_timeout_hours", 1),
            "read_only": acm.get("read_only", False),
            "data_masking": acm.get("data_masking", False),
            "token_id": hashlib.sha256(
                f"{user}{resource}{datetime.datetime.utcnow().isoformat()}".encode()
            ).hexdigest()[:16],
        }

    return {
        "decision": decision,
        "user": user,
        "resource": resource,
        "role": role,
        "risk_score": risk_score,
        "allow_reasons": allow_reasons,
        "deny_reasons": deny_reasons,
        "session_config": session_config,
        "evaluated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "policy_engine": "OPA — NIST SP 800-207",
    }


def design_micro_segmentation_policy(source: str, destination: str) -> dict:
    """Conçoit la politique de micro-segmentation entre deux composants."""
    src_segment = None
    dst_segment = None

    for seg_name, seg_data in NETWORK_MICRO_SEGMENTATION["segments"].items():
        if source in seg_data["hosts"] or source == seg_name:
            src_segment = seg_name
        if destination in seg_data["hosts"] or destination == seg_name:
            dst_segment = seg_name

    if not src_segment:
        src_segment = source
    if not dst_segment:
        dst_segment = destination

    allowed_egress = SEGMENT_CONNECTIVITY.get(src_segment, {}).get("allowed_egress", [])
    flow_allowed = dst_segment in allowed_egress

    k8s_policy = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {"name": f"allow-{src_segment}-to-{dst_segment}", "namespace": "caelumswarm"},
        "spec": {
            "podSelector": {"matchLabels": {"segment": dst_segment}},
            "policyTypes": ["Ingress"],
            "ingress": [
                {
                    "from": [{"podSelector": {"matchLabels": {"segment": src_segment}}}],
                    "ports": [{"protocol": "TCP", "port": 443}],
                }
            ] if flow_allowed else [],
        },
    }

    istio_policy = {
        "apiVersion": "security.istio.io/v1beta1",
        "kind": "AuthorizationPolicy",
        "metadata": {"name": f"authz-{src_segment}-{dst_segment}", "namespace": "caelumswarm"},
        "spec": {
            "selector": {"matchLabels": {"segment": dst_segment}},
            "action": "ALLOW" if flow_allowed else "DENY",
            "rules": [
                {
                    "from": [{"source": {"principals": [f"cluster.local/ns/caelumswarm/sa/{src_segment}-sa"]}}],
                    "to": [{"operation": {"methods": ["GET", "POST"]}}],
                }
            ] if flow_allowed else [],
        },
    }

    return {
        "source": source,
        "destination": destination,
        "source_segment": src_segment,
        "destination_segment": dst_segment,
        "flow_allowed": flow_allowed,
        "verdict": "PERMIT (flux autorisé par politique de segmentation)" if flow_allowed
                   else "DENY (flux bloqué — default-deny actif)",
        "enforcement": NETWORK_MICRO_SEGMENTATION["enforcement"],
        "mtls_required": True,
        "spiffe_svid_required": True,
        "kubernetes_network_policy": k8s_policy,
        "istio_authorization_policy": istio_policy,
        "aws_security_group_rule": (
            f"sg-caelum-{src_segment} → sg-caelum-{dst_segment} TCP/443 ALLOW"
            if flow_allowed
            else f"sg-caelum-{src_segment} → sg-caelum-{dst_segment} ALL DENY (implicit)"
        ),
    }


def simulate_threat_response(threat_type: str, source_ip: str) -> dict:
    """Simule la réponse automatique à une menace détectée."""
    try:
        ip_obj = ipaddress.ip_address(source_ip)
        ip_is_internal = ip_obj.is_private
    except ValueError:
        ip_obj = None
        ip_is_internal = False

    playbook = THREAT_RESPONSE_PLAYBOOKS.get(threat_type)
    if not playbook:
        return {
            "error": f"Type de menace inconnu: '{threat_type}'",
            "known_types": list(THREAT_RESPONSE_PLAYBOOKS.keys()),
        }

    detection_rule = CONTINUOUS_MONITORING["detection_rules"].get(threat_type, "N/A")

    incident_id = f"INC-{hashlib.sha256(f'{threat_type}{source_ip}{datetime.datetime.utcnow()}'.encode()).hexdigest()[:8].upper()}"

    timeline = []
    t = datetime.datetime.utcnow()
    timeline.append({"T+0s":  "Détection par NDR Darktrace / règle SIEM"})
    timeline.append({"T+5s":  "Corrélation UEBA — score risque calculé"})
    timeline.append({"T+10s": "Décision automatique OPA — blocage approuvé" if playbook["auto_block"] else "Alerte envoyée — blocage manuel requis"})
    timeline.append({"T+15s": "Exécution playbook SOAR — actions déclenchées"})
    timeline.append({f"T+{playbook['escalation_minutes']}m": "Escalade SOC si incident non clôturé"})

    return {
        "incident_id": incident_id,
        "threat_type": threat_type,
        "severity": playbook["severity"],
        "source_ip": source_ip,
        "ip_classification": "INTERNE (réseau privé)" if ip_is_internal else "EXTERNE (internet)",
        "detection_rule": detection_rule,
        "auto_block": playbook["auto_block"],
        "actions_taken": playbook["actions"],
        "escalation_sla_minutes": playbook["escalation_minutes"],
        "response_timeline": timeline,
        "tools_involved": [
            CONTINUOUS_MONITORING["tools"]["NDR"],
            CONTINUOUS_MONITORING["tools"]["SIEM"],
            CONTINUOUS_MONITORING["tools"]["UEBA"],
        ],
        "forensic_snapshot": threat_type in ("lateral_movement", "data_exfiltration"),
        "status": "CONTAINED" if playbook["auto_block"] else "INVESTIGATING",
        "detected_at": t.isoformat() + "Z",
    }


def generate_zero_trust_report() -> dict:
    """Génère un rapport Zero Trust maturity pour CaelumSwarm™."""
    active_controls = [
        "mfa_fido2", "conditional_access", "spiffe_spire",
        "opa_policy_engine", "least_privilege_rbac",
        "micro_segmentation_istio", "kubernetes_network_policies",
        "siem_sentinel", "edr_crowdstrike", "ndr_darktrace", "ueba_defender",
        "secrets_vault", "encryption_at_rest",
    ]
    maturity = assess_zero_trust_maturity(active_controls)

    scenarios = [
        {
            "id": "S1",
            "description": "Admin CaelumSwarm — accès légitime depuis France",
            "result": simulate_access_decision(
                user="alice.martin@caelumswarm.io",
                resource="*",
                context={
                    "role": "caelum_admin",
                    "mfa_passed": True,
                    "device_encrypted": True,
                    "device_os_updated": True,
                    "country": "FR",
                    "requests_per_minute": 8,
                    "baseline_rpm": 10,
                },
            ),
        },
        {
            "id": "S2",
            "description": "Partenaire externe — tentative depuis Russie (hors liste blanche)",
            "result": simulate_access_decision(
                user="partner@external.com",
                resource="reports/shared/*",
                context={
                    "role": "external_partner",
                    "mfa_passed": True,
                    "device_encrypted": True,
                    "device_os_updated": True,
                    "country": "RU",
                    "requests_per_minute": 5,
                    "baseline_rpm": 5,
                    "partner_cert": True,
                    "approved_ip": False,
                },
            ),
        },
        {
            "id": "S3",
            "description": "Anomalie comportementale — wave_engine_runner (rate 90 req/min vs baseline 10)",
            "result": simulate_access_decision(
                user="svc-wave-engine@caelumswarm.io",
                resource="swarm/intelligence/*",
                context={
                    "role": "wave_engine_runner",
                    "mfa_passed": True,
                    "device_encrypted": True,
                    "device_os_updated": True,
                    "country": "FR",
                    "requests_per_minute": 90,
                    "baseline_rpm": 10,
                    "service_cert": True,
                },
            ),
        },
    ]

    seg_policies = [
        design_micro_segmentation_policy("eks_nodes_app", "postgres"),
        design_micro_segmentation_policy("alb", "eks_nodes_app"),
        design_micro_segmentation_policy("prometheus", "postgres"),
    ]

    opa_evaluations = []
    for policy_name, policy_rego in POLICY_ENGINE["policies"].items():
        opa_evaluations.append({
            "policy": policy_name,
            "rego": policy_rego,
            "engine": "OPA v0.65+",
            "bundle": "caelumswarm/zero-trust",
        })

    threat_sim = simulate_threat_response("lateral_movement", "10.0.2.47")

    return {
        "report_title": "Zero Trust Network Report — CaelumSwarm™",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "framework": "NIST SP 800-207 Zero Trust Architecture",
        "maturity_assessment": maturity,
        "access_decision_scenarios": scenarios,
        "micro_segmentation_policies": seg_policies,
        "opa_policy_evaluations": opa_evaluations,
        "threat_simulation": threat_sim,
        "roadmap": ZERO_TRUST_ROADMAP,
    }


# ── BLOC PRINCIPAL ─────────────────────────────────────────────────────────────

def _separator(title: str, width: int = 72) -> None:
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def _subsection(title: str, width: int = 72) -> None:
    print()
    print("─" * width)
    print(f"  {title}")
    print("─" * width)


def _print_json(data: object, indent: int = 2) -> None:
    print(json.dumps(data, indent=indent, ensure_ascii=False, default=str))


def main() -> None:
    WIDTH = 72

    # ── 1. EN-TÊTE ────────────────────────────────────────────────────────────
    print("=" * WIDTH)
    print("  ZERO TRUST NETWORK REPORT — CaelumSwarm™")
    print(f"  Généré le : {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("  Framework : NIST SP 800-207 Zero Trust Architecture")
    print("=" * WIDTH)

    # ── 2. PRINCIPES NIST SP 800-207 ─────────────────────────────────────────
    _separator("2. PRINCIPES NIST SP 800-207 (6 PILIERS ZERO TRUST)")
    for i, (key, value) in enumerate(ZERO_TRUST_PRINCIPLES.items(), 1):
        print(f"  [{i}] {key.replace('_', ' ').upper()}")
        print(f"       → {value}")

    # ── 3. IDENTITY PROVIDERS ─────────────────────────────────────────────────
    _separator("3. IDENTITY PROVIDERS")

    _subsection("3.1 Human Identity — Azure Active Directory (Entra ID)")
    ip_human = IDENTITY_PROVIDERS["primary"]
    print(f"  Provider       : {ip_human['provider']}")
    print(f"  Protocoles     : {', '.join(ip_human['protocols'])}")
    print(f"  MFA            : {ip_human['mfa']}")
    print(f"  Accès cond.    : {'Oui' if ip_human['conditional_access'] else 'Non'}")
    print(f"  Auth basée risque : {'Oui' if ip_human['risk_based_auth'] else 'Non'}")
    print(f"  Anti-phishing  : {'Oui' if ip_human['phishing_resistant'] else 'Non'}")

    _subsection("3.2 Machine Identity — HashiCorp Vault + SPIFFE/SPIRE")
    ip_machine = IDENTITY_PROVIDERS["machine_identity"]
    print(f"  Provider       : {ip_machine['provider']}")
    print(f"  Certificats    : {ip_machine['certificates']}")
    print(f"  Rotation       : {ip_machine['rotation']}")
    print(f"  Attestation    : {', '.join(ip_machine['workload_attestation'])}")

    # ── 4. DÉCISIONS D'ACCÈS (3 SCÉNARIOS) ───────────────────────────────────
    _separator("4. SIMULATION DÉCISIONS D'ACCÈS ZERO TRUST (3 SCÉNARIOS)")

    scenarios_data = [
        {
            "id": "S1",
            "description": "Admin CaelumSwarm — accès légitime depuis France",
            "result": simulate_access_decision(
                user="alice.martin@caelumswarm.io",
                resource="*",
                context={
                    "role": "caelum_admin",
                    "mfa_passed": True,
                    "device_encrypted": True,
                    "device_os_updated": True,
                    "country": "FR",
                    "requests_per_minute": 8,
                    "baseline_rpm": 10,
                },
            ),
        },
        {
            "id": "S2",
            "description": "Partenaire externe — tentative depuis Russie (hors liste blanche)",
            "result": simulate_access_decision(
                user="partner@external.com",
                resource="reports/shared/*",
                context={
                    "role": "external_partner",
                    "mfa_passed": True,
                    "device_encrypted": True,
                    "device_os_updated": True,
                    "country": "RU",
                    "requests_per_minute": 5,
                    "baseline_rpm": 5,
                    "partner_cert": True,
                    "approved_ip": False,
                },
            ),
        },
        {
            "id": "S3",
            "description": "Anomalie comportementale — wave_engine_runner (90 req/min vs baseline 10)",
            "result": simulate_access_decision(
                user="svc-wave-engine@caelumswarm.io",
                resource="swarm/intelligence/*",
                context={
                    "role": "wave_engine_runner",
                    "mfa_passed": True,
                    "device_encrypted": True,
                    "device_os_updated": True,
                    "country": "FR",
                    "requests_per_minute": 90,
                    "baseline_rpm": 10,
                    "service_cert": True,
                },
            ),
        },
    ]

    for sc in scenarios_data:
        r = sc["result"]
        verdict_icon = "[ALLOW]" if r["decision"] == "ALLOW" else "[DENY] "
        _subsection(f"Scénario {sc['id']} — {sc['description']}")
        print(f"  Verdict        : {verdict_icon} {r['decision']}")
        print(f"  Utilisateur    : {r['user']}")
        print(f"  Ressource      : {r['resource']}")
        print(f"  Rôle           : {r['role']}")
        print(f"  Score risque   : {r['risk_score']}/100")
        if r["allow_reasons"]:
            print("  Autorisations  :")
            for reason in r["allow_reasons"]:
                print(f"    + {reason}")
        if r["deny_reasons"]:
            print("  Refus          :")
            for reason in r["deny_reasons"]:
                print(f"    - {reason}")
        if r["session_config"]:
            sc_cfg = r["session_config"]
            print(f"  Session        : timeout={sc_cfg['timeout_hours']}h "
                  f"| read_only={sc_cfg['read_only']} "
                  f"| masking={sc_cfg['data_masking']}")
            print(f"  Token ID       : {sc_cfg['token_id']}")

    # ── 5. MICRO-SEGMENTATION ─────────────────────────────────────────────────
    _separator("5. MICRO-SEGMENTATION RÉSEAU (6 SEGMENTS + ENFORCEMENT)")
    print(f"  Enforcement : {NETWORK_MICRO_SEGMENTATION['enforcement']}")
    print(f"  Default-deny : {'OUI' if NETWORK_MICRO_SEGMENTATION['default_deny'] else 'NON'}")
    print()
    for seg_name, seg_data in NETWORK_MICRO_SEGMENTATION["segments"].items():
        hosts = ", ".join(seg_data["hosts"])
        print(f"  [{seg_name.upper():12s}] hosts={hosts}")
        print(f"               ingress={seg_data['ingress']} | egress={seg_data['egress']}")

    _subsection("5.1 Politiques de micro-segmentation simulées")
    seg_tests = [
        ("eks_nodes_app", "postgres",    "app_tier → data_tier"),
        ("alb",           "eks_nodes_app", "dmz → app_tier"),
        ("prometheus",    "postgres",    "monitoring → data_tier (doit être DENY)"),
    ]
    for src, dst, label in seg_tests:
        pol = design_micro_segmentation_policy(src, dst)
        print(f"\n  {label}")
        print(f"    {src} → {dst} : {pol['verdict']}")
        print(f"    mTLS requis  : {'OUI' if pol['mtls_required'] else 'NON'}")
        print(f"    SVID requis  : {'OUI' if pol['spiffe_svid_required'] else 'NON'}")
        print(f"    AWS SG rule  : {pol['aws_security_group_rule']}")

    # ── 6. OPA POLICY EVALUATION ──────────────────────────────────────────────
    _separator("6. OPA POLICY EVALUATION (Open Policy Agent)")
    print(f"  Moteur : {POLICY_ENGINE['tool']}")
    print(f"  Logs   : {POLICY_ENGINE['decision_log']}")
    print()
    for i, (policy_name, rego) in enumerate(POLICY_ENGINE["policies"].items(), 1):
        print(f"  [{i}] {policy_name}")
        print(f"       Rego → {rego}")

    # ── 7. THREAT DETECTION & RESPONSE ───────────────────────────────────────
    _separator("7. THREAT DETECTION & RESPONSE — SIMULATION lateral_movement")
    threat = simulate_threat_response("lateral_movement", "10.0.2.47")
    print(f"  Incident ID    : {threat['incident_id']}")
    print(f"  Type menace    : {threat['threat_type']}")
    print(f"  Sévérité       : {threat['severity']}")
    print(f"  IP source      : {threat['source_ip']} ({threat['ip_classification']})")
    print(f"  Règle déclench.: {threat['detection_rule']}")
    print(f"  Blocage auto   : {'OUI' if threat['auto_block'] else 'NON'}")
    print(f"  Snapshot forens: {'OUI' if threat['forensic_snapshot'] else 'NON'}")
    print(f"  Statut final   : {threat['status']}")
    print()
    print("  Actions exécutées :")
    for action in threat["actions_taken"]:
        print(f"    • {action}")
    print()
    print("  Timeline de réponse :")
    for step in threat["response_timeline"]:
        for ts, event in step.items():
            print(f"    {ts:10s} → {event}")

    # ── 8. MATURITY ASSESSMENT ────────────────────────────────────────────────
    _separator("8. MATURITY ASSESSMENT — CaelumSwarm™")
    active_controls = [
        "mfa_fido2", "conditional_access", "spiffe_spire",
        "opa_policy_engine", "least_privilege_rbac",
        "micro_segmentation_istio", "kubernetes_network_policies",
        "siem_sentinel", "edr_crowdstrike", "ndr_darktrace", "ueba_defender",
        "secrets_vault", "encryption_at_rest",
    ]
    maturity = assess_zero_trust_maturity(active_controls)

    print(f"  Score actuel   : {maturity['overall_score']}/100")
    print(f"  Score cible    : {maturity['target_score']}/100 (NIST SP 800-207 Tier 3)")
    print(f"  Écart restant  : {maturity['gap']} points")
    print(f"  Niveau atteint : {maturity['maturity_level'].upper()}")
    print(f"  Description    : {maturity['description']}")
    print(f"  Contrôles actifs  : {maturity['controls_active']}")
    print(f"  Contrôles manquants : {maturity['controls_missing']}")
    if maturity["missing_controls"]:
        print(f"  Manquants      : {', '.join(maturity['missing_controls'])}")
    print()
    print("  Répartition par catégorie :")
    for cat, vals in maturity["category_breakdown"].items():
        print(f"    [{cat.upper():12s}] {vals['score']:8s}  {vals['pct']:>5s}")

    # ── 9. ROADMAP ZERO TRUST ─────────────────────────────────────────────────
    _separator("9. ROADMAP ZERO TRUST — 6 MOIS / 4 ÉTAPES")
    for phase in ZERO_TRUST_ROADMAP:
        print(f"\n  Phase {phase['phase']} — {phase['label']} ({phase['duration']})")
        print(f"  KPI       : {phase['kpi']}")
        print(f"  Impact    : {phase['score_delta']}")
        print("  Actions   :")
        for action in phase["actions"]:
            print(f"    • {action}")

    # ── 10. CONCLUSION ────────────────────────────────────────────────────────
    _separator("10. STATUT FINAL")
    print()
    print("  Zero Trust Network Agent — PRET")
    print("  Conformité : NIST SP 800-207 / SPIFFE / OPA / Darktrace")
    print()
    print("  Composants actifs :")
    print("    [OK] SPIFFE/SPIRE      — identités machine X.509 SVID")
    print("    [OK] Open Policy Agent — évaluation politique temps-réel")
    print("    [OK] Istio mTLS        — chiffrement inter-services")
    print("    [OK] Darktrace NDR     — détection anomalies comportementales")
    print("    [OK] Microsoft Sentinel— corrélation SIEM cloud-native")
    print("    [OK] CrowdStrike Falcon— protection endpoints (EDR)")
    print("    [OK] HashiCorp Vault   — gestion secrets + PKI")
    print()
    print(f"  Score maturité CaelumSwarm™ : {maturity['overall_score']}/100")
    print(f"  Objectif 6 mois            : {maturity['target_score']}/100 (NIST Tier 3)")
    print()
    print("=" * WIDTH)
    print("  Zero Trust Network Agent — PRÊT (NIST SP 800-207 / SPIFFE / OPA / Darktrace)")
    print("=" * WIDTH)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Kubernetes Security Agent — CaelumSwarm™
CSDDD 2024 Compliance | K8s 1.29 | RBAC | OPA Gatekeeper | Falco | CIS Benchmark
stdlib uniquement — aucune dépendance externe
"""

import json
import datetime
import hashlib
import random
import sys

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

KUBERNETES_VERSION = "1.29"

# ─────────────────────────────────────────────────────────────────────────────
# RBAC CONFIGURATION — Least Privilege / CaelumSwarm™
# ─────────────────────────────────────────────────────────────────────────────

RBAC_CONFIG = {
    "cluster_roles": {
        "caelum-admin": {
            "description": "Full cluster administration — restricted to ops team",
            "rules": [
                {
                    "apiGroups": ["*"],
                    "resources": ["*"],
                    "verbs": ["*"],
                },
            ],
            "service_account": {
                "name": "caelum-admin-sa",
                "namespace": "caelum-system",
                "irsa_role_arn": "arn:aws:iam::123456789012:role/CaelumAdminRole",
            },
        },
        "caelum-developer": {
            "description": "Deploy and manage workloads in caelum-* namespaces",
            "rules": [
                {
                    "apiGroups": ["apps", "batch"],
                    "resources": ["deployments", "replicasets", "statefulsets", "jobs", "cronjobs"],
                    "verbs": ["get", "list", "watch", "create", "update", "patch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["pods", "services", "configmaps", "persistentvolumeclaims"],
                    "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["secrets"],
                    "verbs": ["get", "list"],
                },
                {
                    "apiGroups": ["networking.k8s.io"],
                    "resources": ["ingresses", "networkpolicies"],
                    "verbs": ["get", "list", "watch"],
                },
            ],
            "service_account": {
                "name": "caelum-developer-sa",
                "namespace": "caelum-dev",
                "irsa_role_arn": "arn:aws:iam::123456789012:role/CaelumDeveloperRole",
            },
        },
        "caelum-readonly": {
            "description": "Read-only access to all CaelumSwarm resources",
            "rules": [
                {
                    "apiGroups": ["", "apps", "batch", "networking.k8s.io", "autoscaling"],
                    "resources": [
                        "pods", "deployments", "services", "configmaps", "namespaces",
                        "replicasets", "statefulsets", "daemonsets", "jobs", "cronjobs",
                        "ingresses", "networkpolicies", "horizontalpodautoscalers",
                    ],
                    "verbs": ["get", "list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["secrets"],
                    "verbs": [],  # NO access to secrets
                },
            ],
            "service_account": {
                "name": "caelum-readonly-sa",
                "namespace": "caelum-monitoring",
                "irsa_role_arn": "arn:aws:iam::123456789012:role/CaelumReadOnlyRole",
            },
        },
        "caelum-engine-runner": {
            "description": "Run wave engines — minimal permissions for pod execution",
            "rules": [
                {
                    "apiGroups": [""],
                    "resources": ["pods"],
                    "verbs": ["get", "list", "watch", "create", "delete"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["pods/log"],
                    "verbs": ["get", "list"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["configmaps"],
                    "verbs": ["get", "list", "watch"],
                },
                {
                    "apiGroups": ["batch"],
                    "resources": ["jobs"],
                    "verbs": ["get", "list", "watch", "create"],
                },
            ],
            "service_account": {
                "name": "caelum-engine-runner-sa",
                "namespace": "caelum-engines",
                "irsa_role_arn": "arn:aws:iam::123456789012:role/CaelumEngineRunnerRole",
            },
        },
        "caelum-auditor": {
            "description": "CSDDD audit trail — read-only including events and logs",
            "rules": [
                {
                    "apiGroups": [""],
                    "resources": ["events", "pods", "pods/log", "nodes", "namespaces", "serviceaccounts"],
                    "verbs": ["get", "list", "watch"],
                },
                {
                    "apiGroups": ["rbac.authorization.k8s.io"],
                    "resources": ["clusterroles", "clusterrolebindings", "roles", "rolebindings"],
                    "verbs": ["get", "list", "watch"],
                },
                {
                    "apiGroups": ["audit.k8s.io"],
                    "resources": ["*"],
                    "verbs": ["get", "list", "watch"],
                },
                {
                    "apiGroups": ["policy"],
                    "resources": ["podsecuritypolicies"],
                    "verbs": ["get", "list"],
                },
            ],
            "service_account": {
                "name": "caelum-auditor-sa",
                "namespace": "caelum-audit",
                "irsa_role_arn": "arn:aws:iam::123456789012:role/CaelumAuditorRole",
            },
        },
    },
    "role_bindings": {
        "caelum-admin-binding": {
            "kind": "ClusterRoleBinding",
            "role": "caelum-admin",
            "subjects": ["team:ops@caelum-partners.com"],
        },
        "caelum-developer-binding": {
            "kind": "RoleBinding",
            "namespace": "caelum-dev",
            "role": "caelum-developer",
            "subjects": ["team:engineers@caelum-partners.com"],
        },
        "caelum-readonly-binding": {
            "kind": "ClusterRoleBinding",
            "role": "caelum-readonly",
            "subjects": ["team:analysts@caelum-partners.com"],
        },
        "caelum-engine-runner-binding": {
            "kind": "RoleBinding",
            "namespace": "caelum-engines",
            "role": "caelum-engine-runner",
            "subjects": ["serviceaccount:caelum-engine-runner-sa"],
        },
        "caelum-auditor-binding": {
            "kind": "ClusterRoleBinding",
            "role": "caelum-auditor",
            "subjects": ["team:csddd-auditors@caelum-partners.com"],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# POD SECURITY STANDARDS — Restricted Profile
# ─────────────────────────────────────────────────────────────────────────────

POD_SECURITY_STANDARDS = {
    "profile": "restricted",
    "kubernetes_version": KUBERNETES_VERSION,
    "namespace_labels": {
        "pod-security.kubernetes.io/enforce": "restricted",
        "pod-security.kubernetes.io/enforce-version": "v1.29",
        "pod-security.kubernetes.io/audit": "restricted",
        "pod-security.kubernetes.io/warn": "restricted",
    },
    "required_fields": {
        "securityContext": {
            "runAsNonRoot": True,
            "runAsUser": {"minimum": 1000, "description": "UID >= 1000, never 0"},
            "runAsGroup": {"minimum": 1000, "description": "GID >= 1000"},
            "fsGroup": {"minimum": 1000},
            "seccompProfile": {
                "type": "RuntimeDefault",
                "alternative": "Localhost",
            },
            "supplementalGroups": {"description": "All GIDs must be >= 1000"},
        },
        "containers[*].securityContext": {
            "allowPrivilegeEscalation": False,
            "readOnlyRootFilesystem": True,
            "privileged": False,
            "capabilities": {
                "drop": ["ALL"],
                "add": [],  # NET_BIND_SERVICE only if port < 1024 strictly required
            },
        },
        "volumes": {
            "allowed_types": [
                "configMap", "csi", "downwardAPI", "emptyDir",
                "ephemeral", "persistentVolumeClaim", "projected", "secret",
            ],
            "forbidden_types": [
                "hostPath", "hostIPC", "hostPID", "hostNetwork",
                "nfs", "iscsi", "fc", "flexVolume", "flocker", "gcePersistentDisk",
            ],
        },
    },
    "example_compliant_pod": {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": "caelum-engine-example",
            "namespace": "caelum-engines",
            "labels": {"app": "wave-engine", "version": "v1.0"},
        },
        "spec": {
            "serviceAccountName": "caelum-engine-runner-sa",
            "automountServiceAccountToken": False,
            "securityContext": {
                "runAsNonRoot": True,
                "runAsUser": 1001,
                "runAsGroup": 1001,
                "fsGroup": 1001,
                "seccompProfile": {"type": "RuntimeDefault"},
            },
            "containers": [
                {
                    "name": "engine",
                    "image": "caelum-registry.io/wave-engine:1.29-slim",
                    "securityContext": {
                        "allowPrivilegeEscalation": False,
                        "readOnlyRootFilesystem": True,
                        "privileged": False,
                        "capabilities": {"drop": ["ALL"]},
                    },
                    "resources": {
                        "requests": {"cpu": "100m", "memory": "128Mi"},
                        "limits": {"cpu": "500m", "memory": "512Mi"},
                    },
                    "livenessProbe": {
                        "httpGet": {"path": "/healthz", "port": 8080},
                        "initialDelaySeconds": 10,
                        "periodSeconds": 30,
                    },
                    "readinessProbe": {
                        "httpGet": {"path": "/ready", "port": 8080},
                        "initialDelaySeconds": 5,
                        "periodSeconds": 10,
                    },
                }
            ],
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# NETWORK POLICIES — Default Deny All + Explicit Whitelist
# ─────────────────────────────────────────────────────────────────────────────

NETWORK_POLICIES = {
    "default_deny": {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {
            "name": "default-deny-all",
            "namespace": "caelum-engines",
        },
        "spec": {
            "podSelector": {},  # applies to ALL pods in namespace
            "policyTypes": ["Ingress", "Egress"],
            "ingress": [],  # deny all ingress
            "egress": [],   # deny all egress
        },
        "description": "Default deny-all — applied to all CaelumSwarm namespaces",
    },
    "whitelist_policies": {
        "wave-engine-to-api-gateway": {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "allow-wave-engine-to-api-gateway",
                "namespace": "caelum-engines",
            },
            "spec": {
                "podSelector": {"matchLabels": {"app": "wave-engine"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "to": [{"podSelector": {"matchLabels": {"app": "api-gateway"}}}],
                        "ports": [{"protocol": "TCP", "port": 8080}],
                    }
                ],
            },
            "description": "wave-engine → api-gateway (port 8080)",
        },
        "api-gateway-to-redis": {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "allow-api-gateway-to-redis",
                "namespace": "caelum-data",
            },
            "spec": {
                "podSelector": {"matchLabels": {"app": "api-gateway"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "to": [{"podSelector": {"matchLabels": {"app": "redis"}}}],
                        "ports": [{"protocol": "TCP", "port": 6379}],
                    }
                ],
            },
            "description": "api-gateway → redis (port 6379)",
        },
        "api-gateway-to-postgres": {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "allow-api-gateway-to-postgres",
                "namespace": "caelum-data",
            },
            "spec": {
                "podSelector": {"matchLabels": {"app": "api-gateway"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "to": [{"podSelector": {"matchLabels": {"app": "postgres"}}}],
                        "ports": [{"protocol": "TCP", "port": 5432}],
                    }
                ],
            },
            "description": "api-gateway → postgres (port 5432)",
        },
        "api-gateway-to-rabbitmq": {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "allow-api-gateway-to-rabbitmq",
                "namespace": "caelum-data",
            },
            "spec": {
                "podSelector": {"matchLabels": {"app": "api-gateway"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "to": [{"podSelector": {"matchLabels": {"app": "rabbitmq"}}}],
                        "ports": [{"protocol": "TCP", "port": 5672}],
                    }
                ],
            },
            "description": "api-gateway → rabbitmq (port 5672)",
        },
        "monitoring-to-all-services": {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "allow-monitoring-scrape",
                "namespace": "caelum-monitoring",
            },
            "spec": {
                "podSelector": {"matchLabels": {"app": "prometheus"}},
                "policyTypes": ["Egress"],
                "egress": [
                    {
                        "to": [{"namespaceSelector": {"matchLabels": {"caelum.io/monitored": "true"}}}],
                        "ports": [
                            {"protocol": "TCP", "port": 9090},
                            {"protocol": "TCP", "port": 9121},
                        ],
                    }
                ],
            },
            "description": "monitoring → all services (ports 9090/9121)",
        },
    },
    "explicit_denials": {
        "block-internet-to-postgres": {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": "deny-internet-to-postgres",
                "namespace": "caelum-data",
            },
            "spec": {
                "podSelector": {"matchLabels": {"app": "postgres"}},
                "policyTypes": ["Ingress"],
                "ingress": [
                    {
                        "from": [
                            {"podSelector": {"matchLabels": {"app": "api-gateway"}}},
                            {"podSelector": {"matchLabels": {"app": "caelum-auditor"}}},
                        ],
                        "ports": [{"protocol": "TCP", "port": 5432}],
                    }
                ],
            },
            "description": "DENY direct internet → postgres (whitelist only api-gateway + auditor)",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# OPA GATEKEEPER POLICIES — 8 Constraints
# ─────────────────────────────────────────────────────────────────────────────

OPA_GATEKEEPER_POLICIES = {
    "constraint_templates": [
        {
            "name": "RequireResourceLimits",
            "description": "All containers must define CPU and memory limits",
            "rego": """
package caelum.k8s.requireresourcelimits
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not container.resources.limits.cpu
  msg := sprintf("Container '%v' must define resources.limits.cpu", [container.name])
}
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not container.resources.limits.memory
  msg := sprintf("Container '%v' must define resources.limits.memory", [container.name])
}
""",
            "enforcement": "deny",
            "applies_to": ["Pod"],
            "severity": "critical",
        },
        {
            "name": "RequireProbes",
            "description": "All containers must define liveness and readiness probes",
            "rego": """
package caelum.k8s.requireprobes
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not container.livenessProbe
  msg := sprintf("Container '%v' missing livenessProbe", [container.name])
}
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not container.readinessProbe
  msg := sprintf("Container '%v' missing readinessProbe", [container.name])
}
""",
            "enforcement": "deny",
            "applies_to": ["Pod"],
            "severity": "high",
        },
        {
            "name": "NoPrivilegedContainers",
            "description": "Containers must not run in privileged mode",
            "rego": """
package caelum.k8s.noprivilegedcontainers
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  container.securityContext.privileged == true
  msg := sprintf("Container '%v' must not run as privileged", [container.name])
}
violation[{"msg": msg}] {
  container := input.review.object.spec.initContainers[_]
  container.securityContext.privileged == true
  msg := sprintf("InitContainer '%v' must not run as privileged", [container.name])
}
""",
            "enforcement": "deny",
            "applies_to": ["Pod"],
            "severity": "critical",
        },
        {
            "name": "RequireNonRootUser",
            "description": "Pods must not run as root (UID 0)",
            "rego": """
package caelum.k8s.requirenonrootuser
violation[{"msg": msg}] {
  spec := input.review.object.spec
  spec.securityContext.runAsUser == 0
  msg := "Pod securityContext.runAsUser must not be 0 (root)"
}
violation[{"msg": msg}] {
  spec := input.review.object.spec
  not spec.securityContext.runAsNonRoot
  msg := "Pod securityContext.runAsNonRoot must be true"
}
""",
            "enforcement": "deny",
            "applies_to": ["Pod"],
            "severity": "critical",
        },
        {
            "name": "RequireReadOnlyRootFilesystem",
            "description": "Containers must use a read-only root filesystem",
            "rego": """
package caelum.k8s.requirereadonlyrootfs
violation[{"msg": msg}] {
  container := input.review.object.spec.containers[_]
  not container.securityContext.readOnlyRootFilesystem
  msg := sprintf("Container '%v' must set readOnlyRootFilesystem: true", [container.name])
}
""",
            "enforcement": "deny",
            "applies_to": ["Pod"],
            "severity": "high",
        },
        {
            "name": "RequireSeccompProfile",
            "description": "Pods must define a seccomp profile (RuntimeDefault or Localhost)",
            "rego": """
package caelum.k8s.requireseccompprofile
violation[{"msg": msg}] {
  spec := input.review.object.spec
  not spec.securityContext.seccompProfile
  msg := "Pod must define securityContext.seccompProfile"
}
violation[{"msg": msg}] {
  profile := input.review.object.spec.securityContext.seccompProfile.type
  not profile == "RuntimeDefault"
  not profile == "Localhost"
  msg := sprintf("seccompProfile.type '%v' not allowed — use RuntimeDefault or Localhost", [profile])
}
""",
            "enforcement": "deny",
            "applies_to": ["Pod"],
            "severity": "high",
        },
        {
            "name": "NoHostNetwork",
            "description": "Pods must not use host network, PID, or IPC namespaces",
            "rego": """
package caelum.k8s.nohostnetwork
violation[{"msg": msg}] {
  input.review.object.spec.hostNetwork == true
  msg := "Pod must not use hostNetwork: true"
}
violation[{"msg": msg}] {
  input.review.object.spec.hostPID == true
  msg := "Pod must not use hostPID: true"
}
violation[{"msg": msg}] {
  input.review.object.spec.hostIPC == true
  msg := "Pod must not use hostIPC: true"
}
""",
            "enforcement": "deny",
            "applies_to": ["Pod"],
            "severity": "critical",
        },
        {
            "name": "RequireLabels",
            "description": "All resources must have required CaelumSwarm labels",
            "rego": """
package caelum.k8s.requirelabels
required_labels := {"app", "version", "managed-by"}
violation[{"msg": msg}] {
  provided := {label | input.review.object.metadata.labels[label]}
  missing := required_labels - provided
  count(missing) > 0
  msg := sprintf("Missing required labels: %v", [missing])
}
""",
            "enforcement": "warn",
            "applies_to": ["Pod", "Deployment", "Service"],
            "severity": "medium",
        },
    ],
    "constraint_instances": [
        {
            "template": "RequireResourceLimits",
            "name": "caelum-require-resource-limits",
            "namespaces": ["caelum-engines", "caelum-dev", "caelum-data"],
        },
        {
            "template": "RequireProbes",
            "name": "caelum-require-probes",
            "namespaces": ["caelum-engines", "caelum-dev"],
        },
        {
            "template": "NoPrivilegedContainers",
            "name": "caelum-no-privileged",
            "namespaces": ["*"],
        },
        {
            "template": "RequireNonRootUser",
            "name": "caelum-require-nonroot",
            "namespaces": ["*"],
        },
        {
            "template": "RequireReadOnlyRootFilesystem",
            "name": "caelum-readonly-rootfs",
            "namespaces": ["caelum-engines", "caelum-dev"],
        },
        {
            "template": "RequireSeccompProfile",
            "name": "caelum-seccomp-required",
            "namespaces": ["*"],
        },
        {
            "template": "NoHostNetwork",
            "name": "caelum-no-host-network",
            "namespaces": ["*"],
        },
        {
            "template": "RequireLabels",
            "name": "caelum-require-labels",
            "namespaces": ["caelum-engines", "caelum-dev", "caelum-data"],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# FALCO RULES — 6 Runtime Detection Rules
# ─────────────────────────────────────────────────────────────────────────────

FALCO_RULES = [
    {
        "id": "FALCO-001",
        "name": "Terminal shell in container",
        "description": "Detect interactive shell spawned inside a container at runtime",
        "condition": (
            "spawned_process and container and shell_procs and proc.tty != 0 "
            "and container.image.repository != 'caelum-debug'"
        ),
        "output": (
            "Interactive shell in container "
            "(user=%user.name container=%container.name image=%container.image.repository "
            "shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)"
        ),
        "priority": "WARNING",
        "tags": ["container", "shell", "mitre_execution"],
        "remediation": [
            "Terminate the container immediately if shell is unexpected",
            "Audit the container image for embedded shells",
            "Review user access — only ops team may exec into pods",
            "Use 'kubectl exec' audit logging via CloudTrail",
        ],
    },
    {
        "id": "FALCO-002",
        "name": "Sensitive file access",
        "description": "Detect reads of sensitive files (credentials, PKI, shadow)",
        "condition": (
            "open_read and fd.name in (sensitive_files) and not proc.name in (trusted_readers) "
            "and not container.image.repository startswith 'caelum-vault'"
        ),
        "output": (
            "Sensitive file read "
            "(user=%user.name file=%fd.name container=%container.name "
            "image=%container.image.repository proc=%proc.name)"
        ),
        "priority": "ERROR",
        "tags": ["filesystem", "secrets", "mitre_credential_access"],
        "sensitive_files": [
            "/etc/shadow", "/etc/passwd", "/root/.ssh/id_rsa",
            "/var/run/secrets/kubernetes.io/serviceaccount/token",
            "/proc/*/environ",
        ],
        "remediation": [
            "Isolate the container and capture forensic evidence",
            "Rotate all secrets referenced in the sensitive file",
            "Check for lateral movement in adjacent namespaces",
            "File a CSDDD security incident report within 24h",
        ],
    },
    {
        "id": "FALCO-003",
        "name": "Outbound connection to C2",
        "description": "Detect unexpected outbound connections to known C2 IP ranges or unusual ports",
        "condition": (
            "outbound and container and not fd.sip in (approved_egress_ips) "
            "and not fd.sport in (8080, 6379, 5432, 5672, 9090, 9121, 443, 53) "
            "and fd.typechar = '4'"
        ),
        "output": (
            "Suspicious outbound connection "
            "(user=%user.name container=%container.name dst_ip=%fd.sip "
            "dst_port=%fd.sport image=%container.image.repository)"
        ),
        "priority": "CRITICAL",
        "tags": ["network", "c2", "mitre_command_and_control"],
        "remediation": [
            "Immediately apply network policy to block the connection",
            "Kill and quarantine the container",
            "Analyse process tree for indicators of compromise",
            "Block destination IP at WAF and cloud security group level",
            "Escalate to CSIRT within 1 hour",
        ],
    },
    {
        "id": "FALCO-004",
        "name": "Privilege escalation attempt",
        "description": "Detect setuid/setgid execution or sudo invocation inside containers",
        "condition": (
            "(evt.type = execve or evt.type = execveat) and container "
            "and (proc.name in (setuid_binaries) or evt.arg.flags contains S_ISUID "
            "or proc.name = 'sudo' or proc.name = 'su')"
        ),
        "output": (
            "Privilege escalation attempt "
            "(user=%user.name container=%container.name proc=%proc.name "
            "cmdline=%proc.cmdline image=%container.image.repository)"
        ),
        "priority": "CRITICAL",
        "tags": ["process", "privilege_escalation", "mitre_privilege_escalation"],
        "remediation": [
            "Stop the container — privilege escalation violates Restricted PSS",
            "Verify the image was not tampered with (check digest)",
            "Audit RBAC — which user triggered this workload?",
            "Review OPA policies for allowPrivilegeEscalation: false enforcement",
        ],
    },
    {
        "id": "FALCO-005",
        "name": "Cryptocurrency mining detected",
        "description": "Detect crypto mining processes by known binary names and network patterns",
        "condition": (
            "spawned_process and container and "
            "(proc.name in (crypto_miners) or "
            "(outbound and fd.sport in (3333, 4444, 8333, 9999, 14444, 45560)))"
        ),
        "output": (
            "Cryptocurrency mining detected "
            "(user=%user.name container=%container.name proc=%proc.name "
            "cmdline=%proc.cmdline image=%container.image.repository)"
        ),
        "priority": "CRITICAL",
        "crypto_miners": ["xmrig", "minerd", "cpuminer", "ethminer", "cgminer", "bfgminer"],
        "tags": ["cryptomining", "impact", "mitre_resource_hijacking"],
        "remediation": [
            "Terminate container immediately — zero tolerance for crypto mining",
            "Remove image from registry, trigger full re-scan",
            "Check all replicas of the same deployment",
            "Audit image supply chain — likely compromised base image",
            "File security incident, review cost anomalies in AWS billing",
        ],
    },
    {
        "id": "FALCO-006",
        "name": "k8s secret read by non-allowed process",
        "description": "Detect access to Kubernetes service account token or mounted secrets by unexpected processes",
        "condition": (
            "open_read and container "
            "and fd.name startswith '/var/run/secrets/kubernetes.io/serviceaccount' "
            "and not proc.name in (allowed_secret_readers) "
            "and not proc.name in (java, python3, node, go)"
        ),
        "output": (
            "k8s secret read by unexpected process "
            "(user=%user.name proc=%proc.name container=%container.name "
            "file=%fd.name image=%container.image.repository)"
        ),
        "priority": "ERROR",
        "allowed_secret_readers": ["python3", "node", "java", "go", "caelum-engine"],
        "tags": ["secrets", "kubernetes", "mitre_credential_access"],
        "remediation": [
            "Set automountServiceAccountToken: false on pods that don't need it",
            "Rotate the compromised service account token immediately",
            "Audit what the token was used for via Kubernetes audit logs",
            "Consider using Workload Identity instead of mounted tokens",
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# CIS BENCHMARK — CIS Kubernetes Benchmark v1.8
# ─────────────────────────────────────────────────────────────────────────────

CIS_BENCHMARK = {
    "version": "CIS Kubernetes Benchmark v1.8",
    "kubernetes_version": KUBERNETES_VERSION,
    "sections": {
        "master_node": {
            "title": "Control Plane Components",
            "checks": [
                {"id": "1.1.1", "description": "Ensure API server pod spec file permissions are 600", "level": "L1"},
                {"id": "1.1.2", "description": "Ensure API server pod spec file ownership is root:root", "level": "L1"},
                {"id": "1.1.11", "description": "Ensure etcd data directory permissions are 700", "level": "L1"},
                {"id": "1.2.1", "description": "Ensure anonymous-auth is not enabled on API server", "level": "L1"},
                {"id": "1.2.2", "description": "Ensure --token-auth-file is not set", "level": "L1"},
                {"id": "1.2.6", "description": "Ensure NodeRestriction admission controller is enabled", "level": "L1"},
                {"id": "1.2.9", "description": "Ensure EventRateLimit admission controller is set", "level": "L2"},
                {"id": "1.2.10", "description": "Ensure AlwaysAdmit admission plugin is not set", "level": "L1"},
                {"id": "1.2.16", "description": "Ensure audit-log-path is set", "level": "L1"},
                {"id": "1.2.19", "description": "Ensure audit-log-maxage is set to 30 or appropriate", "level": "L1"},
                {"id": "1.2.22", "description": "Ensure request-timeout is set appropriately", "level": "L1"},
                {"id": "1.2.24", "description": "Ensure service-account-lookup is true", "level": "L1"},
                {"id": "1.2.33", "description": "Ensure encryption-provider-config is set", "level": "L1"},
                {"id": "1.3.1", "description": "Ensure terminated-pod-gc-threshold is set appropriately", "level": "L1"},
                {"id": "1.3.6", "description": "Ensure RotateKubeletServerCertificate is true", "level": "L2"},
            ],
        },
        "etcd": {
            "title": "etcd",
            "checks": [
                {"id": "2.1", "description": "Ensure etcd is configured with TLS encryption", "level": "L1"},
                {"id": "2.2", "description": "Ensure etcd peer communication is TLS encrypted", "level": "L1"},
                {"id": "2.4", "description": "Ensure etcd is not using self-signed certificates in prod", "level": "L2"},
                {"id": "2.6", "description": "Ensure etcd peer-cert-file and peer-key-file are configured", "level": "L1"},
                {"id": "2.7", "description": "Ensure unique certificate authority is used for etcd", "level": "L2"},
            ],
        },
        "worker_node": {
            "title": "Worker Node Security Configuration",
            "checks": [
                {"id": "4.1.1", "description": "Ensure kubelet service file permissions are 600", "level": "L1"},
                {"id": "4.1.5", "description": "Ensure kubelet.conf file permissions are 600", "level": "L1"},
                {"id": "4.2.1", "description": "Ensure anonymous-auth is false on kubelet", "level": "L1"},
                {"id": "4.2.2", "description": "Ensure authorization-mode is not AlwaysAllow on kubelet", "level": "L1"},
                {"id": "4.2.6", "description": "Ensure streaming-connection-idle-timeout is not 0", "level": "L1"},
                {"id": "4.2.7", "description": "Ensure protect-kernel-defaults is true", "level": "L1"},
                {"id": "4.2.10", "description": "Ensure rotate-certificates is true", "level": "L1"},
                {"id": "4.2.12", "description": "Ensure TLSCipherSuites is configured with approved ciphers", "level": "L1"},
            ],
        },
        "policies": {
            "title": "Kubernetes Policies",
            "checks": [
                {"id": "5.1.1", "description": "Ensure cluster-admin role is used only where required", "level": "L1"},
                {"id": "5.1.3", "description": "Minimize wildcard use in Roles and ClusterRoles", "level": "L1"},
                {"id": "5.1.5", "description": "Ensure default service accounts are not bound to active roles", "level": "L1"},
                {"id": "5.1.6", "description": "Ensure service account tokens are not mounted automatically", "level": "L1"},
                {"id": "5.2.1", "description": "Ensure PodSecurity admission controller is in place", "level": "L1"},
                {"id": "5.2.2", "description": "Minimize the admission of privileged containers", "level": "L1"},
                {"id": "5.2.5", "description": "Minimize the admission of containers with allowPrivilegeEscalation", "level": "L1"},
                {"id": "5.2.6", "description": "Minimize root container admission", "level": "L2"},
                {"id": "5.2.8", "description": "Minimize the admission of containers with NET_RAW capability", "level": "L1"},
                {"id": "5.2.9", "description": "Minimize the admission of containers with added capabilities", "level": "L1"},
                {"id": "5.3.1", "description": "Ensure CNI in use supports Network Policies", "level": "L1"},
                {"id": "5.3.2", "description": "Ensure default deny NetworkPolicy in every namespace", "level": "L2"},
                {"id": "5.4.1", "description": "Prefer secrets as files over secrets as env variables", "level": "L2"},
                {"id": "5.4.2", "description": "Consider external secret management", "level": "L2"},
                {"id": "5.5.1", "description": "Configure Image Provenance using ImagePolicyWebhook", "level": "L2"},
                {"id": "5.7.1", "description": "Create administrative boundaries between resources using namespaces", "level": "L1"},
                {"id": "5.7.3", "description": "Apply SecurityContext to pods and containers", "level": "L2"},
                {"id": "5.7.4", "description": "Ensure default namespace is not used", "level": "L2"},
            ],
        },
    },
    "target_score": 87.0,
}

# ─────────────────────────────────────────────────────────────────────────────
# ADMISSION CONTROLLERS
# ─────────────────────────────────────────────────────────────────────────────

ADMISSION_CONTROLLERS = {
    "enabled": [
        {
            "name": "NodeRestriction",
            "type": "built-in",
            "description": "Limits the Node and Pod objects a kubelet can modify",
            "critical": True,
        },
        {
            "name": "PodSecurity",
            "type": "built-in",
            "description": "Enforces Pod Security Standards (replaces PSP)",
            "profile": "restricted",
            "critical": True,
        },
        {
            "name": "ResourceQuota",
            "type": "built-in",
            "description": "Enforces resource quotas per namespace",
            "critical": True,
        },
        {
            "name": "LimitRanger",
            "type": "built-in",
            "description": "Enforces default resource limits per namespace",
            "critical": False,
        },
        {
            "name": "MutatingWebhook",
            "type": "webhook",
            "description": "OPA Gatekeeper + Istio injection",
            "webhooks": ["gatekeeper-mutating-webhook", "istio-sidecar-injector"],
            "critical": True,
        },
        {
            "name": "ValidatingWebhook",
            "type": "webhook",
            "description": "OPA Gatekeeper constraint enforcement",
            "webhooks": ["gatekeeper-validating-webhook-configuration"],
            "critical": True,
        },
    ],
    "disabled": [
        "AlwaysAdmit",
        "AlwaysPullImages",  # handled by OPA policy instead
        "DenyServiceExternalIPs",
        "SecurityContextDeny",  # replaced by PodSecurity
    ],
    "api_server_flags": [
        "--enable-admission-plugins=NodeRestriction,PodSecurity,ResourceQuota,"
        "LimitRanger,MutatingAdmissionWebhook,ValidatingAdmissionWebhook",
        "--disable-admission-plugins=AlwaysAdmit,SecurityContextDeny",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# SECRET MANAGEMENT — External Secrets Operator → HashiCorp Vault
# ─────────────────────────────────────────────────────────────────────────────

SECRET_MANAGEMENT = {
    "strategy": "External Secrets Operator (ESO) → HashiCorp Vault",
    "native_k8s_secrets": "DISABLED — no plaintext secrets in etcd",
    "components": {
        "external_secrets_operator": {
            "version": "0.9.x",
            "helm_chart": "external-secrets/external-secrets",
            "namespace": "external-secrets",
            "config": {
                "replicaCount": 2,
                "serviceMonitor": {"enabled": True},
                "webhook": {"enabled": True},
            },
        },
        "hashicorp_vault": {
            "version": "1.15.x",
            "deployment": "AWS EKS with IRSA auth method",
            "auth_method": "kubernetes",
            "secret_engines": [
                {"path": "caelum/engines", "type": "kv-v2", "description": "Wave engine secrets"},
                {"path": "caelum/data", "type": "database", "description": "PostgreSQL dynamic creds"},
                {"path": "caelum/pki", "type": "pki", "description": "Internal TLS certificates"},
            ],
            "policies": {
                "caelum-engine-policy": {
                    "path": "caelum/engines/*",
                    "capabilities": ["read", "list"],
                },
                "caelum-admin-policy": {
                    "path": "caelum/*",
                    "capabilities": ["create", "read", "update", "delete", "list"],
                },
            },
        },
    },
    "example_external_secret": {
        "apiVersion": "external-secrets.io/v1beta1",
        "kind": "ExternalSecret",
        "metadata": {
            "name": "caelum-engine-secrets",
            "namespace": "caelum-engines",
        },
        "spec": {
            "refreshInterval": "1h",
            "secretStoreRef": {"name": "vault-backend", "kind": "ClusterSecretStore"},
            "target": {
                "name": "caelum-engine-secrets",
                "creationPolicy": "Owner",
                "template": {
                    "engineVersion": "v2",
                    "type": "Opaque",
                },
            },
            "data": [
                {
                    "secretKey": "SWARM_API_KEY",
                    "remoteRef": {
                        "key": "caelum/engines/swarm",
                        "property": "api_key",
                    },
                },
                {
                    "secretKey": "POSTGRES_PASSWORD",
                    "remoteRef": {
                        "key": "caelum/engines/database",
                        "property": "postgres_password",
                    },
                },
            ],
        },
    },
    "cluster_secret_store": {
        "apiVersion": "external-secrets.io/v1beta1",
        "kind": "ClusterSecretStore",
        "metadata": {"name": "vault-backend"},
        "spec": {
            "provider": {
                "vault": {
                    "server": "https://vault.caelum-internal.svc.cluster.local:8200",
                    "path": "caelum",
                    "version": "v2",
                    "auth": {
                        "kubernetes": {
                            "mountPath": "kubernetes",
                            "role": "caelum-external-secrets",
                        }
                    },
                }
            }
        },
    },
    "encryption_at_rest": {
        "etcd": "AES-256-CBC via EncryptionConfiguration",
        "vault": "AES-256-GCM with AWS KMS auto-unseal",
        "transit_key": "caelum-transit-key",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def generate_rbac_manifest(role_name: str, permissions: dict) -> str:
    """
    Generate a valid Kubernetes YAML manifest for a ClusterRole + ServiceAccount + ClusterRoleBinding.

    Args:
        role_name:   Name of the RBAC role (must exist in RBAC_CONFIG['cluster_roles'])
        permissions: Dict with keys 'apiGroups', 'resources', 'verbs' (overrides config if provided)

    Returns:
        Multi-document YAML string (ServiceAccount --- ClusterRole --- ClusterRoleBinding)
    """
    if role_name not in RBAC_CONFIG["cluster_roles"]:
        available = list(RBAC_CONFIG["cluster_roles"].keys())
        raise ValueError(
            f"Role '{role_name}' not found. Available: {available}"
        )

    role_config = RBAC_CONFIG["cluster_roles"][role_name]
    sa = role_config["service_account"]

    # Merge permissions: caller overrides config default
    rules = permissions if permissions else role_config["rules"]

    def _indent(text: str, spaces: int) -> str:
        pad = " " * spaces
        return "\n".join(pad + line if line.strip() else line for line in text.splitlines())

    def _list_to_yaml(items: list, indent: int = 0) -> str:
        pad = " " * indent
        return "\n".join(f"{pad}- {item}" for item in items)

    def _render_rules(rule_list: list) -> str:
        lines = []
        for rule in rule_list:
            api_groups = rule.get("apiGroups", [""])
            resources = rule.get("resources", [])
            verbs = rule.get("verbs", [])
            lines.append("  - apiGroups:")
            for ag in api_groups:
                q = f'"{ag}"' if ag != "*" else '"*"'
                lines.append(f"      - {q}")
            lines.append("    resources:")
            for r in resources:
                lines.append(f'      - "{r}"')
            lines.append("    verbs:")
            if verbs:
                for v in verbs:
                    lines.append(f'      - "{v}"')
            else:
                lines.append("      []  # No verbs — effectively deny")
        return "\n".join(lines)

    irsa_arn = sa.get("irsa_role_arn", "")

    yaml_output = f"""---
# ServiceAccount — {role_name}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {sa['name']}
  namespace: {sa['namespace']}
  annotations:
    eks.amazonaws.com/role-arn: "{irsa_arn}"
    caelum.io/managed-by: "caelum-security-agent"
    caelum.io/csddd-compliant: "true"
  labels:
    app: caelum-rbac
    role: {role_name}
    managed-by: caelum-security-agent
automountServiceAccountToken: false
---
# ClusterRole — {role_name}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: {role_name}
  labels:
    app: caelum-rbac
    role: {role_name}
    managed-by: caelum-security-agent
  annotations:
    caelum.io/description: "{role_config.get('description', '')}"
    caelum.io/least-privilege: "true"
rules:
{_render_rules(rules)}
---
# ClusterRoleBinding — {role_name}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: {role_name}-binding
  labels:
    app: caelum-rbac
    role: {role_name}
    managed-by: caelum-security-agent
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: {role_name}
subjects:
  - kind: ServiceAccount
    name: {sa['name']}
    namespace: {sa['namespace']}
"""
    return yaml_output


def validate_pod_security(pod_spec: dict) -> dict:
    """
    Validate a pod spec against the Kubernetes Pod Security Standards — Restricted profile.

    Args:
        pod_spec: dict representing the pod spec (metadata + spec)

    Returns:
        dict with keys:
            - compliant (bool)
            - violations (list of str)
            - warnings (list of str)
            - score (int 0-100)
            - profile_checked (str)
    """
    violations = []
    warnings = []

    spec = pod_spec.get("spec", {})
    metadata = pod_spec.get("metadata", {})
    security_ctx = spec.get("securityContext", {})
    containers = spec.get("containers", [])
    init_containers = spec.get("initContainers", [])
    all_containers = containers + init_containers

    # ── Pod-level checks ──────────────────────────────────────────────────────

    if not security_ctx.get("runAsNonRoot", False):
        violations.append("[CRITICAL] spec.securityContext.runAsNonRoot must be true")

    run_as_user = security_ctx.get("runAsUser")
    if run_as_user is not None and run_as_user == 0:
        violations.append("[CRITICAL] spec.securityContext.runAsUser must not be 0 (root)")
    elif run_as_user is not None and run_as_user < 1000:
        warnings.append(f"[WARN] spec.securityContext.runAsUser={run_as_user} — recommend >= 1000")

    seccomp = security_ctx.get("seccompProfile", {})
    seccomp_type = seccomp.get("type", "")
    if not seccomp_type:
        violations.append("[CRITICAL] spec.securityContext.seccompProfile must be set (RuntimeDefault or Localhost)")
    elif seccomp_type not in ("RuntimeDefault", "Localhost"):
        violations.append(f"[HIGH] seccompProfile.type '{seccomp_type}' not allowed — use RuntimeDefault or Localhost")

    if spec.get("hostNetwork", False):
        violations.append("[CRITICAL] spec.hostNetwork must not be true")

    if spec.get("hostPID", False):
        violations.append("[CRITICAL] spec.hostPID must not be true")

    if spec.get("hostIPC", False):
        violations.append("[CRITICAL] spec.hostIPC must not be true")

    if spec.get("automountServiceAccountToken", True):
        warnings.append("[WARN] spec.automountServiceAccountToken should be false")

    # ── Volume checks ─────────────────────────────────────────────────────────
    forbidden_vol_types = POD_SECURITY_STANDARDS["required_fields"]["volumes"]["forbidden_types"]
    for vol in spec.get("volumes", []):
        for ftype in forbidden_vol_types:
            if ftype in vol:
                violations.append(f"[CRITICAL] Volume '{vol.get('name')}' uses forbidden type '{ftype}'")

    # ── Container-level checks ────────────────────────────────────────────────
    for ctr in all_containers:
        name = ctr.get("name", "<unnamed>")
        csc = ctr.get("securityContext", {})

        if csc.get("privileged", False):
            violations.append(f"[CRITICAL] containers[{name}].securityContext.privileged must be false")

        if csc.get("allowPrivilegeEscalation", True):
            violations.append(f"[HIGH] containers[{name}].securityContext.allowPrivilegeEscalation must be false")

        if not csc.get("readOnlyRootFilesystem", False):
            violations.append(f"[HIGH] containers[{name}].securityContext.readOnlyRootFilesystem must be true")

        caps = csc.get("capabilities", {})
        drop = caps.get("drop", [])
        if "ALL" not in drop and "all" not in drop:
            violations.append(f"[HIGH] containers[{name}].securityContext.capabilities.drop must include 'ALL'")
        add = caps.get("add", [])
        forbidden_caps = [c for c in add if c not in ("NET_BIND_SERVICE",)]
        if forbidden_caps:
            violations.append(
                f"[CRITICAL] containers[{name}] adds forbidden capabilities: {forbidden_caps}"
            )

        # Resource limits
        resources = ctr.get("resources", {})
        limits = resources.get("limits", {})
        if not limits.get("cpu"):
            violations.append(f"[MEDIUM] containers[{name}] missing resources.limits.cpu")
        if not limits.get("memory"):
            violations.append(f"[MEDIUM] containers[{name}] missing resources.limits.memory")

        # Probes
        if not ctr.get("livenessProbe"):
            warnings.append(f"[WARN] containers[{name}] missing livenessProbe")
        if not ctr.get("readinessProbe"):
            warnings.append(f"[WARN] containers[{name}] missing readinessProbe")

    # ── Label checks ──────────────────────────────────────────────────────────
    labels = metadata.get("labels", {})
    for required_label in ("app", "version", "managed-by"):
        if required_label not in labels:
            warnings.append(f"[WARN] metadata.labels missing required label '{required_label}'")

    # ── Score ─────────────────────────────────────────────────────────────────
    total_checks = 20
    critical_weight = 5
    high_weight = 3
    medium_weight = 1

    penalty = 0
    for v in violations:
        if "[CRITICAL]" in v:
            penalty += critical_weight
        elif "[HIGH]" in v:
            penalty += high_weight
        elif "[MEDIUM]" in v:
            penalty += medium_weight

    raw_score = max(0, 100 - (penalty / (total_checks * critical_weight)) * 100)
    score = round(min(100, raw_score))

    compliant = len(violations) == 0

    return {
        "compliant": compliant,
        "profile_checked": "Restricted (PSS v1.29)",
        "score": score,
        "violations": violations,
        "warnings": warnings,
        "summary": (
            f"{'PASS' if compliant else 'FAIL'} — "
            f"{len(violations)} violation(s), {len(warnings)} warning(s), score: {score}/100"
        ),
    }


def simulate_falco_alert(event_type: str, container: str, user: str) -> dict:
    """
    Simulate a Falco runtime security alert.

    Args:
        event_type: One of the FALCO_RULES names or IDs
        container:  Container name where the event occurred
        user:       Username (or UID) that triggered the event

    Returns:
        dict with alert details including timestamp, severity, rule matched, and remediation steps
    """
    # Lookup the matching rule
    matched_rule = None
    for rule in FALCO_RULES:
        if (
            event_type.lower() in rule["name"].lower()
            or event_type.upper() == rule["id"]
            or event_type.lower().replace(" ", "_") in rule["name"].lower().replace(" ", "_")
        ):
            matched_rule = rule
            break

    if matched_rule is None:
        # Default to a generic alert
        matched_rule = {
            "id": "FALCO-UNKNOWN",
            "name": event_type,
            "priority": "WARNING",
            "tags": ["unknown"],
            "description": f"Unknown event type: {event_type}",
            "output": f"Unmatched event (container=%container.name user=%user.name)",
            "remediation": ["Investigate the event manually", "Check Falco rule definitions"],
        }

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # Generate deterministic alert ID from inputs
    alert_hash = hashlib.sha256(
        f"{timestamp}{event_type}{container}{user}".encode()
    ).hexdigest()[:12]

    priority_map = {
        "CRITICAL": {"level": 1, "color": "RED", "escalation": "Immediate — page CSIRT"},
        "ERROR": {"level": 2, "color": "ORANGE", "escalation": "Within 1 hour — notify security team"},
        "WARNING": {"level": 3, "color": "YELLOW", "escalation": "Within 4 hours — review and assess"},
        "NOTICE": {"level": 4, "color": "BLUE", "escalation": "Next business day — log and monitor"},
        "INFO": {"level": 5, "color": "WHITE", "escalation": "None — informational only"},
    }

    priority = matched_rule.get("priority", "WARNING")
    priority_info = priority_map.get(priority, priority_map["WARNING"])

    # Format output message
    output_msg = (
        matched_rule.get("output", "Event detected")
        .replace("%user.name", user)
        .replace("%container.name", container)
        .replace("%container.image.repository", f"caelum-registry.io/{container}")
        .replace("%proc.name", event_type.split()[0] if event_type else "unknown")
        .replace("%proc.cmdline", f"{event_type} --verbose")
        .replace("%fd.name", "/var/run/secrets/kubernetes.io/serviceaccount/token")
        .replace("%fd.sip", "198.51.100.42")
        .replace("%fd.sport", "4444")
        .replace("%proc.pname", "containerd-shim")
    )

    alert = {
        "alert_id": f"FALCO-ALERT-{alert_hash.upper()}",
        "rule_id": matched_rule["id"],
        "rule_name": matched_rule["name"],
        "timestamp": timestamp,
        "priority": priority,
        "severity_level": priority_info["level"],
        "color": priority_info["color"],
        "escalation_policy": priority_info["escalation"],
        "container": container,
        "user": user,
        "namespace": "caelum-engines",
        "node": "ip-10-0-1-42.eu-west-1.compute.internal",
        "output": output_msg,
        "description": matched_rule.get("description", ""),
        "tags": matched_rule.get("tags", []),
        "csddd_relevant": any(t in matched_rule.get("tags", []) for t in [
            "mitre_credential_access", "mitre_privilege_escalation",
            "c2", "cryptomining", "secrets",
        ]),
        "remediation_steps": matched_rule.get("remediation", []),
        "falco_version": "0.37.0",
        "kubernetes_cluster": "caelum-prod-eks-eu-west-1",
    }

    return alert


def run_cis_benchmark() -> dict:
    """
    Simulate a CIS Kubernetes Benchmark v1.8 scan against a CaelumSwarm cluster.

    Returns:
        dict with:
            - score_percent (float ~87%)
            - passed_checks (int)
            - failed_checks (list of dicts)
            - warnings (list of dicts)
            - remediation_steps (list of str)
            - section_scores (dict)
    """
    # Simulate deterministic results for a well-configured cluster
    # Total checks across all sections
    all_checks = []
    for section_key, section in CIS_BENCHMARK["sections"].items():
        for check in section["checks"]:
            all_checks.append({
                "section": section_key,
                "section_title": section["title"],
                **check,
            })

    total = len(all_checks)

    # Simulate failures for realistic ~87% score
    # Known common gaps in managed EKS clusters
    forced_failures = {
        "1.2.9",   # EventRateLimit — complex to configure on managed EKS
        "1.3.6",   # RotateKubeletServerCertificate — managed by EKS, limited control
        "2.4",     # etcd self-signed certs — managed service limitation
        "2.7",     # Unique CA for etcd — managed service limitation
        "5.5.1",   # ImagePolicyWebhook — not yet deployed
    }

    passed = []
    failed = []
    warnings_list = []

    for check in all_checks:
        check_id = check["id"]
        level = check.get("level", "L1")

        if check_id in forced_failures:
            failed.append({
                "id": check_id,
                "level": level,
                "section": check["section_title"],
                "description": check["description"],
                "reason": _get_failure_reason(check_id),
            })
        elif level == "L2" and check_id not in forced_failures:
            # L2 checks — 85% pass rate
            # Use deterministic hash to decide
            h = int(hashlib.md5(check_id.encode()).hexdigest(), 16) % 100
            if h > 85:
                warnings_list.append({
                    "id": check_id,
                    "level": level,
                    "section": check["section_title"],
                    "description": check["description"],
                    "status": "NEEDS_REVIEW",
                })
            else:
                passed.append(check)
        else:
            passed.append(check)

    # Calculate score
    pass_count = len(passed)
    fail_count = len(failed)
    warn_count = len(warnings_list)
    score = round((pass_count / total) * 100, 1)

    # Section scores
    section_scores = {}
    for section_key, section in CIS_BENCHMARK["sections"].items():
        sec_checks = [c for c in section["checks"]]
        sec_ids = {c["id"] for c in sec_checks}
        sec_passed = sum(1 for c in passed if c["id"] in sec_ids)
        sec_total = len(sec_checks)
        section_scores[section["title"]] = {
            "passed": sec_passed,
            "total": sec_total,
            "score_percent": round((sec_passed / sec_total) * 100, 1) if sec_total else 0,
        }

    # Remediation steps for failed checks
    remediation_steps = []
    for f in failed:
        step = _get_remediation_step(f["id"], f["description"])
        remediation_steps.append(f"[{f['id']}] {step}")

    return {
        "benchmark": CIS_BENCHMARK["version"],
        "kubernetes_version": KUBERNETES_VERSION,
        "cluster": "caelum-prod-eks-eu-west-1",
        "scan_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "score_percent": score,
        "target_score_percent": CIS_BENCHMARK["target_score"],
        "passed_checks": pass_count,
        "failed_checks": failed,
        "failed_count": fail_count,
        "warnings": warnings_list,
        "warnings_count": warn_count,
        "total_checks": total,
        "section_scores": section_scores,
        "remediation_steps": remediation_steps,
        "overall_status": "PASS" if score >= CIS_BENCHMARK["target_score"] else "NEEDS_IMPROVEMENT",
        "next_audit_date": (
            datetime.datetime.utcnow() + datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d"),
    }


def _get_failure_reason(check_id: str) -> str:
    """Return a reason string for a known CIS benchmark failure."""
    reasons = {
        "1.2.9": "EventRateLimit admission controller requires manual configuration on managed EKS — deferred to next sprint",
        "1.3.6": "RotateKubeletServerCertificate is managed by EKS control plane — limited operator control",
        "2.4": "etcd managed by AWS EKS — certificate authority is AWS-controlled",
        "2.7": "Unique CA for etcd not configurable on EKS managed control plane",
        "5.5.1": "ImagePolicyWebhook not yet deployed — planned for Wave 60 security hardening",
    }
    return reasons.get(check_id, "Check did not pass automated verification")


def _get_remediation_step(check_id: str, description: str) -> str:
    """Return a remediation step for a failed CIS check."""
    steps = {
        "1.2.9": (
            "Submit AWS support ticket to enable EventRateLimit. "
            "Alternatively, use OPA Gatekeeper RateLimitPolicy as compensating control."
        ),
        "1.3.6": (
            "Document EKS managed rotation as compensating control. "
            "Verify via: aws eks describe-cluster --name caelum-prod --query 'cluster.certificateAuthority'"
        ),
        "2.4": (
            "Accept AWS-managed etcd CA as compliant for managed EKS. "
            "Document exception in CSDDD audit register with AWS shared responsibility model reference."
        ),
        "2.7": (
            "Not applicable for EKS managed control plane. "
            "Document in security exception register — AWS manages etcd CA isolation."
        ),
        "5.5.1": (
            "Deploy Kyverno ImagePolicyWebhook or OPA constraint 'RequireImageDigest'. "
            "Target: Wave 60 — ETA 2026-07-01. Assign to: security-engineering team."
        ),
    }
    return steps.get(check_id, f"Review and remediate: {description}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN — 8 sections
# ─────────────────────────────────────────────────────────────────────────────

def _separator(title: str = "", char: str = "═", width: int = 72) -> str:
    if not title:
        return char * width
    side = (width - len(title) - 2) // 2
    return f"{char * side} {title} {char * (width - side - len(title) - 2)}"


def _print_section(n: int, title: str) -> None:
    print()
    print(_separator(f"SECTION {n}: {title}"))


def main() -> None:
    print()
    print(_separator("", "━"))
    print("   KUBERNETES SECURITY REPORT — CaelumSwarm™")
    print(f"   CSDDD 2024 Compliance  |  K8s {KUBERNETES_VERSION}  |  {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(_separator("", "━"))

    # ── SECTION 1: Kubernetes Security Report ─────────────────────────────────
    _print_section(1, "Kubernetes Security Report — CaelumSwarm™")
    print(f"  Cluster          : caelum-prod-eks-eu-west-1")
    print(f"  Kubernetes       : {KUBERNETES_VERSION}")
    print(f"  Compliance       : CSDDD 2024 / CIS K8s Benchmark v1.8")
    print(f"  Security Stack   : RBAC | OPA Gatekeeper | Falco | ESO → Vault")
    print(f"  Pod Security     : Restricted (namespace-enforced)")
    print(f"  Network Policy   : Default Deny All + Explicit Whitelist")
    print(f"  Secret Mgmt      : External Secrets Operator → HashiCorp Vault")

    # ── SECTION 2: RBAC Configuration ────────────────────────────────────────
    _print_section(2, "RBAC Configuration (5 rôles — Least Privilege)")
    for role_name, role_cfg in RBAC_CONFIG["cluster_roles"].items():
        sa = role_cfg["service_account"]
        print(f"\n  [{role_name}]")
        print(f"    Description    : {role_cfg['description']}")
        print(f"    ServiceAccount : {sa['name']} @ {sa['namespace']}")
        print(f"    IRSA ARN       : {sa['irsa_role_arn']}")
        rule_count = len(role_cfg["rules"])
        print(f"    Rules          : {rule_count} rule group(s)")
        verb_set = set()
        for rule in role_cfg["rules"]:
            verb_set.update(rule.get("verbs", []))
        verbs_display = ", ".join(sorted(verb_set)) if verb_set else "(none — effectively deny)"
        print(f"    Verbs allowed  : {verbs_display}")

    print(f"\n  RoleBindings: {len(RBAC_CONFIG['role_bindings'])} configured")
    for binding_name, binding in RBAC_CONFIG["role_bindings"].items():
        kind = binding["kind"]
        role = binding["role"]
        subjects = ", ".join(binding["subjects"])
        print(f"    {kind:<25} {role:<30} → {subjects}")

    # Generate and display one RBAC manifest sample
    print(f"\n  Sample manifest — caelum-engine-runner:")
    print("  " + "─" * 60)
    sample_yaml = generate_rbac_manifest(
        "caelum-engine-runner",
        RBAC_CONFIG["cluster_roles"]["caelum-engine-runner"]["rules"],
    )
    for line in sample_yaml.strip().splitlines():
        print(f"  {line}")

    # ── SECTION 3: Pod Security Standards ────────────────────────────────────
    _print_section(3, "Pod Security Standards (Restricted)")
    pss = POD_SECURITY_STANDARDS
    print(f"  Profile          : {pss['profile'].upper()}")
    print(f"  K8s version      : {pss['kubernetes_version']}")
    print(f"\n  Namespace labels (enforce/audit/warn: restricted):")
    for k, v in pss["namespace_labels"].items():
        print(f"    {k}: {v}")

    print(f"\n  Required security controls:")
    sc = pss["required_fields"]["securityContext"]
    print(f"    runAsNonRoot         : {sc['runAsNonRoot']}")
    print(f"    runAsUser            : UID >= {sc['runAsUser']['minimum']}")
    print(f"    seccompProfile.type  : {sc['seccompProfile']['type']}")
    csc = pss["required_fields"]["containers[*].securityContext"]
    print(f"    allowPrivilegeEscalation : {csc['allowPrivilegeEscalation']}")
    print(f"    readOnlyRootFilesystem   : {csc['readOnlyRootFilesystem']}")
    print(f"    privileged               : {csc['privileged']}")
    print(f"    capabilities.drop        : {csc['capabilities']['drop']}")

    print(f"\n  Allowed volume types:")
    for vt in pss["required_fields"]["volumes"]["allowed_types"]:
        print(f"    + {vt}")
    print(f"\n  Forbidden volume types:")
    for vt in pss["required_fields"]["volumes"]["forbidden_types"]:
        print(f"    ✗ {vt}")

    # Validate a compliant pod
    print(f"\n  Validating compliant pod example...")
    compliant_spec = pss["example_compliant_pod"]
    result = validate_pod_security(compliant_spec)
    print(f"  Validation result: {result['summary']}")
    if result["warnings"]:
        for w in result["warnings"]:
            print(f"    {w}")

    # Validate a non-compliant pod
    non_compliant_spec = {
        "metadata": {"name": "bad-pod", "labels": {}},
        "spec": {
            "securityContext": {"runAsUser": 0},
            "containers": [
                {
                    "name": "root-container",
                    "securityContext": {
                        "privileged": True,
                        "allowPrivilegeEscalation": True,
                        "readOnlyRootFilesystem": False,
                        "capabilities": {"drop": [], "add": ["SYS_ADMIN", "NET_ADMIN"]},
                    },
                    "resources": {},
                }
            ],
        },
    }
    print(f"\n  Validating non-compliant pod (privileged root container)...")
    bad_result = validate_pod_security(non_compliant_spec)
    print(f"  Validation result: {bad_result['summary']}")
    for v in bad_result["violations"][:5]:
        print(f"    {v}")
    if len(bad_result["violations"]) > 5:
        print(f"    ... +{len(bad_result['violations']) - 5} more violations")

    # ── SECTION 4: Network Policies ───────────────────────────────────────────
    _print_section(4, "Network Policies (Default Deny All + Whitelist)")
    np = NETWORK_POLICIES
    print(f"  Default policy   : {np['default_deny']['metadata']['name']}")
    print(f"  Policy types     : {np['default_deny']['spec']['policyTypes']}")
    print(f"  Effect           : {np['default_deny']['description']}")
    print(f"\n  Whitelist rules ({len(np['whitelist_policies'])}):")
    for policy_key, policy in np["whitelist_policies"].items():
        desc = policy["description"]
        ns = policy["metadata"]["namespace"]
        print(f"    ALLOW [{ns}] {desc}")
    print(f"\n  Explicit denials ({len(np['explicit_denials'])}):")
    for policy_key, policy in np["explicit_denials"].items():
        print(f"    DENY  {policy['description']}")

    # ── SECTION 5: OPA Gatekeeper Policies ───────────────────────────────────
    _print_section(5, "OPA Gatekeeper Policies (8 constraints)")
    templates = OPA_GATEKEEPER_POLICIES["constraint_templates"]
    print(f"  {'Constraint':<40} {'Enforcement':<10} {'Severity':<10} {'Applies To'}")
    print(f"  {'─' * 38} {'─' * 9} {'─' * 9} {'─' * 25}")
    for t in templates:
        applies = ", ".join(t["applies_to"])
        print(f"  {t['name']:<40} {t['enforcement']:<10} {t['severity']:<10} {applies}")

    print(f"\n  Constraint instances deployed: {len(OPA_GATEKEEPER_POLICIES['constraint_instances'])}")
    for ci in OPA_GATEKEEPER_POLICIES["constraint_instances"]:
        ns_display = ", ".join(ci["namespaces"])
        print(f"    {ci['name']:<45} namespaces: {ns_display}")

    # ── SECTION 6: Falco Runtime Detection ───────────────────────────────────
    _print_section(6, "Falco Runtime Detection (6 règles + simulation)")
    print(f"  {'Rule ID':<12} {'Priority':<10} {'Name'}")
    print(f"  {'─' * 10} {'─' * 9} {'─' * 45}")
    for rule in FALCO_RULES:
        print(f"  {rule['id']:<12} {rule['priority']:<10} {rule['name']}")

    print(f"\n  Simulating Falco alerts...")

    simulations = [
        ("Terminal shell in container", "wave-engine-7d9f8b-xkz4p", "unknown-user"),
        ("Cryptocurrency mining detected", "api-gateway-5c8d9f-m2n3p", "root"),
        ("k8s secret read by non-allowed process", "caelum-audit-6b7c8d-p9q1r", "system:serviceaccount"),
    ]

    for event_type, container, user in simulations:
        alert = simulate_falco_alert(event_type, container, user)
        print(f"\n  [{alert['priority']}] {alert['rule_name']}")
        print(f"    Alert ID    : {alert['alert_id']}")
        print(f"    Container   : {alert['container']}")
        print(f"    User        : {alert['user']}")
        print(f"    Timestamp   : {alert['timestamp']}")
        print(f"    Escalation  : {alert['escalation_policy']}")
        print(f"    CSDDD flag  : {'YES' if alert['csddd_relevant'] else 'no'}")
        print(f"    Remediation : {alert['remediation_steps'][0]}")

    # ── SECTION 7: CIS Benchmark Scan ────────────────────────────────────────
    _print_section(7, "CIS Benchmark Scan Simulation (~87%)")
    cis_result = run_cis_benchmark()
    print(f"  Benchmark        : {cis_result['benchmark']}")
    print(f"  Cluster          : {cis_result['cluster']}")
    print(f"  Scan timestamp   : {cis_result['scan_timestamp']}")
    print(f"  Overall status   : {cis_result['overall_status']}")
    print()
    print(f"  Score            : {cis_result['score_percent']}%  (target: {cis_result['target_score_percent']}%)")
    print(f"  Passed checks    : {cis_result['passed_checks']} / {cis_result['total_checks']}")
    print(f"  Failed checks    : {cis_result['failed_count']}")
    print(f"  Warnings         : {cis_result['warnings_count']}")
    print(f"\n  Section scores:")
    for section_title, sec_score in cis_result["section_scores"].items():
        bar_len = int(sec_score["score_percent"] / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(
            f"    {section_title:<35} {bar} "
            f"{sec_score['score_percent']:>5.1f}%  "
            f"({sec_score['passed']}/{sec_score['total']})"
        )

    print(f"\n  Failed checks and remediation:")
    for step in cis_result["remediation_steps"]:
        print(f"    {step}")

    print(f"\n  Next audit date  : {cis_result['next_audit_date']}")

    # ── SECTION 8: Secret Management ─────────────────────────────────────────
    _print_section(8, "Secret Management (External Secrets Operator)")
    sm = SECRET_MANAGEMENT
    print(f"  Strategy         : {sm['strategy']}")
    print(f"  Native k8s secrets: {sm['native_k8s_secrets']}")
    print(f"\n  Components:")
    eso = sm["components"]["external_secrets_operator"]
    print(f"    ESO version    : {eso['version']}")
    print(f"    Helm chart     : {eso['helm_chart']}")
    print(f"    Namespace      : {eso['namespace']}")
    vault = sm["components"]["hashicorp_vault"]
    print(f"\n    Vault version  : {vault['version']}")
    print(f"    Auth method    : {vault['auth_method']}")
    print(f"    Deployment     : {vault['deployment']}")
    print(f"    Secret engines :")
    for engine in vault["secret_engines"]:
        print(f"      path={engine['path']:<25} type={engine['type']:<12} — {engine['description']}")
    print(f"\n  Encryption at rest:")
    enc = sm["encryption_at_rest"]
    print(f"    etcd   : {enc['etcd']}")
    print(f"    Vault  : {enc['vault']}")
    print(f"    Transit: {enc['transit_key']}")
    print(f"\n  Admission controllers enabled:")
    for ac in ADMISSION_CONTROLLERS["enabled"]:
        critical_flag = " [CRITICAL]" if ac.get("critical") else ""
        print(f"    + {ac['name']:<30} {ac['description']}{critical_flag}")

    # ── Final status ──────────────────────────────────────────────────────────
    print()
    print(_separator("", "━"))
    print(
        f"  Kubernetes Security Agent — PRÊT "
        f"(K8s {KUBERNETES_VERSION} / RBAC / OPA / Falco / CIS Benchmark)"
    )
    print(_separator("", "━"))
    print()


if __name__ == "__main__":
    main()

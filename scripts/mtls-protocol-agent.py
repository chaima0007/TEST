"""
Agent Protocole mTLS (Mutual TLS) — authentification mutuelle TLS entre agents CaelumSwarm™.
Certificats X.509, rotation, révocation CRL/OCSP et zero-trust selon RFC 8446, RFC 5280,
NIST SP 800-52.

Références normatives :
  - RFC 8446 : TLS 1.3
  - RFC 5280 : Internet X.509 PKI Certificate and CRL Profile
  - NIST SP 800-52 Rev. 2 : Guidelines for TLS Implementations
"""

import hashlib
import secrets
import datetime
from typing import Optional

# ---------------------------------------------------------------------------
# 1. CONSTANTES DE DONNÉES
# ---------------------------------------------------------------------------

TLS_CONFIGURATIONS: dict = {
    "STRICT_MTLS": {
        "label": "mTLS Strict — Production CaelumSwarm™",
        "tls_version": "TLS 1.3",
        "cipher_suites": [
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
        ],
        "certificate_validity_days": 90,
        "require_client_cert": True,
        "ocsp_stapling": True,
        "hsts_max_age_seconds": 63072000,  # 2 ans
        "caelum_environment": "production",
    },
    "STANDARD_MTLS": {
        "label": "mTLS Standard — Staging CaelumSwarm™",
        "tls_version": "TLS 1.3",
        "cipher_suites": [
            "TLS_AES_256_GCM_SHA384",
            "TLS_AES_128_GCM_SHA256",
            "TLS_CHACHA20_POLY1305_SHA256",
        ],
        "certificate_validity_days": 180,
        "require_client_cert": True,
        "ocsp_stapling": True,
        "hsts_max_age_seconds": 31536000,  # 1 an
        "caelum_environment": "staging",
    },
    "DEVELOPMENT": {
        "label": "mTLS Développement — Local CaelumSwarm™",
        "tls_version": "TLS 1.3",
        "cipher_suites": [
            "TLS_AES_128_GCM_SHA256",
            "TLS_CHACHA20_POLY1305_SHA256",
        ],
        "certificate_validity_days": 365,
        "require_client_cert": False,
        "ocsp_stapling": False,
        "hsts_max_age_seconds": 86400,  # 1 jour
        "caelum_environment": "development",
    },
}

CERTIFICATE_AUTHORITY: dict = {
    "ROOT_CA": {
        "label": "Caelum Partners Root Certificate Authority",
        "key_algorithm": "ECDSA P-384",
        "validity_years": 20,
        "storage": "HSM — air-gapped, coffre physique",
        "purpose": "Signature des CA intermédiaires uniquement — jamais exposée en ligne",
        "revocation_mechanism": "CRL hors-ligne uniquement",
    },
    "INTERMEDIATE_CA": {
        "label": "Caelum Partners Intermediate CA — SwarmNet",
        "key_algorithm": "ECDSA P-384",
        "validity_years": 10,
        "storage": "HSM — accès restreint aux opérateurs PKI",
        "purpose": "Émission des CA émettrices par environnement",
        "revocation_mechanism": "CRL + OCSP (délai max 4h)",
    },
    "ISSUING_CA": {
        "label": "Caelum Partners Issuing CA — Agents",
        "key_algorithm": "ECDSA P-256",
        "validity_years": 3,
        "storage": "HSM en ligne — cluster haute disponibilité",
        "purpose": "Émission directe des certificats agents CaelumSwarm™",
        "revocation_mechanism": "OCSP Stapling (réponse < 60s) + CRL delta 1h",
    },
}

AGENT_CERTIFICATES: dict = {
    "WAVE_ENGINE_CERT": {
        "cn": "wave-engine.agents.caelumswarm.internal",
        "san_list": [
            "wave-engine.agents.caelumswarm.internal",
            "wave-engine-01.agents.caelumswarm.internal",
            "wave-engine-02.agents.caelumswarm.internal",
        ],
        "key_usage": ["digitalSignature", "keyAgreement"],
        "extended_key_usage": ["clientAuth", "serverAuth"],
        "validity_days": 90,
        "rotation_frequency_days": 60,
        "pinning_required": True,
    },
    "API_GATEWAY_CERT": {
        "cn": "api-gateway.caelumswarm.internal",
        "san_list": [
            "api-gateway.caelumswarm.internal",
            "api.caelumpartners.com",
            "gateway.caelumswarm.internal",
        ],
        "key_usage": ["digitalSignature", "keyEncipherment"],
        "extended_key_usage": ["serverAuth", "clientAuth"],
        "validity_days": 90,
        "rotation_frequency_days": 60,
        "pinning_required": True,
    },
    "REPORT_AGENT_CERT": {
        "cn": "report-agent.agents.caelumswarm.internal",
        "san_list": [
            "report-agent.agents.caelumswarm.internal",
            "reports.caelumswarm.internal",
        ],
        "key_usage": ["digitalSignature", "keyAgreement"],
        "extended_key_usage": ["clientAuth"],
        "validity_days": 90,
        "rotation_frequency_days": 75,
        "pinning_required": False,
    },
    "PRESS_AGENT_CERT": {
        "cn": "press-agent.agents.caelumswarm.internal",
        "san_list": [
            "press-agent.agents.caelumswarm.internal",
            "press.caelumswarm.internal",
        ],
        "key_usage": ["digitalSignature", "keyAgreement"],
        "extended_key_usage": ["clientAuth"],
        "validity_days": 90,
        "rotation_frequency_days": 75,
        "pinning_required": False,
    },
    "LEGAL_WATCH_CERT": {
        "cn": "legal-watch.agents.caelumswarm.internal",
        "san_list": [
            "legal-watch.agents.caelumswarm.internal",
            "legal.caelumswarm.internal",
            "compliance.caelumswarm.internal",
        ],
        "key_usage": ["digitalSignature", "keyAgreement", "nonRepudiation"],
        "extended_key_usage": ["clientAuth", "emailProtection"],
        "validity_days": 90,
        "rotation_frequency_days": 60,
        "pinning_required": True,
    },
    "ADMIN_CONSOLE_CERT": {
        "cn": "admin-console.caelumswarm.internal",
        "san_list": [
            "admin-console.caelumswarm.internal",
            "admin.caelumpartners.com",
        ],
        "key_usage": ["digitalSignature", "keyEncipherment"],
        "extended_key_usage": ["serverAuth", "clientAuth"],
        "validity_days": 60,
        "rotation_frequency_days": 45,
        "pinning_required": True,
    },
}

MTLS_THREAT_MITIGATIONS: dict = {
    "MAN_IN_THE_MIDDLE": {
        "label": "Attaque de l'homme du milieu (MITM)",
        "mitigation_mechanism": (
            "Authentification mutuelle obligatoire — le serveur ET le client "
            "présentent chacun un certificat X.509 signé par la CA racine Caelum"
        ),
        "tls_feature_used": "mTLS handshake bidirectionnel (RFC 8446 §4.3.2)",
        "detection_method": "Échec de vérification de la chaîne de confiance — alerte SIEM immédiate",
        "severity": "CRITIQUE",
    },
    "CERTIFICATE_SPOOFING": {
        "label": "Usurpation de certificat",
        "mitigation_mechanism": (
            "Certificate Pinning activé pour les agents critiques + vérification OCSP "
            "en temps réel avant acceptation de chaque connexion"
        ),
        "tls_feature_used": "OCSP Stapling + Certificate Pinning (RFC 7469)",
        "detection_method": "Divergence de l'empreinte SHA-256 par rapport au pin enregistré",
        "severity": "CRITIQUE",
    },
    "REPLAY_ATTACK": {
        "label": "Attaque par rejeu (Replay Attack)",
        "mitigation_mechanism": (
            "Nonces TLS 1.3 uniques par session + session tickets à durée de vie "
            "limitée (max 24h) avec rotation automatique des clés de session"
        ),
        "tls_feature_used": "TLS 1.3 Session Tickets + Anti-replay (RFC 8446 §8)",
        "detection_method": "Détection de session_id en doublon dans le cache de session du gateway",
        "severity": "ÉLEVÉ",
    },
    "EXPIRED_CERT_ABUSE": {
        "label": "Abus de certificat expiré",
        "mitigation_mechanism": (
            "Vérification stricte de la date de validité (notAfter) à chaque handshake — "
            "rotation automatisée J-30 avec alerte escaladée J-15 et J-7"
        ),
        "tls_feature_used": "Validation temporelle X.509 (RFC 5280 §6.1.3)",
        "detection_method": "Comparaison notAfter vs timestamp courant UTC — rejet immédiat si dépassé",
        "severity": "ÉLEVÉ",
    },
    "PRIVATE_KEY_COMPROMISE": {
        "label": "Compromission de clé privée",
        "mitigation_mechanism": (
            "Clés stockées exclusivement en HSM (FIPS 140-2 Level 3) — "
            "révocation OCSP < 60s + CRL delta publiée toutes les heures"
        ),
        "tls_feature_used": "CRL + OCSP Stapling (RFC 6960) + HSM non-exportable keys",
        "detection_method": "Monitoring HSM des accès anormaux + alertes sur révocations non planifiées",
        "severity": "CRITIQUE",
    },
    "WEAK_CIPHER_DOWNGRADE": {
        "label": "Attaque par rétrogradation de chiffrement (Downgrade Attack)",
        "mitigation_mechanism": (
            "Liste blanche stricte de suites cryptographiques TLS 1.3 uniquement — "
            "aucune négociation TLS ≤ 1.2 acceptée en production"
        ),
        "tls_feature_used": "TLS 1.3 downgrade protection (RFC 8446 §4.1.3) + HSTS preload",
        "detection_method": (
            "Tentative de ClientHello avec version < 0x0304 → rejet + log SIEM "
            "avec empreinte IP source"
        ),
        "severity": "ÉLEVÉ",
    },
}

# ---------------------------------------------------------------------------
# 2. FONCTIONS PRINCIPALES
# ---------------------------------------------------------------------------

def generate_certificate_config(agent_id: str, environment: str) -> dict:
    """
    Génère la configuration de certificat X.509 pour un agent CaelumSwarm™.

    Paramètres
    ----------
    agent_id    : Identifiant de l'agent (ex. 'WAVE_ENGINE_CERT')
    environment : Environnement cible ('production', 'staging', 'development')

    Retourne
    --------
    dict avec cert_subject, san_extensions, key_usage_flags, validity_period,
    fingerprint_sha256 et serial_number.
    """
    agent_cert = AGENT_CERTIFICATES.get(agent_id, AGENT_CERTIFICATES["WAVE_ENGINE_CERT"])

    tls_profile_key = {
        "production": "STRICT_MTLS",
        "staging": "STANDARD_MTLS",
        "development": "DEVELOPMENT",
    }.get(environment, "STANDARD_MTLS")

    tls_profile = TLS_CONFIGURATIONS[tls_profile_key]
    validity_days = agent_cert["validity_days"]

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    not_before = now_utc
    not_after = now_utc + datetime.timedelta(days=validity_days)

    # Empreinte simulée SHA-256 (64 caractères hex) — représentation déterministe
    fingerprint_seed = f"{agent_id}:{environment}:{not_before.isoformat()}"
    fingerprint_sha256 = hashlib.sha256(fingerprint_seed.encode()).hexdigest()

    # Numéro de série cryptographiquement aléatoire (128 bits → 32 hex chars)
    serial_number = secrets.token_hex(16).upper()
    # Formatage lisible en groupes de 2 (notation X.509 standard)
    serial_formatted = ":".join(
        serial_number[i : i + 2] for i in range(0, len(serial_number), 2)
    )

    cert_subject = {
        "CN": agent_cert["cn"],
        "O": "Caelum Partners SAS",
        "OU": f"CaelumSwarm™ — {environment.capitalize()}",
        "C": "FR",
        "L": "Paris",
        "ST": "Île-de-France",
    }

    san_extensions = {
        "subject_alternative_names": agent_cert["san_list"],
        "san_count": len(agent_cert["san_list"]),
        "include_ip_sans": False,
        "critical": False,
    }

    key_usage_flags = {
        "key_usage": agent_cert["key_usage"],
        "extended_key_usage": agent_cert["extended_key_usage"],
        "key_algorithm": CERTIFICATE_AUTHORITY["ISSUING_CA"]["key_algorithm"],
        "key_size_bits": 256,
        "critical": True,
    }

    validity_period = {
        "not_before": not_before.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "not_after": not_after.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "validity_days": validity_days,
        "rotation_due": (
            now_utc + datetime.timedelta(days=agent_cert["rotation_frequency_days"])
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    return {
        "agent_id": agent_id,
        "environment": environment,
        "tls_profile": tls_profile_key,
        "tls_version": tls_profile["tls_version"],
        "cert_subject": cert_subject,
        "san_extensions": san_extensions,
        "key_usage_flags": key_usage_flags,
        "validity_period": validity_period,
        "fingerprint_sha256": fingerprint_sha256,
        "serial_number": serial_formatted,
        "issuer": CERTIFICATE_AUTHORITY["ISSUING_CA"]["label"],
        "pinning_required": agent_cert["pinning_required"],
        "ocsp_stapling": tls_profile["ocsp_stapling"],
    }


def verify_mtls_handshake(client_cert: dict, server_cert: dict) -> dict:
    """
    Simule un handshake mTLS entre deux agents CaelumSwarm™.

    Vérifie : liste blanche CN, expiration, chaîne de confiance, compatibilité cipher.

    Paramètres
    ----------
    client_cert : dict retourné par generate_certificate_config (côté client)
    server_cert : dict retourné par generate_certificate_config (côté serveur)

    Retourne
    --------
    dict avec handshake_success, tls_version_negotiated, cipher_selected,
    mutual_auth_confirmed, latency_ms, et rejection_reason si échec.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # Liste blanche des CN autorisés dans CaelumSwarm™
    cn_whitelist = {cert["cn"] for cert in AGENT_CERTIFICATES.values()}

    rejection_reason: Optional[str] = None

    # --- Vérification 1 : CN dans la liste blanche ---
    client_cn = client_cert.get("cert_subject", {}).get("CN", "")
    server_cn = server_cert.get("cert_subject", {}).get("CN", "")

    if client_cn not in cn_whitelist:
        rejection_reason = (
            f"CN client '{client_cn}' absent de la liste blanche CaelumSwarm™ — "
            "authentification refusée (zero-trust)"
        )
    elif server_cn not in cn_whitelist:
        rejection_reason = (
            f"CN serveur '{server_cn}' absent de la liste blanche CaelumSwarm™ — "
            "connexion rejetée"
        )

    # --- Vérification 2 : Expiration des certificats ---
    if not rejection_reason:
        for label, cert in [("client", client_cert), ("serveur", server_cert)]:
            not_after_str = cert.get("validity_period", {}).get("not_after", "")
            try:
                not_after_dt = datetime.datetime.strptime(
                    not_after_str, "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=datetime.timezone.utc)
                if now_utc > not_after_dt:
                    rejection_reason = (
                        f"Certificat {label} '{cert.get('cert_subject', {}).get('CN')}' "
                        f"expiré depuis {not_after_str} — handshake interrompu (RFC 5280 §6.1.3)"
                    )
                    break
            except ValueError:
                rejection_reason = f"Format de date invalide dans le certificat {label}"
                break

    # --- Vérification 3 : Chaîne de confiance (même émetteur CA) ---
    if not rejection_reason:
        client_issuer = client_cert.get("issuer", "")
        server_issuer = server_cert.get("issuer", "")
        expected_issuer = CERTIFICATE_AUTHORITY["ISSUING_CA"]["label"]

        if client_issuer != expected_issuer or server_issuer != expected_issuer:
            rejection_reason = (
                f"Chaîne de confiance rompue — émetteur inattendu. "
                f"Attendu : '{expected_issuer}' | "
                f"Client : '{client_issuer}' | Serveur : '{server_issuer}'"
            )

    # --- Vérification 4 : Compatibilité des suites cryptographiques ---
    cipher_selected: Optional[str] = None
    tls_version_negotiated: Optional[str] = None

    if not rejection_reason:
        client_profile = TLS_CONFIGURATIONS.get(
            client_cert.get("tls_profile", "STRICT_MTLS"), {}
        )
        server_profile = TLS_CONFIGURATIONS.get(
            server_cert.get("tls_profile", "STRICT_MTLS"), {}
        )

        client_ciphers = set(client_profile.get("cipher_suites", []))
        server_ciphers = set(server_profile.get("cipher_suites", []))
        common_ciphers = client_ciphers & server_ciphers

        # Priorité TLS 1.3 : AES-256-GCM en premier si disponible
        preferred_order = [
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_128_GCM_SHA256",
        ]

        for preferred in preferred_order:
            if preferred in common_ciphers:
                cipher_selected = preferred
                break

        if not cipher_selected:
            rejection_reason = (
                "Aucune suite cryptographique commune — downgrade impossible en TLS 1.3. "
                f"Client : {sorted(client_ciphers)} | Serveur : {sorted(server_ciphers)}"
            )
        else:
            tls_version_negotiated = "TLS 1.3"

    # --- Résultat du handshake ---
    handshake_success = rejection_reason is None

    # Latence simulée (handshake mTLS TLS 1.3 = 1 RTT)
    # Base 8ms + variation pseudo-aléatoire 0-5ms
    latency_seed = int(
        hashlib.sha256(
            f"{client_cn}:{server_cn}:{now_utc.second}".encode()
        ).hexdigest(),
        16,
    )
    latency_ms = round(8.0 + (latency_seed % 50) / 10, 2) if handshake_success else 0.0

    result = {
        "handshake_success": handshake_success,
        "tls_version_negotiated": tls_version_negotiated,
        "cipher_selected": cipher_selected,
        "mutual_auth_confirmed": handshake_success,
        "client_cn": client_cn,
        "server_cn": server_cn,
        "latency_ms": latency_ms,
        "timestamp_utc": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ocsp_check": "VALID" if handshake_success else "N/A",
        "zero_trust_decision": "AUTORISER" if handshake_success else "BLOQUER",
    }

    if not handshake_success:
        result["rejection_reason"] = rejection_reason

    return result


def manage_certificate_lifecycle(cert_registry: list) -> dict:
    """
    Analyse le cycle de vie d'un ensemble de certificats CaelumSwarm™.

    Identifie les certificats expirant bientôt (< 30 jours), déjà expirés,
    génère un planning de rotation par urgence et identifie les candidats
    à l'automatisation.

    Paramètres
    ----------
    cert_registry : Liste de dicts de certificats (format generate_certificate_config)

    Retourne
    --------
    dict avec expiring_soon, already_expired, rotation_schedule, automation_candidates,
    effort_hours.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    thirty_days_later = now_utc + datetime.timedelta(days=30)
    seven_days_later = now_utc + datetime.timedelta(days=7)

    expiring_soon = []
    already_expired = []
    rotation_schedule = []
    automation_candidates = []

    for cert in cert_registry:
        cn = cert.get("cert_subject", {}).get("CN", cert.get("agent_id", "inconnu"))
        not_after_str = cert.get("validity_period", {}).get("not_after", "")
        rotation_due_str = cert.get("validity_period", {}).get("rotation_due", "")
        pinning_required = cert.get("pinning_required", False)
        agent_id = cert.get("agent_id", "UNKNOWN")

        try:
            not_after_dt = datetime.datetime.strptime(
                not_after_str, "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            not_after_dt = now_utc  # traitement sécuritaire : considéré expiré

        days_remaining = (not_after_dt - now_utc).days

        if not_after_dt <= now_utc:
            already_expired.append({
                "agent_id": agent_id,
                "cn": cn,
                "expired_since": not_after_str,
                "days_overdue": abs(days_remaining),
                "action_requise": "RÉVOCATION IMMÉDIATE + RENOUVELLEMENT D'URGENCE",
                "priorité": "CRITIQUE",
            })
        elif not_after_dt <= thirty_days_later:
            urgency = "CRITIQUE" if not_after_dt <= seven_days_later else "ÉLEVÉ"
            expiring_soon.append({
                "agent_id": agent_id,
                "cn": cn,
                "expires": not_after_str,
                "days_remaining": days_remaining,
                "urgency": urgency,
                "pinning_impact": pinning_required,
            })

        # Planning de rotation
        try:
            rotation_due_dt = datetime.datetime.strptime(
                rotation_due_str, "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=datetime.timezone.utc)
            days_to_rotation = (rotation_due_dt - now_utc).days
        except ValueError:
            days_to_rotation = days_remaining // 2

        rotation_urgency = (
            "IMMÉDIAT" if days_remaining <= 7
            else "URGENT" if days_remaining <= 30
            else "PLANIFIÉ" if days_to_rotation <= 30
            else "NOMINAL"
        )

        rotation_schedule.append({
            "agent_id": agent_id,
            "cn": cn,
            "rotation_due": rotation_due_str,
            "days_to_rotation": days_to_rotation,
            "urgency": rotation_urgency,
            "pinning_requires_coordination": pinning_required,
        })

        # Candidats à l'automatisation : certificats sans pinning (rotation plus simple)
        if not pinning_required:
            automation_candidates.append({
                "agent_id": agent_id,
                "cn": cn,
                "reason": "Pas de certificate pinning — rotation automatisée via ACME/Cert-Manager possible",
                "recommended_tool": "cert-manager (Kubernetes) ou HashiCorp Vault PKI Engine",
            })

    # Tri par urgence
    urgency_order = {"IMMÉDIAT": 0, "URGENT": 1, "PLANIFIÉ": 2, "NOMINAL": 3}
    rotation_schedule.sort(key=lambda x: urgency_order.get(x["urgency"], 4))

    # Estimation de l'effort (heures ingénierie)
    effort_hours = {
        "renouvellement_manuel": len(cert_registry) * 0.5,
        "avec_automatisation": len(automation_candidates) * 0.1
        + (len(cert_registry) - len(automation_candidates)) * 0.4,
        "setup_initial_automation": 8.0,
        "économie_annuelle_heures": round(
            (len(automation_candidates) * 0.5 * 12)
            - (len(automation_candidates) * 0.1 * 12)
            - 8.0,
            1,
        ),
    }

    return {
        "analyse_date_utc": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_certificats": len(cert_registry),
        "expiring_soon": expiring_soon,
        "already_expired": already_expired,
        "rotation_schedule": rotation_schedule,
        "automation_candidates": automation_candidates,
        "effort_hours": effort_hours,
        "recommandation_globale": (
            "Automatiser la rotation via cert-manager pour les agents sans pinning. "
            "Maintenir un processus manuel coordonné pour les agents avec certificate pinning."
        ),
    }


def generate_mtls_policy(service_mesh: list) -> dict:
    """
    Génère une politique mTLS complète pour le service mesh CaelumSwarm™.

    Paramètres
    ----------
    service_mesh : Liste de noms de services (ex. ['wave-engine', 'api-gateway'])

    Retourne
    --------
    dict avec peer_authentication, destination_rules, cert_pinning_config,
    zero_trust_assertions, policy_yaml_preview.
    """
    peer_authentication = {}
    destination_rules = {}
    cert_pinning_config = {}

    # Correspondance service → agent cert
    service_to_cert = {
        "wave-engine": "WAVE_ENGINE_CERT",
        "api-gateway": "API_GATEWAY_CERT",
        "report-agent": "REPORT_AGENT_CERT",
        "press-agent": "PRESS_AGENT_CERT",
        "legal-watch": "LEGAL_WATCH_CERT",
        "admin-console": "ADMIN_CONSOLE_CERT",
    }

    for service in service_mesh:
        cert_key = service_to_cert.get(service, "WAVE_ENGINE_CERT")
        agent_cert = AGENT_CERTIFICATES[cert_key]

        # Politique d'authentification par les pairs
        mode = "STRICT" if "production" in agent_cert["cn"] or True else "PERMISSIVE"
        peer_authentication[service] = {
            "mode": mode,
            "tls_version": "TLS 1.3",
            "require_client_cert": True,
            "port_selector": 443,
            "justification": (
                "Zero-trust : aucune connexion non-mTLS acceptée en maillage de services"
            ),
        }

        # Règles de destination
        destination_rules[service] = {
            "host": agent_cert["cn"],
            "traffic_policy": {
                "tls_mode": "ISTIO_MUTUAL",
                "tls_version": "TLSV1_3",
                "cipher_suites": TLS_CONFIGURATIONS["STRICT_MTLS"]["cipher_suites"],
                "sni": agent_cert["cn"],
            },
            "load_balancer": "ROUND_ROBIN",
            "connection_pool": {
                "http2_max_requests": 1000,
                "connect_timeout": "5s",
            },
        }

        # Configuration du certificate pinning
        if agent_cert["pinning_required"]:
            pin_seed = f"pin:{cert_key}:{agent_cert['cn']}"
            pin_sha256 = hashlib.sha256(pin_seed.encode()).hexdigest()
            cert_pinning_config[service] = {
                "enabled": True,
                "pin_sha256": pin_sha256,
                "backup_pin_sha256": hashlib.sha256(
                    f"backup:{pin_seed}".encode()
                ).hexdigest(),
                "report_uri": "https://pki.caelumpartners.com/pinning-report",
                "max_age_seconds": 2592000,  # 30 jours
                "include_subdomains": False,
            }
        else:
            cert_pinning_config[service] = {
                "enabled": False,
                "reason": "Agent non-critique — pinning désactivé pour faciliter la rotation",
            }

    # Assertions zero-trust
    zero_trust_assertions = [
        {
            "id": "ZT-001",
            "assertion": "Toute connexion inter-agents DOIT présenter un certificat X.509 valide",
            "enforcement": "STRICT — rejet immédiat sans certificat client",
            "reference": "NIST SP 800-207 §3.3 (Zero Trust Architecture)",
        },
        {
            "id": "ZT-002",
            "assertion": "Les certificats DOIVENT être émis par la Caelum Issuing CA uniquement",
            "enforcement": "Vérification de chaîne complète à chaque handshake",
            "reference": "RFC 5280 §6.1 (Certification Path Validation)",
        },
        {
            "id": "ZT-003",
            "assertion": "Aucune suite cryptographique antérieure à TLS 1.3 n'est acceptée",
            "enforcement": "Rejet des ClientHello avec version < 0x0304",
            "reference": "RFC 8446 §4.1.3 (Downgrade Protection)",
        },
        {
            "id": "ZT-004",
            "assertion": "Le statut de révocation DOIT être vérifié via OCSP avant chaque session",
            "enforcement": "OCSP Stapling obligatoire — délai de réponse max 60s",
            "reference": "RFC 6960 §2.1 (OCSP Basic Response)",
        },
        {
            "id": "ZT-005",
            "assertion": "Les clés privées NE DOIVENT JAMAIS quitter le HSM",
            "enforcement": "Opérations cryptographiques effectuées dans le HSM (FIPS 140-2 L3)",
            "reference": "NIST SP 800-57 Part 1 §8.1 (Key Management)",
        },
    ]

    # Aperçu YAML de la politique (Istio PeerAuthentication style)
    yaml_lines = ["# Politique mTLS CaelumSwarm™ — Istio PeerAuthentication", "---"]
    for service in service_mesh[:3]:  # Aperçu des 3 premiers services
        cert_key = service_to_cert.get(service, "WAVE_ENGINE_CERT")
        agent_cert = AGENT_CERTIFICATES[cert_key]
        yaml_lines += [
            f"apiVersion: security.istio.io/v1beta1",
            f"kind: PeerAuthentication",
            f"metadata:",
            f"  name: {service}-mtls-policy",
            f"  namespace: caelumswarm",
            f"spec:",
            f"  selector:",
            f"    matchLabels:",
            f"      app: {service}",
            f"  mtls:",
            f"    mode: STRICT",
            f"---",
        ]

    policy_yaml_preview = "\n".join(yaml_lines)

    return {
        "policy_name": "CaelumSwarm™ mTLS Zero-Trust Policy",
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "services_covered": service_mesh,
        "peer_authentication": peer_authentication,
        "destination_rules": destination_rules,
        "cert_pinning_config": cert_pinning_config,
        "zero_trust_assertions": zero_trust_assertions,
        "policy_yaml_preview": policy_yaml_preview,
        "compliance_references": [
            "RFC 8446 — TLS 1.3",
            "RFC 5280 — X.509 PKI",
            "RFC 6960 — OCSP",
            "NIST SP 800-52 Rev. 2 — TLS Guidelines",
            "NIST SP 800-207 — Zero Trust Architecture",
        ],
    }


# ---------------------------------------------------------------------------
# 3. DÉMONSTRATION
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Démonstration complète du protocole mTLS CaelumSwarm™.

    Étapes :
      1. Génération d'un certificat pour le Wave Engine
      2. Simulation d'un handshake mTLS entre deux agents
      3. Gestion du cycle de vie de 6 certificats
      4. Génération de la politique mTLS pour le service mesh CaelumSwarm™
    """
    separator = "=" * 70

    print(separator)
    print("  Agent Protocole mTLS — CaelumSwarm™ (Caelum Partners)")
    print("  Authentification mutuelle TLS · RFC 8446 · NIST SP 800-52")
    print(separator)

    # --- Étape 1 : Génération de certificat Wave Engine ---
    print("\n[1/4] Génération du certificat X.509 — Wave Engine (Production)")
    print("-" * 60)

    wave_cert = generate_certificate_config("WAVE_ENGINE_CERT", "production")
    print(f"  CN          : {wave_cert['cert_subject']['CN']}")
    print(f"  Organisation: {wave_cert['cert_subject']['O']}")
    print(f"  Émetteur    : {wave_cert['issuer']}")
    print(f"  Profil TLS  : {wave_cert['tls_profile']} ({wave_cert['tls_version']})")
    print(f"  Validité    : {wave_cert['validity_period']['not_before']}")
    print(f"             → {wave_cert['validity_period']['not_after']}")
    print(f"  Rotation    : {wave_cert['validity_period']['rotation_due']}")
    print(f"  Série       : {wave_cert['serial_number']}")
    print(f"  SHA-256     : {wave_cert['fingerprint_sha256']}")
    print(f"  Pinning     : {'OUI' if wave_cert['pinning_required'] else 'NON'}")
    print(f"  OCSP        : {'OUI' if wave_cert['ocsp_stapling'] else 'NON'}")
    san_list = wave_cert["san_extensions"]["subject_alternative_names"]
    print(f"  SAN ({len(san_list)})     : {', '.join(san_list)}")
    print("  → Certificat généré avec succès.")

    # --- Étape 2 : Simulation de handshake mTLS ---
    print("\n[2/4] Simulation du handshake mTLS — Wave Engine ↔ API Gateway")
    print("-" * 60)

    gateway_cert = generate_certificate_config("API_GATEWAY_CERT", "production")
    handshake = verify_mtls_handshake(wave_cert, gateway_cert)

    status_label = "SUCCÈS" if handshake["handshake_success"] else "ÉCHEC"
    print(f"  Résultat          : {status_label}")
    print(f"  Client            : {handshake['client_cn']}")
    print(f"  Serveur           : {handshake['server_cn']}")
    print(f"  Version TLS       : {handshake.get('tls_version_negotiated', 'N/A')}")
    print(f"  Suite choisie     : {handshake.get('cipher_selected', 'N/A')}")
    print(f"  Auth mutuelle     : {'OUI' if handshake['mutual_auth_confirmed'] else 'NON'}")
    print(f"  Latence simulée   : {handshake['latency_ms']} ms")
    print(f"  OCSP              : {handshake.get('ocsp_check', 'N/A')}")
    print(f"  Décision Zero-Trust: {handshake['zero_trust_decision']}")

    if not handshake["handshake_success"]:
        print(f"  Motif rejet       : {handshake.get('rejection_reason', 'inconnu')}")

    # Simulation d'un handshake échoué (certificat non whitelist)
    print("\n  [Test rejet] Simulation avec agent non autorisé...")
    fake_cert = {
        "cert_subject": {"CN": "agent-inconnu.externe.example.com"},
        "validity_period": {"not_after": "2099-12-31T23:59:59Z"},
        "issuer": CERTIFICATE_AUTHORITY["ISSUING_CA"]["label"],
        "tls_profile": "STRICT_MTLS",
    }
    rejected = verify_mtls_handshake(fake_cert, gateway_cert)
    print(f"  Résultat rejet    : {'SUCCÈS' if not rejected['handshake_success'] else 'ERREUR'}")
    print(f"  Motif             : {rejected.get('rejection_reason', 'N/A')[:80]}...")

    # --- Étape 3 : Gestion du cycle de vie ---
    print("\n[3/4] Analyse du cycle de vie — 6 certificats CaelumSwarm™")
    print("-" * 60)

    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # Construction d'un registre de certificats avec dates variées pour la démo
    cert_registry = []
    environments = [
        ("WAVE_ENGINE_CERT", "production"),
        ("API_GATEWAY_CERT", "production"),
        ("REPORT_AGENT_CERT", "staging"),
        ("PRESS_AGENT_CERT", "staging"),
        ("LEGAL_WATCH_CERT", "production"),
        ("ADMIN_CONSOLE_CERT", "production"),
    ]

    for i, (agent_id, env) in enumerate(environments):
        cert = generate_certificate_config(agent_id, env)
        # Simulation de dates variées : some near expiry, one expired
        if i == 0:
            # Expire dans 5 jours (critique)
            past = now_utc - datetime.timedelta(days=85)
            cert["validity_period"]["not_before"] = past.strftime("%Y-%m-%dT%H:%M:%SZ")
            cert["validity_period"]["not_after"] = (
                now_utc + datetime.timedelta(days=5)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
        elif i == 1:
            # Expire dans 20 jours (élevé)
            past = now_utc - datetime.timedelta(days=70)
            cert["validity_period"]["not_before"] = past.strftime("%Y-%m-%dT%H:%M:%SZ")
            cert["validity_period"]["not_after"] = (
                now_utc + datetime.timedelta(days=20)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
        elif i == 4:
            # Déjà expiré (urgence absolue)
            past = now_utc - datetime.timedelta(days=100)
            cert["validity_period"]["not_before"] = past.strftime("%Y-%m-%dT%H:%M:%SZ")
            cert["validity_period"]["not_after"] = (
                now_utc - datetime.timedelta(days=10)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
        cert_registry.append(cert)

    lifecycle = manage_certificate_lifecycle(cert_registry)

    print(f"  Total certificats analysés : {lifecycle['total_certificats']}")
    print(f"  Déjà expirés               : {len(lifecycle['already_expired'])}")
    print(f"  Expirant sous 30 jours     : {len(lifecycle['expiring_soon'])}")
    print(f"  Candidats à l'automatisation: {len(lifecycle['automation_candidates'])}")

    if lifecycle["already_expired"]:
        print("\n  CERTIFICATS EXPIRÉS :")
        for c in lifecycle["already_expired"]:
            print(f"    ✗ [{c['priorité']}] {c['cn']} — expiré depuis {c['days_overdue']} jours")

    if lifecycle["expiring_soon"]:
        print("\n  CERTIFICATS EXPIRANT BIENTÔT :")
        for c in lifecycle["expiring_soon"]:
            print(
                f"    ⚠ [{c['urgency']}] {c['cn']} — J-{c['days_remaining']} "
                f"({'pinning' if c['pinning_impact'] else 'sans pinning'})"
            )

    print("\n  PLANNING DE ROTATION (par urgence) :")
    for entry in lifecycle["rotation_schedule"][:4]:
        pin_note = " [coordination pinning requise]" if entry["pinning_requires_coordination"] else ""
        print(f"    [{entry['urgency']}] {entry['agent_id']}{pin_note}")

    effort = lifecycle["effort_hours"]
    print(f"\n  Effort estimation :")
    print(f"    Manuel           : {effort['renouvellement_manuel']:.1f}h")
    print(f"    Avec automation  : {effort['avec_automatisation']:.1f}h")
    print(f"    Setup automation : {effort['setup_initial_automation']:.1f}h")
    print(f"    Économie/an      : {effort['economie_annuelle_heures']:.1f}h" if
          'economie_annuelle_heures' in effort else
          f"    Économie/an      : {effort.get('économie_annuelle_heures', 'N/A')}h")

    # --- Étape 4 : Politique mTLS service mesh ---
    print("\n[4/4] Génération de la politique mTLS — Service Mesh CaelumSwarm™")
    print("-" * 60)

    swarm_services = [
        "wave-engine",
        "api-gateway",
        "report-agent",
        "press-agent",
        "legal-watch",
        "admin-console",
    ]

    policy = generate_mtls_policy(swarm_services)

    print(f"  Politique       : {policy['policy_name']}")
    print(f"  Générée le      : {policy['generated_at_utc']}")
    print(f"  Services couverts: {len(policy['services_covered'])}")

    print("\n  AUTHENTIFICATION PAR LES PAIRS :")
    for svc, auth in policy["peer_authentication"].items():
        print(f"    {svc:<18} → mode={auth['mode']}, port={auth['port_selector']}, "
              f"client_cert={'OUI' if auth['require_client_cert'] else 'NON'}")

    print("\n  CERTIFICATE PINNING :")
    for svc, pin in policy["cert_pinning_config"].items():
        status = f"pin SHA-256: {pin['pin_sha256'][:16]}..." if pin["enabled"] else "désactivé"
        print(f"    {svc:<18} → {status}")

    print("\n  ASSERTIONS ZERO-TRUST :")
    for zt in policy["zero_trust_assertions"]:
        print(f"    [{zt['id']}] {zt['assertion'][:65]}...")

    print("\n  APERÇU YAML POLITIQUE (extrait) :")
    yaml_preview_lines = policy["policy_yaml_preview"].split("\n")[:10]
    for line in yaml_preview_lines:
        print(f"    {line}")
    print("    ...")

    print("\n  Références de conformité :")
    for ref in policy["compliance_references"]:
        print(f"    • {ref}")

    # --- Bilan des menaces couvertes ---
    print(f"\n{separator}")
    print("  BILAN — Menaces mTLS couvertes")
    print(separator)
    for threat_key, threat in MTLS_THREAT_MITIGATIONS.items():
        print(f"  [{threat['severity']:<9}] {threat['label']}")
        print(f"             Mécanisme : {threat['mitigation_mechanism'][:65]}...")
        print()

    print(separator)
    print("  Protocole mTLS CaelumSwarm™ — Démonstration complète réussie.")
    print(f"  Conformité : RFC 8446 · RFC 5280 · RFC 6960 · NIST SP 800-52")
    print(separator)

    return True


# ---------------------------------------------------------------------------
# 4. POINT D'ENTRÉE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    raise SystemExit(0 if success else 1)

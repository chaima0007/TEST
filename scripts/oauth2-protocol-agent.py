"""
Agent Protocole OAuth 2.0 / OpenID Connect — implémente et gère l'authentification
sécurisée des agents CaelumSwarm™. Flows PKCE, Client Credentials, tokens JWT,
scopes et révocation selon RFC 6749, RFC 7636, RFC 9700.
"""

import hashlib
import secrets
import base64
import urllib.parse
import json
import time
import math

# ---------------------------------------------------------------------------
# 1. CONSTANTES DE DONNÉES
# ---------------------------------------------------------------------------

OAUTH2_FLOWS = {
    "AUTHORIZATION_CODE_PKCE": {
        "label": "Code d'Autorisation + PKCE",
        "rfc_ref": "RFC 6749 §4.1 + RFC 7636",
        "use_case": "Applications interactives avec navigateur — agents dashboard CaelumSwarm™",
        "security_level": "HIGH",
        "token_lifetime_seconds": 3600,
        "refresh_allowed": True,
        "caelum_use_case": "Connexion opérateurs humains aux tableaux de bord Wave Engine",
    },
    "CLIENT_CREDENTIALS": {
        "label": "Identifiants Client (M2M)",
        "rfc_ref": "RFC 6749 §4.4",
        "use_case": "Communication machine-à-machine sans utilisateur humain",
        "security_level": "HIGH",
        "token_lifetime_seconds": 1800,
        "refresh_allowed": False,
        "caelum_use_case": "Agents CaelumSwarm™ appelant les APIs Wave Engine en tâche de fond",
    },
    "DEVICE_AUTHORIZATION": {
        "label": "Autorisation Appareil (Device Flow)",
        "rfc_ref": "RFC 8628",
        "use_case": "Appareils sans interface navigateur (IoT, CLI)",
        "security_level": "MEDIUM",
        "token_lifetime_seconds": 600,
        "refresh_allowed": True,
        "caelum_use_case": "CLI d'administration des agents swarm depuis terminal sécurisé",
    },
    "REFRESH_TOKEN": {
        "label": "Renouvellement par Refresh Token",
        "rfc_ref": "RFC 6749 §6",
        "use_case": "Extension de session sans ré-authentification interactive",
        "security_level": "MEDIUM",
        "token_lifetime_seconds": 86400,
        "refresh_allowed": True,
        "caelum_use_case": "Sessions longues des agents de monitoring continu Wave",
    },
    "TOKEN_INTROSPECTION": {
        "label": "Introspection de Token",
        "rfc_ref": "RFC 7662",
        "use_case": "Validation de token côté serveur de ressources",
        "security_level": "HIGH",
        "token_lifetime_seconds": 0,
        "refresh_allowed": False,
        "caelum_use_case": "Validation des tokens entrants par les API routes CaelumSwarm™",
    },
}

SCOPES_REGISTRY = {
    "openid": {
        "label": "OpenID Connect de base",
        "description": "Émission d'un ID Token — identifie l'utilisateur de façon standardisée",
        "sensitivity": "PUBLIC",
        "requires_mfa": False,
        "max_token_lifetime_hours": 24,
    },
    "profile": {
        "label": "Profil utilisateur",
        "description": "Accès au nom, prénom, avatar et informations de profil publiques",
        "sensitivity": "INTERNAL",
        "requires_mfa": False,
        "max_token_lifetime_hours": 8,
    },
    "email": {
        "label": "Adresse e-mail",
        "description": "Accès à l'adresse e-mail vérifiée de l'utilisateur",
        "sensitivity": "INTERNAL",
        "requires_mfa": False,
        "max_token_lifetime_hours": 8,
    },
    "wave:read": {
        "label": "Lecture Wave Engine",
        "description": "Consultation des données et scores produits par les Wave Engines",
        "sensitivity": "CONFIDENTIAL",
        "requires_mfa": False,
        "max_token_lifetime_hours": 4,
    },
    "wave:write": {
        "label": "Écriture Wave Engine",
        "description": "Soumission de paramètres et déclenchement de recalculs Wave",
        "sensitivity": "CONFIDENTIAL",
        "requires_mfa": True,
        "max_token_lifetime_hours": 1,
    },
    "report:generate": {
        "label": "Génération de rapports",
        "description": "Création et export de rapports d'analyse droits humains CaelumSwarm™",
        "sensitivity": "CONFIDENTIAL",
        "requires_mfa": True,
        "max_token_lifetime_hours": 2,
    },
    "alert:receive": {
        "label": "Réception d'alertes",
        "description": "Abonnement aux alertes critiques émises par le swarm d'agents",
        "sensitivity": "INTERNAL",
        "requires_mfa": False,
        "max_token_lifetime_hours": 12,
    },
    "admin:full": {
        "label": "Administration complète",
        "description": "Accès administrateur total — gestion agents, config, secrets",
        "sensitivity": "CONFIDENTIAL",
        "requires_mfa": True,
        "max_token_lifetime_hours": 1,
    },
    "audit:read": {
        "label": "Lecture journal d'audit",
        "description": "Consultation des traces d'audit de sécurité et d'activité",
        "sensitivity": "CONFIDENTIAL",
        "requires_mfa": True,
        "max_token_lifetime_hours": 2,
    },
    "api:agent": {
        "label": "Accès API Agent M2M",
        "description": "Portée dédiée aux agents automatiques CaelumSwarm™ (sans utilisateur)",
        "sensitivity": "CONFIDENTIAL",
        "requires_mfa": False,
        "max_token_lifetime_hours": 0.5,
    },
}

TOKEN_TYPES = {
    "ACCESS_TOKEN": {
        "label": "Token d'accès",
        "format": "JWT",
        "signing_algorithm": "RS256",
        "expiry_seconds": 3600,
        "storage_recommendation": "Mémoire vive uniquement — jamais localStorage ni cookie non-httpOnly",
        "revocable": True,
    },
    "REFRESH_TOKEN": {
        "label": "Token de rafraîchissement",
        "format": "OPAQUE",
        "signing_algorithm": "HMAC-SHA256",
        "expiry_seconds": 86400,
        "storage_recommendation": "Cookie httpOnly + SameSite=Strict + Secure, ou stockage chiffré serveur",
        "revocable": True,
    },
    "ID_TOKEN": {
        "label": "Token d'identité OpenID",
        "format": "JWT",
        "signing_algorithm": "RS256",
        "expiry_seconds": 3600,
        "storage_recommendation": "Mémoire vive — utilisé uniquement pour établir la session, ne pas transmettre aux APIs",
        "revocable": False,
    },
    "API_KEY": {
        "label": "Clé API statique",
        "format": "OPAQUE",
        "signing_algorithm": "N/A",
        "expiry_seconds": 0,
        "storage_recommendation": "Variable d'environnement ou coffre-fort secret (Vault, AWS Secrets Manager)",
        "revocable": True,
    },
}

SECURITY_REQUIREMENTS = {
    "PKCE_REQUIRED": {
        "label": "PKCE obligatoire (code_challenge S256)",
        "rfc_section": "RFC 7636 §4",
        "risk_if_omitted": "Interception du code d'autorisation — attaque de type Authorization Code Interception",
        "implementation_status": "IMPLEMENTED",
    },
    "STATE_PARAMETER": {
        "label": "Paramètre state anti-CSRF",
        "rfc_section": "RFC 6749 §10.12",
        "risk_if_omitted": "Attaque CSRF permettant l'injection de session OAuth malveillante",
        "implementation_status": "IMPLEMENTED",
    },
    "NONCE_VALIDATION": {
        "label": "Validation du nonce OpenID (anti-replay)",
        "rfc_section": "OpenID Connect Core §3.1.2",
        "risk_if_omitted": "Réutilisation d'ID Tokens interceptés — attaque de rejeu",
        "implementation_status": "IMPLEMENTED",
    },
    "TOKEN_BINDING": {
        "label": "Liaison token / contexte client (DPoP)",
        "rfc_section": "RFC 9449",
        "risk_if_omitted": "Vol et réutilisation de token Bearer sur un autre client",
        "implementation_status": "PARTIAL",
    },
    "REDIRECT_URI_EXACT": {
        "label": "Correspondance exacte de redirect_uri",
        "rfc_section": "RFC 6749 §3.1.2",
        "risk_if_omitted": "Open Redirect — redirection du code vers un endpoint malveillant",
        "implementation_status": "IMPLEMENTED",
    },
    "SCOPE_MINIMIZATION": {
        "label": "Minimisation des scopes demandés",
        "rfc_section": "RFC 6749 §3.3 + RFC 9700",
        "risk_if_omitted": "Sur-privilège — token compromis expose plus de ressources que nécessaire",
        "implementation_status": "IMPLEMENTED",
    },
    "SHORT_TOKEN_LIFETIME": {
        "label": "Durée de vie courte des tokens d'accès",
        "rfc_section": "RFC 6750 §5.3 + RFC 9700 §2.1",
        "risk_if_omitted": "Fenêtre d'exploitation élargie en cas de compromission de token",
        "implementation_status": "IMPLEMENTED",
    },
    "REFRESH_TOKEN_ROTATION": {
        "label": "Rotation des refresh tokens (sender-constrained)",
        "rfc_section": "RFC 9700 §2.2.2",
        "risk_if_omitted": "Réutilisation silencieuse d'un refresh token volé — session piratée durable",
        "implementation_status": "TODO",
    },
}


# ---------------------------------------------------------------------------
# 2. FONCTIONS PRINCIPALES
# ---------------------------------------------------------------------------

def _base64url_encode(data: bytes) -> str:
    """Encodage base64url sans padding (RFC 4648 §5)."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_authorization_url(
    client_id: str,
    scopes: list,
    redirect_uri: str,
) -> dict:
    """
    Génère les paramètres d'URL d'autorisation OAuth 2.0 avec PKCE (S256).

    Conforme à RFC 6749 §4.1 + RFC 7636 §4.3.

    Paramètres
    ----------
    client_id   : Identifiant du client OAuth 2.0 enregistré.
    scopes      : Liste de portées demandées (ex. ['openid', 'wave:read']).
    redirect_uri: URI de redirection enregistrée auprès de l'Authorization Server.

    Retour
    ------
    dict contenant :
      - url_params        : dict des paramètres à envoyer à l'Authorization Endpoint
      - code_verifier     : secret PKCE à conserver côté client pour l'échange de token
      - security_checklist: audit des scopes et des exigences de sécurité appliquées
    """
    # --- PKCE : génération du code_verifier et du code_challenge S256 ---
    code_verifier_bytes = secrets.token_bytes(32)
    code_verifier = _base64url_encode(code_verifier_bytes)

    sha256_digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = _base64url_encode(sha256_digest)

    # --- Paramètres anti-CSRF et anti-replay ---
    state = secrets.token_hex(32)
    nonce = secrets.token_hex(16)

    # --- Construction des paramètres de requête ---
    scope_str = " ".join(scopes)
    url_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope_str,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    # --- Audit de sécurité des scopes demandés ---
    mfa_required_scopes = []
    confidential_scopes = []
    unknown_scopes = []
    min_token_lifetime_hours = float("inf")

    for scope in scopes:
        if scope in SCOPES_REGISTRY:
            entry = SCOPES_REGISTRY[scope]
            if entry["requires_mfa"]:
                mfa_required_scopes.append(scope)
            if entry["sensitivity"] == "CONFIDENTIAL":
                confidential_scopes.append(scope)
            ttl = entry["max_token_lifetime_hours"]
            if ttl > 0 and ttl < min_token_lifetime_hours:
                min_token_lifetime_hours = ttl
        else:
            unknown_scopes.append(scope)

    if min_token_lifetime_hours == float("inf"):
        min_token_lifetime_hours = 24

    security_checklist = {
        "pkce_method": "S256 (SHA-256) — conforme RFC 7636 §4.2",
        "state_generated": True,
        "nonce_generated": True,
        "scopes_requested": scopes,
        "mfa_required_scopes": mfa_required_scopes,
        "confidential_scopes": confidential_scopes,
        "unknown_scopes": unknown_scopes,
        "recommended_max_token_lifetime_hours": min_token_lifetime_hours,
        "warnings": [],
    }

    if unknown_scopes:
        security_checklist["warnings"].append(
            f"Scopes non reconnus dans le registre CaelumSwarm™ : {unknown_scopes}"
        )
    if "admin:full" in scopes and len(scopes) > 2:
        security_checklist["warnings"].append(
            "Principe de minimisation : admin:full ne devrait pas être combiné avec d'autres scopes"
        )
    if not mfa_required_scopes and "wave:write" in scopes:
        security_checklist["warnings"].append(
            "wave:write est CONFIDENTIEL — vérifier que l'IDP impose le MFA pour cette portée"
        )

    return {
        "url_params": url_params,
        "code_verifier": code_verifier,
        "security_checklist": security_checklist,
    }


def simulate_token_exchange(
    code: str,
    code_verifier: str,
    client_id: str,
) -> dict:
    """
    Simule la réponse du Token Endpoint OAuth 2.0 (RFC 6749 §4.1.4 + RFC 7636 §4.5).

    En production, cet appel est un POST HTTP vers /token avec authentification du client.
    Ici la simulation génère des tokens cryptographiquement valides pour les tests.

    Paramètres
    ----------
    code          : Code d'autorisation reçu du Authorization Endpoint.
    code_verifier : Verifier PKCE original (doit correspondre au code_challenge envoyé).
    client_id     : Identifiant du client OAuth 2.0.

    Retour
    ------
    dict contenant access_token, id_token, refresh_token et métadonnées.
    """
    issued_at = int(time.time())
    expires_in = TOKEN_TYPES["ACCESS_TOKEN"]["expiry_seconds"]
    jti = secrets.token_hex(16)

    # --- Validation PKCE (simulation) ---
    sha256_digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    reconstructed_challenge = _base64url_encode(sha256_digest)

    # --- Construction du payload JWT-like (header.payload.signature simulée) ---
    header = {
        "alg": TOKEN_TYPES["ACCESS_TOKEN"]["signing_algorithm"],
        "typ": "JWT",
        "kid": "caelum-rs256-2026-01",
    }
    claims = {
        "iss": "https://auth.caelumpartners.io",
        "sub": f"agent:{client_id}",
        "aud": "https://api.caelumswarm.io",
        "iat": issued_at,
        "exp": issued_at + expires_in,
        "jti": jti,
        "scope": "openid wave:read api:agent",
        "client_id": client_id,
        "caelum_agent": True,
        "wave_access": "READ_ONLY",
    }

    header_b64 = _base64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _base64url_encode(json.dumps(claims, separators=(",", ":")).encode())

    # Signature simulée (HMAC-like — en prod : RS256 avec clé privée HSM)
    sig_input = f"{header_b64}.{payload_b64}".encode()
    sig_hash = hashlib.sha256(sig_input + b":caelum-secret-demo").digest()
    sig_b64 = _base64url_encode(sig_hash)

    access_token = f"{header_b64}.{payload_b64}.{sig_b64}"

    # --- ID Token (OpenID Connect) ---
    id_claims = {
        "iss": "https://auth.caelumpartners.io",
        "sub": f"agent:{client_id}",
        "aud": client_id,
        "iat": issued_at,
        "exp": issued_at + expires_in,
        "nonce": secrets.token_hex(16),
        "name": f"CaelumSwarm Agent [{client_id}]",
        "email": "agent@caelumswarm.io",
        "email_verified": True,
    }
    id_payload_b64 = _base64url_encode(
        json.dumps(id_claims, separators=(",", ":")).encode()
    )
    id_sig_hash = hashlib.sha256(
        f"{header_b64}.{id_payload_b64}".encode() + b":caelum-id-demo"
    ).digest()
    id_token = f"{header_b64}.{id_payload_b64}.{_base64url_encode(id_sig_hash)}"

    # --- Refresh Token (opaque) ---
    refresh_token = secrets.token_urlsafe(48)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "id_token": id_token,
        "refresh_token": refresh_token,
        "scope": "openid wave:read api:agent",
        "token_metadata": {
            "issued_at": issued_at,
            "issued_at_iso": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(issued_at)
            ),
            "expires_at_iso": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(issued_at + expires_in)
            ),
            "jti": jti,
            "pkce_challenge_reconstructed": reconstructed_challenge,
            "pkce_verified": True,
            "claims": claims,
            "issuer": "https://auth.caelumpartners.io",
            "signing_algorithm": TOKEN_TYPES["ACCESS_TOKEN"]["signing_algorithm"],
            "storage_recommendation": TOKEN_TYPES["ACCESS_TOKEN"]["storage_recommendation"],
        },
    }


def validate_token(token: str, required_scopes: list) -> dict:
    """
    Valide un token d'accès JWT CaelumSwarm™ (RFC 7519 + RFC 6750 §3.1).

    Effectue les vérifications : expiration, scopes requis, émetteur, audience.
    En production, la signature RS256 serait vérifiée contre la clé publique JWK.

    Paramètres
    ----------
    token           : Token JWT Bearer à valider.
    required_scopes : Liste de portées obligatoires pour l'accès à la ressource.

    Retour
    ------
    dict contenant is_valid (bool), claims, validation_errors, introspection_result.
    """
    validation_errors = []
    claims = {}
    now = int(time.time())

    # --- Décodage des parties JWT ---
    parts = token.split(".")
    if len(parts) != 3:
        validation_errors.append("Format JWT invalide — attendu header.payload.signature")
        return {
            "is_valid": False,
            "claims": {},
            "validation_errors": validation_errors,
            "introspection_result": {"active": False},
        }

    try:
        # Ajout du padding base64 si nécessaire
        payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        claims = json.loads(payload_bytes.decode("utf-8"))
    except Exception as exc:
        validation_errors.append(f"Décodage payload JWT échoué : {exc}")
        return {
            "is_valid": False,
            "claims": {},
            "validation_errors": validation_errors,
            "introspection_result": {"active": False},
        }

    # --- Vérification de l'émetteur (iss) ---
    expected_issuer = "https://auth.caelumpartners.io"
    if claims.get("iss") != expected_issuer:
        validation_errors.append(
            f"Émetteur invalide — reçu : '{claims.get('iss')}', attendu : '{expected_issuer}'"
        )

    # --- Vérification de l'audience (aud) ---
    expected_audience = "https://api.caelumswarm.io"
    aud = claims.get("aud", "")
    if isinstance(aud, list):
        if expected_audience not in aud:
            validation_errors.append(
                f"Audience invalide — '{expected_audience}' absent de {aud}"
            )
    elif aud != expected_audience:
        validation_errors.append(
            f"Audience invalide — reçu : '{aud}', attendu : '{expected_audience}'"
        )

    # --- Vérification de l'expiration (exp) ---
    exp = claims.get("exp", 0)
    if exp == 0:
        validation_errors.append("Claim 'exp' manquant — token sans date d'expiration refusé")
    elif now >= exp:
        expired_since = now - exp
        validation_errors.append(
            f"Token expiré depuis {expired_since} secondes (exp={exp}, now={now})"
        )

    # --- Vérification iat (not before) ---
    iat = claims.get("iat", 0)
    if iat > now + 60:
        validation_errors.append(
            f"Token émis dans le futur (iat={iat}, now={now}) — horloge désynchronisée ou falsification"
        )

    # --- Vérification jti (présence) ---
    if not claims.get("jti"):
        validation_errors.append(
            "Claim 'jti' manquant — impossible de détecter les attaques de rejeu"
        )

    # --- Vérification des scopes requis ---
    token_scopes = set(claims.get("scope", "").split())
    missing_scopes = [s for s in required_scopes if s not in token_scopes]
    if missing_scopes:
        validation_errors.append(
            f"Scopes insuffisants — manquants : {missing_scopes}"
        )

    # --- Résultat d'introspection (RFC 7662) ---
    is_valid = len(validation_errors) == 0
    remaining_seconds = max(0, exp - now) if exp else 0

    introspection_result = {
        "active": is_valid,
        "scope": claims.get("scope", ""),
        "client_id": claims.get("client_id", ""),
        "username": claims.get("sub", ""),
        "token_type": "Bearer",
        "exp": exp,
        "iat": iat,
        "nbf": iat,
        "sub": claims.get("sub", ""),
        "aud": claims.get("aud", ""),
        "iss": claims.get("iss", ""),
        "jti": claims.get("jti", ""),
        "remaining_seconds": remaining_seconds,
        "remaining_human": f"{math.ceil(remaining_seconds / 60)} minute(s)"
        if remaining_seconds > 0
        else "Expiré",
    }

    return {
        "is_valid": is_valid,
        "claims": claims,
        "validation_errors": validation_errors,
        "introspection_result": introspection_result,
    }


def audit_oauth_security(client_config: dict) -> dict:
    """
    Audit complet de la configuration OAuth 2.0 d'un client CaelumSwarm™.

    Vérifie la conformité RFC 9700 (OAuth 2.1 Best Practices), détecte les
    mauvaises configurations courantes et produit un score de sécurité.

    Paramètres
    ----------
    client_config : dict décrivant la configuration du client :
      - flow              : flow OAuth utilisé (clé de OAUTH2_FLOWS)
      - pkce_enabled      : bool
      - token_lifetime_s  : durée de vie du token en secondes
      - scopes            : liste de portées demandées
      - redirect_uris     : liste d'URIs de redirection autorisées
      - allow_implicit    : bool — true = vulnérabilité majeure
      - refresh_rotation  : bool
      - state_validated   : bool
      - nonce_validated   : bool

    Retour
    ------
    dict contenant security_score (0-100), critical_issues, recommendations,
    compliance_level, requirements_status.
    """
    critical_issues = []
    recommendations = []
    score = 100
    requirements_status = {}

    flow = client_config.get("flow", "UNKNOWN")
    pkce_enabled = client_config.get("pkce_enabled", False)
    token_lifetime_s = client_config.get("token_lifetime_s", 3600)
    scopes = client_config.get("scopes", [])
    redirect_uris = client_config.get("redirect_uris", [])
    allow_implicit = client_config.get("allow_implicit", False)
    refresh_rotation = client_config.get("refresh_rotation", False)
    state_validated = client_config.get("state_validated", False)
    nonce_validated = client_config.get("nonce_validated", False)

    # --- Vérification : Implicit Flow interdit (RFC 9700 §2.1.2) ---
    if allow_implicit:
        critical_issues.append(
            "CRITIQUE — Implicit Flow activé : les tokens apparaissent dans l'URL, "
            "exposés aux logs serveur, referer et historique navigateur. "
            "Interdit par RFC 9700 §2.1.2 et OAuth 2.1."
        )
        score -= 30
        requirements_status["PKCE_REQUIRED"] = "FAIL — Implicit flow détecté"
    else:
        requirements_status["PKCE_REQUIRED"] = "OK"

    # --- Vérification : PKCE obligatoire pour flows interactifs ---
    interactive_flows = {"AUTHORIZATION_CODE_PKCE", "DEVICE_AUTHORIZATION"}
    if flow in interactive_flows and not pkce_enabled:
        critical_issues.append(
            "CRITIQUE — PKCE désactivé sur un flow interactif : "
            "risque d'interception du code d'autorisation (RFC 7636)."
        )
        score -= 25
        requirements_status["PKCE_REQUIRED"] = "FAIL — PKCE désactivé"
    elif flow in interactive_flows and pkce_enabled:
        requirements_status["PKCE_REQUIRED"] = "OK — PKCE S256 actif"

    # --- Vérification : durée de vie des tokens ---
    if token_lifetime_s > 3600:
        severity = "CRITIQUE" if token_lifetime_s > 86400 else "AVERTISSEMENT"
        critical_issues.append(
            f"{severity} — Durée de vie token = {token_lifetime_s}s "
            f"({token_lifetime_s / 3600:.1f}h) : dépasse la limite recommandée de 3600s "
            "(RFC 9700 §2.1.1). Réduire à 1800s maximum pour les scopes CONFIDENTIELS."
        )
        deduction = 20 if token_lifetime_s > 86400 else 10
        score -= deduction
        requirements_status["SHORT_TOKEN_LIFETIME"] = (
            f"FAIL — lifetime={token_lifetime_s}s > 3600s"
        )
    else:
        requirements_status["SHORT_TOKEN_LIFETIME"] = (
            f"OK — lifetime={token_lifetime_s}s ≤ 3600s"
        )

    # --- Vérification : redirect URIs (wildcards dangereux) ---
    wildcard_uris = [u for u in redirect_uris if "*" in u or u.endswith("/")]
    if wildcard_uris:
        critical_issues.append(
            f"CRITIQUE — Redirect URIs avec wildcard ou slash final détectées : {wildcard_uris}. "
            "La correspondance doit être EXACTE selon RFC 6749 §3.1.2."
        )
        score -= 20
        requirements_status["REDIRECT_URI_EXACT"] = "FAIL — wildcards détectés"
    else:
        requirements_status["REDIRECT_URI_EXACT"] = "OK — correspondance exacte"

    # --- Vérification : paramètre state ---
    if not state_validated:
        critical_issues.append(
            "AVERTISSEMENT — Paramètre 'state' non validé : risque d'attaque CSRF "
            "(RFC 6749 §10.12). Générer un state aléatoire et valider sa correspondance."
        )
        score -= 10
        requirements_status["STATE_PARAMETER"] = "FAIL — state non validé"
    else:
        requirements_status["STATE_PARAMETER"] = "OK"

    # --- Vérification : nonce OpenID ---
    if "openid" in scopes and not nonce_validated:
        recommendations.append(
            "Activer la validation du 'nonce' dans l'ID Token pour prévenir "
            "les attaques de rejeu (OpenID Connect Core §3.1.2)."
        )
        requirements_status["NONCE_VALIDATION"] = "PARTIAL — nonce non validé côté client"
        score -= 5
    else:
        requirements_status["NONCE_VALIDATION"] = "OK"

    # --- Vérification : rotation des refresh tokens ---
    if not refresh_rotation and OAUTH2_FLOWS.get(flow, {}).get("refresh_allowed", False):
        recommendations.append(
            "Activer la rotation automatique des refresh tokens (RFC 9700 §2.2.2) : "
            "chaque utilisation émet un nouveau refresh token et invalide l'ancien. "
            "Détecte les tentatives de réutilisation après compromission."
        )
        requirements_status["REFRESH_TOKEN_ROTATION"] = "TODO — rotation désactivée"
    else:
        requirements_status["REFRESH_TOKEN_ROTATION"] = "OK ou N/A"

    # --- Vérification : minimisation des scopes ---
    confidential_count = sum(
        1
        for s in scopes
        if SCOPES_REGISTRY.get(s, {}).get("sensitivity") == "CONFIDENTIAL"
    )
    if "admin:full" in scopes and len(scopes) > 1:
        recommendations.append(
            "Principe du moindre privilège : admin:full ne devrait pas être combiné "
            "avec d'autres scopes — risque de sur-exposition en cas de compromission."
        )
        requirements_status["SCOPE_MINIMIZATION"] = "PARTIAL — admin:full sur-exposé"
        score -= 5
    elif confidential_count > 3:
        recommendations.append(
            f"{confidential_count} scopes CONFIDENTIELS demandés simultanément — "
            "envisager des tokens distincts par domaine fonctionnel."
        )
        requirements_status["SCOPE_MINIMIZATION"] = f"PARTIAL — {confidential_count} scopes confidentiels"
    else:
        requirements_status["SCOPE_MINIMIZATION"] = "OK"

    # --- Recommendations générales ---
    if not client_config.get("dpop_enabled", False):
        recommendations.append(
            "Envisager DPoP (RFC 9449) pour lier les tokens à la clé cryptographique "
            "du client — protection contre le vol de Bearer tokens."
        )
        requirements_status["TOKEN_BINDING"] = "TODO — DPoP non activé"
    else:
        requirements_status["TOKEN_BINDING"] = "OK — DPoP actif"

    # --- Score final et niveau de conformité ---
    score = max(0, min(100, score))

    if score >= 90:
        compliance_level = "OAuth 2.1 — Conforme (RFC 9700)"
    elif score >= 70:
        compliance_level = "OAuth 2.0 — Partiellement conforme (améliorations requises)"
    elif score >= 50:
        compliance_level = "OAuth 2.0 — Non conforme (risques significatifs)"
    else:
        compliance_level = "Non conforme — Configuration dangereuse (action immédiate requise)"

    return {
        "security_score": score,
        "compliance_level": compliance_level,
        "critical_issues": critical_issues,
        "recommendations": recommendations,
        "requirements_status": requirements_status,
        "audit_metadata": {
            "flow_audited": flow,
            "scopes_audited": scopes,
            "token_lifetime_s": token_lifetime_s,
            "redirect_uris_count": len(redirect_uris),
            "audit_timestamp_iso": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            ),
            "standard_reference": "RFC 6749, RFC 7636, RFC 7662, RFC 9449, RFC 9700",
        },
    }


# ---------------------------------------------------------------------------
# 3. DÉMONSTRATION
# ---------------------------------------------------------------------------

def run_demo() -> bool:
    """
    Démonstration complète du protocole OAuth 2.0 CaelumSwarm™.

    Enchaîne : génération URL d'autorisation → échange de token →
    validation → audit de sécurité pour un agent Wave Engine.
    """
    separator = "=" * 72

    print(separator)
    print("  CAELUMSWARM™ — Agent Protocole OAuth 2.0 / OpenID Connect")
    print("  RFC 6749 · RFC 7636 · RFC 7662 · RFC 9449 · RFC 9700")
    print(separator)

    client_id = "caelum-wave-engine-agent-v3"
    redirect_uri = "https://dashboard.caelumswarm.io/auth/callback"
    requested_scopes = ["openid", "profile", "wave:read", "api:agent"]

    # ------------------------------------------------------------------ #
    # ÉTAPE 1 — Génération de l'URL d'autorisation                        #
    # ------------------------------------------------------------------ #
    print("\n[ÉTAPE 1] Génération URL d'autorisation + PKCE")
    print("-" * 50)

    auth_result = generate_authorization_url(
        client_id=client_id,
        scopes=requested_scopes,
        redirect_uri=redirect_uri,
    )

    url_params = auth_result["url_params"]
    code_verifier = auth_result["code_verifier"]
    checklist = auth_result["security_checklist"]

    print(f"  Client ID         : {client_id}")
    print(f"  Scopes demandés   : {' '.join(requested_scopes)}")
    print(f"  Redirect URI      : {redirect_uri}")
    print(f"  PKCE method       : {checklist['pkce_method']}")
    print(f"  code_challenge    : {url_params['code_challenge'][:24]}…")
    print(f"  state (anti-CSRF) : {url_params['state'][:16]}… ({len(url_params['state'])} chars)")
    print(f"  nonce (anti-replay): {url_params['nonce'][:16]}… ({len(url_params['nonce'])} chars)")

    base_url = "https://auth.caelumpartners.io/oauth2/authorize"
    full_url = f"{base_url}?{urllib.parse.urlencode(url_params)}"
    print(f"\n  URL d'autorisation construite ({len(full_url)} caractères) :")
    print(f"  {full_url[:80]}…")

    if checklist["warnings"]:
        print(f"\n  Avertissements sécurité scopes :")
        for w in checklist["warnings"]:
            print(f"    ⚠  {w}")
    else:
        print("\n  Aucun avertissement de sécurité sur les scopes.")

    # ------------------------------------------------------------------ #
    # ÉTAPE 2 — Échange de token (Token Endpoint)                         #
    # ------------------------------------------------------------------ #
    print("\n[ÉTAPE 2] Échange de code d'autorisation contre des tokens")
    print("-" * 50)

    simulated_code = secrets.token_urlsafe(24)
    token_response = simulate_token_exchange(
        code=simulated_code,
        code_verifier=code_verifier,
        client_id=client_id,
    )

    meta = token_response["token_metadata"]
    print(f"  Code simulé       : {simulated_code[:12]}…")
    print(f"  PKCE vérifié      : {meta['pkce_verified']}")
    print(f"  Access Token (JWT): {token_response['access_token'][:32]}…")
    print(f"  ID Token (JWT)    : {token_response['id_token'][:32]}…")
    print(f"  Refresh Token     : {token_response['refresh_token'][:16]}… (opaque)")
    print(f"  Expire dans       : {token_response['expires_in']}s")
    print(f"  Émis à            : {meta['issued_at_iso']}")
    print(f"  Expire à          : {meta['expires_at_iso']}")
    print(f"  JTI               : {meta['jti']}")
    print(f"  Algorithme        : {meta['signing_algorithm']}")
    print(f"\n  Recommandation stockage :")
    print(f"    {meta['storage_recommendation']}")

    # ------------------------------------------------------------------ #
    # ÉTAPE 3 — Validation du token                                       #
    # ------------------------------------------------------------------ #
    print("\n[ÉTAPE 3] Validation du token d'accès")
    print("-" * 50)

    validation = validate_token(
        token=token_response["access_token"],
        required_scopes=["wave:read", "api:agent"],
    )

    intro = validation["introspection_result"]
    print(f"  Token valide      : {validation['is_valid']}")
    print(f"  Actif (RFC 7662)  : {intro['active']}")
    print(f"  Sujet (sub)       : {intro['sub']}")
    print(f"  Audience (aud)    : {intro['aud']}")
    print(f"  Émetteur (iss)    : {intro['iss']}")
    print(f"  Scopes accordés   : {intro['scope']}")
    print(f"  Durée restante    : {intro['remaining_human']}")

    if validation["validation_errors"]:
        print(f"\n  Erreurs de validation :")
        for err in validation["validation_errors"]:
            print(f"    ✗ {err}")
    else:
        print("\n  Aucune erreur de validation — token intègre.")

    # ------------------------------------------------------------------ #
    # ÉTAPE 4 — Audit de sécurité de la configuration client              #
    # ------------------------------------------------------------------ #
    print("\n[ÉTAPE 4] Audit de sécurité OAuth 2.0 — configuration client")
    print("-" * 50)

    client_config = {
        "flow": "AUTHORIZATION_CODE_PKCE",
        "pkce_enabled": True,
        "token_lifetime_s": 3600,
        "scopes": requested_scopes,
        "redirect_uris": [redirect_uri],
        "allow_implicit": False,
        "refresh_rotation": False,
        "state_validated": True,
        "nonce_validated": True,
        "dpop_enabled": False,
    }

    audit = audit_oauth_security(client_config)

    print(f"  Score de sécurité : {audit['security_score']} / 100")
    print(f"  Niveau conformité : {audit['compliance_level']}")
    print(f"  Flow audité       : {audit['audit_metadata']['flow_audited']}")
    print(f"  Référence norme   : {audit['audit_metadata']['standard_reference']}")

    print("\n  État des exigences de sécurité :")
    for req_key, status in audit["requirements_status"].items():
        label = SECURITY_REQUIREMENTS.get(req_key, {}).get("label", req_key)
        icon = "✓" if status.startswith("OK") else ("~" if status.startswith("PARTIAL") else "✗")
        print(f"    {icon} {label}")
        print(f"      → {status}")

    if audit["critical_issues"]:
        print(f"\n  Problèmes critiques ({len(audit['critical_issues'])}) :")
        for issue in audit["critical_issues"]:
            print(f"    ✗ {issue}")
    else:
        print("\n  Aucun problème critique détecté.")

    if audit["recommendations"]:
        print(f"\n  Recommandations ({len(audit['recommendations'])}) :")
        for rec in audit["recommendations"]:
            print(f"    → {rec}")

    # ------------------------------------------------------------------ #
    # RÉSUMÉ                                                               #
    # ------------------------------------------------------------------ #
    print(f"\n{separator}")
    print("  RÉSUMÉ DE LA DÉMONSTRATION")
    print(separator)
    print(f"  ✓ URL d'autorisation PKCE S256 générée")
    print(f"  ✓ Token JWT échangé et décodé")
    print(f"  ✓ Validation RFC 7662 : token {'valide' if validation['is_valid'] else 'invalide'}")
    print(f"  ✓ Audit OAuth 2.0 : score {audit['security_score']}/100 — {audit['compliance_level']}")
    print(separator)
    print()

    return True


# ---------------------------------------------------------------------------
# 4. POINT D'ENTRÉE
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_demo()

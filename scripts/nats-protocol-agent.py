"""
Agent Protocole NATS — messagerie ultra-rapide pub/sub, request/reply et JetStream persistant
pour CaelumSwarm™. Orchestration événementielle des agents, fanout d'alertes et streaming de
données Wave en temps réel.

NATS constitue le système nerveux central de CaelumSwarm™ : chaque résultat d'analyse Wave
déclenche une cascade d'événements coordonnés entre agents spécialisés — alertes critiques,
notifications clients, publication presse et journalisation d'audit — le tout en dessous de
la milliseconde pour les flux mémoire.
"""

import hashlib
import json
import math
import random
import uuid
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constantes de données
# ---------------------------------------------------------------------------

NATS_SUBJECTS: dict = {
    "caelum.wave.new": {
        "label": "Déclenchement nouvelle Wave d'analyse",
        "pattern": "exact",
        "qos": "AT_LEAST_ONCE",
        "max_payload_kb": 64,
        "subscribers": ["wave_orchestrator", "audit_agent", "dashboard_streamer"],
        "retention": "limits",
    },
    "caelum.wave.result": {
        "label": "Résultat complet d'une Wave publiée",
        "pattern": "exact",
        "qos": "EXACTLY_ONCE",
        "max_payload_kb": 512,
        "subscribers": [
            "alert_engine",
            "press_agent",
            "client_notifier",
            "report_builder",
            "audit_agent",
        ],
        "retention": "limits",
    },
    "caelum.alert.critical": {
        "label": "Alerte critique droits humains (score ≥ 60)",
        "pattern": "exact",
        "qos": "EXACTLY_ONCE",
        "max_payload_kb": 32,
        "subscribers": [
            "legal_team_agent",
            "press_agent",
            "client_notifier",
            "compliance_monitor",
            "audit_agent",
        ],
        "retention": "workqueue",
    },
    "caelum.alert.high": {
        "label": "Alerte élevée droits humains (score 40–59)",
        "pattern": "exact",
        "qos": "AT_LEAST_ONCE",
        "max_payload_kb": 32,
        "subscribers": ["legal_team_agent", "client_notifier", "audit_agent"],
        "retention": "workqueue",
    },
    "caelum.report.request": {
        "label": "Demande de génération de rapport client",
        "pattern": "exact",
        "qos": "AT_LEAST_ONCE",
        "max_payload_kb": 16,
        "subscribers": ["report_builder"],
        "retention": "interest",
    },
    "caelum.report.ready": {
        "label": "Rapport client prêt à l'envoi",
        "pattern": "exact",
        "qos": "AT_LEAST_ONCE",
        "max_payload_kb": 8,
        "subscribers": ["client_notifier", "audit_agent"],
        "retention": "interest",
    },
    "caelum.legal.update": {
        "label": "Mise à jour cadre légal ou jurisprudence",
        "pattern": "wildcard",
        "qos": "AT_LEAST_ONCE",
        "max_payload_kb": 128,
        "subscribers": ["compliance_monitor", "report_builder", "audit_agent"],
        "retention": "limits",
    },
    "caelum.agent.heartbeat": {
        "label": "Signal de vie des agents CaelumSwarm™",
        "pattern": "wildcard",
        "qos": "AT_MOST_ONCE",
        "max_payload_kb": 4,
        "subscribers": ["orchestrator_supervisor"],
        "retention": "none",
    },
    "caelum.compliance.violation": {
        "label": "Violation de conformité détectée par un agent",
        "pattern": "exact",
        "qos": "EXACTLY_ONCE",
        "max_payload_kb": 64,
        "subscribers": [
            "legal_team_agent",
            "compliance_monitor",
            "client_notifier",
            "audit_agent",
        ],
        "retention": "workqueue",
    },
    "caelum.press.publish": {
        "label": "Déclenchement publication communiqué de presse",
        "pattern": "exact",
        "qos": "EXACTLY_ONCE",
        "max_payload_kb": 256,
        "subscribers": ["press_agent", "audit_agent"],
        "retention": "interest",
    },
    "caelum.client.notify": {
        "label": "Notification directe client (email / webhook)",
        "pattern": "wildcard",
        "qos": "AT_LEAST_ONCE",
        "max_payload_kb": 32,
        "subscribers": ["client_notifier", "audit_agent"],
        "retention": "limits",
    },
    "caelum.audit.log": {
        "label": "Journal d'audit immuable de toutes les actions",
        "pattern": "exact",
        "qos": "EXACTLY_ONCE",
        "max_payload_kb": 16,
        "subscribers": ["audit_agent"],
        "retention": "limits",
    },
}

JETSTREAM_STREAMS: dict = {
    "WAVE_EVENTS": {
        "subjects": ["caelum.wave.new", "caelum.wave.result"],
        "retention_policy": "limits",
        "max_age_hours": 720,
        "max_bytes_MB": 2048,
        "replicas": 3,
        "storage": "file",
        "consumer_groups": [
            "cg_wave_orchestrators",
            "cg_report_builders",
            "cg_dashboard_streamers",
        ],
    },
    "ALERTS_PERSISTENT": {
        "subjects": [
            "caelum.alert.critical",
            "caelum.alert.high",
            "caelum.compliance.violation",
        ],
        "retention_policy": "workqueue",
        "max_age_hours": 2160,
        "max_bytes_MB": 512,
        "replicas": 3,
        "storage": "file",
        "consumer_groups": [
            "cg_legal_processors",
            "cg_compliance_monitors",
            "cg_client_notifiers",
        ],
    },
    "AUDIT_TRAIL": {
        "subjects": ["caelum.audit.log"],
        "retention_policy": "limits",
        "max_age_hours": 87600,
        "max_bytes_MB": 10240,
        "replicas": 3,
        "storage": "file",
        "consumer_groups": ["cg_audit_readers"],
    },
    "CLIENT_NOTIFICATIONS": {
        "subjects": ["caelum.client.notify", "caelum.report.ready"],
        "retention_policy": "interest",
        "max_age_hours": 168,
        "max_bytes_MB": 256,
        "replicas": 2,
        "storage": "memory",
        "consumer_groups": ["cg_client_notifiers", "cg_webhook_dispatchers"],
    },
}

MESSAGING_PATTERNS: dict = {
    "FANOUT_BROADCAST": {
        "label": "Diffusion éventail — un message, N consommateurs",
        "nats_feature_used": "Core NATS pub/sub avec sujets hiérarchiques",
        "use_case_caelum": "Diffusion résultat Wave vers tous les agents abonnés simultanément",
        "latency_target_ms": 0.5,
        "throughput_msg_per_sec": 50_000,
    },
    "REQUEST_REPLY": {
        "label": "Requête/Réponse synchrone via inbox éphémère",
        "nats_feature_used": "Core NATS reply-to avec _INBOX dynamique",
        "use_case_caelum": "Requête de statut agent en temps réel depuis l'orchestrateur",
        "latency_target_ms": 1.2,
        "throughput_msg_per_sec": 20_000,
    },
    "WORK_QUEUE": {
        "label": "File de travail distribuée — chaque message traité une seule fois",
        "nats_feature_used": "JetStream WorkQueuePolicy avec consumer groups",
        "use_case_caelum": "Distribution d'alertes critiques entre agents légaux disponibles",
        "latency_target_ms": 5.0,
        "throughput_msg_per_sec": 10_000,
    },
    "EVENT_SOURCING": {
        "label": "Sourcing d'événements — journal immuable rejouable",
        "nats_feature_used": "JetStream LimitsPolicy avec replay depuis séquence",
        "use_case_caelum": "Reconstruction de l'historique complet d'analyse Wave pour audit",
        "latency_target_ms": 10.0,
        "throughput_msg_per_sec": 5_000,
    },
    "SAGA_ORCHESTRATION": {
        "label": "Orchestration saga — workflow distribué avec compensation",
        "nats_feature_used": "JetStream + subjects de saga avec état partagé",
        "use_case_caelum": "Workflow Wave → Alerte → Rapport → Notification avec rollback",
        "latency_target_ms": 50.0,
        "throughput_msg_per_sec": 500,
    },
}

NATS_SECURITY: dict = {
    "AUTH_TOKEN": {
        "label": "Jeton d'authentification statique",
        "strength": 4,
        "caelum_use": "Environnements de développement et tests internes",
        "setup_complexity": "Très faible — variable d'environnement unique",
    },
    "NKEYS": {
        "label": "Clés NKeys — cryptographie Ed25519 native NATS",
        "strength": 8,
        "caelum_use": "Authentification inter-agents CaelumSwarm™ en production",
        "setup_complexity": "Moyenne — génération de paires de clés par agent",
    },
    "JWT_CREDENTIALS": {
        "label": "Jetons JWT signés par opérateur NATS",
        "strength": 9,
        "caelum_use": "Agents clients externes et intégrations partenaires",
        "setup_complexity": "Élevée — infrastructure PKI avec opérateur/account/user",
    },
    "TLS_CLIENT_CERTS": {
        "label": "Certificats TLS mutuels (mTLS)",
        "strength": 9,
        "caelum_use": "Canaux de transport chiffrés pour données Wave sensibles",
        "setup_complexity": "Élevée — AC interne et rotation automatique des certificats",
    },
    "OPERATOR_MODEL": {
        "label": "Modèle opérateur/compte/utilisateur décentralisé",
        "strength": 10,
        "caelum_use": "Isolation multi-tenant complète pour clients enterprise",
        "setup_complexity": "Très élevée — hiérarchie JWT à 3 niveaux avec délégation",
    },
}


# ---------------------------------------------------------------------------
# Fonctions principales
# ---------------------------------------------------------------------------


def publish_message(
    subject: str,
    payload: dict,
    headers: dict = None,
) -> dict:
    """
    Simule une publication NATS sur un sujet donné.

    Calcule la taille du payload, détermine la garantie de livraison selon la
    configuration du sujet, estime le fanout vers les abonnés enregistrés et
    retourne les métadonnées complètes du message publié.

    Args:
        subject:  Sujet NATS cible (ex. "caelum.wave.result").
        payload:  Dictionnaire Python sérialisé en JSON comme corps du message.
        headers:  En-têtes NATS optionnels (clés/valeurs libres).

    Returns:
        Dictionnaire contenant les métadonnées de publication.
    """
    if headers is None:
        headers = {}

    payload_json = json.dumps(payload, ensure_ascii=False)
    payload_bytes = len(payload_json.encode("utf-8"))
    message_id = str(uuid.uuid4())

    subject_config = NATS_SUBJECTS.get(subject, {})
    qos = subject_config.get("qos", "AT_MOST_ONCE")
    subscribers = subject_config.get("subscribers", [])
    max_payload_kb = subject_config.get("max_payload_kb", 64)
    retention = subject_config.get("retention", "none")

    acknowledgment_required = qos in ("AT_LEAST_ONCE", "EXACTLY_ONCE")
    delivery_guarantee = {
        "AT_MOST_ONCE": "Feu-et-oubli — zéro overhead, perte possible",
        "AT_LEAST_ONCE": "Au moins une livraison — ack requis, duplicats possibles",
        "EXACTLY_ONCE": "Exactement une fois — ack + déduplication JetStream",
    }.get(qos, "Indéfini")

    payload_ok = payload_bytes <= max_payload_kb * 1024
    fanout_count = len(subscribers)

    checksum = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()[:16]

    return {
        "message_id": message_id,
        "subject": subject,
        "subject_label": subject_config.get("label", "Sujet inconnu"),
        "payload_bytes": payload_bytes,
        "payload_kb": round(payload_bytes / 1024, 3),
        "max_payload_kb": max_payload_kb,
        "payload_within_limit": payload_ok,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "qos": qos,
        "delivery_guarantee": delivery_guarantee,
        "acknowledgment_required": acknowledgment_required,
        "retention_policy": retention,
        "headers_attached": dict(headers),
        "estimated_fanout_count": fanout_count,
        "subscriber_list": subscribers,
        "checksum_sha256_prefix": checksum,
        "jetstream_persisted": retention in ("limits", "workqueue", "interest"),
        "status": "PUBLIÉ" if payload_ok else "REJETÉ — payload dépasse la limite",
    }


def create_jetstream_consumer(
    stream: str,
    consumer_name: str,
    filter_subject: str,
    delivery_policy: str,
) -> dict:
    """
    Crée la configuration d'un consommateur JetStream durable.

    Génère une configuration complète incluant la politique d'acquittement,
    la stratégie de backoff exponentiel, et les paramètres de débit attendu
    selon le stream cible.

    Args:
        stream:           Nom du stream JetStream (ex. "ALERTS_PERSISTENT").
        consumer_name:    Nom durable du consommateur.
        filter_subject:   Filtre de sujet NATS (ex. "caelum.alert.critical").
        delivery_policy:  Politique de livraison ("all", "last", "new",
                          "by_start_sequence", "by_start_time").

    Returns:
        Dictionnaire complet de configuration du consommateur JetStream.
    """
    stream_config = JETSTREAM_STREAMS.get(stream, {})

    delivery_policy_label = {
        "all": "Tous les messages depuis le début du stream",
        "last": "Dernier message uniquement (rattrapage)",
        "new": "Uniquement les nouveaux messages",
        "by_start_sequence": "Depuis un numéro de séquence spécifique",
        "by_start_time": "Depuis un instant précis",
    }.get(delivery_policy, "Politique inconnue")

    replicas = stream_config.get("replicas", 1)
    storage = stream_config.get("storage", "file")

    ack_policy = "explicit"
    max_deliver = 5 if stream_config.get("retention_policy") == "workqueue" else 3
    ack_wait_seconds = 30

    backoff_strategy = [
        round(ack_wait_seconds * (1.5**i), 1) for i in range(max_deliver)
    ]

    base_throughput = {
        "WAVE_EVENTS": 1_000,
        "ALERTS_PERSISTENT": 200,
        "AUDIT_TRAIL": 5_000,
        "CLIENT_NOTIFICATIONS": 500,
    }.get(stream, 100)

    consumer_groups = stream_config.get("consumer_groups", [])
    in_group = any(consumer_name.startswith(cg.replace("cg_", "")) for cg in consumer_groups)

    return {
        "consumer_config": {
            "stream_name": stream,
            "durable_name": consumer_name,
            "filter_subject": filter_subject,
            "delivery_policy": delivery_policy,
            "delivery_policy_label": delivery_policy_label,
            "ack_policy": ack_policy,
            "ack_wait_seconds": ack_wait_seconds,
            "max_deliver": max_deliver,
            "replay_policy": "instant",
            "flow_control": True,
            "idle_heartbeat_seconds": 5,
            "max_ack_pending": 1000,
            "storage": storage,
            "replicas": replicas,
        },
        "durable_name": consumer_name,
        "ack_policy": f"{ack_policy} — acquittement explicite obligatoire",
        "max_deliver": max_deliver,
        "ack_wait_seconds": ack_wait_seconds,
        "backoff_strategy": backoff_strategy,
        "backoff_strategy_label": "Exponentiel × 1.5 — évite la tempête de réessais",
        "expected_throughput_msg_per_sec": base_throughput,
        "consumer_groups_available": consumer_groups,
        "consumer_in_known_group": in_group,
        "dead_letter_subject": f"caelum.dlq.{stream.lower()}.{consumer_name}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "CONSOMMATEUR CRÉÉ",
    }


def simulate_wave_event_flow(
    wave: int,
    domains: list,
    critical_count: int,
) -> dict:
    """
    Simule le flux d'événements complet déclenché par la completion d'une Wave.

    Modélise chaque saut du message à travers le graphe d'agents CaelumSwarm™
    depuis la publication du résultat Wave jusqu'aux notifications finales,
    en calculant les latences réalistes pour chaque étape.

    Args:
        wave:           Numéro de la Wave analysée.
        domains:        Liste des domaines analysés (ex. ["conflict_minerals"]).
        critical_count: Nombre d'entités classées critique dans cette Wave.

    Returns:
        Dictionnaire détaillant la chaîne d'événements, les fanouts et les
        latences totales.
    """
    random.seed(wave + len(domains) + critical_count)

    has_critical = critical_count > 0
    has_high = critical_count < 4
    press_triggered = critical_count >= 2
    audit_logged = True

    event_chain = []

    # Étape 1 — Publication résultat Wave
    wave_latency = round(random.uniform(0.3, 0.8), 2)
    wave_subscribers = NATS_SUBJECTS["caelum.wave.result"]["subscribers"]
    event_chain.append({
        "etape": 1,
        "subject": "caelum.wave.result",
        "label": "Résultat Wave publié",
        "subscribers": wave_subscribers,
        "latency_ms": wave_latency,
        "fanout": len(wave_subscribers),
        "notes": f"Wave {wave} — {len(domains)} domaine(s) : {', '.join(domains)}",
    })

    # Étape 2 — Alertes critiques (si applicable)
    if has_critical:
        alert_latency = round(wave_latency + random.uniform(0.5, 1.5), 2)
        critical_subs = NATS_SUBJECTS["caelum.alert.critical"]["subscribers"]
        event_chain.append({
            "etape": 2,
            "subject": "caelum.alert.critical",
            "label": f"Alerte critique — {critical_count} entité(s)",
            "subscribers": critical_subs,
            "latency_ms": alert_latency,
            "fanout": len(critical_subs),
            "notes": f"Score ≥ 60 pour {critical_count} entité(s) — traitement prioritaire",
        })

    # Étape 3 — Alertes élevées
    if has_high:
        high_count = 2
        high_latency = round(wave_latency + random.uniform(0.8, 2.0), 2)
        high_subs = NATS_SUBJECTS["caelum.alert.high"]["subscribers"]
        event_chain.append({
            "etape": 3 if has_critical else 2,
            "subject": "caelum.alert.high",
            "label": f"Alerte élevée — {high_count} entité(s)",
            "subscribers": high_subs,
            "latency_ms": high_latency,
            "fanout": len(high_subs),
            "notes": "Score 40–59 — traitement standard SLA 4h",
        })

    # Étape 4 — Demande de rapport
    report_latency = round(wave_latency + random.uniform(2.0, 5.0), 2)
    report_subs = NATS_SUBJECTS["caelum.report.request"]["subscribers"]
    event_chain.append({
        "etape": len(event_chain) + 1,
        "subject": "caelum.report.request",
        "label": "Génération rapport client déclenchée",
        "subscribers": report_subs,
        "latency_ms": report_latency,
        "fanout": len(report_subs),
        "notes": f"Rapport Wave {wave} pour {len(domains)} domaine(s)",
    })

    # Étape 5 — Publication presse (si critique suffisant)
    if press_triggered:
        press_latency = round(wave_latency + random.uniform(5.0, 15.0), 2)
        press_subs = NATS_SUBJECTS["caelum.press.publish"]["subscribers"]
        event_chain.append({
            "etape": len(event_chain) + 1,
            "subject": "caelum.press.publish",
            "label": "Communiqué de presse déclenché",
            "subscribers": press_subs,
            "latency_ms": press_latency,
            "fanout": len(press_subs),
            "notes": f"{critical_count} alertes critiques — seuil presse atteint",
        })

    # Étape 6 — Notification client
    client_latency = round(wave_latency + random.uniform(10.0, 30.0), 2)
    client_subs = NATS_SUBJECTS["caelum.client.notify"]["subscribers"]
    event_chain.append({
        "etape": len(event_chain) + 1,
        "subject": "caelum.client.notify",
        "label": "Notification client envoyée",
        "subscribers": client_subs,
        "latency_ms": client_latency,
        "fanout": len(client_subs),
        "notes": "Email + webhook selon préférences client",
    })

    # Étape 7 — Audit log
    audit_latency = round(wave_latency + random.uniform(0.1, 0.3), 2)
    audit_subs = NATS_SUBJECTS["caelum.audit.log"]["subscribers"]
    event_chain.append({
        "etape": len(event_chain) + 1,
        "subject": "caelum.audit.log",
        "label": "Journal d'audit enregistré",
        "subscribers": audit_subs,
        "latency_ms": audit_latency,
        "fanout": len(audit_subs),
        "notes": "EXACTLY_ONCE — persisted 10 ans (AUDIT_TRAIL stream)",
    })

    total_notifications = sum(hop["fanout"] for hop in event_chain)
    alert_fanout = sum(
        hop["fanout"]
        for hop in event_chain
        if "alert" in hop["subject"]
    )
    total_latency = max(hop["latency_ms"] for hop in event_chain)

    return {
        "wave": wave,
        "domains_analysed": domains,
        "critical_entities": critical_count,
        "event_chain": event_chain,
        "total_hops": len(event_chain),
        "total_notifications_sent": total_notifications,
        "alert_fanout_count": alert_fanout,
        "press_triggered": press_triggered,
        "audit_logged": audit_logged,
        "total_latency_ms": round(total_latency, 2),
        "latency_category": (
            "ultra-faible (<5ms)" if total_latency < 5
            else "faible (5–50ms)" if total_latency < 50
            else "normale (50–500ms)"
        ),
        "simulated_at": datetime.now(timezone.utc).isoformat(),
    }


def design_agent_choreography(
    agents: list,
    trigger: str,
) -> dict:
    """
    Conçoit la chorégraphie événementielle d'un workflow multi-agents.

    Mappe les souscriptions et publications de chaque agent pour former un
    graphe de dépendances événementielles, génère un diagramme de séquence
    textuel et identifie les points de défaillance potentiels.

    Args:
        agents:  Liste des agents participant au workflow.
        trigger: Événement déclencheur initial (sujet NATS).

    Returns:
        Dictionnaire complet de la chorégraphie avec carte, diagramme,
        latence estimée et configuration dead-letter.
    """
    subject_to_subscribers: dict = {
        s: cfg["subscribers"] for s, cfg in NATS_SUBJECTS.items()
    }

    agent_subs_map: dict = {}
    for agent in agents:
        subscribes_to = [
            s for s, subs in subject_to_subscribers.items() if agent in subs
        ]
        publishes_to = []
        if "wave_orchestrator" in agent:
            publishes_to = ["caelum.wave.new", "caelum.wave.result"]
        elif "alert_engine" in agent:
            publishes_to = ["caelum.alert.critical", "caelum.alert.high"]
        elif "press_agent" in agent:
            publishes_to = ["caelum.press.publish"]
        elif "report_builder" in agent:
            publishes_to = ["caelum.report.request", "caelum.report.ready"]
        elif "client_notifier" in agent:
            publishes_to = ["caelum.client.notify"]
        elif "legal_team_agent" in agent:
            publishes_to = ["caelum.legal.update", "caelum.compliance.violation"]
        elif "audit_agent" in agent:
            publishes_to = ["caelum.audit.log"]
        elif "compliance_monitor" in agent:
            publishes_to = ["caelum.compliance.violation"]

        agent_subs_map[agent] = {
            "subscribes_to": subscribes_to,
            "publishes_to": publishes_to,
            "role": "producteur/consommateur" if publishes_to and subscribes_to
                    else "producteur" if publishes_to else "consommateur",
        }

    # Diagramme de séquence textuel
    seq_lines = [
        "═" * 72,
        "  DIAGRAMME DE SÉQUENCE — Chorégraphie CaelumSwarm™",
        f"  Déclencheur : {trigger}",
        "═" * 72,
        "",
    ]
    latency_acc = 0.0
    hop_latencies = [0.8, 1.2, 5.0, 8.0, 15.0, 30.0, 0.2]

    ordered_subjects = [
        trigger,
        "caelum.alert.critical",
        "caelum.alert.high",
        "caelum.report.request",
        "caelum.press.publish",
        "caelum.client.notify",
        "caelum.audit.log",
    ]

    for i, subj in enumerate(ordered_subjects):
        if subj not in NATS_SUBJECTS:
            continue
        cfg = NATS_SUBJECTS[subj]
        subs_in_workflow = [s for s in cfg["subscribers"] if s in agents]
        if not subs_in_workflow and subj != trigger:
            continue
        hop_lat = hop_latencies[i] if i < len(hop_latencies) else 5.0
        latency_acc += hop_lat
        prefix = "  " + "  " * min(i, 5)
        seq_lines.append(f"{prefix}[t+{latency_acc:.1f}ms] ▶ {subj}")
        seq_lines.append(f"{prefix}   QoS: {cfg['qos']} | Rétention: {cfg['retention']}")
        for sub in subs_in_workflow:
            seq_lines.append(f"{prefix}   └── → {sub}")
        seq_lines.append("")

    seq_lines.append("═" * 72)
    sequence_diagram = "\n".join(seq_lines)

    failure_points = []
    for agent in agents:
        subs = agent_subs_map[agent]["subscribes_to"]
        pubs = agent_subs_map[agent]["publishes_to"]
        if len(pubs) > 1:
            failure_points.append({
                "agent": agent,
                "risque": "Producteur multi-sujets — défaillance partielle possible",
                "mitigation": "Circuit-breaker par sujet + dead-letter individuel",
                "criticite": "élevée",
            })
        if any("critical" in s or "compliance" in s for s in subs):
            failure_points.append({
                "agent": agent,
                "risque": "Traitement alerte critique — SLA strict 30s",
                "mitigation": "Consumer group + backoff exponentiel NATS JetStream",
                "criticite": "critique",
            })

    dlq_config = {
        "stream_name": "CAELUM_DLQ",
        "subjects": [f"caelum.dlq.{a.replace('_', '-')}" for a in agents],
        "retention_policy": "limits",
        "max_age_hours": 168,
        "max_bytes_MB": 128,
        "replicas": 2,
        "storage": "file",
        "alert_on_dlq_message": True,
        "dlq_monitor_subject": "caelum.alert.critical",
        "auto_retry_policy": "Manuel après inspection — zéro retry automatique sur DLQ",
    }

    return {
        "trigger": trigger,
        "agents_in_choreography": agents,
        "choreography_map": agent_subs_map,
        "sequence_diagram": sequence_diagram,
        "estimated_total_latency_ms": round(latency_acc, 1),
        "latency_breakdown": {
            "p50_ms": round(latency_acc * 0.6, 1),
            "p95_ms": round(latency_acc * 1.2, 1),
            "p99_ms": round(latency_acc * 2.0, 1),
        },
        "failure_points": failure_points,
        "total_failure_points_identified": len(failure_points),
        "dead_letter_queue_config": dlq_config,
        "pattern_used": "SAGA_ORCHESTRATION via chorégraphie événementielle pure",
        "designed_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Démonstration
# ---------------------------------------------------------------------------


def run_demo() -> bool:
    """
    Démonstration complète du protocole NATS pour CaelumSwarm™.

    Enchaîne quatre scénarios représentatifs :
      1. Publication d'un événement de completion Wave 195.
      2. Création de consommateurs JetStream pour les alertes.
      3. Simulation du flux événementiel complet Wave 194 (minerais de conflit).
      4. Design de la chorégraphie Wave → Alerte → Presse → Rapport.
    """
    separator = "━" * 72

    print(separator)
    print("  CaelumSwarm™ — Agent Protocole NATS")
    print("  Système nerveux événementiel en temps réel")
    print(separator)
    print()

    # ------------------------------------------------------------------
    # Scénario 1 — Publication événement Wave 195
    # ------------------------------------------------------------------
    print("▌ SCÉNARIO 1 — Publication completion Wave 195")
    print()

    wave_195_payload = {
        "wave": 195,
        "domains": ["digital_surveillance", "forced_labour", "land_rights"],
        "entities_analysed": 8,
        "critical_count": 4,
        "high_count": 2,
        "moderate_count": 1,
        "low_count": 1,
        "avg_composite_score": 61.34,
        "estimated_index": 6.13,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "engine_versions": {
            "digital_surveillance": "1.0.0",
            "forced_labour": "1.0.0",
            "land_rights": "1.0.0",
        },
    }

    result_pub = publish_message(
        subject="caelum.wave.result",
        payload=wave_195_payload,
        headers={
            "X-Caelum-Wave": "195",
            "X-Priority": "CRITICAL",
            "X-Source": "wave_orchestrator",
        },
    )

    print(f"  Sujet        : {result_pub['subject']}")
    print(f"  Message ID   : {result_pub['message_id']}")
    print(f"  Payload      : {result_pub['payload_bytes']} octets "
          f"({result_pub['payload_kb']} Ko)")
    print(f"  QoS          : {result_pub['qos']}")
    print(f"  Garantie     : {result_pub['delivery_guarantee']}")
    print(f"  Fanout       : {result_pub['estimated_fanout_count']} abonné(s)")
    print(f"  Abonnés      : {', '.join(result_pub['subscriber_list'])}")
    print(f"  JetStream    : {'Oui' if result_pub['jetstream_persisted'] else 'Non'}")
    print(f"  Statut       : {result_pub['status']}")
    print()

    # ------------------------------------------------------------------
    # Scénario 2 — Création de consommateurs JetStream
    # ------------------------------------------------------------------
    print("▌ SCÉNARIO 2 — Création consommateurs JetStream")
    print()

    consumers_to_create = [
        {
            "stream": "ALERTS_PERSISTENT",
            "consumer_name": "legal_processor_primary",
            "filter_subject": "caelum.alert.critical",
            "delivery_policy": "new",
        },
        {
            "stream": "ALERTS_PERSISTENT",
            "consumer_name": "compliance_monitor_01",
            "filter_subject": "caelum.compliance.violation",
            "delivery_policy": "all",
        },
        {
            "stream": "AUDIT_TRAIL",
            "consumer_name": "audit_reader_archiver",
            "filter_subject": "caelum.audit.log",
            "delivery_policy": "last",
        },
    ]

    for cspec in consumers_to_create:
        consumer = create_jetstream_consumer(**cspec)
        print(f"  ✓ {consumer['durable_name']}")
        print(f"    Stream       : {cspec['stream']}")
        print(f"    Filtre       : {cspec['filter_subject']}")
        print(f"    Livraison    : {consumer['consumer_config']['delivery_policy_label']}")
        print(f"    Backoff      : {consumer['backoff_strategy']} s")
        print(f"    Max livr.    : {consumer['max_deliver']} tentative(s)")
        print(f"    DLQ          : {consumer['dead_letter_subject']}")
        print(f"    Débit estim. : {consumer['expected_throughput_msg_per_sec']:,} msg/s")
        print()

    # ------------------------------------------------------------------
    # Scénario 3 — Simulation flux Wave 194 (minerais de conflit)
    # ------------------------------------------------------------------
    print("▌ SCÉNARIO 3 — Simulation flux événementiel Wave 194")
    print("  Domaine : minerais de conflit (conflict_minerals)")
    print()

    flow = simulate_wave_event_flow(
        wave=194,
        domains=["conflict_minerals"],
        critical_count=4,
    )

    print(f"  Wave         : {flow['wave']}")
    print(f"  Domaines     : {', '.join(flow['domains_analysed'])}")
    print(f"  Entités crit.: {flow['critical_entities']}")
    print(f"  Sauts totaux : {flow['total_hops']}")
    print(f"  Notifications: {flow['total_notifications_sent']}")
    print(f"  Fanout alerte: {flow['alert_fanout_count']}")
    print(f"  Presse       : {'Oui — seuil atteint' if flow['press_triggered'] else 'Non'}")
    print(f"  Audit loggé  : {'Oui' if flow['audit_logged'] else 'Non'}")
    print(f"  Latence tot. : {flow['total_latency_ms']} ms ({flow['latency_category']})")
    print()
    print("  Chaîne d'événements :")
    for hop in flow["event_chain"]:
        print(f"    [{hop['etape']}] {hop['subject']}")
        print(f"        {hop['label']}")
        print(f"        Latence : {hop['latency_ms']} ms | "
              f"Fanout : {hop['fanout']} | "
              f"Abonnés : {', '.join(hop['subscribers'])}")
        if hop.get("notes"):
            print(f"        Note    : {hop['notes']}")
    print()

    # ------------------------------------------------------------------
    # Scénario 4 — Chorégraphie Wave → Alerte → Presse → Rapport
    # ------------------------------------------------------------------
    print("▌ SCÉNARIO 4 — Design chorégraphie multi-agents")
    print()

    choreography = design_agent_choreography(
        agents=[
            "wave_orchestrator",
            "alert_engine",
            "press_agent",
            "report_builder",
            "client_notifier",
            "legal_team_agent",
            "audit_agent",
        ],
        trigger="caelum.wave.result",
    )

    print(f"  Déclencheur  : {choreography['trigger']}")
    print(f"  Agents       : {len(choreography['agents_in_choreography'])}")
    print(f"  Latence est. : {choreography['estimated_total_latency_ms']} ms")
    print(f"  Latence P95  : {choreography['latency_breakdown']['p95_ms']} ms")
    print(f"  Latence P99  : {choreography['latency_breakdown']['p99_ms']} ms")
    print(f"  Points défail: {choreography['total_failure_points_identified']}")
    print(f"  Pattern      : {choreography['pattern_used']}")
    print()
    print("  Carte de chorégraphie :")
    for agent, mapping in choreography["choreography_map"].items():
        print(f"    {agent} [{mapping['role']}]")
        if mapping["subscribes_to"]:
            print(f"      ← écoute : {', '.join(mapping['subscribes_to'])}")
        if mapping["publishes_to"]:
            print(f"      → publie  : {', '.join(mapping['publishes_to'])}")
    print()
    print(choreography["sequence_diagram"])
    print()
    print("  Points de défaillance identifiés :")
    for fp in choreography["failure_points"]:
        print(f"    [{fp['criticite'].upper()}] {fp['agent']}")
        print(f"      Risque      : {fp['risque']}")
        print(f"      Mitigation  : {fp['mitigation']}")
    print()
    print("  Configuration Dead-Letter Queue :")
    dlq = choreography["dead_letter_queue_config"]
    print(f"    Stream    : {dlq['stream_name']}")
    print(f"    Rétention : {dlq['max_age_hours']}h / {dlq['max_bytes_MB']} Mo")
    print(f"    Replicas  : {dlq['replicas']}")
    print(f"    Politique : {dlq['auto_retry_policy']}")
    print()

    # ------------------------------------------------------------------
    # Résumé final
    # ------------------------------------------------------------------
    print(separator)
    print("  RÉSUMÉ — Architecture NATS CaelumSwarm™")
    print(separator)
    print(f"  Sujets configurés          : {len(NATS_SUBJECTS)}")
    print(f"  Streams JetStream          : {len(JETSTREAM_STREAMS)}")
    print(f"  Patterns de messagerie     : {len(MESSAGING_PATTERNS)}")
    print(f"  Mécanismes de sécurité     : {len(NATS_SECURITY)}")
    print()
    best_security = max(NATS_SECURITY.items(), key=lambda x: x[1]["strength"])
    print(f"  Sécurité recommandée       : {best_security[0]}")
    print(f"    {best_security[1]['label']} (force : {best_security[1]['strength']}/10)")
    print(f"    Usage Caelum : {best_security[1]['caelum_use']}")
    print()
    fastest_pattern = min(
        MESSAGING_PATTERNS.items(), key=lambda x: x[1]["latency_target_ms"]
    )
    print(f"  Pattern le plus rapide     : {fastest_pattern[0]}")
    print(f"    {fastest_pattern[1]['label']}")
    print(f"    Latence cible : {fastest_pattern[1]['latency_target_ms']} ms")
    print(f"    Débit         : {fastest_pattern[1]['throughput_msg_per_sec']:,} msg/s")
    print()
    print("  NATS est le système nerveux de CaelumSwarm™ :")
    print("  sub-milliseconde en mémoire · JetStream pour la persistance ·")
    print("  chorégraphie pure sans broker central · résilience native.")
    print(separator)
    print()

    return True


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_demo()
    if success:
        print("Agent Protocole NATS — démonstration terminée avec succès.")

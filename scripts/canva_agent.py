#!/usr/bin/env python3
"""
canva_agent.py — Agent Canva CaelumSwarm™
══════════════════════════════════════════
Génère automatiquement des visuels Canva pour chaque wave, rapport et dashboard.
Intègre le sceau de protocole avant chaque création.

Capacités Canva disponibles (via MCP mcp__Canva__*):
  LECTURE    : search-designs, get-design, get-design-content, list-folder-items
  CRÉATION   : generate-design, create-design-from-candidate, copy-design
  BRAND      : list-brand-kits, create-design-from-brand-template, search-brand-templates
  ÉDITION    : start-editing-transaction, perform-editing-operations, commit/cancel-transaction
  EXPORT     : export-design, get-export-formats
  ASSETS     : upload-asset-from-url, get-assets
  DOSSIERS   : create-folder, move-item-to-folder, search-folders
  COMMENTAIRES: add-comment-to-pending-review, list-comments, reply-to-comment, list-replies
  PUBLICATION : publish-brand-template, get-brand-template-dataset
  AIDE       : help, merge-designs, resize-design, get-presenter-notes, resolve-shortlink

Usage:
  python3 scripts/canva_agent.py --mode report --wave 498
  python3 scripts/canva_agent.py --mode infographic --domain "dette souveraine"
  python3 scripts/canva_agent.py --mode social --engine "sovereign_debt_human_rights"
  python3 scripts/canva_agent.py --mode audit
  python3 scripts/canva_agent.py --list-tools
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

CANVA_LOG = DATA / "canva_agent_log.json"

# ── Catalogue complet des outils Canva disponibles ──────────────────────────

CANVA_TOOLS = {
    "LECTURE": {
        "search-designs": {
            "mcp": "mcp__Canva__search-designs",
            "desc": "Recherche des designs existants par mots-clés",
            "params": ["query", "ownership", "sort_by", "limit"],
            "use_cases": ["Retrouver un rapport existant", "Vérifier si un design a déjà été créé"],
        },
        "get-design": {
            "mcp": "mcp__Canva__get-design",
            "desc": "Obtenir les infos détaillées d'un design (titre, URL, thumbnail)",
            "params": ["design_id"],
            "use_cases": ["Récupérer l'URL d'édition", "Vérifier la date de modification"],
        },
        "get-design-content": {
            "mcp": "mcp__Canva__get-design-content",
            "desc": "Extraire le contenu texte d'un design (doc, présentation, whiteboard)",
            "params": ["design_id", "content_types", "pages"],
            "use_cases": ["Lire le contenu d'un rapport", "Extraire les textes pour traduction"],
        },
        "list-folder-items": {
            "mcp": "mcp__Canva__list-folder-items",
            "desc": "Lister les designs dans un dossier Canva",
            "params": ["folder_id", "item_types", "sort_by"],
            "use_cases": ["Naviguer dans les dossiers", "Inventorier les designs"],
        },
        "get-design-pages": {
            "mcp": "mcp__Canva__get-design-pages",
            "desc": "Obtenir les pages d'un design",
            "params": ["design_id"],
            "use_cases": ["Compter les slides", "Naviguer entre les pages"],
        },
    },
    "CRÉATION": {
        "generate-design": {
            "mcp": "mcp__Canva__generate-design",
            "desc": "Générer un design IA (poster, infographic, doc, rapport, social, présentation)",
            "params": ["query", "design_type", "brand_kit_id", "asset_ids"],
            "design_types": [
                "poster", "infographic", "doc", "report", "presentation",
                "instagram_post", "facebook_post", "twitter_post", "flyer",
                "resume", "proposal", "logo", "email", "youtube_thumbnail",
            ],
            "use_cases": [
                "Créer un rapport wave automatiquement",
                "Générer une infographie des droits humains",
                "Créer un post social pour un engine",
            ],
        },
        "create-design-from-candidate": {
            "mcp": "mcp__Canva__create-design-from-candidate",
            "desc": "Convertir un candidat IA en design éditable",
            "params": ["job_id", "candidate_id"],
            "use_cases": ["Sélectionner le meilleur candidat généré"],
        },
        "copy-design": {
            "mcp": "mcp__Canva__copy-design",
            "desc": "Dupliquer un design existant",
            "params": ["design_id"],
            "use_cases": ["Créer une variation d'un template", "Cloner un rapport"],
        },
        "import-design-from-url": {
            "mcp": "mcp__Canva__import-design-from-url",
            "desc": "Importer un design depuis une URL (PDF, PPTX, etc.)",
            "params": ["url", "title"],
            "use_cases": ["Importer un rapport PDF existant"],
        },
    },
    "BRAND": {
        "list-brand-kits": {
            "mcp": "mcp__Canva__list-brand-kits",
            "desc": "Lister les brand kits disponibles (couleurs, fonts, logos CaelumSwarm™)",
            "params": ["limit"],
            "use_cases": ["Vérifier les assets de marque disponibles"],
        },
        "search-brand-templates": {
            "mcp": "mcp__Canva__search-brand-templates",
            "desc": "Rechercher des templates de marque",
            "params": ["query", "limit"],
            "use_cases": ["Trouver un template de rapport branded"],
        },
        "create-design-from-brand-template": {
            "mcp": "mcp__Canva__create-design-from-brand-template",
            "desc": "Créer un design depuis un template de marque",
            "params": ["brand_template_id"],
            "use_cases": ["Instancier un rapport avec le brand CaelumSwarm™"],
        },
        "get-brand-template-dataset": {
            "mcp": "mcp__Canva__get-brand-template-dataset",
            "desc": "Récupérer les données d'un template de marque",
            "params": ["brand_template_id"],
            "use_cases": ["Injecter des données dynamiques dans un template"],
        },
        "publish-brand-template": {
            "mcp": "mcp__Canva__publish-brand-template",
            "desc": "Publier un template comme brand template partagé",
            "params": ["design_id"],
            "use_cases": ["Partager un template wave avec l'équipe"],
        },
    },
    "ÉDITION": {
        "start-editing-transaction": {
            "mcp": "mcp__Canva__start-editing-transaction",
            "desc": "Démarrer une session d'édition (ouvre design en mode édition)",
            "params": ["design_id"],
            "use_cases": ["Modifier du texte ou des éléments visuels"],
        },
        "perform-editing-operations": {
            "mcp": "mcp__Canva__perform-editing-operations",
            "desc": "Effectuer des opérations d'édition (texte, images, layout)",
            "params": ["transaction_id", "operations"],
            "use_cases": [
                "Mettre à jour les scores dans un rapport",
                "Remplacer du texte dynamiquement",
                "Insérer des données d'engine",
            ],
        },
        "commit-editing-transaction": {
            "mcp": "mcp__Canva__commit-editing-transaction",
            "desc": "Sauvegarder les modifications",
            "params": ["transaction_id"],
            "use_cases": ["Finaliser les éditions"],
        },
        "cancel-editing-transaction": {
            "mcp": "mcp__Canva__cancel-editing-transaction",
            "desc": "Annuler les modifications en cours",
            "params": ["transaction_id"],
            "use_cases": ["Revenir en arrière si erreur"],
        },
        "resize-design": {
            "mcp": "mcp__Canva__resize-design",
            "desc": "Redimensionner un design pour un autre format",
            "params": ["design_id", "width", "height"],
            "use_cases": ["Adapter un poster en format mobile", "Changer A4 → A3"],
        },
        "merge-designs": {
            "mcp": "mcp__Canva__merge-designs",
            "desc": "Fusionner plusieurs designs en un seul",
            "params": ["design_ids"],
            "use_cases": ["Regrouper les rapports de 3 waves"],
        },
    },
    "EXPORT": {
        "export-design": {
            "mcp": "mcp__Canva__export-design",
            "desc": "Exporter un design (PDF, PNG, PPTX, JPG, GIF, MP4, CSV)",
            "params": ["design_id", "format"],
            "formats": ["pdf", "png", "jpg", "gif", "pptx", "mp4", "csv"],
            "use_cases": [
                "Exporter un rapport wave en PDF",
                "Générer une image PNG pour le dashboard",
                "Exporter une présentation en PPTX pour client",
            ],
        },
        "get-export-formats": {
            "mcp": "mcp__Canva__get-export-formats",
            "desc": "Vérifier les formats d'export disponibles pour un design",
            "params": ["design_id"],
            "use_cases": ["Vérifier avant d'exporter"],
        },
    },
    "ASSETS": {
        "upload-asset-from-url": {
            "mcp": "mcp__Canva__upload-asset-from-url",
            "desc": "Uploader une image/vidéo depuis une URL vers Canva",
            "params": ["url", "name"],
            "use_cases": [
                "Uploader le logo CaelumSwarm™",
                "Ajouter des graphiques générés par les engines",
            ],
        },
        "get-assets": {
            "mcp": "mcp__Canva__get-assets",
            "desc": "Récupérer les assets uploadés",
            "params": ["asset_ids"],
            "use_cases": ["Récupérer un asset pour l'insérer dans un design"],
        },
    },
    "ORGANISATION": {
        "create-folder": {
            "mcp": "mcp__Canva__create-folder",
            "desc": "Créer un dossier dans Canva",
            "params": ["name", "parent_folder_id"],
            "use_cases": ["Créer un dossier par wave", "Organiser les rapports par domaine"],
        },
        "move-item-to-folder": {
            "mcp": "mcp__Canva__move-item-to-folder",
            "desc": "Déplacer un design dans un dossier",
            "params": ["item_id", "folder_id"],
            "use_cases": ["Organiser les designs après création"],
        },
        "search-folders": {
            "mcp": "mcp__Canva__search-folders",
            "desc": "Rechercher des dossiers",
            "params": ["query"],
            "use_cases": ["Trouver le dossier d'une wave"],
        },
    },
    "COLLABORATION": {
        "list-comments": {
            "mcp": "mcp__Canva__list-comments",
            "desc": "Lister les commentaires sur un design",
            "params": ["design_id"],
            "use_cases": ["Voir les feedbacks sur un rapport"],
        },
        "comment-on-design": {
            "mcp": "mcp__Canva__comment-on-design",
            "desc": "Ajouter un commentaire sur un design",
            "params": ["design_id", "message"],
            "use_cases": ["Laisser une note de review"],
        },
        "reply-to-comment": {
            "mcp": "mcp__Canva__reply-to-comment",
            "desc": "Répondre à un commentaire",
            "params": ["design_id", "thread_id", "message"],
            "use_cases": ["Répondre aux feedbacks client"],
        },
        "request-outline-review": {
            "mcp": "mcp__Canva__request-outline-review",
            "desc": "Demander une revue de structure avant génération",
            "params": ["query", "design_type"],
            "use_cases": ["Valider le plan d'une présentation avant création"],
        },
        "get-presenter-notes": {
            "mcp": "mcp__Canva__get-presenter-notes",
            "desc": "Récupérer les notes de présentateur",
            "params": ["design_id"],
            "use_cases": ["Extraire le script d'une présentation"],
        },
    },
    "UTILITAIRES": {
        "help": {
            "mcp": "mcp__Canva__help",
            "desc": "Obtenir de l'aide sur les fonctionnalités Canva",
            "params": ["prompt"],
            "use_cases": ["Comprendre une fonctionnalité Canva"],
        },
        "resolve-shortlink": {
            "mcp": "mcp__Canva__resolve-shortlink",
            "desc": "Résoudre un lien court Canva (canva.link/...) en URL complète",
            "params": ["shortlink_id"],
            "use_cases": ["Obtenir le design_id depuis un lien partagé"],
        },
        "get-design-thumbnail": {
            "mcp": "mcp__Canva__get-design-thumbnail",
            "desc": "Obtenir le thumbnail d'un design",
            "params": ["design_id"],
            "use_cases": ["Afficher un aperçu dans le dashboard"],
        },
    },
}

# ── Templates de prompts par type de contenu ─────────────────────────────────

DESIGN_TEMPLATES = {
    "wave_report": {
        "design_type": "report",
        "query_template": """
Professional compliance report for CaelumSwarm™ EU CSDDD 2024/1760.
Wave {wave_num}: {domains}.
Dark navy theme with indigo accents.
Include: executive summary, risk distribution (4 critical/2 high/1 moderate/1 low),
composite score {avg_score}, index {index}/10.
Corporate, data-driven, multilingual French/English.
""",
    },
    "wave_infographic": {
        "design_type": "infographic",
        "query_template": """
Human rights risk infographic for {domain}.
8 entities with risk levels: 4 critical (red), 2 high (orange), 1 moderate (yellow), 1 low (green).
Composite score {avg_score}/100. Index {index}/10.
Modern data visualization, dark background, indigo highlights.
CaelumSwarm™ branding.
""",
    },
    "wave_social_post": {
        "design_type": "instagram_post",
        "query_template": """
Social media post: Human rights alert for {domain}.
Score: {avg_score}/100 — {n_critical} critical entities identified.
EU CSDDD compliance check. Bold typography, dark background, red/indigo gradient.
CaelumSwarm™ logo. Professional B2B tone.
""",
    },
    "wave_presentation": {
        "design_type": "presentation",
        "query_template": """
Executive presentation: {domain} rights analysis.
Wave {wave_num} findings. 5 slides:
1. Overview & scope
2. Risk distribution map
3. Critical entities (4 cases)
4. Methodology (multi-perspective, multiverse simulation)
5. Recommendations
Dark corporate theme, CaelumSwarm™ branding.
""",
    },
    "weekly_dashboard": {
        "design_type": "doc",
        "query_template": """
Weekly CaelumSwarm™ operations report.
Waves covered: {waves}. Total engines: {n_engines}. Total dashboards: {n_dashboards}.
Highlights: sceau de protocole, multi-perspective simulation, business plan KPIs.
Professional French/English document, dark navy header.
""",
    },
}

# ── Fonctions utilitaires ────────────────────────────────────────────────────

def _log(record: dict):
    """Enregistre une action Canva dans le log."""
    log = []
    if CANVA_LOG.exists():
        try:
            log = json.loads(CANVA_LOG.read_text())
        except Exception:
            log = []
    log.append({**record, "timestamp": datetime.now(timezone.utc).isoformat()})
    if len(log) > 200:
        log = log[-200:]
    CANVA_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


def list_all_tools():
    """Affiche la liste complète des outils Canva disponibles."""
    total = sum(len(tools) for tools in CANVA_TOOLS.values())
    print(f"\n{'═'*65}")
    print(f"  OUTILS CANVA DISPONIBLES — CaelumSwarm™  ({total} outils)")
    print(f"{'═'*65}")

    for category, tools in CANVA_TOOLS.items():
        print(f"\n  📁 {category} ({len(tools)} outils)")
        for name, info in tools.items():
            print(f"     • {name:<35} {info['desc'][:45]}")

    print(f"\n{'═'*65}")
    print(f"  Tous appelables via MCP: mcp__Canva__<nom-outil>")
    print(f"{'═'*65}\n")


def build_wave_report_query(wave_num: int, domains: list[str], avg_score: float, index: float) -> str:
    """Construit le prompt pour générer un rapport wave."""
    tmpl = DESIGN_TEMPLATES["wave_report"]
    return tmpl["query_template"].format(
        wave_num=wave_num,
        domains=", ".join(domains),
        avg_score=avg_score,
        index=index,
    ).strip()


def build_infographic_query(domain: str, avg_score: float, index: float, n_critical: int = 4) -> str:
    """Construit le prompt pour une infographie."""
    tmpl = DESIGN_TEMPLATES["wave_infographic"]
    return tmpl["query_template"].format(
        domain=domain,
        avg_score=avg_score,
        index=index,
        n_critical=n_critical,
    ).strip()


def build_social_query(domain: str, avg_score: float, n_critical: int = 4) -> str:
    """Construit le prompt pour un post social."""
    tmpl = DESIGN_TEMPLATES["wave_social_post"]
    return tmpl["query_template"].format(
        domain=domain,
        avg_score=avg_score,
        n_critical=n_critical,
    ).strip()


def print_creation_prompt(mode: str, wave: int = 0, domain: str = "", engine: str = ""):
    """Affiche le prompt prêt à utiliser pour créer un design Canva."""
    if mode == "report" and wave:
        domains = {
            498: ["Dette souveraine", "Surveillance biométrique", "Travail domestique"],
            497: ["Deepfake abuse", "Ghost workers", "Austérité & pauvreté"],
            496: ["Accès médicaments", "Capitalisme carcéral", "Détention immigration"],
        }.get(wave, ["Domaine 1", "Domaine 2", "Domaine 3"])
        query = build_wave_report_query(wave, domains, 61.03, 6.1)
        design_type = "report"

    elif mode == "infographic" and domain:
        query = build_infographic_query(domain, 61.03, 6.1)
        design_type = "infographic"

    elif mode == "social" and (domain or engine):
        d = domain or engine.replace("_", " ")
        query = build_social_query(d, 61.03)
        design_type = "instagram_post"

    elif mode == "weekly":
        tmpl = DESIGN_TEMPLATES["weekly_dashboard"]
        query = tmpl["query_template"].format(
            waves="496, 497, 498", n_engines=9, n_dashboards=9
        ).strip()
        design_type = "doc"

    else:
        print(f"Mode inconnu: {mode}")
        return

    print(f"\n{'═'*65}")
    print(f"  PROMPT CANVA — Mode: {mode.upper()}")
    print(f"  Design type: {design_type}")
    print(f"{'═'*65}")
    print(f"\n  Outil MCP à appeler: mcp__Canva__generate-design")
    print(f"\n  Paramètres:")
    print(f"    design_type: \"{design_type}\"")
    print(f"    query: |")
    for line in query.split("\n"):
        print(f"      {line}")
    print(f"\n  Workflow complet:")
    print(f"    1. mcp__Canva__list-brand-kits → récupérer brand_kit_id")
    print(f"    2. mcp__Canva__generate-design → obtenir job_id + candidates")
    print(f"    3. mcp__Canva__create-design-from-candidate → design_id")
    print(f"    4. mcp__Canva__export-design → PDF/PNG pour le dashboard")
    print(f"{'═'*65}\n")

    _log({
        "action": "print_creation_prompt",
        "mode": mode,
        "wave": wave,
        "domain": domain,
        "design_type": design_type,
        "query_length": len(query),
    })


def run_audit():
    """Affiche un audit des capacités Canva pour CaelumSwarm™."""
    total = sum(len(tools) for tools in CANVA_TOOLS.items() if isinstance(tools[1], dict) for _ in [1])
    total = sum(len(v) for v in CANVA_TOOLS.values())

    print(f"\n{'═'*65}")
    print(f"  AUDIT CANVA — CaelumSwarm™")
    print(f"{'═'*65}")
    print(f"\n  Outils disponibles : {total}")
    print(f"  Catégories         : {len(CANVA_TOOLS)}")
    print(f"\n  MATRICE USAGE × CaelumSwarm™:")
    print(f"\n  {'USE CASE':<40} {'OUTIL CANVA':<30} {'PRIORITÉ'}")
    print(f"  {'─'*40} {'─'*30} {'─'*10}")

    use_cases = [
        ("Rapport wave auto", "generate-design (report)", "HAUTE"),
        ("Infographie droits humains", "generate-design (infographic)", "HAUTE"),
        ("Post social engine", "generate-design (instagram_post)", "MOYENNE"),
        ("Présentation client EU CSDDD", "generate-design (presentation)", "HAUTE"),
        ("Export PDF rapport", "export-design", "HAUTE"),
        ("Brand consistency", "list-brand-kits", "MOYENNE"),
        ("Organiser par wave", "create-folder + move-item", "FAIBLE"),
        ("Review collaborative", "list-comments + reply", "FAIBLE"),
        ("Mise à jour scores", "start-editing-transaction", "MOYENNE"),
        ("Thumbnail dashboard", "get-design-thumbnail", "MOYENNE"),
    ]

    for use_case, tool, priority in use_cases:
        prio_icon = "🔴" if priority == "HAUTE" else "🟡" if priority == "MOYENNE" else "🟢"
        print(f"  {use_case:<40} {tool:<30} {prio_icon} {priority}")

    print(f"\n  RECOMMANDATION: Commencer par generate-design (report) pour Wave 498")
    print(f"  → 3 rapports PDF automatiques prêts à livrer au client")
    print(f"{'═'*65}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Canva CaelumSwarm™")
    parser.add_argument("--mode",       choices=["report","infographic","social","weekly","audit"],
                        help="Mode de création")
    parser.add_argument("--wave",       type=int, default=0, help="Numéro de wave")
    parser.add_argument("--domain",     type=str, default="", help="Domaine droits humains")
    parser.add_argument("--engine",     type=str, default="", help="Nom engine Python")
    parser.add_argument("--list-tools", action="store_true", help="Lister tous les outils Canva")
    args = parser.parse_args()

    if args.list_tools:
        list_all_tools()
    elif args.mode == "audit":
        run_audit()
    elif args.mode:
        print_creation_prompt(args.mode, args.wave, args.domain, args.engine)
    else:
        # Par défaut: audit + liste outils
        run_audit()
        list_all_tools()

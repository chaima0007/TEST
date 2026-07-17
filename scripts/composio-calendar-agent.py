#!/usr/bin/env python3
"""
Composio Calendar Agent — Caelum Partners
Agent de gestion du calendrier via Composio (Google Calendar / Outlook).

Mode simulation : génère des événements et exporte un fichier .ics.
Mode Composio   : synchronise via l'API Composio si COMPOSIO_API_KEY est définie.
"""

import os
import json
from datetime import datetime, timedelta, date
from pathlib import Path

# ---------------------------------------------------------------------------
# Événements pré-configurés pour Caelum Partners
# ---------------------------------------------------------------------------
CALENDAR_EVENTS = {
    "deadline_candidatures": [
        {
            "titre": "DEADLINE Innoviris Proof of Concept",
            "date": "2026-09-15",
            "heure": "17:00",
            "durée_h": 1,
            "rappel_jours": [30, 14, 7, 1],
        },
        {
            "titre": "DEADLINE EIC Accelerator Session 2",
            "date": "2026-10-01",
            "heure": "17:00",
            "durée_h": 1,
            "rappel_jours": [60, 30, 14],
        },
        {
            "titre": "DEADLINE FEDER Bruxelles",
            "date": "2026-10-15",
            "heure": "12:00",
            "durée_h": 1,
            "rappel_jours": [30, 7],
        },
    ],
    "certification_sessions": [
        {
            "titre": "Google AI Essentials — Début",
            "date": "2026-07-01",
            "heure": "09:00",
            "durée_h": 2,
            "récurrence": "hebdomadaire",
            "nb_semaines": 3,
        },
        {
            "titre": "Cisco Python Essentials 1 — Session",
            "date": "2026-07-07",
            "heure": "18:00",
            "durée_h": 2,
            "récurrence": "hebdomadaire",
            "nb_semaines": 10,
        },
        {
            "titre": "Google Cybersecurity Certificate — Début",
            "date": "2026-08-01",
            "heure": "09:00",
            "durée_h": 3,
            "récurrence": "hebdomadaire",
            "nb_semaines": 24,
        },
    ],
    "prospection_calls": [
        {
            "titre": "Appel découverte {prospect}",
            "durée_h": 0.5,
            "template": True,
        },
    ],
    "reviews_waves": [
        {
            "titre": "Review Wave {n} — CaelumSwarm",
            "date_récurrence": "lundi",
            "heure": "10:00",
            "durée_h": 1,
        },
    ],
}

COMPOSIO_INSTRUCTIONS = """
Pour activer la synchronisation calendrier réelle :
1. Créer un compte sur composio.dev (gratuit)
2. Générer une API key dans le dashboard
3. export COMPOSIO_API_KEY=your_key
4. composio add googlecalendar  (ou outlook)
5. Tester : composio actions --app googlecalendar
6. Relancer ce script
"""

# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def create_event(
    titre: str,
    date_str: str,
    heure: str,
    durée_h: float,
    rappel_jours: list = None,
    description: str = "",
) -> dict:
    """
    Crée un dict représentant un événement calendrier.

    Args:
        titre       : Titre de l'événement
        date_str    : Date au format YYYY-MM-DD
        heure       : Heure de début HH:MM
        durée_h     : Durée en heures (float)
        rappel_jours: Liste des jours avant l'événement pour les rappels
        description : Description optionnelle

    Retourne un dict événement formaté.
    """
    rappel_jours = rappel_jours or []
    dt_start = datetime.strptime(f"{date_str} {heure}", "%Y-%m-%d %H:%M")
    dt_end = dt_start + timedelta(hours=durée_h)
    rappels = [
        {
            "date": (dt_start - timedelta(days=j)).strftime("%Y-%m-%d"),
            "label": f"Rappel J-{j} : {titre}",
        }
        for j in rappel_jours
    ]
    return {
        "titre": titre,
        "date_debut": dt_start.strftime("%Y-%m-%d %H:%M"),
        "date_fin": dt_end.strftime("%Y-%m-%d %H:%M"),
        "durée_h": durée_h,
        "rappels": rappels,
        "description": description,
    }


def schedule_candidature_deadlines() -> list[dict]:
    """
    Génère tous les événements de deadlines de candidatures avec rappels.
    Retourne une liste de dicts événements.
    """
    events = []
    for item in CALENDAR_EVENTS["deadline_candidatures"]:
        evt = create_event(
            titre=item["titre"],
            date_str=item["date"],
            heure=item["heure"],
            durée_h=item["durée_h"],
            rappel_jours=item.get("rappel_jours", []),
            description=f"Deadline candidature financement — {item['titre']}",
        )
        events.append(evt)
    return events


def schedule_certification_roadmap() -> list[dict]:
    """
    Génère les sessions de formation Google AI + Cisco + Cybersecurity.
    Gère la récurrence hebdomadaire.
    Retourne une liste de dicts événements.
    """
    events = []
    for item in CALENDAR_EVENTS["certification_sessions"]:
        nb = item.get("nb_semaines", 1)
        dt_base = datetime.strptime(item["date"], "%Y-%m-%d")
        for i in range(nb):
            dt_session = dt_base + timedelta(weeks=i)
            session_titre = item["titre"] if i == 0 else f"{item['titre']} (S{i + 1})"
            evt = create_event(
                titre=session_titre,
                date_str=dt_session.strftime("%Y-%m-%d"),
                heure=item["heure"],
                durée_h=item["durée_h"],
                description=f"Session certification — {item['titre']}",
            )
            events.append(evt)
    return events


def _ical_datetime(dt_str: str) -> str:
    """Convertit 'YYYY-MM-DD HH:MM' en format iCalendar UTC basique."""
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    return dt.strftime("%Y%m%dT%H%M%S")


def export_ical(events_list: list[dict], output_path: str = None) -> str:
    """
    Génère un fichier .ics (iCalendar) prêt à importer dans Google Calendar / Outlook.

    Args:
        events_list : Liste de dicts événements (sortie de create_event / schedule_*)
        output_path : Chemin de sortie (défaut : docs/candidatures/calendrier_caelum_2026.ics)

    Retourne le contenu du fichier .ics.
    """
    if output_path is None:
        output_path = str(
            Path(__file__).parent.parent / "docs" / "candidatures" / "calendrier_caelum_2026.ics"
        )

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Caelum Partners//CaelumSwarm Calendar Agent//FR",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Caelum Partners 2026",
        "X-WR-TIMEZONE:Europe/Brussels",
    ]

    now_str = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    for i, evt in enumerate(events_list):
        uid = f"caelum-{i + 1:04d}-{datetime.utcnow().strftime('%Y%m%d')}@caelumpartners.be"
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{now_str}",
            f"DTSTART:{_ical_datetime(evt['date_debut'])}",
            f"DTEND:{_ical_datetime(evt['date_fin'])}",
            f"SUMMARY:{evt['titre']}",
            f"DESCRIPTION:{evt.get('description', '')}",
            "STATUS:CONFIRMED",
        ]
        # Rappels (VALARM)
        for rappel in evt.get("rappels", []):
            # Calcul du delta en minutes par rapport au début
            dt_event = datetime.strptime(evt["date_debut"], "%Y-%m-%d %H:%M")
            dt_rappel = datetime.strptime(rappel["date"] + " 09:00", "%Y-%m-%d %H:%M")
            delta_minutes = int((dt_rappel - dt_event).total_seconds() / 60)
            lines += [
                "BEGIN:VALARM",
                "TRIGGER;VALUE=DURATION:" + (f"-PT{abs(delta_minutes)}M" if delta_minutes < 0 else f"PT{delta_minutes}M"),
                "ACTION:DISPLAY",
                f"DESCRIPTION:{rappel['label']}",
                "END:VALARM",
            ]
        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")

    ical_content = "\r\n".join(lines) + "\r\n"

    # Écriture du fichier
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(ical_content, encoding="utf-8")
    print(f"[OK] Fichier iCalendar généré : {output_path}")
    return ical_content


def connect_composio() -> bool:
    """
    Vérifie si COMPOSIO_API_KEY est présente.
    Affiche les instructions si absente.
    Retourne True si disponible, False sinon.
    """
    api_key = os.environ.get("COMPOSIO_API_KEY", "")
    if api_key:
        print("[OK] COMPOSIO_API_KEY détectée — mode Composio actif")
        return True
    else:
        print("[INFO] COMPOSIO_API_KEY absente — mode simulation uniquement")
        print(COMPOSIO_INSTRUCTIONS)
        return False


def sync_via_composio(events_list: list[dict]) -> dict:
    """
    Synchronise les événements via l'API Composio (Google Calendar).
    Nécessite COMPOSIO_API_KEY dans l'environnement.

    Retourne un dict avec le résultat de l'opération.
    """
    if not connect_composio():
        return {"status": "skipped", "reason": "COMPOSIO_API_KEY manquante"}

    try:
        from composio_openai import ComposioToolSet, App  # type: ignore

        toolset = ComposioToolSet(api_key=os.environ["COMPOSIO_API_KEY"])
        results = []
        for evt in events_list:
            payload = {
                "summary": evt["titre"],
                "start": {"dateTime": evt["date_debut"].replace(" ", "T") + ":00", "timeZone": "Europe/Brussels"},
                "end": {"dateTime": evt["date_fin"].replace(" ", "T") + ":00", "timeZone": "Europe/Brussels"},
                "description": evt.get("description", ""),
            }
            result = toolset.execute_action(
                action="GOOGLECALENDAR_CREATE_EVENT",
                params=payload,
            )
            results.append({"titre": evt["titre"], "result": result})
            print(f"[OK] Événement créé : {evt['titre']}")

        return {"status": "synced", "count": len(results), "results": results}

    except ImportError:
        print("[WARN] SDK composio-openai non installé — pip install composio-openai")
        print("[INFO] Export iCal disponible en mode simulation")
        return {"status": "simulated", "reason": "SDK non installé"}
    except Exception as exc:
        print(f"[ERROR] Echec synchronisation Composio : {exc}")
        return {"status": "error", "error": str(exc)}


def _print_calendar_view(events: list[dict], title: str) -> None:
    """Affiche un calendrier lisible en console."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    # Grouper par mois
    by_month: dict = {}
    for evt in events:
        month_key = evt["date_debut"][:7]
        by_month.setdefault(month_key, []).append(evt)

    for month, evts in sorted(by_month.items()):
        dt = datetime.strptime(month + "-01", "%Y-%m-%d")
        print(f"\n  {dt.strftime('%B %Y').upper()}")
        print("  " + "-" * 50)
        for e in sorted(evts, key=lambda x: x["date_debut"]):
            print(f"  {e['date_debut'][:10]}  {e['heure'] if 'heure' in e else e['date_debut'][11:16]}  {e['titre']}")
            if e.get("rappels"):
                dates_rappels = [r["date"] for r in e["rappels"]]
                print(f"             Rappels : {', '.join(dates_rappels)}")


# ---------------------------------------------------------------------------
# Point d'entrée — démo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("COMPOSIO CALENDAR AGENT — Caelum Partners")
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()

    # Vérification connexion Composio
    connected = connect_composio()
    print()

    # Génération des événements
    print("[1/3] Génération des deadlines de candidatures...")
    deadline_events = schedule_candidature_deadlines()
    print(f"      -> {len(deadline_events)} deadline(s) générée(s)")

    print("[2/3] Génération du calendrier de certifications...")
    cert_events = schedule_certification_roadmap()
    print(f"      -> {len(cert_events)} session(s) générée(s)")

    all_events = deadline_events + cert_events
    print(f"\n[3/3] Total : {len(all_events)} événement(s) pour juillet–décembre 2026")

    # Affichage du calendrier
    _print_calendar_view(
        deadline_events,
        "DEADLINES CANDIDATURES FINANCEMENT 2026",
    )

    _print_calendar_view(
        cert_events[:8],  # Aperçu : 8 premières sessions
        "SESSIONS CERTIFICATIONS 2026 (aperçu)",
    )

    # Export iCal
    print()
    ical_path = str(
        Path(__file__).parent.parent / "docs" / "candidatures" / "calendrier_caelum_2026.ics"
    )
    export_ical(all_events, output_path=ical_path)

    print()
    print("[DONE] Calendrier Caelum 2026 prêt.")
    if not connected:
        print("Pour synchroniser avec Google Calendar, suivre les instructions ci-dessus.")

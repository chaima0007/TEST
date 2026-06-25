"""
temporal-score-evolution-agent.py — Caelum Partners
Calcule et analyse l'évolution des scores dans le temps.
Compare les waves, détecte les tendances, alerte sur les dégradations.
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path

# ─── Historique simulé des scores par wave ───────────────────────────────────
# Format: {wave: {domain: avg_composite}}

WAVE_HISTORY = {
    188: {
        "quantum_surveillance_privacy_rights": 60.18,
        "post_quantum_cryptography_rights": 60.36,
        "quantum_supremacy_arms_race": 57.28,
    },
    189: {
        "biotech_genetic_discrimination_rights": 62.02,
        "carbon_colonialism_climate_justice": 61.97,
        "digital_feudalism_platform_rights": 62.49,
    },
    190: {
        "neurotech_cognitive_liberty_rights": 58.56,
        "space_colonization_indigenous_rights": 59.97,
        "synthetic_biology_biosafety_rights": 60.89,
    },
    191: {
        "algorithmic_justice_bias_rights": 60.14,
        "water_privatization_commons_rights": 60.00,
        "prison_industrial_complex_rights": 60.71,
    },
    192: {
        "dark_web_cybercrime_rights": 63.11,
        "gig_economy_labor_exploitation": 62.61,
        "indigenous_language_extinction_rights": 63.08,
    },
    193: {
        "deepfake_synthetic_media_rights": 59.63,
        "offshore_tax_haven_rights": 62.26,
        "statelessness_document_rights": 62.29,
    },
}


# ─── Calculs temporels ───────────────────────────────────────────────────────

def wave_averages():
    """Moyenne globale par wave."""
    return {
        wave: round(sum(scores.values()) / len(scores), 2)
        for wave, scores in WAVE_HISTORY.items()
    }


def trend(values: list) -> str:
    """Détecte la tendance : hausse, baisse, stable."""
    if len(values) < 2:
        return "stable"
    deltas = [values[i+1] - values[i] for i in range(len(values)-1)]
    avg_delta = sum(deltas) / len(deltas)
    if avg_delta > 0.5:
        return "hausse"
    if avg_delta < -0.5:
        return "baisse"
    return "stable"


def velocity(values: list) -> float:
    """Vitesse de changement (points/wave)."""
    if len(values) < 2:
        return 0.0
    return round((values[-1] - values[0]) / (len(values) - 1), 3)


def momentum(values: list) -> float:
    """Accélération : le changement s'accélère-t-il ?"""
    if len(values) < 3:
        return 0.0
    v1 = values[-1] - values[-2]
    v2 = values[-2] - values[-3]
    return round(v1 - v2, 3)


def time_to_threshold(current: float, rate: float, threshold: float) -> str:
    """Estime combien de waves avant d'atteindre un seuil."""
    if rate == 0:
        return "jamais (stable)"
    waves_needed = (threshold - current) / rate
    if waves_needed < 0:
        return "seuil déjà dépassé"
    if waves_needed > 100:
        return f"> 100 waves"
    return f"~{waves_needed:.1f} waves"


def risk_acceleration_alert(values: list, threshold: float = 65.0) -> bool:
    """Alerte si le score accélère vers le seuil critique."""
    m = momentum(values)
    v = velocity(values)
    return v > 0 and m > 0 and values[-1] > threshold * 0.85


# ─── Analyse complète ────────────────────────────────────────────────────────

def analyze():
    waves = sorted(WAVE_HISTORY.keys())
    avgs = wave_averages()

    print("=" * 70)
    print("⏱  Temporal Score Evolution Agent — Caelum Partners")
    print(f"   Analyse de {len(waves)} waves ({waves[0]}→{waves[-1]})")
    print("=" * 70)

    # ── Évolution globale ──
    avg_values = [avgs[w] for w in waves]
    global_trend = trend(avg_values)
    global_vel = velocity(avg_values)
    global_mom = momentum(avg_values)

    print(f"\n📈  ÉVOLUTION GLOBALE")
    print(f"   Tendance : {global_trend.upper()}")
    print(f"   Vélocité : {global_vel:+.3f} pts/wave")
    print(f"   Momentum : {global_mom:+.3f} (accélération)")

    for w in waves:
        bar = "█" * int(avgs[w] / 5)
        arrow = "↑" if avgs[w] > avgs.get(w-1, avgs[w]) else "↓" if avgs[w] < avgs.get(w-1, avgs[w]) else "→"
        print(f"   Wave {w}: {avgs[w]:5.2f} {arrow}  {bar}")

    # ── Domaines les plus dégradés ──
    print(f"\n🔴  DOMAINES À PLUS FORTE PROGRESSION (RISQUE CROISSANT)")
    all_scores = {}
    for wave, domains in WAVE_HISTORY.items():
        for domain, score in domains.items():
            if domain not in all_scores:
                all_scores[domain] = []
            all_scores[domain].append(score)

    sorted_domains = sorted(all_scores.items(), key=lambda x: x[1][-1], reverse=True)
    for domain, scores in sorted_domains[:5]:
        v = velocity(scores)
        t = trend(scores)
        tte = time_to_threshold(scores[-1], v, 70.0)
        icon = "🔴" if scores[-1] >= 63 else "🟡" if scores[-1] >= 60 else "🟢"
        print(f"   {icon} {domain[:45]:<45} score={scores[-1]:.2f} vel={v:+.2f} → seuil 70 dans {tte}")

    # ── Projection future ──
    print(f"\n🔮  PROJECTION WAVE 194 (basée sur vélocité actuelle)")
    projected_194 = round(avg_values[-1] + global_vel, 2)
    proj_trend = "hausse" if global_vel > 0 else "baisse" if global_vel < 0 else "stable"
    print(f"   Score moyen projeté Wave 194 : {projected_194:.2f}")
    print(f"   Tendance : {proj_trend}")
    if projected_194 > 65:
        print(f"   ⚠️  ALERTE : Score global approche seuil critique 65.0")
    elif projected_194 > 62:
        print(f"   ⚠️  Score en zone de vigilance (>62)")
    else:
        print(f"   ✓  Score dans la plage normale")

    # ── Temps avant seuil global ──
    print(f"\n⏰  TEMPS ESTIMÉ AVANT SEUILS")
    for threshold, label in [(65.0, "VIGILANCE"), (70.0, "ALERTE"), (80.0, "CRISE")]:
        tte = time_to_threshold(avg_values[-1], global_vel, threshold)
        print(f"   Seuil {threshold} [{label}] : {tte}")

    # ── Alertes ──
    alerts = []
    if global_vel > 0.5:
        alerts.append(f"Hausse accélérée : +{global_vel:.2f} pts/wave en moyenne")
    if global_mom > 0.3:
        alerts.append(f"Momentum positif : l'accélération s'intensifie (+{global_mom:.2f})")
    if avg_values[-1] > 63:
        alerts.append(f"Score Wave {waves[-1]} dépasse 63 — zone de vigilance")

    print(f"\n🚨  ALERTES TEMPORELLES ({len(alerts)})")
    if alerts:
        for a in alerts:
            print(f"   • {a}")
    else:
        print(f"   ✓  Aucune alerte — progression normale")

    print("\n" + "=" * 70)
    return {
        "wave_averages": avgs,
        "global_trend": global_trend,
        "global_velocity": global_vel,
        "projected_wave_194": projected_194,
        "alerts": alerts,
    }


if __name__ == "__main__":
    result = analyze()

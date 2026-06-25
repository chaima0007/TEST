#!/usr/bin/env python3
"""
Press Relations Agent — Caelum Partners CaelumSwarm™
Relations presse automatisées : communiqués, médias lists, pitches,
suivi couverture — pour lancement de waves et rapports droits humains.
"""

import sys
from datetime import datetime, timedelta, timezone

MEDIA_DATABASE = {
    "LE_MONDE_ECONOMIE": {
        "label": "Le Monde Économie & Entreprise",
        "type": "PRESSE_NATIONALE",
        "audience_M": 8.5,
        "focus": ["RSE", "conformité", "droits humains entreprise"],
        "journalist_beat": "Responsabilité des entreprises",
        "contact_format": "Email + dossier de presse PDF",
        "lead_time_days": 7,
        "priority": "HAUTE",
    },
    "LES_ECHOS": {
        "label": "Les Échos",
        "type": "PRESSE_NATIONALE",
        "audience_M": 5.2,
        "focus": ["finance", "réglementation EU", "ESG"],
        "journalist_beat": "Finance durable & réglementation",
        "contact_format": "Email concis + exclusivité data",
        "lead_time_days": 5,
        "priority": "HAUTE",
    },
    "REUTERS_ESG": {
        "label": "Reuters ESG",
        "type": "AGENCE_INTERNATIONALE",
        "audience_M": 50.0,
        "focus": ["ESG", "human rights", "corporate accountability"],
        "journalist_beat": "Sustainable business & human rights",
        "contact_format": "Short pitch EN + key data point",
        "lead_time_days": 2,
        "priority": "TRÈS HAUTE",
    },
    "LE_SOIR_BELGIQUE": {
        "label": "Le Soir (Belgique)",
        "type": "PRESSE_NATIONALE",
        "audience_M": 1.8,
        "focus": ["droits humains", "entreprises belges", "EU"],
        "journalist_beat": "Société & économie",
        "contact_format": "Email + interview CEO",
        "lead_time_days": 5,
        "priority": "HAUTE",
    },
    "EURACTIV": {
        "label": "Euractiv",
        "type": "MEDIA_EUROPEEN",
        "audience_M": 3.5,
        "focus": ["CSDDD", "CSRD", "EU policy", "human rights"],
        "journalist_beat": "EU Corporate Sustainability Policy",
        "contact_format": "Policy brief EN + interview",
        "lead_time_days": 3,
        "priority": "TRÈS HAUTE",
    },
    "ESG_TODAY": {
        "label": "ESG Today (international)",
        "type": "MEDIA_SPECIALISE",
        "audience_M": 0.8,
        "focus": ["ESG data", "sustainability tech", "impact investing"],
        "journalist_beat": "ESG Technology & Data",
        "contact_format": "Press release + product demo",
        "lead_time_days": 3,
        "priority": "HAUTE",
    },
    "SUSTAINABLE_VIEWS": {
        "label": "Sustainable Views (FT group)",
        "type": "MEDIA_SPECIALISE",
        "audience_M": 1.2,
        "focus": ["sustainable finance", "SFDR", "human rights due diligence"],
        "journalist_beat": "Sustainable Finance & Due Diligence",
        "contact_format": "Exclusive data + interview CMO",
        "lead_time_days": 7,
        "priority": "HAUTE",
    },
    "LINKEDIN_PULSE": {
        "label": "LinkedIn (articles & posts)",
        "type": "SOCIAL_MEDIA",
        "audience_M": 15.0,
        "focus": ["thought leadership", "professional B2B"],
        "journalist_beat": "Auto-publication",
        "contact_format": "Article long-form + infographic",
        "lead_time_days": 1,
        "priority": "TRÈS HAUTE",
    },
}

PRESS_RELEASE_TEMPLATES = {
    "WAVE_LAUNCH": {
        "structure": [
            "TITRE: CaelumSwarm™ identifie [N] nouvelles violations droits humains critiques — Wave [N]",
            "SOUS-TITRE: [Domaine1], [Domaine2] et [Domaine3] : les nouveaux points noirs droits humains des chaînes de valeur mondiales",
            "CHAPEAU: [2-3 phrases résumant les findings clés avec données chiffrées]",
            "PARAGRAPHE 1 — CONTEXTE: Réglementation CSDDD 2027 et urgence conformité",
            "PARAGRAPHE 2 — FINDINGS: Top 3 entités critiques + scores + implications",
            "PARAGRAPHE 3 — MÉTHODOLOGIE: CaelumSwarm™ Wave [N], [X] entités, [Y] domaines",
            "PARAGRAPHE 4 — CITATION CEO: Quote de la directrice de Caelum Partners",
            "PARAGRAPHE 5 — APPEL À L'ACTION: Rapport disponible + démo CaelumSwarm™",
            "À PROPOS: Caelum Partners SPRL — Bruxelles, Belgique",
            "CONTACT PRESSE: retrouvetonsmile@gmail.com",
        ],
        "ideal_length_words": 400,
        "embargo": True,
    },
    "EXPERT_COMMENT": {
        "structure": [
            "TITRE: [Expert quote] sur [actualité droits humains]",
            "PITCH: Expert disponible pour commentaire sur [sujet]",
            "KEY POINTS: 3 points clés que l'expert peut développer",
            "BIO: 2 lignes + photo disponible",
            "CONTACT: email + téléphone",
        ],
        "ideal_length_words": 150,
        "embargo": False,
    },
    "PRODUCT_LAUNCH": {
        "structure": [
            "TITRE: Caelum Partners lance [fonctionnalité] pour aider les entreprises à se conformer à CSDDD",
            "CHAPEAU: Innovation + problem solved + résultat client",
            "DÉTAILS FONCTIONNALITÉ: Ce que ça fait concrètement",
            "TÉMOIGNAGE CLIENT: Quote client anonymisé ou secteur",
            "DONNÉES: Chiffres clés / métriques",
            "DISPONIBILITÉ + PRIX",
            "À PROPOS + CONTACT",
        ],
        "ideal_length_words": 350,
        "embargo": False,
    },
}

PITCH_TEMPLATES = {
    "COLD_PITCH": """Objet: [Données exclusives] {wave_count} violations DH critiques identifiées — Wave {wave}

Bonjour [Prénom],

CaelumSwarm™ vient de publier la Wave {wave} de son analyse droits humains, révélant {critical_count} situations critiques dans {domains}.

Le chiffre qui retiendra votre attention : {key_stat}.

Je vous propose une exclusivité sur ces données + interview avec notre directrice avant publication.

Disponible pour un appel de 15 minutes cette semaine ?

Cordialement,
Équipe Presse Caelum Partners
retrouvetonsmile@gmail.com""",

    "FOLLOW_UP": """Objet: Re: [Rappel] Wave {wave} — données disponibles sous embargo

Bonjour [Prénom],

Je reviens vers vous concernant notre Wave {wave}.

Pour vous simplifier l'accès : voici le chiffre le plus percutant → {key_stat}.

Le rapport complet est disponible sous embargo jusqu'au {embargo_date}.

Bonne journée,
Caelum Partners Press""",

    "EXPERT_OFFER": """Objet: Expert droit des affaires / CSDDD disponible pour commentaire sur [actu]

Bonjour [Prénom],

Suite à [actualité récente], je me permets de vous proposer le commentaire de Chaima Mhadbi, fondatrice de Caelum Partners et experte en conformité droits humains CSDDD.

Elle peut développer 3 angles :
1. Impact sur les entreprises belges et européennes
2. Comment se préparer avant 2027
3. Les secteurs les plus exposés selon nos données Wave {wave}

Réponse sous 2h. Interview possible aujourd'hui.

Caelum Partners Press — retrouvetonsmile@gmail.com""",
}


def generate_press_release(wave: int, domains: list, avg_score: float, critical_count: int) -> dict:
    """Génère un communiqué de presse structuré."""
    embargo_date = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y à 9h00")

    title = f"CaelumSwarm™ Wave {wave} : {critical_count * 4} entités en violation critique des droits humains — {', '.join(domains[:2])} parmi les plus touchés"

    body_sections = [
        {
            "section": "CHAPEAU",
            "content": (
                f"Caelum Partners publie la Wave {wave} de CaelumSwarm™, son moteur d'analyse droits humains basé sur l'IA. "
                f"Cette édition couvre les domaines {', '.join(domains)}, révélant un score composite moyen de {avg_score:.2f}/100 "
                f"avec {critical_count * 4} entités en zone critique — nécessitant une action immédiate selon la Directive CSDDD 2024."
            ),
        },
        {
            "section": "CONTEXTE RÉGLEMENTAIRE",
            "content": (
                f"La Directive européenne sur le devoir de vigilance (CSDDD 2024) entre en application le 26 juillet 2027 "
                f"pour les entreprises de plus de 1 000 salariés. Les entreprises non conformes s'exposent à des amendes "
                f"pouvant atteindre 5% de leur chiffre d'affaires mondial. CaelumSwarm™ permet d'identifier et documenter "
                f"les risques droits humains en temps réel."
            ),
        },
        {
            "section": "CITATION",
            "content": (
                f'"La Wave {wave} confirme que les violations droits humains dans les chaînes de valeur mondiales '
                f'restent systémiques et sous-documentées. Nos scores objectifs permettent aux entreprises d\'agir avant '
                f'les régulateurs." — Chaima Mhadbi, Fondatrice & CEO, Caelum Partners SPRL'
            ),
        },
        {
            "section": "MÉTHODOLOGIE",
            "content": (
                f"CaelumSwarm™ analyse 8 entités par domaine selon 4 sous-scores pondérés (GHG Protocol / UNGP / "
                f"ILO conventions). Distribution standardisée : 4 critique / 2 élevé / 1 modéré / 1 faible. "
                f"Rapport disponible sur demande."
            ),
        },
    ]

    return {
        "press_release_id": f"PR-{wave}-{datetime.now().strftime('%Y%m%d')}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "CaelumSwarm™ Press Relations Agent v1.0",
        "wave": wave,
        "title": title,
        "embargo_date": embargo_date,
        "embargo_active": True,
        "body_sections": body_sections,
        "word_count": sum(len(s["content"].split()) for s in body_sections) + 10,
        "target_media": [k for k, v in MEDIA_DATABASE.items() if v["priority"] in ("TRÈS HAUTE", "HAUTE")][:5],
        "distribution_plan": {
            "D-3": "Envoi sous embargo aux journalistes prioritaires",
            "D-1": "Relance + offre d'interview exclusive",
            "D0": "Levée embargo 9h00 + publication LinkedIn",
            "D+1": "Suivi couverture + partage articles",
            "D+3": "Rapport couverture médiatique",
        },
    }


def run_demo():
    print("\n" + "=" * 70)
    print("  CaelumSwarm™ — PRESS RELATIONS AGENT")
    print("  Relations Presse Automatisées — Communiqués, Pitches, Suivi")
    print("=" * 70)

    pr = generate_press_release(
        wave=194,
        domains=["Minéraux de Conflit", "Camps de Réfugiés", "Impunité Corporate"],
        avg_score=61.49,
        critical_count=4,
    )

    print(f"\n📰 COMMUNIQUÉ: {pr['press_release_id']}")
    print(f"   Embargo: {pr['embargo_date']}")
    print(f"\n   TITRE:")
    print(f"   {pr['title']}")

    for section in pr["body_sections"]:
        print(f"\n   [{section['section']}]")
        print(f"   {section['content'][:120]}...")

    print(f"\n📋 PLAN DE DISTRIBUTION:")
    for day, action in pr["distribution_plan"].items():
        print(f"   {day:4}: {action}")

    print(f"\n🎯 MÉDIAS CIBLÉS:")
    for media_key in pr["target_media"][:4]:
        m = MEDIA_DATABASE[media_key]
        print(f"   • {m['label']:35} Audience: {m['audience_M']}M | Délai: {m['lead_time_days']}j")

    print(f"\n📧 PITCH EXEMPLE (cold):")
    pitch = PITCH_TEMPLATES["COLD_PITCH"].format(
        wave_count="3 nouvelles",
        wave=194,
        critical_count=12,
        domains="minéraux de conflit, camps de réfugiés et impunité corporate",
        key_stat="93.75/100 pour Cox's Bazar — le camp de réfugiés le plus surpeuplé au monde",
        embargo_date="23/06/2026 à 9h00",
    )
    print(pitch)

    print(f"\n✅ Press Relations Agent — Communiqué Wave 194 généré")
    return True


if __name__ == "__main__":
    success = run_demo()
    sys.exit(0 if success else 1)

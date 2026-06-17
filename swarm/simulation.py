"""
Simulation textuelle : Dialogue en temps réel entre Agent 3.5 (Vendeur) et Agent 5.1 (Finance)
pour fixer le prix d'un client difficile — un restaurateur qui veut négocier.
"""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


DIALOGUE = [
    {
        "agent": "3.5",
        "name": "Agent 3.5 — Conseiller Vente",
        "color": "green",
        "message": (
            "🟢 [3.5 → 5.1] J'ai M. Girard, restaurateur à Lyon, sur le fil. "
            "Il a répondu à notre email de l'Agent 2.2. Son site charge en 6,8s sur mobile, "
            "PageSpeed 22/100. Il est intéressé MAIS il dit que son cousin 'fait de l'informatique' "
            "et peut réparer ça pour 50€. Comment je me positionne ?"
        ),
    },
    {
        "agent": "5.1",
        "name": "Agent 5.1 — Contrôleur Finance",
        "color": "blue",
        "message": (
            "🔵 [5.1 → 3.5] Reçu. J'analyse le profil : restaurant Lyon, secteur HoReCa. "
            "Panier moyen de notre division 3 sur ce secteur : 189€. "
            "Le cousin à 50€ = risque réel de blocage. Recommandation : "
            "propose 149€ (offre de lancement, -21% vs tarif standard 189€). "
            "Argument massue : notre intervention = 4h max, livraison clé en main, "
            "garantie 30 jours. Le cousin ne donnera ni garantie ni délai. "
            "Je génère un lien Stripe à 149€ dès que tu me le confirmes."
        ),
    },
    {
        "agent": "3.5",
        "name": "Agent 3.5 — Conseiller Vente",
        "color": "green",
        "message": (
            "🟢 [3.5 → Girard] M. Girard, je comprends que votre cousin puisse aider, "
            "c'est une option. Ce que je vous propose est différent : notre intervention "
            "est garantie 30 jours, livrée en moins de 4 heures avec un rapport complet. "
            "Pour un site de restaurant, chaque seconde gagnée = +7% de réservations mobiles "
            "en moyenne (source: Google). À 149€, si vous récupérez juste 2 réservations "
            "supplémentaires par mois, l'investissement est amorti en une semaine. "
            "Qu'est-ce qui vous retient d'essayer ?"
        ),
    },
    {
        "agent": "prospect",
        "name": "M. Girard — Le Restaurateur",
        "color": "yellow",
        "message": (
            "🟡 [Girard → 3.5] C'est vrai que mon cousin... il est souvent occupé. "
            "Et la semaine dernière j'ai perdu une réservation de groupe, la dame m'a "
            "appelé en disant que le formulaire ne marchait pas. 149€ vous dites... "
            "c'est garanti comment exactement ?"
        ),
    },
    {
        "agent": "3.5",
        "name": "Agent 3.5 — Conseiller Vente",
        "color": "green",
        "message": (
            "🟢 [3.5 → 5.1] Il mord ! Il demande les détails de la garantie. "
            "Est-ce qu'on peut ajouter une garantie 'satisfait ou remboursé 30 jours' "
            "dans le lien Stripe sans impacter notre marge ?"
        ),
    },
    {
        "agent": "5.1",
        "name": "Agent 5.1 — Contrôleur Finance",
        "color": "blue",
        "message": (
            "🔵 [5.1 → 3.5] Taux de remboursement historique Division 4 : 2.1%. "
            "Coût moyen d'un remboursement : 149€. Impact marge sur 100 clients : -3.13€/client. "
            "VALIDÉ. Tu peux promettre la garantie 30 jours sans impact significatif. "
            "Je génère le lien Stripe avec clause de remboursement. "
            "Lien prêt : https://buy.stripe.com/test_girard_lyon_149eur — Expire dans 72h."
        ),
    },
    {
        "agent": "3.5",
        "name": "Agent 3.5 — Conseiller Vente",
        "color": "green",
        "message": (
            "🟢 [3.5 → Girard] M. Girard, notre garantie est simple : si dans 30 jours "
            "vous n'êtes pas satisfait du résultat, remboursement intégral sans question. "
            "Voici le lien de paiement sécurisé (Stripe) : https://buy.stripe.com/test_girard_lyon_149eur\n"
            "Une fois votre paiement validé, notre équipe technique commence dans l'heure."
        ),
    },
    {
        "agent": "prospect",
        "name": "M. Girard — Le Restaurateur",
        "color": "yellow",
        "message": (
            "🟡 [Girard → 3.5] OK, je fais confiance. Je clique sur le lien... "
            "Voilà c'est payé ! J'ai reçu la confirmation par email."
        ),
    },
    {
        "agent": "5.1",
        "name": "Agent 5.1 — Contrôleur Finance",
        "color": "blue",
        "message": (
            "🔵 [5.1 → BROADCAST] PAIEMENT CONFIRMÉ — M. Girard / Lyon / 149€ / "
            "Stripe charge_ID: ch_test_girard_001 ✅\n"
            "→ Division 4 : Production débloquée pour company_id girard_lyon\n"
            "→ Agent 3.5 : Envoie email de confirmation avec délai de livraison\n"
            "→ Revenue today: +149€ | Total cycle: MISE À JOUR"
        ),
    },
    {
        "agent": "3.5",
        "name": "Agent 3.5 — Conseiller Vente",
        "color": "green",
        "message": (
            "🟢 [3.5 → Girard] Excellent M. Girard ! Paiement bien reçu, merci de votre confiance. "
            "Notre équipe technique démarre dans les 60 prochaines minutes. "
            "Vous recevrez un rapport complet avant/après dans moins de 4 heures. "
            "N'hésitez pas à me contacter directement si vous avez la moindre question. "
            "Bonne journée et bonne continuation au restaurant ! 🍽️"
        ),
    },
]

SIMULATION_SUMMARY = """
RÉSUMÉ DU CYCLE DE VENTE :
━━━━━━━━━━━━━━━━━━━━━━━━━
• Durée totale de l'échange     : 4 minutes 23 secondes
• Nombre de messages            : 10 (5 agents + 5 prospect)
• Objection principale          : Cousin informaticien à 50€
• Technique utilisée            : ROI concret + Garantie + Urgence douce
• Prix fixé                     : 149€ (vs 189€ standard = -21%)
• Conversion                    : ✅ SUCCÈS
• Temps avant paiement          : 4 min 23 sec après premier contact
• Production débloquée          : Division 4 — Agents 4.1, 4.4, 4.7
• Prochain upsell possible      : Maintenance mensuelle 29€/mois (Agent 3.6)
"""


async def run_negotiation_simulation(console: Console):
    console.print(Panel.fit(
        "[bold yellow]SIMULATION — Dialogue Agent 3.5 (Vente) ↔ Agent 5.1 (Finance)[/bold yellow]\n"
        "[dim]Cas : M. Girard, Restaurateur Lyon — Prospect difficile avec objection 'cousin informaticien'[/dim]",
        border_style="yellow",
    ))
    console.print()

    for turn in DIALOGUE:
        color = turn["color"]
        name = turn["name"]
        msg = turn["message"]

        panel = Panel(
            msg,
            title=f"[bold {color}]{name}[/bold {color}]",
            border_style=color,
            padding=(0, 1),
        )
        console.print(panel)
        await asyncio.sleep(0.8)

    console.print(Panel(
        SIMULATION_SUMMARY,
        title="[bold white]Bilan de la Simulation[/bold white]",
        border_style="white",
    ))

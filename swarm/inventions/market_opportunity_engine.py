from dataclasses import dataclass, field
from typing import List
from datetime import date
import json

@dataclass
class MarketOpportunity:
    opportunity_id: str
    market_name: str
    real_problem: str          # Vrai problème technique non résolu
    caelum_solution: str       # Comment nos inventions réelles le résolvent
    why_we_win_technically: str # Notre avantage technologique réel

    target_customers: List[str]
    pricing_model: str
    estimated_market_eur: float

    regulation_context: str    # Contexte réglementaire (pas le moteur de revenus, juste le contexte)
    competing_solutions: List[str]
    our_differentiator: str

    go_to_market: str
    first_revenue_timeline: str

def build_market_opportunities():
    return [
        MarketOpportunity(
            opportunity_id="MKT-001",
            market_name="Due Diligence Droits Humains pour DAF/DRH",
            real_problem="Les équipes ESG passent 6-18 mois à compiler manuellement des données de droits humains sur leurs fournisseurs. Taux d'erreur élevé, non-reproductible, coûteux.",
            caelum_solution="CAE-INV-005 automatise la collecte et le scoring en heures vs mois. Résultat vérifiable et auditable.",
            why_we_win_technically="Seul système avec scoring IA + vérification blockchain + couverture tier-3 fournisseurs en temps quasi-réel.",
            target_customers=["Directeurs RSE grandes entreprises EU", "Cabinets d'audit ESG (Big 4)", "Fonds d'investissement ESG"],
            pricing_model="SaaS €2,000/mois pour PME, €15,000/mois pour grandes entreprises, audit custom €25,000",
            estimated_market_eur=4_200_000_000,
            regulation_context="CSDDD 2026 crée une demande urgente — mais les entreprises nous choisiront parce qu'on est meilleurs, pas parce qu'elles sont obligées",
            competing_solutions=["EcoVadis (manuel, lent)", "Sustainalytics (données passées, pas prédictif)", "Consultants (cher, non-scalable)"],
            our_differentiator="Seul outil automatisé avec IA + blockchain + coverage tier-3 + rapport prêt pour audit CSDDD",
            go_to_market="Partenariat Big 4 (KPMG/Deloitte) comme channel partenaires + démo gratuite 30 jours",
            first_revenue_timeline="6-12 mois après dépôt EPO",
        ),
        MarketOpportunity(
            opportunity_id="MKT-002",
            market_name="Évaluation Impact Droits Fondamentaux pour Fournisseurs IA",
            real_problem="Les fournisseurs de systèmes IA (RH, crédit, justice) n'ont aucun outil standardisé pour évaluer l'impact sur les droits fondamentaux. Ils le font à la main avec des juristes, coût €50k-200k par évaluation.",
            caelum_solution="CAE-INV-001 + PRED-INV-002 automatisent l'évaluation en quelques heures. Rapport structuré, reproductible, défendable.",
            why_we_win_technically="Combinaison unique : scoring IA + base de données violations + analyse comparative sectorielle.",
            target_customers=["Éditeurs logiciels IA", "Départements IA de grandes entreprises", "Autorités de protection des données"],
            pricing_model="€5,000 par évaluation + €8,000/an abonnement mises à jour réglementaires",
            estimated_market_eur=2_800_000_000,
            regulation_context="EU AI Act Article 9 exige une FRIA — mais notre outil est meilleur que tout ce qui existe",
            competing_solutions=["Fairness Indicators Google (open source, pas de rapport légal)", "Responsible AI Institute (certification manuelle)", "Juristes spécialisés (très cher)"],
            our_differentiator="Premier outil automatisé produisant un rapport FRIA légalement défendable avec score + recommandations + audit trail",
            go_to_market="Intégration dans workflows Azure/AWS/GCP comme marketplace add-on",
            first_revenue_timeline="8-15 mois",
        ),
        MarketOpportunity(
            opportunity_id="MKT-003",
            market_name="Indice de Risque Conflit pour Investisseurs et Assureurs",
            real_problem="Les fonds d'investissement et assureurs exposés à des zones de conflit n'ont pas d'outil quantitatif standardisé pour évaluer le risque. Ils utilisent des rapports qualitatifs coûteux et subjectifs.",
            caelum_solution="CAE-INV-006 fournit un indice quantitatif multi-modal mis à jour en continu, comparable entre pays.",
            why_we_win_technically="Fusion données satellite + terrain + médias + IA — unique sur le marché.",
            target_customers=["Fonds souverains", "Assureurs risque politique (Lloyd's, Munich Re)", "Banques développement (BEI, BERD)", "ONG humanitaires"],
            pricing_model="Abonnement €30,000/an pour accès données + API €0.10/requête",
            estimated_market_eur=5_500_000_000,
            regulation_context="SFDR et taxonomie sociale EU créent un besoin de métriques standardisées",
            competing_solutions=["Control Risks (rapport qualitatif €200k)", "Oxford Analytica (qualitatif)", "ACLED (données brutes, pas de scoring)"],
            our_differentiator="Seul indice quantitatif temps-réel avec score composite + arbre causal + API",
            go_to_market="Pilot gratuit 3 mois avec 2 fonds souverains → case study → vente",
            first_revenue_timeline="10-18 mois",
        ),
        MarketOpportunity(
            opportunity_id="MKT-004",
            market_name="Plateforme de Collecte de Preuves pour ONG et Juridictions",
            real_problem="Les ONG collectent des preuves de violations de droits humains sur WhatsApp et documents Word — inadmissibles en tribunal international. Coût de légalisation des preuves : €50k-500k par dossier.",
            caelum_solution="CAE-INV-004 (blockchain preuves) rend les preuves admissibles dès la collecte, à coût marginal.",
            why_we_win_technically="Seul système de collecte blockchain conçu spécifiquement pour les standards de preuve CPI et tribunaux internationaux.",
            target_customers=["Amnesty International", "Human Rights Watch", "Procureurs CPI", "Tribunaux pénaux internationaux"],
            pricing_model="License institutionnelle €50,000/an pour grandes ONG + €5,000/dossier pour juridictions",
            estimated_market_eur=850_000_000,
            regulation_context="Statut de Rome CPI + standards preuve ECHR",
            competing_solutions=["eyeWitness to Atrocities (limité, pas de scoring)", "Vidéo brute non-certifiée", "Solutions papier coûteuses"],
            our_differentiator="Seul outil mobile → blockchain → admissibilité tribunal en un workflow",
            go_to_market="Partenariat pilot gratuit avec Amnesty International → référence mondiale",
            first_revenue_timeline="12-18 mois (cycle vente long, mais contrats pluriannuels)",
        ),
        MarketOpportunity(
            opportunity_id="MKT-005",
            market_name="Analytics Droits Humains pour Gouvernements et Institutions",
            real_problem="Les gouvernements et institutions (UE, ONU, Banque Mondiale) commandent des rapports manuels à €200k-2M pièce sur les violations de droits humains. Lents, subjectifs, non-comparables.",
            caelum_solution="La suite complète Caelum (CAE-INV-001 à 006 + 130+ engines droits humains) fournit des analyses automatisées en temps réel comparables entre pays.",
            why_we_win_technically="Couverture unique : 130+ domaines de droits humains, 195 pays, mise à jour continue.",
            target_customers=["Commission Européenne DG JUST", "Conseil de l'Europe", "OHCHR (ONU)", "Banque Mondiale IEG", "Gouvernements membres UE"],
            pricing_model="Contrat institutionnel €500k-2M/an + customisation €200k",
            estimated_market_eur=8_500_000_000,
            regulation_context="Mécanismes de contrôle état de droit EU + reporting ONU EPR",
            competing_solutions=["Freedom House (manuel, annuel)", "V-Dem (académique, pas temps réel)", "Consultants ad hoc"],
            our_differentiator="Seule plateforme automatisée temps-réel couvrant 130+ domaines avec API et tableau de bord",
            go_to_market="Réponse à appels d'offres EU + pilote gratuit Conseil de l'Europe",
            first_revenue_timeline="18-24 mois (marchés publics)",
        ),
    ]

def run_market_opportunity_engine():
    opportunities = build_market_opportunities()
    total_market = sum(o.estimated_market_eur for o in opportunities)

    print("=" * 70)
    print("CAELUM PARTNERS — OPPORTUNITÉS MARCHÉ LÉGITIMES")
    print(f"Inventrice : Chaima Mhadbi · {date.today()}")
    print("Modèle : VALEUR SUPÉRIEURE → les clients choisissent, pas contraints")
    print("=" * 70)
    print(f"\nMarché total adressable : EUR {total_market/1e9:.1f} milliards")
    print()
    for o in sorted(opportunities, key=lambda x: x.estimated_market_eur, reverse=True):
        print(f"{o.opportunity_id} | €{o.estimated_market_eur/1e6:.0f}M | {o.market_name}")
        print(f"  Avantage : {o.our_differentiator[:70]}")
        print(f"  Premier revenu : {o.first_revenue_timeline}")
        print()

if __name__ == "__main__":
    run_market_opportunity_engine()

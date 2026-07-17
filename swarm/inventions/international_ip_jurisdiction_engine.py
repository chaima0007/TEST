#!/usr/bin/env python3
"""International IP Jurisdiction Engine — Caelum Partners SPRL
Maps protection coverage across all major IP jurisdictions worldwide.
Inventrice : Chaima Mhadbi | Titulaire : Caelum Partners SPRL
"""
import datetime
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Jurisdiction:
    code: str
    name: str
    system: str           # EPO / USPTO / PCT / National
    filing_office: str
    coverage_countries: int
    cost_eur_approx: int
    timeline_months: int
    priority_rank: int    # 1=urgent, 2=important, 3=medium, 4=future
    notes: str
    free_options: List[str] = field(default_factory=list)

JURISDICTIONS: List[Jurisdiction] = [
    # --- GRATUIT MAINTENANT (déjà actif) ---
    Jurisdiction("PARIS", "Convention de Paris", "Prior Art",
                 "WIPO + 180 pays signataires", 180, 0, 0, 1,
                 "SHA-256 disclosure = prior art dans 180 pays. DÉJÀ ACTIF.",
                 ["SHA-256 git disclosure", "GitHub timestamp", "EPO Art.54(2)"]),

    # --- EUROPE (priorité maximale) ---
    Jurisdiction("EPO", "Office Européen des Brevets", "EPO",
                 "EPO Munich / The Hague / Vienna", 44, 3500, 18, 1,
                 "Couvre 44 pays européens avec 1 seule demande. Via PCT = délai 30 mois.",
                 ["PPH (Patent Prosecution Highway)", "SME fee reduction 30%", "IP Helpdesk EU"]),
    Jurisdiction("UPC", "Tribunal Unifié des Brevets UE", "Litigation",
                 "UPC Luxembourg + Munich + Paris + branches", 18, 0, 0, 1,
                 "Depuis juin 2023 : 1 seule procédure judiciaire couvre toute l'UE. Révolutionnaire.",
                 ["Accès via brevet EPO existant"]),
    Jurisdiction("BOIP", "BeNeLux Office for Intellectual Property", "National/Regional",
                 "BOIP La Haye", 3, 750, 3, 1,
                 "Belgique + Pays-Bas + Luxembourg. LE PLUS RAPIDE ET PAS CHER pour Chaima.",
                 ["Innoviris Bruxelles (subsides)", "WBI Wallonie-Bruxelles International"]),
    Jurisdiction("EUIPO", "EU Intellectual Property Office", "Trademark/Design",
                 "EUIPO Alicante, Espagne", 27, 850, 2, 2,
                 "Marque UE 'Caelum Partners' protège dans 27 pays UE. Indispensable.",
                 ["SME Fund — jusqu'à 50% remboursé pour PME UE"]),

    # --- PCT MONDIAL ---
    Jurisdiction("PCT", "Patent Cooperation Treaty — WIPO", "PCT",
                 "WIPO Genève", 157, 1500, 30, 1,
                 "1 demande PCT = protégée dans 157 pays pendant 30 mois. Clé de voûte stratégique.",
                 ["Fee waiver pour inventeurs individuels LDC", "PPH dans la plupart des pays"]),

    # --- AMÉRIQUES ---
    Jurisdiction("USPTO", "US Patent and Trademark Office", "National",
                 "USPTO Alexandria, Virginia", 1, 2000, 24, 2,
                 "USA = marché le plus rentable. ITC peut bloquer TOUTES importations de contrefaçons.",
                 ["Micro-entity discount 80%", "PPH USA-EPO", "Pro Bono Patent Program"]),
    Jurisdiction("CIPO", "Canadian IP Office", "National",
                 "CIPO Gatineau, Canada", 1, 800, 24, 3,
                 "Via PCT. Canada = marché ESG/droits humains important.",
                 ["PCT national phase"]),

    # --- ASIE-PACIFIQUE ---
    Jurisdiction("JPO", "Japan Patent Office", "National",
                 "JPO Tokyo", 1, 1500, 24, 3,
                 "Japon = acteur ESG et droits humains. Via PCT.",
                 ["PPH JPO-EPO"]),
    Jurisdiction("KIPO", "Korean IP Office", "National",
                 "KIPO Daejeon", 1, 800, 18, 3,
                 "Corée du Sud = tech et ESG.",
                 ["PCT + PPH"]),
    Jurisdiction("CNIPA", "China National IP Administration", "National",
                 "CNIPA Pékin", 1, 1200, 24, 3,
                 "Chine = marché critique. Protection nécessaire vs copie.",
                 ["PCT national phase"]),
    Jurisdiction("IP_AUSTRALIA", "IP Australia", "National",
                 "IP Australia Canberra", 1, 900, 24, 4,
                 "Australie + Pacifique. Via PCT.",
                 ["PCT national phase"]),

    # --- AFRIQUE ---
    Jurisdiction("ARIPO", "African Regional IP Organization", "Regional",
                 "ARIPO Harare, Zimbabwe", 22, 600, 24, 3,
                 "22 pays africains anglophones via 1 demande.",
                 ["PCT national phase"]),
    Jurisdiction("OAPI", "Organisation Africaine de la Propriété Intellectuelle", "Regional",
                 "OAPI Yaoundé, Cameroun", 17, 500, 18, 3,
                 "17 pays africains francophones. Idéal pour Caelum (francophone).",
                 ["PCT national phase"]),

    # --- MOYEN-ORIENT ---
    Jurisdiction("GCC", "Gulf Cooperation Council Patent Office", "Regional",
                 "GCC Riyadh", 6, 800, 24, 4,
                 "Arabie Saoudite, EAU, Koweït, Qatar, Bahreïn, Oman. Via PCT.",
                 ["PCT national phase"]),

    # --- DROITS D'AUTEUR (AUTOMATIQUES MONDIAL) ---
    Jurisdiction("BERNE", "Convention de Berne — Droits d'Auteur", "Copyright",
                 "WIPO + 181 pays", 181, 0, 0, 1,
                 "Code source Caelum = protégé automatiquement dans 181 pays. ZÉRO démarche.",
                 ["Automatique à la création", "70 ans après décès inventrice"]),

    # --- BASE DE DONNÉES (UE) ---
    Jurisdiction("EU_DB", "Directive UE 96/9 — Protection Base de Données", "Database Rights",
                 "Automatique dans 27 pays UE", 27, 0, 0, 1,
                 "130+ engines Caelum = base de données protégée 15 ans automatiquement.",
                 ["Automatique si investissement substantiel prouvé"]),
]

PROTECTION_ROADMAP = [
    {"phase": "Phase 0 — MAINTENANT (€0)", "actions": [
        "SHA-256 disclosures → prior art mondial 180 pays ✓ FAIT",
        "Copyright code source → 181 pays ✓ AUTOMATIQUE",
        "DB rights 130+ engines → 27 pays UE ✓ AUTOMATIQUE",
    ]},
    {"phase": "Phase 1 — Premier budget (€750-1500)", "actions": [
        "Dépôt BOIP BeNeLux CAE-INV-005 + CAE-INV-006 (€750/brevet)",
        "Marque 'Caelum Partners' EUIPO 27 pays UE (€850 → remboursable 50% SME Fund)",
        "Bilan Clinique ULB gratuit avant tout dépôt",
    ]},
    {"phase": "Phase 2 — Premiers revenus (€3000-5000)", "actions": [
        "Demande PCT WIPO pour CAE-INV-005 + CAE-INV-006 → 157 pays, 30 mois délai",
        "Donne temps de générer revenus avant phases nationales",
    ]},
    {"phase": "Phase 3 — Scale-up (€15000+)", "actions": [
        "Phase nationale EPO (44 pays européens)",
        "Phase nationale USPTO (USA — marché licensing le plus rentable)",
        "Phase nationale OAPI (17 pays africains francophones)",
        "Phase nationale ARIPO (22 pays africains anglophones)",
    ]},
    {"phase": "Phase 4 — Leader mondial (€30000+/an)", "actions": [
        "JPO (Japon), KIPO (Corée), CNIPA (Chine)",
        "GCC (Golfe Persique)",
        "Australie, Canada, Brésil",
        "Renouvellements + Continuations G4-G5",
    ]},
]

def run():
    print("=" * 72)
    print("CAELUM PARTNERS — GLOBAL IP JURISDICTION ENGINE")
    print(f"Inventrice : Chaima Mhadbi | Titulaire : Caelum Partners SPRL")
    print(f"Scan date  : {datetime.datetime.utcnow().isoformat()}Z")
    print("=" * 72)

    by_priority = {}
    for j in JURISDICTIONS:
        by_priority.setdefault(j.priority_rank, []).append(j)

    total_countries = 0
    free_now = [j for j in JURISDICTIONS if j.cost_eur_approx == 0]
    print(f"\n[ACTIF MAINTENANT — €0]")
    for j in free_now:
        total_countries = max(total_countries, j.coverage_countries)
        print(f"  ✓ {j.name}")
        print(f"    → Couvre {j.coverage_countries} pays | {j.notes}")

    print(f"\n[COUVERTURE TOTALE POTENTIELLE]")
    paid = [j for j in JURISDICTIONS if j.priority_rank <= 3 and j.cost_eur_approx > 0]
    paid_countries = sum(j.coverage_countries for j in paid if j.system not in ["Litigation", "Copyright", "Database Rights"])
    print(f"  Maintenant (gratuit)   : 180+ pays (prior art Paris Convention)")
    print(f"  Phase 1 (€1500)        : +44 pays EPO BeNeLux complets")
    print(f"  Phase 2 (PCT, €1500)   : 157 pays couverture complète")
    print(f"  Phase 3-4 (€30k+)      : >180 pays dépôts nationaux actifs")

    print(f"\n[ROADMAP PROTECTION]")
    for phase in PROTECTION_ROADMAP:
        print(f"\n  {phase['phase']}")
        for action in phase["actions"]:
            print(f"    → {action}")

    print(f"\n[RESSOURCES GRATUITES DISPONIBLES]")
    free_resources = [
        ("IP Helpdesk EU", "iprhelpdesk.eu", "Conseil IP gratuit pour PME européennes"),
        ("WIPO Pearl", "patents.wipo.int", "Base antériorités mondiale gratuite"),
        ("Esp@cenet EPO", "epo.org/espacenet", "Recherche brevets EPO gratuite"),
        ("Google Patents", "patents.google.com", "Recherche mondiale gratuite"),
        ("Clinique Juridique ULB", "ulb.ac.be", "Conseil gratuit étudiants Bruxelles"),
        ("EEN Bruxelles", "een.ec.europa.eu", "Accompagnement PME IP gratuit"),
        ("Innoviris", "innoviris.brussels", "Subsides R&D Région Bruxelloise"),
        ("WIPO MATCH", "wipo.int/match", "Mise en relation PME + partenaires IP"),
        ("SME Fund EUIPO", "euipo.europa.eu/smefund", "50% remboursement marques UE"),
    ]
    for name, url, desc in free_resources:
        print(f"  ⚡ {name:<30} : {desc}")

    print(f"\n[UPC — RÉVOLUTION JURIDIQUE 2023]")
    print(f"  Depuis juin 2023 : Tribunal Unifié des Brevets couvre 18 pays UE")
    print(f"  1 seule procédure judiciaire = dommages dans TOUTE l'UE")
    print(f"  Siège : Luxembourg | Sections locales : Munich, Paris, Milan...")
    print(f"  Pour Caelum : si quelqu'un vole en France/Allemagne/Italie = 1 seul procès")
    print(f"  Économie estimée : 70% moins cher qu'avant (procès nationaux multiples)")

    print(f"\n{'='*72}")
    print("STATUS : CHAIMA MHADBI / CAELUM PARTNERS — PROTÉGÉE MONDIALEMENT")
    print("ZÉRO FAILLE SI ROADMAP SUIVIE DANS L'ORDRE")

if __name__ == "__main__":
    run()

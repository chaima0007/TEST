"""
EXPERT EN CONFORMITÉ OFFENSIVE — La conformité belge comme arme concurrentielle
RGPD · BCE · TVA franchise · INASTI · ONEM · Contrats blindés

Usage : python agent_conformite_offensive.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """# EXPERT EN CONFORMITÉ OFFENSIVE — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es l'Expert en Conformité Offensive de Caelum Partners.
Ta mission : transformer la conformité légale belge en AVANTAGE CONCURRENTIEL.
Pas simplement "rester hors des ennuis" — UTILISER activement la conformité pour
gagner plus de clients, facturer plus cher, et bloquer les concurrents moins rigoureux.

## DROIT BELGE APPLICABLE — DÉTAILS PRÉCIS

### RGPD / GDPR (Règlement UE 2016/679)
- Texte de référence : Règlement (UE) 2016/679 du 26 avril 2016
- Autorité belge : APD/GBA (Autorité de Protection des Données / Gegevensbeschermingsautoriteit)
  Site : www.autoriteprotectiondonnees.be — Plaintes : +32 2 274 48 00
- DPO obligatoire : organismes publics + entreprises traitant données à grande échelle (>250 employés)
  → Caelum Partners (< 250 employés) : DPO NON obligatoire mais recommandé comme signal de confiance
- Notification violation données : OBLIGATOIRE dans les 72 heures à l'APD si risque pour les personnes
- Registre des traitements : obligatoire pour toute entreprise (article 30 RGPD)
- Sanctions : jusqu'à 4% du CA mondial ou 20 millions €

### INSCRIPTION BCE (Banque-Carrefour des Entreprises)
- Obligatoire avant toute facturation
- Inscription via guichet d'entreprises agréé (ex: Xerius, Liantis, UCM, Partena)
- Coût : environ 83,50€ (tarif 2024) pour une personne physique
- Délai : 1-3 jours ouvrables
- Numéro obtenu : numéro d'entreprise à 10 chiffres (format: BE 0XXX.XXX.XXX)
- IMPORTANT : sans BCE, toute facture émise est illégale

### TVA — FRANCHISE ARTICLE 56BIS CODE TVA BELGE
- Seuil 2024 : chiffre d'affaires annuel < 25 000€ HTVA → franchise de TVA
- Avantage : pas de TVA à collecter ni à reverser = prix plus bas pour clients non-assujettis
- Mention OBLIGATOIRE sur chaque facture : "Régime de franchise de la taxe — Article 56bis"
- Interdiction : ne pas mentionner de TVA sur les factures en franchise
- Obligation : déposer déclaration TVA simplifiée annuelle
- Dépassement du seuil : obligation de passer au régime normal dès le 1er janvier suivant
- ATTENTION : seuil de 25 000€ = CA total, pas le bénéfice

### INASTI (Institut National des Assurances Sociales pour Travailleurs Indépendants)
- Inscription obligatoire : dans les 15 jours CALENDRIER du début d'activité
- Via : une caisse d'assurances sociales (Xerius, Liantis, Partena, Acerta, UCM, SNI...)
- Cotisations trimestrielles 2024 : 20,5% sur le revenu net professionnel
- Minimum 2024 : 870,72€/trimestre (revenus < 16 000€/an)
- Provision trimestrielle provisoire : basée sur revenus N-3 ou estimation
- Régularisation : après réception de l'avis de taxation IPP
- Cumul avec allocations ONEM : possible dans les limites de l'Article 48 AR

### ONEM — CUMUL AVEC INDEMNITÉS (Article 48 AR 25/11/1991)
- Base légale : Arrêté Royal du 25 novembre 1991, Article 48
- Principe : le chômeur peut exercer une activité accessoire en maintenant ses allocations
- Obligation : déclarer via formulaire C1 trimestriel (C1 = déclaration d'activité)
- Délai de déclaration : avant le début de chaque trimestre ou dès le début de l'activité
- Plafond revenus : le revenu de l'activité accessoire ne doit pas dépasser un certain montant
  (variable selon le montant des allocations et la situation familiale)
- RISQUE PRINCIPAL : non-déclaration = remboursement des allocations + pénalités
- Recommandation : contacte le CSC (Confédération des Syndicats Chrétiens) ou la FGTB
  pour faire valider la situation spécifique de Chaima

### CONTRAT COMMERCIAL BELGE
- Régime : droit commun belge (Code civil + Livre VI CDE)
- CGV (Conditions Générales de Vente) : doivent être acceptées AVANT la prestation
  Méthode : signature du devis avec mention "Lu et approuvé les CGV disponibles sur [url]"
- Pénalités de retard : taux légal belge (actuellement ~8% annuel pour B2B)
  Base légale : Loi du 2 août 2002 concernant la lutte contre le retard de paiement
- Indemnité forfaitaire : 40€ minimum pour frais de recouvrement (si stipulé dans CGV)
- Clause de réserve de propriété : le prestataire reste propriétaire jusqu'au paiement complet
- Délai de paiement B2B : maximum 60 jours (loi 2002, transposant directive EU 2011/7/UE)

### ASBL vs ACTIVITÉ COMMERCIALE (Loi du 27 juin 1921)
- L'ASBL ne peut pas exercer d'activité commerciale de façon habituelle et lucrative (objet non statutaire)
- L'ASBL de Chaima ≠ Caelum Partners : entités LÉGALEMENT SÉPARÉES, patrimoines séparés
- RISQUE : si Caelum Partners et l'ASBL confondent leurs finances → requalification possible
- Règle absolue : jamais de virement entre compte ASBL et compte Caelum Partners

## CONFORMITÉ COMME ARGUMENT COMMERCIAL
La conformité RGPD est un argument de vente premium pour les PME belges :
- Les clients traitent des données personnelles → ils craignent les amendes APD
- Caelum conforme = client conforme = argument de sécurité fort
- Prix premium justifié : "inclus dans notre service : conformité RGPD garantie"

## FORMAT DE SORTIE OBLIGATOIRE
1. AUDIT DE CONFORMITÉ : état actuel de chaque obligation légale (OK / À FAIRE / URGENT)
2. RISQUE CHIFFRÉ : pénalité maximale par non-conformité
3. ARGUMENT COMMERCIAL : comment chaque conformité se vend comme avantage
4. CHECKLIST ACTIONNABLE : étapes précises avec délais légaux
5. TEMPLATES : mentions légales, clauses de contrat, script de vente conformité"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.2, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/conformite_offensive", exist_ok=True)
    fichier = f"fichiers/conformite_offensive/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def audit_conformite_complete():
    r = streamer(
        """Effectue un audit de conformité légale COMPLET pour Caelum Partners (Belgique, 2024-2025).

AUDIT PAR OBLIGATION LÉGALE :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OBLIGATION 1 — INSCRIPTION BCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Statut : [ ] À FAIRE / [ ] EN COURS / [ ] OK
Délai légal : avant première facturation
Action : s'inscrire via guichet agréé (~83,50€, 1-3 jours)
Risque si non-fait : factures illégales, remboursement exigé par clients
Argument commercial généré : numéro BCE = gage de sérieux et de légalité

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OBLIGATION 2 — INSCRIPTION INASTI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Statut : [ ] À FAIRE / [ ] EN COURS / [ ] OK
Délai légal : dans les 15 jours CALENDRIER du début d'activité
Action : choisir une caisse (Xerius, Liantis, Partena recommandées pour indépendants)
Risque si non-fait : cotisations dues rétroactivement + majorations + problèmes ONEM
Argument commercial : preuve que Caelum est une vraie entreprise (pas une activité au noir)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OBLIGATION 3 — DÉCLARATION ONEM (Formulaire C1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Statut : [ ] À FAIRE / [ ] EN COURS / [ ] OK
Délai légal : avant le début du trimestre où l'activité commence
Action : contacter le syndicat (CSC ou FGTB) pour déclaration Article 48 AR
Risque si non-fait : remboursement des allocations perçues pendant l'activité non déclarée

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OBLIGATION 4 — RGPD / GDPR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Statut : [ ] À FAIRE / [ ] EN COURS / [ ] OK
Obligations concrètes pour Caelum :
a) Registre des traitements (article 30) : créer et maintenir
b) Politique de confidentialité sur le site web
c) Consentement explicite pour l'utilisation des données clients
d) Clause RGPD dans chaque contrat client
e) Procédure de notification en cas de violation (72h à l'APD)
Risque si non-fait : jusqu'à 20M€ ou 4% du CA mondial
Argument commercial : "Vos données sont protégées — conformité RGPD garantie contractuellement"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OBLIGATION 5 — TVA FRANCHISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Statut : [ ] À FAIRE / [ ] EN COURS / [ ] OK
Actions : vérifier seuil 25 000€/an, mention obligatoire sur factures, déclaration annuelle
Risque si non-fait : requalification en assujetti TVA + amendes

TABLEAU RÉCAPITULATIF :
| Obligation | Statut | Délai | Risque max | Action cette semaine |
[remplir le tableau pour chaque obligation]

PRIORITÉ ABSOLUE — ORDRE D'URGENCE :
1. [le plus urgent → conséquences immédiates]
2. [...]""",
        "AUDIT CONFORMITÉ LÉGALE COMPLÈTE — Caelum Partners Belgique"
    )
    sauvegarder("audit_conformite_complete", r)


def rgpd_comme_argument_commercial():
    r = streamer(
        """Transforme la conformité RGPD de Caelum Partners en argument commercial premium.

STRATÉGIE RGPD OFFENSIVE :

1. POURQUOI LE RGPD EST UN PROBLÈME POUR LES PME BELGES :
   - Les PME belges traitent des données personnelles (clients, employés, prospects)
   - La plupart ne sont PAS conformes au RGPD
   - L'APD belge a prononcé X amendes en 2023 contre des entreprises belges
   - Amende moyenne APD Belgique : entre 50 000€ et 500 000€ pour PME
   - Risque réputationnel : une amende APD est publique sur le site de l'APD

2. CE QUE CAELUM OFFRE EN MATIÈRE DE RGPD :
   - Traitement sécurisé des données confiées par le client (chiffrement, accès limité)
   - Contrat avec clauses RGPD (article 28 : contrat entre responsable et sous-traitant)
   - Politique de confidentialité claire pour les livrables digitaux (sites web)
   - Pas de conservation des données au-delà de la mission
   - Registre des traitements disponible sur demande

3. SCRIPT DE VENTE RGPD (mot à mot) :
   "Monsieur/Madame [nom], en plus du [service demandé], notre offre inclut
   automatiquement la conformité RGPD de tous les livrables que nous vous remettons.
   Concrètement : [explication en 2 phrases simples].
   Cela vous protège d'une amende pouvant aller jusqu'à [montant] de l'APD belge.
   Nos concurrents ne proposent pas ce niveau de protection en standard."

4. CLAUSE RGPD À INTÉGRER DANS CHAQUE CONTRAT :
   [rédaction de la clause article 28 RGPD pour contrat Caelum]

5. ARGUMENT DE DIFFÉRENCIATION TARIFAIRE :
   Comment utiliser la conformité RGPD pour justifier un prix 20-30% plus élevé
   que des concurrents non conformes (exemple chiffré avec ROI pour le client)""",
        "RGPD COMME ARGUMENT COMMERCIAL — Script et stratégie Caelum"
    )
    sauvegarder("rgpd_argument_commercial", r)


def structurer_contrats_solides():
    r = streamer(
        """Conçois des contrats blindés pour Caelum Partners qui préviennent tout litige.

STRUCTURE DU CONTRAT TYPE CAELUM PARTNERS :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 — IDENTIFICATION DES PARTIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Template avec champs à remplir]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — OBJET ET PÉRIMÈTRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Description précise des livrables (qu'est-ce qui est inclus ET exclu)
- Critères d'acceptation (comment définir "livré et accepté")
- Clause de périmètre : "toute demande hors périmètre fera l'objet d'un nouveau devis"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — PRIX ET CONDITIONS DE PAIEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Prix HT avec mention franchise TVA Article 56bis
- Acompte 50% à la signature (condition suspensive : pas de démarrage sans acompte)
- Solde à la livraison (définition précise de "livraison")
- Pénalités de retard : taux légal belge + 40€ forfait recouvrement
- Clause de suspension : "le prestataire peut suspendre les travaux en cas de non-paiement"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — DÉLAIS ET OBLIGATIONS DU CLIENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Délai de livraison conditionnel aux obligations du client
- Obligations du client : fournir les accès, valider dans les 5 jours, être disponible
- Clause de délai glissant : si le client retarde, le délai glisse d'autant

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5 — PROPRIÉTÉ INTELLECTUELLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Propriété des livrables transférée au client après paiement COMPLET
- Licence d'utilisation des outils IA de Caelum : usage exclusif client (pas de revente)
- Caelum conserve le droit de citer le projet comme référence (avec accord client)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6 — RGPD ET CONFIDENTIALITÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Clause article 28 RGPD — contrat sous-traitant]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 7 — RÉSILIATION ET LITIGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Résiliation par le client : acompte non remboursable si travaux commencés
- Résiliation par Caelum : remboursement prorata des sommes reçues
- Juridiction compétente : tribunaux de Bruxelles
- Tentative de médiation préalable obligatoire (30 jours)

ALERTES LÉGALES :
- Clauses à éviter absolument (clauses abusives selon Livre VI CDE belge)
- Clauses obligatoires souvent oubliées par les prestataires IA""",
        "CONTRATS BLINDÉS — Structure juridique Caelum Partners"
    )
    sauvegarder("contrats_solides", r)


def avantage_tva_franchise():
    r = streamer(
        """Explique comment utiliser la franchise TVA Article 56bis comme avantage concurrentiel sur les grandes agences.

COMPRENDRE L'AVANTAGE CONCURRENTIEL TVA :

SITUATION DES GRANDS CONCURRENTS (agences web, cabinets conseil) :
- CA > 25 000€/an → assujettis à la TVA belge (21% standard)
- Leurs prix HTVA + 21% TVA → prix TTC facturé au client
- Exemple : service à 1 000€ HTVA → le client paie 1 210€

SITUATION DE CAELUM PARTNERS (sous le seuil 25 000€/an) :
- Franchise TVA Article 56bis → pas de TVA à collecter
- Même service à 1 000€ → le client paie 1 000€ (pas de TVA)
- Avantage prix : 17,4% moins cher à qualité égale

COMMENT UTILISER CET AVANTAGE :

STRATÉGIE A — PRIX PLUS BAS :
"Notre prix est de 1 000€ tout inclus — nos concurrents de même niveau facturent 1 210€"
→ Argument : 17% d'économie pour le client final

STRATÉGIE B — MÊME PRIX, MARGE PLUS HAUTE :
"Notre prix est 1 200€ — concurrent : 1 210€"
→ Quasi même prix pour le client, mais marge de 20% supplémentaire pour Caelum

STRATÉGIE C — PREMIUM JUSTIFIÉ :
Utiliser l'économie TVA pour financer une offre plus complète au même prix total

CIBLES IDÉALES POUR CET ARGUMENT :
- Particuliers (non-assujettis TVA) : économie réelle de 21%
- Petites ASBL : souvent non-assujetties TVA → économie de 21%
- Micro-entreprises belges (sous le seuil TVA elles-mêmes) : économie 21%
- Professions libérales exemptées TVA (médecins, dentistes) : économie 21%

MENTION OBLIGATOIRE SUR LES FACTURES :
Texte exact à inclure sur CHAQUE facture :
"Régime de franchise de la taxe — Article 56bis du Code de la TVA belge.
TVA non applicable."

QUAND CET AVANTAGE DISPARAÎT-IL ?
Dès que le CA dépasse 25 000€ → obligations TVA → perte de cet avantage.
Stratégie de transition : comment préparer le passage au régime TVA sans perdre de clients.""",
        "AVANTAGE TVA FRANCHISE — Stratégie commerciale Caelum Partners"
    )
    sauvegarder("avantage_tva_franchise", r)


def certification_conformite():
    r = streamer(
        """Roadmap vers les certifications et labels de confiance pour Caelum Partners.

CERTIFICATIONS ET LABELS QUI SIGNALENT LA CONFIANCE AUX PME BELGES :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIVEAU 1 — LABELS GRATUITS ET RAPIDES (mois 1-3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. INSCRIPTION BCE VISIBLE :
   - Afficher le numéro BCE sur le site web et les documents
   - Signal : entreprise légalement constituée
   - Coût : 83,50€ (déjà obligatoire) — délai : 3 jours

2. POLITIQUE DE CONFIDENTIALITÉ RGPD PUBLIQUE :
   - Page dédiée sur le site web avec registre simplifié des traitements
   - Signal : conformité RGPD proactive
   - Coût : 0€ — délai : 1 jour

3. PROFIL LINKEDIN CERTIFIÉ ET COMPLET :
   - Certification LinkedIn Learning "IA pour les entreprises"
   - Signal : expertise démontrée et vérifiable
   - Coût : 0€ — délai : 1-2 jours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIVEAU 2 — LABELS PAYANTS À FORT IMPACT (mois 3-12)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. LABEL "ENTERPRISE EUROPE NETWORK" (EEN) :
   - Réseau EU d'entreprises innovantes — participation via Agoria ou BECI
   - Signal : reconnaissance européenne de l'innovation
   - Coût : faible ou gratuit — délai : 1-3 mois

5. MEMBRE AGORIA (fédération belge technologie) :
   - Annuaire des membres accessible aux entreprises cherchant des prestataires tech
   - Signal : légitimité dans l'écosystème tech belge
   - Coût : 500-2000€/an — délai : 1 mois

6. HUB.BRUSSELS PARTNER LABEL :
   - Label Hub.Brussels pour les entreprises innovantes bruxelloises
   - Signal : recommandation officielle de la Région de Bruxelles-Capitale
   - Coût : faible — délai : 2-3 mois

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIVEAU 3 — CERTIFICATIONS PREMIUM (an 2-3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7. ISO 27001 (Sécurité de l'information) :
   - Signal ultime de confiance en matière de données
   - Coût : 10 000-30 000€ — délai : 12-18 mois
   - À viser quand le CA justifie l'investissement (> 100K€/an)

PLAN PRIORISÉ :
Cette semaine : obtenir 3 labels gratuits
Ce mois : préparer la candidature Hub.Brussels
Cette année : rejoindre Agoria et commencer la démarche ISO 27001""",
        "ROADMAP CERTIFICATIONS — Labels de confiance Caelum Partners"
    )
    sauvegarder("certification_conformite", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  CONFORMITÉ OFFENSIVE — Caelum Partners")
    print("  RGPD · BCE · TVA franchise · INASTI · Contrats blindés")
    print("═"*65)

    while True:
        print("\n  1. Audit de conformité légale complète")
        print("  2. RGPD comme argument commercial (script)")
        print("  3. Structurer des contrats blindés")
        print("  4. Avantage TVA franchise vs concurrents")
        print("  5. Roadmap certifications et labels de confiance")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            audit_conformite_complete()
        elif choix == "2":
            rgpd_comme_argument_commercial()
        elif choix == "3":
            structurer_contrats_solides()
        elif choix == "4":
            avantage_tva_franchise()
        elif choix == "5":
            certification_conformite()
        else:
            print("  Choix invalide.")

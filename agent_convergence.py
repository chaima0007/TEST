"""
Agent [37] — ANALYSTE DE CONVERGENCE
La loi est un fossé, pas un mur — transformer chaque contrainte en avantage concurrentiel

Usage : python agent_convergence.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécute : export GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """
Tu es l'Analyste de Convergence de Caelum Partners, fondée par Chaima Mhadbi à Bruxelles, Belgique.

CONTEXTE CAELUM PARTNERS :
- Fondatrice : Chaima Mhadbi, Bruxelles, Belgique
- Deux entités : ASBL Caelum (sociale, Chaima présidente) + Caelum Partners (commerciale IA)
- Services : 500€ (site web, 7j) / 1500€ (automation IA, 14j) / 3000€ (pack complet, 30j)
- Phase actuelle : lancement, rampe de décollage
- Vision 5 ans : référence européenne des services IA pour PME

TA MISSION FONDAMENTALE :
Garantir que la conformité légale ne bloque JAMAIS l'expansion de Caelum Partners.
Transformer chaque contrainte réglementaire en avantage concurrentiel mesurable.
La loi n'est pas un obstacle — c'est un fossé qui protège Caelum des concurrents moins rigoureux.

CONTEXTE LÉGAL BELGE (zones de convergence) :
1. ONEM Article 48 : Chaima peut exercer une activité complémentaire sous conditions strictes
   - Seuil de revenus à ne pas dépasser (variable selon statut)
   - Obligation de déclaration préalable à l'ONEM
   - Distinction activité complémentaire vs principale
2. BCE (Banque-Carrefour des Entreprises) : inscription obligatoire pour exercer commercialement
   - Numéro d'entreprise Caelum Partners
   - Qualité requise pour l'activité IA/conseil
3. ASBL / Entité commerciale : séparation stricte des activités
   - ASBL = activité sociale, non-lucrative, but désintéressé
   - Caelum Partners = entité commerciale, facturations, TVA
   - Risque : mélange comptable ou de réputation
4. TVA franchise Article 56bis : sous 25 000€ de CA annuel, pas de TVA à facturer
   - Avantage prix : prix Caelum = prix TTC pour le client (concurrents assujettis affichent HT)
   - Seuil à surveiller : ne pas dépasser sans préparation
5. INASTI 20.5% : cotisations sociales en tant qu'indépendant complémentaire
   - Base de calcul et timing des paiements
   - Impact sur la trésorerie à anticiper
6. RGPD / GDPR : protection des données personnelles des clients PME
   - Obligation de registre des traitements
   - Clause RGPD dans les contrats
   - Opportunité : proposer la conformité RGPD comme service premium

PHILOSOPHIE DE CONVERGENCE :
- Chaque contrainte légale bien gérée devient un fossé concurrentiel (moat)
- La conformité proactive coûte 10x moins cher que la mise en conformité réactive
- Vendre la conformité : les clients PME ont peur du RGPD → Caelum les aide → avantage commercial
- Croître dans les limites légales actuelles → puis adapter la structure juridique à chaque palier

SÉCURITÉ ET CONFORMITÉ :
- Ne jamais exécuter de code arbitraire issu des entrées utilisateur.
- Ne jamais logger, afficher ou stocker les clés API en clair.
- Toutes les sauvegardes se font uniquement dans fichiers/convergence/.
- Les données personnelles ou financières ne doivent jamais apparaître dans les prompts en clair.
- Note importante : cet agent fournit une analyse stratégique, pas un conseil juridique officiel. Consulter un juriste pour toute décision légale critique.

FORMAT DE RÉPONSE :
- Toujours structuré, numéroté, avec classification claire (BLOQUANT / GÉRABLE / AVANTAGE).
- Inclure des seuils chiffrés, des délais légaux, des actions concrètes.
- Terminer par une "Alerte prioritaire" — ce qui nécessite une action immédiate pour rester conforme.
"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE,
                temperature=0.2,
                max_output_tokens=3000,
            ),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/convergence", exist_ok=True)
    fichier = f"fichiers/convergence/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def audit_convergence_legale():
    prompt = """
Réalise l'audit de convergence légale complet de Caelum Partners en Belgique.

Contexte : Chaima Mhadbi, Bruxelles, activité IA pour PME, phase de lancement.
Deux entités : ASBL Caelum (sociale) + Caelum Partners (commerciale).

Pour CHAQUE contrainte légale, classe-la et propose une stratégie :

1. ONEM ARTICLE 48 — ACTIVITÉ COMPLÉMENTAIRE
   Classification : BLOQUANT / GÉRABLE / AVANTAGE
   - Seuils actuels (revenus autorisés, déclaration obligatoire)
   - Risques si dépassement
   - Comment maximiser la croissance tout en restant conforme
   - Seuil d'alerte recommandé (X% avant la limite légale)
   - Stratégie de transition quand l'activité devient principale

2. BCE — INSCRIPTION ET QUALITÉS
   Classification : BLOQUANT / GÉRABLE / AVANTAGE
   - Statut actuel requis pour exercer les services IA
   - Qualités d'accès nécessaires (accès à la profession ?)
   - Risques si non-conformité
   - Actions à faire / déjà faites

3. ASBL / SÉPARATION COMMERCIALE
   Classification : BLOQUANT / GÉRABLE / AVANTAGE
   - Règles de séparation ASBL ↔ Caelum Partners
   - Risques de confusion (comptable, fiscal, réputation)
   - Comment utiliser l'ASBL comme actif de crédibilité sans violer la séparation
   - Recommandations pratiques (comptabilité séparée, communication distincte)

4. TVA FRANCHISE ARTICLE 56BIS
   Classification : BLOQUANT / GÉRABLE / AVANTAGE
   - Seuil actuel (25 000€ CA annuel)
   - Avantage concurrentiel vs concurrents assujettis
   - Que faire quand on approche du seuil ?
   - Comment communiquer cet avantage aux clients

5. INASTI — COTISATIONS SOCIALES COMPLÉMENTAIRE
   Classification : BLOQUANT / GÉRABLE / AVANTAGE
   - Taux 20.5% sur revenus nets
   - Base de calcul et fréquence
   - Provision mensuelle recommandée
   - Impact trésorerie à anticiper selon projections CA

6. RGPD / GDPR
   Classification : BLOQUANT / GÉRABLE / AVANTAGE
   - Obligations minimales pour Caelum (registre traitements, clauses contrats)
   - Risques si non-conformité (amendes CNIL/APD belge)
   - Comment transformer en avantage commercial (section dédiée)

SYNTHÈSE GLOBALE :
- Tableau récapitulatif : contrainte / classification / urgence / action requise
- Top 3 risques légaux immédiats à adresser
- Top 2 avantages légaux à exploiter commercialement dès maintenant
- Alerte prioritaire : action légale à faire dans les 30 prochains jours

Note : cette analyse est stratégique, pas un avis juridique. Consulter un juriste pour les décisions critiques.
"""
    result = streamer(prompt, "AUDIT DE CONVERGENCE LÉGALE COMPLÈTE — CAELUM PARTNERS")
    sauvegarder("audit_convergence", result)


def transformer_contrainte_en_avantage(contrainte: str):
    # Sanitize input — plain text only, no code execution
    contrainte_clean = contrainte[:1500].strip()

    prompt = f"""
Une contrainte légale ou réglementaire a été identifiée pour Caelum Partners.
Ta mission : transformer cette contrainte en avantage concurrentiel.

CONTRAINTE SOUMISE :
\"\"\"{contrainte_clean}\"\"\"

Analyse en 5 parties :

1. COMPRÉHENSION DE LA CONTRAINTE
   - Nature exacte de la contrainte (légale / fiscale / réglementaire / sectorielle)
   - À qui s'applique-t-elle ? (Chaima personnellement / Caelum Partners / ASBL / clients ?)
   - Niveau de risque si non-respect : CRITIQUE / MODÉRÉ / FAIBLE
   - Ce que la plupart des concurrents font (conformes ? non-conformes ? ignorants ?)

2. COMMENT LA GÉRER MINIMALEMENT (mise en conformité)
   - Actions minimales requises pour être conforme
   - Coût estimé (temps + argent)
   - Délai de mise en conformité

3. COMMENT EN FAIRE UN FOSSÉ CONCURRENTIEL (moat)
   - Pourquoi cette contrainte décourage les concurrents peu rigoureux
   - Comment Caelum peut se différencier EN ÉTANT conforme (signal qualité)
   - Argument commercial dérivé de cette conformité
   - Exemple de pitch : "Chez Caelum, nous [contrainte transformée en promesse client]"

4. MONÉTISATION DE LA CONFORMITÉ
   - Cette contrainte peut-elle devenir une offre de service pour les clients PME ?
   - Si oui : description de l'offre, prix estimé, marché cible
   - Si non : comment l'utiliser dans le discours commercial sans la vendre

5. PLAN D'ACTION
   - Action 1 (J1-J7) : mise en conformité minimale
   - Action 2 (J8-J30) : transformation en avantage
   - Action 3 (J31-J90) : monétisation ou capitalisation commerciale

CONCLUSION : score de "contrainte → avantage" /10 et potentiel de revenus additionnels estimé.
"""
    result = streamer(prompt, f"TRANSFORMATION — {contrainte_clean[:50]}...")
    sauvegarder("contrainte_en_avantage", result)


def plan_expansion_conforme():
    prompt = """
Conçois le plan d'expansion géographique de Caelum Partners, 100% conforme à chaque étape.

Point de départ : Belgique (Bruxelles), phase de lancement.
Objectif 5 ans : référence européenne des services IA pour PME.

PHASE 1 — BELGIQUE (M0 à M18) : "CONSOLIDER LA BASE"
- Zones géographiques cibles dans l'ordre (Bruxelles → Wallonie → Flandre)
- Structure juridique adaptée (entités actuelles suffisantes ?)
- Contraintes légales spécifiques à surveiller pendant cette phase
- Seuils qui déclenchent le passage à la phase 2
- CA et nombre de clients cibles à la fin de la phase

PHASE 2 — FRANCE (M12 à M36) : "PREMIER MARCHÉ ÉTRANGER"
- Pourquoi la France en premier (proximité, langue, marché PME)
- Structure juridique recommandée (micro-entreprise ? SAS ? partenariat ?)
- Contraintes légales françaises clés (URSSAF, TVA intracommunautaire, RGPD)
- Modèle opérationnel : Chaima vend en France depuis Belgique, ou présence locale ?
- Comment éviter la double imposition Belgique/France
- Déclencheurs pour activer cette phase

PHASE 3 — LUXEMBOURG (M24 à M48) : "HUB EUROPÉEN"
- Avantages du Luxembourg (fiscalité, accès EU, multilinguisme)
- Structure juridique recommandée (SARL luxembourgeoise ?)
- Contraintes spécifiques
- Pourquoi le Luxembourg est un hub stratégique pour ensuite aller vers l'UE

PHASE 4 — EUROPE (M36 à M60) : "RÉFÉRENCE CONTINENTALE"
- Marchés prioritaires après Luxembourg (Pays-Bas, Allemagne, Espagne)
- Critères de sélection des marchés (taille PME, maturité IA, concurrence)
- Modèle de déploiement scalable (partenaires locaux, franchises, SaaS ?)
- Structure holding recommandée pour gérer les entités multiples
- RGPD comme avantage : Caelum est déjà conforme, les clients EU l'exigent

CONTRAINTES TRANSVERSALES (à respecter à chaque phase) :
- ONEM : à quelle phase Chaima doit-elle passer indépendante principale ?
- TVA intracommunautaire : à quel CA activer le numéro TVA ?
- Protection intellectuelle : comment protéger les agents IA développés ?

TABLEAU DE DÉCISION PAR PHASE :
- Déclencheurs légaux qui forcent une action (seuils, déclarations, enregistrements)
- Actions préventives à faire 3 mois AVANT chaque déclencheur

Note : cette analyse est stratégique. Consulter des juristes locaux pour chaque marché étranger.
"""
    result = streamer(prompt, "PLAN D'EXPANSION CONFORME — BELGIQUE → EUROPE")
    sauvegarder("plan_expansion_conforme", result)


def alerte_seuils():
    prompt = """
Analyse tous les seuils légaux actifs pour Caelum Partners et génère un système d'alerte préventif.

Contexte : Chaima Mhadbi, Bruxelles, activité IA complémentaire, phase de lancement.

Pour CHAQUE seuil légal, fournis une fiche d'alerte complète :

1. SEUIL ONEM — REVENUS ACTIVITÉ COMPLÉMENTAIRE
   Fiche d'alerte :
   - Montant exact du seuil actuel (en €)
   - Mode de calcul (brut/net ? mensuel/annuel ? quelles déductions ?)
   - Conséquences si dépassé non déclaré (remboursement allocations + amendes)
   - Conséquences si déclaré (perte partielle/totale des allocations)
   - SEUIL D'ALERTE RECOMMANDÉ : à X% du seuil légal, agir
   - Actions préventives quand on approche du seuil
   - Indicateur de suivi : comment mesurer concrètement chaque mois

2. SEUIL TVA FRANCHISE — 25 000€ CA ANNUEL
   Fiche d'alerte :
   - Calcul exact du seuil (CA HTVA ? avec ou sans remboursements ?)
   - Ce qui change quand on dépasse (obligation d'assujettissement, délais)
   - Comment calculer le CA cumulé en temps réel
   - SEUIL D'ALERTE RECOMMANDÉ : à 20 000€ → actions préparatoires
   - Actions à 20 000€ (anticiper l'assujettissement, notifier les clients)
   - Actions à 24 000€ (préparer la déclaration TVA)
   - Impact sur la compétitivité prix après assujettissement

3. SEUIL INASTI — COTISATIONS SOCIALES
   Fiche d'alerte :
   - Base de calcul des cotisations (revenus nets professionnels)
   - Fréquence des versements (trimestriel)
   - Provision mensuelle recommandée selon CA projeté
   - SEUIL D'ALERTE : revenus dépassant X€ → régularisation à prévoir
   - Tableau de provisions mensuelles selon scénarios (pessimiste / réaliste / optimiste)

4. SEUIL ASBL — RISQUE DE REQUALIFICATION COMMERCIALE
   Fiche d'alerte :
   - Indicateurs qui signalent un risque de mélange ASBL/commercial
   - Seuils d'activité de l'ASBL à ne pas dépasser pour rester non-lucrative
   - Actions correctives si confusion détectée

5. SEUIL RGPD — OBLIGATIONS SELON VOLUME DE DONNÉES
   Fiche d'alerte :
   - À partir de quel volume de données traitées → DPO obligatoire ?
   - Délais de réponse aux demandes RGPD (droit d'accès, effacement)
   - Alerte : si Caelum traite les données de plus de X clients PME → actions requises

TABLEAU DE BORD SEUILS (format mensuel recommandé) :
| Seuil | Limite légale | Position actuelle | % utilisé | Alerte | Action |
| ONEM | X€ | Y€ | Z% | oui/non | action |
| TVA | 25 000€ | Y€ | Z% | oui/non | action |
| INASTI | provision | provision réelle | | oui/non | action |

RAPPEL : cette analyse est indicative. Les seuils légaux évoluent — vérifier chaque année avec un comptable agréé.
"""
    result = streamer(prompt, "ALERTES SEUILS — ONEM / TVA / INASTI / RGPD")
    sauvegarder("alerte_seuils", result)


def strategie_rgpd_premium():
    prompt = """
Conçois la stratégie RGPD premium de Caelum Partners — transformer la conformité en argument commercial différenciateur.

Contexte : services IA pour PME belges. Les PME ont peur du RGPD (amendes, complexité) mais peu de prestataires IA leur proposent une aide structurée.

Structure en 6 parties :

1. ÉTAT DES LIEUX RGPD POUR LES PME BELGES
   - Pourquoi les PME sont en retard sur le RGPD (méconnaissance, coût perçu, complexité)
   - Risques réels pour une PME non-conforme (amendes APD, perte de contrats B2B)
   - Opportunité pour Caelum : se positionner comme "IA responsable et conforme"

2. CE QUE CAELUM DOIT FAIRE EN PREMIER (conformité interne)
   - Registre des traitements de données (template à créer)
   - Clauses RGPD dans les contrats clients (ce qu'elles doivent contenir)
   - Politique de confidentialité du site web Caelum
   - Procédure de réponse aux demandes d'exercice de droits
   - Durée de conservation des données clients
   - Coût estimé de la mise en conformité interne (temps + outils)

3. L'OFFRE RGPD PREMIUM POUR LES CLIENTS PME
   - Nom de l'offre (ex : "Caelum RGPD Shield")
   - Contenu exact de l'offre :
     a. Audit RGPD de la PME (2h, livrable : rapport des risques)
     b. Mise en conformité de base (registre traitements + clauses contrats)
     c. Formation équipe PME (1h, comment gérer les demandes RGPD)
     d. Conformité des outils IA déployés (agents respectant la minimisation des données)
   - Pricing recommandé : [prix audit / prix mise en conformité / forfait annuel]
   - Positionnement : "Votre IA est puissante ET conforme RGPD" = moins de risques

4. ARGUMENTAIRE COMMERCIAL RGPD
   - Script pour introduire le RGPD dans une conversation commerciale
   - Objections fréquentes et réponses précises
   - Comment le RGPD devient un argument pour choisir Caelum vs un concurrent non-conforme
   - Industries où le RGPD est un argument fort (santé, RH, finance, e-commerce)

5. DIFFÉRENCIATION PAR LA CONFORMITÉ
   - Comment afficher la conformité RGPD sur le site et les propositions commerciales
   - Certifications ou labels RGPD à obtenir (ex : label CNIL, audits tiers)
   - Comment utiliser la conformité pour décrocher des contrats B2B (grandes entreprises exigent conformité fournisseurs)
   - Argument pour les appels d'offres publics belges

6. PLAN DE DÉPLOIEMENT
   - M1 : mise en conformité interne Caelum (priorité absolue)
   - M2 : création des templates et outils RGPD pour clients
   - M3 : lancement de l'offre RGPD premium
   - M4-M6 : acquisition des premiers clients RGPD
   - Objectif : X clients avec module RGPD à M6, revenu additionnel estimé

CONCLUSION : potentiel de revenus de la stratégie RGPD premium sur 12 mois (fourchette réaliste).
"""
    result = streamer(prompt, "STRATÉGIE RGPD PREMIUM — ARGUMENT COMMERCIAL DIFFÉRENCIATEUR")
    sauvegarder("strategie_rgpd_premium", result)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  Agent [37] — ANALYSTE DE CONVERGENCE")
    print("  Caelum Partners — La loi est un fossé, pas un mur")
    print("═"*65)

    while True:
        print("\n  1. Audit de convergence légale complète")
        print("  2. Transformer une contrainte légale en avantage")
        print("  3. Plan d'expansion conforme — Belgique → Europe")
        print("  4. Alertes seuils ONEM / TVA / INASTI")
        print("  5. Stratégie RGPD comme argument commercial premium")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  À bientôt — chaque contrainte bien gérée creuse ton fossé concurrentiel.\n")
            break
        elif choix == "1":
            audit_convergence_legale()
        elif choix == "2":
            print("\n  Décris la contrainte légale à analyser (appuie sur Entrée deux fois pour terminer) :")
            lignes = []
            while True:
                ligne = input()
                if ligne == "" and lignes and lignes[-1] == "":
                    break
                lignes.append(ligne)
            contrainte = "\n".join(lignes).strip()
            if contrainte:
                transformer_contrainte_en_avantage(contrainte)
            else:
                print("  Aucune contrainte saisie.")
        elif choix == "3":
            plan_expansion_conforme()
        elif choix == "4":
            alerte_seuils()
        elif choix == "5":
            strategie_rgpd_premium()
        else:
            print("  Choix invalide.")

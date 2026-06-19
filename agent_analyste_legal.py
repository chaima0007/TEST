# [50] ANALYSTE DE BASE DE DONNÉES LÉGALES — Caelum Partners

import os
import json
import requests
from datetime import datetime

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

SYSTEM_PROMPT = """Tu es un Analyste de Bases de Données Légales pour Caelum Partners.
Mission: Ingérer et structurer des corpus juridiques belges en données exploitables.
Directives:
- Transformer les textes de loi en JSON structuré (article → règle → condition → conséquence)
- Identifier les obligations légales applicables à Caelum Partners
- Créer des schémas de données pour les bases SQL/JSON
- Résumer les lois en langage actionnable (pas du jargon)
- Sécurité: traiter les données légales comme confidentielles, ne pas exposer données clients
Domaines: ONEM/INASTI, TVA, BCE, RGPD, droit commercial belge, contrats de services"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def sanitize_input(text: str, max_length: int = 8000) -> str:
    """Sanitize user input: strip, limit length, remove null bytes."""
    if not isinstance(text, str):
        text = str(text)
    text = text.replace('\x00', '')  # remove null bytes
    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length] + "\n[... tronqué pour sécurité ...]"
    return text


def streamer_ollama(prompt: str, system: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": prompt, "system": system, "stream": True},
            stream=True,
            timeout=120
        )
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                data = json.loads(line)
                token = data.get("response", "")
                print(token, end="", flush=True)
                reponse += token
                if data.get("done"):
                    break
    except requests.exceptions.ConnectionError:
        print("[ERREUR] Ollama non démarré. Lance: ollama serve")
    except Exception as e:
        print(f"[Erreur: {e}]")
    print()
    return reponse


def get_save_dir(subdir: str) -> str:
    if os.name == "nt":  # Windows
        base = os.path.join("C:\\", "Caelum_Projets", subdir)
    else:
        base = os.path.join(os.path.expanduser("~"), "Caelum_Projets", subdir)
    os.makedirs(base, exist_ok=True)
    return base


def sauvegarder(nom: str, contenu: str, subdir: str):
    base = get_save_dir(subdir)
    fichier = os.path.join(base, f"{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé localement → {fichier}")


def verifier_ollama():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        modeles = [m["name"] for m in r.json().get("models", [])]
        if modeles:
            print(f"  ✅ Ollama connecté — Modèles: {', '.join(modeles[:3])}")
        else:
            print(f"  ⚠️  Ollama connecté mais aucun modèle. Lance: ollama pull llama3.2")
    except Exception:
        print(f"  ❌ Ollama inaccessible sur {OLLAMA_URL}")
        print(f"  → Lance: ollama serve")
        print(f"  → Puis: ollama pull llama3.2")


def lire_multilignes(invite: str) -> str:
    """Lire un bloc de texte multi-lignes jusqu'à 'FIN' sur une ligne seule."""
    print(invite)
    print("  (Tape FIN sur une ligne seule pour terminer)\n")
    lignes = []
    while True:
        try:
            ligne = input()
        except EOFError:
            break
        if ligne.strip() == "FIN":
            break
        lignes.append(ligne)
    return "\n".join(lignes)


# ── Fonctions principales ───────────────────────────────────────────────────────

def structurer_texte_legal(texte_loi: str):
    """Convertit un texte de loi brut en JSON structuré exploitable."""
    texte_loi = sanitize_input(texte_loi, max_length=10000)
    if not texte_loi:
        print("  ⚠️  Texte de loi vide. Abandon.")
        return

    prompt = f"""Analyse et structure ce texte de loi belge en données JSON exploitables.

TEXTE DE LOI:
{texte_loi}

INSTRUCTIONS DE STRUCTURATION:
Transforme ce texte en JSON structuré selon le schéma suivant.
Pour CHAQUE article identifié, extrait:

SCHÉMA JSON ATTENDU:
{{
  "loi": {{
    "titre": "...",
    "reference": "...",
    "date_entree_vigueur": "...",
    "domaine": "..."
  }},
  "articles": [
    {{
      "numero_article": "Art. X",
      "titre_article": "...",
      "regle_principale": "En une phrase claire et actionnable",
      "conditions_applicabilite": [
        "Condition 1: ...",
        "Condition 2: ..."
      ],
      "obligations": [
        {{
          "qui": "Sujet obligé (ex: l'employeur, le prestataire)",
          "quoi": "Action requise",
          "quand": "Délai ou fréquence",
          "comment": "Modalités d'exécution"
        }}
      ],
      "consequences_non_respect": [
        {{
          "type": "Amende / Sanction pénale / Nullité / Autre",
          "montant_ou_duree": "...",
          "autorite_competente": "..."
        }}
      ],
      "delais": [
        {{
          "description": "...",
          "duree": "...",
          "point_de_depart": "..."
        }}
      ],
      "exceptions": ["..."],
      "renvois": ["Référence à d'autres articles ou lois"]
    }}
  ],
  "resume_operationnel": "Résumé en 3-5 phrases du texte entier en langage non-juridique",
  "checklist_conformite": [
    "Action 1 à effectuer pour être conforme",
    "Action 2...",
    "Action 3..."
  ]
}}

IMPORTANT:
- Utilise UNIQUEMENT les informations présentes dans le texte fourni
- Si une information est absente, mets null (pas de valeur inventée)
- Le JSON doit être valide et parseable
- Traduis le jargon juridique en langage clair dans resume_operationnel
- La checklist_conformite doit être actionnable immédiatement

Fournis d'abord le JSON structuré, puis un résumé exécutif en français simple."""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "STRUCTURATION DU TEXTE LÉGAL")
    sauvegarder("loi_structuree", resultat, "legal")


def extraire_obligations(domaine: str):
    """Extrait toutes les obligations légales applicables à Caelum Partners dans un domaine."""
    domaine = sanitize_input(domaine, max_length=200)
    if not domaine:
        print("  ⚠️  Domaine vide. Abandon.")
        return

    prompt = f"""Identifie et liste toutes les obligations légales applicables à Caelum Partners dans le domaine suivant.

DOMAINE LÉGAL:
{domaine}

CONTEXTE DE CAELUM PARTNERS:
- Société de consulting basée à Bruxelles, Belgique
- Statut: société (forme juridique à préciser selon le domaine)
- Activités: conseil en stratégie, gestion de projets, services B2B
- Taille: PME (moins de 50 collaborateurs)
- Droit applicable: droit belge principalement, droit européen si applicable

INSTRUCTIONS D'EXTRACTION:
Pour le domaine "{domaine}", génère une checklist exhaustive et actionnable:

1. CADRE LÉGAL APPLICABLE:
   - Lois et règlements principaux (avec références officielles)
   - Autorités de contrôle compétentes
   - Dernières modifications législatives importantes

2. OBLIGATIONS LÉGALES (format checklist):
   Pour chaque obligation:
   - [ ] Description claire de l'obligation en langage non-juridique
   - Qui est responsable chez Caelum Partners (gérant, RH, comptable...)
   - Délai/Fréquence: (ex: "avant le 31 mars de chaque année", "dans les 30 jours")
   - Document requis: (ex: formulaire X, déclaration Y)
   - Autorité destinataire: (ex: SPF Finances, ONSS, BCE)
   - Sanction en cas de non-respect

3. OBLIGATIONS CLASSÉES PAR URGENCE:
   - IMMÉDIAT (à faire dans les 30 jours)
   - ANNUEL (obligations récurrentes annuelles)
   - PONCTUEL (lors d'événements spécifiques: nouveau contrat, embauche...)
   - CONTINU (obligations permanentes)

4. DOCUMENTS À CONSERVER:
   - Liste des documents obligatoires
   - Durée de conservation légale
   - Format requis (papier/électronique)

5. RESSOURCES OFFICIELLES:
   - Sites web des autorités compétentes
   - Formulaires officiels à utiliser

FORMAT:
# Obligations légales — {domaine} — Caelum Partners
## Cadre légal
## Checklist d'obligations
### Immédiat
### Annuel
### Ponctuel
### Continu
## Documents à conserver
## Ressources officielles

AVERTISSEMENT: Ceci est une analyse indicative. Consulter un juriste pour validation."""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, f"EXTRACTION DES OBLIGATIONS — {domaine.upper()}")
    sauvegarder("obligations_legales", resultat, "legal")


def creer_schema_base_donnees(entites: str):
    """Conçoit un schéma JSON et SQL pour stocker des données légales structurées."""
    entites = sanitize_input(entites, max_length=2000)
    if not entites:
        print("  ⚠️  Description des entités vide. Abandon.")
        return

    prompt = f"""Conçois un schéma de base de données complet pour stocker des données légales structurées.

ENTITÉS À MODÉLISER:
{entites}

CONTEXTE D'UTILISATION:
- Application de gestion de conformité légale pour Caelum Partners
- Données: textes de loi, obligations, deadlines, documents de conformité
- Utilisateurs: équipe administrative (non-techniciens)
- Volume estimé: petite à moyenne base (< 100K enregistrements)

INSTRUCTIONS DE CONCEPTION:

PARTIE 1 — SCHÉMA JSON (pour API/stockage NoSQL):
Fournis des exemples de schémas JSON pour chaque entité avec:
- Tous les champs nécessaires avec leurs types
- Champs obligatoires vs optionnels
- Exemples de valeurs réelles
- Validations (format date, longueur max, valeurs acceptées)

Format:
```json
{{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "[NomEntité]",
  "type": "object",
  "required": [...],
  "properties": {{
    "id": {{"type": "string", "description": "..."}},
    ...
  }}
}}
```

PARTIE 2 — SCHÉMA SQL (DDL PostgreSQL compatible):
Fournis les instructions CREATE TABLE pour chaque entité avec:
- Clés primaires (UUID recommandé)
- Clés étrangères avec ON DELETE/UPDATE appropriés
- Index sur les colonnes fréquemment recherchées
- Contraintes CHECK pour les valeurs métier
- Commentaires sur chaque colonne

Format:
```sql
-- [Description de la table]
CREATE TABLE [nom_table] (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ...
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX idx_[table]_[colonne] ON [table]([colonne]);

-- Contraintes
COMMENT ON TABLE [table] IS '...';
COMMENT ON COLUMN [table].[colonne] IS '...';
```

PARTIE 3 — RELATIONS ET DIAGRAMME:
- Décris les relations entre entités (1:1, 1:N, N:M)
- Représente le diagramme en ASCII art simple
- Explique les choix de modélisation

PARTIE 4 — REQUÊTES TYPES:
Fournis 3-5 requêtes SQL utiles pour les cas d'usage courants (recherche d'obligations par deadline, filtrage par domaine, etc.)"""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "CRÉATION DU SCHÉMA DE BASE DE DONNÉES")
    sauvegarder("schema_bdd", resultat, "legal")


def analyser_conformite_document(document: str):
    """Analyse la conformité légale d'un document contractuel ou administratif."""
    document = sanitize_input(document, max_length=10000)
    if not document:
        print("  ⚠️  Document vide. Abandon.")
        return

    prompt = f"""Analyse la conformité légale de ce document dans le contexte belge.

DOCUMENT À ANALYSER:
{document}

CONTEXTE:
- Entreprise: Caelum Partners, société de consulting à Bruxelles
- Droit applicable: droit belge, droit européen si pertinent
- Objectif: identifier les lacunes légales et risques avant signature/utilisation

INSTRUCTIONS D'ANALYSE DE CONFORMITÉ:

1. IDENTIFICATION DU DOCUMENT:
   - Type de document (contrat, annexe, CGV, politique, formulaire...)
   - Parties impliquées (si mentionnées)
   - Objet principal du document
   - Lois potentiellement applicables

2. LOIS ET RÉGLEMENTATIONS APPLICABLES:
   Pour chaque loi/règlement pertinent identifié:
   - Référence officielle
   - Pourquoi elle s'applique à ce document
   - Exigences spécifiques imposées

3. ANALYSE DES LACUNES DE CONFORMITÉ:
   Pour chaque problème identifié:
   | # | Clause/Section | Problème | Loi violée | Risque | Correction requise |
   |---|----------------|----------|------------|--------|--------------------|

   Classe par sévérité:
   - BLOQUANT: Illégal, nullité possible, sanction certaine
   - MAJEUR: Non-conforme, risque élevé si non corrigé
   - MINEUR: Lacune, best practice non respectée
   - INFO: Observation sans impact légal immédiat

4. RISQUES JURIDIQUES:
   - Risque de nullité du document (oui/non + pourquoi)
   - Risques financiers (amendes, dommages-intérêts)
   - Risques opérationnels (blocage d'activité)
   - Risques réputationnels

5. CORRECTIONS REQUISES:
   Pour chaque lacune BLOQUANTE ou MAJEURE:
   - Texte actuel (problématique)
   - Texte corrigé suggéré
   - Justification légale

6. RÉSUMÉ EXÉCUTIF:
   Score de conformité estimé: X/10
   Verdict: [CONFORME / NON-CONFORME / PARTIELLEMENT CONFORME]
   Actions prioritaires avant utilisation du document.

AVERTISSEMENT: Analyse indicative uniquement. Validation par juriste recommandée."""

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "ANALYSE DE CONFORMITÉ LÉGALE")
    sauvegarder("conformite_document", resultat, "legal")


def generer_checklist_legale():
    """Génère une checklist complète de conformité légale pour Caelum Partners."""
    prompt = """Génère une checklist de conformité légale complète et actionnable pour Caelum Partners.

PROFIL DE L'ENTREPRISE:
- Nom: Caelum Partners
- Type: Société de consulting (conseil en stratégie et gestion de projets)
- Localisation: Bruxelles, Belgique
- Activités: Prestations de services B2B, conseil, accompagnement de projets
- Taille: PME, moins de 50 collaborateurs
- Clients: Entreprises belges et européennes

INSTRUCTIONS:
Génère une checklist exhaustive couvrant TOUS les domaines légaux ci-dessous.
Pour chaque item:
- [ ] Action concrète et vérifiable (pas de jargon)
- Fréquence/Délai: quand agir
- Responsable: qui dans l'entreprise
- Document/Preuve: comment prouver la conformité
- Référence légale: loi ou règlement applicable

═══════════════════════════════════════════════════════════
DOMAINE 1 — BCE (Banque-Carrefour des Entreprises)
═══════════════════════════════════════════════════════════
- Inscription et numéro BCE
- Mise à jour des données (adresse, activités, représentants)
- Unités d'établissement
- Publication des comptes annuels

═══════════════════════════════════════════════════════════
DOMAINE 2 — TVA (Taxe sur la Valeur Ajoutée)
═══════════════════════════════════════════════════════════
- Assujettissement TVA belge
- Déclarations périodiques (mensuelles ou trimestrielles)
- Listing annuel des clients assujettis
- TVA intracommunautaire (clients UE)
- Facturation conforme (mentions obligatoires)
- Conservation des documents TVA (7 ans)

═══════════════════════════════════════════════════════════
DOMAINE 3 — RGPD (Règlement Général sur la Protection des Données)
═══════════════════════════════════════════════════════════
- Registre des activités de traitement
- Bases légales pour chaque traitement
- Politique de confidentialité (site web, contrats)
- Droits des personnes (accès, rectification, effacement)
- Sécurité des données (mesures techniques)
- Data breach notification (72h à l'APD)
- Transferts hors UE
- DPO (nécessaire ou non?)
- Consentement cookies

═══════════════════════════════════════════════════════════
DOMAINE 4 — ONEM/INASTI (Sécurité Sociale)
═══════════════════════════════════════════════════════════
- Affiliation ONSS pour les employés
- Déclarations DIMONA (entrée/sortie travailleurs)
- Cotisations sociales employeur
- Si indépendant: affiliation INASTI et caisse d'assurances sociales
- Cotisations sociales indépendant (trimestrielles)
- Congé annuel (secteur)

═══════════════════════════════════════════════════════════
DOMAINE 5 — DROIT COMMERCIAL BELGE
═══════════════════════════════════════════════════════════
- Contrats de services (clauses obligatoires)
- Conditions Générales de Vente/Prestation
- Délais de paiement légaux (60 jours B2B)
- Intérêts de retard légaux
- Garanties légales
- Résolution des litiges (clause arbitrage/médiation)
- Droit applicable et juridiction compétente

═══════════════════════════════════════════════════════════
DOMAINE 6 — FACTURATION ET COMPTABILITÉ
═══════════════════════════════════════════════════════════
- Mentions obligatoires sur les factures belges
- Numérotation séquentielle des factures
- Délai d'envoi des factures
- Conservation comptable (7 ans minimum)
- Comptes annuels (dépôt BNB)
- Audit si applicable

═══════════════════════════════════════════════════════════
FORMAT FINAL:
═══════════════════════════════════════════════════════════
# Checklist Conformité Légale — Caelum Partners
## Date de génération: {date}
## Dernière révision recommandée: annuelle

[Pour chaque domaine, liste structurée avec cases à cocher]

## Calendrier de conformité annuel
[Vue mensuelle des deadlines récurrentes]

## Contacts utiles
[Autorités compétentes avec sites web officiels belges]

AVERTISSEMENT: Cette checklist est indicative. Consulter un comptable agréé et/ou un juriste pour validation et adaptation à la situation spécifique de Caelum Partners.""".format(
        date=datetime.now().strftime('%d/%m/%Y')
    )

    resultat = streamer_ollama(prompt, SYSTEM_PROMPT, "CHECKLIST LÉGALE COMPLÈTE — CAELUM PARTNERS")
    sauvegarder("checklist_legale_complete", resultat, "legal")


# ── Menu principal ──────────────────────────────────────────────────────────────

def afficher_banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║    [50] ANALYSTE DE BASE DE DONNÉES LÉGALES — Caelum Partners   ║
╠══════════════════════════════════════════════════════════════════╣
║  Agent local via Ollama — Données légales traitées localement   ║
╚══════════════════════════════════════════════════════════════════╝""")
    print(f"  Modèle : {MODEL}")
    print(f"  URL    : {OLLAMA_URL}")
    print()
    verifier_ollama()
    print()


def afficher_menu():
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                        MENU PRINCIPAL                           │
├─────────────────────────────────────────────────────────────────┤
│  1. Structurer un texte de loi en JSON                          │
│  2. Extraire les obligations par domaine légal                  │
│  3. Créer un schéma de base de données légale                   │
│  4. Analyser la conformité d'un document                        │
│  5. Générer la checklist légale complète Caelum Partners        │
├─────────────────────────────────────────────────────────────────┤
│  0. Quitter                                                     │
└─────────────────────────────────────────────────────────────────┘""")


def main():
    afficher_banner()

    while True:
        afficher_menu()
        try:
            choix = input("\n  Ton choix (0-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Au revoir!")
            break

        if choix == "0":
            print("\n  Au revoir!")
            break

        elif choix == "1":
            texte = lire_multilignes("\n📋 Colle le texte de loi à structurer:")
            structurer_texte_legal(texte)

        elif choix == "2":
            domaine = input(
                "\n⚖️  Domaine légal à analyser\n"
                "  (ex: TVA, RGPD, BCE, ONEM, droit commercial, contrats de services): "
            ).strip()
            extraire_obligations(domaine)

        elif choix == "3":
            entites = lire_multilignes(
                "\n📊 Décris les entités à modéliser\n"
                "  (ex: 'lois, articles, obligations, entreprises, documents de conformité'):"
            )
            creer_schema_base_donnees(entites)

        elif choix == "4":
            document = lire_multilignes("\n📋 Colle le document à analyser pour conformité:")
            analyser_conformite_document(document)

        elif choix == "5":
            print("\n  Génération de la checklist légale complète pour Caelum Partners...")
            generer_checklist_legale()

        else:
            print("  ⚠️  Choix invalide. Entre un nombre entre 0 et 5.")

        input("\n  Appuie sur Entrée pour continuer...")


if __name__ == "__main__":
    main()

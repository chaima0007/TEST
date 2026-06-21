# Checklist Onboarding Client Pilote — J0 à J30

**Caelum Partners — Human Rights Intelligence Platform**

> Ce document est la checklist opérationnelle pour chaque nouveau client pilote.  
> Responsable : Chaima Mhadbi (CEO)

---

## J0 — Signature & Activation

- [ ] Pilot Agreement signé par les deux parties (PDF archivé dans `/clients/[NOM]/`)
- [ ] Référence pilote générée : `PILOT-[YYYY-MM-NNN]`
- [ ] 5 engines sélectionnés par le client — notés dans tracking_table.md
- [ ] Credentials créés : 2 utilisateurs nommés (email + mot de passe temporaire)
- [ ] Email de bienvenue envoyé avec :
  - Lien tableau de bord
  - Credentials
  - Date onboarding J2 confirmée
  - Lien calendrier support
- [ ] Slack/email interne : notifier l'équipe technique de l'activation

**Template email bienvenue :**
```
Objet : Bienvenue chez Caelum Partners — votre pilote est activé !

Bonjour [Prénom],

Votre accès pilote Caelum Partners est activé. Voici vos informations :

Tableau de bord : [URL]
Identifiant : [EMAIL]
Mot de passe temporaire : [PWD] (à changer à la première connexion)

Engines activés : [liste des 5 engines]

Notre session onboarding Zoom est confirmée pour le [DATE J2] à [HEURE].
Lien : [ZOOM_LINK]

En attendant, n'hésitez pas à explorer le tableau de bord.
Je réponds à toutes vos questions par email sous 24h.

À bientôt,
Chaima Mhadbi
chaima@caelumpartners.eu
```

---

## J2 — Session Onboarding Zoom (2h)

**Agenda session :**

### Partie 1 — Prise en main (45 min)
- [ ] Tour du dashboard principal
- [ ] Navigation entre les 5 engines client
- [ ] Lecture d'un score composite (exemple live)
- [ ] Utilisation du filtre "critique" (score ≥ 60)
- [ ] Ouverture d'un DetailModal — sous-scores et sources
- [ ] Export PDF d'un rapport (demo)

### Partie 2 — Cas d'usage client (45 min)
- [ ] Identifier les entités géographiques les plus exposées pour leur secteur
- [ ] Relier les scores aux obligations CSRD/CSDDD/LkSG du client
- [ ] Démontrer comment un score alimente un rapport de due diligence
- [ ] Q&A sur les données sources et la méthodologie

### Partie 3 — Next Steps (30 min)
- [ ] Confirmer les 5 engines sélectionnés (ou ajuster)
- [ ] Planifier le rapport automatique J7
- [ ] Définir les KPIs du pilote (ce que le client veut mesurer)
- [ ] Rappeler les conditions de conversion (Easy Access / Enterprise Premium)

**Post-session :**
- [ ] Envoyer compte-rendu écrit de la session sous 24h
- [ ] Documenter les KPIs retenus dans tracking_table.md
- [ ] Créer rappel J7 dans calendrier

---

## J7 — Premier Rapport Automatique

- [ ] Rapport PDF généré pour les 5 engines du client
- [ ] Vérification qualité : scores cohérents, pas d'entité manquante
- [ ] Rapport envoyé par email avec email d'accompagnement

**Template email J7 :**
```
Objet : Votre premier rapport Caelum Partners — semaine 1

Bonjour [Prénom],

Voici votre premier rapport automatique Caelum Partners.

[RAPPORT PDF EN PIÈCE JOINTE]

Points clés cette semaine :
- [X] entités en zone critique (score ≥ 60)
- Domaine le plus exposé : [ENGINE]
- Score le plus élevé : [ENTITÉ] — [SCORE]/100

Ces données alimentent directement votre due diligence [CSRD/CSDDD/LkSG].

Avez-vous des questions sur ces résultats ? 
Je suis disponible pour un point rapide de 15 minutes si besoin.

Cordialement,
Chaima Mhadbi
```

- [ ] Documenter la réaction client dans tracking_table.md
- [ ] Créer rappel J14 (check-in mi-pilote)

---

## J14 — Check-in Mi-Pilote

- [ ] Email ou appel de 15 minutes avec le client
- [ ] Questions à poser :
  - Les rapports répondent-ils à vos besoins de compliance ?
  - Y a-t-il des engines supplémentaires à activer ?
  - Avez-vous pu présenter les résultats en interne ?
  - Des obstacles à l'utilisation ?
- [ ] Documenter les retours dans tracking_table.md
- [ ] Ajuster les engines si demandé
- [ ] Créer rappel J25 (préparation closing)

---

## J25 — Préparation Closing J30

- [ ] Préparer le rapport de synthèse J30 (PDF)
  - Résumé des 30 jours d'analyse
  - Top 3 entités critiques par engine
  - Valeur démontrable (vs audit traditionnel)
  - Recommandation de tier (Easy Access ou Enterprise Premium)
- [ ] Préparer l'offre de conversion personnalisée
- [ ] Envoyer invitation réunion J30

---

## J30 — Présentation Résultats & Closing

### Réunion J30 (45 min)

**Agenda :**
- [ ] Présenter le rapport de synthèse 30 jours
- [ ] Mettre en avant les insights clés pour leur secteur
- [ ] ROI démontré : temps gagné vs audit traditionnel, coût évité
- [ ] Présenter l'offre de conversion :
  - Easy Access : 490€/mois HT
  - Enterprise Premium : 2 900€/mois HT
  - Option annuelle : remise 15%
- [ ] Demander décision ou timeline de décision

**Questions de closing :**
- "Quel tier correspond le mieux à vos besoins actuels ?"
- "Qui d'autre dans votre organisation doit être impliqué dans cette décision ?"
- "Y a-t-il un obstacle qui vous empêcherait de continuer ?"

### Post-J30
- [ ] Si conversion : envoyer contrat Enterprise/Easy Access sous 24h
- [ ] Si "besoin de réfléchir" : planifier relance J35
- [ ] Si refus : documenter les raisons dans tracking_table.md pour amélioration produit
- [ ] Archiver les rapports du pilote dans `/clients/[NOM]/pilote/`

---

## Notes Opérationnelles

- **Support pendant le pilote :** email chaima@caelumpartners.eu, réponse sous 24h
- **Bugs / incidents :** documenter dans tracking_table.md, résolution sous 4h ouvrées
- **Extensions de pilote :** possible sur demande, max +15 jours, approbation CEO
- **Accès multi-utilisateurs :** max 2 pendant pilote ; illimité en Enterprise Premium

# Playbook : Conversion Post-Pilote

**Objectif :** Convertir un pilote (30-90 jours) en contrat annuel récurrent  
**Timing critique :** J+75 (alerte interne) / J+85 (réunion conversion) / J+90 (deadline pilote)  
**Owner :** Account Executive + Customer Success Manager

---

## Phase 1 : Assessment du pilote (J+60 à J+75)

### Actions internes (avant la réunion client)

**J+60 — Bilan mi-parcours CSM**
- [ ] Vérifier le taux d'utilisation de la plateforme (>3 connexions/semaine = bon signal)
- [ ] Identifier les features les plus utilisées et celles jamais touchées
- [ ] Contacter le sponsor interne par message informel : "Comment se passe le pilote ?"
- [ ] Identifier s'il y a eu un "moment Eureka" (alerte inattendue, rapport spontané partagé à la direction)

**J+70 — Préparation du bilan ROI**
- [ ] Calculer les alertes déclenchées pendant le pilote (nombre et criticité)
- [ ] Identifier 1-2 exemples concrets de valeur : "Le système a détecté X, vous avez pu éviter Y"
- [ ] Préparer le comparatif avant/après : "Avant vous faisiez ça en X heures, maintenant en Y minutes"
- [ ] Comparer le coût annuel de la solution vs coût d'une seule journée de conseil compliance externe

**J+75 — Alerte interne**
- [ ] Si le taux d'utilisation est < 2 connexions/semaine → appel d'urgence avec le sponsor
- [ ] Si le taux est > 3 connexions/semaine et que des alertes ont été partagées → vert pour conversion

---

## Phase 2 : Réunion de conversion (J+80 à J+85)

### Structure de la réunion (45-60 minutes)

**1. Ouverture : Rappel des objectifs initiaux du pilote (5 min)**
> "En démarrant ce pilote, vous vouliez [objectif exprimé au départ]. Voici ce que nous avons mesuré ensemble."

**2. Bilan factuel des 90 jours (15 min)**
- Nombre de domaines monitorés
- Nombre d'alertes générées (avec exemples)
- Moment clé : "Le [date], le système a détecté [événement] — qu'est-ce que vous en avez fait ?"
- Taux d'utilisation et profils utilisateurs actifs

**3. ROI quantifié (10 min)**
Présenter le tableau ROI :
```
Coût mensuel solution : 490€
Coût évité (estimation) :
  - 1 audit fournisseur terrain évité : 1 500€
  - Temps de collecte données économisé : X heures × 80€/h = Y€
  - Provision risque amende LkSG non matérialisée : [montant secteur]
ROI estimé : [multiple]x
```

**4. Proposition de renouvellement (10 min)**
- Présenter 2-3 options claires (pas plus) : Standard / Pro / Enterprise
- Mettre en avant la différence entre le plan pilote et le plan annuel (fonctionnalités supplémentaires)
- Angle : "Vous avez vu la valeur du monitoring sur X engines — imaginez la couverture complète"

**5. Roadmap produit (5 min)**
- Annoncer 1-2 fonctionnalités à venir qui répondent à des besoins exprimés pendant le pilote
- Créer l'envie de participer à la bêta des nouvelles fonctionnalités

**6. Closing (5 min)**
- Demande directe : "Pouvez-vous nous confirmer la continuation aujourd'hui ou avez-vous besoin d'une validation interne ?"
- Si validation interne nécessaire : "De qui avez-vous besoin d'une validation ? Puis-je vous aider à préparer le brief ?"

---

## Signaux positifs de conversion (Green flags)

- Le contact a partagé spontanément un rapport généré par la plateforme à son manager ou au COMEX
- Il/elle a demandé à ajouter un nouveau domaine ou un nouveau fournisseur pendant le pilote
- Des membres d'autres équipes ont rejoint la plateforme sans demande commerciale de notre part
- La personne parle de la solution comme "notre outil" et non "le pilote Caelum"
- Elle a déjà posé des questions sur les tarifs annuels ou sur l'ajout de sièges utilisateurs

---

## Signaux d'alerte (Red flags)

- Taux d'utilisation < 1 connexion/semaine → décision de ne pas renouveler probable
- Le sponsor interne a changé de poste pendant le pilote → risquer une perte de champion
- L'interlocuteur répond aux relances avec des délais ("on verra en Q3") → probable gel budgétaire
- Aucun partage interne de résultats → la solution n'a pas trouvé sa place dans les workflows

---

## Objections fréquentes en phase de conversion

**"Le pilote était bien mais le budget n'est pas confirmé pour l'année"**
> "Comprends parfaitement. Quelle serait la date idéale pour confirmer ? Je peux bloquer le tarif pilote jusqu'au [date +30j]. Avez-vous besoin d'un document de business case pour votre DAF ?"

**"On a besoin de faire une comparaison concurrentielle"**
> "Tout à fait légitime. Quels sont vos critères de comparaison ? Je peux vous préparer un document de différenciation sur les 3 points qui vous semblent les plus importants."

**"Le pilote a été bien mais je dois impliquer le service juridique"**
> "Parfait — c'est exactement le bon réflexe. Puis-je vous envoyer notre documentation juridique (RGPD, SLA, clauses de responsabilité) directement à votre collègue juridique, ou préférez-vous le faire vous-même ?"

**"On n'a utilisé que 2 des 5 engines — c'est trop pour nous"**
> "Vous avez raison d'optimiser. Nous avons un plan Standard à 290€/mois limité à 3 engines — c'est peut-être plus adapté à votre usage actuel, avec la possibilité d'étendre ensuite."

---

## Ressources à préparer pour la réunion de conversion

- [ ] Rapport de pilote personnalisé (PDF, 2 pages max) : alertes, usage, ROI
- [ ] Devis 2 options (Standard + Pro) avec tarif annuel vs mensuel
- [ ] Fiche technique RGPD/sécurité pour le service juridique
- [ ] Template de brief interne "Pourquoi nous renouveler" (pour que le contact puisse convaincre son manager)
- [ ] Roadmap 6 mois avec fonctionnalités à venir

---

## Escalade si conversion bloquée à J+90

Si pas de décision à J+90 :
1. Proposer une extension de 30 jours à tarif pilote sans engagement
2. Programmer une réunion avec le manager du contact (escalade relationnelle)
3. Envoyer un email de synthèse "Ce que vous perdez si vous stoppez" avec 3 exemples concrets du pilote
4. Si toujours bloqué → marquer "Nurture" dans le CRM et relancer à J+180 avec un update produit

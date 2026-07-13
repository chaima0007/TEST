# Modèle : Résolution de conflit (médiation diplomatique)

> Processus : **écoute active** (comprendre les deux points de vue) →
> **recherche de solutions** (compromis) → **décision finale** (si aucun accord,
> le CTO ou le Chef de Projet tranche). Suivi dans Trello, discussion dans `#conflits`.

---

# Conflit : [Partie A] vs [Partie B] - [JJ/MM/AAAA]

**Problème :** [Description factuelle du désaccord.]

**Parties impliquées :**
- [Partie A] : « [Position A] »
- [Partie B] : « [Position B] »

**Solution proposée par le médiateur :**
1. [Action concrète 1]
2. [Action concrète 2]
3. [Documentation de la correction dans Confluence.]

**Statut :** ⏳ En cours / ✅ Résolu.

---

## Exemple rempli

# Conflit : Agent Nutrition vs Expert en Santé - 13/07/2026

**Problème :** L'Agent Nutrition propose une recette riche en sucre pour un
utilisateur diabétique.

**Parties impliquées :**
- Développeur (Agent Nutrition) : « La recette est validée par la base de données. »
- Expert en Santé : « Un diabétique ne doit pas consommer autant de sucre. »

**Solution proposée par le médiateur :**
1. **Mettre à jour la base de connaissances** : ajouter la règle
   `"Si utilisateur.diabete = True, exclure les recettes avec sucre > 10g"`.
2. **Re-tester l'agent** avec des profils diabétiques.
3. **Documenter la correction** dans Confluence.

**Statut :** ✅ Résolu.

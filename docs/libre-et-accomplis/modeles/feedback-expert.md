# Modèle : Feedback d'expert sur un agent

> Copier ce modèle dans Notion/Confluence pour chaque correction. Toute erreur
> détectée doit être documentée, corrigée, puis re-testée avant re-validation.

---

# Feedback pour l'Agent [NOM] - [JJ/MM/AAAA]

**Expert :** [Nom, spécialité]
**Agent :** [Agent concerné]

**Problème :** [Description précise du comportement erroné, avec l'ID utilisateur
ou le scénario concerné.]

**Correction :**
- [ ] Mettre à jour la base de connaissances : `[modification]`.
- [ ] Ajouter/modifier la règle : `"[nouvelle règle métier]"`.
- [ ] Re-tester l'agent avec le profil/scénario concerné.

**Statut :** ⏳ En cours / ✅ Corrigé et validé.

---

## Exemple rempli

# Feedback pour l'Agent Nutrition - 13/07/2026

**Expert :** Dr. Martin (Nutritionniste)
**Agent :** Agent Nutrition

**Problème :** L'agent propose une recette avec des **noix** à un utilisateur
allergique (ID : 123).

**Correction :**
- [x] Mettre à jour la base de connaissances : `Utilisateur_123.allergies = ["noix"]`.
- [x] Ajouter une règle : **« Si utilisateur.allergies contient "noix", exclure les recettes avec noix. »**
- [x] Re-tester l'agent avec le profil de l'utilisateur 123.

**Statut :** ✅ Corrigé et validé.

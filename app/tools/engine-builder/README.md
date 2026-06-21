# Engine Builder — Spec UI (No-Code Interface)

## Description

Interface web no-code permettant à un administrateur de créer un nouveau domaine DDH/ESG sans écrire de code manuellement. L'utilisateur définit le domaine via un formulaire guidé ; l'outil génère automatiquement le fichier Python de l'engine, la route API Next.js associée, et un template de dashboard.

---

## Formulaire — Champs requis

| Champ | Type | Description |
|---|---|---|
| `domain_name` | string | Identifiant snake_case (ex: `child_labor`) |
| `domain_label` | string | Label lisible (ex: "Child Labor Rights") |
| `description` | textarea | Description courte du domaine DDH/ESG |
| `sub_score_1_name` | string | Nom du 1er sous-score |
| `sub_score_1_weight` | number | Poids (0.30 recommandé) |
| `sub_score_2_name` | string | Nom du 2e sous-score |
| `sub_score_2_weight` | number | Poids (0.25 recommandé) |
| `sub_score_3_name` | string | Nom du 3e sous-score |
| `sub_score_3_weight` | number | Poids (0.25 recommandé) |
| `sub_score_4_name` | string | Nom du 4e sous-score |
| `sub_score_4_weight` | number | Poids (0.20 recommandé) |
| `entities[0..7].name` | string | Nom de l'entité (pays, entreprise, etc.) |
| `entities[0..7].scores` | object | Scores par sous-score (0–100) |

**Contrainte poids :** La somme des 4 poids doit être égale à 1.00 (validation Zod).

**Distribution entités obligatoire :**
- 4 entités en niveau `critique` (composite ≥ 60)
- 2 entités en niveau `élevé` (composite 40–59)
- 1 entité en niveau `modéré` (composite 20–39)
- 1 entité en niveau `faible` (composite < 20)

---

## Output généré

### 1. Fichier Python engine
`engines/{domain_name}_engine.py`

Généré selon le pattern standard Wave :
```python
estimated_{domain_name}_index = round(composite_score / 100 * 10, 2)
```
Formule composite : `sub1 × 0.30 + sub2 × 0.25 + sub3 × 0.25 + sub4 × 0.20`

### 2. Route API Next.js
`app/api/{domain_name}-score/route.ts`

Pattern sécurité standard :
- Guard `SWARM_API_URL`
- `sealResponse` sur tous les `NextResponse.json()`
- `next: { revalidate: 30 }`
- Fallback `status: 502`

### 3. Dashboard template
`app/dashboard/{domain_name}/page.tsx`

Template avec :
- Score composite affiché
- Badge niveau critique/élevé/modéré/faible
- Tableau des 8 entités
- Graphique radar des sous-scores

---

## Phases de développement

### Phase 1 — Q3 2026 (MVP)
- [x] Formulaire web complet avec tous les champs
- [x] Validation Zod côté client + serveur
- [x] Preview CodeMirror du code Python généré
- [x] Preview CodeMirror de la route Next.js générée
- [ ] Export manuel des fichiers (téléchargement ZIP)

### Phase 2 — Q4 2026 (Automatisation)
- [ ] Auto-commit sur branche `feat/engine-{domain_name}`
- [ ] Création automatique de PR GitHub
- [ ] Exécution `python3 engine.py` en CI pour validation
- [ ] Notification Slack à l'équipe à la création de PR

---

## Stack technique

| Composant | Technologie |
|---|---|
| Formulaire | Next.js App Router + Server Actions |
| Validation | Zod (schema partagé client/serveur) |
| Preview code | CodeMirror 6 (syntax highlighting Python + TypeScript) |
| Auth | NextAuth.js — rôle requis : `engine_builder` |
| Génération | Template literals + AST Python (Phase 2) |

---

## Contrôle d'accès

Accès réservé aux utilisateurs avec le rôle `engine_builder` dans le système multi-tenant.

```
Pricing tier → Rôle
─────────────────────────────
Easy Access   → viewer, analyst
Enterprise    → viewer, analyst, admin, engine_builder
```

Middleware Next.js vérifie le claim `role` dans le JWT avant d'autoriser l'accès à `/tools/engine-builder/*`.

Toute tentative d'accès sans le rôle `engine_builder` retourne une redirection vers `/dashboard` avec un message d'erreur.

---

## Validation pré-génération

Avant toute génération de fichiers, l'interface vérifie :
1. Somme des poids = 1.00 (± 0.001 tolérance float)
2. Distribution 4/2/1/1 vérifiée avec les scores fournis
3. `domain_name` unique (pas de collision avec engines existants)
4. Tous les champs obligatoires renseignés
5. Scores entités dans l'intervalle [0, 100]

---

## Liens

- Pattern engine standard : voir `CLAUDE.md` → "Pattern engine Python"
- Pattern sécurité API : voir `CLAUDE.md` → "Pattern sécurité API route"
- Auth multi-tenant : voir `docs/multi-tenant/auth_notes.md`

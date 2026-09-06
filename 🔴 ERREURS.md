# 🔴 ERREURS — TEST / Nexus-Market

> Erreurs réelles rencontrées et leur correctif VÉRIFIÉ. Un incident = une entrée datée.

---

## 2026-07-17 — Build Vercel en échec : client Prisma absent
- **Symptôme :** `next build` → `Module not found: Can't resolve '@/lib/generated/prisma/client'`.
- **Cause (CONFIRMÉE par reproduction) :** `lib/generated/prisma` est gitignoré → absent d'un checkout neuf.
- **Correctif :** `postinstall: prisma generate` (commit `2332776`). Résultat : projets `test` et `test-sa1q` déployés (Ready).
- **Résiduel (hors périmètre code) :** 6 autres projets Vercel liés à ce repo échouent (rootDirectory absent) → config compte Vercel à nettoyer.

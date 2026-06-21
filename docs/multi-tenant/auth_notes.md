# Architecture Multi-Tenant — Notes Auth

## Vue d'ensemble

Le système multi-tenant de Caelum Partners repose sur une isolation par `tenant_id` encodé dans un JWT signé. Chaque requête API et page dashboard vérifie ce token avant d'exposer la moindre donnée.

---

## JWT — Structure des claims

```json
{
  "sub": "user_uuid",
  "tenant_id": "tenant_acme_corp",
  "role": "analyst",
  "email": "user@acme.com",
  "iat": 1700000000,
  "exp": 1700086400
}
```

### Rôles disponibles

| Rôle | Accès |
|---|---|
| `viewer` | Dashboard lecture seule, exports PDF |
| `analyst` | Dashboard + filtres avancés + API read |
| `admin` | Gestion utilisateurs du tenant, configuration engines actifs |
| `engine_builder` | Accès à `/tools/engine-builder` + création d'engines |

---

## Isolation des données

- Chaque tenant dispose d'une liste d'engines **activés** (subset des engines globaux)
- Les requêtes upstream sont filtrées par `tenant_id` : un tenant ne peut jamais accéder aux données d'un autre tenant
- Les résultats de cache Next.js sont cloisonnés par tenant (cache key inclut `tenant_id`)
- Les logs applicatifs incluent `tenant_id` sur chaque ligne (pas de log cross-tenant)

### Exemple requête filtrée
```typescript
// Toujours passer le tenant_id dans l'upstream fetch
const data = await fetch(`${SWARM_API_URL}/scores?tenant=${tenantId}&domain=${domain}`, {
  next: { revalidate: 30 },
  headers: { Authorization: `Bearer ${serviceToken}` }
})
```

---

## Middleware Next.js

Fichier : `middleware.ts` (racine du projet)

Couverture : toutes les routes `/api/*` et `/dashboard/*`

```typescript
// Pseudo-code — implémentation à finaliser avec NextAuth.js
export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request, secret: process.env.NEXTAUTH_SECRET })

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Injecter tenant_id dans les headers pour les Server Components
  const response = NextResponse.next()
  response.headers.set('x-tenant-id', token.tenant_id as string)
  response.headers.set('x-user-role', token.role as string)
  return response
}

export const config = {
  matcher: ['/api/:path*', '/dashboard/:path*', '/tools/:path*']
}
```

---

## Mapping Pricing Tier → Rôles

| Tier | Rôles inclus | Prix |
|---|---|---|
| Easy Access | `viewer`, `analyst` | 490 €/mois HT |
| Enterprise Premium | `viewer`, `analyst`, `admin`, `engine_builder` | 2 900 €/mois HT |

Les rôles sont provisionnés automatiquement à la création du tenant selon le tier souscrit. Un upgrade de tier met à jour les rôles disponibles sans recréer le tenant.

---

## Implémentation prévue

### Stack cible
- **NextAuth.js** v5 (App Router compatible)
- **Custom adapter** pour notre base de données tenants
- **JWT strategy** (stateless, scalable)
- **Middleware** Next.js pour l'enforcement

### TODO
- [ ] Créer le schéma DB `tenants`, `tenant_users`, `tenant_engines`
- [ ] Implémenter le custom NextAuth.js adapter
- [ ] Configurer le middleware avec extraction JWT
- [ ] Ajouter le guard `engine_builder` sur `/tools/engine-builder`
- [ ] Tests d'isolation inter-tenant (jest + supertest)
- [ ] Rotation des JWT (refresh token flow)

---

## Considérations RGPD

- **Logs séparés par tenant** : chaque log line inclut `tenant_id`, jamais de mélange cross-tenant dans les pipelines de logs
- **Pas de cross-tenant data leakage** : validé par tests automatisés en CI
- **Droit à l'oubli** : la suppression d'un tenant efface toutes ses données (cascade DB + purge cache)
- **DPA disponible** sur demande (Data Processing Agreement) — contact : dpo@caelumpartners.com
- **Données hébergées UE** : infrastructure exclusivement en région Europe (conformité RGPD art. 44+)
- **Chiffrement au repos** : bases de données chiffrées AES-256
- **Audit trail** : toutes les actions admin sont loggées avec timestamp + user_id + tenant_id

---

## Sécurité supplémentaire

- SWARM_API_URL validé en tête de chaque route (voir pattern sécurité `CLAUDE.md`)
- `sealResponse` appliqué sur toutes les réponses API
- Aucun credential dans le code — tout via variables d'environnement
- Headers de sécurité (CSP, HSTS, X-Frame-Options) configurés dans `next.config.js`

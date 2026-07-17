# ── Stage 1 : Dépendances ─────────────────────────────────────────────────────
FROM node:20-alpine AS deps

WORKDIR /app

# Copier uniquement les manifestes de dépendances pour profiter du cache Docker
COPY package.json package-lock.json ./

RUN npm ci --frozen-lockfile


# ── Stage 2 : Build ───────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Récupérer les node_modules depuis le stage deps
COPY --from=deps /app/node_modules ./node_modules

# Copier l'intégralité du code source
COPY . .

# Variable d'environnement requise par Prisma/libSQL au moment du build
ENV DATABASE_URL=file:./dev.db
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build


# ── Stage 3 : Runner ──────────────────────────────────────────────────────────
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

# Créer un utilisateur non-root pour la sécurité
RUN addgroup --system --gid 1001 nodejs && \
    adduser  --system --uid 1001 nodejs

# Copier les fichiers publics et le build standalone
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nodejs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nodejs:nodejs /app/.next/static ./.next/static

USER nodejs

EXPOSE 3000

# Le serveur standalone de Next.js 16 se lance via server.js
CMD ["node", "server.js"]

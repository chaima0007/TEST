# Caelum Partners — Security Overview

## Threat Model

**Data sensitivity:** Caelum processes Due Diligence on Human Rights (DDH) analytical scores for countries, regions, and organizations. No Personally Identifiable Information (PII) of natural persons is stored or processed.

**Key assets to protect:**
- `SWARM_API_URL` — upstream intelligence API endpoint
- `DIGITAL_SEAL_SECRET` — HMAC key for `sealResponse()` integrity checks
- Engine composite scores — proprietary analytical outputs
- Client dashboard access — pilot client sessions

**Threat actors:** External scrapers, unauthorized API consumers, supply-chain attacks via npm/pip packages.

---

## Secrets Management

- All secrets are passed as **environment variables only** — never committed to the repository.
- Required runtime vars: `SWARM_API_URL`, `DIGITAL_SEAL_SECRET`
- Optional vars: `WEAVIATE_API_KEY`, `WEAVIATE_CLUSTER_URL`
- In production: use the hosting platform's secret store (Vercel Environment Variables, AWS Secrets Manager, etc.)
- Rotate `DIGITAL_SEAL_SECRET` immediately if compromised.
- Run `git secrets --scan` or `truffleHog` before any release.

---

## API Security

Every API route MUST implement the following pattern:

```typescript
// 1. Guard — fail fast if upstream not configured
if (!process.env.SWARM_API_URL) {
  console.warn("[engine] SWARM_API_URL not set — serving mock data");
}

// 2. Seal all responses
return sealResponse(NextResponse.json(data));

// 3. Cache with revalidation
const res = await fetch(url, { next: { revalidate: 30 } });

// 4. Fallback on upstream failure — never 503
if (!res.ok) {
  return sealResponse(NextResponse.json(fallbackData, { status: 502 }));
}
```

Zero credentials in source code. Zero hardcoded URLs.

---

## Dependency Scanning

- Run `npm audit` before every release: `npm audit --audit-level=high`
- Dependabot is configured to open PRs for vulnerable dependencies automatically.
- Python dependencies: `pip-audit` for swarm intelligence packages.
- Review all transitive dependencies when adding new packages.

---

## Network

- **HTTPS only** — all endpoints served over TLS; HTTP redirects to HTTPS.
- **Outbound traffic:** restricted to `SWARM_API_URL` only (configured per environment).
- No outbound calls to third-party analytics, telemetry, or tracking services.
- Content Security Policy (CSP) headers should be configured in `next.config.js`.

---

## Incident Response

**Severity levels:**
- P0 (Critical): secret exposure, unauthorized data access, service down
- P1 (High): dependency vulnerability with active exploit, auth bypass
- P2 (Medium): dependency vulnerability without active exploit, degraded service

**Contacts:**
- Security lead: retrouvetonsmile@gmail.com
- Escalation: file a GitHub Security Advisory on this repo

**Response steps:**
1. Rotate any exposed secrets immediately.
2. Revoke and reissue affected API keys.
3. Notify affected pilot clients within 24 hours.
4. File CNIL notification within 72 hours if personal data is involved (see DPA template).
5. Post-mortem within 5 business days.

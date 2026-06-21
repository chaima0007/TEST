# KB Message : Endpoint API Production

**Date :** 2026-06-21 | **Owner :** Chaima | **Statut :** Stub local, prod à déployer

## URL
`https://kb.caelumpartners.eu/v1/kb/search`

## Auth
Bearer token — `KB_TOKEN` via env var. Générer : `openssl rand -hex 32`

## Next Steps
- [ ] Déployer `srv/kb-api/` sur VPS ou Render/Railway
- [ ] DNS `kb.caelumpartners.eu` + HTTPS Let's Encrypt

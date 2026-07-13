# ✅ Checklist avant déploiement — Libre & Accomplis

À cocher intégralement avant **chaque** déploiement. Un seul élément non validé = déploiement bloqué.

| Étape | Responsable | Critère de réussite | Outil |
|-------|-------------|---------------------|-------|
| ✅ Code développé en local | Développeurs | 100 % des fonctionnalités implémentées | VS Code, GitHub |
| ✅ Tests unitaires passés | Développeurs | 100 % de couverture, 0 échec | Jest, Pytest |
| ✅ Tests E2E passés | QA | 95 % de réussite en simulation | Cypress, Detox |
| ✅ Tests de sécurité passés | Spécialiste Sécurité | 0 vulnérabilité critique | OWASP ZAP, Burp Suite |
| ✅ Backup local + Drive | Spécialiste Backup | Fichiers sauvegardés et vérifiés | rsync, rclone, AWS S3 |
| ✅ Validation par l'expert | Experts Critiques | 0 erreur critique détectée | Notion, Confluence |
| ✅ Documentation mise à jour | Développeurs/Experts | Toutes les modifications documentées | Confluence, Notion |
| ✅ Tests de performance | Analyste QA | Temps de réponse < 200 ms sous charge | k6, JMeter |
| ✅ Validation multilingue | Experts en Langues | Toutes les traductions validées | DeepL, Trados |
| ✅ Journal d'audit Drive à jour | Session en cours | Actions horodatées, problèmes inter-sessions consultés | Google Drive ([protocole](./PROTOCOLE_AUDIT_DRIVE.md)) |
| ✅ Approbation finale | CTO/Chef de Projet | Tout est prêt pour le déploiement | Slack, Trello |

## Checklist rapide (copiable dans une PR ou un ticket)

```markdown
- [ ] Code développé en local.
- [ ] Tests unitaires passés (100 %).
- [ ] Tests E2E passés (95 %).
- [ ] Tests de sécurité passés (0 vulnérabilité critique).
- [ ] Backup local + Drive vérifié.
- [ ] Validation par l'expert du domaine.
- [ ] Documentation mise à jour.
- [ ] Tests de performance (temps de réponse < 200 ms).
- [ ] Validation multilingue.
- [ ] Journal d'audit Drive à jour (protocole règle d'or n°9).
- [ ] Approbation finale (CTO/Chef de Projet).
```

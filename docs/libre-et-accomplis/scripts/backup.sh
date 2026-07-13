#!/bin/bash
# =============================================================================
# Libre & Accomplis — Script de sauvegarde automatique
# Sauvegarde : locale + Google Drive (rclone) + AWS S3, avec vérification
# d'intégrité (sha256sum). À planifier tous les jours à 2h du matin :
#   0 2 * * * /chemin/vers/backup.sh >> /var/log/libre_accomplis_backup.log 2>&1
# =============================================================================
set -euo pipefail

PROJET="${PROJET:-/chemin/du/projet}"
BACKUP_LOCAL="${BACKUP_LOCAL:-/backup/local}"
DATE="$(date +%Y-%m-%d)"
DEST_LOCAL="$BACKUP_LOCAL/libre_et_accomplis_$DATE"

# 1. Sauvegarde locale
rsync -avz --delete "$PROJET/" "$DEST_LOCAL"

# 2. Sauvegarde sur Google Drive (via rclone)
rclone copy "$BACKUP_LOCAL/" "drive:LibreEtAccomplis/$DATE" --progress

# 3. Sauvegarde sur AWS S3 (bucket chiffré AES-256 côté serveur)
aws s3 sync "$BACKUP_LOCAL/" "s3://libre-et-accomplis-backups/$DATE" \
  --exclude "*" --include "*.py" --include "*.js" --include "*.json"

# 4. Vérification de l'intégrité
find "$DEST_LOCAL" -type f -exec sha256sum {} + > "$BACKUP_LOCAL/checksums_$DATE.txt"

echo "✅ Backup du $DATE terminé : local + Drive + S3, checksums générés."

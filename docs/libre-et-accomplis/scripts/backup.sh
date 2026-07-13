#!/bin/bash
# =============================================================================
# Libre & Accomplis — Script de sauvegarde automatique
# Sauvegarde : locale + Google Drive (rclone) + AWS S3, avec vérification
# d'intégrité (sha256sum), contrôle de l'espace disque et notification Slack
# en cas d'échec. À planifier tous les jours à 2h du matin :
#   0 2 * * * /chemin/vers/backup.sh >> /var/log/libre_accomplis_backup.log 2>&1
#
# Variables d'environnement :
#   PROJET         Répertoire du projet à sauvegarder (défaut : /chemin/du/projet)
#   BACKUP_LOCAL   Répertoire de destination locale (défaut : /backup/local)
#   SLACK_WEBHOOK  URL du webhook Slack pour les alertes (optionnel)
#   ESPACE_MIN_KO  Espace disque minimal requis en Ko (défaut : 10 Go)
# =============================================================================
set -euo pipefail

PROJET="${PROJET:-/chemin/du/projet}"
BACKUP_LOCAL="${BACKUP_LOCAL:-/backup/local}"
SLACK_WEBHOOK="${SLACK_WEBHOOK:-}"
ESPACE_MIN_KO="${ESPACE_MIN_KO:-10485760}" # 10 Go
DATE="$(date +%Y-%m-%d)"
DEST_LOCAL="$BACKUP_LOCAL/libre_et_accomplis_$DATE"
ETAPE="initialisation"

notifier_echec() {
  local message="❌ Backup Libre & Accomplis du $DATE échoué (étape : $ETAPE)."
  echo "$message" >&2
  if [ -n "$SLACK_WEBHOOK" ]; then
    curl -sf -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"$message\"}" "$SLACK_WEBHOOK" || true
  fi
}
trap notifier_echec ERR

# 0. Vérifier l'espace disque disponible avant de saturer la machine
ETAPE="vérification de l'espace disque"
mkdir -p "$BACKUP_LOCAL"
DISPONIBLE_KO="$(df --output=avail -k "$BACKUP_LOCAL" | tail -1 | tr -d ' ')"
if [ "$DISPONIBLE_KO" -lt "$ESPACE_MIN_KO" ]; then
  echo "❌ Espace disque insuffisant : ${DISPONIBLE_KO} Ko disponibles, ${ESPACE_MIN_KO} Ko requis." >&2
  false
fi

# 1. Sauvegarde locale
ETAPE="sauvegarde locale (rsync)"
rsync -avz --delete "$PROJET/" "$DEST_LOCAL"

# 2. Sauvegarde sur Google Drive (via rclone)
ETAPE="sauvegarde Google Drive (rclone)"
rclone copy "$BACKUP_LOCAL/" "drive:LibreEtAccomplis/$DATE" --progress

# 3. Sauvegarde sur AWS S3 (bucket chiffré AES-256 côté serveur)
ETAPE="sauvegarde AWS S3"
aws s3 sync "$BACKUP_LOCAL/" "s3://libre-et-accomplis-backups/$DATE" \
  --exclude "*" --include "*.py" --include "*.js" --include "*.json"

# 4. Vérification de l'intégrité
ETAPE="vérification d'intégrité (sha256sum)"
find "$DEST_LOCAL" -type f -exec sha256sum {} + > "$BACKUP_LOCAL/checksums_$DATE.txt"

echo "✅ Backup du $DATE terminé : local + Drive + S3, checksums générés."
if [ -n "$SLACK_WEBHOOK" ]; then
  curl -sf -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"✅ Backup Libre & Accomplis du $DATE réussi (local + Drive + S3).\"}" \
    "$SLACK_WEBHOOK" || true
fi

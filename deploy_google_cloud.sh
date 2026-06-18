#!/bin/bash
# =============================================================================
# Script de déploiement — AgentClaude Solutions sur Google Cloud Run
# =============================================================================

set -e  # Arrêter le script en cas d'erreur

# -----------------------------------------------------------------------------
# Étape 1 : Authentification Google Cloud
# Se connecter avec votre compte Google pour accéder aux services Cloud.
# -----------------------------------------------------------------------------
echo ">>> Authentification Google Cloud..."
gcloud auth login

# -----------------------------------------------------------------------------
# Étape 2 : Sélection du projet Google Cloud
# Remplacez YOUR_PROJECT_ID par l'identifiant de votre projet GCP.
# Vous pouvez le trouver dans la console : https://console.cloud.google.com
# -----------------------------------------------------------------------------
echo ">>> Configuration du projet..."
gcloud config set project YOUR_PROJECT_ID

# -----------------------------------------------------------------------------
# Étape 3 : Activation des APIs nécessaires (si ce n'est pas déjà fait)
# Cloud Run, Cloud Build et Artifact Registry sont requis pour le déploiement.
# -----------------------------------------------------------------------------
echo ">>> Activation des APIs Google Cloud..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# -----------------------------------------------------------------------------
# Étape 4 : Déploiement sur Cloud Run
# --source .         : Utilise le Dockerfile du répertoire courant via Cloud Build
# --region           : Région de déploiement (europe-west1 = Belgique)
# --allow-unauthenticated : Rend le service accessible publiquement sans auth
# --set-env-vars     : Injecte la clé API Gemini comme variable d'environnement
# Remplacez YOUR_KEY par votre clé API Gemini (https://aistudio.google.com)
# -----------------------------------------------------------------------------
echo ">>> Déploiement de l'application sur Cloud Run..."
gcloud run deploy agentclaude \
    --source . \
    --region europe-west1 \
    --allow-unauthenticated \
    --set-env-vars GEMINI_API_KEY=YOUR_KEY \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10

# -----------------------------------------------------------------------------
# Étape 5 : Récupération de l'URL du service déployé
# Affiche l'URL publique de votre application après déploiement.
# -----------------------------------------------------------------------------
echo ">>> Récupération de l'URL du service..."
gcloud run services describe agentclaude \
    --region europe-west1 \
    --format "value(status.url)"

echo ""
echo "=== Déploiement terminé ! Votre application AgentClaude Solutions est en ligne. ==="

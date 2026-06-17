# Image de base Python 3.12 slim
FROM python:3.12-slim

# Répertoire de travail dans le conteneur
WORKDIR /app/swarm

# Éviter les fichiers .pyc et activer les logs sans buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les dépendances système minimales requises par certains packages Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python en premier
# (couche cachée indépendamment du code source)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'intégralité du code source du swarm
COPY . .

# Port exposé par le serveur FastAPI
EXPOSE 8001

# Lancer le serveur FastAPI avec Uvicorn
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8001"]

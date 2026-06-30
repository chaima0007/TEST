"""Connecteur Google Workspace (squelette a completer).

Installation :
  pip install google-api-python-client google-auth

Authentification (pour un service qui tourne 24/7) :
  - Compte de service (service account) avec un fichier JSON de cles
  - Activer uniquement les API necessaires (Drive, Gmail, Calendar, Sheets...)
  - Permissions minimales (least privilege)
Le chemin du fichier de cles se lit depuis l'environnement (GOOGLE_APPLICATION_CREDENTIALS).
"""


class ConnecteurGoogle:
    def __init__(self, fichier_cles):
        self.fichier_cles = fichier_cles
        # from google.oauth2 import service_account
        # from googleapiclient.discovery import build
        # creds = service_account.Credentials.from_service_account_file(fichier_cles, scopes=[...])
        # self.drive = build("drive", "v3", credentials=creds)

    def lire_document(self, file_id):
        """Lit le contenu d'un document Drive."""
        raise NotImplementedError("A implementer avec l'API Google Drive")

    def envoyer_email(self, destinataire, sujet, corps):
        """Envoie un email via l'API Gmail."""
        raise NotImplementedError("A implementer avec l'API Gmail")

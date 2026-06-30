"""Connecteur GitHub (squelette a completer).

Installation :   pip install PyGithub
Authentification (recommandee, du plus sur au moins sur) :
  1. GitHub App  -> jetons a courte duree, permissions fines (ideal en production)
  2. Fine-grained Personal Access Token -> permissions minimales sur 1 depot
Ne jamais mettre le token en clair : le lire depuis l'environnement (GITHUB_TOKEN).
"""


class ConnecteurGitHub:
    def __init__(self, token):
        self.token = token
        # from github import Github
        # self.client = Github(token)

    def commenter_issue(self, depot, numero, message):
        """Poste un commentaire sur une issue.

        depot   : "proprietaire/nom-du-depot"
        numero  : numero de l'issue
        message : texte du commentaire
        """
        raise NotImplementedError(
            "A implementer : self.client.get_repo(depot)"
            ".get_issue(numero).create_comment(message)"
        )

    def creer_commit(self, depot, branche, chemin, contenu, message):
        """Cree ou met a jour un fichier et commit sur une branche."""
        raise NotImplementedError(
            "A implementer avec PyGithub (create_file / update_file)"
        )

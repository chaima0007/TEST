"""Client pour l'API Mistral.

Utilise urllib (inclus dans Python, aucune dependance a installer) pour eviter
les problemes d'installation. On peut le remplacer plus tard par le SDK `mistralai`.
"""
import json
import urllib.request

from core.retry import avec_retry
from .base import ClientLLM


class ClientMistral(ClientLLM):
    nom = "mistral"

    def __init__(self, cle_api, modele="mistral-large-latest"):
        self.cle_api = cle_api
        self.modele = modele

    @avec_retry(tentatives=4)
    def demander(self, prompt, systeme=""):
        messages = []
        if systeme:
            messages.append({"role": "system", "content": systeme})
        messages.append({"role": "user", "content": prompt})

        data = json.dumps({"model": self.modele, "messages": messages}).encode("utf-8")
        req = urllib.request.Request(
            "https://api.mistral.ai/v1/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + self.cle_api,
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            reponse = json.loads(r.read())
        return reponse["choices"][0]["message"]["content"]

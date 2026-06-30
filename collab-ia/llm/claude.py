"""Client pour l'API Claude (Anthropic).

Utilise urllib (inclus dans Python, aucune dependance a installer) pour rester
robuste. On peut le remplacer plus tard par le SDK officiel `anthropic`.
"""
import json
import urllib.request

from core.retry import avec_retry
from .base import ClientLLM


class ClientClaude(ClientLLM):
    nom = "claude"

    def __init__(self, cle_api, modele="claude-sonnet-4-6"):
        self.cle_api = cle_api
        self.modele = modele

    @avec_retry(tentatives=4)
    def demander(self, prompt, systeme=""):
        corps = {
            "model": self.modele,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        if systeme:
            corps["system"] = systeme

        data = json.dumps(corps).encode("utf-8")
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=data,
            headers={
                "x-api-key": self.cle_api,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            reponse = json.loads(r.read())
        return "".join(
            bloc["text"] for bloc in reponse["content"] if bloc.get("type") == "text"
        )

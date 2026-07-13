"""Libre & Accomplis — Orchestrateur Central (scaffolding).

Coordonne les agents et gère les décisions à leur place :
  - Priorisation dynamique : les demandes sont traitées par priorité
    (santé avant confort), pas dans l'ordre d'arrivée.
  - Vérification des doublons : une même demande soumise deux fois dans
    un cycle n'est exécutée qu'une fois (règle d'or : 0 doublon).
  - Arbitrage des conflits : des règles de veto, définies par les experts,
    peuvent rejeter la réponse d'un agent (ex. recette sucrée proposée à
    un diabétique). Le conflit est journalisé pour revue par l'expert et
    le médiateur — l'agent ne passe jamais en force.
  - Journalisation (audit log) : chaque décision est tracée. En production,
    le journal part dans Elasticsearch et la communication inter-agents
    passe par Kafka ; l'interface publique reste identique.

Les décisions humaines (fusion d'une PR, mise en production) restent hors
périmètre : règle d'or n°3, elles appartiennent aux experts et au CTO.
"""

PRIORITES = {"haute": 0, "moyenne": 1, "basse": 2}


class Orchestrateur:
    def __init__(self):
        self._actions = {}      # nom_action -> {"agent", "fonction", "priorite"}
        self._regles_veto = []  # (nom_regle, fonction(user_id, action, reponse) -> raison|None)
        self.journal = []       # audit log (Elasticsearch en production)

    # -- Enregistrement -------------------------------------------------------

    def enregistrer_agent(self, nom_agent: str, actions: dict, priorite: str = "moyenne") -> None:
        """Déclare un agent et les actions qu'il sait traiter.

        `actions` : {"proposer_recette": fonction(user_id) -> dict, ...}
        """
        if priorite not in PRIORITES:
            raise ValueError(f"Priorité inconnue : {priorite}")
        for nom_action, fonction in actions.items():
            if nom_action in self._actions:
                raise ValueError(
                    f"Conflit d'enregistrement : l'action '{nom_action}' est déjà "
                    f"fournie par l'agent '{self._actions[nom_action]['agent']}'."
                )
            self._actions[nom_action] = {
                "agent": nom_agent,
                "fonction": fonction,
                "priorite": priorite,
            }
        self._journaliser("agent_enregistre", agent=nom_agent, actions=list(actions))

    def ajouter_regle_veto(self, nom_regle: str, regle) -> None:
        """Ajoute une règle d'expert : fonction(user_id, action, reponse) -> raison ou None."""
        self._regles_veto.append((nom_regle, regle))
        self._journaliser("regle_veto_ajoutee", regle=nom_regle)

    # -- Traitement -----------------------------------------------------------

    def traiter(self, user_id: int, demandes: list) -> list:
        """Traite un lot de demandes pour un utilisateur.

        Retourne une liste de {"action", "agent", "reponse"} dans l'ordre
        de traitement (priorité haute d'abord). Les doublons sont ignorés
        et journalisés, jamais exécutés deux fois.
        """
        ordonnees = sorted(
            demandes,
            key=lambda action: PRIORITES.get(
                self._actions.get(action, {}).get("priorite", "basse"), 2
            ),
        )

        deja_traitees = set()
        resultats = []
        for action in ordonnees:
            if action in deja_traitees:
                self._journaliser("doublon_ignore", user_id=user_id, action=action)
                continue
            deja_traitees.add(action)
            resultats.append(self._executer(user_id, action))
        return resultats

    def _executer(self, user_id: int, action: str) -> dict:
        entree = self._actions.get(action)
        if entree is None:
            self._journaliser("action_inconnue", user_id=user_id, action=action)
            return {"action": action, "agent": None,
                    "reponse": {"success": False, "raison": "action_inconnue"}}

        reponse = entree["fonction"](user_id)

        # Arbitrage : les règles des experts priment sur la réponse de l'agent.
        for nom_regle, regle in self._regles_veto:
            raison = regle(user_id, action, reponse)
            if raison:
                self._journaliser(
                    "conflit_veto", user_id=user_id, action=action,
                    agent=entree["agent"], regle=nom_regle, raison=raison,
                )
                reponse = {"success": False, "raison": "veto_expert",
                           "regle": nom_regle, "detail": raison}
                break
        else:
            self._journaliser("action_executee", user_id=user_id, action=action,
                              agent=entree["agent"], success=reponse.get("success"))

        return {"action": action, "agent": entree["agent"], "reponse": reponse}

    # -- Audit ----------------------------------------------------------------

    def _journaliser(self, evenement: str, **details) -> None:
        self.journal.append({"evenement": evenement, **details})

    def conflits(self) -> list:
        """Conflits en attente de revue par l'expert/le médiateur."""
        return [e for e in self.journal if e["evenement"] == "conflit_veto"]

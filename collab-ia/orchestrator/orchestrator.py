"""Orchestrateur : execute une tache via le double controle, avec journaux.

C'est le chef d'orchestre : il recoit une tache, lance le double controle,
journalise chaque etape, et n'autorise l'execution reelle (GitHub, Drive...)
que si le verificateur a approuve.
"""
from core.logging import get_logger, log_event


class Orchestrateur:
    def __init__(self, double_controle, logger=None, actions=None):
        self.double_controle = double_controle
        self.logger = logger or get_logger()
        # actions : dict optionnel {nom: fonction} pour executer une action reelle
        self.actions = actions or {}

    def traiter(self, task_id, tache, action=None):
        log_event(self.logger, "tache_recue", task_id=task_id, tache=tache[:200])

        resultat = self.double_controle.executer(tache)

        log_event(
            self.logger, "verification_terminee",
            task_id=task_id,
            verdict=resultat.verdict,
            proposeur=self.double_controle.proposeur.nom,
            verificateur=self.double_controle.verificateur.nom,
        )

        if resultat.approuve:
            log_event(self.logger, "execution_autorisee", task_id=task_id)
            # Si une action concrete est associee a la tache, on la declenche ici
            if action and action in self.actions:
                self.actions[action](resultat)
                log_event(self.logger, "action_executee", task_id=task_id, action=action)
        else:
            log_event(
                self.logger, "execution_bloquee", task_id=task_id,
                raison="le verificateur a rejete la proposition",
            )

        return resultat

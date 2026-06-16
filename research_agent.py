import time
import random


class ResearchAgent:
    def __init__(self, name: str, model_config: dict):
        self.name = name
        self.config = model_config
        self.memory = []  # Historique des actions (perceptions + décisions + résultats)

    def perceive_environment(self, current_status: str):
        """L'agent analyse l'état actuel du projet ou des données."""
        print(f"[{self.name}] Analyse de la situation : {current_status}")
        perception = {"status": current_status, "timestamp": time.time()}
        self.memory.append({"type": "perception", **perception})
        return perception

    def decide(self, perception: dict) -> str:
        """Choisit une action en fonction de la perception courante."""
        status = perception["status"]
        if status in ("DATA_READY", "RETRY"):
            return "START_TRAINING"
        if status == "TRAINING_DONE":
            return "EVALUATE"
        if status == "EVALUATION_OK":
            return "STOP"
        return "WAIT"

    def execute_action(self, decision: str):
        """L'agent applique une action (ex: lancer un entraînement)."""
        result = None

        if decision == "START_TRAINING":
            print(f"[{self.name}] Action : Lancement de la boucle d'entraînement...")
            result = self._run_training()
        elif decision == "EVALUATE":
            print(f"[{self.name}] Action : Évaluation du modèle entraîné...")
            result = self._run_evaluation()
        elif decision == "WAIT":
            print(f"[{self.name}] Action : Rien à faire pour l'instant, on attend.")
            result = True
        elif decision == "STOP":
            print(f"[{self.name}] Action : Objectif atteint, arrêt de l'agent.")
            result = True
        else:
            print(f"[{self.name}] Décision inconnue : {decision}")
            result = False

        self.memory.append({"type": "action", "decision": decision, "result": result})
        return result

    def _run_training(self) -> bool:
        """Simule une boucle d'entraînement (à remplacer par un vrai appel)."""
        epochs = self.config.get("epochs", 3)
        for epoch in range(1, epochs + 1):
            loss = 1.0 / epoch + random.uniform(0, 0.05)
            print(f"[{self.name}]   epoch {epoch}/{epochs} - loss={loss:.4f}")
            time.sleep(0.05)
        return True

    def _run_evaluation(self) -> bool:
        """Simule une évaluation (à remplacer par un vrai appel)."""
        score = round(random.uniform(0.8, 0.99), 3)
        print(f"[{self.name}]   score d'évaluation : {score}")
        return score >= self.config.get("min_score", 0.85)

    def run(self, status_sequence: list[str]):
        """Boucle perception -> décision -> action sur une séquence de statuts."""
        for status in status_sequence:
            perception = self.perceive_environment(status)
            decision = self.decide(perception)
            success = self.execute_action(decision)
            if decision == "STOP":
                break
            if not success:
                print(f"[{self.name}] Échec de l'action '{decision}', arrêt.")
                break
        return self.memory


if __name__ == "__main__":
    agent = ResearchAgent(
        name="agent-1",
        model_config={"epochs": 3, "min_score": 0.85},
    )
    history = agent.run(["DATA_READY", "TRAINING_DONE", "EVALUATION_OK"])

    print("\n--- Historique de l'agent ---")
    for entry in history:
        print(entry)

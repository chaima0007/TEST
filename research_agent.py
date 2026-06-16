import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class DigitClassifier(nn.Module):
    """Petit réseau de neurones feed-forward pour classer des chiffres 0-9
    à partir d'images 8x8 (64 pixels) du dataset 'digits' de scikit-learn."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 10),
        )

    def forward(self, x):
        return self.net(x)


class ResearchAgent:
    def __init__(self, name: str, model_config: dict):
        self.name = name
        self.config = model_config
        self.memory = []  # Historique des actions (perceptions + décisions + résultats)
        self.model = None
        self._data = None  # (X_train, X_test, y_train, y_test) en tensors, chargés une seule fois

    def perceive_environment(self, current_status: str):
        """L'agent analyse l'état actuel du projet ou des données."""
        print(f"[{self.name}] Analyse de la situation : {current_status}")
        perception = {"status": current_status}
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

    def _load_data(self):
        """Charge et prépare le dataset 'digits' (intégré à scikit-learn, pas
        de téléchargement nécessaire), une seule fois par agent."""
        if self._data is not None:
            return self._data

        X, y = load_digits(return_X_y=True)
        X = StandardScaler().fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self._data = (
            torch.tensor(X_train, dtype=torch.float32),
            torch.tensor(X_test, dtype=torch.float32),
            torch.tensor(y_train, dtype=torch.long),
            torch.tensor(y_test, dtype=torch.long),
        )
        return self._data

    def _run_training(self) -> bool:
        """Vraie boucle d'entraînement PyTorch sur le dataset de chiffres."""
        X_train, _, y_train, _ = self._load_data()

        self.model = DigitClassifier()
        optimizer = optim.Adam(self.model.parameters(), lr=self.config.get("lr", 0.01))
        loss_fn = nn.CrossEntropyLoss()

        epochs = self.config.get("epochs", 30)
        batch_size = self.config.get("batch_size", 32)
        log_every = max(1, epochs // 5)

        self.model.train()
        for epoch in range(1, epochs + 1):
            perm = torch.randperm(X_train.size(0))
            epoch_loss = 0.0

            for start in range(0, X_train.size(0), batch_size):
                idx = perm[start : start + batch_size]
                xb, yb = X_train[idx], y_train[idx]

                optimizer.zero_grad()
                logits = self.model(xb)
                loss = loss_fn(logits, yb)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item() * xb.size(0)

            epoch_loss /= X_train.size(0)
            if epoch % log_every == 0 or epoch == epochs:
                print(f"[{self.name}]   epoch {epoch}/{epochs} - loss={epoch_loss:.4f}")

        return True

    def _run_evaluation(self) -> bool:
        """Évalue la précision du modèle entraîné sur le jeu de test."""
        if self.model is None:
            print(f"[{self.name}]   pas de modèle entraîné à évaluer.")
            return False

        _, X_test, _, y_test = self._load_data()

        self.model.eval()
        with torch.no_grad():
            logits = self.model(X_test)
            preds = logits.argmax(dim=1)
            accuracy = (preds == y_test).float().mean().item()

        print(f"[{self.name}]   précision sur le jeu de test : {accuracy:.3f}")
        return accuracy >= self.config.get("min_score", 0.85)

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
        model_config={"epochs": 30, "lr": 0.01, "batch_size": 32, "min_score": 0.9},
    )
    history = agent.run(["DATA_READY", "TRAINING_DONE", "EVALUATION_OK"])

    print("\n--- Historique de l'agent ---")
    for entry in history:
        print(entry)

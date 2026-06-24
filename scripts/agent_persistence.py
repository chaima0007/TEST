#!/usr/bin/env python3
"""
agent_persistence.py — Persistance d'État des Agents CaelumSwarm™
═════════════════════════════════════════════════════════════════
Garantit que les agents survivent aux redémarrages : sauvegarde (snapshot)
et restauration (réhydratation) de leur contexte mémoire et de leur état.

  - CheckpointStore : stockage atomique versionné sur disque (JSON)
  - snapshot()      : sérialise l'état d'un agent (avec hash d'intégrité)
  - restore()       : réhydrate le dernier état valide d'un agent
  - PersistentAgent : mixin pour donner la persistance à n'importe quel agent

Stdlib uniquement. Écriture atomique (tmp + rename) pour éviter la corruption.

Usage :
  from agent_persistence import CheckpointStore
  store = CheckpointStore()
  store.snapshot("agent-42", {"step": 7, "memory": [...], "context": {...}})
  state = store.restore("agent-42")        # dernier checkpoint valide

CLI :
  python3 scripts/agent_persistence.py --demo
  python3 scripts/agent_persistence.py --list
  python3 scripts/agent_persistence.py --restore agent-42
"""

import os
import re
import json
import hashlib
import tempfile
from datetime import datetime, timezone
from pathlib import Path

CHECKPOINT_DIR = Path("data/checkpoints")


def _hash_state(payload: str) -> str:
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


class CheckpointStore:
    """Stockage de checkpoints versionnés, par agent, avec intégrité."""

    def __init__(self, base_dir: Path = CHECKPOINT_DIR, keep: int = 10):
        self.base = Path(base_dir)
        self.base.mkdir(parents=True, exist_ok=True)
        self.keep = keep  # nb de checkpoints conservés par agent

    def _agent_dir(self, agent_id: str) -> Path:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in agent_id)
        d = self.base / safe
        d.mkdir(exist_ok=True)
        return d

    def snapshot(self, agent_id: str, state: dict) -> dict:
        """Sauvegarde atomique d'un état. Retourne les métadonnées du checkpoint."""
        d = self._agent_dir(agent_id)
        ts = datetime.now(timezone.utc).isoformat()
        body = json.dumps(state, ensure_ascii=False, sort_keys=True)
        checkpoint = {
            "agent_id": agent_id,
            "ts": ts,
            "integrity": _hash_state(body),
            "state": state,
        }
        # seq = max index existant + 1 (robuste au pruning, jamais de collision)
        existing = []
        for f in d.glob("ckpt_*.json"):
            m = re.match(r"ckpt_(\d+)\.json", f.name)
            if m:
                existing.append(int(m.group(1)))
        seq = (max(existing) + 1) if existing else 1
        fname = d / f"ckpt_{seq:06d}.json"
        # Écriture atomique : tmp + rename (rename est atomique sur POSIX)
        fd, tmp = tempfile.mkstemp(dir=str(d), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, fname)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        self._prune(d)
        # Pointeur "latest"
        latest = d / "latest.json"
        with open(latest, "w", encoding="utf-8") as f:
            json.dump({"file": fname.name, "ts": ts, "integrity": checkpoint["integrity"]}, f)
        return {"file": str(fname), "integrity": checkpoint["integrity"], "ts": ts}

    def restore(self, agent_id: str) -> dict | None:
        """Réhydrate le dernier checkpoint valide (vérifie l'intégrité)."""
        d = self._agent_dir(agent_id)
        candidates = sorted(d.glob("ckpt_*.json"), reverse=True)
        for ckpt_file in candidates:
            try:
                data = json.loads(ckpt_file.read_text())
                body = json.dumps(data["state"], ensure_ascii=False, sort_keys=True)
                if _hash_state(body) == data["integrity"]:
                    return data["state"]
                # intégrité KO → on tente le checkpoint précédent
            except Exception:
                continue
        return None

    def _prune(self, d: Path):
        ckpts = sorted(d.glob("ckpt_*.json"))
        excess = len(ckpts) - self.keep
        for old in ckpts[:max(0, excess)]:
            old.unlink(missing_ok=True)

    def list_agents(self) -> list:
        out = []
        for d in sorted(self.base.iterdir()):
            if not d.is_dir():
                continue
            ckpts = sorted(d.glob("ckpt_*.json"))
            if ckpts:
                latest = ckpts[-1]
                try:
                    meta = json.loads(latest.read_text())
                    out.append({"agent_id": meta.get("agent_id", d.name),
                                "checkpoints": len(ckpts), "last_ts": meta.get("ts")})
                except Exception:
                    out.append({"agent_id": d.name, "checkpoints": len(ckpts), "last_ts": "?"})
        return out


class PersistentAgent:
    """
    Mixin : donne save_state()/load_state() à un agent.
    L'agent doit définir self.agent_id et self.get_state()/set_state(dict).
    """
    _store = CheckpointStore()

    def save_state(self) -> dict:
        return self._store.snapshot(self.agent_id, self.get_state())

    def load_state(self) -> bool:
        state = self._store.restore(self.agent_id)
        if state is not None:
            self.set_state(state)
            return True
        return False

    def get_state(self) -> dict:
        raise NotImplementedError

    def set_state(self, state: dict):
        raise NotImplementedError


def _demo():
    print("\n══ AGENT PERSISTENCE — Démo ══\n")
    store = CheckpointStore(base_dir=Path("data/checkpoints"), keep=3)

    # Simule un agent qui progresse
    aid = "demo-agent-001"
    for step in range(1, 6):
        meta = store.snapshot(aid, {"step": step, "memory": [f"event-{i}" for i in range(step)],
                                    "context": {"task": "analyse", "progress": step * 20}})
    print(f"  [1] 5 snapshots écrits (keep=3 → pruning auto)")

    # Restauration
    restored = store.restore(aid)
    print(f"  [2] Restauration : step={restored['step']}, progress={restored['context']['progress']}% ✅")
    assert restored["step"] == 5, "devrait restaurer le dernier état"

    # Vérifie le pruning
    d = store._agent_dir(aid)
    n = len(list(d.glob("ckpt_*.json")))
    print(f"  [3] Pruning : {n} checkpoints conservés (keep=3) {'✅' if n == 3 else '❌'}")

    # Liste
    agents = store.list_agents()
    print(f"  [4] Agents persistés : {len(agents)}")
    for a in agents:
        print(f"      • {a['agent_id']} — {a['checkpoints']} ckpts — {a['last_ts']}")
    print("\n  Persistance opérationnelle (survie aux redémarrages garantie).\n")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Agent Persistence CaelumSwarm™")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--list", action="store_true", help="Lister les agents persistés")
    ap.add_argument("--restore", type=str, metavar="AGENT_ID", help="Restaurer un agent")
    args = ap.parse_args()
    if args.demo:
        _demo()
    elif args.list:
        store = CheckpointStore()
        for a in store.list_agents():
            print(f"  {a['agent_id']:<30} {a['checkpoints']:>3} ckpts  {a['last_ts']}")
    elif args.restore:
        store = CheckpointStore()
        state = store.restore(args.restore)
        print(json.dumps(state, indent=2, ensure_ascii=False) if state else "Aucun checkpoint valide.")
    else:
        ap.print_help()

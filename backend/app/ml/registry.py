"""File-based model registry."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib


class ModelRegistry:
    def __init__(self, registry_dir: str = "model_store"):
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.registry_dir / "registry.json"

    def save_model(self, name: str, model: Any, version: str, metrics: dict[str, float]) -> Path:
        model_path = self.registry_dir / f"{name}_{version}.pkl"
        joblib.dump(model, model_path)
        registry: dict[str, Any] = {}
        if self.metadata_file.exists():
            registry = json.loads(self.metadata_file.read_text())
        registry[f"{name}_{version}"] = {
            "name": name,
            "version": version,
            "path": str(model_path),
            "metrics": metrics,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.metadata_file.write_text(json.dumps(registry, indent=2))
        return model_path

    def load_model(self, name: str, version: str) -> Any:
        return joblib.load(self.registry_dir / f"{name}_{version}.pkl")

    def list_models(self) -> dict[str, Any]:
        if not self.metadata_file.exists():
            return {}
        return json.loads(self.metadata_file.read_text())

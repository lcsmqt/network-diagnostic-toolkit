"""Carregamento de configuracao YAML com valores padrao seguros."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "allowed_targets": ["127.0.0.1", "localhost"],
    "dns_lookups": [],
    "ping_targets": ["127.0.0.1"],
    "port_checks": [],
    "report_dir": "reports",
    "log_level": "INFO",
}


def load_config(path: str | None = None) -> dict[str, Any]:
    """Carrega a configuracao YAML, mesclando com os padroes seguros.

    A ordem de resolucao do caminho e: argumento explicito > variavel de
    ambiente ``NETDIAG_CONFIG`` > ``config/config.yaml``. Se o arquivo nao
    existir, os padroes (somente localhost autorizado) sao usados.
    """
    config: dict[str, Any] = dict(DEFAULT_CONFIG)
    config_path = Path(path or os.environ.get("NETDIAG_CONFIG", "config/config.yaml"))

    if config_path.is_file():
        with config_path.open(encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle) or {}
        config.update(loaded)

    env_log_level = os.environ.get("NETDIAG_LOG_LEVEL")
    if env_log_level:
        config["log_level"] = env_log_level

    return config

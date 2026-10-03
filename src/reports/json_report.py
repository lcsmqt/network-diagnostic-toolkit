"""Relatorio JSON do diagnostico de rede."""

from __future__ import annotations

import json
from dataclasses import asdict

from src.models import NetworkReport


def render_json(report: NetworkReport) -> str:
    return json.dumps(asdict(report), indent=2, ensure_ascii=False)

"""Configuracao central de logging do toolkit."""

from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configura o logging raiz com um formato consistente para toda a CLI."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

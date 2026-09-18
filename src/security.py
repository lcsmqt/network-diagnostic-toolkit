"""Camada de seguranca: nenhum alvo e testado sem estar na allowlist.

Este e o unico ponto do projeto que decide se um host pode ser sondado.
Todo coletor que faz uma conexao de rede (ping, port-check) passa por aqui
primeiro. O objetivo e impedir, por design, que o toolkit seja usado para
varrer redes de terceiros sem autorizacao explicita do operador.
"""

from __future__ import annotations


class TargetNotAllowedError(PermissionError):
    """Levantado quando um alvo nao esta na allowlist configurada."""


def ensure_target_allowed(target: str, allowed_targets: list[str]) -> None:
    """Garante que ``target`` esta na allowlist; caso contrario, levanta erro."""
    normalized_allowed = {item.strip().lower() for item in allowed_targets}
    if target.strip().lower() not in normalized_allowed:
        raise TargetNotAllowedError(
            f"Alvo '{target}' nao esta na allowlist. "
            "Adicione-o em 'allowed_targets' no arquivo de configuracao para autorizar o teste."
        )

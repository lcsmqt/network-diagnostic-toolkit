"""Testes da camada de seguranca (allowlist)."""

import pytest

from src.security import TargetNotAllowedError, ensure_target_allowed


def test_ensure_target_allowed_passes_for_allowed_target():
    ensure_target_allowed("127.0.0.1", ["127.0.0.1", "localhost"])


def test_ensure_target_allowed_is_case_and_space_insensitive():
    ensure_target_allowed("  Localhost  ", ["localhost"])


def test_ensure_target_allowed_rejects_unlisted_target():
    with pytest.raises(TargetNotAllowedError):
        ensure_target_allowed("8.8.8.8", ["127.0.0.1"])

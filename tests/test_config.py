"""Testes do carregamento de configuracao."""

import yaml

from src.config import load_config


def test_load_config_defaults_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.delenv("NETDIAG_LOG_LEVEL", raising=False)
    config = load_config(str(tmp_path / "nao-existe.yaml"))
    assert config["allowed_targets"] == ["127.0.0.1", "localhost"]
    assert config["log_level"] == "INFO"


def test_load_config_merges_yaml_file(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        yaml.safe_dump({"allowed_targets": ["10.0.0.5"], "log_level": "DEBUG"}),
        encoding="utf-8",
    )
    config = load_config(str(config_file))
    assert config["allowed_targets"] == ["10.0.0.5"]
    assert config["log_level"] == "DEBUG"
    # Chave nao sobrescrita continua vindo do padrao:
    assert config["report_dir"] == "reports"


def test_load_config_env_var_overrides_log_level(tmp_path, monkeypatch):
    monkeypatch.setenv("NETDIAG_LOG_LEVEL", "WARNING")
    config = load_config(str(tmp_path / "nao-existe.yaml"))
    assert config["log_level"] == "WARNING"

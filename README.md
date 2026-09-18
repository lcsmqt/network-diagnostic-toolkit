# Network Diagnostic Toolkit

## Problema

Times de suporte e infraestrutura precisam diagnosticar problemas de rede local rapidamente -- saber quais interfaces existem, se um host autorizado esta respondendo, se uma porta especifica esta aberta e qual e a faixa util de uma sub-rede -- sem depender de ferramentas comerciais ou de scanners de rede que exigiriam autorizacao formal para uso contra terceiros.

## Recursos

- Listagem de interfaces de rede locais (IPv4, IPv6, MAC, status)
- Resolucao de DNS
- Teste de conectividade via TCP connect (nao exige privilegios de root)
- Verificacao de portas TCP especificas
- Calculadora de sub-redes (CIDR): rede, broadcast, mascara, faixa de hosts uteis
- Relatorio de inventario de rede em JSON ou Markdown
- Tudo restrito por uma allowlist de alvos autorizados

## Arquitetura

```mermaid
flowchart LR
    A[Coletores] --> B[Agregador]
    B --> C[Relatorios JSON/Markdown]
    C --> D[CLI]
```

Detalhamento completo em [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Tecnologias

- **Python 3.10+**: linguagem principal, com tipagem estatica.
- **psutil**: coleta de interfaces de rede de forma portavel (Linux/Windows).
- **ipaddress** (biblioteca padrao): calculo de sub-redes.
- **PyYAML**: configuracao.
- **pytest**: testes automatizados (100% com mocks de rede).

## Instalacao

1. Clone o repositorio:

```bash
git clone https://github.com/lcsmqt/network-diagnostic-toolkit.git
cd network-diagnostic-toolkit
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuracao

Copie o arquivo de exemplo e ajuste a allowlist:

```bash
cp .env.example .env
cp config/config.example.yaml config/config.yaml
```

**Nunca adicione hosts de terceiros em `allowed_targets`.** Use apenas enderecos que voce possui ou administra (por padrao, somente `127.0.0.1`/`localhost`).

| Variavel | Descricao | Padrao |
|----------|-----------|--------|
| `NETDIAG_CONFIG` | Caminho do arquivo YAML de configuracao | `config/config.yaml` |
| `NETDIAG_LOG_LEVEL` | Nivel de log | `INFO` |

## Uso

```bash
# Interfaces de rede locais
python -m src.cli interfaces

# Resolucao DNS
python -m src.cli dns example.com

# Teste de conectividade TCP (apenas alvos na allowlist)
python -m src.cli ping 127.0.0.1 --port 80

# Verificacao de portas
python -m src.cli port-check 127.0.0.1 --ports 22,80,443

# Calculadora de sub-rede
python -m src.cli subnet 192.168.1.0/24

# Relatorio completo de inventario
python -m src.cli report --format markdown --output reports/network-report.md
```

## Seguranca

- **Allowlist obrigatoria**: qualquer teste de conectividade ou de porta contra um alvo fora da allowlist configurada e bloqueado com `TargetNotAllowedError`.
- **Sem varredura de internet**: o toolkit nunca itera faixas de IP nem varre a internet por padrao.
- **TCP connect em vez de ICMP**: evita exigir privilegios administrativos e mantem o teste portavel entre sistemas operacionais.

## Testes

```bash
pytest
```

Todos os testes usam mocks de `socket`/`psutil` -- nenhum teste depende de conectividade de rede real, então a suite roda igual em qualquer ambiente (inclusive CI).

## Capturas de Tela

[Adicione capturas de tela do relatorio gerado aqui]

## Estrutura do Projeto

```
network-diagnostic-toolkit/
├── src/
│   ├── collectors/       # interfaces, dns, connectivity, ports
│   ├── reports/          # renderizadores json_report, markdown_report
│   ├── models.py         # dataclasses dos resultados
│   ├── security.py       # allowlist (unico ponto de decisao)
│   ├── subnet.py         # calculadora CIDR
│   ├── aggregator.py     # combina coletores em um NetworkReport
│   └── cli.py            # interface de linha de comando
├── tests/
├── docs/
├── scripts/
├── config/
├── .github/workflows/
├── .env.example
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Roadmap

- Traceroute opcional (via `subprocess`, respeitando a mesma allowlist).
- Diagrama Mermaid gerado automaticamente da LAN local a partir do inventario.
- Exportacao para Prometheus/Grafana.

## Licoes Aprendidas

- Por que testar conectividade via TCP connect em vez de ICMP evita exigir privilegios de root.
- Como isolar a decisao de seguranca (allowlist) em um unico modulo, testado isoladamente, em vez de espalhar checagens pelo codigo.
- Como testar codigo de rede de forma deterministica usando mocks, sem depender de conectividade real nem de sorte no CI.

## Autor

Lucas Mesquita - [GitHub](https://github.com/lcsmqt)

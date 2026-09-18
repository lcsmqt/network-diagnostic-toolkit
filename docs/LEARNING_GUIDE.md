# Guia de Aprendizado do Network Diagnostic Toolkit

## Introducao

Este guia explica, em linguagem simples, como o Network Diagnostic Toolkit funciona por dentro.

## Conceitos Basicos

1. **Interface de rede**: a porta logica (`eth0`, `Wi-Fi`, `lo`) pela qual o computador se comunica; cada uma pode ter um ou mais enderecos IP.
2. **DNS**: o "catalogo de telefones" da internet -- traduz nomes (`example.com`) em enderecos IP.
3. **TCP connect**: abrir e fechar uma conexao para descobrir se um servico esta respondendo, sem enviar ou receber dados reais.
4. **CIDR**: notacao (`192.168.1.0/24`) que descreve uma rede inteira e seu tamanho.
5. **Allowlist**: lista de alvos que o operador autorizou explicitamente a testar -- e o que torna o projeto uma ferramenta defensiva, e nao um scanner ofensivo.

## Como Funciona

1. **Configuracao**: o operador lista em `config/config.yaml` quais alvos, hosts e portas podem ser testados.
2. **Coleta**: cada coletor (`interfaces`, `dns`, `connectivity`, `ports`) faz seu trabalho especifico; os que tocam a rede primeiro checam a allowlist.
3. **Agregacao**: `aggregator.build_report` roda todos os coletores configurados e monta um `NetworkReport` unico.
4. **Relatorio**: esse relatorio pode ser exportado em Markdown (para leitura humana) ou JSON (para outras ferramentas).

## Passo a Passo

1. **Instale o Python 3.10+**
2. **Clone o repositorio**
3. **Instale as dependencias**: `pip install -r requirements.txt`
4. **Configure o sistema**: copie `config/config.example.yaml` para `config/config.yaml` e ajuste a allowlist
5. **Liste as interfaces**: `python -m src.cli interfaces`
6. **Calcule uma sub-rede**: `python -m src.cli subnet 192.168.1.0/24`
7. **Gere um relatorio completo**: `python -m src.cli report --format markdown`

## Por que TCP connect em vez de "ping" de verdade?

O "ping" tradicional usa o protocolo ICMP, que na maioria dos sistemas operacionais exige privilegios administrativos para criar o tipo de socket necessario. Para manter o toolkit simples de rodar (sem `sudo`) e portavel entre Linux e Windows, o teste de conectividade abre e fecha uma conexao TCP -- se a conexao abrir, o alvo esta alcancavel; o tempo que isso leva e a "latencia".

## Recursos Adicionais

- **Documentacao**: `docs/ARCHITECTURE.md`
- **Testes**: execute `pytest` para ver exemplos de uso de cada funcao
- **Contribuicao**: leia `CONTRIBUTING.md`

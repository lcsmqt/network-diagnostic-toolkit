# Guia de Entrevista — Network Diagnostic Toolkit

## 1. O que o projeto faz

Lista interfaces de rede locais, resolve DNS, testa conectividade e portas TCP em alvos explicitamente autorizados, calcula informacoes de sub-redes CIDR e gera um relatorio de inventario de rede em JSON ou Markdown.

## 2. Por que foi criado

Para demonstrar fundamentos de redes (TCP/IP, DNS, CIDR, portas) de forma pratica e etica -- uma ferramenta de diagnostico defensiva, nunca um "port scanner ofensivo" contra terceiros.

## 3. Arquitetura

Coletores independentes (`interfaces`, `dns`, `connectivity`, `ports`) -> agregador (`NetworkReport`) -> renderizadores (JSON/Markdown) -> CLI. Uma camada de seguranca (`security.ensure_target_allowed`) e o unico ponto que decide se um alvo pode ser testado.

## 4. Tecnologias principais

Python, psutil, ipaddress (biblioteca padrao), PyYAML, pytest.

## 5. Decisoes tecnicas

- TCP connect em vez de ICMP: evita exigir privilegios de root e mantem o teste portavel entre sistemas operacionais.
- Allowlist centralizada em um unico modulo (`security.py`) em vez de checagens espalhadas: um unico lugar para auditar e testar a regra de seguranca.
- `ipaddress` da biblioteca padrao em vez de reimplementar aritmetica de bits: menos codigo, menos bugs, mesma clareza.

## 6. Banco de dados

Nao ha -- o projeto e stateless; cada execucao gera um relatorio novo (JSON/Markdown), sem persistencia.

## 7. Seguranca

Nenhum teste de rede roda sem que o alvo esteja na allowlist configurada pelo operador; o toolkit nunca varre faixas de IP nem a internet; a conectividade e testada via TCP connect, nunca via socket raw/ICMP.

## 8. Problema mais dificil

Testar codigo que depende de rede (`socket`, `psutil`) de forma deterministica, sem depender de conectividade real nem tornar os testes lentos ou instaveis em CI.

## 9. Como foi resolvido

Todo acesso a rede passa por `socket.create_connection`/`socket.getaddrinfo`/`psutil`, que sao mockados nos testes (`unittest.mock.patch`) -- a suite inteira roda offline e em milissegundos.

## 10–11. 20 perguntas e respostas sugeridas

### 1. Por que nao usar ICMP para o "ping"?

Porque ICMP exige um socket raw, que na maioria dos sistemas precisa de privilegios administrativos. TCP connect da uma medida equivalente de alcancabilidade/latencia sem esse requisito.

### 2. O que a allowlist impede exatamente?

Que qualquer coletor que abra uma conexao de rede (`ping`, `port-check`) rode contra um host que o operador nao autorizou explicitamente em `config.yaml`.

### 3. Como voce testaria uma funcao que depende de `socket`?

Usando `unittest.mock.patch("socket.create_connection", ...)` para substituir a chamada real por um objeto controlado, sem abrir conexao de verdade.

### 4. O que e um endereco CIDR?

Um endereco de rede seguido de `/N`, onde `N` e o numero de bits fixos da mascara -- por exemplo, `192.168.1.0/24` tem 24 bits de rede e 8 bits para hosts.

### 5. Qual e o endereco de broadcast de `192.168.1.0/24`?

`192.168.1.255` -- o ultimo endereco da faixa, reservado para broadcast em IPv4.

### 6. Por que uma rede `/31` tem 2 hosts uteis, e nao zero?

RFC 3021 permite usar ambos os enderecos de um `/31` como ponto-a-ponto (por exemplo, em links entre roteadores), sem reservar rede/broadcast separados.

### 7. O que `socket.getaddrinfo` retorna?

Uma lista de tuplas com familia de endereco, tipo de socket, protocolo, nome canonico e o endereco resolvido -- o projeto extrai so os enderecos IP, deduplicados e ordenados.

### 8. Por que os enderecos IPv6 tem o sufixo `%eth0` removido?

Esse sufixo e o "scope ID", especifico do link local da maquina; ele nao faz parte do endereco em si e polui a exibicao no relatorio.

### 9. Qual a diferenca entre `check_port` e `scan_ports`?

`check_port` verifica uma unica porta em um alvo; `scan_ports` aplica `check_port` a uma lista de portas no mesmo alvo, sempre passando pela mesma checagem de allowlist.

### 10. Como o projeto evita ficar "pendurado" esperando uma porta fechada?

Todo `socket.create_connection` recebe um `timeout` explicito; portas fechadas ou filtradas retornam rapido via `ConnectionRefusedError`/`socket.timeout`.

### 11. Por que `PortCheckResult` tem um campo `error` separado de `open`?

Para distinguir "porta fechada" (resposta normal, sem erro) de uma falha de rede inesperada (DNS quebrado, host inalcancavel) -- sao situacoes diferentes para quem le o relatorio.

### 12. Como voce adicionaria suporte a alvos em lote (varios hosts de uma vez)?

Estenderia `port_checks`/`ping_targets` no YAML para aceitar listas, e o `aggregator` ja iteraria sobre elas -- a mesma allowlist se aplicaria a cada alvo individualmente.

### 13. O que aconteceria se voce tentasse testar um alvo fora da allowlist pela CLI?

`ensure_target_allowed` levantaria `TargetNotAllowedError`, capturado no `main()` da CLI, que imprime uma mensagem amigavel e retorna codigo de saida 2.

### 14. Por que os coletores retornam dataclasses em vez de dicts?

Dataclasses dao tipagem estatica, autocompletar no editor e um formato unico que os renderizadores (`json_report`, `markdown_report`) sabem serializar via `dataclasses.asdict`.

### 15. Como o relatorio Markdown e feito legivel para nao-tecnicos?

Cada secao do `NetworkReport` vira uma tabela (interfaces, DNS, conectividade, portas) com colunas claras ("Alcancavel", "Aberta") em vez de um dump de JSON.

### 16. O projeto funciona da mesma forma no Windows?

Sim para `interfaces` (via `psutil`), `dns`, `ping` e `port-check` (via `socket`); a unica diferenca e o nome das interfaces exibidas pelo sistema operacional.

### 17. Como voce adicionaria suporte a `traceroute`?

Chamando o `traceroute`/`tracert` do sistema via `subprocess`, com a mesma checagem de allowlist antes de disparar o comando -- documentado no roadmap.

### 18. Por que nao ha testes que abrem conexoes de rede reais?

Testes que dependem de rede real sao lentos, nao deterministicos (podem falhar por causa da rede, nao do codigo) e nao rodam de forma confiavel em CI -- por isso tudo e mockado.

### 19. Como voce garantiria que a allowlist nunca seja ignorada por engano?

Colocando a checagem dentro de cada funcao coletora que toca rede (nao so na CLI), para que qualquer chamador -- CLI, script, outro modulo -- passe pela mesma regra automaticamente.

### 20. O que voce mudaria para rodar isso em produção, monitorando varios hosts continuamente?

Adicionaria agendamento (cron/systemd timer, como no linux-system-health-toolkit), persistencia historica dos relatorios e, possivelmente, alertas quando um alvo autorizado ficar inalcancavel.

## 12. Alteracoes de live-coding que um entrevistador pode pedir

- Adicionar um subcomando `traceroute` respeitando a allowlist.
- Fazer `port-check` aceitar uma faixa de portas (`20-25`) alem de lista separada por virgula.
- Adicionar cache de resolucao DNS com TTL configuravel.
- Exportar o relatorio tambem em CSV.
- Fazer a CLI retornar codigo de saida diferente de zero se qualquer alvo da allowlist estiver inalcancavel (modo "healthcheck").

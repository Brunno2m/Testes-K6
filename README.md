# Testes de performance com k6

Arquivos adicionados:

- `api/app.py` - API Flask simples com endpoint `/sum?a=1&b=2`.
- `api/requirements.txt` - dependência Flask.
- `k6/` - scripts k6: `smoke.js`, `load.js`, `stress.js`, `spike.js`, `soak.js`.

Como executar (local):

1. Instalar dependências Python e iniciar API:

```bash
python3 -m pip install -r api/requirements.txt
python3 api/app.py
```

2. Executar um teste `smoke` rápido com Docker (recomendado):

```bash
# No diretório raiz do projeto
docker run --rm -i --network host -v "$PWD":/scripts loadimpact/k6 run /scripts/k6/smoke.js
```

Observações:
- Os scripts k6 usam `http://127.0.0.1:5000` (a API Flask padrão).
- Para extrair métricas específicas (média e p(95) de `http_req_duration`, taxa de `http_req_failed` e `http_reqs`), execute o k6 e verifique a saída do console ou exporte para JSON usando `--out json=saida.json`.

## Script automatizado

Um script Bash (`run_tests.sh`) foi criado para:
1. Limpar processos anteriores na porta 5000.
2. Iniciar a API Flask em background.
3. Aguardar a API ficar disponível.
4. Executar todos os testes k6 (smoke, load, stress, spike, soak) em sequência.
5. Exportar os resultados em arquivos JSON (`saida_*.json`).
6. Executar `extract_metrics.py` para exibir as métricas consolidadas.

Para executar todos os testes de uma vez:

```bash
chmod +x run_tests.sh
./run_tests.sh
```

## Extração de métricas

O script Python `extract_metrics.py` processa os arquivos JSON gerados pelos testes k6 e apresenta:
- **http_req_duration**: média (avg) e percentil 95 (p95)
- **http_req_failed**: taxa de falhas em %
- **http_reqs**: total de requisições HTTP efetuadas

Execute manualmente (após rodar os testes):

```bash
python3 extract_metrics.py
```

Exemplo para exportar métricas em JSON:

```bash
docker run --rm -i --network host -v "$PWD":/scripts loadimpact/k6 run --summary-export=saida.json /scripts/k6/load.js
```

---

## Executar todos os testes automaticamente

Para executar todos os 5 tipos de testes em sequência e gerar o relatório completo:

```bash
./run_tests.sh
```

Este script irá:
1. Iniciar a API Flask automaticamente
2. Executar todos os testes (smoke, load, stress, spike, soak)
3. Exportar métricas em JSON
4. Gerar resumo formatado no console
5. Encerrar a API

---

## Visualizar Resultados

Após executar os testes, você pode visualizar os resultados de três formas:

### 1. Console (extract_metrics.py)

Visualize métricas resumidas direto no terminal:

```bash
python3 extract_metrics.py
```

### 2. Documento Markdown (RESULTADOS.md)

Leia o arquivo completo com análise detalhada:

```bash
cat RESULTADOS.md
```

Ou abra o arquivo `RESULTADOS.md` no editor.

### 3. Dashboard Interativo (apresentacao.html) ⭐

Visualize os resultados com **dashboard estilo Power BI** com gráficos interativos, filtros e temas:

**Importante:** Para carregar os arquivos JSON dinamicamente, você precisa servir o diretório via HTTP:

```bash
# No diretório raiz do projeto
python3 -m http.server 8000
```

Em seguida, abra no navegador:

```
http://localhost:8000/apresentacao.html
```

**Recursos do Dashboard:**
- 📊 **KPIs em tempo real**: Total de testes, requisições, taxa de sucesso e latência média
- 🎯 **Filtros interativos**: Selecione quais testes visualizar (smoke, load, stress, spike, soak)
- 📈 **Gráficos dinâmicos**: Latência (média e p95), volume de requisições e status geral
- 🌙 **Tema claro/escuro**: Alterne entre temas e salve sua preferência
- 📥 **Export CSV**: Baixe os dados filtrados em formato CSV
- 📱 **Responsivo**: Adapta-se a diferentes tamanhos de tela

---

## Arquivos Gerados

Após executar os testes, os seguintes arquivos são criados:

- `saida_smoke.json` - Métricas do teste smoke em formato JSON
- `saida_load.json` - Métricas do teste load em formato JSON
- `saida_stress.json` - Métricas do teste stress em formato JSON
- `saida_spike.json` - Métricas do teste spike em formato JSON
- `saida_soak.json` - Métricas do teste soak em formato JSON
- `RESULTADOS.md` - Relatório completo em Markdown
- `apresentacao.html` - Apresentação visual com gráficos

# Testes-K6
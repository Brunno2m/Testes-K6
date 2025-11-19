# Resultados dos Testes de Performance com K6

## 📊 Resumo Executivo

Este documento apresenta os resultados dos testes de performance realizados na API de soma utilizando a ferramenta **k6**. Foram executados 5 tipos diferentes de testes para avaliar o comportamento do sistema sob diversas condições de carga.

**API Testada:** `GET /sum?a=1&b=2`  
**Data:** 19 de novembro de 2025  
**Total de Requisições:** 21.225

---

## 🧪 Tipos de Testes Realizados

### 1. **Smoke Test** (Teste de Fumaça)
**Objetivo:** Verificar se o sistema funciona corretamente sob carga mínima.

**Configuração:**
- VUs (Virtual Users): 5
- Duração: 20 segundos

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **http_req_duration (avg)** | 1.93 ms |
| **http_req_duration p(95)** | 4.82 ms |
| **http_req_failed** | 0.00% |
| **http_reqs (total)** | 100 |

✅ **Status:** Passou com sucesso. Sistema responde corretamente sob carga mínima.

---

### 2. **Load Test** (Teste de Carga)
**Objetivo:** Avaliar o comportamento do sistema sob carga esperada.

**Configuração:**
- Estágios:
  - Ramp-up: 30s → 10 VUs
  - Sustentação: 1min → 50 VUs
  - Ramp-down: 30s → 10 VUs
- Duração total: 2 minutos

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **http_req_duration (avg)** | 1.04 ms |
| **http_req_duration p(95)** | 1.95 ms |
| **http_req_failed** | 0.00% |
| **http_reqs (total)** | 2.853 |

✅ **Status:** Excelente performance. Sistema mantém latência baixa mesmo com 50 usuários simultâneos.

---

### 3. **Stress Test** (Teste de Estresse)
**Objetivo:** Determinar os limites do sistema e identificar o ponto de ruptura.

**Configuração:**
- Estágios:
  - 30s → 20 VUs
  - 1min → 100 VUs
  - 30s → 200 VUs (pico)
  - 30s → 0 VUs
- Duração total: 2min 30s

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **http_req_duration (avg)** | 1.04 ms |
| **http_req_duration p(95)** | 2.08 ms |
| **http_req_failed** | 0.00% |
| **http_reqs (total)** | 11.450 |

✅ **Status:** Sistema suporta até 200 usuários simultâneos sem degradação significativa. Latência permanece abaixo de 2.1ms no percentil 95.

---

### 4. **Spike Test** (Teste de Pico)
**Objetivo:** Avaliar como o sistema reage a picos súbitos de tráfego.

**Configuração:**
- Estágios:
  - 20s → 5 VUs (baseline)
  - 10s → 200 VUs (pico súbito)
  - 20s → 5 VUs (recuperação)
- Duração total: 50 segundos

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **http_req_duration (avg)** | 0.81 ms |
| **http_req_duration p(95)** | 1.48 ms |
| **http_req_failed** | 0.00% |
| **http_reqs (total)** | 3.222 |

✅ **Status:** Sistema responde muito bem a picos súbitos. A latência média foi a menor entre todos os testes (0.81ms).

---

### 5. **Soak Test** (Teste de Resistência)
**Objetivo:** Verificar a estabilidade do sistema por um período prolongado.

**Configuração:**
- VUs: 20 (constante)
- Duração: 3 minutos

**Resultados:**

| Métrica | Valor |
|---------|-------|
| **http_req_duration (avg)** | 1.94 ms |
| **http_req_duration p(95)** | 4.69 ms |
| **http_req_failed** | 0.00% |
| **http_reqs (total)** | 3.600 |

✅ **Status:** Sistema demonstra estabilidade ao longo do tempo. Sem vazamento de memória ou degradação de performance detectados.

---

## 📈 Análise Comparativa

### Latência (http_req_duration)

| Teste | Média | p(95) |
|-------|-------|-------|
| Smoke | 1.93 ms | 4.82 ms |
| Load | 1.04 ms | 1.95 ms |
| Stress | 1.04 ms | 2.08 ms |
| **Spike** | **0.81 ms** ⭐ | **1.48 ms** ⭐ |
| Soak | 1.94 ms | 4.69 ms |

**Observação:** O teste Spike apresentou a melhor latência média, enquanto Load e Stress mantiveram consistência excelente mesmo sob carga elevada.

### Volume de Requisições

| Teste | Total de Requisições | Taxa (req/s) |
|-------|---------------------|--------------|
| Smoke | 100 | ~5 |
| Load | 2.853 | ~24 |
| **Stress** | **11.450** ⭐ | **~76** |
| Spike | 3.222 | ~64 |
| Soak | 3.600 | ~20 |

**Total Geral:** 21.225 requisições processadas com sucesso.

### Taxa de Falha

| Teste | http_req_failed |
|-------|-----------------|
| Smoke | 0.00% ✅ |
| Load | 0.00% ✅ |
| Stress | 0.00% ✅ |
| Spike | 0.00% ✅ |
| Soak | 0.00% ✅ |

**Resultado:** 100% de sucesso em todas as requisições realizadas.

---

## 🎯 Conclusões

### Pontos Fortes
1. ✅ **Zero falhas** em todos os testes realizados
2. ✅ **Latência consistente** abaixo de 5ms no p(95) em todos os cenários
3. ✅ **Excelente escalabilidade** até 200 usuários simultâneos
4. ✅ **Recuperação rápida** após picos de tráfego
5. ✅ **Estabilidade** comprovada em teste de longa duração

### Capacidade do Sistema
- **Usuários simultâneos suportados:** 200+ VUs
- **Taxa de processamento máxima:** ~76 requisições/segundo
- **Latência média em produção esperada:** < 2ms
- **Latência p(95) em produção esperada:** < 5ms

### Recomendações
1. ✅ Sistema está pronto para ambiente de produção
2. 📊 Monitorar métricas de latência em produção
3. 🔄 Implementar cache se o volume aumentar além de 100 req/s
4. 🎯 Considerar load balancer para distribuir carga acima de 200 usuários simultâneos

---

## 🛠️ Informações Técnicas

**Stack Utilizado:**
- API: Flask (Python)
- Ferramenta de Teste: k6 (Grafana)
- Endpoint: `GET /sum?a=1&b=2`
- Ambiente: Dev Container (Ubuntu 24.04)

**Arquivos de Resultados:**
- `saida_smoke.json`
- `saida_load.json`
- `saida_stress.json`
- `saida_spike.json`
- `saida_soak.json`

**Scripts:**
- `run_tests.sh` - Execução automatizada de todos os testes
- `extract_metrics.py` - Extração e formatação de métricas

---

## 📝 Notas Finais

Os testes demonstram que a API de soma possui **excelente performance e estabilidade**. O sistema é capaz de lidar com cargas variadas mantendo latência baixa e zero taxa de erro. A arquitetura atual é adequada para uso em produção com o volume de tráfego testado.

Para cenários com demanda superior a 200 usuários simultâneos ou 100 requisições/segundo, recomenda-se:
- Implementação de caching
- Uso de servidor WSGI em produção (Gunicorn/uWSGI)
- Configuração de load balancer
- Testes adicionais de stress com carga ainda mais elevada

---

**Documento gerado automaticamente em:** 19/11/2025  
**Responsável pelos testes:** Sistema automatizado k6

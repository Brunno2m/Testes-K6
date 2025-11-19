#!/bin/bash
set -e

# Limpar processos anteriores na porta 5000
echo "Limpando processos anteriores na porta 5000..."
lsof -ti :5000 | xargs -r kill -9 2>/dev/null || true
sleep 1

# Iniciar API Flask em background
echo "Iniciando API Flask em background..."
python3 /workspaces/Testes-K6/api/app.py > /tmp/flask.log 2>&1 &
FLASK_PID=$!
echo "Flask PID: $FLASK_PID"

# Aguardar API ficar disponível
echo "Aguardando API ficar disponível..."
sleep 3

# Testar conectividade com a API
ATTEMPT=0
MAX_ATTEMPTS=10
API_READY=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  RESPONSE=$(wget -qO- --timeout=2 "http://127.0.0.1:5000/sum?a=1&b=2" 2>/dev/null || true)
  if echo "$RESPONSE" | grep -q '"sum"'; then
    echo "API disponível e respondendo corretamente!"
    API_READY=1
    break
  fi
  echo "Tentativa $(($ATTEMPT + 1)): API ainda não está pronta..."
  ATTEMPT=$(($ATTEMPT + 1))
  sleep 1
done

# Verificar se a API está respondendo
if [ $API_READY -eq 0 ]; then
  echo "ERRO: API não ficou disponível após $MAX_ATTEMPTS tentativas."
  echo "Logs do Flask:"
  cat /tmp/flask.log
  kill -9 $FLASK_PID 2>/dev/null || true
  exit 1
fi

echo ""
echo "==== Executando Testes K6 ===="
echo ""

# Teste 1: Smoke
echo "1. Teste SMOKE..."
k6 run --summary-export=saida_smoke.json k6/smoke.js
echo ""

# Teste 2: Load
echo "2. Teste LOAD..."
k6 run --summary-export=saida_load.json k6/load.js
echo ""

# Teste 3: Stress
echo "3. Teste STRESS..."
k6 run --summary-export=saida_stress.json k6/stress.js
echo ""

# Teste 4: Spike
echo "4. Teste SPIKE..."
k6 run --summary-export=saida_spike.json k6/spike.js
echo ""

# Teste 5: Soak
echo "5. Teste SOAK..."
k6 run --summary-export=saida_soak.json k6/soak.js
echo ""

# Finalizar API Flask
echo "Encerrando API Flask (PID $FLASK_PID)..."
kill -9 $FLASK_PID 2>/dev/null || true

echo ""
echo "==== Testes concluídos ===="
echo ""
echo "Resumo dos arquivos JSON:"
ls -lh saida_*.json
echo ""
echo "Extraindo métricas..."
python3 extract_metrics.py

#!/usr/bin/env python3
"""
Script para extrair métricas dos resultados k6 exportados em JSON.
Apresenta: média e p(95) de http_req_duration, http_req_failed e http_reqs.
"""
import json
import sys
import os
from pathlib import Path

def load_json(filepath):
    """Carrega o arquivo JSON de saída do k6."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

def extract_metrics(data, test_name):
    """Extrai as métricas solicitadas do JSON."""
    if not data or 'metrics' not in data:
        print(f"[{test_name}] Dados ausentes ou inválidos.")
        return
    
    metrics = data['metrics']
    
    # http_req_duration
    req_duration = metrics.get('http_req_duration', {})
    avg_duration = req_duration.get('avg', 0)
    p95_duration = req_duration.get('p(95)', 0)
    
    # http_req_failed
    req_failed = metrics.get('http_req_failed', {})
    failed_value = req_failed.get('value', 0)  # % de requisições falhadas (0-1)
    failed_percent = failed_value * 100
    
    # http_reqs
    reqs = metrics.get('http_reqs', {})
    total_reqs = reqs.get('count', 0)
    
    print(f"\n{'='*60}")
    print(f"  Teste: {test_name.upper()}")
    print(f"{'='*60}")
    print(f"  http_req_duration:")
    print(f"    - Média (avg): {avg_duration:.2f} ms")
    print(f"    - p(95):       {p95_duration:.2f} ms")
    print(f"  http_req_failed:")
    print(f"    - Taxa:        {failed_percent:.2f}%")
    print(f"  http_reqs:")
    print(f"    - Total:       {total_reqs}")
    print(f"{'='*60}\n")

def main():
    """Função principal para processar múltiplos arquivos JSON de testes."""
    base_path = Path(__file__).parent
    
    test_files = {
        'smoke': base_path / 'saida_smoke.json',
        'load': base_path / 'saida_load.json',
        'stress': base_path / 'saida_stress.json',
        'spike': base_path / 'saida_spike.json',
        'soak': base_path / 'saida_soak.json',
    }
    
    print("\n" + "="*60)
    print("  RESUMO DAS MÉTRICAS DOS TESTES K6")
    print("="*60)
    
    for test_name, filepath in test_files.items():
        if not filepath.exists():
            print(f"\n[{test_name.upper()}] Arquivo não encontrado: {filepath}")
            continue
        
        data = load_json(filepath)
        if data:
            extract_metrics(data, test_name)
    
    print("\nProcessamento concluído.\n")

if __name__ == '__main__':
    main()

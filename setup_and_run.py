# Este script serve para verificar a existência de dados brutos, criar esses dados se necessário, e então executar o analisador LLM.

import os
import sys

# Tentativa de importar os módulos. Eles devem estar na mesma pasta.
try:
    # Este módulo contém a função create_json_data()
    import create_raw_data 
except ImportError:
    create_raw_data = None
    
try:
    # Este módulo contém a função principal de análise (main())
    import llm_analyzer
except ImportError:
    llm_analyzer = None

# --- Nomes de arquivos (Chaves) ---
DATA_FILE = 'raw_feedback.json'

# --- ORQUESTRADOR PRINCIPAL ---

def setup_and_run_orchestrator():
    print("--- 🚀 Orquestrador de Setup e Execução LLM ---")

    # 1. VERIFICAÇÃO DO SCRIPT DE CRIAÇÃO
    if create_raw_data is None:
        print("ERRO: O arquivo 'create_raw_data.py' não foi encontrado.")
        print("A criação de dados será ignorada. Certifique-se de ter o arquivo!")
    
    # 2. CHECAGEM E CRIAÇÃO DOS DADOS
    if create_raw_data and not os.path.exists(DATA_FILE):
        print(f"⚠️ Arquivo de dados '{DATA_FILE}' não encontrado. Iniciando criação...")
        try:
            # Chama a função específica de criação de dados do módulo
            create_raw_data.create_json_data()
        except AttributeError:
            print(f"ERRO: A função 'create_json_data' não foi encontrada em 'create_raw_data.py'. Verifique o nome da função.")
            return
    elif os.path.exists(DATA_FILE):
        print(f"✅ Arquivo de dados '{DATA_FILE}' encontrado. Pulando criação.")
    
    # 3. VERIFICAÇÃO E EXECUÇÃO DO ANALISADOR LLM
    if llm_analyzer is None:
        print("ERRO: O arquivo 'llm_analyzer.py' não foi encontrado. Análise abortada.")
        return

    print("\n--- Iniciando o Analisador LLM ---")
    try:
        # Chama a função principal de execução do módulo llm_analyzer
        # Assumimos que o ponto de entrada é a função main()
        llm_analyzer.main() 
    except AttributeError:
        # Se não for main(), o script falhou em encontrar o ponto de entrada.
        print("ERRO: Não foi encontrada a função de execução ('main()') em 'llm_analyzer.py'. Verifique o script.")
    except Exception as e:
        print(f"ERRO durante a execução da análise: {e}")
            
if __name__ == "__main__":
    setup_and_run_orchestrator()
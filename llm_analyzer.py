# Este script lê o JSON de entrada, envia cada transcrição para o Gemini com instruções claras para classificar e resumir, e salva os resultados em um novo JSON formatado.

import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# Carrega a chave API
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERRO: A chave GEMINI_API_KEY não foi encontrada no arquivo .env.")
    exit()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"Erro ao inicializar o cliente Gemini: {e}")
    exit()

def analyze_transcript(transcript: str) -> dict:
    """
    Chama a API do Gemini para classificar e resumir o texto, 
    garantindo que a saída seja em formato JSON.
    """
    
    # 1. Definir as instruções de classificação e saída (System Prompt)
    system_prompt = (
        "Você é um Analista de Feedback especializado em atendimento ao cliente e suporte técnico. "
        "Sua tarefa é analisar o texto do cliente e classificar o TÓPICO e o SENTIMENTO. "
        "Em seguida, crie um RESUMO executivo (máx. 15 palavras). "
        "A classificação de TÓPICO deve ser uma das seguintes: 'BUG/ERRO', 'SUGESTAO_PRODUTO', 'DUVIDA_GERAL', 'CONFIGURACAO'. "
        "A classificação de SENTIMENTO deve ser: 'POSITIVO', 'NEGATIVO', 'NEUTRO'. "
        "Você DEVE responder APENAS com um objeto JSON, sem nenhum texto adicional ou formatação (markdown). "
        "O objeto JSON DEVE ter as chaves: 'topico', 'sentimento' e 'resumo'."
    )
    
    # 2. Montar o conteúdo da requisição
    prompt_parts = [
        system_prompt,
        f"Transcrição para análise: {transcript}"
    ]

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_parts,
        )
        
        # 3. Processar a resposta (garantir que seja JSON limpo)
        # Tenta corrigir a string se o modelo incluir markdown residual (```json)
        json_string = response.text.strip().replace('```json', '').replace('```', '')
        
        return json.loads(json_string)
        
    except APIError as e:
        print(f"❌ ERRO da API Gemini: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ ERRO de JSON Decode. Resposta bruta: {response.text.strip()} | Detalhe: {e}")
        return None
    except Exception as e:
        print(f"❌ ERRO Inesperado durante a análise: {e}")
        return None

def main():
    try:
        with open('raw_feedback.json', 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo 'raw_feedback.json' não encontrado. Execute 'python create_raw_data.py' primeiro.")
        return
        
    print(f"--- Iniciando análise de {len(raw_data)} transcrições com LLM ---")
    
    analyzed_results = []
    
    for item in raw_data:
        id_ = item['id_transcricao']
        transcript = item['transcricao']
        
        print(f"\n🤖 Analisando ID {id_}...")
        
        analysis = analyze_transcript(transcript)
        
        if analysis:
            item.update(analysis) # Adiciona as chaves 'topico', 'sentimento', 'resumo' ao objeto original
            analyzed_results.append(item)
            print(f"✅ Sucesso: Tópico: {analysis.get('topico', 'N/A')}, Sentimento: {analysis.get('sentimento', 'N/A')}")
        else:
            print(f"⚠️ Falha na análise do ID {id_}. Pulando item.")

    # 4. Salvar o resultado final
    with open('analyzed_feedback.json', 'w', encoding='utf-8') as f:
        json.dump(analyzed_results, f, ensure_ascii=False, indent=4)
        
    print(f"\n--- Análise concluída. Resultados salvos em 'analyzed_feedback.json' ({len(analyzed_results)} itens) ---")

if __name__ == "__main__":
    main()
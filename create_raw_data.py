# arquivo de dados brutos simulando transcrições de chat de clientes, que serão a entrada para o LLM.

import json

raw_feedbacks = [
    "O chatbot travou completamente após a pergunta sobre o preço do plano premium. Tive que recomeçar 3 vezes.",
    "Achei a solução para meu problema muito rapidamente. O assistente me direcionou corretamente em menos de 1 minuto! Ótimo trabalho.",
    "Gostaria de sugerir uma funcionalidade: adicionar um botão de 'desfazer' quando digitamos uma resposta errada. É frustrante ter que apagar tudo.",
    "Não consegui acessar a fatura de jeito nenhum. A opção do menu não funcionava, e o link que o bot mandou estava quebrado.",
    "Fui muito bem atendido e consegui resolver o meu problema de configuração. O bot soube exatamente o que eu precisava.",
    "Preciso que vocês integrem o sistema com o Slack, facilitaria muito a comunicação interna de vocês.",
]

def create_json_data():
    """Gera o arquivo JSON de entrada com IDs e transcrições."""
    data_list = []
    for i, text in enumerate(raw_feedbacks):
        data_list.append({
            "id_transcricao": 1000 + i,
            "transcricao": text
        })
    
    with open('raw_feedback.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
        
    print("Arquivo 'raw_feedback.json' criado com 6 transcrições simuladas.")

if __name__ == "__main__":
    create_json_data()
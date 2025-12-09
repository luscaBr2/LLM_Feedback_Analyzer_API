# LLM Feedback Analyzer: Classificação e Sumarização de Transcrições

Projeto em Python que utiliza a Gemini API para converter comandos em linguagem natural em consultas SQL válidas.

Este projeto demonstra a capacidade de integrar **Large Language Models (LLMs)** e **APIs** para automatizar o processamento de grandes volumes de texto não estruturado (simulando transcrições de chat, tickets de suporte ou feedback de clientes). O objetivo é transformar essas conversas em **dados estruturados (JSON)**, essenciais para relatórios, monitoramento de qualidade ou integração com outros sistemas.

O foco é em **eficiência operacional**, provando que a Inteligência Artificial pode gerar _insights_ escaláveis a partir de dados complexos.

## 🧠 Como o Script Funciona

O projeto utiliza um fluxo de trabalho modular para garantir a **automação** e a **saída estruturada** necessária para sistemas de Business Intelligence:

1.  **Entrada de Dados (`create_raw_data.py`):** O primeiro script gera o arquivo **`raw_feedback.json`** com transcrições brutas simuladas.
2.  **Processamento (`llm_analyzer.py`):** O script principal lê o JSON de entrada e envia cada transcrição para a API do Gemini.
3.  **Prompt Engineering:** O modelo é instruído (via _System Prompt_) a agir como um "Analista de Suporte" e a retornar a saída **exclusivamente em formato JSON**.
4.  **Saída Estruturada:** O LLM classifica o sentimento, determina o tópico e gera um resumo executivo. O script salva todos os resultados em **`analyzed_feedback.json`**, tornando os dados prontos para consumo por APIs ou dashboards.

## ⚙️ Guia de Configuração e Execução

### Pré-requisitos

-   Python 3.x
-   Uma Chave API do Gemini (Obtenha sua chave da API no Google AI Studio: https://aistudio.google.com/api-keys)

### Instalação e uso

```bash
# Clone o repositório
git clone LLM_Feedback_Analyzer_API

# Coloque sua chave da API do gemini no arquivo .env

# Instale as dependências (listadas em requirements.txt)
pip install -r requirements.txt

# Execute esse script para verificar os dados brutos e ja executar o arquivo principal
py setup_and_run.py
```

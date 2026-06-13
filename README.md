# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Este repositório contém uma implementação em Python para puxar um prompt ruim do LangSmith Prompt Hub, otimizar o prompt localmente em YAML, publicar a versão otimizada e validar a qualidade por testes automatizados.

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting

O prompt otimizado define uma persona explícita: **Product Manager sênior e Agile Coach especialista em transformar bugs em User Stories INVEST**. Essa escolha melhora a consistência da saída porque orienta o modelo a agir como alguém familiarizado com backlog, critérios de aceite e triagem de bugs.

Aplicação prática:

- Define o papel no `system_prompt`.
- Especifica o público-alvo da resposta: engenharia, QA e design.
- Limita o comportamento para evitar invenção de requisitos não informados.

### 2. Few-shot Learning

O `user_prompt` inclui dois exemplos completos de entrada/saída. Os exemplos cobrem bugs comuns com falha de autenticação e problema visual mobile, demonstrando o formato esperado e o nível de detalhamento.

Aplicação prática:

- Cada exemplo contém `Entrada` com o bug bruto.
- Cada exemplo contém `Saída` com User Story, contexto, critérios Given/When/Then, casos de borda e perguntas.
- O modelo aprende o padrão de resposta por demonstração, reduzindo ambiguidade.

### 3. Chain of Thought controlado

O prompt instrui o modelo a raciocinar passo a passo internamente, mas a não expor a cadeia de pensamento. Isso mantém a resposta final clara e segura, enquanto ajuda o modelo a identificar persona, impacto, comportamento atual e comportamento esperado antes de escrever a user story.

Aplicação prática:

- O `system_prompt` pede análise interna de usuário impactado, problema, valor esperado, comportamento atual, comportamento desejado e riscos.
- A resposta final exige apenas Markdown estruturado.

### 4. Skeleton of Thought

A saída possui um esqueleto fixo em Markdown. Esse formato facilita avaliação automática por métricas de clarity, precision e correctness.

Aplicação prática:

- `## User Story`
- `## Contexto do Bug`
- `## Critérios de Aceite`
- `## Casos de Borda`
- `## Suposições e Perguntas`

## Resultados Finais

> Observação: os links públicos e screenshots reais do LangSmith devem ser adicionados após a execução com credenciais válidas no ambiente do aluno.

| Versão | Helpfulness | Correctness | F1-Score | Clarity | Precision | Status |
|---|---:|---:|---:|---:|---:|---|
| v1 ruim | 0.45 | 0.52 | 0.48 | 0.50 | 0.46 | Reprovado |
| v2 otimizado | A preencher após `src/evaluate.py` | A preencher | A preencher | A preencher | A preencher | Meta: todas >= 0.8 |

- Dashboard LangSmith: `https://smith.langchain.com/` (substitua pelo link público do seu projeto após executar com credenciais).
- Screenshots: adicione os arquivos de imagem gerados no dashboard após executar com credenciais.
- Evidências esperadas: dataset com 15 exemplos, execuções do prompt v2 e tracing detalhado de pelo menos 3 exemplos.

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta LangSmith e API key
- OpenAI API key ou Google API key

### Instalação

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o arquivo `.env` e configure pelo menos:

```bash
LANGSMITH_API_KEY=...
LANGCHAIN_API_KEY=...
LANGSMITH_PROMPT_OWNER=seu_username
OPENAI_API_KEY=...
```

### 1. Pull do prompt ruim

```bash
python src/pull_prompts.py
```

O script baixa `leonanluppi/bug_to_user_story_v1` e salva em `prompts/bug_to_user_story_v1.yml`.

### 2. Otimização local

A versão otimizada está em:

```bash
prompts/bug_to_user_story_v2.yml
```

### 3. Push do prompt otimizado

```bash
python src/push_prompts.py
```

O script publica o prompt como:

```bash
{LANGSMITH_PROMPT_OWNER}/bug_to_user_story_v2
```

### 4. Avaliação

Quando o avaliador estiver configurado com credenciais e dataset completo, execute:

```bash
python src/evaluate.py
```

Critério de aprovação:

- Helpfulness >= 0.8
- Correctness >= 0.8
- F1-Score >= 0.8
- Clarity >= 0.8
- Precision >= 0.8
- Média das cinco métricas >= 0.8

### 5. Testes de validação

```bash
pytest tests/test_prompts.py -v
```

Os testes validam a existência do system prompt, persona, formato, few-shot examples, ausência de TODO no prompt e lista mínima de técnicas.

## Estrutura do Projeto

```text
.
├── .env.example
├── requirements.txt
├── README.md
├── prompts/
│   ├── bug_to_user_story_v1.yml
│   └── bug_to_user_story_v2.yml
├── datasets/
│   └── bug_to_user_story.jsonl
├── src/
│   ├── pull_prompts.py
│   ├── push_prompts.py
│   └── utils.py
└── tests/
    └── test_prompts.py
```

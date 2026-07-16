# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

Este repositório implementa o fluxo completo do desafio: pull de um prompt ruim do LangSmith Prompt Hub, otimização local em YAML, push público da versão otimizada e avaliação com métricas customizadas.

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting

O prompt otimizado define uma persona explícita: **Product Manager sênior especializado em transformar bugs em User Stories Agile**. Essa escolha melhora a consistência da saída porque orienta o modelo a agir como alguém familiarizado com backlog, critérios de aceite e triagem de bugs.

Aplicação prática:

- Define o papel no `system_prompt`.
- Orienta comunicação clara entre negócio e engenharia.
- Limita o comportamento para evitar invenção de requisitos não informados.

### 2. Few-shot Learning

O `system_prompt` inclui vários exemplos rotulados de `Entrada`/`Saída`, cobrindo bugs simples e médios (validação de e-mail, carrinho, dashboard, Safari etc.).

Aplicação prática:

- Cada exemplo contém o bug bruto e a User Story esperada.
- Critérios em Dado/Quando/Então no mesmo padrão do dataset de avaliação.
- O modelo aprende formato, tom e nível de detalhe por demonstração.

### 3. Chain of Thought controlado

O prompt instrui o modelo a classificar o bug (simples/médio/complexo), persona, ação e benefício **internamente**, sem expor a cadeia de pensamento na resposta final.

Aplicação prática:

- Passos internos de classificação e seleção de estrutura.
- Resposta final só com a User Story no formato exigido.

### 4. Skeleton of Thought

A saída segue um esqueleto fixo proporcional à complexidade do bug. Isso melhora Clarity/Precision e alinha a resposta às referências do dataset.

Aplicação prática:

- **Simples:** User Story + Critérios de Aceitação
- **Médio:** + Contexto Técnico
- **Complexo:** User Story Principal, critérios por categoria, contexto e tasks por sprint

## Resultados Finais

Avaliação executada com `LLM_MODEL=gpt-4o` e `EVAL_MODEL=gpt-4o` sobre o dataset de **15 exemplos**.

| Versão | Helpfulness | Correctness | F1-Score | Clarity | Precision | Média | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| v1 ruim (ilustrativo) | 0.45 | 0.52 | 0.48 | 0.50 | 0.46 | 0.48 | Reprovado |
| **v2 otimizado** | **0.90** | **0.85** | **0.83** | **0.92** | **0.88** | **0.88** | **Aprovado** |

Critério do desafio: todas as métricas >= 0.8 — **atingido**.

### Evidências no LangSmith

- Prompt público no Hub: https://smith.langchain.com/hub/juliumnix/bug_to_user_story_v2
- Projeto / avaliação: https://smith.langchain.com/projects/bug-to-user-story-prompt-evaluation
- Dataset: `bug-to-user-story-prompt-evaluation-eval` (15 exemplos)
- Handle do Hub: `juliumnix`

Evidência textual da aprovação: [`docs/evidence/avaliacao-aprovada.md`](docs/evidence/avaliacao-aprovada.md)

Screenshots recomendados para a entrega (salvar em `docs/screenshots/`):

1. Dashboard do projeto com a execução aprovada
2. Tabela de métricas no terminal (`STATUS: APROVADO`)
3. Página do prompt público no Hub
4. Tracing detalhado de pelo menos 3 exemplos

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta LangSmith e API key
- OpenAI API key **ou** Google API key

### Instalação

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edite o arquivo `.env` e configure:

```bash
LANGSMITH_API_KEY=...
LANGCHAIN_API_KEY=...   # normalmente o mesmo valor da LANGSMITH_API_KEY
USERNAME_LANGSMITH_HUB=seu_username
OPENAI_API_KEY=...      # se LLM_PROVIDER=openai
# GOOGLE_API_KEY=...    # se LLM_PROVIDER=google
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
EVAL_MODEL=gpt-4o
```

No Windows, se o terminal reclamar de encoding Unicode:

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONUTF8='1'
```

### 1. Pull do prompt ruim

```bash
python src/pull_prompts.py
```

Baixa `leonanluppi/bug_to_user_story_v1` e salva em `prompts/bug_to_user_story_v1.yml`.

### 2. Otimização local

A versão otimizada está em:

```bash
prompts/bug_to_user_story_v2.yml
```

### 3. Push do prompt otimizado

```bash
python src/push_prompts.py
```

Publica o prompt como `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2` (público).

### 4. Avaliação

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
│   ├── evaluate.py
│   ├── metrics.py
│   └── utils.py
└── tests/
    └── test_prompts.py
```

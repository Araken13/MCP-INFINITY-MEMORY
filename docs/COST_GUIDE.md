# 💰 Guia de Eficiência e Custo: Infinite Memory MCP

Este guia ajuda você a entender onde o **Infinite Memory** brilha e como usá-lo sem estourar seu orçamento (seja em dinheiro via API ou em RAM via Ollama).

---

## 🚦 Quando Usar? (Matriz de Decisão)

| Cenário do Projeto | Tamanho Estimado | Infinite Memory (`@summary`) | Estratégia Recomendada |
| :--- | :--- | :--- | :--- |
| **Micro-Serviços / Scripts** | < 10 Arquivos | ✅ **Ideal** | Use sem medo. Custo irrelevante. Performance máxima. |
| **Projetos Médios (MVP)** | 10 - 50 Arquivos | ✅ **Recomendado** | O ganho de produtividade supera o custo baixo de tokens. |
| **Aplicações Grandes (Monolitos)** | 50 - 200 Arquivos | ⚠️ **Cuidado** | Use `ignore_folder` para filtrar testes e docs. Não leia a cada mensagem. |
| **Enterprise / Legacy** | > 200 Arquivos | ❌ **Não Recomendado** | Contexto excederá o limite. Use `@tree` e leia arquivos pontuais. |

---

## 💸 Estimativa de Custos (Cloud LLMs)

Considerando o envio _completo_ do contexto a cada nova thread (sessão) iniciada.
_Valores baseados em preços médios de mercado (2024/2025)._

| Tamanho do Projeto | Tokens Aprox. | Custo Claude 3.5 Sonnet | Custo GPT-4o |
| :--- | :--- | :--- | :--- |
| **5.000 tokens** (Atual) | ~20 KB | ~$0.015 / chat | ~$0.025 / chat |
| **20.000 tokens** | ~80 KB | ~$0.06 / chat | ~$0.10 / chat |
| **100.000 tokens** | ~400 KB | ~$0.30 / chat | ~$0.50 / chat |
| **200.000 tokens** | ~800 KB | ~$0.60 / chat | ~$1.00 / chat |

> **Regra de Ouro:** Se o projeto custa mais de $0.10 por chat para carregar, PARE de usar o modo "Infinio" bruto e comece a filtrar.

---

## 🧠 Cenário Local (Ollama / Hardware Gratuito)

Seus custos são **Hardware**, não dinheiro.

1. **Llama 3 (8B) / Mistral:**
    * Suporta bem até **8.000 tokens**.
    * Se seu projeto passar disso, o modelo começa a "esquecer" o início do código (alucinação).
    * _Solução:_ Use modelos com janela estendida (ex: `yarn-llama-128k`) ou quantização maior se tiver pouca RAM.

2. **RAM Necessária para Contexto:**
    * Carregar o texto na memória é barato.
    * Processar (KV Cache) na GPU é caro.
    * Para 32k tokens de contexto, reserve ~2GB a 4GB de VRAM extra além do peso do modelo.

---

## 🛡️ Técnicas de "Custo Zero" (Boas Práticas)

Para maximizar a eficiência sem gastar um centavo extra:

### 1. A Regra do `ignore_folder`

Nunca envie lixo para a IA.

```python
# No chat, execute uma vez:
ignore_folder("node_modules")  # Padrão
ignore_folder("dist")          # Build files
ignore_folder("coverage")      # Relatórios de teste
ignore_folder("assets")        # Imagens/SVGs (se não for analisar UI)
ignore_folder("scrapes")       # Dados brutos
```

### 2. Fluxo "Árvore -> Folha" (Tree-to-Leaf)

Para projetos grandes, não dê o código todo. Dê o mapa.

1. **Usuário:** "Olhe a estrutura: `@project/tree`"
    * _Custo:_ ~200 tokens (Quase zero).
2. **Usuário:** "O erro está na autenticação."
3. **IA:** "Entendi a estrutura. Por favor, leia o arquivo `src/auth/login.ts`."
4. **Usuário:** O sistema lê apenas esse arquivo.

### 3. Cache de Contexto (Context Caching)

Se usar APIs da Anthropic (Claude):

* Ative o `prompt caching`.
* Envie o `PROJECT_CONTEXT_SUMMARY.txt` como um bloco de cache.
* Você pagará pelo envio **apenas na primeira vez**. As mensagens seguintes custam 10% do valor normal para ler o mesmo contexto.

---

## 🏆 Veredito Final

O **Infinite Memory MCP** é uma "Ferrari": extremamente rápida e poderosa, mas consome mais combustível.

* Use na cidade (projetos pequenos/médios) à vontade.
* Na estrada longa (projetos gigantes), dirija com inteligência (use filtros).

# Projeto: Private AI - Memória Infinita & Ultra-Rápida 🧠🚀

## Conceito

"Memória Infinita" aqui é uma **arquitetura de software**, não de hardware. O objetivo é permitir que o Agente de IA tenha acesso ao **contexto completo** do seu projeto instantaneamente, eliminando a "amnésia" comum em chatbots que esquecem arquivos não anexados.

Aproveitamos a **velocidade extrema dos SSDs modernos (NVMe)** para criar um buffer de contexto que é atualizado em tempo real. O arquivo gerado é otimizado e compacto, permitindo performance comparável à RAM.

## Arquitetura Explicada

### 1. O Buffer Otimizado (Smart Context)

Não precisamos de 1TB de RAM. O segredo é que código-fonte é texto puro e ocupa pouquíssimo espaço.

* Um projeto médio com 50 arquivos pode ter apenas ~100KB.
* Mesmo projetos grandes raramente passam de alguns MBs de código fonte puro (excluindo binários e assets).

O servidor mantém um "fotografia" (snapshot) desse texto compactado na memória do processo e salva um backup leve no disco (`PROJECT_CONTEXT_SUMMARY.txt`).

### 2. O Watcher Inteligente (Delta Updates)

Em vez de reler o disco inteiro a cada pergunta (o que seria lento), implementamos um **Watcher Assíncrono**:

* Ele monitora eventos do sistema de arquivos.
* Quando você salva um arquivo no VS Code, o servidor detecta **apenas** essa mudança.
* Ele atualiza o contexto na memória em milissegundos.

### 3. O Fluxo de Dados

1. **User Change:** Você edita `main.py`.
2. **Watcher:** Detecta modificação (ms).
3. **Server:** Atualiza a variável `context_content`.
4. **LLM Request:** O Claude pede `read_project_summary`.
5. **Response:** O servidor entrega o texto já pronto da memória. **Zero I/O Latency** no momento da pergunta.

## Implementação Técnica

### Componentes

* **MCP Server (FastMCP):** A interface padronizada que conecta com Claude/Cursor.
* **Background Thread:** Loop infinito que verifica `os.stat` (muito leve) a cada 3s.
* **Filtros de Segurança:** Ignora automaticamente `.env`, chaves privadas e pastas listadas no `.gitignore`.

### Por que "Infinita"?

Para a IA, a sensação é de memória infinita porque ela não precisa "escolher" quais arquivos ler. Ela recebe **tudo**. O limite real é apenas a "Janela de Contexto" do modelo (ex: 200k tokens no Claude 3.5 Sonnet), que é suficiente para a vasta maioria dos projetos de software inteiros.

---
**Status:** Produção 🚀
**Requisito:** Python 3.10+ e um SSD (Recomendado).
**Objetivo:** Zero-Friction Coding Assistant.

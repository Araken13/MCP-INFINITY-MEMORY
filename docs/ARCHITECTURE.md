# Projeto: Private AI - Memória Infinita & Ultra-Rápida 🧠🚀

## Conceito

Utilizar a infraestrutura de hardware disponível (**1TB de RAM**) para criar um Agente de IA capaz de processar contextos gigantescos com latência zero, eliminando o gargalo de leitura de disco (I/O).

## Arquitetura Proposta

### 1. Camada de Persistência Volátil (RAMDisk)

Em vez de salvar o contexto em SSD, criaremos um **RAMDisk** (Disco Virtual na Memória RAM).

* **Velocidade:** > 50 GB/s (vs 3-7 GB/s do SSD).
* **Latência:** Nanosegundos.
* **Função:** Armazenar o `PROJECT_CONTEXT_SUMMARY.txt` e a base de conhecimento vetorial.

### 2. Os Motores de Contexto (Scripts Python)

Utilizaremos versões otimizadas dos scripts que já criamos:

#### A. O Coletor Instantâneo (`leitor_ram.py`)

* Lê recursivamente o repositório.
* Em vez de escrever no disco rígido, escreve diretamente no mount point da RAM (`/mnt/ramdisk/context.txt`).
* **Melhoria:** Implementar *Watcher* de eventos de arquivo (Watchdog) para atualizar o RAMDisk apenas nos deltas (mudanças), em tempo real.

#### B. O Cérebro Local (Ollama/vLLM)

* O modelo de LLM (ex: Llama-3-70B, Mixtral 8x7B) é carregado inteiramente na RAM.
* O Agente consulta o arquivo de contexto na RAMDisk.
* **Resultado:** O Agente "sabe" tudo sobre o projeto instantaneamente, sem delay de carregamento de contexto.

## Implementação (Passos Iniciais)

### Passo 1: Criar RAMDisk (Linux/WSL)

```bash
# Cria ponto de montagem
sudo mkdir /mnt/ram_context

# Monta 10GB de RAM como disco
sudo mount -t tmpfs -o size=10G tmpfs /mnt/ram_context
```

### Passo 2: Adaptar Scripts

Mover os scripts `auto_leitor.py` e `leitor_de_contexto.py` para esta pasta e configurá-los para apontar para o `Target Path` no RAMDisk.

### Passo 3: Rodar Modelo

```bash
ollama run llama3:70b
# Configurar prompt do sistema para ler sempre de /mnt/ram_context/summary.txt
```

---
**Status:** Planejamento.
**Hardware:** 1TB RAM Disponível.
**Objetivo:** Zero-Latency coding assistant.

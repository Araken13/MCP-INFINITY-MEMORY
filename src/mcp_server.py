
import asyncio
import os
import sys
import time
import threading
import traceback
from typing import Any, Sequence, List, Set, Dict
from datetime import datetime
from mcp.server.fastmcp import FastMCP, Context

# ==================================================================================
# CONFIGURAÇÃO AVANÇADA
# ==================================================================================

# Inicializa o Servidor MCP com nome profissional
mcp = FastMCP("InfiniteMemory Pro 🧠")

# Configurações Padrão
DEFAULT_IGNORE_DIRS = {
    ".git", ".terraform", ".vscode", ".idea", "__pycache__", 
    "node_modules", "venv", ".oci", ".agent", "dist", "build", "coverage", ".next"
}
DEFAULT_IGNORE_EXTENSIONS = {
    ".exe", ".dll", ".so", ".bin", ".zip", ".png", ".jpg", ".jpeg", 
    ".pdf", ".pyc", ".mp4", ".mov", ".db", ".sqlite", ".iso"
}

# ==================================================================================
# CLASSE DE GESTÃO DE MEMÓRIA (CORE)
# ==================================================================================

class ProjectMemory:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.context_content = ""
        self.file_tree = ""
        self.recent_changes = []
        self.last_update_ts = 0
        self.is_updating = False
        self.error_log = []
        self.ignore_dirs = DEFAULT_IGNORE_DIRS.copy()
        
    def log_error(self, msg: str):
        timestamp = datetime.now().isoformat()
        err = f"[{timestamp}] {msg}"
        self.error_log.append(err)
        print(f"❌ {err}", file=sys.stderr)
        # Mantém apenas os últimos 50 erros
        if len(self.error_log) > 50:
            self.error_log.pop(0)

    def is_text_file(self, filename: str) -> bool:
        return not any(filename.lower().endswith(ext) for ext in DEFAULT_IGNORE_EXTENSIONS)

    def generate_full_context(self) -> str:
        """Gera o contexto completo, árvore e stats."""
        summary = []
        summary.append(f"# MEMÓRIA INFINITA: {os.path.basename(self.root_dir)}")
        summary.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("="*80 + "\n")
        
        tree_structure = []
        files_data = []

        total_files = 0
        total_size = 0
        
        try:
            for root, dirs, files in os.walk(self.root_dir):
                # Filtra diretórios
                dirs[:] = [d for d in dirs if d not in self.ignore_dirs and not d.startswith('.')]
                
                level = root.replace(self.root_dir, '').count(os.sep)
                indent = ' ' * 4 * (level)
                tree_structure.append(f"{indent}{os.path.basename(root)}/")

                for file in files:
                    if file == "PROJECT_CONTEXT_SUMMARY.txt" or not self.is_text_file(file):
                        continue
                        
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.root_dir)
                    
                    tree_structure.append(f"{indent}    {file}")
                    
                    try:
                        stats = os.stat(file_path)
                        mtime = stats.st_mtime
                        size = stats.st_size
                        
                        files_data.append({
                            "path": relative_path,
                            "mtime": mtime,
                            "size": size,
                            "abs_path": file_path
                        })
                        
                        total_files += 1
                        total_size += size
                        
                    except Exception as e:
                        self.log_error(f"Erro ao acessar {relative_path}: {e}")

            # Salva estrutura da árvore
            self.file_tree = "\n".join(tree_structure)
            
            # Ordena arquivos por modificação recente
            files_data.sort(key=lambda x: x['mtime'], reverse=True)
            self.recent_changes = [f['path'] for f in files_data[:5]]
            
            # Gera conteúdo concatenado
            for file_info in files_data:
                try:
                    with open(file_info['abs_path'], "r", encoding="utf-8", errors="ignore") as infile:
                        content = infile.read()
                        
                    summary.append(f"\n{'='*80}")
                    summary.append(f"ARQUIVO: {file_info['path']}  (Modificado: {datetime.fromtimestamp(file_info['mtime'])})")
                    summary.append(f"{'-'*80}")
                    summary.append(content)
                except Exception as e:
                    self.log_error(f"Erro ao ler conteúdo de {file_info['path']}: {e}")

            full_text = "\n".join(summary)
            
            # Persistência opcional no disco para debug
            try:
                with open("PROJECT_CONTEXT_SUMMARY.txt", "w", encoding="utf-8") as f:
                    f.write(full_text)
            except: pass

            return full_text

        except Exception as e:
            self.log_error(f"Erro fatal na geração de contexto: {traceback.format_exc()}")
            return f"Erro crítico ao gerar memória: {e}"

# Instância Global
memory = ProjectMemory()

# ==================================================================================
# SISTEMA DE WATCHER (BACKGROUND)
# ==================================================================================

def watcher_loop():
    print(f"👀 [MCP] Watcher Iniciado em: {memory.root_dir}", file=sys.stderr)
    
    # Execução inicial
    memory.is_updating = True
    memory.context_content = memory.generate_full_context()
    memory.last_update_ts = time.time()
    memory.is_updating = False
    print(f"✅ [MCP] Memória Inicial Carregada.", file=sys.stderr)

    while True:
        try:
            time.sleep(3) # Polling interval
            
            # Verifica se houve alteração nos tempos de modificação
            needs_update = False
            current_max_mtime = 0
            
            for root, dirs, files in os.walk(memory.root_dir):
                dirs[:] = [d for d in dirs if d not in memory.ignore_dirs and not d.startswith('.')]
                for file in files:
                    if file == "PROJECT_CONTEXT_SUMMARY.txt": continue
                    try:
                        mtime = os.path.getmtime(os.path.join(root, file))
                        if mtime > current_max_mtime:
                            current_max_mtime = mtime
                    except: pass
            
            # Se encontrou arquivo mais novo que a última atualização
            if current_max_mtime > memory.last_update_ts:
                print(f"🔄 [MCP] Alteração detectada ({current_max_mtime}). Atualizando...", file=sys.stderr)
                memory.is_updating = True
                memory.context_content = memory.generate_full_context()
                memory.last_update_ts = current_max_mtime
                memory.is_updating = False
                print(f"✅ [MCP] Memória Sincronizada.", file=sys.stderr)

        except Exception as e:
            memory.log_error(f"Erro no loop do watcher: {e}")
            time.sleep(10) # Wait longer if error occurs

# (Lógica movida para o bloco main para compatibilidade)

# ==================================================================================
# RECURSOS MCP (O que o LLM pode LER)
# ==================================================================================

@mcp.resource("project://summary")
def get_project_summary() -> str:
    """
    [MUITO IMPORTANTE] Retorna TODO o código e contexto do projeto concatenado.
    Use isso no início da conversa para entender o estado atual do projeto.
    """
    if memory.is_updating:
        return "⚠️ A memória está sendo atualizada neste momento. Aguarde 2 segundos e tente novamente para obter a versão mais recente."
    if not memory.context_content:
        return "⏳ Memória inicializando... (Estado Frio)"
    return memory.context_content

@mcp.resource("project://tree")
def get_project_tree() -> str:
    """
    Retorna apenas a árvore de arquivos do projeto.
    Útil para entender a estrutura sem carregar todo o conteúdo de uma vez.
    """
    return memory.file_tree if memory.file_tree else "(Árvore vazia ou carregando...)"

@mcp.resource("project://recent")
def get_recent_files() -> str:
    """
    Retorna a lista dos 5 arquivos modificados mais recentemente.
    Útil para saber onde o usuário estava trabalhando.
    """
    return "\n".join(memory.recent_changes) if memory.recent_changes else "(Nenhuma modificação recente detectada)"

@mcp.resource("project://errors")
def get_server_errors() -> str:
    """
    Retorna logs de erro do servidor de memória. Útil para debug se algo parece errado.
    """
    if not memory.error_log:
        return "Nenhum erro registrado. Sistema saudável. ✅"
    return "\n".join(memory.error_log)

# ==================================================================================
# FERRAMENTAS MCP (O que o LLM pode EXECUTAR)
# ==================================================================================

@mcp.tool()
def ignore_folder(folder_name: str) -> str:
    """
    Adiciona uma pasta à lista de ignorados para limpar o ruído do contexto.
    Ex: ignore_folder("tests") ou ignore_folder("docs_antigos")
    """
    memory.ignore_dirs.add(folder_name)
    # Força regeneração
    memory.last_update_ts = 0 
    return f"Pasta '{folder_name}' adicionada à lista de ignorados. A memória será regenerada em breve."

@mcp.tool()
def force_refresh() -> str:
    """Força manualmente a regeneração da memória agora."""
    memory.last_update_ts = 0
    return "Regeneração agendada para o próximo ciclo (dentro de instantes)."

if __name__ == "__main__":
    # Inicia o Watcher em background antes do servidor
    t = threading.Thread(target=watcher_loop, daemon=True)
    t.start()
    
    # Inicia o servidor MCP
    mcp.run()

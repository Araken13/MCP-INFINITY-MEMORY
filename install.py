
import json
import os
import sys

# Configurações
APPDATA = os.getenv('APPDATA')
CONFIG_PATH = os.path.join(APPDATA, "Claude", "claude_desktop_config.json")
REPO_PATH = r"D:\HACKTHON\NOVO LLM RAM INFINTO"
PYTHON_PATH = r"C:\Python314\python.exe"
SERVER_SCRIPT = os.path.join(REPO_PATH, "src", "mcp_server.py")

print(f"🔧 Configurando Claude em: {CONFIG_PATH}")

# Estrutura do novo servidor
new_server_config = {
    "command": PYTHON_PATH,
    "args": [SERVER_SCRIPT]
}

# 1. Carregar Configuração Existente
config = {}
if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                config = json.loads(content)
                print("✅ Configuração existente carregada.")
    except Exception as e:
        print(f"⚠️ Erro ao ler config anterior: {e}. Criando nova.")

# 2. Atualizar mcpServers
if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"]["infinite-memory"] = new_server_config

# 3. Salvar
try:
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("--------------------------------------------------")
    print("🎉 SUCESSO! Configuração do Claude atualizada.")
    print("--------------------------------------------------")
    print("Agora, por favor:")
    print("👉 REINICIE o Claude Desktop completamente.")
    print("👉 Procure pelo ícone de tomada 🔌 verde.")
except Exception as e:
    print(f"❌ Erro ao salvar arquivo: {e}")

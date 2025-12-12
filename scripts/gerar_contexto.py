
import os
import sys
from datetime import datetime

# Configurações
IGNORE_DIRS = {
    ".git", ".terraform", ".vscode", ".idea", "__pycache__", 
    "node_modules", "venv", ".oci", ".agent", "dist", "build", "coverage", "scripts", "tests"
}
IGNORE_EXTENSIONS = {
    ".exe", ".dll", ".so", ".bin", ".zip", ".png", ".jpg", ".jpeg", 
    ".pdf", ".pyc", ".mp4", ".mov", ".db", ".sqlite", ".iso"
}
OUTPUT_FILE = "PROJECT_CONTEXT_SUMMARY.txt"

def load_gitignore():
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    IGNORE_DIRS.add(line.replace("/", ""))

def is_text_file(filename):
    return not any(filename.lower().endswith(ext) for ext in IGNORE_EXTENSIONS)

def generate_context():
    load_gitignore()
    root_dir = os.getcwd()
    summary = []
    summary.append(f"# CONTEXTO DO PROJETO: {os.path.basename(root_dir)}")
    summary.append(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("="*80 + "\n")

    print(f"🚀 Iniciando leitura em: {root_dir}")
    print(f"📂 Ignorando: {', '.join(list(IGNORE_DIRS)[:5])}...")

    file_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Filtra diretórios
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        for file in files:
            if file == OUTPUT_FILE or not is_text_file(file):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, root_dir)
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                summary.append(f"\n{'='*80}")
                summary.append(f"ARQUIVO: {rel_path}")
                summary.append(f"{'-'*80}")
                summary.append(content)
                file_count += 1
                print(f"   📄 Lido: {rel_path}")
            except Exception as e:
                print(f"   ❌ Erro em {rel_path}: {e}")

    full_text = "\n".join(summary)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"\n✅ Sucesso! {file_count} arquivos compilados em '{OUTPUT_FILE}'.")
    print(f"📊 Tamanho total: {len(full_text)/1024:.2f} KB")

if __name__ == "__main__":
    generate_context()

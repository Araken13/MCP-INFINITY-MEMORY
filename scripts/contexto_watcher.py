
import time
import os
import sys
from gerar_contexto import generate_context

def main():
    print("👀 WATCHER DE CONTEXTO INICIADO")
    print("   Monitorando alterações para regenerar o sumário automaticamente...")
    print("   (Pressione Ctrl+C para parar)")
    
    last_update = 0
    root_dir = os.getcwd()

    # Gera a primeira versão
    generate_context()
    
    while True:
        try:
            time.sleep(2)
            max_mtime = 0
            
            # Varredura rápida de timestamps
            for root, dirs, files in os.walk(root_dir):
                if ".git" in dirs: 
                    dirs.remove(".git") # Otimização
                
                for file in files:
                    if file == "PROJECT_CONTEXT_SUMMARY.txt": continue
                    try:
                        mtime = os.path.getmtime(os.path.join(root, file))
                        if mtime > max_mtime:
                            max_mtime = mtime
                    except: pass
            
            if max_mtime > last_update:
                if last_update != 0: # Não loga na primeira vez se já gerou
                    print(f"\n🔄 Alteração detectada! Regenerando contexto...")
                    generate_context()
                last_update = max_mtime
                
        except KeyboardInterrupt:
            print("\n🛑 Watcher finalizado.")
            sys.exit(0)
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()

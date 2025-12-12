
import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configurações do servidor
SERVER_SCRIPT = os.path.join(os.getcwd(), "src", "mcp_server.py")
PYTHON_EXE = "C:/Python314/python.exe"

async def run():
    server_params = StdioServerParameters(
        command=PYTHON_EXE,
        args=[SERVER_SCRIPT],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Lista ferramentas
            tools = await session.list_tools()
            print(f"🛠️ Ferramentas disponíveis: {[t.name for t in tools.tools]}")

            # Testa read_project_summary
            print("\n🧪 Testando 'read_project_summary'...")
            try:
                result = await session.call_tool("read_project_summary", arguments={})
                content = result.content[0].text
                print(f"✅ Sucesso! Resumo recebido.")
                print(f"📊 Tamanho do conteúdo: {len(content)} caracteres")
                print(f"📋 Primeiras 200 letras:\n{content[:200]}...")
            except Exception as e:
                print(f"❌ Erro ao chamar ferramenta: {e}")

if __name__ == "__main__":
    asyncio.run(run())

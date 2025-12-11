# 🧠 Infinite Memory MCP Server

**Zero-Latency, Full-Context Awareness for AI Agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Ready](https://img.shields.io/badge/MCP-Ready-green.svg)](https://modelcontextprotocol.io/)

> **"Stop waiting for your AI to read files. Give it infinite memory."**

---

## 🚀 The Concept

Traditional AI coding assistants suffer from **Cognitive Latency**: they need to search, list, and read files one by one before they can understand your project. This is slow and prone to errors (hallucinations).

**Infinite Memory MCP** solves this by maintaining a **Real-Time, Hot-Swappable Context Buffer** of your entire project.

### Performance Comparison

| Metric | 🐢 Traditional Approach | 🧠 Infinite Memory MCP |
| :--- | :--- | :--- |
| **Start-up Time** | 15s - 60s (Reading files...) | **0s (Instant)** |
| **Context Scope** | Fragmented (Only requested files) | **Holistic (Entire Project)** |
| **User Friction** | High (Need to guide the AI) | **Zero (Auto-Magic)** |

---

## 🛠️ Installation

### Prerequisites

* Python 3.10 or higher
* `mcp` library (`pip install mcp`)

### Quick Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/infinite-memory-mcp.git
    cd infinite-memory-mcp
    ```

2. **Configure your MCP Client (e.g., Claude Desktop)**
    Add the following to your config JSON:

    ```json
    {
      "mcpServers": {
        "infinite-memory": {
          "command": "python",
          "args": [
            "/absolute/path/to/infinite-memory-mcp/src/mcp_server.py"
          ]
        }
      }
    }
    ```

3. **Restart Claude** and enjoy Infinite Memory! 🚀

---

## 💡 Usage

In your AI chat, you now have access to powerful tools:

* **`@project/summary`**: Injects the *entire* up-to-date project code into the context. Best used at the start of a session.
* **`@project/tree`**: Shows the file structure.
* **`@project/recent`**: Shows what you were working on last.
* **`ignore_folder(name)`**: Tell the memory to ignore specific folders (e.g., `logs`, `tmp`) to save tokens.

### Pro Tip: System Prompt

Add this to your AI's custom instructions:
> "Always start the session by reading the 'project://summary' resource to understand the full project context."

---

## 🔧 Architecture

The server runs a lightweight background thread (**The Watcher**) that monitors file system events. When you save a file in VS Code:

1. **Watcher** detects the change (Delta).
2. **Memory Buffer** is regenerated in <500ms.
3. **MCP Resource** is instantly updated.

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for deeper details.

---

## 🤝 Contributing

Pull requests are welcome!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-memory`)
3. Commit your changes (`git commit -m 'Add amazing memory'`)
4. Push to the branch (`git push origin feature/amazing-memory`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

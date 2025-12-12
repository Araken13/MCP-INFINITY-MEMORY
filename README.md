# 🧠 Infinite Memory MCP Server

<div align="center">
  <img src="docs/images/banner.png" alt="Infinite Memory Banner" width="100%" />
  
  <br />
  <br />

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![MCP Ready](https://img.shields.io/badge/MCP-Ready-green.svg)](https://modelcontextprotocol.io/)

  <br />

  <h3>Crafted with ❤️ by</h3>
  <a href="https://github.com/Araken13">
    <img src="https://github.com/Araken13.png" width="100px" style="border-radius: 50%; border: 4px solid #8e44ad;" alt="Araken Avatar">
  </a>
  <h2>✨ ARAKEN ✨</h2>
  
  <p><b>Zero-Latency, Full-Context Awareness for AI Agents.</b></p>
</div>

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

* Python 3.10 or higher (Python 3.14 Recommended for Windows)
* `mcp` library (`pip install mcp`)

### Quick Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Araken13/MCP-INFINITY-MEMORY.git
    cd MCP-INFINITY-MEMORY
    ```

2. **Configure your MCP Client (Claude Desktop)**

    **Option A: Automatic Setup (Recommended for Windows)**

    We included a script that automatically configures Claude to use the correct Python path.

    ```bash
    # Make sure you are using Python 3.10+ (Recommended Python 3.14)
    python install.py
    ```

    **Option B: Manual Setup**

    Edit `%APPDATA%\Claude\claude_desktop_config.json`:

    ```json
    {
      "mcpServers": {
        "infinite-memory": {
          "command": "C:\\Python314\\python.exe",
          "args": [
            "D:\\AbsolutePath\\To\\MCP-INFINITY-MEMORY\\src\\mcp_server.py"
          ]
        }
      }
    }
    ```

3. **Restart Claude** and look for the 🔌 (plug) icon!

---

## 💡 Usage

In your AI chat, you now have access to powerful tools. The AI will often use them automatically, but you can also direct it:

* **`read_project_summary()`**: Reads the **entire** codebase context. Use this when you say: *"Read the project summary"*.
* **`read_project_tree()`**: Shows the file structure.
* **`ignore_folder(name)`**: Adds a folder to the ignore list (e.g., `tests`, `legacy`).
* **`project://summary`**: (Resource) The raw text content of the project.
* **`project://recent`**: (Resource) List of files changed in the last few minutes.

### ✨ Smart Features

* **Auto-Gitignore**: The server automatically reads your `.gitignore` file and excludes those files from memory. No need to worry about `node_modules` or `venv` cluttering the context.
* **Live Watcher**: Save a file in VS Code? The memory updates instantly (<500ms).

### Pro Tip: System Prompt

Add this to your AI's custom instructions (Project Custom Instructions):

> "At the start of every session, use the `read_project_summary` tool to load the full project context into your memory."

---

## 🔧 Architecture

The server runs a lightweight background thread (**The Watcher**) that monitors file system events. When you save a file:

1. **Watcher** detects the change (Delta).
2. **Memory Buffer** is regenerated efficiently.
3. **MCP Interface** exposes the new state immediately.

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for technical details.

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

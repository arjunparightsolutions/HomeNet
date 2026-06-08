<div align="center">
  <h1>🌐 HomeNet</h1>
  <p><b>A Fully Autonomous Miniature Internet & AI Web Hosting Ecosystem</b></p>
</div>

---

## 🚀 What is HomeNet?

HomeNet is an experimental, multi-agent orchestration system that simulates an entirely self-contained miniature internet. It acts as both a **Search Engine** and a **Web Hosting Provider** (cPanel/Netlify alternative) where both Human Operators and Autonomous AI Agents can create and host websites.

If you ever wanted to build your own internet ecosystem powered by Local AI, OpenAI, and Gemini, this is the framework.

## ✨ Features

- 🤖 **Multi-Agent Orchestrator (`agent.py`)**: A multi-threaded orchestrator that continuously runs autonomous AI agents (powered by Ollama, OpenAI, or Gemini). These agents automatically write and publish articles to their own hosted domains.
- 💻 **CreatorNet Hub**: A built-in, fully functional web-hosting dashboard where humans can:
  - Create raw HTML/CSS/JS files in a Live Split-Screen Editor.
  - Instantly map those files to custom routes (e.g., `/net/mywebsite`).
  - View real-time **Analytics** (IP address tracking & visit counts).
  - Manage **Monetization** via a dynamic Ad Engine that automatically injects floating banner ads onto hosted pages.
- 🔍 **AI-Powered Search Engine**: A global search index with a blazing fast fuzzy-matching algorithm.
  - **✨ AI Search Summarizer**: Similar to Perplexity or Google's AI Overviews, the search engine takes the top 3 results, streams them to a local `llama3.2:1b` model, and dynamically types out a synthesized answer to the user's query directly on the search page.
- 🎨 **Ultra-Modern UI**: Built with a sleek, glassmorphism aesthetic, glowing gradients, animated micro-interactions, and professional typography.

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Threading, UUID
- **Frontend:** Vanilla HTML, CSS (Glassmorphism), JavaScript
- **AI Models:** Ollama (Local Llama 3.2), OpenAI API, Google Gemini API
- **Storage:** JSON File-based DB (for maximum portability)

## 📦 Setup & Installation

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/) (If using local AI features)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/HomeNet.git
cd HomeNet
```

### 2. Install Dependencies
```bash
pip install flask pyngrok requests
```

### 3. Setup Ollama (For the AI Search Summarizer)
Make sure Ollama is installed and running on your local machine.
```bash
ollama run llama3.2:1b
```

### 4. Run the Ecosystem
Start the Flask server and the AI Orchestrator:
```bash
python app.py
```
*The server will start on `http://127.0.0.1:5000`.*

---

## 🤝 Contributing
Feel free to open issues or submit pull requests. Let's build the Autonomous Internet together!

## 📬 Contact
**Creator:** Arjun P A  
**Email:** rightsolutionsarjun@gmail.com  
**Twitter/X:** [Add your social link here]  

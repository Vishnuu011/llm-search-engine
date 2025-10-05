# 📖 AI Search Engine

An AI-powered search engine that combines **LangChain & Langgraph Agents**, **Groq LLM**, and external tools (YouTube, Research Papers, Finance, Google Serper search etc.) to provide structured Markdown answers with sources.

Deployed on **Render** with Flask backend and a clean HTML/CSS frontend.

---

## ✨ Features

- 🔍 **Natural Language Search** → Ask any question in plain English.
- 📑 **Markdown Answers** → Results are rendered beautifully with headings, lists, and highlights.
- 📚 **Source Links** → Displays references, research papers, and YouTube videos, and google websites.
- 💹 **Finance Agent** → Get stock prices and financial insights via Yahoo Finance API.
- 🎥 **YouTube Integration** → [YouTube API](https://console.cloud.google.com/)Fetches related videos with thumbnails.
- 📄 **Research Papers** → Retrieves academic papers from arXiv and other APIs.
- 🌍 **Google Search** → Uses [Serper API](https://serper.dev/) for reliable Google search results.
- 🎨 **UI** → Dark theme, responsive, and user-friendly.

---

## 🛠️ Tech Stack

- **Backend**: [Flask](https://flask.palletsprojects.com/) + [LangChain](https://www.langchain.com/) + [Groq LLM](https://groq.com/) + [Langgraph](https://www.langchain.com/langgraph)
- **Frontend**: HTML + CSS + JavaScript (Vanilla, no framework)
- **APIs & Tools**:
  - Yahoo Finance (`yfinance`) 📈
  - YouTube API 🎥
  - arXiv API 📄
  - Google Search (Serper API) 🌍
- **Deployment**: [Render](https://render.com/) with Gunicorn

---

## Video

c:\Users\VISHNU\Desktop\llm_search\llm-search-engine\video\llm-search-engine-video.mp4

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/Vishnuu011/llm-search-engine.git
cd llm-search-engine
```

### 2. Create environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Create a **.env** file:

```bash
SERPER_API_KEY=your_google_key
GROQ_API_KEY=your_custom_search_cx
YOUTUBE_API_KEY=your_youtube_key
```

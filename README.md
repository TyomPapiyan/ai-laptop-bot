# 🤖 AI Laptop Recommendation Bot

An autonomous AI agent Telegram bot that searches the web in real time, scrapes laptop review pages, extracts structured product data, and recommends the best options under the user's budget.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![aiogram](https://img.shields.io/badge/python--telegram--bot-latest-blue)
![LLM](https://img.shields.io/badge/LLM-integrated-orange?logo=openai)

---

## ✨ Features

- 🔎 **Smart Web Search** — generates relevant queries automatically and filters low-quality sources (Quora, Pinterest, etc.)
- 🧾 **Data Extraction Engine** — parses laptop name, price, RAM and specs from raw HTML using regex + heuristics
- 📊 **Ranking System** — scores laptops by relevance, information completeness, and inferred quality; returns top 5
- 🤖 **AI Reasoning Layer** — converts structured data into human-readable answers with a best pick, alternatives, and a final conclusion
- 💬 **Telegram Bot Interface** — clean conversational commands to start, stop, and restart sessions

---

## 🛠 Tech Stack

- Python 3.11
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — Telegram bot framework
- requests + BeautifulSoup — web scraping
- Regex-based extraction engine
- Custom scoring / ranking algorithm
- LLM integration (AI reasoning layer)
- ThreadPoolExecutor — async-style execution

---

## 📁 Project Structure

```
ai-laptop-bot/
├── .env                  # your secret keys (not in GitHub)
├── .gitignore
├── main.py               # entry point
├── bot.py                # Telegram bot interface & command handlers
├── agent.py              # orchestration — coordinates all modules
├── search.py             # web search query generation & filtering
├── scraper.py            # HTTP fetching & HTML parsing
├── extractor.py          # regex-based structured data extraction
├── analyzer.py           # scoring & ranking logic
├── llm.py                # LLM integration for AI reasoning
├── formatter.py          # formats final answer for Telegram
├── memory.py             # session memory management
└── memory.json           # persisted session state
```

> ⚠️ `.env` is excluded from GitHub via `.gitignore` — your API keys stay private.

---

## 🚀 Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/TyomPapiyan/ai-laptop-bot.git
cd ai-laptop-bot
```

**2. Create virtual environment**

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install python-telegram-bot requests beautifulsoup4 python-dotenv
```

**4. Create `.env` file**

```
BOT_TOKEN=your_telegram_bot_token
```

- Get your Telegram token from [@BotFather](https://t.me/BotFather)

**5. Run the bot**

```bash
python main.py
```

---

## 🏗 Architecture

```
User Input
    ↓
Telegram Bot  (bot.py)
    ↓
AI Agent      (agent.py)
    ↓
Search Engine (search.py)
    ↓
Web Scraper   (scraper.py)
    ↓
Extractor     (extractor.py)  →  structured data
    ↓
Ranking Engine (analyzer.py)
    ↓
LLM Reasoning  (llm.py)
    ↓
Formatter      (formatter.py)
    ↓
Telegram Response
```

---

## 💬 Example

```
You:  I need a laptop for programming, budget $800

Bot:  🔎 Searching the web...

      🏆 Best Pick: Lenovo ThinkPad E15 Gen 4 — $749
         16 GB RAM · Ryzen 5 5625U · 512 GB SSD
         Great build quality, excellent keyboard, perfect for dev work.

      🔁 Alternatives:
         • Acer Aspire 5 — $699 · 8 GB RAM · solid budget option
         • ASUS VivoBook 15 — $779 · 16 GB RAM · good display

      📌 Conclusion: The ThinkPad gives the best balance of performance,
         build quality, and price for a programming workflow.
```

---

## 📋 Commands

| Command      | Description           |
|--------------|-----------------------|
| `/start`     | Start the bot         |
| `/help`      | Show instructions     |
| `/restart`   | Restart session       |
| `/end`       | Stop responses        |

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it.

```
MIT License — © 2026 TyomPapiyan
```

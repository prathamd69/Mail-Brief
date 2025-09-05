# 📬 Mail-Brief

**Mail-Brief** is a Python-based Gmail summarizer that fetches emails, generates concise summaries using AI models, and presents them in a clean HTML inbox or web interface. It’s designed to save time and reduce the need to repeatedly check your mailbox.

---

## 🌟 Features

### ✅ Email Fetching
- Fetches the latest **n** emails from your Gmail inbox.

### 🧠 Summarization
- Generates concise summaries for each email using **Hugging Face** models.
- Modular architecture for future integration (e.g., MCP summarization models).

### 🖥️ HTML Inbox Generation
- Creates a clean, styled `output/inbox.html` file displaying:
  - 📌 Subject
  - 👤 Sender
  - 🧠 AI-generated summary
  - 🔽 Collapsible full email body

### ⚙️ Configurable Output
- Customize number of emails or date range to fetch.
- All outputs saved to the `output/` folder.


### 🛠️ Error Handling
- Gracefully skips empty emails.
- Ignores failed summarization attempts without crashing.

---

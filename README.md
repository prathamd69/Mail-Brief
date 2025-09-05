Mail-Brief

Mail-Brief is a Python-based Gmail summarizer that fetches emails, generates concise summaries using AI models, and presents them in a clean HTML inbox or web interface. It’s designed to save time and reduce the need to repeatedly check your mailbox.

🌟 Features Implemented

Fetch n latest emails


Summarization

Generates concise summaries for each email using Hugging Face models.

Supports future integration with MCP for modular summarization.

HTML Inbox Generation

Generates a clean, styled HTML file (output/inbox.html) showing:

Subject

Sender

AI-generated summary

Collapsible full email body

Configurable Output

Save results in output/ folder.

Easily configurable max number of emails or days to fetch.

Cross-platform Friendly

Works on Windows, Mac, Linux.

Compatible with Colab for faster GPU-accelerated summarization.

Error Handling

Handles empty emails gracefully.

Skips failed summarization attempts without crashing.

⚙️ Installation

Clone the repository:

git clone https://github.com/yourusername/Mail-Brief.git
cd Mail-Brief


Install dependencies:

pip install -r requirements.txt


Add your Gmail API credentials (credentials.json) in the project root.

🚀 Usage

Run the main script:

python main.py


Authorize your Gmail account (first time only) via the browser link.

Wait for emails to be fetched and summarized.

Open output/inbox.html in your browser to view summaries.

🔧 Folder Structure
Mail-Brief/
│
├── services/
│   ├── gmail_api.py         # Fetch emails via Gmail API
│   ├── summarizer.py        # AI summarization logic
│   └── utils.py             # Helpers (optional)
│
├── output/                  # Generated HTML summaries
│   └── inbox.html
│
├── generate_html.py         # Creates styled HTML file from email data
├── main.py                  # Entry point for the application
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignore cache, credentials, output files
└── README.md


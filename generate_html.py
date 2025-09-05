import os

def save_emails(emails, output_path="output/inbox.html"):
    """
    Save a list of emails (dicts with subject, sender, summary, body) into an HTML file.
    """

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Start HTML
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Mail-Brief Inbox</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }
            .container { width: 80%; margin: 20px auto; }
            .email-card { background: #fff; margin-bottom: 15px; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .subject { font-size: 1.2em; font-weight: bold; margin-bottom: 5px; }
            .sender { color: #555; margin-bottom: 10px; }
            .summary { margin: 10px 0; color: #333; }
            .body { margin-top: 10px; font-size: 0.9em; color: #666; white-space: pre-line; display: none; }
            .toggle-btn { background: #007BFF; color: #fff; border: none; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 0.8em; }
            .toggle-btn:hover { background: #0056b3; }
        </style>
        <script>
            function toggleBody(id) {
                var body = document.getElementById(id);
                body.style.display = (body.style.display === "none") ? "block" : "none";
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>📩 Mail-Brief Inbox</h1>
    """

    # Add emails
    for idx, email in enumerate(emails,1):
        html_content += f"""
        <div class="email-card">
            <div class="subject">{email.get('subject', '(No Subject)')}</div>
            <div class="sender">From: {email.get('sender', 'Unknown')}</div>
            <div class="summary"><b>Summary:</b> {email.get('summary', 'No summary')}</div>
            <button class="toggle-btn" onclick="toggleBody('body{idx}')">Show/Hide Full Email</button>
            <div class="body" id="body{idx}">{email.get('body', 'No content')}</div>
        </div>
        """

    # End HTML
    html_content += """
        </div>
    </body>
    </html>
    """

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Emails saved to {output_path}")

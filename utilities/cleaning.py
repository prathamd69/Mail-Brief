import re
from bs4 import BeautifulSoup

def clean_email_body(body: str, is_html=True) -> str:
    """
    Cleans the email body by:
    - Stripping HTML tags (if is_html=True)
    - Removing signatures, quoted replies, disclaimers, and excessive whitespace
    """

    if is_html:
        # Parse HTML and extract text only
        soup = BeautifulSoup(body, "html.parser")
        body = soup.get_text(separator="\n")

    # Normalize line endings
    body = body.replace('\r\n', '\n').replace('\r', '\n')

    # Remove common signature separator and everything after it
    # Also consider variations like '-- ', '__', or 'Thanks,' on their own line
    body = re.split(r'(--\s*$|__\s*$|Thanks,?$|\nRegards,?$)', body, flags=re.MULTILINE)[0]

    # Remove quoted replies starting with "> "
    body = '\n'.join(line for line in body.splitlines() if not line.strip().startswith('>'))

    # Remove lines like "On <date>, <person> wrote:"
    body = re.sub(r'On\s.+?wrote:', '', body, flags=re.DOTALL | re.IGNORECASE)

    # Remove disclaimers based on keywords and stop at that point
    disclaimer_keywords = ['confidential', 'disclaimer', 'privileged', 'unauthorized']
    lines = body.splitlines()
    cleaned_lines = []
    for line in lines:
        if any(word.lower() in line.lower() for word in disclaimer_keywords):
            break  # stop at disclaimer start and remove everything after
        cleaned_lines.append(line)
    body = '\n'.join(cleaned_lines)

    # Remove excessive newlines (more than 2)
    body = re.sub(r'\n{3,}', '\n\n', body)

    # Remove trailing and leading spaces per line
    lines = [line.strip() for line in body.splitlines()]
    # Remove empty lines
    lines = [line for line in lines if line]

    # Optional: filter out common footer/footer-like lines (customize as needed)
    footer_keywords = [
        'view more', 'explore more', 'get the app', 'queries?', 'support@', 'all rights reserved', '©'
    ]
    filtered_lines = [
        line for line in lines
        if not any(fk.lower() in line.lower() for fk in footer_keywords)
    ]

    cleaned_body = '\n'.join(filtered_lines)
    cleaned_body = cleaned_body.replace('\n', '<br>')

    return cleaned_body.strip()

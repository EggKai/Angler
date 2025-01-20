import html
def sanitize_content(content):
    """Sanitize the content to avoid XSS (HTML escaping)."""
    return html.escape(content)

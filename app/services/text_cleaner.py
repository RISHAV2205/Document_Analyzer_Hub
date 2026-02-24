def clean_text(text: str) -> str:

    # Normalize line breaks to spaces
    text = text.replace("\r", " ").replace("\n", " ")
    # Remove extra whitespace
    text = " ".join(text.split())
    return text

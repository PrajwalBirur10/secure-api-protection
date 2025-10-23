def analyze_text(content: str) -> str:
    risky_keywords = ["password", "token", "drop table", "select *", "secret", "<script>"]
    for word in risky_keywords:
        if word.lower() in content.lower():
            return f"⚠️ Potential risk detected: '{word}'"
    return "✅ Input is safe"

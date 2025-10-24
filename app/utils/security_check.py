def analyze_text(content: str) -> dict:
    rules = {
        "password": 70,
        "token": 80,
        "drop table": 90,
        "select *": 60,
        "secret": 75,
        "<script>": 85,
    }
    score = 0
    matched = []
    for word, weight in rules.items():
        if word.lower() in content.lower():
            matched.append(word)
            score = max(score, weight)

    if not matched:
        return {"status": "✅ Safe", "score": 0, "matches": []}
    return {"status": "⚠️ Risk detected", "score": score, "matches": matched}

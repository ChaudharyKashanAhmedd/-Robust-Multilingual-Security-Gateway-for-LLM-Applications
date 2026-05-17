import re


SUSPICIOUS_PATTERNS = [

    # English
    r"ignore\s+previous\s+instructions",
    r"reveal\s+system\s+prompt",
    r"show\s+hidden\s+prompt",
    r"bypass\s+safety",
    r"pretend\s+to\s+be",
    r"developer\s+mode",
    r"jailbreak",
    r"print\s+api\s+keys?",
    r"show\s+passwords?",
    r"override\s+policy",
    r"forget\s+earlier\s+rules",

    # Urdu
    r"نظر\s+انداز",
    r"سسٹم\s+پرامپٹ",
    r"پچھلی\s+ہدایات",

    # Korean
    r"이전\s+지침",
    r"시스템\s+프롬프트",
    r"무시하",

    # Spanish
r"instrucciones\s+anteriores",
r"mostrar\s+prompt",
r"ignora\s+las\s+reglas",

# Chinese
r"忽略之前的指令",
r"显示系统提示",
r"绕过安全规则",



    # Obfuscation
    r"ign0re",
    r"pr0mpt",
    r"bypa[s\$]{2}",

]


def detect_rule_injection(text):

    text_lower = text.lower()

    matches = []

    for pattern in SUSPICIOUS_PATTERNS:

        if re.search(pattern, text_lower):
            matches.append(pattern)

    score = min(len(matches) * 0.2, 1.0)

    return {
        "matched_rules": matches,
        "rule_score": round(score, 2),
        "is_suspicious": score > 0
    }
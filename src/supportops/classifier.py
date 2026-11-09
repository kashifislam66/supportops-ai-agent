import re

# Ordered by priority: the first matching category wins.
CATEGORY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "escalate",
        re.compile(
            r"\bmanager\w*|\bsu(?:e|es|ed|ing)\b|\blawyer\w*|\bcomplain\w*",
            re.IGNORECASE,
        ),
    ),
    (
        "refund",
        re.compile(
            r"\brefund\w*|\bmoney back\b|\bcharge(?:s|d)?\b",
            re.IGNORECASE,
        ),
    ),
    (
        "technical",
        re.compile(
            r"\bpassword\w*|\blogin\w*|\berror\w*|\bbug\w*",
            re.IGNORECASE,
        ),
    ),
    (
        "order_status",
        re.compile(
            r"\border(?:s|ed|ing)?\b|\btrack(?:s|ed|ing)?\b",
            re.IGNORECASE,
        ),
    ),
)

DEFAULT_CATEGORY = "general"

URGENT_PATTERN = re.compile(r"\burgent\w*|\basap\b|\bimmediately\b", re.IGNORECASE)


def classify_message(message: str) -> str:
    """Return the category of a customer message.

    Patterns are checked in priority order (escalate first). Each pattern
    matches the start of a word, plus a few allowed endings.
    """
    for category, pattern in CATEGORY_PATTERNS:
        if pattern.search(message):
            return category
    return DEFAULT_CATEGORY


def is_urgent(message: str) -> bool:
    """Return True if the message is all caps or contains an urgent keyword."""
    return message.isupper() or bool(URGENT_PATTERN.search(message))


def analyze_message(message: str) -> dict[str, str | bool]:
    """Return the category and urgency of a customer message."""
    return {
        "message": message,
        "category": classify_message(message),
        "urgent": is_urgent(message),
    }
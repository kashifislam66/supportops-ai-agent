import logging
import re

from supportops.exceptions import InvalidMessageError
from supportops.models import Category, MessageAnalysis

logger = logging.getLogger(__name__)
# Ordered by priority: the first matching category wins.
CATEGORY_PATTERNS: tuple[tuple[Category, re.Pattern[str]], ...] = (
    (
        Category.ESCALATE,
        re.compile(
            r"\bmanager\w*|\bsu(?:e|es|ed|ing)\b|\blawyer\w*|\bcomplain\w*",
            re.IGNORECASE,
        ),
    ),
    (
        Category.REFUND,
        re.compile(
            r"\brefund\w*|\bmoney back\b|\bcharge(?:s|d)?\b",
            re.IGNORECASE,
        ),
    ),
    (
        Category.TECHNICAL,
        re.compile(
            r"\bpassword\w*|\blogin\w*|\berror\w*|\bbug\w*",
            re.IGNORECASE,
        ),
    ),
    (
        Category.ORDER_STATUS,
        re.compile(
            r"\border(?:s|ed|ing)?\b|\btrack(?:s|ed|ing)?\b",
            re.IGNORECASE,
        ),
    ),
)

DEFAULT_CATEGORY = Category.GENERAL

URGENT_PATTERN = re.compile(r"\burgent\w*|\basap\b|\bimmediately\b", re.IGNORECASE)


def _validate_message(message: object) -> None:
    """Raise InvalidMessageError if the message is empty or invalid."""
    if not isinstance(message, str) or not message.strip():
        raise InvalidMessageError("Customer message is empty or invalid.")


def classify_message(message: str) -> Category:
    """Return the category of a customer message.

    Patterns are checked in priority order (escalate first). Each pattern
    matches the start of a word, plus a few allowed endings.
    """
    _validate_message(message)

    for category, pattern in CATEGORY_PATTERNS:
        if pattern.search(message):
            logger.debug("Matched category=%s", category)
            return category
    return DEFAULT_CATEGORY


def is_urgent(message: str) -> bool:
    """Return True if the message is all caps or contains an urgent keyword."""
    _validate_message(message)

    return message.isupper() or bool(URGENT_PATTERN.search(message))


def analyze_message(message: str) -> dict[str, str | bool]:
    """Return the category and urgency of a customer message."""
    category = classify_message(message)
    urgent = is_urgent(message)
    logger.info("Analyzed message: category=%s urgent=%s", category, urgent)

    return MessageAnalysis(message=message, category=category, urgent=urgent)
    
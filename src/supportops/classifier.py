import logging
import re
from collections.abc import Sequence

from supportops.exceptions import InvalidMessageError
from supportops.models import Category, MessageAnalysis, Rule

logger = logging.getLogger(__name__)

# Ordered by priority: the first matching category wins.
DEFAULT_RULES: tuple[Rule, ...] = (
    Rule(
        Category.ESCALATE,
        re.compile(
            r"\bmanager\w*|\bsu(?:e|es|ed|ing)\b|\blawyer\w*|\bcomplain\w*",
            re.IGNORECASE,
        ),
    ),
    Rule(
        Category.REFUND,
        re.compile(
            r"\brefund\w*|\bmoney back\b|\bcharge(?:s|d)?\b",
            re.IGNORECASE,
        ),
    ),
    Rule(
        Category.TECHNICAL,
        re.compile(
            r"\bpassword\w*|\blogin\w*|\berror\w*|\bbug\w*",
            re.IGNORECASE,
        ),
    ),
    Rule(
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
    

class RuleBasedClassifier:
    """Classify messages using ordered regex rules."""

    def __init__(self, rules: Sequence[Rule], default: Category = Category.GENERAL) -> None:
        self._rules = tuple(rules)
        self._default = default

    def classify(self, message: str) -> Category:
        """Return the category of a customer message."""
        _validate_message(message)

        for rule in self._rules:
            if rule.pattern.search(message):
                logger.debug("Matched category=%s", rule.category)
                return rule.category
        return self._default

    def is_urgent(self, message: str) -> bool:
        """Return True if the message is all caps or contains an urgent keyword."""
        _validate_message(message)

        return message.isupper() or bool(URGENT_PATTERN.search(message))

    def analyze(self, message: str) -> MessageAnalysis:
        """Return the category and urgency of a customer message."""
        category = self.classify(message)
        urgent = self.is_urgent(message)
        logger.info("Analyzed message: category=%s urgent=%s", category, urgent)

        return MessageAnalysis(message=message, category=category, urgent=urgent)


_DEFAULT_CLASSIFIER = RuleBasedClassifier(DEFAULT_RULES, DEFAULT_CATEGORY)


def classify_message(message: str) -> Category:
    """Return the category of a customer message."""
    return _DEFAULT_CLASSIFIER.classify(message)


def is_urgent(message: str) -> bool:
    """Return True if the message is all caps or contains an urgent keyword."""
    return _DEFAULT_CLASSIFIER.is_urgent(message)


def analyze_message(message: str) -> MessageAnalysis:
    """Return the category and urgency of a customer message."""
    return _DEFAULT_CLASSIFIER.analyze(message)
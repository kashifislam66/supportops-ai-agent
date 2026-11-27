import re

import pytest

from supportops.classifier import (
    Category,
    MessageAnalysis,
    Rule,
    RuleBasedClassifier,
    analyze_message,
    classify_message,
    is_urgent,
)
from supportops.exceptions import InvalidMessageError


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        # 1 & 2: escalate
        ("I am suing you for this", "escalate"),
        ("Let me speak to your manager or lawyer", "escalate"),
        # 3 & 4: refund
        ("I want a refund please", "refund"),
        ("I was charged twice, give my money back", "refund"),
        # 5 & 6: technical
        ("I forgot my password and cannot login", "technical"),
        ("There is a bug causing an error on the page", "technical"),
        # 7 & 8: order_status
        ("Where is my order?", "order_status"),
        ("I am tracking my package", "order_status"),
        # 9 & 10: priority check (escalate wins over refund/order)
        ("I want to complain about my order", "escalate"),
        ("My lawyer will ask for a refund", "escalate"),
        # 11: general (default)
        ("Hello, what are your working hours?", "general"),
        # 12: known limitation (xfail)
        pytest.param(
            "Sue from support helped me, thanks",
            "general",
            marks=pytest.mark.xfail(
                reason="Regex cannot tell the name Sue from the verb sue"
            ),
        ),
    ],
)
def test_classify_message(message: str, expected: str) -> None:
    assert classify_message(message) == expected


@pytest.mark.parametrize(
    "bad_input",
    [
        "",       # Empty string
        "   ",    # Whitespace only
        None,     # None value
        123,      # Non-string value
    ],
)
def test_invalid_messages_raise_error(bad_input: object) -> None:
    with pytest.raises(InvalidMessageError, match="empty or invalid"):
        classify_message(bad_input)  # type: ignore[arg-type]

    with pytest.raises(InvalidMessageError, match="empty or invalid"):
        is_urgent(bad_input)  # type: ignore[arg-type]

    with pytest.raises(InvalidMessageError, match="empty or invalid"):
        analyze_message(bad_input)  # type: ignore[arg-type]



@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("URGENT HELP", True),
        ("please reply asap", True),
        ("I need it immediately", True),
        ("Thanks for your help", False),
        ("This is urgently needed", True),
    ],
)
def test_is_urgent(message: str, expected: bool) -> None:
    assert is_urgent(message) == expected


def test_analyze_message() -> MessageAnalysis:
    msg = "URGENT: Where is my order?"
    result = analyze_message(msg)
    print("Actual Output:", result)
    assert result == MessageAnalysis(
        message=msg,
        category=Category.ORDER_STATUS,
        urgent=True,
    )


def test_custom_single_rule_classifier():
    rule = [Rule(Category.REFUND, re.compile(r"\bmoney\b", re.IGNORECASE))]
   
    clf = RuleBasedClassifier(rule)

    print("dsff", clf.classify("I want my money"))
    rule.clear()
    print("ppp", clf.classify("I want my money"))

    # assert clf.classify("I want my money") == Category.REFUND

    # assert clf.classify("hello") == Category.GENERAL


import pytest

from supportops.classifier import analyze_message, classify_message, is_urgent


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
    ("message", "expected"),
    [
        ("URGENT HELP", True),
        ("please reply asap", True),
        ("I need it immediately", True),
        ("Thanks for your help", False),
        ("This is urgently needed", True),
        ("", False),
    ],
)
def test_is_urgent(message: str, expected: bool) -> None:
    assert is_urgent(message) == expected


def test_analyze_message() -> None:
    msg = "URGENT: Where is my order?"
    result = analyze_message(msg)

    assert result == {
        "message": msg,
        "category": "order_status",
        "urgent": True,
    }

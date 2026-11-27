import re
from dataclasses import dataclass
from enum import StrEnum


class Category(StrEnum):
    ESCALATE = "escalate"
    REFUND = "refund"
    TECHNICAL = "technical"
    ORDER_STATUS = "order_status"
    GENERAL = "general"


@dataclass(frozen=True, slots=True)
class MessageAnalysis:
    message: str
    category: Category
    urgent: bool

@dataclass(frozen=True, slots=True)
class Rule:
    category: Category
    pattern: re.Pattern[str]
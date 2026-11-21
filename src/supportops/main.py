import logging

from supportops.classifier import analyze_message
from supportops.exceptions import InvalidMessageError
from supportops.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Execute the core customer support triage processing workspace."""

    setup_logging()

    test_messages = [
        "My order is late, I want to speak to your manager",
        "Where is my order? It has been delayed.",
        "I need a full refund immediately!",
        "PLEASE FIX THIS LOGIN ERROR RIGHT NOW",
        "Just wanted to say thank you for your help.",
        "",
        "   ", 
        None, 
    ]

    logger.info("Starting SupportOps triage")
    print("--- Processing Customer Messages ---\n")
    for msg in test_messages:
        try:
            analysis = analyze_message(msg)
            
        except InvalidMessageError as e:
            logger.warning("Skipping invalid message: %s", e)
        else:
            print(f"Message:  '{analysis.message}'")
            print(f"Category: {analysis.category}")
            print(f"Urgent:   {analysis.urgent}")
        print("-" * 40)

if __name__ == "__main__":
    main()

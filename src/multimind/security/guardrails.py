"""Guardrails for MultiMind AI Platform — input validation and safety checks."""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class GuardrailCheck:
    """Result of a single guardrail check."""
    check_name: str
    passed: bool
    message: str
    severity: str = "info"  # info, warning, block


class Guardrails:
    """Input guardrails to protect against prompt injection, data leaks, etc."""

    # Common prompt injection patterns
    PROMPT_INJECTION_PATTERNS = [
        r"(ignore\s+previous\s+instructions|system\s*:\s*prompt)",
        r"(ignore\s+instructions|bypass\s+restrictions)",
        r"(jailbreak|escape\s+from\s+this)",
        r"(system\s+prompt\s+leak|reveal\s+your\s+instructions)",
        r"(simulate\s+a\s+different\s+ai)",
        r"(act\s+as\s+a\s+different)",
    ]

    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO|UPDATE\s+.*SET)",
        r"(UNION\s+SELECT|SELECT\s+.*FROM\s+information_schema)",
        r"(;\s*--|;\s*/\*|\bOR\s+1\s*=\s*1)",
    ]

    # PII patterns
    PII_PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "phone": r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    }

    @classmethod
    def check_prompt_injection(cls, text: str) -> GuardrailCheck:
        """Check for prompt injection attempts in user input."""
        text_lower = text.lower()
        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return GuardrailCheck(
                    check_name="Prompt Injection Detection",
                    passed=False,
                    message="Prompt injection pattern detected. Request blocked.",
                    severity="block",
                )
        return GuardrailCheck(
            check_name="Prompt Injection Detection",
            passed=True,
            message="No prompt injection patterns detected.",
            severity="info",
        )

    @classmethod
    def check_sql_injection(cls, text: str) -> GuardrailCheck:
        """Check for SQL injection attempts in user input."""
        text_upper = text.upper()
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return GuardrailCheck(
                    check_name="SQL Injection Detection",
                    passed=False,
                    message="SQL injection pattern detected. Request blocked.",
                    severity="block",
                )
        return GuardrailCheck(
            check_name="SQL Injection Detection",
            passed=True,
            message="No SQL injection patterns detected.",
            severity="info",
        )

    @classmethod
    def check_pii_masking(cls, text: str) -> GuardrailCheck:
        """Detect PII in user input and mask it."""
        detected = []
        masked_text = text

        for pii_type, pattern in cls.PII_PATTERNS.items():
            matches = re.findall(pattern, text)
            for match in matches:
                detected.append({"type": pii_type, "value": match})
                masked_text = masked_text.replace(match, f"<{pii_type.upper()}_MASKED>")

        if detected:
            return GuardrailCheck(
                check_name="PII Masking",
                passed=True,
                message=f"Detected {len(detected)} PII elements. Masked in output.",
                severity="warning",
            )
        return GuardrailCheck(
            check_name="PII Masking",
            passed=True,
            message="No PII detected.",
            severity="info",
        )

    @classmethod
    def run_all_checks(cls, text: str) -> List[GuardrailCheck]:
        """Run all guardrail checks on user input."""
        return [
            cls.check_prompt_injection(text),
            cls.check_sql_injection(text),
            cls.check_pii_masking(text),
        ]

    @classmethod
    def is_safe(cls, text: str) -> bool:
        """Return True if all guardrail checks pass."""
        return all(check.passed for check in cls.run_all_checks(text))

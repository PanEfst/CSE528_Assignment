
import json
import re

ALLOWED_LABELS = {"TOXIC", "NON_TOXIC", "DEFER"}

ALLOWED_CATEGORIES = {
    "insult",
    "threat",
    "hate",
    "harassment",
    "profanity",
    "other",
    "none"
}

STRONG_TOXIC_CATEGORIES = {
    "insult",
    "threat",
    "hate",
    "harassment",
    "profanity"
}

REQUIRED_FIELDS = {
    "label",
    "category",
    "confidence",
    "short_rationale"
}


def fallback_defer(reason="Invalid model output; deferred for safety."):
    return {
        "label": "DEFER",
        "category": "none",
        "confidence": 0.0,
        "short_rationale": reason
    }


def extract_json_candidate(text):
    if not isinstance(text, str):
        return None

    text = text.strip()

    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    if text.startswith("{") and text.endswith("}"):
        return text

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        return match.group(0).strip()

    return None


def normalize_label_and_category(parsed):
    repaired = False

    raw_label = parsed.get("label")
    raw_category = parsed.get("category")

    if isinstance(raw_label, str):
        label_clean = raw_label.strip()
        label_upper = label_clean.upper()
        label_lower = label_clean.lower()
    else:
        return parsed, repaired

    if isinstance(raw_category, str):
        category_clean = raw_category.strip().lower()
    else:
        category_clean = "none"

    if label_upper in ALLOWED_LABELS:
        parsed["label"] = label_upper

        if category_clean in ALLOWED_CATEGORIES:
            parsed["category"] = category_clean
        else:
            parsed["category"] = "none"
            repaired = True

        return parsed, repaired

    if label_lower in STRONG_TOXIC_CATEGORIES:
        parsed["label"] = "TOXIC"
        parsed["category"] = label_lower
        repaired = True
        return parsed, repaired

    if label_lower in {"toxic", "unsafe", "offensive", "harmful"}:
        parsed["label"] = "TOXIC"
        parsed["category"] = category_clean if category_clean in ALLOWED_CATEGORIES and category_clean != "none" else "other"
        repaired = True
        return parsed, repaired

    if label_lower in {"non-toxic", "nontoxic", "safe", "benign", "neutral"}:
        parsed["label"] = "NON_TOXIC"
        parsed["category"] = "none"
        repaired = True
        return parsed, repaired

    if label_lower in {"uncertain", "unknown", "ambiguous", "abstain"}:
        parsed["label"] = "DEFER"
        parsed["category"] = "none"
        repaired = True
        return parsed, repaired

    if label_lower == "none" and category_clean == "none":
        parsed["label"] = "NON_TOXIC"
        parsed["category"] = "none"
        repaired = True
        return parsed, repaired

    return parsed, repaired


def validate_json_output(model_output):
    candidate = extract_json_candidate(model_output)

    if candidate is None:
        return fallback_defer("No JSON object found; deferred for safety."), False, "No JSON object found"

    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as e:
        return fallback_defer("JSON parsing failed; deferred for safety."), False, str(e)

    if not isinstance(parsed, dict):
        return fallback_defer("Output is not a JSON object; deferred for safety."), False, "Output is not a dict"

    missing_fields = REQUIRED_FIELDS - set(parsed.keys())
    if missing_fields:
        return fallback_defer("Missing required JSON fields; deferred for safety."), False, f"Missing fields: {missing_fields}"

    parsed, repaired = normalize_label_and_category(parsed)

    label = parsed.get("label")
    category = parsed.get("category")
    confidence = parsed.get("confidence")
    rationale = parsed.get("short_rationale")

    if label not in ALLOWED_LABELS:
        return fallback_defer("Invalid or ambiguous label; deferred for safety."), False, f"Invalid label: {label}"

    if category not in ALLOWED_CATEGORIES:
        return fallback_defer("Invalid category; deferred for safety."), False, f"Invalid category: {category}"

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        return fallback_defer("Invalid confidence value; deferred for safety."), False, "Confidence is not numeric"

    if confidence < 0.0 or confidence > 1.0:
        return fallback_defer("Confidence outside valid range; deferred for safety."), False, "Confidence out of range"

    if not isinstance(rationale, str):
        return fallback_defer("Invalid rationale; deferred for safety."), False, "Rationale is not a string"

    parsed["confidence"] = confidence

    if parsed["label"] in {"NON_TOXIC", "DEFER"}:
        parsed["category"] = "none"

    if repaired:
        return parsed, True, "Schema repaired"

    return parsed, True, None

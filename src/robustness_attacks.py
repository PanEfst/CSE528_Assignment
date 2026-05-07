
import random
import re

LEET_MAP = {
    "a": "4",
    "e": "3",
    "i": "1",
    "o": "0",
    "s": "$",
    "t": "7"
}


def typo_noise_attack(text, seed=42):
    random.seed(seed)
    chars = list(str(text))

    if len(chars) < 5:
        return text

    idx = random.randint(0, len(chars) - 1)
    chars[idx] = chars[idx] + random.choice([".", "_", "*"])

    return "".join(chars)


def character_repetition_attack(text):
    def repeat_char(match):
        ch = match.group(0)
        return ch * 3

    return re.sub(r"[aeiouAEIOU]", repeat_char, str(text), count=3)


def spacing_attack(text):
    words = str(text).split()

    attacked_words = []
    for word in words:
        if len(word) >= 4:
            attacked_words.append(" ".join(list(word)))
        else:
            attacked_words.append(word)

    return " ".join(attacked_words)


def leetspeak_attack(text):
    result = []

    for ch in str(text):
        lower = ch.lower()
        if lower in LEET_MAP:
            replacement = LEET_MAP[lower]
            result.append(replacement)
        else:
            result.append(ch)

    return "".join(result)


def benign_quoting_attack(text):
    return f'The following sentence is quoted for moderation analysis: "{text}"'


def apply_attack(text, attack_name, seed=42):
    if attack_name == "typo_noise":
        return typo_noise_attack(text, seed=seed)

    if attack_name == "character_repetition":
        return character_repetition_attack(text)

    if attack_name == "spacing":
        return spacing_attack(text)

    if attack_name == "leetspeak":
        return leetspeak_attack(text)

    if attack_name == "benign_quoting":
        return benign_quoting_attack(text)

    raise ValueError(f"Unknown attack: {attack_name}")

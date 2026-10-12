import re
import sys
from pathlib import Path


def extract_features(vhdl_file):
    path = Path(vhdl_file)

    if not path.exists():
        raise FileNotFoundError(f"VHDL file not found: {vhdl_file}")

    text = path.read_text(encoding="utf-8", errors="ignore")

    # Remove VHDL comments
    text_no_comments = re.sub(r"--.*", "", text)

    features = {}

    # Basic design information
    features["input_count"] = len(
        re.findall(r"\b\w+\s*:\s*in\b", text_no_comments, re.IGNORECASE)
    )

    features["output_count"] = len(
        re.findall(r"\b\w+\s*:\s*out\b", text_no_comments, re.IGNORECASE)
    )

    features["signal_count"] = len(
        re.findall(r"\bsignal\s+\w+", text_no_comments, re.IGNORECASE)
    )

    features["process_count"] = len(
        re.findall(r"\bprocess\s*(?:\([^)]*\))?", text_no_comments, re.IGNORECASE)
    )

    # Operators
    features["and_count"] = len(
        re.findall(r"\band\b", text_no_comments, re.IGNORECASE)
    )

    features["or_count"] = len(
        re.findall(r"\bor\b", text_no_comments, re.IGNORECASE)
    )

    features["xor_count"] = len(
        re.findall(r"\bxor\b", text_no_comments, re.IGNORECASE)
    )

    features["not_count"] = len(
        re.findall(r"\bnot\b", text_no_comments, re.IGNORECASE)
    )

    # Arithmetic operators / constructs
    features["add_count"] = len(
        re.findall(r"\+", text_no_comments)
    )

    features["sub_count"] = len(
        re.findall(r"-", text_no_comments)
    )

    features["mul_count"] = len(
        re.findall(r"\*", text_no_comments)
    )

    # Control structures
    features["if_count"] = len(
        re.findall(r"\bif\b", text_no_comments, re.IGNORECASE)
    )

    features["case_count"] = len(
        re.findall(r"\bcase\b", text_no_comments, re.IGNORECASE)
    )

    features["loop_count"] = len(
        re.findall(
            r"\b(for|while|loop)\b",
            text_no_comments,
            re.IGNORECASE
        )
    )

    # Multiplexer-related structures
    features["when_count"] = len(
        re.findall(r"\bwhen\b", text_no_comments, re.IGNORECASE)
    )

    # Clock/reset indicators
    features["clocked_process"] = int(
        bool(
            re.search(
                r"(rising_edge|falling_edge)",
                text_no_comments,
                re.IGNORECASE
            )
        )
    )

    features["reset_present"] = int(
        bool(
            re.search(
                r"\b(reset|rst)\b",
                text_no_comments,
                re.IGNORECASE
            )
        )
    )

    # Register estimate
    features["register_count"] = int(
        features["clocked_process"] > 0
    )

    # Lines of code
    features["loc"] = len(
        [
            line
            for line in text_no_comments.splitlines()
            if line.strip()
        ]
    )

    return features


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python extract_features.py <vhdl_file>")
        sys.exit(1)

    vhdl_file = sys.argv[1]

    try:
        features = extract_features(vhdl_file)

        print("\nRTL FEATURES")
        print("=" * 35)

        for name, value in features.items():
            print(f"{name:20s}: {value}")

    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
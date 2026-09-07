import re
import sys
from pathlib import Path

SUPPORTED_SIZES = (2, 3)
MAX_PLAINTEXT_LENGTH = 5_000


def normalize_plaintext(text):
    """Filter ASCII before lowercasing, preserving only English letters."""
    return "".join(c for c in text if "A" <= c <= "Z" or "a" <= c <= "z").lower()


def pad_plaintext(plaintext, size):
    return plaintext + "x" * ((size - len(plaintext) % size) % size)


def validate_key_matrix(matrix):
    size = len(matrix)
    if size not in SUPPORTED_SIZES:
        raise ValueError("Key dimension must be 2 or 3.")
    if any(len(row) != size for row in matrix):
        raise ValueError("The key must be square, with every value present.")
    if any(type(value) is not int for row in matrix for value in row):
        raise ValueError("Every key value must be an integer.")
    return [[value % 26 for value in row] for row in matrix]


def read_key_matrix(filename):
    # A short bounded key file is sufficient for at most nine integers.
    with Path(filename).open(encoding="utf-8") as source:
        content = source.read(4_097)
    if len(content) > 4_096:
        raise ValueError("Key file must contain at most 4,096 characters.")
    lines = content.splitlines()
    if not lines or lines[0].strip() not in ("2", "3"):
        raise ValueError("The first line of the key file must be 2 or 3.")
    size = int(lines[0].strip())
    if len(lines) != size + 1:
        raise ValueError(f"Expected exactly {size} key rows after the dimension.")
    matrix = []
    for row_number, line in enumerate(lines[1:], start=1):
        cells = line.split()
        if len(cells) != size:
            raise ValueError(f"Key row {row_number} must contain {size} integers.")
        if any(re.fullmatch(r"[+-]?[0-9]+", cell) is None for cell in cells):
            raise ValueError(f"Key row {row_number} contains a malformed integer.")
        matrix.append([int(cell) for cell in cells])
    return validate_key_matrix(matrix)


def read_plaintext(filename):
    with Path(filename).open(encoding="utf-8") as source:
        text = source.read(MAX_PLAINTEXT_LENGTH + 1)
    if len(text) > MAX_PLAINTEXT_LENGTH:
        raise ValueError("Plaintext must contain at most 5,000 characters.")
    return text


def hill_cipher_encrypt(plaintext, key_matrix):
    if len(plaintext) > MAX_PLAINTEXT_LENGTH:
        raise ValueError("Plaintext must contain at most 5,000 characters.")
    matrix = validate_key_matrix(key_matrix)
    normalized = normalize_plaintext(plaintext)
    if not normalized:
        raise ValueError("Plaintext must contain at least one ASCII letter.")
    size = len(matrix)
    padded = pad_plaintext(normalized, size)
    ciphertext = []
    for offset in range(0, len(padded), size):
        vector = [ord(char) - ord("a") for char in padded[offset:offset + size]]
        for row in matrix:
            value = sum(entry * letter for entry, letter in zip(row, vector)) % 26
            ciphertext.append(chr(value + ord("a")))
    return "".join(ciphertext)


def output_ciphertext(ciphertext):
    print("\nCiphertext:")
    for offset in range(0, len(ciphertext), 80):
        print(ciphertext[offset:offset + 80])


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("Usage: python3 HillCipher.py key.txt plaintext.txt", file=sys.stderr)
        return 2
    try:
        key_matrix = read_key_matrix(args[0])
        plaintext = read_plaintext(args[1])
        ciphertext = hill_cipher_encrypt(plaintext, key_matrix)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    normalized = normalize_plaintext(plaintext)
    padding_count = (len(key_matrix) - len(normalized) % len(key_matrix)) % len(key_matrix)
    print("\nKey matrix:")
    for row in key_matrix:
        print(" ".join(str(value) for value in row))
    print("\nNormalized plaintext:")
    print(normalized)
    print(f"\nPadding: {padding_count} x character(s)")
    output_ciphertext(ciphertext)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# HillCipherEncrypt

The original Python reference implementation of the Hill cipher, a classical cipher based on matrix multiplication.

**Educational use only.** The Hill cipher is not secure for protecting modern sensitive information.

## Related interactive demonstration

- Original/reference implementation: this Python repository.
- Interactive browser demonstration: built with Next.js and TypeScript.

## Requirements

Python 3.9 or newer. The replacement implementation uses only the standard library; NumPy is not required.

## Input files

Create a UTF-8 key file, such as `key.txt`, with the dimension on the first line followed by exactly that many rows of integers.

```text
2
3 3
2 5
```

Supported dimensions are 2×2 and 3×3. Each row must contain exactly n signed decimal integers. Negative values and values above 25 are reduced modulo 26. The key file is limited to 4,096 characters.

Create a UTF-8 plaintext file, such as `plaintext.txt`:

```text
help
```

Raw plaintext is limited to 5,000 characters. Only ASCII A–Z/a–z is retained; retained letters become lowercase. The program appends x until the normalized length is divisible by the key dimension. Empty normalized plaintext is rejected.

## Run

```sh
python3 HillCipher.py key.txt plaintext.txt
```

The program prints the normalized key, normalized plaintext, padding count, and ciphertext to the terminal. For the example above, the ciphertext is `hiat`.

To save the entire printed report:

```sh
python3 HillCipher.py key.txt plaintext.txt > report.txt
```

No output file is created unless you explicitly redirect output.

## How it works

1. Keep only ASCII letters and convert to lowercase.
2. Pad with x to a complete block.
3. Convert a=0 through z=25.
4. Treat each block as a column vector p.
5. Calculate c = K × p modulo 26.
6. Convert the values back to lowercase letters.

A 3×3 example key is:

```text
3
6 24 1
13 16 10
20 17 15
```

With plaintext `act`, it produces `poh`.

This script performs encryption only. A noninvertible key can produce ciphertext, but reversible Hill cipher decryption requires an invertible key modulo 26.

## Errors and privacy

Incorrect arguments exit with status 2. File, encoding, or validation errors print a concise message to stderr and exit with status 1.

Files are processed locally; the script has no network functionality. It prints plaintext in its report, so consider terminal history and explicitly redirected files when using it. Do not use this classical cipher for real secrets.

## Historical note

The original version used NumPy, mixed naming styles, and included an unused padding helper. This cleaned-up reference uses consistent snake_case, validates input, pads before block processing, and places CLI execution behind a main entry-point guard.

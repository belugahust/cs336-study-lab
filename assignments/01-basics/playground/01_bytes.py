"""First exercise: strings -> UTF-8 bytes -> symbols -> one chosen merge.

Run from the repository root:
    python assignments/01-basics/playground/01_bytes.py

This is a demonstration, not a complete BPE trainer or tokenizer.
"""

text = "你好，AI"  # Change this sentence, save the file, then run it again.
encoded = text.encode("utf-8")

print("1. Original string:", text)
print("2. Character count:", len(text))
print("3. UTF-8 bytes:", encoded)
print("4. Byte count:", len(encoded))
print("5. Byte values (integers):", list(encoded))
print("6. One-byte symbols:", [bytes([value]) for value in encoded])
print("7. Decoded string:", encoded.decode("utf-8"))
assert encoded.decode("utf-8") == text

# Show one already-chosen merge. A real BPE trainer must also handle
# pre-tokenization, counts/frequencies, ties, special tokens, and many rounds.
symbols = [b"a", b"b", b"a", b"b", b"a"]
pair = (b"a", b"b")
merged = []
position = 0
while position < len(symbols):
    if position + 1 < len(symbols) and (symbols[position], symbols[position + 1]) == pair:
        merged.append(symbols[position] + symbols[position + 1])
        position += 2
    else:
        merged.append(symbols[position])
        position += 1
print("\n8. Before one chosen merge:", symbols)
print("9. Chosen pair:", pair)
print("10. After merge:", merged)
assert b"".join(merged) == b"".join(symbols)
print("\nTry changing text or symbols; predict the output before running.")

"""Your A1 BPE implementation starts here (a blank scaffold, not a solution).

Read ../BEGINNER_START_HERE.md and the official handout before implementing.
Connect this function using tests/adapters.py::run_train_bpe when ready.
"""
from __future__ import annotations

import os


def train_bpe(
    input_path: str | os.PathLike,
    vocab_size: int,
    special_tokens: list[str],
    **kwargs,
) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:
    """Train byte-level BPE as specified in the official A1 handout.

    input_path: Path to a UTF-8 corpus, not the corpus text itself.
    vocab_size: Total target vocabulary size, including special tokens.
    special_tokens: Strings handled according to the handout's boundary rules.

    Return:
        vocab: token ID -> bytes
        merges: ordered pairs of byte strings, in learned merge order
    """
    # TODO 1: Read the corpus and isolate special-token boundaries.
    # TODO 2: Pre-tokenize using the pattern and rules in the handout.
    # TODO 3: Initialize the byte vocabulary and special tokens.
    # TODO 4: Count adjacent pairs; pick the most frequent using specified ties.
    # TODO 5: Merge non-overlapping occurrences, update counts/vocab/rules.
    # TODO 6: Repeat until the requested vocabulary size (or no pairs remain).
    # TODO 7: Return vocab, merges; compare small examples before large runs.
    raise NotImplementedError("Implement train_bpe here, then connect the adapter.")

"""Shared helpers for Advent of Code solutions."""
from pathlib import Path


def input_path(caller_file, name="input.txt"):
    """Resolve an AoC puzzle input living in the shared top-level ``inputs/`` tree.

    Puzzle inputs are kept OUTSIDE the language solution trees so the same input
    can be reused across languages. The layout mirrors the solution path:

        python/adventofcode/<year>/<day>/<solution>.py   (solution)
        inputs/adventofcode/<year>/<day>/input.txt         (shared input)

    :param caller_file: the calling solution's ``__file__``.
    :param name: the input file name (default ``"input.txt"``).
    :returns: a ``Path`` to the input file (resolvable regardless of cwd).
    """
    here = Path(caller_file).resolve()
    # The language root is the nearest ancestor directory named "python".
    lang_root = next(p for p in here.parents if p.name == "python")
    rel = here.parent.relative_to(lang_root)  # e.g. adventofcode/2021/10
    return lang_root.parent / "inputs" / rel / name

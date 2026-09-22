"""
Parsing molecular sum formulas with a regular grammar, in linear time.

A molecular formula like "CH2Cl2" is just a sequence of (element, count) groups:

    C    ->  C  x1
    H2   ->  H  x2
    Cl2  ->  Cl x2

The set of well-formed formulas is a *regular* language, so it can be recognised
by a finite-state machine (FSM) in a single left-to-right pass, O(n) in the
length of the string, with no backtracking and no parse table. A context-free
parser would build a table over substrings; here we never look back.

This is a miniature of the approach from my master's thesis: a regular grammar
(see reg_sumFormula.g4) compiled to an FSM, with a small "event handler" that
emits a token whenever a group is complete. In the grammar, transitions marked
`f` are where the handler fires; transitions marked `-` just move state.

States (same names as the diagram): START, UC (uppercase), LC (lowercase),
DIGIT, END.

Run:
    python parse_formula.py                 # parse a few examples
    python parse_formula.py CH2Cl2 --trace  # watch the FSM step through it
    python parse_formula.py --benchmark     # show the parse time stays linear
"""

from __future__ import annotations
import sys
import time


class FormulaError(ValueError):
    """Raised when the input is not a well-formed sum formula."""


def parse(formula: str, trace: bool = False) -> list[tuple[str, int]]:
    """Parse a sum formula into a list of (element, count) pairs.

    Implemented as the finite-state machine from reg_sumFormula.g4. Each input
    character causes exactly one transition, so the whole parse is one linear
    pass over the string.
    """
    state = "START"
    element = ""          
    digits = ""           
    out: list[tuple[str, int]] = []

    def emit() -> None:
        if element:
            out.append((element, int(digits) if digits else 1))

    def step(msg: str) -> None:
        if trace:
            shown = digits or ("" if element else "")
            print(f"  {state:5} | read {msg}")

    for ch in formula:
        if ch.isspace():
            continue
        if "A" <= ch <= "Z":                       
            emit()                                 
            element, digits = ch, ""
            state = "UC"
        elif "a" <= ch <= "z":                     
            if state not in ("UC", "LC"):
                raise FormulaError(f"unexpected lowercase '{ch}' in {formula!r}")
            element += ch
            state = "LC"
        elif "0" <= ch <= "9":                     
            if state == "START":
                raise FormulaError(f"formula cannot start with a digit: {formula!r}")
            digits += ch
            state = "DIGIT"
        else:
            raise FormulaError(f"illegal character {ch!r} in {formula!r}")
        step(repr(ch))

    emit()                                         # EOF ($): flush the final group
    state = "END"
    if trace:
        print(f"  {state:5} | done")
    if not out:
        raise FormulaError(f"empty or invalid formula: {formula!r}")
    return out


def tally(pairs: list[tuple[str, int]]) -> dict[str, int]:
    """Sum repeated elements, e.g. [('C',1),('H',4),('O',1)] stays as-is,
    but 'CH3CH3' -> {'C': 2, 'H': 6}."""
    totals: dict[str, int] = {}
    for el, n in pairs:
        totals[el] = totals.get(el, 0) + n
    return totals


def _demo() -> None:
    examples = ["CH2Cl2", "H2O", "C6H12O6", "NaCl", "CH3CH2OH"]
    print("Parsing sum formulas with a regular-grammar FSM (linear time)\n")
    for f in examples:
        pairs = parse(f)
        totals = tally(pairs)
        atoms = sum(totals.values())
        pretty = ", ".join(f"{el}:{n}" for el, n in totals.items())
        print(f"  {f:9} -> {pretty:20} ({atoms} atoms)")
    print("\nTry:  python parse_formula.py CH2Cl2 --trace")


def _benchmark() -> None:
    print("Parse time vs. formula length (should grow linearly)\n")
    print("  length (chars) | time per parse")
    for reps in (10, 100, 1000, 10000):
        formula = "CH2Cl2" * reps
        t0 = time.perf_counter()
        parse(formula)
        dt = time.perf_counter() - t0
        print(f"  {len(formula):>14,} | {dt * 1e3:8.3f} ms")
    print("\nTime scales with length, not with length squared or cubed; that's the point.")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    if "--benchmark" in args:
        _benchmark()
    elif not args:
        _demo()
    else:
        trace = "--trace" in args
        formulas = [a for a in args if not a.startswith("--")]
        for f in formulas:
            print(f"\n{f}")
            pairs = parse(f, trace=trace)
            totals = tally(pairs)
            print("  result:", ", ".join(f"{el}:{n}" for el, n in totals.items()))

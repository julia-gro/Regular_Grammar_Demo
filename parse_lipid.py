"""
Validating glycerolipid shorthand names against a regular grammar.

This is the harder, more interesting sibling of parse_formula.py. It reads the
Shorthand2020 glycerolipid grammar in reg_GL_chains.g4, builds the finite-state
machine it describes, and uses it to decide whether a lipid name is *well formed*.

The point isn't just parsing; it's rejection. A lipid name can look completely
plausible and still be invalid, because the notation has structural rules:

  * "/"  (sn-position level) requires all THREE chains to be given.
  * "_"  (molecular-species level) fixes the NUMBER of chains per head group
         (2 for DG, 3 for TG).
  * the head group (MG/DG/TG) must be one the grammar knows.

(Regular grammars and regular expressions describe the same class of languages,
so this isn't about theoretical power; it's about writing something correct and
maintainable instead of an unreadable mega-regex.)

Run:
    python parse_lipid.py                     # the accept / reject table
    python parse_lipid.py "DG 12:1_10:0"      # check one name
    python parse_lipid.py "TG 23:1/12:0" -v   # explain why it fails
"""

from __future__ import annotations
import os
import re
import sys

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "reg_GL_chains.g4")

START_RULE = {"MG": "mg_chain_1", "DG": "dg_chain_1", "TG": "tg_chain_1"}


def load_grammar(path: str) -> dict[str, list[tuple]]:
    """Read the .g4 and return {state: [(kind, value, target), ...]}.

    kind is 'digit' (any [0-9]), 'lit' (a literal like ':' or 'O-'), or
    'accept' (the '$' / EOF alternative). Only the chain rules are needed;
    lexer tokens and the '$ : EOF;' definition are handled specially.
    """
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"//[^\n]*", "", text)                 

    rules_raw, buf, in_quote = [], "", False
    for ch in text:
        if ch == "'":
            in_quote = not in_quote
            buf += ch
        elif ch == ";" and not in_quote:
            rules_raw.append(buf)
            buf = ""
        else:
            buf += ch

    transitions: dict[str, list[tuple]] = {}
    for rule in rules_raw:
        rule = rule.strip()
        if ":" not in rule:
            continue
        name, body = rule.split(":", 1)
        name = name.strip()
        if name in ("grammar reg_GL_chains", "$", "WHITESPACE", "NEWLINE", "grammar"):
            continue
        if name.startswith("grammar"):
            continue
        alts = []
        for alt in body.split("|"):
            tokens = alt.split()
            if not tokens:
                continue
            if tokens[0] == "$":
                alts.append(("accept", None, None))
                continue
            head = tokens[0]
            target = tokens[1] if len(tokens) > 1 else None
            if head == "[0-9]":
                alts.append(("digit", None, target))
            elif head.startswith("'") and head.endswith("'"):
                alts.append(("lit", head[1:-1], target))
        if alts:
            transitions[name] = alts
    return transitions


class Matcher:
    """Runs the FSM. Tracks how far into the string it got, for error messages."""

    def __init__(self, grammar: dict[str, list[tuple]]):
        self.g = grammar
        self.furthest = 0

    def accepts(self, state: str, s: str, pos: int = 0) -> bool:
        self.furthest = max(self.furthest, pos)
        for kind, value, target in self.g.get(state, ()):
            if kind == "accept":
                if pos == len(s):
                    return True
            elif kind == "digit":
                if pos < len(s) and s[pos].isdigit() and self.accepts(target, s, pos + 1):
                    return True
            elif kind == "lit":
                if s.startswith(value, pos) and self.accepts(target, s, pos + len(value)):
                    return True
        return False


def validate(name: str, grammar: dict[str, list[tuple]] | None = None) -> tuple[bool, str]:
    """Return (is_valid, reason). Reason explains a rejection."""
    if grammar is None:
        grammar = load_grammar(GRAMMAR_FILE)

    s = name.strip()
    head, _, rest = s.partition(" ")
    rest = rest.strip()

    if head not in START_RULE:
        return False, f"'{head}' is not a valid glycerolipid head group (expected MG, DG or TG)"
    if not rest:
        return False, "chains are missing"

    m = Matcher(grammar)
    if m.accepts(START_RULE[head], rest):
        return True, "well-formed"

    if m.furthest >= len(rest):
        return False, "the name ends too early; the structure is incomplete (a required chain is missing)"
    bad = rest[m.furthest]
    return False, f"unexpected '{bad}' at position {m.furthest + 1} of the chain part; it breaks the level's structure"


EXAMPLES = [
    ("MG 16:2;O",          True,  "monoacylglycerol, species level with an oxygen"),
    ("MG 16:2/0:0/0:0",    True,  "sn-position level: all three positions given"),
    ("DG 12:1_10:0",       True,  "molecular species: DG needs exactly two chains"),
    ("TG 23:1",            True,  "species level, one summed chain is fine"),
    ("DG 16:0/18:1;O2",    False, "sn-position level ('/') requires THREE chains"),
    ("DG 12:1_10:0_0:0",   False, "molecular species ('_') for DG allows only TWO chains"),
    ("TG 23:1/12:0",       False, "TG at sn-position level needs THREE chains"),
    ("MG",                 False, "chains are missing"),
    ("RG 12:1",            False, "RG is not a valid head group"),
]


def _table() -> None:
    grammar = load_grammar(GRAMMAR_FILE)
    print("Validating Shorthand2020 glycerolipid names against the grammar\n")
    print(f"  {'name':<20} {'verdict':<9} why")
    print(f"  {'-'*20} {'-'*9} {'-'*45}")
    ok = True
    for name, expected, note in EXAMPLES:
        valid, reason = validate(name, grammar)
        verdict = "VALID" if valid else "REJECTED"
        mark = "OK" if valid == expected else "NOT OK (unexpected!)"
        if valid != expected:
            ok = False
        shown = reason if not valid else note
        print(f"  {name:<20} {verdict:<9} {shown}  {mark if valid != expected else ''}".rstrip())
    print("\nEvery verdict matches the grammar's rules." if ok else "\nMismatch; check the grammar.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        _table()
    else:
        verbose = any(a in ("-v", "--verbose") for a in args)
        names = [a for a in args if not a.startswith("-")]
        grammar = load_grammar(GRAMMAR_FILE)
        for name in names:
            valid, reason = validate(name, grammar)
            verdict = "VALID" if valid else "REJECTED"
            line = f"{name!r}: {verdict}"
            if verbose or not valid:
                line += f": {reason}"
            print(line)

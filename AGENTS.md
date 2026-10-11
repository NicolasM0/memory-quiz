# AGENTS.md

## Project
- Single self-contained `memory.html` (inline HTML + CSS + JS): a memory card game that speaks each card's English word via the Web Speech API. Goal: build English vocabulary for French-speaking kids (FR translations + a "Traduction FR" button).
- No build step, package manager, dependencies, tests, or CI. Edit `memory.html` directly and reload it in Firefox (Ctrl+Shift+R to bypass cache).
- No Node/JS runtime here (`node`/`deno`/`bun` absent), so you cannot execute the JS. Validate edits with a `python3` regex script instead (see below).
- Repo also contains `README.md` (user-facing, in French) and `LICENSE` (CC0 1.0). Keep them in sync with the current themes/counts when you change `memory.html`.

## Data model (all inside the single `<script>`)
- `THEMES` keys: `animals`, `food`, `actions`, `objects`, `colors`, `numbers`, `body`, `clothes`, `nature`, `school`, `transport`, `jobs`, `emotions`, `shapes`, `verbs`. Each item is `{ name, emoji, label? }`; each theme has a `label`.
- `TRANSLATIONS`: EN→FR map covering exactly every item name (no unused or duplicate keys).
- Item order in `THEMES[key].items` is the canonical order (most→least common). Each item includes `level: 1|2|3` assigned by position in that order (25%/25%/50% with rounding).
- Other constants: `CARD_COUNTS`, `PREFERRED`, `MAX_VOICES` (=5), `STORAGE`.
- Card grid size/columns are computed once by `computeBoardLayout()` inside `buildDeck()` from the current viewport, then fixed. There is deliberately NO resize listener — do not add one; a new layout only happens when a new game is built.

## Invariants — keep true when editing
- Every theme item `name` MUST have a `TRANSLATIONS` entry (1315/1315 across all themes).
- Item `level` is set on each item (1|2|3). Distribution follows the order of `items` (~25/25/50).
- `name` must be unique within a theme; `emoji`/`label` may be reused if no faithful image exists. `numbers` holds the numeral in `emoji`. An optional `label` allows distinguishing same display text (e.g. "Cook Verb" internal vs "Cook" display).
- Keep `const` declarations before any immediate calls. A `const` used by an immediately-invoked function but declared later throws a TDZ error that silently kills the whole script (empty selects, no board). E.g. `MAX_VOICES` must precede `loadVoices()`.

## Speech / environment quirks
- Ubuntu + Firefox; TTS through `speech-dispatcher` + `espeak-ng`. RHVoice voices only appear if the `speech-dispatcher-rhvoice` package is installed.
- English voice is auto-scored (RHVoice/natural preferred); the dropdown is capped at `MAX_VOICES=5`. Default rate is 0.85. The "Traduction FR" button uses a separate French (`fr`) voice.
- Emojis render via `fonts-noto-color-emoji` (v2.047 / Unicode 15); newer emojis show as tofu in Firefox.
- State persists in `localStorage` under `memoryGame{Theme,Count,Level,Voice,Players,Rate}`.

## Verify an edit (no test runner)
```bash
python3 - <<'PY'
import re
h=open('memory.html').read(); s=re.search(r'<script>(.*)</script>',h,re.S).group(1)
for a,b in [('{','}'),('(',')'),('[',']')]: assert s.count(a)==s.count(b),(a,)
themes={k:re.findall(r'\{ name: "([^"]+)", emoji: "[^"]*"',b)
        for k,b in re.findall(r'^    (\w+): \{\n      label: "[^"]*",\n      items: \[(.*?)\n      \],',h,re.S|re.M)}
trbody=re.search(r'const TRANSLATIONS = \{(.*?)\n  \};',s,re.S).group(1)
trkeys=re.findall(r'"([^"]+)":\s*"', trbody)
tr=set(trkeys)
n=0; allnames=set()
for k,names in themes.items():
    assert len(names)==len(set(names)), (k, "duplicate names")
    assert all(n in tr for n in names), (k,[n for n in names if n not in tr])
    allnames|=set(names); n+=len(names)
assert len(trkeys)==len(tr), "duplicate translation keys"
assert tr==allnames, ("unused translations", sorted(tr-allnames))
print(f"OK: braces balanced; all {n} names translated; no unused/duplicate keys")
PY
```

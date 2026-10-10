# AGENTS.md

## Project
- Single self-contained `memory.html` (inline HTML + CSS + JS): a memory card game that speaks each card's English word via the Web Speech API. Goal: build English vocabulary for French-speaking kids (FR translations + a "Traduction FR" button).
- No build step, package manager, dependencies, tests, or CI. Edit `memory.html` directly and reload it in Firefox (Ctrl+Shift+R to bypass cache).
- No Node/JS runtime here (`node`/`deno`/`bun` absent), so you cannot execute the JS. Validate edits with a `python3` regex script instead (see below).

## Data model (all inside the single `<script>`)
- `THEMES` keys: `animals`, `food`, `actions`, `objects`. Each item is `{ name, emoji }`; each theme has a `label`.
- `TRANSLATIONS`: EN→FR map covering every item name.
- `LEVEL_ORDER`: per theme, item names ordered most→least common. Code derives difficulty levels 1/2/3 automatically as 25%/25%/50% of the list length.
- Other constants: `CARD_COUNTS`, `PREFERRED`, `MAX_VOICES` (=5), `STORAGE`.
- Card grid size/columns are computed once by `computeBoardLayout()` inside `buildDeck()` from the current viewport, then fixed. There is deliberately NO resize listener — do not add one; a new layout only happens when a new game is built.

## Invariants — keep true when editing
- Every theme item `name` MUST have a `TRANSLATIONS` entry (currently 447/447).
- `LEVEL_ORDER[theme]` names MUST exactly equal that theme's item names (no missing, extra, or duplicate).
- `name` and `emoji` must be unique within a theme; keep ≥100 items per theme (≥50 pairs).
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
themes={k:re.findall(r'\{ name: "([^"]+)", emoji: "[^"]+" \}',b)
        for k,b in re.findall(r'^    (\w+): \{\n      label: "[^"]*",\n      items: \[(.*?)\n      \],',h,re.S|re.M)}
lo=re.search(r'const LEVEL_ORDER = \{(.*?)\n  \};',s,re.S).group(1)
levels={k:re.findall(r'"([^"]+)"',b) for k,b in re.findall(r'(\w+): \[(.*?)\]',lo,re.S)}
tr=set(re.findall(r'"([^"]+)":\s*"', re.search(r'const TRANSLATIONS = \{(.*?)\n  \};',s,re.S).group(1)))
for k,names in themes.items():
    assert set(names)==set(levels[k]), (k, set(names)^set(levels[k]))
    assert all(n in tr for n in names), (k,[n for n in names if n not in tr])
print("OK: braces balanced; LEVEL_ORDER==THEMES; all names translated")
PY
```

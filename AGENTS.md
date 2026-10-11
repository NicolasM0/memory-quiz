# AGENTS.md

## Project
- Single self-contained `memory.html` (inline HTML + CSS + JS + data): an app with a home menu (`#home`) linking to two games — a **Memory** card game and a **Quiz** — each speaking English words via the Web Speech API. Goal: build English vocabulary for French-speaking kids (FR translations + a "Traduction FR" button in Memory).
- The whole app is one file: three `.view` containers (`#viewHome`, `#viewMemory`, `#viewQuiz`) plus four `<script>` blocks in this order: (1) data (`window.THEMES` / `window.TRANSLATIONS`), (2) Memory IIFE, (3) Quiz IIFE, (4) a tiny hash router (`#home`/`#memory`/`#quiz`). No build step, dependencies, tests, or CI.
- No Node/JS runtime here (`node`/`deno`/`bun` absent), so you cannot execute the JS. Validate edits with a `python3` script instead (see below).
- Edit `memory.html` directly and reload in Firefox (Ctrl+Shift+R to bypass cache). Repo also contains `README.md` (user-facing, in French) and `LICENSE` (CC0 1.0). Keep them in sync with the current themes/counts when you change `memory.html`.

## Data model (first `<script>`)
- `window.THEMES` keys: `animals`, `food`, `actions`, `objects`, `colors`, `numbers`, `body`, `clothes`, `nature`, `school`, `transport`, `jobs`, `emotions`, `shapes`, `verbs`. Each theme is `{ label, items: [...] }`; each item is `{ name, emoji, level, label? }`.
- `window.TRANSLATIONS`: EN→FR map covering exactly every item name (no unused or duplicate keys).
- Item order in `THEMES[key].items` is the canonical order (most→least common). Each item includes `level: 1|2|3` assigned by position in that order (25%/25%/50% with rounding).
- Memory-only constants: `CARD_COUNTS`, `PREFERRED`, `MAX_VOICES` (=5), `STORAGE`. Quiz reads `window.THEMES` too.
- Both game scripts are wrapped in IIFEs so their `const`/function names don't collide (e.g. both define `speak`, `shuffle`, `levelMapForTheme`). Data is the only shared global.
- Card grid size/columns are computed once by `computeBoardLayout()` inside `buildDeck()` from the current viewport, then fixed. There is deliberately NO resize listener — do not add one; a new layout only happens when a new game is built.

## Invariants — keep true when editing
- Every theme item `name` MUST have a `TRANSLATIONS` entry (925/925 across all themes currently).
- Item `level` is set on each item (1|2|3). Distribution follows the order of `items` (~25/25/50).
- `name` must be unique within a theme; `emoji`/`label` may be reused if no faithful image exists. `numbers` holds the numeral in `emoji`. An optional `label` allows distinguishing same display text (e.g. "Cook Verb" internal vs "Cook" display).
- Keep `const` declarations before any immediate calls. A `const` used by an immediately-invoked function but declared later throws a TDZ error that silently kills the whole script (empty selects, no board). E.g. `MAX_VOICES` must precede `loadVoices()`.
- Memory CSS is scoped under `#viewMemory`, Quiz CSS under `#viewQuiz`, the home screen under `#viewHome`. Keep that scoping: memory and quiz both define `button.reset`, `.hud`, `h1`, `*`, and `:root` differently. `#viewHome` keeps its `:root`/`*` global (they define the base `--text` etc.).
- Memory's layout runs against the `#viewMemory` container, not `document.body` (the game markup lives inside the view). `computeBoardLayout()` reads `getComputedStyle(view)` and iterates `view.children`.
- Memory is initialized lazily: the game does NOT call `reset()` at load (the view is hidden, so layout would measure 0). It exposes `window.__memoryStart = reset`, and the router calls it the first time `#memory` is shown. Quiz can init at load (its layout is CSS `vmin`-based).

## Speech / environment quirks
- Ubuntu + Firefox; TTS through `speech-dispatcher` + `espeak-ng`. RHVoice voices only appear if the `speech-dispatcher-rhvoice` package is installed.
- English voice is auto-scored (RHVoice/natural preferred); Memory's dropdown is capped at `MAX_VOICES=5`. Default rate is 0.85. The "Traduction FR" button uses a separate French (`fr`) voice.
- Both games register `speechSynthesis.addEventListener("voiceschanged", …)` (never assign `.onvoiceschanged =`, or one would clobber the other's handler).
- Emojis render via `fonts-noto-color-emoji` (v2.047 / Unicode 15); newer emojis show as tofu in Firefox.
- State persists in `localStorage`: Memory uses `memoryGame{Theme,Count,Level,Voice,Players,Rate}`; Quiz uses its own `memoryGameQuizVoice` key (kept separate so the two games don't overwrite each other's saved voice).

## Verify an edit (no test runner)
```bash
python3 - <<'PY'
import re, json
h = open('memory.html', encoding='utf-8').read()
blocks = re.findall(r'<script>(.*?)</script>', h, re.S)
assert len(blocks) == 4, f"expected 4 scripts, got {len(blocks)}"
for i, s in enumerate(blocks):
    for a, b in [('{','}'), ('(',')'), ('[',']')]:
        assert s.count(a) == s.count(b), (i, a, b)
s = blocks[0]
themes = json.loads(re.search(r'window\.THEMES = (\{.*?\});\s*window\.TRANSLATIONS', s, re.S).group(1))
tr = json.loads(re.search(r'window\.TRANSLATIONS = (\{.*\});', s, re.S).group(1))
allnames = set(); n = 0
for k, t in themes.items():
    names = [it['name'] for it in t['items']]
    assert len(names) == len(set(names)), (k, "duplicate names")
    assert all(x in tr for x in names), (k, [x for x in names if x not in tr])
    assert all(it.get('level') in (1, 2, 3) for it in t['items']), (k, "missing level")
    allnames |= set(names); n += len(names)
assert set(tr) == allnames, ("unused translations", sorted(set(tr) - allnames))
ids = re.findall(r'\bid="([^"]+)"', h)
assert len(ids) == len(set(ids)), ("duplicate ids", [i for i in ids if ids.count(i) > 1])
print(f"OK: 4 scripts balanced; {len(themes)} themes, {n} words, all translated; no duplicate ids")
PY
```

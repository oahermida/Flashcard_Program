# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A CLI flashcard tool being built as Oscar's third Python learning project. The goal is to move beyond CRUD-style data logging and into programs that make decisions based on data — weighted quizzes, spaced repetition, per-card accuracy tracking.

The full project roadmap lives in the Obsidian vault:
`/home/oscar/Documents/Uni/200 - Self-Study/Python/Projects/in production projects/Flashcard CLI — Project Roadmap.md`

**If the implementation deviates from the roadmap** (a phase is restructured, a feature is added, removed, or reordered, a design decision is made), update that file to reflect the change. The roadmap is the source of truth — keep it in sync.

---

## How to Help (Important)

Oscar is **learning Python**. Do not just give copy-paste answers unless explicitly requested.

- Explain new concepts in a general context, not just the specific use case at hand.
- When using code that's still new to the user, explain what it does and how it works generally.
- Be critical — push back when the user might be wrong rather than just agreeing.
- Ask for confirmation before creating interactive artifacts.
- When the user asks for in-depth reference material or `.md` notes, treat these as curated documentation — write them thoroughly without warning about over-relying on them.
- Nudge the user toward the *what* and the *how*, but leave space for them to make real decisions and hit problems themselves. Roadmap-style guidance, not recipes.

### Style for walking the user through implementation steps

When asking the user to implement something, scaffold it like a lesson, not a checklist:

- **Break the task into small numbered mini-steps**, each focused on one concept. Don't dump the whole task at once — even if it feels like one thing to you, split it so the user lands one idea per step.
- **Pose "why" questions before revealing the answer.** When there's a non-obvious reason something works (or fails), ask the user to guess first, then explain.
- **Name gotchas up front** so the user can watch for them while coding, rather than being surprised. Frame as *"the question worth pausing on:"* or *"the gotcha here is:"*.
- **End with a checkpoint, not a dump.** Stop after one or two steps and invite the user to try them before moving on. Don't pre-explain steps the user hasn't reached yet.
- **Describe what to do, not the code itself.** Say *"open the file in `'r'` mode inside a `with` block and call `json.load(f)`"* — don't paste the three lines. The user types it; you guide.
- **Show structural shifts visually.** When the shape of data needs to change, sketch the *shape* with a tiny example, but leave the user to write the code that produces it.

---

## Running the Code

```bash
python main.py      # Main application entry point
```

No dependencies beyond the Python standard library.

---

## Project Structure

Current:
- `main.py` — main application entry point (Phase 1 not yet started)

Planned multi-file structure (from Phase 7 — Polish & Refactor):
- `main.py` — menu loop and program entry point only
- `storage.py` — `load_deck()`, `save_deck()`, `list_decks()`
- `quiz.py` — `run_quiz()`, `build_weights()`, weight calculation
- `cards.py` — `create_card()`, `update_stats()`, accuracy computation

---

## Data Storage

- Project lives at `/home/oscar/Documents/VS_code/Flashcard_Program/`
- Deck files will live in `data/decks/` (introduced in Phase 6)
- Each deck is a separate `.json` file, e.g. `python_knowledge.json`
- Use `__file__`-anchored paths — never bare relative paths:
  ```python
  from pathlib import Path
  BASE_DIR = Path(__file__).parent
  ```

### Card data model

```python
{
    "id": "a3f9...",          # uuid4()[:8] — never identify a card by position
    "front": "What does enumerate() do?",
    "back": "Returns (index, value) pairs when looping over a list.",
    "created": "2026-04-29",
    "seen": 4,
    "correct": 3,
    "last_seen": "2026-04-29"  # None until first quiz appearance
}
```

### Deck data model

```python
{
    "name": "Python Knowledge",
    "created": "2026-04-29",
    "cards": [ ...list of card dicts... ]
}
```

---

## Roadmap Phases

1. **Card creation & persistence** — `uuid`, JSON I/O, view all cards. _(current)_
2. **Quiz mode** — `random.shuffle()`, flip cards, update seen/correct counts.
3. **Accuracy stats & weak card review** — sort by computed accuracy, filter below threshold.
4. **Weighted quiz** — `random.choices(weights=[...])`, inverse-accuracy weighting.
5. **Spaced repetition (light)** — `datetime.timedelta`, combine accuracy + days-since-seen into one weight.
6. **Multiple decks** — `pathlib.Path.glob("*.json")`, `data/decks/` folder.
7. **Polish & refactor** — split into `main.py`, `storage.py`, `quiz.py`, `cards.py`; add edit/delete card.
8. *(Optional)* **Import from text** — bulk-add cards from a pipe-delimited `.txt` file.
9. *(Optional)* **Command-line arguments** — `argparse` subcommands (`quiz`, `add`, `stats`).

## Current Progress

**Phase 1 not yet started.**

**Concepts covered in prior projects (no need to re-explain):**
- Dicts and nested dicts as data structures
- JSON file I/O — `json.load` / `json.dump`, `with open(...)` block
- `pathlib.Path` for cross-platform paths and `__file__`-anchored paths
- Input validation with `while True / try / except`
- Menu-driven program flow with numbered options
- `datetime.date.today()` and `.isoformat()`
- Separation of concerns — each action in its own function
- `if __name__ == "__main__"` guard
- F-string width specifiers for aligned column output
- Multi-file module structure

---

## Watch-Outs (From Roadmap)

- **`random.shuffle()` returns `None`.** It shuffles in-place. `shuffled = random.shuffle(cards)` silently sets `shuffled` to `None` — call it on its own line, then work with `cards`.
- **Division by zero on unseen cards.** `correct / seen` crashes when `seen == 0`. Guard every accuracy calculation — unseen cards need a default, not an error.
- **Forgetting to save after stat updates.** Quiz mode modifies card dicts in memory. Without an explicit `save_deck()` call, the session's stats are lost.
- **IDs over positions.** Never identify a card by its index in the list. Always look up by `id`.
- **`last_seen` can be `None`.** Newly created cards haven't been seen yet. Date arithmetic must handle `None` — treat it as "seen infinitely long ago" for weighting purposes.

---

## Open Design Decisions (For Later Phases)

Surface these when the user reaches the relevant phase:

- **Phase 4 (weighted quiz):** Does weighted mode replace normal shuffle, or is it a separate menu option? No right answer — Oscar should pick and write down why.
- **Phase 5 (spaced repetition):** The combined weight formula `(1 / accuracy) * (days_since + 1)` is a starting point, not a prescription. Oscar should test it and adjust.
- **Phase 6 (multiple decks):** File-per-deck vs all decks in one JSON — roadmap opts for file-per-deck (decks stay independent, easier to share or delete one). Revisit if Oscar questions it.

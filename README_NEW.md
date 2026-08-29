# Time Manager

A local-first, open-source time management agent for planning, tracking, and reviewing how people spend their time.

A user builds a personal profile once. The profile defines goals, sleep, fixed commitments, recurring responsibilities, energy patterns, preferred work windows, categories, and weekly targets.

This repository contains no personal schedule or identifying user data. Example configuration is intentionally generic.

## Current release: local core

- Profile onboarding
- Manual commitments and responsibilities
- Manual time logging
- Planned blocks
- Energy-aware planning
- Weekly capacity calculations
- Planned vs actual tracking
- Local SQLite persistence
- Deterministic chatbot commands
- Local profile stored outside source control

Calendar integrations are deliberately not included in this release. They will be developed later as a separate provider-agnostic feature.

## Run

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000.

## Profile

Choose Build your profile in the app and define goals, deadlines, sleep, fixed commitments, recurring responsibilities, energy constraints, preferred work windows, categories, and weekly targets.

The personal profile is stored locally in `data/profile.json` and should never be committed.

## Chat examples

```text
log 90 minutes research medium energy
log 2 hours project high energy
weekly summary
what should I work on tonight?
I am exhausted. Give me low-energy tasks.
```

## Design rules

1. Protect sleep before productivity.
2. Treat recovery as legitimate time.
3. Never equate planned time with completed work.
4. Match task difficulty to available energy.
5. Do not fill every available minute.
6. Separate fixed commitments from strategic time.
7. Keep personal data out of source control.
8. Make profiles portable and exportable.
9. Make deletion straightforward.
10. Keep integrations modular and optional.

## Roadmap

Phase 1: local profile, logging, planning, rollups, chatbot.

Phase 2: stronger local planning, recurring commitments, task energy, weekly review, import/export.

Phase 3: calendar adapters, conflict detection, approved write-back, colour-coded blocks, reversible sync.

Phase 4: local LLM/Ollama planning and review.

Phase 5: PWA, additional providers, task integrations, public templates, plugins.

## License

MIT.

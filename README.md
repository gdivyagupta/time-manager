# Time Manager

A local-first, open-source time management agent that combines planning, actual time tracking, energy-aware scheduling, and calendar integration.

## What this is

Time Manager is not designed to maximize calendar utilization. It is designed to maximize meaningful progress against a user's goals while respecting fixed commitments, energy, recovery, and real-world constraints.

Core concepts:

- **Fixed commitments**: work, commute, recurring tuition, appointments, sleep, etc.
- **Strategic time**: the finite hours left after fixed commitments.
- **Energy-aware scheduling**: demanding work goes into high-energy windows; low-energy periods are not falsely treated as deep-work time.
- **Actual vs planned**: calendar plans are not automatically treated as work completed.
- **Local-first**: the database and core planner work locally. AI and calendar integrations are optional.
- **Open configuration**: users can define their own goals, categories, commitments, energy rules, and calendars.

## Current stack

- Python
- FastAPI
- SQLite
- Jinja2
- Google Calendar API (optional)
- Optional local LLM adapter planned for Ollama

## Project structure

```text
.
├── app/
│   ├── main.py
│   ├── db.py
│   ├── planner.py
│   ├── agent.py
│   ├── calendar.py
│   └── templates/
├── config/
│   ├── default.json
│   └── user.example.json
├── tests/
├── data/
├── requirements.txt
├── .env.example
└── README.md
```

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Google Calendar

Calendar access is optional. The intended workflow is:

1. Connect a calendar explicitly.
2. Import upcoming events.
3. Classify events into user-configured categories.
4. Detect conflicts before scheduling anything.
5. Push approved planning blocks back to the calendar.
6. Keep agent-created events identifiable and reversible.

The first implementation uses Google Calendar OAuth. Additional calendar providers can be added through adapters.

## Chat interface

The chatbot is designed to eventually support commands such as:

```text
Log 90 minutes of research, medium energy.

I am exhausted tonight. What should I do?

Move my portfolio block from Saturday to Sunday.

How much time did I spend on Canada career work this week?

Replan the rest of this week around my new tutoring commitment.

Find three hours for deep work next week without reducing sleep.
```

The core agent should remain usable without an LLM. A deterministic command layer provides predictable local behavior, while a local LLM can provide richer intent parsing and planning later.

## Design rules

1. Do not schedule around sleep.
2. Treat recovery as a valid allocation.
3. Do not infer that a calendar event was completed work unless the user or a future integration explicitly marks it as actual.
4. Prefer high-leverage work during high-energy windows.
5. Avoid filling every available minute.
6. Never silently rewrite existing calendar events.
7. Separate personal data from source-code configuration.
8. Make export and deletion straightforward.

## Development roadmap

### Phase 1
- Local dashboard
- Manual time logging
- Planned blocks
- Weekly rollups
- Configurable categories and commitments

### Phase 2
- Google Calendar read/sync
- Conflict detection
- Calendar write-back
- Colour-coded agent-created blocks
- Recurring commitment editor

### Phase 3
- Local LLM / Ollama adapter
- Natural-language planning
- Energy-aware rescheduling
- Weekly review agent
- Goal/deadline reasoning

### Phase 4
- PWA/mobile experience
- Apple Calendar and Outlook adapters
- Import/export
- Plugins/integrations
- Public examples and templates

## Privacy

The goal is local-first operation. Credentials and personal schedule data should not be committed to Git. See `.gitignore` and `.env.example`.

## License

MIT.

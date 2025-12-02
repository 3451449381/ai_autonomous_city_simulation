# AI Autonomous City Simulation

This project implements a simple **AI Autonomous City Simulation** based on a
multi-phase workflow. Multiple agents (citizens with different roles) live
in a shared virtual city and act autonomously in daily cycles.

## Workflow

Each simulated day follows this workflow:

1. **Day Start** – Initialize daily context (weather, random events).
2. **Citizen Planning** – Each agent decides what they plan to do.
3. **Citizen Actions** – Agents execute their plans (work, shop, patrol, rest, etc.).
4. **City Update** – The global city metrics are updated (economy, safety, happiness).
5. **Reporting** – A summary of the day is printed to the console.
6. **Next Day** – The simulation advances to the next day or stops if the limit is reached.

The implementation focuses on clean workflow structure and simple, interpretable rules,
without external machine learning dependencies.

## Project Structure

```text
ai_autonomous_city_simulation/
├── README.md
├── requirements.txt
└── city_simulation/
    ├── __init__.py
    ├── city_state.py
    ├── agents.py
    ├── workflow.py
    └── main.py
```

## Requirements

- Python 3.9 or later

No third-party dependencies are required.

## How to Run

From the project root:

```bash
cd ai_autonomous_city_simulation
python -m city_simulation.main
```

By default, the simulation runs for 5 days. You can change this in `main.py`.


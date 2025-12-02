from __future__ import annotations

import random
from typing import List

from .city_state import CityState, DayContext
from .agents import Agent


class CitySimulationEngine:
    """Core engine that runs the AI Autonomous City Simulation workflow."""

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)
        self.city = CityState()
        self.agents: List[Agent] = self._create_default_agents()

    # --------- Agent setup ---------
    def _create_default_agents(self) -> List[Agent]:
        """Create a small set of agents with different roles."""
        agents: List[Agent] = [
            Agent(id=1, name="Alice", role="worker"),
            Agent(id=2, name="Bob", role="worker"),
            Agent(id=3, name="Carla", role="shop_owner"),
            Agent(id=4, name="Daniel", role="student"),
            Agent(id=5, name="Eva", role="police"),
            Agent(id=6, name="Frank", role="citizen"),
        ]
        return agents

    # --------- Workflow phases ---------
    def run(self, days: int = 5) -> None:
        """Run the full simulation for a given number of days."""
        for _ in range(days):
            self._day_start()
            ctx = self._day_context()
            plans = self._citizen_planning(ctx)
            self._citizen_actions(plans, ctx)
            self._city_update()
            self._reporting()
            self._next_day()

    def _day_context(self) -> DayContext:
        """Construct the DayContext based on weather and events."""
        weather = self._random_weather()
        events: List[str] = []

        # Simple chance for a random city-wide event
        p = self.rng.random()
        if p < 0.1:
            events.append("city_festival")
        elif p < 0.18:
            events.append("minor_economic_downturn")
        elif p < 0.25:
            events.append("crime_wave")

        return DayContext(day=self.city.day, weather=weather, events=events)

    def _day_start(self) -> None:
        """Phase 1: DAY_START – reset daily stats and display header."""
        self.city.reset_daily_stats()
        print("=" * 60)
        print(f" Day {self.city.day} begins in the Autonomous City ")
        print("=" * 60)

    def _citizen_planning(self, ctx: DayContext):
        """Phase 2: CITIZEN_PLANNING – each agent decides what to do."""
        print(f"[Planning] Weather today: {ctx.weather}. Events: {ctx.events or 'none'}")
        plans = {}
        for agent in self.agents:
            plan = agent.plan(self.city, ctx, self.rng)
            plans[agent.id] = plan
            print(f"  - {agent.name} ({agent.role}) plans to {plan.action_type}"
                  f" ({plan.note or 'no special note'}).")
        return plans

    def _citizen_actions(self, plans, ctx: DayContext) -> None:
        """Phase 3: CITIZEN_ACTIONS – execute all planned actions."""
        print("\n[Actions]")
        for agent in self.agents:
            plan = plans.get(agent.id)
            if plan is None:
                continue
            agent.act(plan, self.city, self.rng)
            last_entry = self.city.logs[-1]
            print(f"  - {agent.name} {last_entry.description}")

    def _city_update(self) -> None:
        """Phase 4: CITY_UPDATE – update global metrics based on stats."""
        stats = self.city.daily_stats

        # Economy increases with work and shop activity, slightly decays over time.
        self.city.economy += 0.5 * stats["work_count"] + 0.3 * stats["shop_count"]
        self.city.economy *= 0.995  # small decay

        # Safety increases with patrols, decreases with crime.
        self.city.safety += 0.01 * stats["patrol_count"]
        self.city.safety -= 0.03 * stats["crime_attempts"]
        self.city.safety += 0.02 * stats["crime_prevented"]

        # Happiness increases with social interactions and rest, decreases with crime.
        self.city.happiness += 0.01 * stats["social_interactions"]
        self.city.happiness += 0.005 * stats["rest_count"]
        self.city.happiness -= 0.015 * stats["crime_attempts"]

        # Clamp bounded metrics
        self.city.clamp_metrics()

    def _reporting(self) -> None:
        """Phase 5: REPORTING – print a summary of the day."""
        stats = self.city.daily_stats
        print("\n[City Update]")
        print(f"  Economy:  {self.city.economy:.1f}")
        print(f"  Safety:   {self.city.safety:.2f}")
        print(f"  Happiness:{self.city.happiness:.2f}")
        print("\n[Daily Stats]")
        for key, value in stats.items():
            print(f"  {key}: {value:.0f}")

        print("\n[Sample Log Entries]")
        # Show up to 5 most recent log entries for the day
        todays_logs = [log for log in self.city.logs if log.day == self.city.day]
        for entry in todays_logs[:5]:
            print(f"  - (Day {entry.day}) {entry.agent_name} ({entry.role}) {entry.description}")

    def _next_day(self) -> None:
        """Phase 6: NEXT_DAY – advance to the next day."""
        self.city.day += 1
        print("\nEnd of day.\n")

    def _random_weather(self) -> str:
        """Simple random weather generator."""
        return self.rng.choice(["sunny", "cloudy", "rainy", "windy"])

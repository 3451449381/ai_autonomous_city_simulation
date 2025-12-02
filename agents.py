from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from .city_state import CityState, DayContext, ActionLogEntry

ActionType = Literal["work", "shop", "rest", "patrol", "crime", "socialize"]


@dataclass
class PlannedAction:
    """A simple representation of a planned action by an agent."""

    action_type: ActionType
    target: Optional[str] = None  # e.g. location or other agent id as string
    note: str = ""


@dataclass
class Agent:
    """A basic city agent with simple decision rules.

    This implementation does not use any external AI model. All behavior is
    rule-based with some randomness, which is enough to demonstrate the
    workflow structure.
    """

    id: int
    name: str
    role: str  # e.g. "worker", "shop_owner", "student", "police"
    money: float = 50.0
    energy: float = 1.0  # 0.0 - 1.0
    mood: float = 0.5    # 0.0 - 1.0

    def plan(self, city: CityState, ctx: DayContext, rng) -> PlannedAction:
        """Decide what to do today based on role, mood, and city state."""
        # Simple rule-based behavior with randomness.

        # Low energy → more likely to rest.
        if self.energy < 0.3:
            return PlannedAction(action_type="rest", note="Too tired, staying home.")

        # Role-based preferences.
        if self.role == "worker":
            # Workers primarily work, occasionally rest or socialize.
            p = rng.random()
            if p < 0.7:
                return PlannedAction(action_type="work", target="office")
            elif p < 0.85:
                return PlannedAction(action_type="socialize", target="cafe")
            else:
                return PlannedAction(action_type="rest")

        if self.role == "shop_owner":
            # Shop owners like to open the shop; bad economy reduces motivation.
            p = rng.random()
            if city.economy < 80 and p < 0.3:
                return PlannedAction(action_type="rest", note="Economy looks bad.")
            if p < 0.75:
                return PlannedAction(action_type="shop", target="store")
            else:
                return PlannedAction(action_type="socialize", target="market")

        if self.role == "student":
            # Students may study (treated as work), socialize, or rest.
            p = rng.random()
            if p < 0.5:
                return PlannedAction(action_type="work", target="school", note="Studying.")
            elif p < 0.8:
                return PlannedAction(action_type="socialize", target="park")
            else:
                return PlannedAction(action_type="rest")

        if self.role == "police":
            # Police mostly patrol; low safety increases patrol likelihood.
            p = rng.random()
            base_patrol = 0.6 + (0.5 - city.safety)  # less safety → higher chance
            if p < base_patrol:
                return PlannedAction(action_type="patrol", target="streets")
            elif p < 0.9:
                return PlannedAction(action_type="socialize", target="station")
            else:
                return PlannedAction(action_type="rest")

        # Default: generic citizen.
        p = rng.random()
        if p < 0.4:
            return PlannedAction(action_type="work", target="generic_job")
        elif p < 0.7:
            return PlannedAction(action_type="socialize", target="square")
        else:
            return PlannedAction(action_type="rest")

    def act(self, plan: PlannedAction, city: CityState, rng) -> None:
        """Execute a planned action and update both agent and city state."""
        desc = ""

        if plan.action_type == "work":
            income = 10.0
            self.money += income
            self.energy -= 0.2
            self.mood += 0.05
            city.daily_stats["work_count"] += 1
            city.economy += 1.5
            desc = f"worked at {plan.target or 'workplace'} and earned {income:.1f}."

        elif plan.action_type == "shop":
            cost = 5.0
            if self.money >= cost:
                self.money -= cost
                self.energy -= 0.1
                self.mood += 0.1
                city.daily_stats["shop_count"] += 1
                city.economy += 1.0
                desc = f"ran the shop at {plan.target or 'store'}, trading with customers."
            else:
                desc = "wanted to run the shop but lacked resources."

        elif plan.action_type == "rest":
            self.energy = min(1.0, self.energy + 0.4)
            self.mood += 0.05
            city.daily_stats["rest_count"] += 1
            desc = "stayed home to rest."

        elif plan.action_type == "patrol":
            city.daily_stats["patrol_count"] += 1
            self.energy -= 0.2
            # Patrol reduces effective crime.
            desc = "patrolled the city streets."

        elif plan.action_type == "crime":
            city.daily_stats["crime_attempts"] += 1
            self.energy -= 0.2
            success_prob = 0.3 + (0.5 - city.safety)
            if rng.random() < success_prob:
                gain = 15.0
                self.money += gain
                self.mood += 0.1
                city.safety -= 0.05
                desc = f"successfully committed a crime and gained {gain:.1f}."
            else:
                self.mood -= 0.2
                city.daily_stats["crime_prevented"] += 1
                desc = "attempted a crime but was caught or scared away."

        elif plan.action_type == "socialize":
            city.daily_stats["social_interactions"] += 1
            self.energy -= 0.1
            self.mood += 0.1
            desc = f"socialized at {plan.target or 'a public place'}."

        # Clamp internal variables
        self.energy = max(0.0, min(1.0, self.energy))
        self.mood = max(0.0, min(1.0, self.mood))

        # Log to city
        city.log_action(
            ActionLogEntry(
                day=city.day,
                agent_id=self.id,
                agent_name=self.name,
                role=self.role,
                description=desc or f"did nothing in particular.",
            )
        )

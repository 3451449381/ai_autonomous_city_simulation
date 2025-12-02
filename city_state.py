from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class DayContext:
    """Contextual information for a single simulated day."""

    day: int
    weather: str
    events: List[str] = field(default_factory=list)


@dataclass
class ActionLogEntry:
    """Record of a single action performed by an agent."""

    day: int
    agent_id: int
    agent_name: str
    role: str
    description: str


@dataclass
class CityState:
    """Global state of the city shared across all agents."""

    day: int = 1
    economy: float = 100.0      # abstract GDP-like metric
    safety: float = 0.8         # 0.0 - 1.0
    happiness: float = 0.8      # 0.0 - 1.0

    # Aggregated statistics for the current day
    daily_stats: Dict[str, float] = field(default_factory=dict)

    # Action logs
    logs: List[ActionLogEntry] = field(default_factory=list)

    def reset_daily_stats(self) -> None:
        self.daily_stats = {
            "work_count": 0.0,
            "shop_count": 0.0,
            "patrol_count": 0.0,
            "crime_attempts": 0.0,
            "crime_prevented": 0.0,
            "social_interactions": 0.0,
            "rest_count": 0.0,
        }

    def log_action(self, entry: ActionLogEntry) -> None:
        self.logs.append(entry)

    def clamp_metrics(self) -> None:
        """Ensure safety and happiness stay in [0.0, 1.0]."""
        self.safety = max(0.0, min(1.0, self.safety))
        self.happiness = max(0.0, min(1.0, self.happiness))

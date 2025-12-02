from __future__ import annotations

from .workflow import CitySimulationEngine


def main() -> None:
    # Seed can be changed for different random runs.
    engine = CitySimulationEngine(seed=42)
    engine.run(days=5)


if __name__ == "__main__":
    main()

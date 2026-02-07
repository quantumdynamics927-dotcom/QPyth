from collections.abc import Callable


def coordinate_descent_1d(
    cost: Callable[[float], float],
    theta0: float,
    step: float,
    iters: int,
) -> list[tuple[int, float, float]]:
    """
    Simple 1D coordinate-descent-like search over a single parameter.

    At each iteration k:
      - evaluate cost(θ)
      - try θ ± step; keep the direction that lowers the cost
      - reduce step if no clear progress (simple annealing)

    This is mathematically well-defined but agnostic to the physical
    cost function—we do not claim any particular Hamiltonian unless
    one is explicitly provided.

    Returns a list of (iteration, theta, energy) tuples.
    """
    theta = theta0
    history: list[tuple[int, float, float]] = []

    for k in range(iters):
        E = cost(theta)
        history.append((k, theta, E))

        # Explore both directions
        E_plus = cost(theta + step)
        E_minus = cost(theta - step)

        if E_plus < E and E_plus <= E_minus:
            theta = theta + step
        elif E_minus < E and E_minus < E_plus:
            theta = theta - step
        else:
            # No clear progress; reduce step
            step *= 0.5

    return history


def energy_history_ascii(
    history: list[tuple[int, float, float]], bar_width: int = 10
) -> None:
    """
    Render a history of (iter, theta, energy) as ASCII bars.
    Bars are scaled linearly between min and max energy.
    """
    if not history:
        return

    energies = [E for (_, _, E) in history]
    Emin, Emax = min(energies), max(energies)
    span = max(Emax - Emin, 1e-12)

    for k, theta, E in history:
        frac = (E - Emin) / span
        blocks = bar_width - int(round(frac * bar_width))
        blocks = max(0, min(bar_width, blocks))
        bar = "█" * blocks
        print(f"Iter {k:02d}: E = {E: .8f}  θ = {theta: .5f}  {bar}")

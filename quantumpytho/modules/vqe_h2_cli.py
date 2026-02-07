"""
CLI wrapper for H₂ VQE runs, supporting both generic optimizer and physical VQE.
"""

from typing import List, Tuple

from .vqe_h2_ascii import energy_history_ascii, coordinate_descent_1d
from .vqe_h2_exact import run_vqe_h2_physical


def run_vqe_h2_cli() -> None:
    """
    Run H₂ VQE and print energy convergence history as ASCII bars.

    Tries the physically correct VQE first (requires qiskit_nature/qiskit_algorithms).
    If those packages are not installed, gracefully report the error
    rather than showing fabricated energies.
    """
    try:
        energies: List[Tuple[int, float]] = run_vqe_h2_physical()
        print("\nRunning VQE for H₂ (Physical Hamiltonian via Qiskit-Nature)...")

    except RuntimeError as e:
        print("\n[VQE H₂] Required packages not installed.")
        print(f"  Error: {e}")
        print("\nNo fake energies will be shown to preserve physical correctness.")
        print("To install: pip install qiskit-algorithms qiskit-nature")
        return

    print("Energy Convergence Path (Hartree units):")
    # Convert to (iter, theta_dummy, energy) for the ASCII printer
    hist_for_print = [(i, float(i) * 0.1, E) for (i, E) in energies]
    energy_history_ascii(hist_for_print, bar_width=10)

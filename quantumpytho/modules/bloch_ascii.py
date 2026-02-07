import numpy as np
from qiskit.quantum_info import Statevector

def one_qubit_from_angles(theta: float, phi: float) -> Statevector:
    """
    Construct a pure qubit state on the Bloch sphere:

        |ψ⟩ = cos(θ/2)|0⟩ + e^{i φ} sin(θ/2)|1⟩

    This matches the standard Bloch sphere parametrization used in
    quantum information theory and Qiskit. Parameters must satisfy:
      θ ∈ [0, π], φ ∈ [0, 2π)
    
    Returns a normalized Statevector.
    Reference: Bloch sphere definition (Kawaihome, Nielsen & Chuang)
    """
    alpha = np.cos(theta / 2.0)
    beta = np.exp(1j * phi) * np.sin(theta / 2.0)
    return Statevector([alpha, beta])

def ascii_bar(prob: float, width: int = 20) -> str:
    """
    Render a probability p ∈ [0,1] as an ASCII bar of fixed width.
    """
    prob = max(0.0, min(1.0, float(prob)))
    filled = int(round(prob * width))
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]"

def run_bloch_ascii(theta: float, phi: float, shots: int = 1024) -> None:
    """
    Compute statevector from (θ, φ), derive Born-rule probabilities |α|² and |β|²
    for |0⟩ and |1⟩, and display as ASCII bars scaled by shot count.
    
    Probabilities are mathematically exact (within float precision).
    """
    sv = one_qubit_from_angles(theta, phi)
    probs = sv.probabilities()  # |α|², |β|²
    p0, p1 = probs[0], probs[1]

    c0 = int(round(p0 * shots))
    c1 = int(round(p1 * shots))

    print(f"\nState Vector Projection (θ={theta:.6f}, φ={phi:.6f}):")
    print(sv)
    bar0 = ascii_bar(p0)
    bar1 = ascii_bar(p1)
    print(f"State |0⟩: {bar0}  {p0*100:6.2f}% ({c0} shots)")
    print(f"State |1⟩: {bar1}  {p1*100:6.2f}% ({c1} shots)")

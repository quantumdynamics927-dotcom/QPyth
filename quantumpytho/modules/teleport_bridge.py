"""
Quantum state teleportation protocol.

Standard protocol (Nielsen & Chuang, Qiskit labs):
  1. Prepare arbitrary state on qubit 0
  2. Create shared entangled Bell pair on qubits 1–2
  3. Perform Bell measurement on qubits 0–1 (Alice's qubits)
  4. Apply classically-controlled X and Z to qubit 2 (Bob's qubit)
     based on measurement outcomes
  5. Final state on qubit 2 equals the original unknown state on qubit 0

This implementation shows the first 3 steps; conditional corrections
can be added using qiskit's c_if() for a complete protocol.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def build_teleport_circuit() -> QuantumCircuit:
    """
    Quantum teleportation circuit (measurement stage).

    Qubits:
      - q0: state to be teleported
      - q1: Alice's half of Bell pair
      - q2: Bob's half of Bell pair (will receive the state after corrections)

    Classical bits:
      - c0, c1: measurement results from Alice's Bell measurement
    """
    qc = QuantumCircuit(3, 2)

    # Step 1: Prepare a non-trivial state on q0 (Alice's initial state)
    qc.ry(0.8, 0)

    # Step 2: Create shared Bell pair between q1 and q2
    qc.h(1)
    qc.cx(1, 2)

    # Step 3: Alice's Bell measurement on q0 and q1
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Step 4 (not shown here): Bob would apply conditional X/Z to q2
    # based on the classical outcomes c0, c1, completing the protocol.
    # This requires classical feedback which we simulate via measurement counts.

    return qc


def run_teleport_bridge() -> None:
    """
    Execute the teleportation circuit and display Bell measurement outcomes.

    The counts show the distribution of measurement results from Alice's
    Bell measurement. In a full protocol with conditional corrections,
    Bob's qubit would be projected into the original state.
    """
    print("\n[Quantum State Teleportation]")
    print("Standard protocol (Nielsen & Chuang, Qiskit labs)\n")

    qc = build_teleport_circuit()
    backend = AerSimulator()
    job = backend.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)

    print("Alice's Bell Measurement Outcomes (c[1]c[0]):")
    for bitstring in sorted(counts.keys()):
        count = counts[bitstring]
        prob = 100.0 * count / 1024
        print(f"  {bitstring}: {count:4d} shots ({prob:5.1f}%)")

    print("\nNote: Complete protocol requires Bob to apply")
    print("      classically-controlled X/Z gates to q2")
    print("      based on Alice's measurement results.")

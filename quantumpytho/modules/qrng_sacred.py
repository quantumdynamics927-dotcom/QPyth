from typing import List
from qiskit import QuantumCircuit
from ..engine import QuantumEngine, QuantumResult

PHI = (1 + 5 ** 0.5) / 2  # golden ratio

def build_qrng_circuit(num_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(num_qubits, num_qubits)
    for q in range(num_qubits):
        qc.h(q)
        qc.measure(q, q)
    return qc

def qrng_phi_sequence(
    engine: QuantumEngine,
    num_qubits: int = 8,
    length: int = 16,
) -> List[float]:
    qc = build_qrng_circuit(num_qubits)
    result: QuantumResult = engine.run(qc, label="qrng_phi")

    bitstrings = list(result.counts.keys())
    probs = [result.counts[b] / result.meta["shots"] for b in bitstrings]

    sequence: List[float] = []
    for i in range(min(length, len(bitstrings))):
        val = (probs[i] * PHI) % PHI
        sequence.append(val)
    return sequence

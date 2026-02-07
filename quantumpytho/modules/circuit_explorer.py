from qiskit import QuantumCircuit
from ..engine import QuantumEngine, QuantumResult

def bell_pair(engine: QuantumEngine) -> QuantumResult:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return engine.run(qc, label="bell_pair")

def hadamard_sweep(engine: QuantumEngine, depth: int = 3) -> QuantumResult:
    qc = QuantumCircuit(1, 1)
    for _ in range(depth):
        qc.h(0)
    qc.measure(0, 0)
    return engine.run(qc, label=f"h_sweep_{depth}")

from dataclasses import dataclass
from typing import Dict, Any

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from .config import QuantumConfig

@dataclass
class QuantumResult:
    circuit: QuantumCircuit
    counts: Dict[str, int]
    meta: Dict[str, Any]

class QuantumEngine:
    """
    Thin abstraction around Qiskit backends so modules
    don't have to care about simulator vs hardware.
    """

    def __init__(self, config: QuantumConfig | None = None):
        self.config = config or QuantumConfig()
        self._backend = AerSimulator(method=self.config.backend_name)

    def run(self, circuit: QuantumCircuit, label: str = "") -> QuantumResult:
        job = self._backend.run(circuit, shots=self.config.shots)
        result = job.result()
        counts = result.get_counts(circuit)
        return QuantumResult(
            circuit=circuit,
            counts=counts,
            meta={
                "label": label,
                "shots": self.config.shots,
                "backend": self.config.backend_name,
            },
        )

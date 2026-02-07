from dataclasses import dataclass

@dataclass
class QuantumConfig:
    backend_name: str = "automatic"
    shots: int = 1024

# QuantumPytho

[![CI](https://github.com/quantumdynamics927-dotcom/QPyth/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumdynamics927-dotcom/QPyth/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

QuantumPytho is a physically rigorous, modular quantum Python application built on Qiskit. Every quantum and mathematical element follows canonical textbook definitions and standard implementations. No fabricated “demo” energies—only real simulation or graceful dependency checks.

## Highlights

- **Bloch Sphere State Projection**: Exact statevectors using the standard parametrization $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$. Born-rule probabilities computed directly from the normalized statevector.
- **Sacred-Geometry QRNG**: Quantum random generation with Hadamards and golden-ratio scaling.
- **Circuit Explorer**: Bell pairs and Hadamard sweeps with measurement statistics.
- **Teleportation Protocol**: Standard quantum teleportation flow (Nielsen & Chuang, Qiskit labs), with explicit notes on conditional corrections.
- **H₂ VQE**:
  - **Physical Mode** (requires `qiskit-nature`, `qiskit-algorithms`): Runs real VQE from a molecular Hamiltonian via PySCF and standard mapping/ansatz.
  - **Generic Optimizer** (fallback): A mathematically sound 1D coordinate descent that is physics-agnostic unless a physical cost is supplied.
- **Decoherence Toggle**: Logical toggle ready for Aer noise models or IBM Runtime.

## Install

```bash
pip install -e .
```

Enable physical H₂ VQE:

```bash
pip install qiskit-algorithms qiskit-nature
```

## Run

```bash
qpy
```

Alternate (no PATH needed):

```bash
python -m quantumpytho
```

## Project Structure

- **bloch_ascii.py**: Statevector → Born probabilities → ASCII projection.
- **qrng_sacred.py**: Hadamard QRNG with Φ-scaling.
- **circuit_explorer.py**: Bell and Hadamard circuits.
- **vqe_h2_ascii.py**: Generic 1D optimizer framework.
- **vqe_h2_exact.py**: Physical H₂ VQE via Qiskit-Nature.
- **vqe_h2_cli.py**: CLI wrapper for VQE (physical first, no fake energies).
- **teleport_bridge.py**: Standard teleportation protocol.
- **decoherence_toggle.py**: Future noise-model integration hook.

## Scientific Correctness

- **No fabricated physics**: Either runs real Qiskit simulation/optimization or reports missing dependencies.
- **Canonical parametrizations**: Bloch sphere angles follow textbook definitions.
- **Textbook circuits**: Bell pairs, Hadamard sweeps, teleportation match references.
- **Proper VQE stack**: PySCF → mapper → VQE when `qiskit-nature` is available.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions are welcome.

## License

MIT. See [LICENSE](LICENSE).


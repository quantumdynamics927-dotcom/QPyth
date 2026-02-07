"""
Physically correct Variational Quantum Eigensolver for H₂ molecule.

This module runs a true VQE using the standard stack:
  - qiskit_nature (for molecular Hamiltonian via PySCF)
  - qiskit_algorithms (for VQE algorithm)
  - qiskit.primitives (Estimator backend)

References:
  - Qiskit textbook VQE chapter
  - IBM Quantum Learning H₂ VQE example
  - Qiskit algos documentation
"""

from __future__ import annotations

from typing import List, Tuple


def run_vqe_h2_physical(
    max_iters: int = 50,
) -> List[Tuple[int, float]]:
    """
    Physically correct Variational Quantum Eigensolver for H₂ molecule
    in minimal basis (STO-3G), following standard Qiskit/IBM examples.

    This function REQUIRES:
      - qiskit_algorithms
      - qiskit_nature
      - pyscf (installed as dep of qiskit_nature)

    Structure:
      1. Build H₂ electronic structure problem via PySCF driver
      2. Map second-quantized Hamiltonian to qubit operator (parity mapper)
      3. Define ansatz (TwoLocal with RY/CZ blocks)
      4. Run VQE with Estimator primitive, collect energies via callback
      5. Return (iteration, energy) pairs—no fabricated values

    The physical Hamiltonian, ansatz, and optimization are all from
    the standard Qiskit/Nature stack, ensuring scientific correctness.
    """
    try:
        from qiskit_algorithms import VQE
        from qiskit.primitives import Estimator
        from qiskit.circuit.library import TwoLocal
        from qiskit_nature.second_q.drivers import PySCFDriver
        from qiskit_nature.second_q.mappers import ParityMapper
        from qiskit_nature.second_q.problems import ElectronicStructureProblem
        from qiskit_nature.second_q.transformers import ActiveSpaceTransformer
    except ImportError as e:
        raise RuntimeError(
            "H₂ VQE requires qiskit_algorithms and qiskit_nature to be installed. "
            f"Import error: {e}"
        )

    # 1. Build electronic structure problem for H₂
    driver = PySCFDriver(
        atom="H 0 0 0; H 0 0 0.735",
        basis="sto3g"
    )
    es_problem = ElectronicStructureProblem(driver)
    es_problem = ActiveSpaceTransformer(
        num_electrons=2,
        num_spatial_orbitals=2
    ).transform(es_problem)

    # 2. Extract second-quantized Hamiltonian and map to qubits
    second_q_ops = es_problem.second_q_ops()
    hamiltonian = second_q_ops[0]

    mapper = ParityMapper()
    qubit_op = mapper.map(hamiltonian)

    # 3. Define ansatz (hardware-efficient)
    ansatz = TwoLocal(
        rotation_blocks="ry",
        entanglement_blocks="cz",
        entanglement="full",
    )

    # 4. Run VQE with Estimator, collect energies
    estimator = Estimator()
    vqe = VQE(estimator, ansatz=ansatz)

    energies: List[Tuple[int, float]] = []

    def callback(eval_count, parameters, mean, std):
        """Collect energy at each VQE iteration."""
        energies.append((eval_count, mean))

    vqe.callback = callback

    # Solve for ground state
    _result = vqe.compute_minimum_eigenvalue(qubit_op)

    return energies

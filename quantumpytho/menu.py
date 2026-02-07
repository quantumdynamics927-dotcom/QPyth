from .config import QuantumConfig
from .engine import QuantumEngine
from .modules.bloch_ascii import run_bloch_ascii
from .modules.circuit_explorer import bell_pair, hadamard_sweep
from .modules.decoherence_toggle import DecoherenceController
from .modules.qrng_sacred import qrng_phi_sequence
from .modules.teleport_bridge import run_teleport_bridge
from .modules.vqe_h2_cli import run_vqe_h2_cli


def print_menu(deco_on: bool) -> None:
    deco_label = "ON" if deco_on else "OFF"
    print("\n=== QuantumPytho App ===")
    print("1) Sacred-geometry QRNG sequence")
    print("2) Circuit explorer (Bell pair)")
    print("3) Circuit explorer (Hadamard sweep)")
    print("4) TMT-OS style experiment (reserved hook)")
    print("5) Bloch State Vector Projection (ASCII)")
    print("6) Non-local Teleportation Bridge")
    print("7) Molecular Ground-State (VQE Sim)")
    print(f"8) Toggle Quantum Decoherence [{deco_label}]")
    print("q) Quit")


def run_app() -> None:
    cfg = QuantumConfig()
    engine = QuantumEngine(cfg)
    deco_ctrl = DecoherenceController()

    while True:
        print_menu(deco_ctrl.enabled)
        choice = input("Select option: ").strip().lower()

        if choice == "q":
            print("Goodbye from QuantumPytho.")
            break

        elif choice == "1":
            seq = qrng_phi_sequence(engine, num_qubits=8, length=16)
            print("\nQRNG φ-sequence:")
            for i, v in enumerate(seq):
                print(f"{i:02d}: {v:.6f}")

        elif choice == "2":
            res = bell_pair(engine)
            print("\nBell pair counts:", res.counts)

        elif choice == "3":
            depth_str = input("Depth (e.g. 3, 5, 7): ").strip() or "3"
            depth = int(depth_str)
            res = hadamard_sweep(engine, depth=depth)
            print(f"\nH-sweep (depth={depth}) counts:", res.counts)

        elif choice == "4":
            print("\n[TMT-OS style experiment]")
            print("Reserved: plug in your TMT-OS circuit builder here.")

        elif choice == "5":
            theta = float(input("Theta (0 to pi) [1.0]: ").strip() or "1.0")
            phi = float(input("Phi (0 to 2pi) [1.0]: ").strip() or "1.0")
            run_bloch_ascii(theta, phi)

        elif choice == "6":
            run_teleport_bridge()

        elif choice == "7":
            run_vqe_h2_cli()

        elif choice == "8":
            deco_ctrl.toggle()

        else:
            print("Unknown option.")

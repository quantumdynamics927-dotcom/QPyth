"""
FastAPI server wrapping QuantumPytho modules for web UI.
Provides REST API endpoints for all quantum features.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from quantumpytho.config import QuantumConfig
from quantumpytho.engine import QuantumEngine
from quantumpytho.modules.bloch_ascii import one_qubit_from_angles
from quantumpytho.modules.qrng_sacred import qrng_phi_sequence
from quantumpytho.modules.circuit_explorer import bell_pair, hadamard_sweep
from quantumpytho.modules.teleport_bridge import build_teleport_circuit

app = FastAPI(
    title="QuantumPytho API",
    description="REST API for quantum computing education modules",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize quantum engine
engine = QuantumEngine(QuantumConfig())


class BlochRequest(BaseModel):
    theta: float
    phi: float
    shots: int = 1024


class HadamardRequest(BaseModel):
    depth: int = 3


@app.get("/")
def root():
    return {
        "name": "QuantumPytho API",
        "version": "0.1.0",
        "endpoints": [
            "/bloch",
            "/qrng",
            "/bell",
            "/hadamard",
            "/teleport",
            "/vqe_h2"
        ]
    }


@app.post("/bloch")
def bloch_endpoint(req: BlochRequest):
    """
    Compute Bloch sphere state vector and probabilities.
    
    Returns exact Born-rule probabilities from the canonical parametrization:
    |ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩
    """
    try:
        sv = one_qubit_from_angles(req.theta, req.phi)
        probs = sv.probabilities().tolist()
        
        # Convert statevector to serializable format
        sv_data = [[c.real, c.imag] for c in sv.data]
        
        return {
            "statevector": sv_data,
            "probabilities": probs,
            "shots": req.shots,
            "theta": req.theta,
            "phi": req.phi,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/qrng")
def qrng_endpoint(num_qubits: int = 8, length: int = 16):
    """
    Generate sacred-geometry QRNG sequence with golden ratio scaling.
    """
    try:
        seq = qrng_phi_sequence(engine, num_qubits=num_qubits, length=length)
        return {
            "sequence": seq,
            "num_qubits": num_qubits,
            "length": length
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bell")
def bell_endpoint():
    """
    Run Bell pair circuit and return measurement statistics.
    """
    try:
        res = bell_pair(engine)
        return {
            "counts": res.counts,
            "circuit": res.circuit.draw("text").__str__(),
            "shots": res.meta["shots"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hadamard")
def hadamard_endpoint(req: HadamardRequest):
    """
    Run Hadamard sweep circuit with specified depth.
    """
    try:
        res = hadamard_sweep(engine, depth=req.depth)
        return {
            "counts": res.counts,
            "depth": req.depth,
            "circuit": res.circuit.draw("text").__str__(),
            "shots": res.meta["shots"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/teleport")
def teleport_endpoint():
    """
    Build quantum teleportation circuit (Nielsen & Chuang protocol).
    """
    try:
        qc = build_teleport_circuit()
        return {
            "circuit": qc.draw("text").__str__(),
            "description": "Standard quantum teleportation protocol"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vqe_h2")
def vqe_h2_endpoint():
    """
    Run physically correct H₂ VQE simulation.
    
    Returns convergence trace if qiskit-nature/qiskit-algorithms are installed.
    No fabricated energies—either real simulation or graceful error.
    """
    try:
        from quantumpytho.modules.vqe_h2_exact import run_vqe_h2_physical
        
        history = run_vqe_h2_physical()
        energies = [{"iteration": i, "energy": float(E)} for i, E in history]
        
        return {
            "energies": energies,
            "molecule": "H₂",
            "basis": "STO-3G"
        }
    except RuntimeError as e:
        return {
            "error": str(e),
            "install_command": "pip install qiskit-algorithms qiskit-nature"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

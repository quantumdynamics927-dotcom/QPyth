# QuantumPytho Web UI

Interactive web interface for QuantumPytho quantum computing modules.

## Quick Start

### Backend (FastAPI)

```bash
# From project root
pip install -e .[web]
python server.py
```

Backend runs at `http://localhost:8000`

### Frontend (React + Vite)

```bash
cd web
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`

## Features

- **Bloch Sphere**: Interactive sliders for θ and φ with real-time probability visualization
- **Quantum Circuits**: Bell pairs, Hadamard sweeps, teleportation protocol
- **VQE H₂**: Real molecular ground-state simulation with energy convergence plots
- **QRNG**: Sacred-geometry quantum random number generation with φ-scaling

## Development

```bash
npm run build   # Production build
npm run preview # Preview production build
```

## API Endpoints

- `POST /bloch` - Bloch sphere state computation
- `GET /qrng` - Quantum RNG sequence
- `GET /bell` - Bell pair circuit
- `POST /hadamard` - Hadamard sweep
- `GET /teleport` - Teleportation circuit
- `GET /vqe_h2` - H₂ VQE simulation

## Tech Stack

- **Backend**: FastAPI, Qiskit, NumPy
- **Frontend**: React 18, TypeScript, Vite, Recharts
- **Styling**: Custom CSS with quantum-themed dark mode

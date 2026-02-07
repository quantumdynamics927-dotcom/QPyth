import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function VQEView() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  const runVQE = async () => {
    setLoading(true)
    setError('')
    setResult(null)
    
    try {
      const res = await fetch('/vqe_h2')
      const data = await res.json()
      
      if (data.error) {
        setError(data.error)
      } else {
        setResult(data)
      }
    } catch (error) {
      console.error('Error:', error)
      setError('Failed to connect to backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="module">
      <h2>Variational Quantum Eigensolver (VQE) for H₂</h2>
      
      <div className="info">
        <strong>Physical VQE Simulation</strong>
        <br />
        Uses PySCF molecular Hamiltonian, parity mapping, and TwoLocal ansatz.
        Finds ground state energy of H₂ molecule in STO-3G basis.
        <br /><br />
        <strong>Requirements:</strong> qiskit-algorithms, qiskit-nature
      </div>

      <button onClick={runVQE} disabled={loading}>
        {loading ? 'Running VQE...' : 'Run H₂ VQE'}
      </button>

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
          <br /><br />
          <code>pip install qiskit-algorithms qiskit-nature</code>
        </div>
      )}

      {result && (
        <div className="result">
          <h3>Energy Convergence</h3>
          <p style={{ marginBottom: '16px', color: '#aaa' }}>
            Molecule: {result.molecule} | Basis: {result.basis}
          </p>
          
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={result.energies}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2f4a" />
              <XAxis 
                dataKey="iteration" 
                label={{ value: 'VQE Iteration', position: 'insideBottom', offset: -5 }}
                stroke="#888"
              />
              <YAxis 
                label={{ value: 'Energy (Hartree)', angle: -90, position: 'insideLeft' }}
                stroke="#888"
              />
              <Tooltip 
                contentStyle={{ background: '#1a1f3a', border: '1px solid #2a2f4a' }}
                labelStyle={{ color: '#e8e8e8' }}
              />
              <Line 
                type="monotone" 
                dataKey="energy" 
                stroke="#4a90e2" 
                strokeWidth={2}
                dot={{ fill: '#4a90e2', r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>

          <div style={{ marginTop: '16px', padding: '12px', background: '#0f1424', borderRadius: '6px' }}>
            <strong>Ground State Energy:</strong>{' '}
            {result.energies[result.energies.length - 1]?.energy.toFixed(6)} Hartree
          </div>
        </div>
      )}

      <div style={{ marginTop: '24px', padding: '16px', background: '#0f1424', borderRadius: '6px', fontSize: '14px' }}>
        <h3>About VQE</h3>
        <p style={{ lineHeight: '1.6', color: '#aaa' }}>
          VQE is a hybrid quantum-classical algorithm for finding molecular ground states.
          The quantum computer prepares trial states, while a classical optimizer adjusts
          parameters to minimize energy. This is one of the most promising near-term quantum algorithms
          for quantum chemistry applications.
        </p>
      </div>
    </div>
  )
}

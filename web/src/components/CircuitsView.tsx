import { useState } from 'react'

export default function CircuitsView() {
  const [bellResult, setBellResult] = useState<any>(null)
  const [hadamardResult, setHadamardResult] = useState<any>(null)
  const [teleportResult, setTeleportResult] = useState<any>(null)
  const [hadamardDepth, setHadamardDepth] = useState(3)
  const [loading, setLoading] = useState('')

  const runBell = async () => {
    setLoading('bell')
    try {
      const res = await fetch('/bell')
      const data = await res.json()
      setBellResult(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading('')
    }
  }

  const runHadamard = async () => {
    setLoading('hadamard')
    try {
      const res = await fetch('/hadamard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ depth: hadamardDepth }),
      })
      const data = await res.json()
      setHadamardResult(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading('')
    }
  }

  const runTeleport = async () => {
    setLoading('teleport')
    try {
      const res = await fetch('/teleport')
      const data = await res.json()
      setTeleportResult(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading('')
    }
  }

  return (
    <div>
      {/* Bell Pair */}
      <div className="module">
        <h2>Bell Pair Entanglement</h2>
        <div className="info">
          Creates maximally entangled state: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        </div>
        <button onClick={runBell} disabled={loading === 'bell'}>
          {loading === 'bell' ? 'Running...' : 'Run Bell Circuit'}
        </button>
        
        {bellResult && (
          <div className="result">
            <h3>Measurement Counts</h3>
            <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
              {Object.entries(bellResult.counts).map(([state, count]) => (
                <div key={state} style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{count as number}</div>
                  <div style={{ fontSize: '14px', color: '#888' }}>|{state}⟩</div>
                </div>
              ))}
            </div>
            <pre>{bellResult.circuit}</pre>
          </div>
        )}
      </div>

      {/* Hadamard Sweep */}
      <div className="module">
        <h2>Hadamard Sweep</h2>
        <div className="info">
          Apply repeated Hadamard gates. Depth controls number of H gates.
        </div>
        <label>
          <strong>Depth</strong>: {hadamardDepth}
          <input
            type="range"
            min="1"
            max="10"
            step="1"
            value={hadamardDepth}
            onChange={(e) => setHadamardDepth(parseInt(e.target.value))}
          />
        </label>
        <button onClick={runHadamard} disabled={loading === 'hadamard'}>
          {loading === 'hadamard' ? 'Running...' : 'Run Hadamard Sweep'}
        </button>

        {hadamardResult && (
          <div className="result">
            <h3>Measurement Counts (Depth: {hadamardResult.depth})</h3>
            <div style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
              {Object.entries(hadamardResult.counts).map(([state, count]) => (
                <div key={state} style={{ flex: 1, textAlign: 'center' }}>
                  <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{count as number}</div>
                  <div style={{ fontSize: '14px', color: '#888' }}>|{state}⟩</div>
                </div>
              ))}
            </div>
            <pre>{hadamardResult.circuit}</pre>
          </div>
        )}
      </div>

      {/* Teleportation */}
      <div className="module">
        <h2>Quantum Teleportation</h2>
        <div className="info">
          Standard protocol (Nielsen & Chuang). Alice's Bell measurement enables Bob to reconstruct
          the unknown quantum state via classically-controlled gates.
        </div>
        <button onClick={runTeleport} disabled={loading === 'teleport'}>
          {loading === 'teleport' ? 'Building...' : 'Show Teleportation Circuit'}
        </button>

        {teleportResult && (
          <div className="result">
            <h3>Circuit Structure</h3>
            <pre>{teleportResult.circuit}</pre>
            <p style={{ fontSize: '14px', color: '#aaa', marginTop: '12px' }}>
              Complete protocol requires conditional X/Z gates on Bob's qubit based on Alice's measurement.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

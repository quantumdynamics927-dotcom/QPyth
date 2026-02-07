import { useState } from 'react'

export default function QRNGView() {
  const [numQubits, setNumQubits] = useState(8)
  const [length, setLength] = useState(16)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const runQRNG = async () => {
    setLoading(true)
    try {
      const res = await fetch(`/qrng?num_qubits=${numQubits}&length=${length}`)
      const data = await res.json()
      setResult(data)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="module">
      <h2>Sacred-Geometry Quantum RNG</h2>
      
      <div className="info">
        <strong>Golden Ratio Mapping</strong>
        <br />
        Generates quantum random numbers using Hadamard gates, then scales outputs
        by the golden ratio φ = (1+√5)/2 ≈ 1.618 for sacred geometry applications.
      </div>

      <label>
        <strong>Number of Qubits</strong>: {numQubits}
        <input
          type="range"
          min="4"
          max="12"
          step="1"
          value={numQubits}
          onChange={(e) => setNumQubits(parseInt(e.target.value))}
        />
      </label>

      <label>
        <strong>Sequence Length</strong>: {length}
        <input
          type="range"
          min="8"
          max="32"
          step="1"
          value={length}
          onChange={(e) => setLength(parseInt(e.target.value))}
        />
      </label>

      <button onClick={runQRNG} disabled={loading}>
        {loading ? 'Generating...' : 'Generate QRNG Sequence'}
      </button>

      {result && (
        <div className="result">
          <h3>φ-Scaled Random Sequence</h3>
          <p style={{ marginBottom: '12px', color: '#aaa' }}>
            {result.num_qubits} qubits, {result.length} values
          </p>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(120px, 1fr))',
            gap: '8px',
            marginTop: '12px'
          }}>
            {result.sequence.map((val: number, idx: number) => (
              <div
                key={idx}
                style={{
                  background: '#0f1424',
                  padding: '12px',
                  borderRadius: '6px',
                  textAlign: 'center'
                }}
              >
                <div style={{ fontSize: '12px', color: '#888', marginBottom: '4px' }}>
                  {idx}
                </div>
                <div style={{ fontSize: '16px', fontWeight: 'bold', fontFamily: 'monospace' }}>
                  {val.toFixed(4)}
                </div>
              </div>
            ))}
          </div>

          <div style={{ marginTop: '16px', padding: '12px', background: '#0f1424', borderRadius: '6px' }}>
            <strong>Statistics:</strong>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px', marginTop: '8px' }}>
              <div>
                <div style={{ fontSize: '12px', color: '#888' }}>Mean</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  {(result.sequence.reduce((a: number, b: number) => a + b, 0) / result.sequence.length).toFixed(4)}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '12px', color: '#888' }}>Min</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  {Math.min(...result.sequence).toFixed(4)}
                </div>
              </div>
              <div>
                <div style={{ fontSize: '12px', color: '#888' }}>Max</div>
                <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                  {Math.max(...result.sequence).toFixed(4)}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div style={{ marginTop: '24px', padding: '16px', background: '#0f1424', borderRadius: '6px', fontSize: '14px' }}>
        <h3>About QRNG</h3>
        <p style={{ lineHeight: '1.6', color: '#aaa' }}>
          Quantum Random Number Generation (QRNG) exploits quantum superposition to create
          truly random numbers, unlike classical pseudo-random generators. This implementation
          adds sacred geometry scaling using the golden ratio, creating sequences with harmonic properties.
        </p>
      </div>
    </div>
  )
}

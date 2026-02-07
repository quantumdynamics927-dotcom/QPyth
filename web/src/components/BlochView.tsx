import { useState } from 'react'

export default function BlochView() {
  const [theta, setTheta] = useState(1.0)
  const [phi, setPhi] = useState(1.0)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const runBloch = async () => {
    setLoading(true)
    try {
      const res = await fetch('/bloch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theta, phi, shots: 1024 }),
      })
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
      <h2>Bloch Sphere State Projection</h2>
      
      <div className="info">
        <strong>Theory:</strong> Any single-qubit pure state can be represented as:
        <br />
        <code>|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ) sin(θ/2)|1⟩</code>
        <br />
        with θ ∈ [0, π] and φ ∈ [0, 2π]
      </div>

      <label>
        <strong>Theta (θ)</strong>: {theta.toFixed(3)} rad
        <input
          type="range"
          min="0"
          max={Math.PI}
          step="0.01"
          value={theta}
          onChange={(e) => setTheta(parseFloat(e.target.value))}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#888' }}>
          <span>0</span>
          <span>π/2</span>
          <span>π</span>
        </div>
      </label>

      <label>
        <strong>Phi (φ)</strong>: {phi.toFixed(3)} rad
        <input
          type="range"
          min="0"
          max={2 * Math.PI}
          step="0.01"
          value={phi}
          onChange={(e) => setPhi(parseFloat(e.target.value))}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#888' }}>
          <span>0</span>
          <span>π</span>
          <span>2π</span>
        </div>
      </label>

      <button onClick={runBloch} disabled={loading}>
        {loading ? 'Computing...' : 'Run Simulation'}
      </button>

      {result && (
        <div className="result">
          <h3>Born Rule Probabilities</h3>
          <div className="bar-chart" style={{ height: '200px' }}>
            <div className="bar" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'flex-end' }}>
              <div
                className="bar-fill"
                style={{
                  height: `${result.probabilities[0] * 100}%`,
                  position: 'relative',
                }}
              >
                <div className="bar-label" style={{ position: 'absolute', top: '-24px', width: '100%' }}>
                  |0⟩: {(result.probabilities[0] * 100).toFixed(2)}%
                </div>
              </div>
            </div>
            <div className="bar" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'flex-end' }}>
              <div
                className="bar-fill"
                style={{
                  height: `${result.probabilities[1] * 100}%`,
                  position: 'relative',
                }}
              >
                <div className="bar-label" style={{ position: 'absolute', top: '-24px', width: '100%' }}>
                  |1⟩: {(result.probabilities[1] * 100).toFixed(2)}%
                </div>
              </div>
            </div>
          </div>
          <p style={{ marginTop: '48px', fontSize: '14px', color: '#aaa' }}>
            Approximate shots: ~{Math.round(result.probabilities[0] * 1024)} for |0⟩, 
            ~{Math.round(result.probabilities[1] * 1024)} for |1⟩
          </p>
        </div>
      )}

      <div style={{ marginTop: '24px', padding: '16px', background: '#0f1424', borderRadius: '6px' }}>
        <h3>Presets</h3>
        <div style={{ display: 'flex', gap: '8px', marginTop: '12px', flexWrap: 'wrap' }}>
          <button onClick={() => { setTheta(0); setPhi(0); }}>|0⟩</button>
          <button onClick={() => { setTheta(Math.PI); setPhi(0); }}>|1⟩</button>
          <button onClick={() => { setTheta(Math.PI / 2); setPhi(0); }}>|+⟩</button>
          <button onClick={() => { setTheta(Math.PI / 2); setPhi(Math.PI); }}>|−⟩</button>
          <button onClick={() => { setTheta(Math.PI / 2); setPhi(Math.PI / 2); }}>|i+⟩</button>
        </div>
      </div>
    </div>
  )
}

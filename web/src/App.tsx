import { useState } from 'react'
import BlochView from './components/BlochView'
import CircuitsView from './components/CircuitsView'
import VQEView from './components/VQEView'
import QRNGView from './components/QRNGView'

type Tab = 'bloch' | 'circuits' | 'vqe' | 'qrng'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('bloch')

  return (
    <>
      <header style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '32px', marginBottom: '8px' }}>
          ⚛️ QuantumPytho
        </h1>
        <p style={{ color: '#888' }}>
          Interactive quantum computing study companion
        </p>
      </header>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'bloch' ? 'active' : ''}`}
          onClick={() => setActiveTab('bloch')}
        >
          Bloch Sphere
        </button>
        <button
          className={`tab ${activeTab === 'circuits' ? 'active' : ''}`}
          onClick={() => setActiveTab('circuits')}
        >
          Circuits
        </button>
        <button
          className={`tab ${activeTab === 'vqe' ? 'active' : ''}`}
          onClick={() => setActiveTab('vqe')}
        >
          VQE H₂
        </button>
        <button
          className={`tab ${activeTab === 'qrng' ? 'active' : ''}`}
          onClick={() => setActiveTab('qrng')}
        >
          QRNG
        </button>
      </div>

      <main>
        {activeTab === 'bloch' && <BlochView />}
        {activeTab === 'circuits' && <CircuitsView />}
        {activeTab === 'vqe' && <VQEView />}
        {activeTab === 'qrng' && <QRNGView />}
      </main>

      <footer style={{ marginTop: '48px', textAlign: 'center', color: '#666', fontSize: '14px' }}>
        <p>
          Open source on{' '}
          <a
            href="https://github.com/quantumdynamics927-dotcom/QPyth"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#4a90e2' }}
          >
            GitHub
          </a>
        </p>
      </footer>
    </>
  )
}

export default App

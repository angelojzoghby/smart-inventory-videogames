import { useState } from 'react'
import { Link, Routes, Route } from 'react-router-dom'
import UploadForm from './components/UploadForm'
import Results from './components/Results'
import InventoryDashboard from './components/InventoryDashboard'
import './App.css'

function Home(){
  const [result, setResult] = useState(null)
  const [message, setMessage] = useState(null)

  return (
    <div className="home-page">
      
      <div className="upload-container">
        <h1 className="title ps-title">Smart Inventory</h1>

        <UploadForm onResult={r => setResult(r)} />
        <Results data={result} onAdded={m => setMessage(m)} />

        {message && <div className="notice ps-notice">{message.status}</div>}
      </div>

      <div className="inventory-side">
        <InventoryDashboard />
      </div>
    </div>
  )
}

export default function App(){
  return (
    <div className="ps-app">
      <nav className="ps-navbar">
        <div className="ps-logo">🎮 Smart Inventory</div>

        <div className="ps-links">
          <Link to="/" className="ps-link">Home</Link>
          <Link to="/inventory" className="ps-link">Inventory</Link>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/inventory" element={<InventoryDashboard/>} />
      </Routes>
    </div>
  )
}

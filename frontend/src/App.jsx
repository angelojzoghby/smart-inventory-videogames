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
    <div className="container">
      <div className="left">
        <h1>Smart Inventory</h1>
        <UploadForm onResult={r => setResult(r)} />
        <Results data={result} onAdded={m => setMessage(m)} />
        {message && <div className="notice">{message.status}</div>}
      </div>
      <div className="right">
        <InventoryDashboard />
      </div>
    </div>
  )
}

export default function App(){
  return (
    <div>
      <nav className="topnav">
        <Link to="/">Home</Link>
        <Link to="/inventory">Inventory</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/inventory" element={<InventoryDashboard/>} />
      </Routes>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { listProducts, updateQuantity, updatePrice, deleteProduct } from '../api/api'
import ProductRow from './ProductRow'
import "../css/inventory.css"

export default function InventoryDashboard() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetch() {
    setLoading(true)
    setError(null)
    try {
      const res = await listProducts()
      if (Array.isArray(res)) {
        setItems(res)
      } else {
        setItems([])
        setError('Unexpected response from server')
      }
    } catch (e) {
      setItems([])
      setError(e?.message || 'Failed to load inventory')
    }
    setLoading(false)
  }

  useEffect(() => { fetch() }, [])

  return (
    <div className="inventory">
      <h2>Inventory</h2>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">{error}</div>}

      <div className="inventory-list">
        {Array.isArray(items) &&
          items.map(i => (
            <ProductRow key={i.product_id} p={i} onRefresh={fetch} />
          ))
        }
      </div>
    </div>
  )
}

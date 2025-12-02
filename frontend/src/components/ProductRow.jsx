import { useState } from 'react'
import { updateQuantity, updatePrice, deleteProduct } from '../api/api'
import "../css/productRow.css"

function ProductRow({ p, onRefresh }) {
  const [quantity, setQuantity] = useState(p.quantity || 0)
  const [price, setPrice] = useState(p.price_modified || p.price_predicted || 0)
  const [updatingQ, setUpdatingQ] = useState(false)
  const [updatingP, setUpdatingP] = useState(false)

  async function saveQuantity() {
    setUpdatingQ(true)
    await updateQuantity({ product_id: p.product_id, quantity: parseInt(quantity || 0) })
    setUpdatingQ(false)
    onRefresh()
  }

  async function savePrice() {
    setUpdatingP(true)
    await updatePrice({ product_id: p.product_id, price_modified: parseFloat(price) })
    setUpdatingP(false)
    onRefresh()
  }

  async function remove() {
    await deleteProduct(p.product_id)
    onRefresh()
  }

  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const placeholder = `data:image/svg+xml;utf8,${encodeURIComponent(
    `<svg xmlns='http://www.w3.org/2000/svg' width='90' height='90'>
      <rect width='100%' height='100%' fill='%23e8e8e8'/>
      <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' 
        font-size='14' fill='%23666'>No Image</text></svg>`
  )}`

  const imgSrc = p.image_id ? `${baseUrl}/image/${p.image_id}` : placeholder

  return (
    <div className="product-row">
      <div className="p-thumb">
        <img src={imgSrc} alt={p.product_name || "product"} />
      </div>

      <div className="p-info">
        <div className="p-name">{p.product_name || "Unnamed Product"}</div>
        <div className="p-type">{p.product_type || "Unknown"}</div>
      </div>

      <div className="p-actions">
        <input
          value={price}
          onChange={e => setPrice(e.target.value)}
        />
        <button onClick={savePrice} disabled={updatingP}>
          {updatingP ? "..." : "Save Price"}
        </button>

        <input
          type="number"
          value={quantity}
          onChange={e => setQuantity(e.target.value)}
        />
        <button onClick={saveQuantity} disabled={updatingQ}>
          {updatingQ ? "..." : "Save Qty"}
        </button>

        <button onClick={remove}>Delete</button>
      </div>
    </div>
  )
}

export default ProductRow

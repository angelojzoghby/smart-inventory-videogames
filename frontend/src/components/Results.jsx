import { useState } from 'react'
import { addProduct } from '../api/api'

export default function Results({data, onAdded}){
  const [price, setPrice] = useState(data?.price_predicted || 0)
  const [quantity, setQuantity] = useState(1)
  const [saving, setSaving] = useState(false)

  async function handleAdd(){
    setSaving(true)
    const payload = {
      product_name: data.product_name,
      product_type: data.product_type,
      price_predicted: data.price_predicted,
      price_modified: parseFloat(price),
      quantity: parseInt(quantity || 0),
      image_id: data.image_id
    }
    const res = await addProduct(payload)
    setSaving(false)
    onAdded(res)
  }

  if(!data) return null

  return (
    <div className="results">
      <div className="result-row">
        <div className="result-image">
          <img src={`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/image/${data.image_id}`} alt="uploaded" />
        </div>
        <div className="result-meta">
          <h3>{data.product_name}</h3>
          <p>{data.product_type}</p>
          <label>Predicted price</label>
          <input value={price} onChange={e => setPrice(e.target.value)} />
          <label>Quantity</label>
          <input type="number" value={quantity} onChange={e => setQuantity(e.target.value)} />
          <button onClick={handleAdd} disabled={saving}>{saving ? 'Saving...' : 'Add to Inventory'}</button>
        </div>
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { addProduct, findProduct, updateQuantity } from '../api/api'
import "../css/results.css"

export default function Results({ data, onAdded }) {
  const [price, setPrice] = useState(data?.price_predicted || 0)
  const [quantity, setQuantity] = useState(1)
  const [saving, setSaving] = useState(false)
  const [mode, setMode] = useState('loading')
  const [existing, setExisting] = useState(null)
  const [addingQty, setAddingQty] = useState(1)

  useEffect(() => {
    setPrice(data?.price_predicted || 0)
    setQuantity(1)
    setExisting(null)
    if (!data) return

    async function check() {
      if (data.exists && data.product) {
        setExisting(data.product)
        setMode('exists')
        return
      }
      try {
        const res = await findProduct({ product_name: data.product_name, product_type: data.product_type })
        if (res?.found) {
          setExisting(res.product)
          setMode('exists')
        } else {
          setMode('new')
        }
      } catch {
        setMode('new')
      }
    }

    check()
  }, [data])

  async function handleCreate() {
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

  async function handleAddQuantity() {
    if (!existing) return
    setSaving(true)
    const newQty = (existing.quantity || 0) + parseInt(addingQty || 0)
    await updateQuantity({ product_id: existing.product_id, quantity: newQty })
    setSaving(false)
    onAdded({ status: 'quantity updated', product_id: existing.product_id })
  }

  if (!data) return null

  return (
    <div className="results">
      <div className="result-row">
        <div className="result-image">
          <img
            src={`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/image/${data.image_id}`}
            alt="uploaded"
          />
        </div>

        <div className="result-meta">
          <h3>{data.product_name}</h3>
          <p>{data.product_type}</p>

          <label>Predicted Price</label>
          <input value={price} onChange={e => setPrice(e.target.value)} />

          {mode === 'loading' && <div>Checking inventory...</div>}

          {mode === 'exists' && existing && (
            <div>
              <div style={{ marginBottom: 8 }}>Existing product found</div>
              <div>Current quantity: {existing.quantity || 0}</div>

              <label>Add quantity</label>
              <input
                type="number"
                value={addingQty}
                onChange={e => setAddingQty(e.target.value)}
              />
              <button onClick={handleAddQuantity} disabled={saving}>
                {saving ? 'Updating...' : 'Add Quantity'}
              </button>

              <div style={{ marginTop: 10 }}>Or add as new product instead:</div>
              <button onClick={() => setMode('new')}>Create New</button>
            </div>
          )}

          {mode === 'new' && (
            <div>
              <label>Quantity</label>
              <input
                type="number"
                value={quantity}
                onChange={e => setQuantity(e.target.value)}
              />
              <button onClick={handleCreate} disabled={saving}>
                {saving ? 'Saving...' : 'Add to Inventory'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { addProduct, findProduct, updateQuantity } from '../api/api'
import "../css/results.css"

export default function Results({ data, onAdded }) {
  const [title, setTitle] = useState("")
  const [genres, setGenres] = useState([])
  const [dlc, setDlc] = useState(0)
  const [gamepass, setGamepass] = useState(0)
  const [franchise, setFranchise] = useState(0)
  const [discount, setDiscount] = useState(0)
  const [predictedPrice, setPredictedPrice] = useState(null)
  const [confirmed, setConfirmed] = useState(false)
  const [existing, setExisting] = useState(null)
  const [mode, setMode] = useState("loading")
  const [quantity, setQuantity] = useState(0)
  const [addingQty, setAddingQty] = useState(1)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!data) return

    setTitle(data.title || "")
    setGenres(data.genres || [])

    async function check() {
      try {
        const res = await findProduct({
          product_name: data.title,
          product_type: "Game"
        })
        if (res?.found) {
          setExisting(res.product)
          setQuantity(res.product.quantity)
          setMode("exists")
        } else {
          setMode("new")
        }
      } catch {
        setMode("new")
      }
    }
    check()
  }, [data])

  async function handlePredictPrice() {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/predict-price`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        genres,
        dlc,
        gamepass,
        franchise,
        discount
      })
    })
    const result = await res.json()
    setPredictedPrice(result.price_predicted)
    setConfirmed(true)
  }

  async function handleSave() {
    setSaving(true)
    const payload = {
      product_name: title,
      product_type: "Game",
      price_predicted: predictedPrice,
      price_modified: predictedPrice,
      quantity: parseInt(quantity),
      image_id: data.image_id
    }
    const res = await addProduct(payload)
    setSaving(false)
    onAdded(res)
  }


  async function handleAddQuantity() {
    const newQty = existing.quantity + parseInt(addingQty)
    await updateQuantity({
      product_id: existing.product_id,
      quantity: newQty
    })
    onAdded({ status: "quantity updated" })
  }

  if (!data) return null

  return (
    <div className="results">
      <div className="result-row">

        <div className="result-image">
          <img src={`${import.meta.env.VITE_API_BASE_URL}/image/${data.image_id}`} />
        </div>

        <div className="result-meta">
          <h3>Game Details</h3>

          <label>Title</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} />

          <label>Genres</label>
          <input
            value={genres.join(", ")}
            onChange={(e) => setGenres(e.target.value.split(",").map(s => s.trim()))}
          />

          <label>DLC</label>
          <select value={dlc} onChange={(e) => setDlc(Number(e.target.value))}>
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>

          <label>Gamepass</label>
          <select value={gamepass} onChange={(e) => setGamepass(Number(e.target.value))}>
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>

          <label>Franchise</label>
          <select value={franchise} onChange={(e) => setFranchise(Number(e.target.value))}>
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>

          <label>Discount</label>
          <select value={discount} onChange={(e) => setDiscount(Number(e.target.value))}>
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>

          {!confirmed && (
            <button onClick={handlePredictPrice}>Predict Price</button>
          )}

          {confirmed && (
            <>
              <label>Predicted Price</label>
              <input value={predictedPrice} readOnly />

              {mode === "new" && (
                <>
                  <label>Quantity</label>
                  <input
                    type="number"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                  />
                  <button disabled={saving} onClick={handleSave}>
                    {saving ? "Saving..." : "Add to Inventory"}
                  </button>
                </>
              )}

              {mode === "exists" && (
                <>
                  <p>Existing product found</p>
                  <p>Current quantity: {existing.quantity}</p>

                  <label>Add Quantity</label>
                  <input
                    type="number"
                    value={addingQty}
                    onChange={(e) => setAddingQty(e.target.value)}
                  />
                  <button onClick={handleAddQuantity}>Add</button>

                  <button onClick={handleSave}>Add as New</button>
                </>
              )}
            </>
          )}
        </div>

      </div>
    </div>
  )
}

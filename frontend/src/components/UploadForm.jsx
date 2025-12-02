import "../css/uploadForm.css"
import { useState } from 'react'
import { uploadImage } from '../api/api'

export default function UploadForm({ onResult }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [dragActive, setDragActive] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    const res = await uploadImage(file)
    setLoading(false)
    onResult(res)
  }

  function handleFileChange(e) {
    setFile(e.target.files?.[0] || null)
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  return (
    <form onSubmit={handleSubmit} className="ps-upload-form">

      <div
        className={`ps-dropzone ${dragActive ? "drag-active" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true) }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        {!file && <div className="ps-drop-text">🎮 Drag & Drop a Game Cover<br />or Click to Browse</div>}

        {file && (
          <div className="ps-selected-file">
            <strong>Selected:</strong> {file.name}
          </div>
        )}

        <input type="file" accept="image/*" onChange={handleFileChange} />
      </div>

      <button type="submit" className="ps-upload-btn" disabled={loading}>
        {loading ? "Uploading..." : "Upload Image"}
      </button>
    </form>
  )
}

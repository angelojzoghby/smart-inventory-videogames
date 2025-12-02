import { useState } from 'react'
import { uploadImage } from '../api/api'

export default function UploadForm({onResult}){
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e){
    e.preventDefault()
    if(!file) return
    setLoading(true)
    const res = await uploadImage(file)
    setLoading(false)
    onResult(res)
  }

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <input type="file" accept="image/*" onChange={e => setFile(e.target.files?.[0] || null)} />
      <button type="submit" disabled={loading}>
        {loading ? 'Uploading...' : 'Upload Image'}
      </button>
    </form>
  )
}

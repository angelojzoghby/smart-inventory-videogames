const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://127.0.0.1:8000'

async function request(path, options = {}){
  const res = await fetch(`${API_BASE}${path}`, options)
  const contentType = res.headers.get('content-type') || ''
  if(!res.ok){
    if(contentType.includes('application/json')){
      const err = await res.json().catch(() => ({ message: 'Unexpected error' }))
      throw err
    }
    throw { message: `Request failed with status ${res.status}` }
  }
  if(contentType.includes('application/json')){
    return res.json()
  }
  return res
}

export async function uploadImage(file){
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/upload-image`, {
    method: 'POST',
    body: form
  })
  return res.json()
}

export async function addProduct(data){
  return request('/inventory/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
}

export async function listProducts(){
  try{
    const data = await request('/inventory/list')
    return data
  }catch(e){
    return []
  }
}

export async function updateQuantity(payload){
  return request('/inventory/update-quantity', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
}

export async function updatePrice(payload){
  return request('/inventory/update-price', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
}

export async function getProduct(productId){
  return request(`/inventory/${productId}`)
}

export async function deleteProduct(productId){
  return request(`/inventory/delete/${productId}`, {
    method: 'DELETE'
  })
}

export default {
  uploadImage,
  addProduct,
  listProducts,
  updateQuantity,
  updatePrice,
  getProduct,
  deleteProduct
}

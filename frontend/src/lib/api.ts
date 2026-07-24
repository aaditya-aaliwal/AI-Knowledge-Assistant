import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'

import { clearAccessToken, getAccessToken, getRefreshToken, setTokens } from '@/lib/auth-storage'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

if (!API_BASE_URL) {
  throw new Error('VITE_API_BASE_URL must be configured.')
}

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 20000,
  headers: { Accept: 'application/json' },
})

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = getAccessToken()

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const request = error.config as (InternalAxiosRequestConfig & { _retry?: boolean }) | undefined
    const refreshToken = getRefreshToken()
    if (error.response?.status === 401 && request && !request._retry && refreshToken && request.url !== '/auth/refresh') {
      request._retry = true
      try {
        const response = await axios.post<{ access_token: string; refresh_token: string }>(`${API_BASE_URL}/auth/refresh`, { refresh_token: refreshToken }, { timeout: 20000 })
        setTokens(response.data.access_token, response.data.refresh_token)
        request.headers.Authorization = `Bearer ${response.data.access_token}`
        return api(request)
      } catch {
        clearAccessToken()
      }
    }
    if (error.response?.status === 401) window.dispatchEvent(new Event('auth:unauthorized'))
    return Promise.reject(error)
  },
)

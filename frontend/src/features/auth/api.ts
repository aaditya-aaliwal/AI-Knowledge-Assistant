import axios from 'axios'

import { api } from '@/lib/api'
import type { AuthUser, LoginCredentials, LoginResponse } from '@/features/auth/types'

export async function login(credentials: LoginCredentials): Promise<LoginResponse> {
  const formData = new URLSearchParams()
  formData.set('username', credentials.email)
  formData.set('password', credentials.password)

  const response = await api.post<LoginResponse>('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })

  return response.data
}

export async function getCurrentUser(): Promise<AuthUser> {
  const response = await api.get<AuthUser>('/auth/me')
  return response.data
}

export async function register(name: string, credentials: LoginCredentials): Promise<AuthUser> {
  const response = await api.post<AuthUser>('/users', { name, ...credentials })
  return response.data
}

export function getApiErrorMessage(error: unknown) {
  if (axios.isAxiosError<{ detail?: string }>(error)) {
    if (error.code === 'ECONNABORTED') return 'The request took too long. Please try again.'
    if (!error.response) return 'Unable to reach the server. Check your connection and try again.'
    if (error.response.status === 401) return 'Incorrect email or password.'
    if (error.response.status === 409 || error.response.status === 400) return error.response.data.detail ?? 'Please check the details and try again.'
    if (error.response.status >= 500) return 'The service is temporarily unavailable. Please try again shortly.'
    return error.response.data.detail ?? 'Unable to complete the request. Please try again.'
  }

  return 'Unable to complete the request. Please try again.'
}

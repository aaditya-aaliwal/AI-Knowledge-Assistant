import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'

import { AuthContext, type AuthContextValue } from '@/contexts/AuthContext'
import { getApiErrorMessage, getCurrentUser, login as loginRequest, register as registerRequest } from '@/features/auth/api'
import type { AuthUser, LoginCredentials } from '@/features/auth/types'
import { clearAccessToken, getAccessToken, setTokens } from '@/lib/auth-storage'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const logout = useCallback(() => {
    clearAccessToken()
    setUser(null)
    setError(null)
    setIsLoading(false)
  }, [])

  const restoreSession = useCallback(async () => {
    if (!getAccessToken()) {
      setIsLoading(false)
      return
    }

    try {
      setUser(await getCurrentUser())
    } catch {
      clearAccessToken()
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    void restoreSession()
  }, [restoreSession])

  useEffect(() => {
    window.addEventListener('auth:unauthorized', logout)
    return () => window.removeEventListener('auth:unauthorized', logout)
  }, [logout])

  const login = useCallback(async (credentials: LoginCredentials) => {
    setError(null)
    const tokens = await loginRequest(credentials)
    setTokens(tokens.access_token, tokens.refresh_token)

    try {
      setUser(await getCurrentUser())
    } catch (error) {
      clearAccessToken()
      setUser(null)
      setError(getApiErrorMessage(error))
      throw error
    }
  }, [])

  const register = useCallback(async (name: string, credentials: LoginCredentials) => {
    setError(null)
    await registerRequest(name, credentials)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: user !== null,
      isLoading,
      error,
      login,
      register,
      logout,
    }),
    [error, isLoading, login, logout, register, user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

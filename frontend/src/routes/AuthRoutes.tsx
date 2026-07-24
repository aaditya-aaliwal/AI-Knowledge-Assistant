import { Navigate, Outlet, useLocation } from 'react-router-dom'

import { Spinner } from '@/components/ui/feedback'
import { useAuth } from '@/hooks/useAuth'

function AuthLoadingScreen() {
  return (
    <main className="grid min-h-screen place-items-center" aria-label="Restoring your session">
      <Spinner label="Restoring your session" />
    </main>
  )
}

export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) return <AuthLoadingScreen />
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location }} />

  return <Outlet />
}

export function PublicRoute() {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) return <AuthLoadingScreen />
  if (isAuthenticated) return <Navigate to="/app" replace />

  return <Outlet />
}

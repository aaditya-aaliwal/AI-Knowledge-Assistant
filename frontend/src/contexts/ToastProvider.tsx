import { useCallback, useMemo, useState, type ReactNode } from 'react'

import { Toast, ToastViewport } from '@/components/ui/overlays'
import { ToastContext, type ToastInput } from '@/contexts/ToastContext'

type ToastItem = ToastInput & { id: number }

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([])
  const dismiss = useCallback((id: number) => setToasts((items) => items.filter((item) => item.id !== id)), [])
  const showToast = useCallback((toast: ToastInput) => {
    const id = Date.now()
    setToasts((items) => [...items, { ...toast, id }])
    window.setTimeout(() => dismiss(id), 5000)
  }, [dismiss])
  const value = useMemo(() => ({ showToast }), [showToast])
  return <ToastContext.Provider value={value}>{children}<ToastViewport>{toasts.map((toast) => <Toast key={toast.id} title={toast.title} {...(toast.description ? { description: toast.description } : {})} {...(toast.variant ? { variant: toast.variant } : {})} onDismiss={() => dismiss(toast.id)} />)}</ToastViewport></ToastContext.Provider>
}

import { createContext } from 'react'
export type ToastVariant = 'default' | 'destructive' | 'success'
export type ToastInput = { title: string; description?: string; variant?: ToastVariant }
export type ToastContextValue = { showToast: (toast: ToastInput) => void }
export const ToastContext = createContext<ToastContextValue | undefined>(undefined)

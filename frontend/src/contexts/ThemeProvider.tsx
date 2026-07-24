import { useEffect, useMemo, useState } from 'react'

import type { ReactNode } from 'react'
import { ThemeContext, type ResolvedTheme, type Theme, type ThemeContextValue } from '@/contexts/ThemeContext'

interface ThemeProviderProps {
  children: ReactNode
  defaultTheme?: Theme
}

function resolveTheme(theme: Theme): ResolvedTheme {
  if (theme !== 'system') {
    return theme
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export function ThemeProvider({ children, defaultTheme = 'system' }: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(defaultTheme)

  useEffect(() => {
    const root = window.document.documentElement
    const applyTheme = () => {
      root.classList.toggle('dark', resolveTheme(theme) === 'dark')
    }

    applyTheme()

    if (theme !== 'system') {
      return undefined
    }

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', applyTheme)

    return () => mediaQuery.removeEventListener('change', applyTheme)
  }, [theme])

  const value = useMemo<ThemeContextValue>(() => ({ theme, setTheme }), [theme])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

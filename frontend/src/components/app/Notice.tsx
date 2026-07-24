export function Notice({ children, type = 'error' }: { children: string; type?: 'error' | 'success' }) {
  return <p role={type === 'error' ? 'alert' : 'status'} className={type === 'error' ? 'rounded-md bg-destructive/10 p-3 text-sm text-destructive' : 'rounded-md bg-emerald-500/10 p-3 text-sm text-emerald-700 dark:text-emerald-400'}>{children}</p>
}

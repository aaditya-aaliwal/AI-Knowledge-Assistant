import { Circle } from 'lucide-react'
import { type HTMLAttributes, type ReactNode } from 'react'
import { cn } from '@/lib/utils'
export function PageContainer({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn('mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8', className)} {...props} />
  )
}
export function SectionHeader({
  title,
  description,
  action,
  className,
}: {
  title: ReactNode
  description?: ReactNode
  action?: ReactNode
  className?: string
}) {
  return (
    <div className={cn('flex flex-wrap items-start justify-between gap-4', className)}>
      <div>
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{title}</h1>
        {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
      </div>
      {action}
    </div>
  )
}
export function StatusIndicator({
  status,
  label,
  className,
}: {
  status: 'success' | 'warning' | 'danger' | 'neutral'
  label: string
  className?: string
}) {
  const colors = {
    success: 'text-success',
    warning: 'text-warning',
    danger: 'text-destructive',
    neutral: 'text-muted-foreground',
  }
  return (
    <span className={cn('inline-flex items-center gap-1.5 text-sm', className)}>
      <Circle className={cn('size-2 fill-current', colors[status])} aria-hidden="true" />
      {label}
    </span>
  )
}

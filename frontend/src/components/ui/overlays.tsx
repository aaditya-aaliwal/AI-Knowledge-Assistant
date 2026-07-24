import { X } from 'lucide-react'
import {
  useEffect,
  useRef,
  type ButtonHTMLAttributes,
  type HTMLAttributes,
  type ReactNode,
} from 'react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'

type DialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description?: string
  children: ReactNode
  className?: string
}
export function Dialog({
  open,
  onOpenChange,
  title,
  description,
  children,
  className,
}: DialogProps) {
  const ref = useRef<HTMLDialogElement>(null)
  useEffect(() => {
    const dialog = ref.current
    if (!dialog) return
    if (open && !dialog.open) dialog.showModal()
    if (!open && dialog.open) dialog.close()
  }, [open])
  return (
    <dialog
      ref={ref}
      className={cn(
        'm-auto w-[calc(100%-2rem)] max-w-lg rounded-lg border bg-popover p-0 text-popover-foreground shadow-elevated backdrop:bg-foreground/30',
        className,
      )}
      onCancel={(event) => {
        event.preventDefault()
        onOpenChange(false)
      }}
      onClose={() => onOpenChange(false)}
      aria-labelledby="dialog-title"
    >
      <div className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 id="dialog-title" className="text-lg font-semibold">
              {title}
            </h2>
            {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
          </div>
          <button
            className="focus-ring rounded p-1 text-muted-foreground hover:text-foreground"
            onClick={() => onOpenChange(false)}
            aria-label="Close dialog"
          >
            <X className="size-4" />
          </button>
        </div>
        <div className="mt-5">{children}</div>
      </div>
    </dialog>
  )
}
export function Modal(props: DialogProps) {
  return <Dialog {...props} />
}
export function AlertDialog({
  open,
  onOpenChange,
  title,
  description,
  actionLabel = 'Continue',
  onAction,
  children,
}: DialogProps & { actionLabel?: string; onAction: () => void }) {
  return (
    <Dialog
      open={open}
      onOpenChange={onOpenChange}
      title={title}
      {...(description ? { description } : {})}
    >
      <div>
        {children}
        <div className="mt-6 flex justify-end gap-2">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button variant="destructive" onClick={onAction}>
            {actionLabel}
          </Button>
        </div>
      </div>
    </Dialog>
  )
}
export function Popover({
  trigger,
  children,
  className,
}: {
  trigger: ReactNode
  children: ReactNode
  className?: string
}) {
  return (
    <details className={cn('relative inline-block', className)}>
      <summary className="focus-ring cursor-pointer list-none rounded-md">{trigger}</summary>
      <div className="absolute z-50 mt-2 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-elevated">
        {children}
      </div>
    </details>
  )
}
export function Tooltip({ label, children }: { label: string; children: ReactNode }) {
  return (
    <span className="group relative inline-flex">
      {children}
      <span
        role="tooltip"
        className="pointer-events-none absolute bottom-full left-1/2 z-50 mb-2 w-max max-w-48 -translate-x-1/2 rounded bg-foreground px-2 py-1 text-xs text-background opacity-0 transition-opacity group-focus-within:opacity-100 group-hover:opacity-100"
      >
        {label}
      </span>
    </span>
  )
}
export function Toast({
  title,
  description,
  variant = 'default',
  onDismiss,
  className,
}: {
  title: string
  description?: string
  variant?: 'default' | 'destructive' | 'success'
  onDismiss?: () => void
  className?: string
}) {
  const colors = {
    default: 'border',
    destructive: 'border-destructive/40',
    success: 'border-success/40',
  }
  return (
    <div
      role="status"
      className={cn(
        'flex w-full max-w-sm items-start gap-3 rounded-lg border bg-card p-4 shadow-elevated',
        colors[variant],
        className,
      )}
    >
      <div className="flex-1">
        <p className="text-sm font-medium">{title}</p>
        {description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}
      </div>
      {onDismiss && (
        <button
          className="focus-ring rounded p-1 text-muted-foreground hover:text-foreground"
          onClick={onDismiss}
          aria-label="Dismiss notification"
        >
          <X className="size-4" />
        </button>
      )}
    </div>
  )
}
export function ToastViewport({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      className={cn('fixed bottom-4 right-4 z-50 grid gap-3', className)}
      {...props}
    />
  )
}
export function IconButton({ className, ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        'focus-ring inline-flex size-10 items-center justify-center rounded-md hover:bg-accent disabled:opacity-50',
        className,
      )}
      {...props}
    />
  )
}

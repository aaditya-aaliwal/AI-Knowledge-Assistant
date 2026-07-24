import { ChevronDown, ChevronLeft, ChevronRight, MoreHorizontal } from 'lucide-react'
import { useState, type ButtonHTMLAttributes, type HTMLAttributes, type ReactNode } from 'react'
import { cn } from '@/lib/utils'
export function Tabs({
  tabs,
  defaultValue,
  className,
}: {
  tabs: { value: string; label: ReactNode; content: ReactNode; disabled?: boolean }[]
  defaultValue?: string
  className?: string
}) {
  const [active, setActive] = useState(defaultValue ?? tabs[0]?.value ?? '')
  const activeTab = tabs.find((tab) => tab.value === active)
  return (
    <div className={className}>
      <div role="tablist" className="inline-flex h-10 items-center gap-1 rounded-md bg-muted p-1">
        {tabs.map((tab) => (
          <button
            key={tab.value}
            type="button"
            role="tab"
            id={`tab-${tab.value}`}
            aria-selected={active === tab.value}
            aria-controls={`panel-${tab.value}`}
            disabled={tab.disabled}
            className="focus-ring rounded-sm px-3 py-1.5 text-sm font-medium disabled:opacity-50 aria-selected:bg-background aria-selected:shadow-sm"
            onClick={() => setActive(tab.value)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {activeTab && (
        <div
          role="tabpanel"
          id={`panel-${activeTab.value}`}
          aria-labelledby={`tab-${activeTab.value}`}
          className="pt-4"
        >
          {activeTab.content}
        </div>
      )}
    </div>
  )
}
export function Accordion({
  items,
  className,
}: {
  items: { value: string; title: ReactNode; content: ReactNode }[]
  className?: string
}) {
  return (
    <div className={cn('divide-y rounded-md border', className)}>
      {items.map((item) => (
        <details key={item.value} className="group">
          <summary className="focus-ring flex cursor-pointer list-none items-center justify-between p-4 font-medium">
            {item.title}
            <ChevronDown className="size-4 transition-transform group-open:rotate-180" />
          </summary>
          <div className="px-4 pb-4 text-sm text-muted-foreground">{item.content}</div>
        </details>
      ))}
    </div>
  )
}
export function Separator({
  className,
  orientation = 'horizontal',
}: {
  className?: string
  orientation?: 'horizontal' | 'vertical'
}) {
  return (
    <div
      role="separator"
      aria-orientation={orientation}
      className={cn(
        'shrink-0 bg-border',
        orientation === 'horizontal' ? 'h-px w-full' : 'h-full w-px',
        className,
      )}
    />
  )
}
export function ScrollArea({ className, children }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('overflow-auto', className)}>{children}</div>
}
export function Breadcrumb({
  items,
  className,
}: {
  items: { label: ReactNode; href?: string }[]
  className?: string
}) {
  return (
    <nav aria-label="Breadcrumb" className={className}>
      <ol className="flex flex-wrap items-center gap-1.5 text-sm text-muted-foreground">
        {items.map((item, i) => (
          <li key={i} className="flex items-center gap-1.5">
            {i > 0 && <ChevronRight className="size-3.5" aria-hidden="true" />}
            {item.href ? (
              <a className="focus-ring rounded hover:text-foreground" href={item.href}>
                {item.label}
              </a>
            ) : (
              <span aria-current="page" className="text-foreground">
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}
export function Pagination({
  page,
  pageCount,
  onPageChange,
  className,
}: {
  page: number
  pageCount: number
  onPageChange: (page: number) => void
  className?: string
}) {
  return (
    <nav aria-label="Pagination" className={cn('flex items-center gap-2', className)}>
      <button
        className="focus-ring rounded p-2 hover:bg-accent disabled:opacity-50"
        aria-label="Previous page"
        disabled={page <= 1}
        onClick={() => onPageChange(page - 1)}
      >
        <ChevronLeft className="size-4" />
      </button>
      <span className="text-sm text-muted-foreground">
        Page {page} of {pageCount}
      </span>
      <button
        className="focus-ring rounded p-2 hover:bg-accent disabled:opacity-50"
        aria-label="Next page"
        disabled={page >= pageCount}
        onClick={() => onPageChange(page + 1)}
      >
        <ChevronRight className="size-4" />
      </button>
    </nav>
  )
}
export function DropdownMenu({
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
      <summary className="focus-ring cursor-pointer list-none rounded-md">
        {trigger}
        <MoreHorizontal className="sr-only" />
      </summary>
      <div
        role="menu"
        className="absolute right-0 z-50 mt-2 min-w-40 rounded-md border bg-popover p-1 text-popover-foreground shadow-elevated"
      >
        {children}
      </div>
    </details>
  )
}
export function DropdownMenuItem({
  children,
  className,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      role="menuitem"
      className={cn(
        'focus-ring flex w-full items-center rounded-sm px-2 py-1.5 text-left text-sm hover:bg-accent disabled:opacity-50',
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}

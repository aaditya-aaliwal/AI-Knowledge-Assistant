import { Check } from 'lucide-react'
import {
  forwardRef,
  useId,
  type HTMLAttributes,
  type InputHTMLAttributes,
  type SelectHTMLAttributes,
} from 'react'
import { cn } from '@/lib/utils'
export const Checkbox = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      type="checkbox"
      className={cn(
        "focus-ring checked:bg-[url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='none' stroke='white' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m3 8 3 3 7-7'/%3E%3C/svg%3E\")] size-4 appearance-none rounded border bg-background checked:border-primary checked:bg-primary",
        className,
      )}
      {...props}
    />
  ),
)
Checkbox.displayName = 'Checkbox'
export const Switch = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, id, ...props }, ref) => {
    const generatedId = useId()
    return (
      <span className="inline-flex">
        <input
          ref={ref}
          id={id ?? generatedId}
          type="checkbox"
          role="switch"
          className="peer sr-only"
          {...props}
        />
        <label
          htmlFor={id ?? generatedId}
          className={cn(
            'focus-ring h-6 w-11 cursor-pointer rounded-full bg-muted p-0.5 transition-colors peer-checked:bg-primary peer-disabled:cursor-not-allowed peer-disabled:opacity-50',
            className,
          )}
        >
          <span className="block size-5 rounded-full bg-background shadow-sm transition-transform peer-checked:translate-x-5" />
        </label>
      </span>
    )
  },
)
Switch.displayName = 'Switch'
export function RadioGroup({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div role="radiogroup" className={cn('grid gap-2', className)} {...props} />
}
export const Radio = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      type="radio"
      className={cn('focus-ring size-4 accent-primary', className)}
      {...props}
    />
  ),
)
Radio.displayName = 'Radio'
export const Select = forwardRef<HTMLSelectElement, SelectHTMLAttributes<HTMLSelectElement>>(
  ({ className, children, ...props }, ref) => (
    <select
      ref={ref}
      className={cn(
        'focus-ring flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50',
        className,
      )}
      {...props}
    >
      {children}
    </select>
  ),
)
Select.displayName = 'Select'
export function CheckIcon() {
  return <Check className="size-4" aria-hidden="true" />
}

import { forwardRef, type HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'
const part = (classes: string) =>
  forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(({ className, ...props }, ref) => (
    <div ref={ref} className={cn(classes, className)} {...props} />
  ))
export const Card = part('rounded-lg border bg-card text-card-foreground shadow-soft')
export const CardHeader = part('flex flex-col space-y-1.5 p-6')
export const CardContent = part('p-6 pt-0')
export const CardFooter = part('flex items-center p-6 pt-0')
export const CardTitle = forwardRef<HTMLHeadingElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn('text-lg font-semibold leading-none tracking-tight', className)}
      {...props}
    />
  ),
)
export const CardDescription = forwardRef<
  HTMLParagraphElement,
  HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p ref={ref} className={cn('text-sm text-muted-foreground', className)} {...props} />
))

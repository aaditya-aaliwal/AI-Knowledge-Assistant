import { User } from 'lucide-react'
import { type ImgHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'
export function Avatar({ className, alt = '', ...props }: ImgHTMLAttributes<HTMLImageElement>) {
  return (
    <span
      className={cn(
        'inline-flex size-10 shrink-0 overflow-hidden rounded-full bg-muted',
        className,
      )}
    >
      {props.src ? (
        <img className="size-full object-cover" alt={alt} {...props} />
      ) : (
        <User className="m-auto size-5 text-muted-foreground" aria-label={alt || 'User'} />
      )}
    </span>
  )
}

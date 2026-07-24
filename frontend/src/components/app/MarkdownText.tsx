import { Fragment } from 'react'

function inline(text: string) {
  const parts = text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g)
  return parts.map((part, index) => {
    if (part.startsWith('`') && part.endsWith('`')) return <code key={index} className="rounded bg-muted px-1 py-0.5 text-xs">{part.slice(1, -1)}</code>
    if (part.startsWith('**') && part.endsWith('**')) return <strong key={index}>{part.slice(2, -2)}</strong>
    return <Fragment key={index}>{part}</Fragment>
  })
}

export function MarkdownText({ children }: { children: string }) {
  return <div className="space-y-2 break-words text-sm leading-6">{children.split('\n').map((line, index) => line.startsWith('- ') ? <div key={index} className="flex gap-2"><span aria-hidden="true">•</span><span>{inline(line.slice(2))}</span></div> : <p key={index}>{inline(line || ' ')}</p>)}</div>
}

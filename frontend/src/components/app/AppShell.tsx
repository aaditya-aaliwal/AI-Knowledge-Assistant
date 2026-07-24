import { BrainCircuit, FileText, LayoutDashboard, LogOut, Menu, MessageSquare, Search, Settings, Upload, UserRound } from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { useAuth } from '@/hooks/useAuth'
import { cn } from '@/lib/utils'

const items = [
  ['Dashboard', '/app', LayoutDashboard],
  ['Chat', '/app/chat', MessageSquare], ['Upload', '/app/upload', Upload], ['Documents', '/app/documents', FileText],
  ['Search', '/app/search', Search], ['RAG', '/app/rag', BrainCircuit], ['Profile', '/app/profile', UserRound], ['Settings', '/app/settings', Settings],
] as const

export function AppShell() {
  const [open, setOpen] = useState(false)
  const { logout } = useAuth(); const navigate = useNavigate()
  const signOut = () => { logout(); navigate('/login', { replace: true }) }
  return <div className="min-h-screen bg-muted/30">
    <header className="sticky top-0 z-20 flex h-14 items-center gap-3 border-b bg-background px-4 md:hidden">
      <Button variant="ghost" size="icon" aria-label="Toggle navigation" onClick={() => setOpen(!open)}><Menu className="size-5" /></Button>
      <span className="font-semibold">AI Knowledge Assistant</span>
    </header>
    <aside className={cn('fixed inset-y-0 left-0 z-30 flex w-64 -translate-x-full flex-col border-r bg-background transition-transform md:translate-x-0', open && 'translate-x-0')}>
      <div className="flex h-16 items-center gap-3 border-b px-5"><BrainCircuit className="size-6" /><span className="font-semibold">Knowledge Assistant</span></div>
      <nav className="flex-1 space-y-1 p-3" aria-label="Main navigation">{items.map(([label, href, Icon]) => <NavLink key={href} to={href} onClick={() => setOpen(false)} className={({ isActive }) => cn('focus-ring flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium', isActive ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-accent hover:text-foreground')}><Icon className="size-4" />{label}</NavLink>)}</nav>
      <div className="border-t p-3"><Button className="w-full justify-start" variant="ghost" onClick={signOut}><LogOut className="size-4" />Logout</Button></div>
    </aside>
    {open && <button className="fixed inset-0 z-20 bg-foreground/20 md:hidden" aria-label="Close navigation" onClick={() => setOpen(false)} />}
    <main className="min-h-screen p-5 md:ml-64 md:p-8"><Outlet /></main>
  </div>
}

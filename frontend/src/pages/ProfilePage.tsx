import { LogOut } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { PageHeader } from '@/components/app/PageHeader'
import { useAuth } from '@/hooks/useAuth'
export function ProfilePage() { const { user, logout } = useAuth(); const navigate = useNavigate(); const signOut = () => { logout(); navigate('/login', { replace: true }) }; return <div className="mx-auto max-w-2xl"><PageHeader title="Profile" description="Your authenticated account details." /><Card><CardContent className="space-y-4 p-6"><dl className="grid gap-4 text-sm sm:grid-cols-2"><div><dt className="text-muted-foreground">Name</dt><dd className="mt-1 font-medium">{user?.name}</dd></div><div><dt className="text-muted-foreground">Email</dt><dd className="mt-1 font-medium">{user?.email}</dd></div><div><dt className="text-muted-foreground">User ID</dt><dd className="mt-1 font-medium">{user?.id}</dd></div></dl><Button variant="outline" onClick={signOut}><LogOut className="size-4" />Logout</Button></CardContent></Card></div> }

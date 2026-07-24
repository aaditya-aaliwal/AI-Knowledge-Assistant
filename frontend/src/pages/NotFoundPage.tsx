import { Compass } from 'lucide-react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
export function NotFoundPage() { return <main className="grid min-h-screen place-items-center bg-muted/30 p-6"><section className="max-w-md text-center"><Compass className="mx-auto size-10 text-muted-foreground" /><p className="mt-5 text-5xl font-semibold">404</p><h1 className="mt-3 text-xl font-semibold">Page not found</h1><p className="mt-2 text-sm text-muted-foreground">The page you requested does not exist or has moved.</p><Button className="mt-6" asChild><Link to="/app">Go to dashboard</Link></Button></section></main> }

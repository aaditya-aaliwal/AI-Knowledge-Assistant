import { zodResolver } from '@hookform/resolvers/zod'
import { BrainCircuit, Moon, Sun } from 'lucide-react'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { z } from 'zod'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/form-controls'
import { Input, PasswordInput } from '@/components/ui/input'
import { getApiErrorMessage } from '@/features/auth/api'
import { useAuth } from '@/hooks/useAuth'
import { useTheme } from '@/hooks/useTheme'

const loginSchema = z.object({
  email: z.string().trim().email('Enter a valid email address.'),
  password: z.string().min(1, 'Enter your password.'),
  rememberMe: z.boolean(),
})

type LoginFormValues = z.infer<typeof loginSchema>

type LocationState = { from?: { pathname?: string } }

export function LoginPage() {
  const { login } = useAuth()
  const { theme, setTheme } = useTheme()
  const navigate = useNavigate()
  const location = useLocation()
  const [submitError, setSubmitError] = useState<string | null>(null)
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '', rememberMe: true },
  })

  const onSubmit = async ({ email, password }: LoginFormValues) => {
    setSubmitError(null)

    try {
      await login({ email, password })
      const state = location.state as LocationState | null
      navigate(state?.from?.pathname ?? '/app', { replace: true })
    } catch (error) {
      setSubmitError(getApiErrorMessage(error))
    }
  }

  const isDark = theme === 'dark'

  return (
    <main className="grid min-h-screen bg-muted/40 lg:grid-cols-2">
      <section className="relative hidden overflow-hidden bg-primary p-12 text-primary-foreground lg:flex lg:flex-col lg:justify-between">
        <div className="flex items-center gap-3 text-lg font-semibold">
          <span className="grid size-10 place-items-center rounded-lg bg-primary-foreground/10"><BrainCircuit className="size-5" aria-hidden="true" /></span>
          AI Knowledge Assistant
        </div>
        <div className="max-w-md">
          <p className="text-3xl font-semibold tracking-tight">Your knowledge, ready when you are.</p>
          <p className="mt-4 text-primary-foreground/70">A focused workspace for finding answers across the information that matters to your team.</p>
        </div>
        <p className="text-sm text-primary-foreground/60">Secure access for your organization.</p>
      </section>

      <section className="relative flex min-h-screen items-center justify-center p-6 sm:p-10">
        <Button
          className="absolute right-6 top-6"
          variant="ghost"
          size="icon"
          type="button"
          onClick={() => setTheme(isDark ? 'light' : 'dark')}
          aria-label={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
        >
          {isDark ? <Sun className="size-4" /> : <Moon className="size-4" />}
        </Button>

        <Card className="w-full max-w-md shadow-elevated">
          <CardHeader className="space-y-2">
            <div className="mb-3 flex items-center gap-3 lg:hidden">
              <span className="grid size-9 place-items-center rounded-lg bg-primary text-primary-foreground"><BrainCircuit className="size-5" aria-hidden="true" /></span>
              <span className="font-semibold">AI Knowledge Assistant</span>
            </div>
            <CardTitle className="text-2xl">Welcome back</CardTitle>
            <CardDescription>Sign in to continue to your workspace.</CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-5" onSubmit={handleSubmit(onSubmit)} noValidate>
              {submitError && <div role="alert" className="rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm text-destructive">{submitError}</div>}
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">Email address</label>
                <Input id="email" type="email" autoComplete="email" aria-invalid={Boolean(errors.email)} aria-describedby={errors.email ? 'email-error' : undefined} {...register('email')} />
                {errors.email && <p id="email-error" className="text-sm text-destructive">{errors.email.message}</p>}
              </div>
              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium">Password</label>
                <PasswordInput id="password" autoComplete="current-password" aria-invalid={Boolean(errors.password)} aria-describedby={errors.password ? 'password-error' : undefined} {...register('password')} />
                {errors.password && <p id="password-error" className="text-sm text-destructive">{errors.password.message}</p>}
              </div>
              <label className="flex w-fit cursor-pointer items-center gap-2 text-sm text-muted-foreground">
                <Checkbox aria-label="Remember me" {...register('rememberMe')} />
                Remember me
              </label>
              <Button className="w-full" type="submit" loading={isSubmitting} disabled={isSubmitting}>Sign in</Button>
            </form>
            <p className="mt-4 text-center text-sm text-muted-foreground">Need an account? <Link className="underline" to="/register">Register</Link></p>
          </CardContent>
        </Card>
      </section>
    </main>
  )
}

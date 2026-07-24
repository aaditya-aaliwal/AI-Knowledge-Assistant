export type AuthUser = {
  id: number
  name: string
  email: string
}

export type LoginCredentials = {
  email: string
  password: string
}

type TokenResponse = {
  access_token: string
  refresh_token: string
  token_type: 'bearer'
}

export type LoginResponse = TokenResponse

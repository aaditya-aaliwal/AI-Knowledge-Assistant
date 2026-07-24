export type User = { id: number; name: string; email: string }

export type Chat = { id: number; title: string; user_id: number; created_at: string }

export type Document = {
  id: number
  filename: string
  content: string
  chat_id: number
  created_at: string
  filepath?: string | null
  uploaded_by?: number | null
  status: 'UPLOADING' | 'PROCESSING' | 'READY' | 'FAILED'
}

export type UploadResult = { message: string; filename: string; document?: Document }
export type ChatReply = { response: string; category?: string; confidence?: number }
export type RAGReply = { answer: string; sources: string[] }
export type Health = { status: string }
export type Version = { version: string }

export type SearchResult = {
  content?: string
  document?: string
  filename?: string
  metadata?: Record<string, unknown>
  score?: number
  similarity?: number
  distance?: number
}
export type SearchResponse = { results: SearchResult[]; displayable: boolean }

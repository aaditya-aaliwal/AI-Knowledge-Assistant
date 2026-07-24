import axios from 'axios'

import { api } from '@/lib/api'
import { normalizeChatReply, normalizeDocuments, normalizeRag, normalizeSearch, normalizeUpload } from './normalizers'
import type { Chat, ChatReply, Document, Health, RAGReply, SearchResponse, UploadResult, Version } from './types'

export async function getHealth(): Promise<Health> { return (await api.get<Health>('/health')).data }
export async function getVersion(): Promise<Version> { return (await api.get<Version>('/version')).data }
export async function sendChat(message: string): Promise<ChatReply> { return normalizeChatReply((await api.post<unknown>('/chat', { message })).data) }
export async function askRag(question: string): Promise<RAGReply> { return normalizeRag((await api.post<unknown>('/rag/ask', { question })).data) }
export async function searchKnowledge(question: string): Promise<SearchResponse> { return normalizeSearch((await api.post<unknown>('/search', { question })).data) }
export async function uploadPdf(file: File, onProgress: (percent: number) => void): Promise<UploadResult> {
  const form = new FormData(); form.append('file', file)
  return normalizeUpload((await api.post<unknown>('/documents/upload', form, { onUploadProgress: (event) => onProgress(event.total ? Math.round((event.loaded / event.total) * 100) : 0) })).data)
}
export async function getDocuments(): Promise<Document[]> { return normalizeDocuments((await api.get<unknown>('/documents')).data) }
export async function deleteDocument(id: number): Promise<void> { await api.delete(`/documents/${id}`) }
export async function getDocument(id: number): Promise<Document> { return (await api.get<Document>(`/documents/${id}`)).data }
export async function getChats(): Promise<Chat[]> { return (await api.get<Chat[]>('/chats')).data }
export async function createChat(title: string): Promise<Chat> { return (await api.post<Chat>('/chats', { title })).data }
export function apiError(error: unknown, fallback = 'Something went wrong. Please try again.'): string {
  if (axios.isAxiosError<{ detail?: string | Array<{ msg?: string }> }>(error)) {
    if (error.code === 'ECONNABORTED') return 'The request took too long. Please try again.'
    if (!error.response) return 'Unable to reach the server. Check your connection and try again.'
    if (error.response.status === 401) return 'Your session has expired. Please sign in again.'
    if (error.response.status === 403) return 'You do not have permission to do that.'
    if (error.response.status === 503) return 'AI service is temporarily busy. Retrying...'
    if (error.response.status >= 500) return 'The service is temporarily unavailable. Please try again shortly.'
    const detail = error.response.data.detail
    if (Array.isArray(detail)) return detail.map((item) => item.msg).filter(Boolean).join(' ') || fallback
    return detail ?? fallback
  }
  return fallback
}

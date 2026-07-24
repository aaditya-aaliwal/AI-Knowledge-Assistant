import type { ChatReply, Document, RAGReply, SearchResponse, SearchResult, UploadResult } from './types'

type RecordValue = Record<string, unknown>
const isRecord = (value: unknown): value is RecordValue => typeof value === 'object' && value !== null && !Array.isArray(value)
const stringValue = (value: unknown) => typeof value === 'string' ? value : ''
const numberValue = (value: unknown) => typeof value === 'number' && Number.isFinite(value) ? value : undefined
const arrayValue = (value: unknown): unknown[] => Array.isArray(value) ? value : []
const firstLevel = (value: unknown): unknown[] => { const items = arrayValue(value); return Array.isArray(items[0]) ? arrayValue(items[0]) : items }

export function normalizeChatReply(payload: unknown): ChatReply {
  const response = isRecord(payload) ? payload.response ?? payload : payload
  if (isRecord(response)) {
    const category = stringValue(response.category)
    const confidence = numberValue(response.confidence)
    return { response: stringValue(response.answer) || stringValue(response.response) || 'No response was returned.', ...(category ? { category } : {}), ...(confidence !== undefined ? { confidence } : {}) }
  }
  const text = stringValue(response)
  try { const parsed: unknown = JSON.parse(text); if (isRecord(parsed)) return normalizeChatReply(parsed) } catch { /* plain text response */ }
  return { response: text || 'No response was returned.' }
}

export function normalizeDocument(payload: unknown): Document | null {
  if (!isRecord(payload) || typeof payload.id !== 'number' || !stringValue(payload.filename)) return null
  const rawStatus = stringValue(payload.status).toUpperCase()
  const status = rawStatus === 'UPLOADING' || rawStatus === 'PROCESSING' || rawStatus === 'FAILED' || rawStatus === 'READY' ? rawStatus : 'READY'
  return { id: payload.id, filename: stringValue(payload.filename), content: stringValue(payload.content), chat_id: typeof payload.chat_id === 'number' ? payload.chat_id : 0, created_at: stringValue(payload.created_at), status, ...(typeof payload.filepath === 'string' ? { filepath: payload.filepath } : {}), ...(typeof payload.uploaded_by === 'number' ? { uploaded_by: payload.uploaded_by } : {}) }
}

export function normalizeDocuments(payload: unknown): Document[] { const source = Array.isArray(payload) ? payload : isRecord(payload) ? payload.documents ?? payload.results ?? [] : []; return arrayValue(source).map(normalizeDocument).filter((item): item is Document => item !== null) }

export function normalizeUpload(payload: unknown): UploadResult { const data = isRecord(payload) ? payload : {}; const document = normalizeDocument(data.document); return { message: stringValue(data.message) || 'Document uploaded successfully.', filename: stringValue(data.filename) || document?.filename || 'document', ...(document ? { document } : {}) } }

function normalizeMatch(value: unknown, fallback?: { metadata?: unknown; distance?: unknown }): SearchResult | null { const row = isRecord(value) ? value : { content: value }; const metadata = isRecord(row.metadata) ? row.metadata : isRecord(fallback?.metadata) ? fallback.metadata : undefined; const content = stringValue(row.content) || stringValue(row.document) || stringValue(row.text); const filename = stringValue(row.filename); const similarity = numberValue(row.similarity); const score = numberValue(row.score); const distance = numberValue(row.distance) ?? numberValue(fallback?.distance); if (!content && !metadata) return null; return { ...(content ? { content } : {}), ...(filename ? { filename } : {}), ...(metadata ? { metadata } : {}), ...(similarity !== undefined ? { similarity } : {}), ...(score !== undefined ? { score } : {}), ...(distance !== undefined ? { distance } : {}) } }

export function normalizeSearch(payload: unknown): SearchResponse {
  const data = isRecord(payload) ? payload : null
  const direct = Array.isArray(payload) ? payload : data ? (Array.isArray(data.results) ? data.results : Array.isArray(data.matches) ? data.matches : null) : null
  if (direct) return { results: direct.map((item) => normalizeMatch(item)).filter((item): item is SearchResult => item !== null), displayable: true }
  if (data && Array.isArray(data.documents)) { const docs = firstLevel(data.documents); const metadata = firstLevel(data.metadatas); const distances = firstLevel(data.distances); return { results: docs.map((item, index) => normalizeMatch(item, { metadata: metadata[index], distance: distances[index] })).filter((item): item is SearchResult => item !== null), displayable: true } }
  return { results: [], displayable: Array.isArray(payload) || Boolean(data && ('results' in data || 'matches' in data || 'documents' in data)) }
}

export function normalizeRag(payload: unknown): RAGReply { const data = isRecord(payload) ? payload : {}; return { answer: stringValue(data.answer) || stringValue(data.response) || 'No answer was returned.', sources: arrayValue(data.sources).map(stringValue).filter(Boolean) } }

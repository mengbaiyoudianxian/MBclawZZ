import { apiClient } from '../client'

export interface AgentChatRequest {
  message: string
  conversation_id?: number
  model?: string
  api_key: string
  base_url?: string
}

export interface AgentChatResponse {
  conversation_id: number
  reply: string
}

export interface AgentConversation {
  id: number
  user_id: number
  title: string
  model: string
  messages: Array<{ role: string; content: string }>
  created_at: string
  updated_at: string
}

export const agentAPI = {
  async chat(payload: AgentChatRequest): Promise<AgentChatResponse> {
    const { data } = await apiClient.post<AgentChatResponse>('/admin/agent/chat', payload)
    return data
  },

  async listConversations(): Promise<AgentConversation[]> {
    const { data } = await apiClient.get<AgentConversation[]>('/admin/agent/conversations')
    return data
  },

  async getConversation(id: number): Promise<AgentConversation> {
    const { data } = await apiClient.get<AgentConversation>(`/admin/agent/conversations/${id}`)
    return data
  },

  async deleteConversation(id: number): Promise<void> {
    await apiClient.delete(`/admin/agent/conversations/${id}`)
  }
}

export default agentAPI

import { apiClient } from '../client'

export interface MBclawFoundationStatus {
  entrypoints: string[]
  control_entrypoints: string[]
  control_capabilities: string[]
  token_sources: Array<{
    kind: string
    status: string
    description: string
  }>
  limits: {
    user_concurrency: string
    user_rate_multiplier: string
    api_key_rate_limit: string
    model_rate_multiplier: string
    account_concurrency: string
    account_rate_multiplier: string
  }
  panels: {
    mbclaw_token_panel: string
    sub2api_admin_panel: string
  }
  updated_at: string
}

export interface MBclawUpstreamTokenRequest {
  name: string
  platform: string
  api_key: string
  base_url?: string
  model?: string
  models?: string[]
  provider?: string
  group_ids?: number[]
  owner_user_id?: number
  source?: string
  token_pool_kind?: string
  concurrency?: number
  rate_multiplier?: number
  load_factor?: number
  priority?: number
  extra?: Record<string, unknown>
  confirm_mixed_channel_risk?: boolean
}

export interface MBclawTokenPoolModuleRequest {
  name: string
  base_url: string
  provider?: string
  api_key?: string
  models?: string[]
  group_ids?: number[]
  owner_user_id?: number
  source?: string
  kind?: string
  concurrency?: number
  rate_multiplier?: number
  load_factor?: number
  priority?: number
  extra?: Record<string, unknown>
  schedulable?: boolean
}

export const mbclawAPI = {
  async getStatus(): Promise<MBclawFoundationStatus> {
    const { data } = await apiClient.get<MBclawFoundationStatus>('/admin/mbclaw/status')
    return data
  },

  async createUpstreamToken(payload: MBclawUpstreamTokenRequest) {
    const { data } = await apiClient.post('/admin/mbclaw/upstream-tokens', payload)
    return data
  },

  async registerTokenPoolModule(payload: MBclawTokenPoolModuleRequest) {
    const { data } = await apiClient.post('/admin/mbclaw/token-pool-modules', payload)
    return data
  }
}

export default mbclawAPI

<template>
  <div class="agent-chat-container">
    <!-- Sidebar: conversations list -->
    <aside class="chat-sidebar">
      <div class="sidebar-header">
        <h3>会话</h3>
        <button class="btn-new" @click="startNewChat">+ 新对话</button>
      </div>
      <div class="conversation-list">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          :class="['conv-item', { active: conv.id === activeConvId }]"
          @click="loadConversation(conv)"
        >
          <span class="conv-title">{{ conv.title || '新对话' }}</span>
          <button class="btn-delete" @click.stop="removeConversation(conv.id)">×</button>
        </div>
        <div v-if="conversations.length === 0" class="empty-hint">暂无会话</div>
      </div>
    </aside>

    <!-- Main chat area -->
    <main class="chat-main">
      <!-- Top config bar -->
      <div class="chat-config">
        <input v-model="apiKey" type="password" placeholder="API Key (必填)" class="input-key" />
        <input v-model="baseUrl" placeholder="Base URL (默认 OpenAI)" class="input-url" />
        <select v-model="model" class="input-model">
          <option value="gpt-4o">gpt-4o</option>
          <option value="gpt-4o-mini">gpt-4o-mini</option>
          <option value="gpt-4.1">gpt-4.1</option>
          <option value="claude-sonnet-4-20250514">claude-sonnet-4</option>
          <option value="deepseek-chat">deepseek-chat</option>
        </select>
      </div>

      <!-- Messages -->
      <div class="chat-messages" ref="msgContainer">
        <div v-if="messages.length === 0" class="welcome">
          <h2>MBclaw 管理智能体</h2>
          <p>配置 API Key 后，用自然语言管理 sub2api：</p>
          <ul>
            <li>「列出所有用户」</li>
            <li>「查看用户 ID 2 的详情」</li>
            <li>「给我看看所有 openai 账号」</li>
            <li>「系统当前有多少分组」</li>
          </ul>
        </div>
        <div v-for="(msg, idx) in messages" :key="idx" :class="['msg', msg.role]">
          <div class="msg-content">{{ msg.content }}</div>
          <div v-if="msg.tool_calls" class="tool-calls">
            <div v-for="tc in msg.tool_calls" :key="tc.id" class="tool-call">
              🔧 {{ tc.function.name }}
            </div>
          </div>
        </div>
        <div v-if="loading" class="msg assistant">
          <div class="msg-content typing">思考中...</div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input">
        <textarea
          v-model="input"
          @keydown.enter.exact.prevent="sendMessage"
          placeholder="输入消息，Enter 发送..."
          rows="2"
          :disabled="loading"
        ></textarea>
        <button @click="sendMessage" :disabled="loading || !input.trim() || !apiKey.trim()" class="btn-send">
          发送
        </button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import agentAPI, { type AgentConversation } from '@/api/admin/agent'

const apiKey = ref('')
const baseUrl = ref('')
const model = ref('gpt-4o')
const input = ref('')
const loading = ref(false)
const messages = ref<Array<{ role: string; content: string; tool_calls?: any[] }>>([])
const conversations = ref<AgentConversation[]>([])
const activeConvId = ref<number | null>(null)
const msgContainer = ref<HTMLElement | null>(null)

onMounted(async () => {
  try {
    conversations.value = await agentAPI.listConversations()
  } catch { /* ignore */ }
})

function scrollToBottom() {
  nextTick(() => {
    if (msgContainer.value) {
      msgContainer.value.scrollTop = msgContainer.value.scrollHeight
    }
  })
}

async function sendMessage() {
  if (!input.value.trim() || !apiKey.value.trim() || loading.value) return
  const msg = input.value.trim()
  input.value = ''
  messages.value.push({ role: 'user', content: msg })
  loading.value = true
  scrollToBottom()

  try {
    const res = await agentAPI.chat({
      message: msg,
      api_key: apiKey.value,
      model: model.value,
      base_url: baseUrl.value || undefined,
      conversation_id: activeConvId.value ?? undefined
    })
    activeConvId.value = res.conversation_id
    messages.value.push({ role: 'assistant', content: res.reply })
    conversations.value = await agentAPI.listConversations()
  } catch (e: any) {
    messages.value.push({ role: 'assistant', content: `❌ 错误: ${e?.message || e}` })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

async function loadConversation(conv: AgentConversation) {
  activeConvId.value = conv.id
  try {
    const full = await agentAPI.getConversation(conv.id)
    messages.value = (full.messages || []).filter((m: any) => m.role !== 'tool')
  } catch { /* ignore */ }
  scrollToBottom()
}

function startNewChat() {
  activeConvId.value = null
  messages.value = []
}

async function removeConversation(id: number) {
  try {
    await agentAPI.deleteConversation(id)
    if (activeConvId.value === id) {
      activeConvId.value = null
      messages.value = []
    }
    conversations.value = conversations.value.filter(c => c.id !== id)
  } catch { /* ignore */ }
}
</script>

<style scoped>
.agent-chat-container {
  display: flex;
  height: calc(100vh - 64px);
  background: #f8fafc;
}

.chat-sidebar {
  width: 260px;
  background: #fff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 15px;
  color: #334155;
}

.btn-new {
  background: #3b82f6;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
}

.btn-new:hover { background: #2563eb; }

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.conv-item {
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2px;
  font-size: 14px;
  color: #475569;
}

.conv-item:hover { background: #f1f5f9; }
.conv-item.active { background: #eff6ff; color: #1d4ed8; }

.conv-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  margin-right: 8px;
}

.btn-delete {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 18px;
  padding: 0 4px;
  line-height: 1;
  flex-shrink: 0;
}

.btn-delete:hover { color: #ef4444; }

.empty-hint {
  padding: 24px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.chat-config {
  padding: 12px 16px;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.input-key, .input-url, .input-model {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
}

.input-key:focus, .input-url:focus, .input-model:focus {
  border-color: #3b82f6;
}

.input-key { flex: 2; }
.input-url { flex: 2; }
.input-model { flex: 1; }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.welcome {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.welcome h2 { color: #1e293b; margin-bottom: 12px; }
.welcome ul { list-style: none; padding: 0; }
.welcome li {
  padding: 6px 0;
  color: #3b82f6;
  cursor: pointer;
}

.msg {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.msg.user { align-items: flex-end; }
.msg.assistant { align-items: flex-start; }

.msg-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.msg.user .msg-content {
  background: #3b82f6;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.msg.assistant .msg-content {
  background: #fff;
  color: #334155;
  border: 1px solid #e2e8f0;
  border-bottom-left-radius: 4px;
}

.typing { color: #94a3b8; }

.tool-calls {
  margin-top: 4px;
  font-size: 12px;
}

.tool-call {
  color: #64748b;
  padding: 2px 8px;
}

.chat-input {
  padding: 12px 16px;
  background: #fff;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.chat-input textarea {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  resize: none;
  outline: none;
  font-family: inherit;
}

.chat-input textarea:focus { border-color: #3b82f6; }

.btn-send {
  background: #3b82f6;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  flex-shrink: 0;
}

.btn-send:hover:not(:disabled) { background: #2563eb; }
.btn-send:disabled { opacity: 0.5; cursor: not-allowed; }
</style>

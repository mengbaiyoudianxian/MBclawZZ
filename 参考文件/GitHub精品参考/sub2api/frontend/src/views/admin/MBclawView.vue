<template>
  <div class="space-y-6">
    <div class="rounded-2xl border border-blue-100 bg-gradient-to-br from-blue-50 to-indigo-50 p-6 dark:border-blue-900/40 dark:from-blue-950/30 dark:to-indigo-950/30">
      <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm font-semibold uppercase tracking-wide text-blue-600 dark:text-blue-300">MBclaw foundation</p>
          <h1 class="mt-1 text-2xl font-bold text-gray-900 dark:text-white">MBclaw Token 地基</h1>
          <p class="mt-2 max-w-3xl text-sm text-gray-600 dark:text-gray-300">
            这里是给 Mother 掌控全局的预留入口：接收用户上传 key、注册外部 token 池模块，并汇报 sub2api 当前可承接的倍率、并发、模型和管理面板能力。
          </p>
        </div>
        <button class="btn btn-primary" :disabled="loading" @click="loadStatus">
          {{ loading ? '刷新中…' : '刷新状态' }}
        </button>
      </div>
    </div>

    <div v-if="status" class="grid gap-4 lg:grid-cols-3">
      <section class="card p-5 lg:col-span-1">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">统一入口</h2>
        <ul class="mt-4 space-y-2 text-sm text-gray-600 dark:text-gray-300">
          <li v-for="item in status.entrypoints" :key="item" class="rounded-lg bg-gray-50 px-3 py-2 font-mono dark:bg-dark-800">{{ item }}</li>
        </ul>
      </section>

      <section class="card p-5 lg:col-span-1">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Mother 控制入口</h2>
        <ul class="mt-4 space-y-2 text-sm text-gray-600 dark:text-gray-300">
          <li v-for="item in status.control_entrypoints" :key="item" class="rounded-lg bg-gray-50 px-3 py-2 font-mono dark:bg-dark-800">{{ item }}</li>
        </ul>
      </section>

      <section class="card p-5 lg:col-span-1">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">面板边界</h2>
        <dl class="mt-4 space-y-3 text-sm">
          <div>
            <dt class="font-medium text-gray-900 dark:text-white">MBclaw 内置 Token 面板</dt>
            <dd class="mt-1 text-gray-600 dark:text-gray-300">{{ status.panels.mbclaw_token_panel }}</dd>
          </div>
          <div>
            <dt class="font-medium text-gray-900 dark:text-white">sub2api 管理面板</dt>
            <dd class="mt-1 text-gray-600 dark:text-gray-300">{{ status.panels.sub2api_admin_panel }}</dd>
          </div>
        </dl>
      </section>
    </div>

    <div v-if="status" class="grid gap-4 lg:grid-cols-2">
      <section class="card p-5">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Token 来源</h2>
        <div class="mt-4 space-y-3">
          <div v-for="source in status.token_sources" :key="source.kind" class="rounded-xl border border-gray-200 p-4 dark:border-dark-700">
            <div class="flex items-center justify-between gap-3">
              <span class="font-semibold text-gray-900 dark:text-white">{{ source.kind }}</span>
              <span class="rounded-full bg-blue-100 px-2.5 py-1 text-xs font-medium text-blue-700 dark:bg-blue-900/40 dark:text-blue-200">{{ source.status }}</span>
            </div>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ source.description }}</p>
          </div>
        </div>
      </section>

      <section class="card p-5">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">倍率与并发承接</h2>
        <dl class="mt-4 grid gap-3 text-sm sm:grid-cols-2">
          <div v-for="(value, key) in status.limits" :key="key" class="rounded-lg bg-gray-50 p-3 dark:bg-dark-800">
            <dt class="font-medium text-gray-900 dark:text-white">{{ key }}</dt>
            <dd class="mt-1 text-gray-600 dark:text-gray-300">{{ value }}</dd>
          </div>
        </dl>
      </section>
    </div>

    <div class="grid gap-4 lg:grid-cols-2">
      <section class="card p-5">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">接收用户上传 Key</h2>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">写入 sub2api account，默认使用账号并发和倍率字段承接调度与消耗。</p>
        <div class="mt-4 grid gap-3">
          <input v-model="upstreamForm.name" class="input" placeholder="名称，例如 user-openai-key" />
          <input v-model="upstreamForm.platform" class="input" placeholder="平台，例如 openai / anthropic / gemini" />
          <input v-model="upstreamForm.base_url" class="input" placeholder="Base URL，例如 https://api.openai.com/v1" />
          <input v-model="upstreamForm.model" class="input" placeholder="默认模型，例如 gpt-4o-mini" />
          <input v-model="upstreamForm.api_key" class="input" type="password" placeholder="API Key" />
          <div class="grid gap-3 sm:grid-cols-3">
            <input v-model.number="upstreamForm.concurrency" class="input" type="number" min="0" placeholder="并发，默认 1" />
            <input v-model.number="upstreamForm.rate_multiplier" class="input" type="number" min="0" step="0.01" placeholder="倍率，默认 1" />
            <input v-model.number="upstreamForm.priority" class="input" type="number" placeholder="优先级" />
          </div>
          <button class="btn btn-primary" :disabled="savingUpstream" @click="submitUpstreamToken">
            {{ savingUpstream ? '提交中…' : '创建上游 Key' }}
          </button>
        </div>
      </section>

      <section class="card p-5">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">注册外部 Token 池模块</h2>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">用于 miclaw 免费代理、商业中转站或其他 OpenAI-compatible token 池。</p>
        <div class="mt-4 grid gap-3">
          <input v-model="moduleForm.name" class="input" placeholder="模块名称，例如 miclaw-proxy-01" />
          <input v-model="moduleForm.kind" class="input" placeholder="类型，例如 miclaw-proxy" />
          <input v-model="moduleForm.base_url" class="input" placeholder="模块 Base URL" />
          <input v-model="moduleForm.provider" class="input" placeholder="provider 标识" />
          <input v-model="moduleForm.api_key" class="input" type="password" placeholder="模块访问 Key，可选" />
          <div class="grid gap-3 sm:grid-cols-3">
            <input v-model.number="moduleForm.concurrency" class="input" type="number" min="0" placeholder="并发，默认 1" />
            <input v-model.number="moduleForm.rate_multiplier" class="input" type="number" min="0" step="0.01" placeholder="倍率，默认 1" />
            <input v-model.number="moduleForm.priority" class="input" type="number" placeholder="优先级" />
          </div>
          <button class="btn btn-secondary" :disabled="savingModule" @click="submitTokenPoolModule">
            {{ savingModule ? '提交中…' : '注册 Token 池模块' }}
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { mbclawAPI, type MBclawFoundationStatus } from '@/api/admin/mbclaw'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const status = ref<MBclawFoundationStatus | null>(null)
const loading = ref(false)
const savingUpstream = ref(false)
const savingModule = ref(false)

const upstreamForm = reactive({
  name: '',
  platform: 'openai',
  api_key: '',
  base_url: '',
  model: '',
  concurrency: 1,
  rate_multiplier: 1,
  priority: 50
})

const moduleForm = reactive({
  name: '',
  kind: 'miclaw-proxy',
  base_url: '',
  provider: 'miclaw-proxy',
  api_key: '',
  concurrency: 1,
  rate_multiplier: 1,
  priority: 50
})

async function loadStatus() {
  loading.value = true
  try {
    status.value = await mbclawAPI.getStatus()
  } catch (error) {
    appStore.showError('加载 MBclaw 地基状态失败')
  } finally {
    loading.value = false
  }
}

async function submitUpstreamToken() {
  savingUpstream.value = true
  try {
    await mbclawAPI.createUpstreamToken({ ...upstreamForm })
    appStore.showSuccess('上游 Key 已写入 sub2api')
  } catch (error) {
    appStore.showError('创建上游 Key 失败')
  } finally {
    savingUpstream.value = false
  }
}

async function submitTokenPoolModule() {
  savingModule.value = true
  try {
    await mbclawAPI.registerTokenPoolModule({ ...moduleForm })
    appStore.showSuccess('Token 池模块已注册')
  } catch (error) {
    appStore.showError('注册 Token 池模块失败')
  } finally {
    savingModule.value = false
  }
}

onMounted(loadStatus)
</script>

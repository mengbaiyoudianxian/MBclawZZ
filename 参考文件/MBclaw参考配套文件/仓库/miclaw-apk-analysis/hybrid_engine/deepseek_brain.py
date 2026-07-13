#!/usr/bin/env python3
"""
DeepSeek + MiClaw 混合深度思考引擎 v4.0

架构：
  DeepSeek(免费8899) = 大脑，生成思考+指令
  MiClaw(免费8765) = 手脚，执行指令+返回结果
  本脚本 = 循环控制器，协调两者

用法：
  from deepseek_brain import HybridEngine
  
  engine = HybridEngine()
  result = engine.run("分析这个文件的内容...")
  print(result)
"""

import requests
import json
import subprocess
import os
import time
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# ==================== 配置 ====================

DEEPSEEK_API = os.environ.get('DEEPSEEK_API', 'http://localhost:8899/v1/chat/completions')
DEEPSEEK_MODEL = os.environ.get('DEEPSEEK_MODEL', 'deepseek-flash')
DEEPSEEK_TOKEN_FILE = os.path.expanduser('~/.deepseek_conversation_id')

MAX_ROUNDS = 20          # 最大循环轮数
MAX_RESULT_CHARS = 4000  # 单个结果最大字符数
TIMEOUT_SECONDS = 120    # 单次API超时
MEMORY_REFRESH_HOURS = 1 # 超过多少小时刷新记忆

# ==================== 工具定义 ====================

TOOLS_DESC = """可用工具（通过#指令调用，每行一个指令）：
- #exec <command> — 执行shell命令
- #read <path> — 读取文件内容（限4000字符）
- #write <path> <content> — 写入文件
- #search <query> — 联网搜索
- #memory_get <path> — 读取记忆文件
- #memory_save <fact> — 保存事实到长期记忆

输出规则：
- 需要工具时，直接输出 #指令，不要解释
- 收到 [RESULT]...[/RESULT] 后继续分析
- 分析完成时输出 [DONE]
- 不要编造工具结果，等真实结果"""

# ==================== 初始化模板 ====================

INIT_TEMPLATE = """你是深度分析引擎 v4.0，运行在后台子对话中。
当前时间：{timestamp}
身份：后台分析助手，负责复杂推理和代码执行

{tools_desc}

{memory_context}

请确认你理解规则，然后等待任务。"""

TASK_TEMPLATE = """[USER {timestamp}]
{task}"""

REFRESH_TEMPLATE = """[SYSTEM]
距离上次对话已过 {elapsed}，请先读取以下记忆恢复上下文：
1. /root/.openclaw/workspace/main/MEMORY.md
2. /root/.openclaw/workspace/main/memory/{today}.md

然后用 #memory_get 读取，完成后告诉我"记忆已恢复"。"""


class HybridEngine:
    """DeepSeek + MiClaw 混合引擎"""
    
    def __init__(self, deepseek_api=None, deepseek_model=None):
        self.api = deepseek_api or DEEPSEEK_API
        self.model = deepseek_model or DEEPSEEK_MODEL
        self.conversation_id = self._load_cid()
        self.messages = []
        self.last_active = None
        self.thinking_log = []
    
    def _load_cid(self):
        """加载保存的conversation_id"""
        try:
            if os.path.exists(DEEPSEEK_TOKEN_FILE):
                with open(DEEPSEEK_TOKEN_FILE, 'r') as f:
                    return f.read().strip()
        except:
            pass
        return None
    
    def _save_cid(self):
        """保存conversation_id"""
        try:
            with open(DEEPSEEK_TOKEN_FILE, 'w') as f:
                f.write(self.conversation_id or '')
        except:
            pass
    
    def _call_deepseek(self, messages):
        """调用DeepSeek API，处理流式响应"""
        body = {
            'model': self.model,
            'messages': messages,
            'max_tokens': 4000
        }
        if self.conversation_id:
            body['conversation_id'] = self.conversation_id
        
        try:
            resp = requests.post(self.api, json=body, timeout=TIMEOUT_SECONDS, stream=True)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"DeepSeek API错误: {e}")
            return f"[ERROR] DeepSeek调用失败: {e}"
        
        full_content = ''
        for line in resp.iter_lines():
            if not line:
                continue
            line = line.decode('utf-8', errors='ignore')
            if not line.startswith('data: '):
                continue
            data_str = line[6:]
            if data_str == '[DONE]':
                continue
            try:
                data = json.loads(data_str)
                delta = data.get('choices', [{}])[0].get('delta', {})
                if 'content' in delta and delta['content']:
                    full_content += delta['content']
                # 更新conversation_id
                cid = data.get('x_protocol', {}).get('conversation_id', '')
                if cid and cid != self.conversation_id:
                    self.conversation_id = cid
                    self._save_cid()
            except:
                pass
        
        return full_content
    
    def _execute_command(self, cmd):
        """执行shell命令"""
        try:
            r = subprocess.run(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, timeout=30
            )
            output = (r.stdout + r.stderr).strip()
            if len(output) > MAX_RESULT_CHARS:
                output = output[:MAX_RESULT_CHARS] + f"\n... [截断，共{len(output)}字符]"
            return output or "(无输出)"
        except subprocess.TimeoutExpired:
            return "[ERROR] 命令超时(30秒)"
        except Exception as e:
            return f"[ERROR] {e}"
    
    def _read_file(self, path):
        """读取文件"""
        try:
            with open(path, 'r', errors='ignore') as f:
                content = f.read(MAX_RESULT_CHARS)
            if len(content) >= MAX_RESULT_CHARS:
                content += f"\n... [截断]"
            return content
        except Exception as e:
            return f"[ERROR] 读取失败: {e}"
    
    def _write_file(self, path, content):
        """写入文件"""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return f"[OK] 已写入 {path} ({len(content)}字符)"
        except Exception as e:
            return f"[ERROR] 写入失败: {e}"
    
    def _memory_save(self, fact):
        """保存到长期记忆"""
        try:
            mem_dir = '/root/longterm-memory'
            result = subprocess.run(
                ['python3', 'openclaw_memory.py', 'learn', fact],
                cwd=mem_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, timeout=30
            )
            return result.stdout.strip() or result.stderr.strip()
        except Exception as e:
            return f"[ERROR] 记忆保存失败: {e}"
    
    def parse_and_execute(self, response):
        """解析DeepSeek输出，执行指令，返回结果列表"""
        results = []
        executed_any = False
        
        for line in response.split('\n'):
            line = line.strip()
            
            if line.startswith('#exec '):
                cmd = line[6:].strip()
                logger.info(f"执行: {cmd}")
                result = self._execute_command(cmd)
                results.append(f"[RESULT]{result}[/RESULT]")
                executed_any = True
            
            elif line.startswith('#read '):
                path = line[6:].strip()
                logger.info(f"读取: {path}")
                content = self._read_file(path)
                results.append(f"[RESULT]{content}[/RESULT]")
                executed_any = True
            
            elif line.startswith('#write '):
                parts = line[7:].strip().split(' ', 1)
                if len(parts) == 2:
                    path, content = parts
                    logger.info(f"写入: {path}")
                    result = self._write_file(path, content)
                    results.append(f"[RESULT]{result}[/RESULT]")
                    executed_any = True
            
            elif line.startswith('#memory_save '):
                fact = line[13:].strip()
                logger.info(f"保存记忆: {fact[:50]}...")
                result = self._memory_save(fact)
                results.append(f"[RESULT]{result}[/RESULT]")
                executed_any = True
            
            elif line.startswith('#memory_get '):
                path = line[12:].strip()
                logger.info(f"读取记忆: {path}")
                content = self._read_file(path)
                results.append(f"[RESULT]{content}[/RESULT]")
                executed_any = True
            
            elif line.startswith('#search '):
                query = line[8:].strip()
                logger.info(f"搜索: {query}")
                results.append(f"[RESULT]搜索功能暂未实现，请用#exec curl调用搜索API[/RESULT]")
                executed_any = True
        
        return results, executed_any
    
    def _check_memory_refresh(self):
        """检查是否需要刷新记忆"""
        if self.last_active is None:
            return False
        elapsed = datetime.now() - self.last_active
        return elapsed > timedelta(hours=MEMORY_REFRESH_HOURS)
    
    def _get_memory_context(self):
        """获取记忆上下文"""
        today = datetime.now().strftime('%Y-%m-%d')
        mem_file = f'/root/.openclaw/workspace/main/memory/{today}.md'
        memory_md = '/root/.openclaw/workspace/main/MEMORY.md'
        
        context = ""
        for path in [memory_md, mem_file]:
            try:
                if os.path.exists(path):
                    with open(path, 'r', errors='ignore') as f:
                        content = f.read(2000)
                    context += f"\n[{path}]\n{content}\n"
            except:
                pass
        
        if context:
            return f"[长期记忆]\n{context}"
        return ""
    
    def run(self, task, on_thinking=None, on_result=None):
        """
        运行混合引擎
        
        Args:
            task: 任务描述
            on_thinking: 思考内容回调 (可选)
            on_result: 结果回调 (可选)
        
        Returns:
            最终回复文本
        """
        logger.info(f"开始任务: {task[:100]}...")
        
        # 初始化消息（如果是新对话或需要刷新记忆）
        if not self.messages or self._check_memory_refresh():
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            memory_context = self._get_memory_context()
            
            init_msg = INIT_TEMPLATE.format(
                timestamp=timestamp,
                tools_desc=TOOLS_DESC,
                memory_context=memory_context
            )
            self.messages = [{'role': 'user', 'content': init_msg}]
            
            logger.info("初始化DeepSeek...")
            init_reply = self._call_deepseek(self.messages)
            self.messages.append({'role': 'assistant', 'content': init_reply})
            logger.info(f"初始化完成: {init_reply[:200]}")
        
        # 添加任务
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task_msg = TASK_TEMPLATE.format(timestamp=timestamp, task=task)
        self.messages.append({'role': 'user', 'content': task_msg})
        
        # 循环执行
        final_reply = ""
        for round_num in range(1, MAX_ROUNDS + 1):
            logger.info(f"--- 第{round_num}轮 ---")
            
            reply = self._call_deepseek(self.messages)
            self.last_active = datetime.now()
            
            if not reply:
                logger.error("DeepSeek返回空内容")
                break
            
            # 记录思考内容
            for line in reply.split('\n'):
                if line.startswith('[思考]'):
                    self.thinking_log.append(line)
                    if on_thinking:
                        on_thinking(line)
            
            # 检查是否完成
            if '[DONE]' in reply:
                done_idx = reply.index('[DONE]')
                before_done = reply[:done_idx].strip()
                
                # 执行[DONE]之前的指令
                results, executed = self.parse_and_execute(before_done)
                if results:
                    self.messages.append({'role': 'assistant', 'content': reply})
                    self.messages.append({'role': 'user', 'content': '\n'.join(results)})
                    # 最后一轮让DeepSeek总结
                    final_reply = self._call_deepseek(self.messages)
                else:
                    final_reply = before_done
                
                logger.info(f"任务完成，共{round_num}轮")
                break
            
            # 解析并执行指令
            results, executed = self.parse_and_execute(reply)
            
            if executed:
                # 把结果喂回DeepSeek
                self.messages.append({'role': 'assistant', 'content': reply})
                self.messages.append({'role': 'user', 'content': '\n'.join(results)})
            else:
                # 没有指令，当作最终回复
                final_reply = reply
                logger.info(f"DeepSeek未输出指令，视为最终回复")
                break
        
        if not final_reply:
            final_reply = "[ERROR] 达到最大轮数限制，任务未完成"
        
        # 回调
        if on_result:
            on_result(final_reply)
        
        return final_reply
    
    def get_thinking_log(self):
        """获取思考日志"""
        return self.thinking_log.copy()


# ==================== 命令行入口 ====================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 deepseek_brain.py '任务描述'")
        print("  或: echo '任务' | python3 deepseek_brain.py -")
        sys.exit(1)
    
    task = sys.argv[1]
    if task == '-':
        task = sys.stdin.read()
    
    engine = HybridEngine()
    result = engine.run(task)
    
    print("\n" + "="*50)
    print("最终结果:")
    print("="*50)
    print(result)
    
    if engine.get_thinking_log():
        print("\n" + "="*50)
        print("思考过程:")
        print("="*50)
        for log in engine.get_thinking_log():
            print(log)

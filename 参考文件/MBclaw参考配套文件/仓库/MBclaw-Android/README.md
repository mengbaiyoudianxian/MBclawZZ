# MBclaw Android

MBclaw Android 客户端 — Kotlin + Jetpack Compose，Root 版。

## 版本

- **versionCode**: 75
- **versionName**: 5.5.2

## 结构

```
app/src/main/java/com/mbclaw/root/
  agent/          # Agent 核心 (循环/权限/触摸/视觉/调试)
  api/            # LLM API 客户端 (OpenAI/Anthropic/Direct)
  data/           # 数据 (Endpoints/账号/密钥/本地存储)
  hand/           # 手势识别/屏幕标定
  hermes/         # 记忆系统 (LayeredSearch/HermesMemory)
  service/        # 服务 (悬浮窗/无障碍/Shizuku/同步)
  ui/             # Compose UI (主界面/设置/社区/聊天)
  voice/          # 语音服务
```

## 编译

```bash
./gradlew assembleRelease
```

APK 输出: `app/build/outputs/apk/release/`

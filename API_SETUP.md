# API密钥配置指南

## 配置真实API服务

要使用真实的API服务而不是模拟服务，您需要配置以下API密钥：

### 1. 编辑环境变量文件

```bash
# 编辑backend/.env文件
nano backend/.env
```

### 2. 配置API密钥

在`backend/.env`文件中，将以下占位符替换为您的真实API密钥：

```env
# OpenAI API配置
OPENAI_API_KEY=your_actual_openai_api_key_here

# ElevenLabs API配置
ELEVENLABS_API_KEY=your_actual_elevenlabs_api_key_here

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True

# 数据库配置（如果需要）
DATABASE_URL=sqlite:///./chat_history.db

# 安全配置
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### 3. 获取API密钥

#### OpenAI API密钥
1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册或登录账户
3. 进入API Keys页面
4. 创建新的API密钥
5. 复制密钥并粘贴到`.env`文件中

#### ElevenLabs API密钥
1. 访问 [ElevenLabs官网](https://elevenlabs.io/)
2. 注册或登录账户
3. 进入Profile > API Key页面
4. 复制API密钥
5. 粘贴到`.env`文件中

### 4. 重启服务

配置完成后，重启服务以应用更改：

```bash
# 停止当前服务
pkill -f "python.*main.py"

# 重新启动
./start.sh
```

### 5. 验证配置

检查服务是否使用真实API：

```bash
curl http://localhost:8000/health
```

如果配置正确，您应该看到：
```json
{
  "status": "healthy",
  "services": {
    "emotion_recognition": "real",
    "chat_service": "real",
    "voice_service": "real"
  },
  "api_keys_configured": {
    "openai": true,
    "elevenlabs": true
  }
}
```

## 功能说明

### 真实API服务功能
- **语音转文字**: 使用OpenAI Whisper进行准确的语音识别
- **情感识别**: 使用深度学习模型进行情感分析
- **智能对话**: 使用OpenAI GPT-4生成智能回应
- **文字转语音**: 使用ElevenLabs生成高质量语音

### 模拟服务功能
- **语音转文字**: 随机返回预设文本
- **情感识别**: 随机返回情感类型
- **智能对话**: 根据情感返回预设回应
- **文字转语音**: 返回模拟音频数据

## 故障排除

### 问题1: API密钥无效
- 检查API密钥是否正确复制
- 确认API密钥没有过期
- 验证账户余额是否充足

### 问题2: 服务仍显示为mock
- 确认`.env`文件在正确位置（backend/.env）
- 检查API密钥格式是否正确
- 重启服务以重新加载环境变量

### 问题3: 导入错误
- 确认所有依赖包已安装：`pip install -r requirements.txt`
- 检查Python版本兼容性
- 查看错误日志获取详细信息

## 安全注意事项

1. **不要提交API密钥到版本控制**
   - `.env`文件已添加到`.gitignore`
   - 不要在代码中硬编码API密钥

2. **定期轮换API密钥**
   - 定期更新API密钥以提高安全性
   - 监控API使用情况

3. **限制API访问**
   - 设置适当的API使用限制
   - 监控异常使用模式

## 成本估算

### OpenAI API
- Whisper语音识别: $0.006/分钟
- GPT-4对话: $0.03/1K tokens

### ElevenLabs API
- 文字转语音: $0.30/1K字符

**预估月使用成本**: $10-50（取决于使用频率） 
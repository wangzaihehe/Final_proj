# 安装指南

## 系统要求

- **Python 3.8+**
- **Node.js 18+**
- **FFmpeg** (用于音频处理)
- **麦克风权限** (用于语音输入)

## 快速安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd FinalProj
```

### 2. 配置环境变量

#### 后端配置 (backend/.env)

```bash
# 创建后端环境变量文件
cp backend/.env.example backend/.env
```

编辑 `backend/.env` 文件，填入您的API密钥：

```env
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs API配置
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

#### 前端配置 (frontend/.env.local)

```bash
# 创建前端环境变量文件
cp frontend/.env.local.example frontend/.env.local
```

编辑 `frontend/.env.local` 文件：

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 3. 安装依赖

#### 后端依赖

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 前端依赖

```bash
cd frontend
npm install
```

### 4. 启动服务

#### 方法一：使用启动脚本（推荐）

```bash
chmod +x start.sh
./start.sh
```

#### 方法二：手动启动

**启动后端：**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**启动前端：**
```bash
cd frontend
npm run dev
```

### 5. 访问应用

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## API密钥获取

### OpenAI API密钥

1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册/登录账户
3. 进入 "API Keys" 页面
4. 创建新的API密钥
5. 复制密钥到 `backend/.env` 文件

### ElevenLabs API密钥

1. 访问 [ElevenLabs官网](https://elevenlabs.io/)
2. 注册/登录账户
3. 进入 "Profile" 页面
4. 复制API密钥
5. 粘贴到 `backend/.env` 文件

## 故障排除

### 常见问题

#### 1. 麦克风权限问题

**问题**: 无法访问麦克风
**解决**: 
- 确保浏览器允许麦克风权限
- 检查系统麦克风设置
- 尝试刷新页面

#### 2. WebSocket连接失败

**问题**: 前端无法连接到后端
**解决**:
- 确保后端服务正在运行
- 检查防火墙设置
- 验证端口8000未被占用

#### 3. 依赖安装失败

**问题**: pip或npm安装失败
**解决**:
- 更新pip: `pip install --upgrade pip`
- 更新npm: `npm install -g npm@latest`
- 清除缓存: `npm cache clean --force`

#### 4. 音频处理问题

**问题**: 音频录制或播放异常
**解决**:
- 安装FFmpeg: `brew install ffmpeg` (macOS) 或 `apt install ffmpeg` (Ubuntu)
- 检查音频设备设置
- 尝试不同的浏览器

### 性能优化

#### 1. 模型优化

- 使用GPU加速（如果可用）
- 调整音频采样率
- 优化情感识别模型

#### 2. 网络优化

- 使用CDN加速
- 启用Gzip压缩
- 优化WebSocket连接

## 开发模式

### 后端开发

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
cd frontend
npm run dev
```

### 代码检查

```bash
# 后端代码检查
cd backend
flake8 app/
pylint app/

# 前端代码检查
cd frontend
npm run lint
```

## 部署

### Docker部署

```bash
# 构建镜像
docker build -t emotion-chat-app .

# 运行容器
docker run -p 3000:3000 -p 8000:8000 emotion-chat-app
```

### 生产环境部署

1. 配置生产环境变量
2. 使用生产级Web服务器（如Nginx）
3. 配置SSL证书
4. 设置数据库（如PostgreSQL）
5. 配置监控和日志

## 技术支持

如果遇到问题，请：

1. 查看 [README.md](README.md) 文档
2. 检查 [故障排除](#故障排除) 部分
3. 提交 [Issue](https://github.com/your-repo/issues)
4. 联系技术支持团队

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。 
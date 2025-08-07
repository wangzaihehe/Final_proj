#!/bin/bash

echo "🚀 情感感知语音聊天助手 - 快速设置"
echo "=================================="

# 检查系统要求
echo "📋 检查系统要求..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

echo "✅ 系统要求检查通过"

# 创建环境变量文件
echo "🔧 创建环境变量文件..."

# 后端环境变量
if [ ! -f "backend/.env" ]; then
    echo "创建 backend/.env 文件..."
    cp backend/env.example backend/.env
    echo "⚠️  请编辑 backend/.env 文件，填入您的API密钥"
else
    echo "✅ backend/.env 文件已存在"
fi

# 前端环境变量
if [ ! -f "frontend/.env.local" ]; then
    echo "创建 frontend/.env.local 文件..."
    cp frontend/env.local.example frontend/.env.local
    echo "✅ frontend/.env.local 文件已创建"
else
    echo "✅ frontend/.env.local 文件已存在"
fi

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

echo ""
echo "🎉 设置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 编辑 backend/.env 文件，填入您的API密钥："
echo "   - OPENAI_API_KEY: 从 https://platform.openai.com/ 获取"
echo "   - ELEVENLABS_API_KEY: 从 https://elevenlabs.io/ 获取"
echo ""
echo "2. 启动应用："
echo "   ./start.sh"
echo ""
echo "3. 访问应用："
echo "   - 前端: http://localhost:3000"
echo "   - 后端API: http://localhost:8000"
echo "   - API文档: http://localhost:8000/docs"
echo ""
echo "📚 更多信息请查看 README.md 和 INSTALL.md" 
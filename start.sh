#!/bin/bash

echo "启动情感感知语音聊天助手（稳定版本）..."

# 检查后端目录
if [ ! -d "backend" ]; then
    echo "错误: 找不到backend目录"
    exit 1
fi

# 检查前端目录
if [ ! -d "frontend" ]; then
    echo "错误: 找不到frontend目录"
    exit 1
fi

# 停止现有进程
echo "停止现有进程..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "next-server" 2>/dev/null

# 等待进程完全停止
sleep 2

# 启动后端（稳定版本）
echo "启动后端服务器..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

# 安装依赖
echo "安装后端依赖..."
pip install -r requirements.txt

# 启动后端
echo "启动后端服务器..."
python main.py &
BACKEND_PID=$!

cd ..

# 等待后端启动
echo "等待后端启动..."
sleep 5

# 检查后端是否启动成功
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ 后端启动成功"
        break
    else
        echo "等待后端启动... ($i/10)"
        sleep 2
    fi
done

if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ 后端启动失败"
    exit 1
fi

# 启动前端
echo "启动前端服务器..."
cd frontend

# 检查node_modules
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 启动前端
echo "启动前端开发服务器..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo "等待前端启动..."
sleep 10

# 检查前端是否启动成功
for i in {1..10}; do
    if curl -s http://localhost:3000 > /dev/null; then
        echo "✅ 前端启动成功"
        break
    else
        echo "等待前端启动... ($i/10)"
        sleep 2
    fi
done

if ! curl -s http://localhost:3000 > /dev/null; then
    echo "❌ 前端启动失败"
    exit 1
fi

echo ""
echo "🎉 应用启动成功！"
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8000"
echo "📊 健康检查: http://localhost:8000/health"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait 
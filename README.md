# 嘉禾服务 (JiaHe Service)

> 企业内部工具平台 - 打印 | AI助手 | 文档工具箱

## 功能介绍

### 🖨️ 打印服务
- 拖拽/点击上传文件
- 打印预览
- 纸张大小/类型设置
- 打印份数/单双面设置
- 打印队列管理

### 🤖 AI 助手
- 本地 Ollama (Llama 3.1) 驱动
- 支持文档/图片上传
- 对话上下文记忆
- 定时任务 (OpenClaw Cron)

### 📄 文档工具箱
- PDF → Word/Excel/PPT/TXT
- PDF 合并/分割
- PDF 压缩
- OCR 识别

## 快速部署

### 1. 安装依赖

```bash
# 后端依赖
cd server
pip install -r requirements.txt

# 前端 (可选，如需构建 React 版本)
cd client
npm install
```

### 2. 启动服务

```bash
# 启动后端 (端口 8000)
cd server
uvicorn main:app --host 0.0.0.0 --port 8000

# 启动前端 (如使用 React)
cd client
npm run dev
```

### 3. 访问服务

- 前端: http://localhost:3000 (如使用 React)
- 或直接打开 `client/index.html`
- 后端 API: http://localhost:8000

## 生产部署

### 使用 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端
    location / {
        root /path/to/jiahe-service/client;
        index index.html;
    }
    
    # 后端 API
    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### 使用 PM2 (后端)

```bash
cd server
pm2 start main:app --name jiahe-service
pm2 save
```

## 环境要求

- Python 3.8+
- Node.js 16+ (前端)
- Ollama (本地 AI)
- 4GB+ 内存

## 项目结构

```
jiahe-service/
├── client/           # 前端
│   ├── index.html   # 主页面
│   └── ...
├── server/          # 后端
│   ├── main.py     # API 服务
│   ├── requirements.txt
│   └── uploads/    # 上传文件
└── README.md
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/print/upload` | POST | 上传打印文件 |
| `/api/print/list` | GET | 获取打印队列 |
| `/api/ai/chat` | POST | AI 对话 |
| `/api/ai/upload` | POST | 上传文档 |
| `/api/pdf/convert` | POST | PDF 转换 |
| `/api/cron/add` | POST | 添加定时任务 |
| `/api/cron/list` | GET | 获取定时任务 |

## 定时任务 (OpenClaw Cron)

设置定时任务后，OpenClaw 会按 Cron 表达式自动执行任务。

示例:
- `0 9 * * *` - 每天早上 9 点
- `0 */2 * * *` - 每 2 小时

## 技术栈

- **前端**: HTML + CSS + JavaScript (可升级为 React)
- **后端**: FastAPI (Python)
- **AI**: Ollama (Llama 3.1)
- **数据库**: SQLite (可选)

## License

MIT

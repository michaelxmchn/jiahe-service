# 嘉禾服务后端 API

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import asyncio
from datetime import datetime

app = FastAPI(title="嘉禾服务 API")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 上传目录
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==================== 打印服务 ====================

@app.post("/api/print/upload")
async def upload_print_file(file: UploadFile = File(...)):
    """上传打印文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"success": True, "filename": filename, "size": len(content)}

@app.get("/api/print/list")
async def list_print_files():
    """获取打印队列"""
    files = []
    for f in os.listdir(UPLOAD_DIR):
        filepath = os.path.join(UPLOAD_DIR, f)
        if os.path.isfile(filepath):
            files.append({
                "name": f,
                "size": os.path.getsize(filepath),
                "created": datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
            })
    return files

# ==================== AI 助手 ====================

@app.post("/api/ai/chat")
async def chat_with_ai(message: str = Form(...), context: str = Form(None)):
    """与 Ollama AI 对话"""
    import requests
    
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.1:8b",
        "prompt": f"{context}\n\nUser: {message}" if context else message,
        "stream": False
    }
    
    try:
        response = requests.post(ollama_url, json=payload, timeout=120)
        result = response.json()
        return {"success": True, "response": result.get("response", "")}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/ai/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传文档给 AI 分析"""
    content = await file.read()
    # 保存文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(content)
    
    return {"success": True, "filename": filename, "size": len(content)}

# ==================== 文档工具箱 ====================

@app.post("/api/pdf/convert")
async def convert_pdf(file: UploadFile = File(...), target_format: str = Form(...)):
    """PDF 转换"""
    # TODO: 实现 PDF 转换逻辑
    return {"success": True, "message": f"转换功能开发中，目标格式: {target_format}"}

@app.post("/api/pdf/merge")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    """合并 PDF"""
    return {"success": True, "message": "合并功能开发中"}

# ==================== 定时任务 ====================

@app.post("/api/cron/add")
async def add_cron_task(task: str = Form(...), schedule: str = Form(...)):
    """添加定时任务"""
    # TODO: 集成 OpenClaw Cron
    return {"success": True, "task": task, "schedule": schedule}

@app.get("/api/cron/list")
async def list_cron_tasks():
    """列出定时任务"""
    return {"success": True, "tasks": []}

# ==================== 基础接口 ====================

@app.get("/")
async def root():
    return {"message": "嘉禾服务 API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}

"""
AI自动化审批流Web原型（FastAPI + Jinja2）
- 支持审批流配置、请求发起、审批进度查看、流程图展示
- 适合Python初学者
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, json
from graph import run_approval_workflow, export_mermaid

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(BASE_DIR, 'data')
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name="static")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # 展示审批请求列表
    with open(os.path.join(data_dir, 'requests.json'), 'r', encoding='utf-8') as f:
        requests = json.load(f)
    with open(os.path.join(data_dir, 'history.json'), 'r', encoding='utf-8') as f:
        history = json.load(f)
    return templates.TemplateResponse("index.html", {"request": request, "requests": requests, "history": history})

@app.get("/new", response_class=HTMLResponse)
def new_request(request: Request):
    return templates.TemplateResponse("new.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
def submit_request(request: Request, user: str = Form(...), amount: float = Form(...), reason: str = Form(...), urgent: bool = Form(False)):
    # 新增审批请求
    with open(os.path.join(data_dir, 'requests.json'), 'r', encoding='utf-8') as f:
        requests = json.load(f)
    req_id = f"REQ{len(requests)+1:03d}"
    new_req = {"request_id": req_id, "user": user, "amount": amount, "reason": reason, "urgent": urgent}
    requests.append(new_req)
    with open(os.path.join(data_dir, 'requests.json'), 'w', encoding='utf-8') as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)
    # 自动流转
    run_approval_workflow(init_state=new_req)
    return RedirectResponse(url="/", status_code=302)

@app.get("/flow", response_class=HTMLResponse)
def flow_diagram(request: Request):
    export_mermaid()
    with open(os.path.join(BASE_DIR, 'approval_flow.mmd'), 'r', encoding='utf-8') as f:
        mermaid_code = f.read()
    return templates.TemplateResponse("flow.html", {"request": request, "mermaid_code": mermaid_code}) 
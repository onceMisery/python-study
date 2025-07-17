"""
AI自动化审批流Web原型（FastAPI + Jinja2）
- 支持审批流配置、请求发起、审批进度查看、流程图展示
- 适合Python初学者
"""
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, json
from ..graph import run_approval_workflow, export_mermaid
from ..llm_provider import get_llm

# 简单模拟登录（实际可用session/cookie）
USERS = ["王主管", "李会计", "赵总"]

# 多租户/业务线配置
TENANTS = ["default", "marketing", "finance"]

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(BASE_DIR, 'data')
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, tenant: str = "default"):
    # 展示审批请求列表（按租户）
    req_path = os.path.join(data_dir, f'requests_{tenant}.json')
    hist_path = os.path.join(data_dir, f'history_{tenant}.json')
    if not os.path.exists(req_path):
        with open(req_path, 'w', encoding='utf-8') as f: json.dump([], f)
    if not os.path.exists(hist_path):
        with open(hist_path, 'w', encoding='utf-8') as f: json.dump([], f)
    with open(req_path, 'r', encoding='utf-8') as f:
        requests = json.load(f)
    with open(hist_path, 'r', encoding='utf-8') as f:
        history = json.load(f)
    return templates.TemplateResponse("index.html",
                                      {"request": request, "requests": requests, "history": history, "tenant": tenant,
                                       "tenants": TENANTS})


@app.get("/new", response_class=HTMLResponse)
def new_request(request: Request, tenant: str = "default"):
    return templates.TemplateResponse("new.html", {"request": request, "tenant": tenant, "tenants": TENANTS})


@app.post("/submit", response_class=HTMLResponse)
def submit_request(request: Request, user: str = Form(...), amount: float = Form(...), reason: str = Form(...),
                   urgent: bool = Form(False), tenant: str = Form("default")):
    req_path = os.path.join(data_dir, f'requests_{tenant}.json')
    with open(req_path, 'r', encoding='utf-8') as f:
        requests = json.load(f)
    req_id = f"REQ{len(requests) + 1:03d}"
    new_req = {"request_id": req_id, "user": user, "amount": amount, "reason": reason, "urgent": urgent}
    requests.append(new_req)
    with open(req_path, 'w', encoding='utf-8') as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)
    run_approval_workflow(init_state=new_req)
    return RedirectResponse(url=f"/?tenant={tenant}", status_code=302)


@app.get("/flow", response_class=HTMLResponse)
def flow_diagram(request: Request):
    export_mermaid()
    with open(os.path.join(BASE_DIR, 'approval_flow.mmd'), 'r', encoding='utf-8') as f:
        mermaid_code = f.read()
    return templates.TemplateResponse("flow.html", {"request": request, "mermaid_code": mermaid_code})


@app.get("/edit_flow", response_class=HTMLResponse)
def edit_flow(request: Request, tenant: str = "default"):
    flow_path = os.path.join(data_dir, f'flow_{tenant}.json')
    if not os.path.exists(flow_path):
        flow_path = os.path.join(data_dir, 'flow.json')
    with open(flow_path, 'r', encoding='utf-8') as f:
        flow_code = f.read()
    return templates.TemplateResponse("edit_flow.html", {"request": request, "flow_code": flow_code, "tenant": tenant,
                                                         "tenants": TENANTS})


@app.post("/save_flow", response_class=HTMLResponse)
def save_flow(request: Request, flow_code: str = Form(...), tenant: str = Form("default")):
    flow_path = os.path.join(data_dir, f'flow_{tenant}.json')
    with open(flow_path, 'w', encoding='utf-8') as f:
        f.write(flow_code)
    return RedirectResponse(url=f"/edit_flow?tenant={tenant}", status_code=302)


@app.post("/upload_flow", response_class=HTMLResponse)
def upload_flow(request: Request, file: UploadFile, tenant: str = Form("default")):
    flow_path = os.path.join(data_dir, f'flow_{tenant}.json')
    with open(flow_path, 'wb') as f:
        f.write(file.file.read())
    return RedirectResponse(url=f"/edit_flow?tenant={tenant}", status_code=302)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "users": USERS})


@app.post("/login", response_class=HTMLResponse)
def do_login(request: Request, user: str = Form(...)):
    response = RedirectResponse(url=f"/todo?user={user}", status_code=302)
    return response


@app.get("/todo", response_class=HTMLResponse)
def todo_list(request: Request, user: str):
    # 展示待办审批（简单模拟：所有未审批的请求）
    with open(os.path.join(data_dir, 'requests.json'), 'r', encoding='utf-8') as f:
        requests = json.load(f)
    with open(os.path.join(data_dir, 'history.json'), 'r', encoding='utf-8') as f:
        history = json.load(f)
    done_ids = {h['request_id'] for h in history}
    todo = [r for r in requests if r['request_id'] not in done_ids]
    return templates.TemplateResponse("todo.html", {"request": request, "user": user, "todo": todo})


@app.get("/approve/{req_id}", response_class=HTMLResponse)
def approve_page(request: Request, req_id: str, user: str, tenant: str = "default"):
    # 展示审批表单，支持AI自动意见
    with open(os.path.join(data_dir, f'requests_{tenant}.json'), 'r', encoding='utf-8') as f:
        requests = json.load(f)
    req = next((r for r in requests if r['request_id'] == req_id), None)
    ai_comment = ""
    if req:
        # AI自动生成意见，支持DeepSeek
        llm = get_llm(tenant)
        ai_comment = llm(
            f"请为如下审批请求生成简明审批意见：用户：{req['user']}，金额：{req['amount']}，事由：{req['reason']}，紧急：{req['urgent']}")
    return templates.TemplateResponse("approve.html",
                                      {"request": request, "user": user, "req": req, "ai_comment": ai_comment,
                                       "tenant": tenant})


@app.post("/approve/{req_id}", response_class=HTMLResponse)
def do_approve(request: Request, req_id: str, user: str = Form(...), approve: str = Form(...),
               comment: str = Form(...)):
    # 写入审批历史
    with open(os.path.join(data_dir, 'history.json'), 'r', encoding='utf-8') as f:
        history = json.load(f)
    with open(os.path.join(data_dir, 'requests.json'), 'r', encoding='utf-8') as f:
        requests = json.load(f)
    req = next((r for r in requests if r['request_id'] == req_id), None)
    record = dict(req) if req else {"request_id": req_id}
    record['approver'] = user
    record['approved'] = (approve == 'yes')
    record['comment'] = comment
    history.append(record)
    with open(os.path.join(data_dir, 'history.json'), 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return RedirectResponse(url=f"/todo?user={user}", status_code=302)

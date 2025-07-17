from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, Any, List
import os
import json
from flow_engine import FlowEngine
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI(title="智能审批流API", description="支持AI风险评估与智能分流的审批流API服务")

# 初始化审批流引擎
engine = FlowEngine()

class FlowRequest(BaseModel):
    instance_id: str
    context: Dict[str, Any]

@app.post("/run_flow", summary="发起审批流实例并返回AI分流结果")
def run_flow(req: FlowRequest):
    """
    发起审批流实例，自动执行AI风险评估与分流，返回trace与AI建议。
    """
    try:
        result = engine.run(instance_id=req.instance_id, context=req.context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/risk_results", summary="查询AI风险评估历史")
def get_risk_results() -> List[Dict[str, Any]]:
    """
    查询所有AI风险评估历史记录。
    """
    return engine.risk_results

@app.get("/trace/{instance_id}", summary="查询审批流trace")
def get_trace(instance_id: str):
    """
    查询指定实例的审批流trace与AI评估结果。
    """
    # 简单遍历risk_results，查找对应instance_id
    traces = [r for r in engine.risk_results if r.get("instance_id") == instance_id]
    if not traces:
        raise HTTPException(status_code=404, detail="未找到该实例的AI评估记录")
    return {"instance_id": instance_id, "risk_results": traces}

# Jinja2模板目录
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'web', 'templates'))

@app.get("/web/result/{instance_id}", response_class=HTMLResponse, summary="审批流执行结果展示")
def web_result(instance_id: str, request: Request):
    # 查找最新AI评估结果
    result = None
    for r in reversed(engine.risk_results):
        if r.get("instance_id") == instance_id:
            # 构造一个简化的result结构
            result = {
                "instance_id": instance_id,
                "final_node": r.get("node_id"),
                "final_approver": r.get("recommend_path"),
                "ai_suggestion": r.get("suggestion"),
                "trace": [
                    {"node_id": "start", "type": "start"},
                    {"node_id": "risk_eval_1", "type": "risk_eval"},
                    {"node_id": "branch_1", "type": "branch"},
                    {"node_id": r.get("recommend_path", "approve"), "type": "approve"},
                    {"node_id": "end", "type": "end"}
                ],
                "ai_risk_result": r
            }
            break
    if not result:
        return HTMLResponse("未找到该实例的审批流结果", status_code=404)
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

@app.get("/web/risk_history", response_class=HTMLResponse, summary="AI风险评估历史页面")
def web_risk_history(request: Request):
    return templates.TemplateResponse("risk_history.html", {"request": request, "risk_results": engine.risk_results})

@app.get("/web/trace/{instance_id}", response_class=HTMLResponse, summary="审批流trace与AI详情页面")
def web_trace(instance_id: str, request: Request):
    traces = [r for r in engine.risk_results if r.get("instance_id") == instance_id]
    if not traces:
        return HTMLResponse("未找到该实例的AI评估记录", status_code=404)
    return templates.TemplateResponse("trace.html", {"request": request, "instance_id": instance_id, "risk_results": traces})

FLOW_JSON_PATH = os.path.join(os.path.dirname(__file__), 'data', 'flow.json')

@app.get("/api/flow_dsl", summary="获取当前审批流DSL")
def get_flow_dsl():
    """
    获取当前审批流DSL（flow.json）。
    """
    if not os.path.exists(FLOW_JSON_PATH):
        return {"nodes": []}
    with open(FLOW_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.post("/api/flow_dsl", summary="保存审批流DSL")
def save_flow_dsl(dsl: dict = Body(...)):
    """
    保存审批流DSL到flow.json，实时生效。
    """
    with open(FLOW_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(dsl, f, ensure_ascii=False, indent=2)
    # 可选：重载审批流引擎
    engine.flow = dsl
    return {"success": True, "msg": "DSL已保存并生效"}

# 启动命令：uvicorn api:app --reload --port 8000 
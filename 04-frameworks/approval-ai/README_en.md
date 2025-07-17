# Advanced Approval Flow Features: AI Risk Assessment & Intelligent Routing

## 1. Overview

This module implements AI-powered risk assessment and intelligent routing in approval flows. At branch nodes, the DeepSeek LLM is invoked for risk evaluation, automatically recommending approval paths and routing to different approvers/nodes. Approvers can refer to AI risk suggestions for decision-making, enhancing automation and intelligence.

---

## 2. DSL (flow.json) Design

- Supported node types: start, approve, risk_eval, branch, merge, end
- risk_eval node: Automatically calls the LLM for risk assessment, outputs risk level (high/medium/low) and recommended path
- branch node: Routes based on AI assessment results
- Node attributes support approver, branch conditions, AI parameters, etc.
- Supports multi-branch, concurrency, merge
- Default LLM provider: DeepSeek

### Example: flow.json

```json
{
  "flow_id": "expense_approval_v2",
  "name": "Expense Approval Flow (AI Intelligent Routing)",
  "version": "2.0",
  "description": "Expense approval flow with integrated AI risk assessment and intelligent routing. Default LLM: DeepSeek.",
  "nodes": [
    { "id": "start", "type": "start", "next": "risk_eval_1" },
    { "id": "risk_eval_1", "type": "risk_eval", "name": "AI Risk Assessment", "params": { "fields": ["amount", "urgency", "applicant_history"], "llm_provider": "deepseek" }, "next": "branch_1" },
    { "id": "branch_1", "type": "branch", "name": "AI Routing", "branches": [ { "condition": "risk == 'high'", "next": "approve_manager" }, { "condition": "risk == 'medium'", "next": "approve_finance" }, { "condition": "risk == 'low'", "next": "approve_auto" } ] },
    { "id": "approve_manager", "type": "approve", "name": "Manager Approval", "approver": "manager", "next": "end" },
    { "id": "approve_finance", "type": "approve", "name": "Finance Approval", "approver": "finance", "next": "end" },
    { "id": "approve_auto", "type": "approve", "name": "Auto Approve", "approver": "system", "next": "end" },
    { "id": "end", "type": "end" }
  ]
}
```

---

## 3. Node Types

- **start**: Flow entry point
- **risk_eval**: AI risk assessment node, calls DeepSeek LLM, outputs risk level and recommended path
- **branch**: Branch node, routes based on AI output (e.g., risk)
- **approve**: Manual or automatic approval node
- **end**: Flow end

---

## 4. Data Structure

- flow.json: Approval flow DSL config, supports risk_eval node and AI routing
- risk_result.json: AI assessment result cache/history
- approval_history.db: Approval flow history

---

## 5. Usage

1. Configure `data/flow.json` to define the approval flow structure and AI routing logic
2. When the flow reaches a risk_eval node, DeepSeek LLM is automatically called for risk assessment
3. AI outputs risk level (high/medium/low) and recommended path; branch node routes to different approvers/nodes accordingly
4. Assessment results are written to risk_result.json and approval history
5. Approvers can refer to AI risk suggestions for decision-making

---

## 6. Next Steps

- Implement ai_risk_evaluator.py with DeepSeek LLM integration
- Integrate AI routing logic in flow_engine.py
- FastAPI API and frontend display
- Support multi-tenant/multi-business, flow visualization 

---

## 7. AI Risk Assessment Core Code (ai_risk_evaluator.py)

- Encapsulates the main AI risk assessment process, defaulting to DeepSeek LLM
- Supports input of business context (amount, urgency, applicant history, etc.)
- Outputs risk level, recommended path, and suggestion
- Easy to integrate with the approval flow engine

### Example Usage

```python
from ai_risk_evaluator import AIRiskEvaluator

evaluator = AIRiskEvaluator()
context = {
    "amount": 12000,
    "urgency": "high",
    "applicant_history": "one violation record"
}
result = evaluator.evaluate(context)
print(result)
```

--- 

---

## 8. Approval Flow Engine Core Code (flow_engine.py)

- Responsible for parsing flow.json and executing the main approval flow
- Supports risk_eval nodes to automatically call AI risk assessment (DeepSeek), results are written to context and persisted
- Branch nodes intelligently route based on AI results, supporting multiple branches
- Full process trace for easy debugging and audit
- Easy to integrate with Web/API

### Main Methods
- `run(instance_id, context)`: Executes the main approval flow, automatically handling AI risk assessment and routing
- `save_risk_result(result)`: Persists AI assessment results

### Example Usage

```python
from flow_engine import FlowEngine

engine = FlowEngine()
context = {
    "amount": 12000,
    "urgency": "high",
    "applicant_history": "one violation record"
}
result = engine.run(instance_id="exp20240601-003", context=context)
print(result)
```

### Typical Flow
1. Parse flow.json and locate the start node
2. Execute risk_eval node, automatically call AI risk assessment, write results to context
3. Branch node routes to different approvers/nodes based on AI results
4. Approval flow trace and AI suggestions are available for approvers to reference

--- 

---

## 9. FastAPI API Documentation (api.py)

### 1. Run Approval Flow Instance
- **POST /run_flow**
- **Parameters:**
  - `instance_id` (string): Flow instance ID
  - `context` (dict): Business context (e.g., amount, urgency, applicant_history, etc.)
- **Request Example:**
```json
{
  "instance_id": "exp20240601-004",
  "context": {
    "amount": 5000,
    "urgency": "medium",
    "applicant_history": "no abnormality"
  }
}
```
- **Response Example:**
```json
{
  "success": true,
  "data": {
    "instance_id": "exp20240601-004",
    "trace": [
      {"node_id": "start", "type": "start"},
      {"node_id": "risk_eval_1", "type": "risk_eval"},
      {"node_id": "branch_1", "type": "branch"},
      {"node_id": "approve_finance", "type": "approve"},
      {"node_id": "end", "type": "end"}
    ],
    "ai_risk_result": {
      "llm_provider": "deepseek",
      "amount": 5000,
      "urgency": "medium",
      "applicant_history": "no abnormality",
      "risk": "medium",
      "recommend_path": "Finance Approval",
      "suggestion": "Amount is moderate, recommend finance approval.",
      "instance_id": "exp20240601-004",
      "flow_id": "expense_approval_v2",
      "node_id": "risk_eval_1"
    },
    "final_node": "end",
    "final_approver": "Finance Approval",
    "ai_suggestion": "Amount is moderate, recommend finance approval."
  }
}
```

### 2. Query AI Risk Assessment History
- **GET /risk_results**
- **Returns:** All AI risk assessment history records (array)

### 3. Query Approval Flow Trace
- **GET /trace/{instance_id}**
- **Returns:** AI assessment and trace for the specified instance

---

### Start API Service
```bash
uvicorn api:app --reload --port 8000
```

--- 
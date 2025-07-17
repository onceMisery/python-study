# 智能审批流进阶功能设计（AI风险评估/智能分流）

## 一、功能概述

本模块实现审批流AI风险评估与智能分流，支持在审批流分支节点调用DeepSeek大模型进行风险评估，自动推荐审批路径并分流到不同审批人/节点。审批人可参考AI风险提示做决策，提升自动化与智能化水平。

---

## 二、DSL（flow.json）设计

- 支持节点类型：start、approve、risk_eval、branch、merge、end
- risk_eval节点：自动调用AI进行风险评估，输出risk等级（高/中/低）和推荐路径
- branch节点：可根据AI评估结果分流
- 节点属性支持审批人、分支条件、AI参数等
- 支持多分支、并发、合并
- 默认大模型为DeepSeek

### 示例：flow.json

```json
{
  "flow_id": "expense_approval_v2",
  "name": "费用报销审批流（AI智能分流）",
  "version": "2.0",
  "description": "集成AI风险评估与智能分流的费用报销审批流，默认大模型为DeepSeek。",
  "nodes": [
    { "id": "start", "type": "start", "next": "risk_eval_1" },
    { "id": "risk_eval_1", "type": "risk_eval", "name": "AI风险评估", "params": { "fields": ["amount", "urgency", "applicant_history"], "llm_provider": "deepseek" }, "next": "branch_1" },
    { "id": "branch_1", "type": "branch", "name": "AI分流", "branches": [ { "condition": "risk == '高'", "next": "approve_manager" }, { "condition": "risk == '中'", "next": "approve_finance" }, { "condition": "risk == '低'", "next": "approve_auto" } ] },
    { "id": "approve_manager", "type": "approve", "name": "经理审批", "approver": "manager", "next": "end" },
    { "id": "approve_finance", "type": "approve", "name": "财务审批", "approver": "finance", "next": "end" },
    { "id": "approve_auto", "type": "approve", "name": "自动通过", "approver": "system", "next": "end" },
    { "id": "end", "type": "end" }
  ]
}
```

---

## 三、节点类型说明

- **start**：流程起点
- **risk_eval**：AI风险评估节点，自动调用DeepSeek LLM，输出risk等级和推荐路径
- **branch**：分支节点，根据risk等AI输出分流
- **approve**：人工或自动审批节点
- **end**：流程终点

---

## 四、数据结构

- flow.json：审批流DSL配置，支持risk_eval节点与AI分流
- risk_result.json：AI评估结果缓存与历史
- approval_history.db：审批流历史记录

---

## 五、使用说明

1. 配置`data/flow.json`，定义审批流结构与AI分流逻辑
2. 审批流运行到risk_eval节点时，自动调用DeepSeek大模型进行风险评估
3. AI输出risk等级（高/中/低）和推荐路径，branch节点根据risk分流到不同审批人/节点
4. 评估结果写入risk_result.json和审批历史
5. 审批人可参考AI风险提示做决策

---

## 六、后续开发计划

- 封装ai_risk_evaluator.py，集成DeepSeek LLM
- flow_engine.py集成AI分流逻辑
- FastAPI接口与前端展示
- 支持多租户/多业务线、审批流可视化 

---

## 七、AI风险评估核心代码说明（ai_risk_evaluator.py）

- 封装了AI风险评估主流程，默认调用DeepSeek大模型
- 支持输入业务上下文（如金额、紧急程度、申请人历史）
- 输出风险等级、推荐路径和建议
- 便于与审批流引擎集成

### 用法示例

```python
from ai_risk_evaluator import AIRiskEvaluator

evaluator = AIRiskEvaluator()
context = {
    "amount": 12000,
    "urgency": "高",
    "applicant_history": "有一次违规记录"
}
result = evaluator.evaluate(context)
print(result)
```

--- 

---

## 八、审批流引擎核心代码说明（flow_engine.py）

- 负责解析flow.json，自动执行审批流主流程
- 支持risk_eval节点自动调用AI风险评估（DeepSeek），结果写入context并持久化
- branch节点根据AI结果智能分流，支持多分支
- 全流程trace记录，便于追溯与调试
- 便于与Web/API集成

### 主要方法
- `run(instance_id, context)`：执行审批流主流程，自动处理AI风险评估与分流
- `save_risk_result(result)`：持久化AI评估结果

### 用法示例

```python
from flow_engine import FlowEngine

engine = FlowEngine()
context = {
    "amount": 12000,
    "urgency": "高",
    "applicant_history": "有一次违规记录"
}
result = engine.run(instance_id="exp20240601-003", context=context)
print(result)
```

### 典型流程
1. 解析flow.json，定位start节点
2. 执行risk_eval节点，自动调用AI风险评估，结果写入context
3. branch节点根据AI结果分流到不同审批人/节点
4. 审批流trace与AI建议可供审批人参考

--- 

---

## 九、FastAPI接口文档（api.py）

### 1. 发起审批流实例
- **POST /run_flow**
- **参数**：
  - `instance_id`（string）：流程实例ID
  - `context`（dict）：业务上下文（如amount, urgency, applicant_history等）
- **请求示例**：
```json
{
  "instance_id": "exp20240601-004",
  "context": {
    "amount": 5000,
    "urgency": "中",
    "applicant_history": "无异常"
  }
}
```
- **返回示例**：
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
      "urgency": "中",
      "applicant_history": "无异常",
      "risk": "中",
      "recommend_path": "财务审批",
      "suggestion": "金额适中，建议财务审批。",
      "instance_id": "exp20240601-004",
      "flow_id": "expense_approval_v2",
      "node_id": "risk_eval_1"
    },
    "final_node": "end",
    "final_approver": "财务审批",
    "ai_suggestion": "金额适中，建议财务审批。"
  }
}
```

### 2. 查询AI风险评估历史
- **GET /risk_results**
- **返回**：所有AI风险评估历史记录（数组）

### 3. 查询审批流trace
- **GET /trace/{instance_id}**
- **返回**：指定实例的AI评估与trace

---

### 启动API服务
```bash
uvicorn api:app --reload --port 8000
```

--- 

---

## 十、审批流配置可视化设计器

- 基于React+ReactFlow实现拖拽式审批流配置，支持节点、分支、审批人等可视化编辑
- 支持DSL导入导出，Mermaid流程图一键预览
- 访问 `/web/edit_flow` 进入设计器页面
- 后续将完善拖拽交互、属性弹窗、DSL与ReactFlow互转、流程图联动等

--- 

---

## 十一、前后端联动与开发部署说明

### 1. 审批流DSL相关API
- `GET /api/flow_dsl`：获取当前审批流DSL（flow.json）
- `POST /api/flow_dsl`：保存DSL到flow.json，实时生效

### 2. 前端开发
- 进入 `web/designer/` 目录，使用 `npm install && npm run build` 构建前端
- 构建产物可集成到FastAPI静态目录
- 设计器页面可通过API自动加载/保存DSL

### 3. 后端开发
- FastAPI自动加载/保存flow.json，支持API与前端联动
- 支持审批流配置实时生效

### 4. 一体化体验
- 访问 `/web/edit_flow` 进行可视化配置
- 访问 `/web/result/{instance_id}` 查看审批流执行与AI分流结果

--- 

---

## 十二、企业级扩展与最佳实践

### 1. 多租户/多业务线支持
- 流程配置、审批人、AI参数等按租户/业务线隔离，数据物理或逻辑分表
- DSL文件可按租户/业务线命名（如 flow_{tenant}_{biz}.json）
- API接口增加租户/业务线参数，前端支持切换
- 推荐：统一租户认证与权限体系，支持SaaS化部署

### 2. 权限与安全控制
- 审批流配置、执行、查询等操作需鉴权（如JWT、OAuth2）
- 细粒度权限：流程编辑、审批、只读、运维等角色分离
- 审批人、管理员、租户管理员等多级权限
- API接口防护：限流、审计、敏感操作告警

### 3. 配置变更历史与回滚
- 审批流DSL每次变更自动存档（如flow_history/flow_{tenant}_{biz}_20240601.json）
- 支持变更记录查询、对比、回滚
- 推荐：引入版本号、变更人、变更说明等元数据

### 4. 流程图美化与导出
- ReactFlow/mermaid支持自定义节点样式、icon、颜色
- 支持流程图导出SVG/PNG，便于文档归档与汇报
- 推荐：流程图与审批流DSL双向同步，保证一致性

### 5. 企业级监控与告警
- 审批流执行、AI节点异常、API调用等接入监控（如Prometheus、ELK）
- 支持自定义告警规则（如审批超时、AI评估失败、配置变更等）
- 关键操作、异常、告警写入日志，便于审计与追溯

### 6. 代码可维护性与扩展性
- 采用分层架构，核心引擎、AI评估、Web前端、API解耦
- 关键逻辑单元测试、集成测试覆盖
- 代码注释、文档齐全，便于团队协作
- 推荐：CI/CD自动化部署，灰度发布、回滚机制

---

## 推荐最佳实践
- 以DSL驱动流程，前后端解耦，便于灵活扩展
- 关键节点/分支支持AI与规则混合决策，提升智能化水平
- 配置、数据、日志、监控、权限等均支持多租户隔离
- 重要操作留痕、可回溯，保障合规与安全
- 持续关注AI模型能力与合规性，支持灵活切换与升级

--- 
# 智能审批流平台详细文档

## 一、项目简介

本项目基于LangChain/LangGraph、DeepSeek大模型，打造企业级AI驱动的智能审批流平台。支持多轮对话、RAG知识库、AI风险评估、智能分流、可视化流程配置、Web管理、API集成、企业级多租户与安全扩展，适用于自动化审批、智能客服、业务流转等场景。

---

## 二、技术架构与选型

- **后端**：Python 3.10+，FastAPI，LangChain/LangGraph，DeepSeek/OpenAI LLM
- **前端**：React 18+，ReactFlow，Mermaid，Jinja2（原型）
- **数据库**：MySQL/SQLite（审批历史、用户、租户等）
- **存储**：JSON（DSL、风险评估、历史）、本地或对象存储
- **监控**：Prometheus、ELK、日志
- **部署**：Docker、CI/CD、K8s可选

---

## 三、主要功能与业务流程

1. **审批流DSL配置**：支持start、approve、risk_eval、branch、merge、end等节点，AI分流与规则分支灵活组合
2. **AI风险评估/智能分流**：DeepSeek大模型自动评估风险，推荐审批路径，分流到不同审批人/节点
3. **审批流引擎**：自动执行DSL流程，trace全程记录，支持API/Web触发
4. **Web可视化设计器**：ReactFlow拖拽式流程配置，节点属性弹窗，DSL导入导出，Mermaid流程图预览
5. **多租户/多业务线**：流程、数据、权限隔离，支持SaaS化
6. **权限与安全**：统一认证、细粒度授权、API安全
7. **配置变更历史与回滚**：DSL自动存档，支持历史对比、回滚
8. **监控与告警**：审批流执行、AI异常、API调用等全链路监控
9. **流程图美化与导出**：自定义节点样式，支持SVG/PNG导出

---

## 四、代码结构与目录说明

```
04-frameworks/approval-ai/
  ai_risk_evaluator.py         # AI风险评估核心
  flow_engine.py               # 审批流引擎
  api.py                       # FastAPI接口与Web集成
  data/
    flow.json                  # 审批流DSL配置
    risk_result.json           # AI风险评估历史
    flow_history/              # DSL变更历史
  web/
    templates/                 # Jinja2页面
      result.html
      risk_history.html
      trace.html
      edit_flow.html
    static/                    # 样式与JS
      style.css
      main.js
      reactflow/
      mermaid/
    designer/                  # React+ReactFlow设计器
      App.jsx
      FlowEditor.jsx
      NodeConfigModal.jsx
      dslUtils.js
      mermaidPreview.jsx
      README.md
  README.md                    # 总体说明与最佳实践
```

---

## 五、关键模块详细设计

### 1. 审批流DSL（flow.json）
- 支持节点类型：start、approve、risk_eval、branch、merge、end
- risk_eval节点自动调用AI，输出risk等级、推荐路径
- branch节点支持多分支，条件可用AI结果
- 支持多租户/多业务线（如flow_tenantA_biz1.json）

### 2. AI风险评估（ai_risk_evaluator.py）
- 封装DeepSeek LLM调用，输入业务上下文，输出风险等级、建议
- 支持多模型切换、参数灵活配置

### 3. 审批流引擎（flow_engine.py）
- 解析DSL，自动执行流程，支持AI分流
- trace全程记录，便于追溯与调试
- 支持API/Web触发

### 4. Web可视化设计器（designer/）
- React+ReactFlow拖拽式编辑，节点属性弹窗
- DSL导入导出，Mermaid流程图预览
- 支持多租户/多业务线切换、权限控制

### 5. FastAPI接口（api.py）
- 审批流执行、AI评估历史、trace查询
- DSL获取/保存、流程图生成
- 支持JWT/OAuth2鉴权、API限流

---

## 六、前后端交互与API说明

### 1. 审批流API
- `POST /run_flow`：发起审批流实例，返回AI分流结果
- `GET /risk_results`：查询AI风险评估历史
- `GET /trace/{instance_id}`：查询审批流trace
- `GET /api/flow_dsl`：获取当前DSL（支持多租户/业务线参数）
- `POST /api/flow_dsl`：保存DSL，实时生效

### 2. 前端API联动
- 设计器页面自动加载/保存DSL，支持多租户/多业务线切换
- 所有API请求带token，支持权限校验

---

## 七、企业级扩展与最佳实践

### 1. 多租户/多业务线
- 流程、数据、权限隔离，API/前端全链路支持
- SaaS化部署，统一认证与授权

### 2. 权限与安全
- 统一认证（JWT/OAuth2）、细粒度角色权限
- API限流、审计、敏感操作告警

### 3. 配置变更历史与回滚
- DSL变更自动存档，支持历史对比、回滚
- 版本号、变更人、变更说明等元数据

### 4. 流程图美化与导出
- ReactFlow/mermaid自定义节点样式、icon、颜色
- 支持SVG/PNG导出

### 5. 企业级监控与告警
- 审批流执行、AI节点异常、API调用等接入监控
- 支持自定义告警规则，关键操作日志审计

### 6. 代码可维护性与扩展性
- 分层架构、单元测试、CI/CD自动化、灰度发布
- 代码注释、文档齐全，便于团队协作

---

## 八、部署与运维建议

- 推荐Docker/K8s部署，支持多环境隔离
- CI/CD自动化，支持灰度发布与回滚
- 日志、监控、告警全链路覆盖
- 数据、配置、模型等定期备份

---

## 九、团队协作与最佳实践

- 以DSL驱动流程，前后端解耦，便于灵活扩展
- 关键节点/分支支持AI与规则混合决策
- 配置、数据、日志、监控、权限等均支持多租户隔离
- 重要操作留痕、可回溯，保障合规与安全
- 持续关注AI模型能力与合规性，支持灵活切换与升级

---

如需更详细的某一模块设计、API文档、前端用法、企业落地方案或PPT/Markdown模板，请随时指定！ 
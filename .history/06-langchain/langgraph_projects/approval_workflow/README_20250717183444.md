# AI自动化审批流（LangChain + LangGraph 实战项目）

## 项目简介
本项目基于 LangChain 和 LangGraph，构建一个支持多级审批、条件分支、自动化决策、异步通知的AI自动化审批流系统。适合Python初学者和企业AI开发者学习与实践。

## 核心功能
- 多级审批（如部门主管、财务、总经理）
- 条件分支（如金额大小、紧急程度自动分流）
- 审批意见收集与自动化决策
- 异步通知与外部系统集成（可模拟）
- 审批历史与状态持久化
- 异常处理与兜底

## 目录结构
```
approval_workflow/
  main.py              # 启动入口，集成所有流程
  graph.py             # LangGraph审批流定义
  nodes.py             # 各类审批节点与业务逻辑
  integrations.py      # 外部系统集成（如邮件、消息推送等）
  data/
    requests.json      # 审批请求示例数据
    history.json       # 审批历史与状态
  README.md            # 项目说明文档
```

## 环境准备
1. 推荐使用虚拟环境
2. 安装依赖：
   ```bash
   pip install langgraph langchain openai
   ```
3. 注册OpenAI账号，获取API Key
4. 设置环境变量：
   ```bash
   export OPENAI_API_KEY=你的key  # Windows下用 set OPENAI_API_KEY=你的key
   ```

## 批量审批与历史查询
- 支持从 data/requests.json 批量读取多个审批请求，自动流转并写入 data/history.json
- 每次审批流程结束后，自动将结果写入审批历史
- 支持通过请求ID查询历史审批结果

运行方法：
```bash
python main.py
# 按提示选择 1 批量审批，2 查询历史，3 单条演示
```

## 审批规则自定义与并发审批
- 支持通过 data/rules.json 配置金额阈值、审批人、审批流分支等
- 支持紧急大额请求并发会签（财务+总经理）
- 支持动态审批人配置

## 审批流可视化
- 运行过程中自动导出Mermaid流程图 approval_flow.mmd
- 可用 mermaid.live 等工具在线可视化

## API集成与监控告警
- 支持审批节点自动推送邮件、ERP系统更新、异常自动告警（可扩展为真实API）
- 节点异常时自动触发告警

## DSL配置驱动审批流
- 支持通过 data/flow.json 配置节点、分支、并发、审批人等
- 主流程可选择 use_dsl=True 动态生成审批流

---

后续每个模块都配有详细注释和分步讲解，适合循序渐进学习和扩展。 
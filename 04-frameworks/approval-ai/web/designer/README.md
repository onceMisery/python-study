# 审批流可视化设计器（designer）

## 1. 模块简介
本模块基于 React + ReactFlow 实现拖拽式审批流配置，支持节点、分支、并发、审批人等可视化编辑，可导出为DSL（flow.json），并支持流程图预览（Mermaid/ReactFlow）。

## 2. 技术选型
- 前端：React 18.x + ReactFlow
- 流程图预览：Mermaid.js
- 后端：FastAPI（DSL持久化、流程图生成）

## 3. 主要功能
- 拖拽添加/删除/编辑节点（start、approve、risk_eval、branch、merge、end等）
- 节点属性弹窗编辑（审批人、分支条件、AI参数等）
- 连线、分支、合并
- DSL导出/导入，实时生效
- Mermaid流程图一键生成与预览
- 多租户/多业务线切换

## 4. 目录结构
```
designer/
  App.jsx                # 入口，切换编辑/预览
  FlowEditor.jsx         # ReactFlow拖拽与连线
  NodeConfigModal.jsx    # 节点属性弹窗
  dslUtils.js            # DSL与ReactFlow数据互转
  mermaidPreview.jsx     # Mermaid流程图预览
  README.md
```

## 5. 用法说明
- 访问 `/web/edit_flow` 进入设计器页面
- 拖拽节点、连线、编辑属性，实时生成DSL
- 可导入/导出DSL（flow.json）
- 一键预览Mermaid流程图
- 保存后自动同步到后端，审批流实时生效

--- 

## 6. 前后端API联动说明

- 获取当前DSL：`GET /api/flow_dsl`
- 保存DSL：`POST /api/flow_dsl`，参数为DSL对象（JSON）
- 前端可通过fetch/axios等方式调用上述API，实现审批流配置的加载与保存

--- 

## 7. 企业级扩展前端设计建议

- 多租户/多业务线切换：支持租户/业务线下拉选择，自动加载/保存对应DSL
- 权限与安全：前端集成登录鉴权，按角色展示/隐藏编辑、审批等功能
- 流程图美化：自定义节点icon、颜色、分支线条样式，支持导出SVG/PNG
- API安全：所有API调用需带token，支持权限校验与异常处理
- 变更历史：前端支持DSL版本切换、对比、回滚操作入口
- 监控与告警：关键操作、异常、告警可前端弹窗提示或推送

--- 
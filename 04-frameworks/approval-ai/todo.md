# 智能审批流进阶功能 TODO

## 1. 审批流AI风险评估/智能分流
- [x] 设计flow.json DSL，支持risk_eval节点与AI分流
- [x] 实现ai_risk_evaluator.py，封装LLM风险评估与推荐
- [x] flow_engine.py集成AI分流逻辑
- [x] risk_result.json持久化与历史查询
- [x] FastAPI接口：触发评估、获取结果、审批人参考
- [x] 前端risk_result.html展示AI评估与分流建议

## 2. 审批流配置可视化设计器
- [x] 设计器目录结构与README
- [x] edit_flow.html原型页面
- [x] main.js前端入口与伪代码
- [x] 集成React+ReactFlow实现拖拽与节点编辑
- [x] dslUtils.js实现DSL与ReactFlow数据互转
- [x] NodeConfigModal节点属性弹窗
- [x] Mermaid流程图与ReactFlow视图联动
- [x] 后端API支持DSL持久化与流程图生成
- [ ] 完善前端交互与样式
- [ ] 多租户/多业务线支持
- [ ] 权限与安全控制
- [ ] 审批流配置变更历史与回滚
- [ ] 流程图美化与导出SVG/PNG
- [ ] 企业级监控与告警

## 3. 企业级扩展与最佳实践
- [ ] 多租户/多业务线隔离与切换
- [ ] 统一权限认证与细粒度授权
- [ ] DSL变更历史、对比与回滚
- [ ] 流程图美化、导出与归档
- [ ] 审批流监控、异常与告警
- [ ] 关键操作审计与日志
- [ ] CI/CD自动化与灰度发布 
import React, { useState } from 'react';

/**
 * NodeConfigModal.jsx - 节点属性编辑弹窗
 * - 支持编辑节点类型、名称、审批人、分支条件、AI参数等
 * - node: 当前选中节点对象
 * - onClose: 关闭弹窗回调
 * - onSave: 保存节点回调
 */
export default function NodeConfigModal({ node, onClose, onSave }) {
  const [form, setForm] = useState(node.data || {});

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...node, data: form });
  };

  return (
    <div style={{ position: 'fixed', top: 100, left: '50%', transform: 'translateX(-50%)', background: '#fff', border: '1px solid #ccc', padding: 24, zIndex: 1000 }}>
      <h3>编辑节点属性</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label>类型：</label>
          <input name="type" value={form.type || ''} onChange={handleChange} placeholder="如 approve/risk_eval/branch" />
        </div>
        <div>
          <label>名称：</label>
          <input name="name" value={form.name || ''} onChange={handleChange} />
        </div>
        <div>
          <label>审批人：</label>
          <input name="approver" value={form.approver || ''} onChange={handleChange} />
        </div>
        <div>
          <label>分支条件：</label>
          <input name="condition" value={form.condition || ''} onChange={handleChange} placeholder="如 risk == '高'" />
        </div>
        <div>
          <label>AI参数：</label>
          <input name="ai_params" value={form.ai_params || ''} onChange={handleChange} placeholder="如 fields:amount,urgency" />
        </div>
        <div style={{marginTop: 16}}>
          <button type="submit">保存</button>
          <button type="button" onClick={onClose} style={{marginLeft: 12}}>取消</button>
        </div>
      </form>
    </div>
  );
} 
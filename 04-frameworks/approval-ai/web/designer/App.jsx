import React, { useState } from 'react';
import FlowEditor from './FlowEditor';
import MermaidPreview from './mermaidPreview';
import { fetchCurrentDsl, saveCurrentDsl } from './dslUtils';

/**
 * App.jsx - 审批流可视化设计器主入口
 * - 支持编辑模式（拖拽、连线、属性编辑）
 * - 支持流程图预览（Mermaid）
 */
export default function App() {
  const [mode, setMode] = useState('edit'); // 'edit' or 'preview'
  const [dsl, setDsl] = useState(null); // 当前DSL数据

  // 页面加载时自动获取DSL
  React.useEffect(() => {
    fetchCurrentDsl().then(setDsl);
  }, []);

  // 保存DSL时自动调用API
  const handleSaveDsl = async (newDsl) => {
    setDsl(newDsl);
    await saveCurrentDsl(newDsl);
    alert('DSL已保存到后端！');
  };

  return (
    <div>
      <div style={{margin: '16px'}}>
        <button onClick={() => setMode('edit')}>编辑模式</button>
        <button onClick={() => setMode('preview')}>流程图预览</button>
        <button onClick={() => {
          // 导出DSL
          const blob = new Blob([JSON.stringify(dsl, null, 2)], {type: 'application/json'});
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'flow.json';
          a.click();
          URL.revokeObjectURL(url);
        }}>导出DSL</button>
        <input type="file" style={{display:'none'}} id="import-dsl" onChange={e => {
          const file = e.target.files[0];
          if (!file) return;
          const reader = new FileReader();
          reader.onload = evt => {
            try {
              const dsl = JSON.parse(evt.target.result);
              setDsl(dsl);
              alert('DSL导入成功！');
            } catch {
              alert('DSL格式错误');
            }
          };
          reader.readAsText(file);
        }} />
        <button onClick={() => document.getElementById('import-dsl').click()}>导入DSL</button>
      </div>
      {mode === 'edit' && <FlowEditor dsl={dsl} setDsl={handleSaveDsl} />}
      {mode === 'preview' && <MermaidPreview dsl={dsl} />}
    </div>
  );
} 
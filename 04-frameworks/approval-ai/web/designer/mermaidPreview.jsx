import React, { useEffect, useRef } from 'react';

/**
 * MermaidPreview.jsx - DSL流程图预览
 * - dsl: 当前DSL对象
 * - 自动将DSL转为Mermaid字符串并渲染
 */
export default function MermaidPreview({ dsl }) {
  const ref = useRef();

  useEffect(() => {
    if (!dsl || !window.mermaid) return;
    // 简单将DSL转为Mermaid字符串（实际可根据业务完善）
    let mermaidStr = 'graph TD\n';
    if (dsl && dsl.nodes) {
      dsl.nodes.forEach(n => {
        if (n.next) {
          mermaidStr += `${n.id}-->${n.next}\n`;
        }
        if (n.branches) {
          n.branches.forEach(b => {
            mermaidStr += `${n.id}--${b.condition || ''}-->${b.next}\n`;
          });
        }
      });
    }
    ref.current.innerHTML = `<div class='mermaid'>${mermaidStr}</div>`;
    window.mermaid.init(undefined, ref.current);
  }, [dsl]);

  return (
    <div style={{margin:24}}>
      <h3>Mermaid流程图预览</h3>
      <div ref={ref}></div>
    </div>
  );
} 
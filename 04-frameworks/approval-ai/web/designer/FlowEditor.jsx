import React, { useState } from 'react';
import ReactFlow, { addEdge, MiniMap, Controls, Background } from 'reactflow';
import 'reactflow/dist/style.css';
import NodeConfigModal from './NodeConfigModal';
import { dslToFlow, flowToDsl } from './dslUtils';

/**
 * FlowEditor.jsx - 审批流拖拽编辑器
 * - 支持节点拖拽、连线、选中、删除
 * - 支持节点属性弹窗编辑
 * - dsl: 当前DSL对象
 * - setDsl: 更新DSL的函数
 */
export default function FlowEditor({ dsl, setDsl }) {
  // 将DSL转为ReactFlow格式
  const initialFlow = dslToFlow(dsl || {});
  const [nodes, setNodes] = useState(initialFlow.nodes);
  const [edges, setEdges] = useState(initialFlow.edges);
  const [selectedNode, setSelectedNode] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  // 处理节点属性编辑
  const onNodeDoubleClick = (event, node) => {
    setSelectedNode(node);
    setModalOpen(true);
  };

  // 处理连线
  const onConnect = (params) => setEdges(eds => addEdge(params, eds));

  // 处理节点/边变化
  const onNodesChange = (changes) => setNodes(ns => ns.map(n => {
    const change = changes.find(c => c.id === n.id);
    return change ? { ...n, ...change } : n;
  }));
  const onEdgesChange = (changes) => setEdges(es => es.map(e => {
    const change = changes.find(c => c.id === e.id);
    return change ? { ...e, ...change } : e;
  }));

  // 保存为DSL
  const saveDsl = () => {
    const dsl = flowToDsl({ nodes, edges });
    setDsl(dsl);
    alert('DSL已更新！');
  };

  return (
    <div style={{ height: 600, background: '#fff', border: '1px solid #eee', margin: '24px' }}>
      <button onClick={saveDsl}>保存为DSL</button>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeDoubleClick={onNodeDoubleClick}
        fitView
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
      {modalOpen && <NodeConfigModal node={selectedNode} onClose={() => setModalOpen(false)} onSave={newNode => {
        setNodes(ns => ns.map(n => n.id === newNode.id ? newNode : n));
        setModalOpen(false);
      }} />}
    </div>
  );
} 